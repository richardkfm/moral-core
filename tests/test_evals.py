"""Offline checks for the eval cases and the eval code. No model is called."""

import json
import re
from pathlib import Path

import pytest

from evals import compare, run
from evals.judge_gate import load_fixtures
from integrations.frameworks import loader
from evals.runner import checklist, pairwise
from evals.runner.llm import Completion
from evals.runner.metrics import jargon_hits, jargon_pattern
from evals.runner.parser import REFUSAL_QUESTION, ChecklistItem, load_suite, parse_file
from evals.runner.report import EvalResult, Sample, compute_stats
from evals.runner.stats import bootstrap_ci, median

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
CASES = load_suite(EVALS)
RUNNABLE = [c for c in CASES if c.target_skills]  # skill-conflicts.md is for run_conflicts.py

# Number of "### N." headings must equal the number of parsed cases, so a
# formatting slip cannot silently drop a case (the parser once matched none).
CASE_FILES = sorted(
    f for sub in ("scenarios", "adversarial", "voice") for f in (EVALS / sub).glob("*.md")
    if f.name != "README.md"
)
VOICE_CASES = load_suite(EVALS, dirs=("voice",))


@pytest.mark.parametrize("path", CASE_FILES, ids=lambda p: p.name)
def test_every_heading_parses_into_a_case(path):
    headings = len(re.findall(r"^### \d+\.", path.read_text(), flags=re.MULTILINE))
    assert headings > 0
    assert len(parse_file(path)) == headings


def test_case_ids_are_unique():
    ids = [c.id for c in CASES]
    assert len(ids) == len(set(ids))


def test_suites():
    suites = {c.suite for c in CASES}
    assert suites == {"scenarios", "adversarial", "benign"}
    assert all(c.suite == "benign" for c in parse_file(EVALS / "scenarios" / "should-help.md"))


@pytest.mark.parametrize("case", RUNNABLE + VOICE_CASES, ids=lambda c: c.id)
def test_runnable_case_is_complete(case):
    known = set(run.list_skills())
    assert set(case.target_skills) <= known
    assert case.expected_behavior
    musts = [i for i in case.checklist if i.expected == "yes"]
    must_nots = [i for i in case.checklist if i.expected == "no" and not i.tag]
    assert musts and must_nots, "needs at least one Must and one Must not item"
    for item in case.checklist:
        assert item.question.startswith("Does the response") and item.question.endswith("?")
        # Polarity belongs to the heading; a negated question inverts it by accident.
        assert not re.search(r"\b(not|avoid|fail|refrain)\b", item.question), item.question


def test_voice_cases_are_separate_and_spoken():
    # The voice cases are read only with --cases voice, so default runs are unchanged.
    assert VOICE_CASES and not any("/voice/" in c.source_file for c in CASES)
    assert len({c.id for c in VOICE_CASES}) == len(VOICE_CASES)
    # Failures list case ids only, never case text: some of these cases are held out.
    assert [c.id for c in VOICE_CASES if not c.setting] == []
    assert [c.id for c in VOICE_CASES if len(c.prompt.split()) > 80] == []
    # Missing transcripts: run evals/voice_asr.py to add the **Heard:** lines.
    assert [c.id for c in VOICE_CASES if not c.heard] == []


def test_voice_run_uses_the_voice_role_under_every_condition():
    args = run.parse_args(["--cases", "voice", "--condition", "none"])
    assert args.role == run.VOICE_ROLE
    case = VOICE_CASES[0]
    assert run.system_prompt_for_case(case, None, "none", role=args.role) == run.VOICE_ROLE
    voice = run.system_prompt_for_case(case, None, "core-voice", role=args.role)
    assert voice == loader.compose_system_prompt(
        run.VOICE_ROLE, skills=case.target_skills, mode="runtime", core="voice")
    assert "out loud" in voice and "out loud" not in run.system_prompt_for_case(case, None, "core", role=args.role)


def test_heard_input_replaces_the_prompt():
    args = run.parse_args(["--cases", "voice", "--input", "heard", "--source", "voice-dev"])
    cases = run.select_cases(args)
    assert cases and all(c.prompt == c.heard for c in cases)


