"""Offline consistency checks for the manifest, the skills and the loader."""

from pathlib import Path

import pytest
import yaml

from integrations.frameworks import loader

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = yaml.safe_load((ROOT / "skills-manifest.yaml").read_text())
SKILLS = [s["name"] for s in MANIFEST["skills"]]
SKILL_FILES = ["SKILL.md", "EXAMPLES.md", "TEST_CASES.md", "MISUSE.md", "NARRATIVES.md"]


def test_manifest_lists_exactly_the_skill_directories():
    on_disk = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
    assert sorted(SKILLS) == on_disk


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_has_all_required_files(skill):
    missing = [f for f in SKILL_FILES if not (ROOT / "skills" / skill / f).exists()]
    assert not missing


def test_bundles_only_name_registered_skills():
    for name, bundle in MANIFEST["bundles"].items():
        unknown = set(bundle["skills"]) - set(SKILLS)
        assert not unknown, f"bundle {name} names unknown skills {unknown}"


def test_skill_bundle_back_references_match_the_bundle_map():
    for skill in MANIFEST["skills"]:
        listed = sorted(skill.get("bundles") or [])
        actual = sorted(b for b, meta in MANIFEST["bundles"].items() if skill["name"] in meta["skills"])
        assert listed == actual, f"{skill['name']}: manifest says {listed}, bundle map says {actual}"


@pytest.mark.parametrize("skill", SKILLS)
def test_rules_mode_returns_a_real_excerpt(skill):
    full = loader.load_skill(skill)
    rules = loader.load_skill(skill, rules_only=True)
    assert 200 < len(rules) < len(full) / 2
    assert rules == loader.load_skill(skill, mode="rules")
    assert "\n## " not in rules  # stops at the next section


def test_rules_mode_raises_instead_of_returning_the_full_text(tmp_path, monkeypatch):
    skill_dir = tmp_path / "skills" / "broken"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Broken\n\n## 1. Purpose\n\nNo rules here.\n")
    monkeypatch.setattr(loader, "MORAL_CORE_PATH", tmp_path)
    with pytest.raises(ValueError):
        loader.load_skill("broken", mode="rules")
    with pytest.raises(FileNotFoundError):
        loader.load_skill("broken", mode="runtime")


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        loader.load_skill("general-ethics", mode="tiny")


def test_bundle_sizes_shrink_with_mode():
    full = loader.load_bundle("baseline-safe")
    rules = loader.load_bundle("baseline-safe", rules_only=True)
    lean = loader.load_bundle("baseline-safe", mode="rules", include_principles=False)
    assert len(full) > len(rules) > len(lean)
    assert full.startswith(loader.load_principles())
    assert not lean.startswith(loader.load_principles()[:200])


def test_compose_system_prompt_keeps_role_first_and_rejects_both_selectors():
    prompt = loader.compose_system_prompt("ROLE TEXT", bundle="baseline-safe", mode="rules")
    assert prompt.startswith("ROLE TEXT\n\n## Ethical Framework\n\n")
    with pytest.raises(ValueError):
        loader.compose_system_prompt("x", bundle="baseline-safe", skills=["empathy"])


def test_runtime_files_are_short_and_do_not_ask_to_be_cited():
    for path in (ROOT / "skills").glob("*/RUNTIME.md"):
        words = len(path.read_text().split())
        assert 100 <= words <= 480, f"{path}: {words} words"


def test_runtime_mode_puts_the_core_first_and_leaves_principles_out():
    core = loader.load_core()
    assert 400 <= len(core.split()) <= 1100
    runtime = loader.load_bundle("baseline-safe", mode="runtime")
    assert runtime.startswith(core)
    assert loader.load_principles()[:200] not in runtime
    one = loader.compose_system_prompt("ROLE", skills=["human-oversight"], mode="runtime")
    assert core in one and loader.load_skill("human-oversight", mode="runtime") in one
    assert len(one) < len(runtime)
    # the older combinations stay available
    lean = loader.load_bundle("baseline-safe", mode="runtime", include_core=False)
    assert core not in lean
    both = loader.load_bundle("baseline-safe", mode="runtime", include_principles=True, include_core=False)
    assert both.startswith(loader.load_principles())
    assert core not in loader.load_bundle("baseline-safe")


def test_core_and_runtime_files_do_not_name_the_framework():
    texts = [ROOT / "CORE.md", ROOT / "CORE-voice.md", *(ROOT / "skills").glob("*/RUNTIME.md")]
    for path in texts:
        text = path.read_text()
        for word in ("PRINCIPLES.md", "Priority Ladder", "moral-core", "SKILL.md"):
            assert word not in text, f"{path} names {word}"


def test_voice_core_is_short_and_loads_in_place_of_core():
    voice = (ROOT / "CORE-voice.md").read_text()
    assert len(voice.split()) <= 950
    prompt = loader.compose_system_prompt("ROLE", skills=["empathy"], mode="runtime", core="voice")
    assert loader.load_core("voice") in prompt and loader.load_core() not in prompt
    assert loader.load_skill("empathy", mode="runtime") in prompt
    with pytest.raises(ValueError):
        loader.load_core("video")


def test_version_badge_matches_version_json():
    import json
    version = json.loads((ROOT / "version.json").read_text())["version"]
    assert f"version-{version}-" in (ROOT / "README.md").read_text()
