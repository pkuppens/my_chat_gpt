"""Unit tests for my_chat_gpt_utils.prompts."""

import os
import tempfile

from my_chat_gpt_utils.prompts import (
    DocumentationPrompt,
    IssueAnalysisPrompt,
    PlaceholderDict,
    get_documentation_prompt,
    load_analyze_issue_prompt,
)


def test_placeholder_dict_returns_braced_key_for_missing():
    """PlaceholderDict should not raise KeyError; missing keys become {key} strings."""

    d = PlaceholderDict({"a": "1"})
    assert d["a"] == "1"
    assert d["missing"] == "{missing}"


def test_load_analyze_issue_prompt_injects_issue_types_and_priority_levels():
    """Standard lists are filled when omitted."""

    system, user = load_analyze_issue_prompt(
        {"issue_title": "T", "issue_body": "B"},
    )
    assert isinstance(system, str) and len(system) > 0
    assert isinstance(user, str)
    assert "T" in user


def test_load_analyze_issue_prompt_with_temp_superprompt_files():
    """load_analyze_issue_prompt reads SuperPrompt/*.txt relative to cwd."""

    with tempfile.TemporaryDirectory() as tmpdir:
        sp = os.path.join(tmpdir, "SuperPrompt")
        os.makedirs(sp)
        with open(os.path.join(sp, "analyze_issue_system_prompt.txt"), "w", encoding="utf-8") as f:
            f.write("SYS {issue_types}")
        with open(os.path.join(sp, "analyze_issue_user_prompt.txt"), "w", encoding="utf-8") as f:
            f.write("USR {issue_title}")

        old = os.getcwd()
        try:
            os.chdir(tmpdir)
            system, user = load_analyze_issue_prompt({"issue_title": "Hello"})
            assert "SYS" in system
            assert "Hello" in user
        finally:
            os.chdir(old)


def test_get_documentation_prompt_includes_fields():
    """Documentation prompt includes title, description, and type from item."""

    text = get_documentation_prompt({"title": "A", "description": "B", "type": "C"})
    assert "A" in text and "B" in text and "C" in text


def test_documentation_prompt_get_prompt_static():
    """DocumentationPrompt.get_prompt matches helper behaviour."""

    item = {"title": "x", "description": "y", "type": "z"}
    assert DocumentationPrompt.get_prompt(item) == get_documentation_prompt(item)


def test_issue_analysis_prompt_get_system_prompt_fallback(tmp_path, monkeypatch):
    """When prompt file is missing, get_system_prompt returns embedded fallback."""

    monkeypatch.chdir(tmp_path)
    p = IssueAnalysisPrompt("Bug", "High", "Title text", "Body text")
    p.system_prompt_file = "nonexistent/path/prompt.txt"
    out = p.get_system_prompt()
    assert "Title text" in out
    assert "Body text" in out