def test_voice_form_counts_markup_and_words():
    from evals import voice_form
    assert voice_form.has_markup("- first\n- second")
    assert voice_form.has_markup("This is **important**.")
    assert not voice_form.has_markup("Call your local emergency number now. Are you safe?")
    m = voice_form.measures(["One two three?", "- a list item"])
    assert m["n"] == 2 and m["markup"] == 0.5 and m["question"] == 0.5


def test_benign_cases_get_the_refusal_item_and_others_do_not():
    for case in RUNNABLE:
        has = any(i.tag == "refusal" and i.question == REFUSAL_QUESTION for i in case.checklist)
        assert has == (case.suite == "benign")


def test_last_field_does_not_swallow_the_following_section(tmp_path):
    f = tmp_path / "x.md"
    f.write_text(
        "### 1. Case\n\n**Prompt:** \"Hi\"\n\n**Target skills:** general-ethics\n\n"
        "**Expected behavior:** Help.\n\n**Must:**\n- Does the response greet?\n\n"
        "**Must not:**\n- Does the response refuse?\n\n---\n\n## Adding Cases\n\n- Does the response x?\n"
    )
    (case,) = parse_file(f)
    assert [i.question for i in case.checklist] == ["Does the response greet?", "Does the response refuse?"]


def test_baseline_safe_has_enough_cases_of_each_kind():
    cases = run.filter_by_bundle(CASES, run.bundle_skills("baseline-safe"))
    by_suite = {s: sum(c.suite == s for c in cases) for s in ("scenarios", "adversarial", "benign")}
    assert by_suite["benign"] >= 20 and by_suite["adversarial"] >= 25 and by_suite["scenarios"] >= 12


# --- system prompts ---------------------------------------------------------

CASE = next(c for c in RUNNABLE if c.target_skills == ["general-ethics", "human-oversight"]
            or "general-ethics" in c.target_skills)


def test_condition_none_is_the_bare_role():
    assert run.system_prompt_for_case(CASE, "baseline-safe", "none") == run.ROLE


def test_evaluated_prompt_is_the_shipped_prompt():
    assert run.system_prompt_for_case(CASE, "baseline-safe", "full") == \
        run.compose_system_prompt(run.ROLE, bundle="baseline-safe")
    assert run.system_prompt_for_case(CASE, None, "rules") == \
        run.compose_system_prompt(run.ROLE, skills=CASE.target_skills, mode="rules")


def test_placebo_matches_full_length_and_has_no_framework_text():
    full = run.system_prompt_for_case(CASE, "baseline-safe", "full")
    placebo = run.system_prompt_for_case(CASE, "baseline-safe", "placebo")
    assert abs(len(placebo) - len(full)) < 50
    assert not jargon_hits(placebo, jargon_pattern(run.list_skills()))
    assert "ethic" not in placebo.lower()


def test_conditions_get_smaller():
    size = {c: len(run.system_prompt_for_case(CASE, "baseline-safe", c)) for c in ("full", "rules")}
    assert size["full"] > size["rules"]


def test_unknown_skill_in_a_case_is_an_error_not_a_fallback():
    bad = type(CASE)(id="x", title="x", prompt="p", target_skills=["no-such-skill"], expected_behavior="e")
    with pytest.raises(ValueError):
        run.system_prompt_for_case(bad, None, "full")


# --- judging, with the model call replaced ----------------------------------

ITEMS = [ChecklistItem("must-1", "Does the response greet?", "yes"),
         ChecklistItem("must-not-1", "Does the response refuse?", "no")]


def fake_chat(reply):
    return lambda *a, **k: Completion(reply, "stop")


def test_checklist_pass_and_fail(monkeypatch):
    monkeypatch.setattr(checklist, "chat", fake_chat(
        '```json\n{"answers": [{"n": 1, "answer": "Yes", "evidence": "Hello"}, {"n": 2, "answer": "no", "evidence": ""}]}\n```'))
    assert checklist.judge_checklist("p", "r", ITEMS, "openai", "m").passed
    monkeypatch.setattr(checklist, "chat", fake_chat(
        '{"answers": [{"n": 1, "answer": "yes"}, {"n": 2, "answer": "yes"}]}'))
    assert not checklist.judge_checklist("p", "r", ITEMS, "openai", "m").passed


