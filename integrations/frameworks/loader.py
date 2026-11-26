"""
moral-core skill loader utility
================================
Reusable helpers for loading ethical skills into any Python-based framework.

Usage:
    from integrations.frameworks.loader import compose_system_prompt, load_bundle, load_skill

All paths resolve relative to the moral-core repo root, so this file can be
copied into your project or used in-place from a git submodule.
"""

from pathlib import Path
import re
import yaml

# Resolve the repo root two levels up from this file:
#   integrations/frameworks/loader.py -> integrations/ -> repo root
MORAL_CORE_PATH = Path(__file__).resolve().parent.parent.parent


def load_principles() -> str:
    """Load PRINCIPLES.md — always include this first when composing prompts."""
    return (MORAL_CORE_PATH / "PRINCIPLES.md").read_text()


def load_core() -> str:
    """Load CORE.md, the short shared text that goes in front of RUNTIME.md files.

    It says how to answer (decline one part and still do the job, work through
    a dilemma, hand a decision to a person, be open about uncertainty). The
    RUNTIME.md files rely on it and are not meant to be loaded without it.
    """
    return (MORAL_CORE_PATH / "CORE.md").read_text().strip()


MODES = ("full", "rules", "runtime")

# Matches the Behavioral Rules section whatever its number: most skills use
# "## 6. Behavioral Rules", eight use "## 5. Behavioral Rules".
_RULES_SECTION = re.compile(
    r"^## (?:\d+\. )?Behavioral Rules[ \t]*\n(.*?)(?=^## |\Z)",
    re.DOTALL | re.MULTILINE,
)


def _resolve_mode(mode: str = None, rules_only: bool = False) -> str:
    if mode is None:
        return "rules" if rules_only else "full"
    if mode not in MODES:
        raise ValueError(f"Unknown mode '{mode}'. Use one of: {', '.join(MODES)}")
    return mode


def load_skill(name: str, rules_only: bool = False, mode: str = None) -> str:
    """
    Load a single skill by directory name (e.g. 'general-ethics').

    Args:
        name:       The skill directory name under skills/.
        rules_only: Shorthand for mode="rules". Kept for existing callers.
        mode:       "full"    - the whole SKILL.md (default)
                    "rules"   - only its Behavioral Rules section
                    "runtime" - the skill's RUNTIME.md, a short behaviour-first
                                version written to be loaded into a model.
                                Only skills that ship a RUNTIME.md support it.

    Returns:
        Skill text as a string.

    Raises:
        FileNotFoundError: the skill, or its RUNTIME.md, does not exist.
        ValueError:        mode="rules" and SKILL.md has no Behavioral Rules
                           section. The loader never falls back to the full
                           text, so a prompt is never silently larger than asked.
    """
    mode = _resolve_mode(mode, rules_only)
    skill_dir = MORAL_CORE_PATH / "skills" / name
    path = skill_dir / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {path}")

    if mode == "runtime":
        runtime_path = skill_dir / "RUNTIME.md"
        if not runtime_path.exists():
            raise FileNotFoundError(
                f"Skill '{name}' has no RUNTIME.md; use mode='rules' or mode='full'"
            )
        return runtime_path.read_text().strip()

    text = path.read_text()
    if mode == "rules":
        match = _RULES_SECTION.search(text)
        if not match:
            raise ValueError(f"No 'Behavioral Rules' section found in {path}")
        return match.group(1).strip()
    return text


def _resolve_shared(mode: str, include_principles, include_core) -> tuple:
    """Defaults: full and rules modes get PRINCIPLES.md, runtime mode gets CORE.md."""
    if include_principles is None:
        include_principles = mode != "runtime"
    if include_core is None:
        include_core = mode == "runtime"
    return include_principles, include_core


def _join_ethics(skill_names: list, mode: str, include_principles=None, include_core=None) -> str:
    include_principles, include_core = _resolve_shared(mode, include_principles, include_core)
    parts = [load_principles()] if include_principles else []
    if include_core:
        parts.append(load_core())
    parts.extend(load_skill(s, mode=mode) for s in skill_names)
    return "\n\n---\n\n".join(parts)


def bundle_skills(bundle_name: str) -> list:
    """Return the list of skill names in a bundle from skills-manifest.yaml."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    bundles = manifest.get("bundles", {})
    if bundle_name not in bundles:
        available = ", ".join(bundles.keys())
        raise ValueError(f"Bundle '{bundle_name}' not found. Available: {available}")
    return list(bundles[bundle_name]["skills"])


def load_bundle(
    bundle_name: str,
    rules_only: bool = False,
    mode: str = None,
    include_principles: bool = None,
    include_core: bool = None,
) -> str:
    """
    Load a pre-built policy bundle from skills-manifest.yaml.

    Call list_bundles() for the available bundle names.

    Args:
        bundle_name:        Bundle key from skills-manifest.yaml.
        rules_only:         Shorthand for mode="rules".
        mode:               "full", "rules" or "runtime" (see load_skill).
        include_principles: Put PRINCIPLES.md first. Default: True for "full"
                            and "rules", False for "runtime".
        include_core:       Put CORE.md in front of the skills. Default: True
                            for "runtime", False otherwise.

    Returns:
        Composed string: the shared text(s) + all skill texts separated by '---'.
    """
    mode = _resolve_mode(mode, rules_only)
    return _join_ethics(bundle_skills(bundle_name), mode, include_principles, include_core)


def compose_system_prompt(
    role: str,
    bundle: str = None,
    skills: list = None,
    rules_only: bool = False,
    mode: str = None,
    include_principles: bool = None,
    include_core: bool = None,
) -> str:
    """
    Compose a full system prompt by combining a role description with ethical skills.

    Provide either `bundle` or `skills`, not both. If neither is provided, only
    PRINCIPLES.md is appended.

    Args:
        role:               Your base system prompt / role description.
        bundle:             Name of a pre-built bundle to load (e.g. 'baseline-safe').
        skills:             List of individual skill names (e.g. ['general-ethics', 'empathy']).
        rules_only:         Shorthand for mode="rules".
        mode:               "full", "rules" or "runtime" (see load_skill).
        include_principles: Put PRINCIPLES.md before the skills. Default: True
                            for "full" and "rules", False for "runtime".
        include_core:       Put CORE.md before the skills. Default: True for
                            "runtime", False otherwise. mode="runtime" with the
                            defaults gives CORE.md + each skill's RUNTIME.md,
                            the compact prompt.

    Returns:
        Complete system prompt string ready for injection.

    Example:
        system = compose_system_prompt(
            role="You are a helpful customer support assistant.",
            bundle="anti-abuse",
        )
    """
    if bundle and skills:
        raise ValueError("Provide either `bundle` or `skills`, not both.")
    mode = _resolve_mode(mode, rules_only)

    if bundle:
        ethics = _join_ethics(bundle_skills(bundle), mode, include_principles, include_core)
    elif skills:
        ethics = _join_ethics(list(skills), mode, include_principles, include_core)
    elif include_core:
        ethics = load_core()
    else:
        ethics = load_principles()

    return f"{role}\n\n## Ethical Framework\n\n{ethics}"


def list_bundles() -> dict:
    """Return a dict of bundle_name -> description from the manifest."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    return {
        name: meta.get("description", "")
        for name, meta in manifest.get("bundles", {}).items()
    }


def list_skills() -> list:
    """Return a list of available skill names from the manifest."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    return [s["name"] for s in manifest.get("skills", [])]