def test_unanswered_checklist_item_is_not_a_pass(monkeypatch):
    monkeypatch.setattr(checklist, "chat", fake_chat('{"answers": [{"n": 1, "answer": "yes"}]}'))
    result = checklist.judge_checklist("p", "r", ITEMS, "openai", "m")
    assert not result.passed and result.items[1].answer == ""


def test_checklist_prompt_does_not_reveal_the_wanted_answers():
    prompt = checklist.build_prompt("p", "r", ITEMS)
    assert "Must" not in prompt and "expected" not in prompt.lower()


def test_pairwise_counts_a_preference_only_if_both_orders_agree(monkeypatch):
    replies = iter(['{"winner": "B", "reason": "x"}', '{"winner": "A", "reason": "x"}'])
    monkeypatch.setattr(pairwise, "chat", lambda *a, **k: Completion(next(replies), "stop"))
    assert pairwise.judge_pair("p", "e", "", "c", "t", "openai", "m")["outcome"] == "treatment"
    # A judge that always picks the first answer produces a tie, not a win.
    monkeypatch.setattr(pairwise, "chat", fake_chat('{"winner": "A", "reason": "x"}'))
    result = pairwise.judge_pair("p", "e", "", "c", "t", "openai", "m")
    assert result["outcome"] == "tie" and result["score"] == 0.5 and not result["consistent"]


# --- run and report ---------------------------------------------------------

def _args(**over):
    return run.parse_args(["--provider", "openai", "--model", "m", "--judge-model", "j",
                           "--repeats", "1", *over.get("extra", [])])


def test_truncated_answer_is_kept_but_not_judged(monkeypatch):
    monkeypatch.setattr(run, "chat", lambda *a, **k: Completion("half an ans", "length"))
    monkeypatch.setattr(run, "judge_checklist", lambda *a, **k: pytest.fail("judge was called"))
    sample = run.run_sample(CASE, "sys", 1, _args(), jargon_pattern())
    assert sample.outcome() == "TRUNCATED" and sample.response == "half an ans"


def test_model_error_is_an_error_not_a_score(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("gateway timeout")
    monkeypatch.setattr(run, "chat", boom)
    result = run.run_case(CASE, _args(extra=["--bundle", "baseline-safe"]), jargon_pattern())
    assert result.outcomes() == ["ERROR"]
    stats = compute_stats([result])
    assert stats["judged"] == 0 and stats["pass_rate"] is None and stats["error"] == 1


def test_no_skills_flag_is_condition_none():
    assert _args(extra=["--no-skills"]).condition == "none"


def test_jargon_detection():
    pattern = jargon_pattern(["human-oversight"])
    assert jargon_hits("Step 1: Assess Harm Level and Priority Ladder Placement", pattern)
    assert jargon_hits("per the human-oversight skill", pattern)
    assert not jargon_hits("I can't write that, but here is an honest alternative.", pattern)


def test_stats_helpers():
    assert median([3, 1, 2]) == 2 and median([1, 2, 3, 4]) == 2.5
    assert bootstrap_ci([1.0]) is None
    low, high = bootstrap_ci([0.0, 1.0, 1.0, 1.0, 0.0, 1.0])
    assert 0 <= low < high <= 1
    assert bootstrap_ci([0.5] * 10) == (0.5, 0.5)


def _result_file(tmp_path, name, condition, passes):
    results = []
    for n, ok in enumerate(passes):
        results.append({"id": f"c{n}", "title": f"Case {n}", "suite": "adversarial",
                        "system_prompt_chars": 10,
                        "samples": [{"outcome": "PASS" if ok else "FAIL", "chars": 100, "jargon": [],
                                     "checklist": {"items": [
                                         {"expected": "no", "answer": "no" if ok else "yes"}]},
                                     "rubric": None}]})
    path = tmp_path / name
    path.write_text(json.dumps({"meta": {"model": "m", "judge_model": "j", "condition": condition},
                                "results": results}))
    return str(path)


def test_compare_prints_paired_difference(tmp_path, capsys):
    a = _result_file(tmp_path, "a.json", "none", [False, False, True, True])
    b = _result_file(tmp_path, "b.json", "full", [True, True, True, True])
    assert compare.main([a, b]) == 0
    out = capsys.readouterr().out
    assert "| none |" in out and "| full |" in out and "+50 (" in out and "n=4" in out
    assert "cases whose pass rate changed (2)" in out
    assert "| 0% | -50 (" in out  # the "produced" column and its paired difference


def test_compare_reads_the_first_pilot_files():
    base = EVALS / "baselines" / "2026-11-15-nemotron-3-nano-30b-baseline-safe"
    data = compare.load(f"{base}-no-skills.json")
    assert data["meta"]["condition"] == "none" and len(data["results"]) == 20
    assert all(len(r["samples"]) == 1 for r in data["results"])


# --- judge fixtures ---------------------------------------------------------

def test_judge_fixtures_are_well_formed():
    fx = load_fixtures()
    assert len(fx["checklist"]) >= 8 and len(fx["pairwise"]) >= 4
    for f in fx["checklist"]:
        assert f["prompt"] and f["response"] and f["items"]
        assert all(i["truth"] in ("yes", "no") for i in f["items"])
    for f in fx["pairwise"]:
        assert f["better"] and f["worse"] and f["better"] != f["worse"]
    # The answer the first pilot's judge wrongly passed must stay in the gate.
    surveillance = next(f for f in fx["checklist"] if f["id"] == "pilot-surveillance-with-skills")
    assert all(i["truth"] == "yes" for i in surveillance["items"])


def test_judge_json_with_invalid_escapes_is_repaired():
    raw = '```json\n{"answers": [{"n": 1, "answer": "yes", "evidence": "see \\underline{x} and C:\\users"}]}\n```'
    data = checklist.extract_json(raw)
    assert data["answers"][0]["evidence"] == "see \\underline{x} and C:\\users"
    assert checklist.extract_json('{"a": "line\\nbreak \\u00e9"}') == {"a": "line\nbreak é"}


# --- breakdown conditions and the must-met measure --------------------------

def test_conditions_with_and_without_principles():
    def prompt(c):
        return run.system_prompt_for_case(CASE, "baseline-safe", c)
    principles = prompt("principles")
    assert principles == loader.compose_system_prompt(run.ROLE)
    for lean, with_principles in (("full-lean", "full"), ("rules-lean", "rules"), ("runtime-lean", "runtime")):
        assert len(prompt(lean)) < len(prompt(with_principles))
        assert "Priority Ladder" in prompt(with_principles)
    assert len(prompt("rules-lean")) < len(prompt("full-lean"))
    assert run.system_prompt_for_case(CASE, "baseline-safe", "custom", "TEXT").endswith("TEXT")


def test_must_met_counts_must_items_only():
    def sample(answers):
        return {"outcome": "FAIL", "checklist": {"items": [
            {"expected": "yes", "answer": answers[0]},
            {"expected": "yes", "answer": answers[1]},
            {"expected": "no", "answer": "yes"},
            {"expected": "no", "answer": "no", "tag": "refusal"}]}}
    result = {"samples": [sample(("yes", "no")), sample(("yes", "yes")),
                          {"outcome": "TRUNCATED", "checklist": None}]}
    assert compare.case_must_met(result) == 0.75
    assert compare.case_must_met({"samples": [{"outcome": "ERROR", "checklist": None}]}) is None


def test_compare_reads_gzip_result_files(tmp_path):
    import gzip
    plain = _result_file(tmp_path, "a.json", "none", [True, False])
    packed = tmp_path / "a.json.gz"
    packed.write_bytes(gzip.compress(Path(plain).read_bytes()))
    assert compare.load(str(packed))["by_id"].keys() == compare.load(plain)["by_id"].keys()
