# ADR-001: Duplicate Issue Detection triggers (`opened` and `edited`)

## Status

Accepted

## Context

The workflow [`.github/workflows/create_issue_comment.yml`](../../.github/workflows/create_issue_comment.yml) runs [`.github/scripts/identify_duplicates.py`](../../.github/scripts/identify_duplicates.py) on GitHub issue events of types **`opened`** and **`edited`**. After refactoring removed unused OpenAI-related code from the script (TF-IDF + cosine similarity only), we need a clear record of why both event types stay enabled.

## Decision

Keep **`issues: opened`** and **`issues: edited`** as workflow triggers. Do not narrow the workflow to `opened` only.

## Rationale

1. **Validation and hygiene:** Maintainers can verify duplicate detection end-to-end by **editing** an issue to add text that overlaps another issue, without opening short-lived test issues for every check.
2. **Behaviour when scope changes:** When someone edits a title or body and the text moves closer to an existing issue, re-running similarity helps surface potential duplicates. The script avoids posting a second “Potential duplicate issues” comment if one already exists on the thread (see `issue_already_has_duplicate_comment` in `identify_duplicates.py`).

## Consequences

- Issue Analyzer ([`issue-analyzer.yml`](../../.github/workflows/issue-analyzer.yml)) is a separate automation; both workflows may react to the same `edited` event for different purposes.
- Documentation for manual validation should prefer the **`edited`** path when possible to reduce noise from disposable issues.

## References

- [WORKFLOW_CONFIGURATION.md](WORKFLOW_CONFIGURATION.md) — Duplicate Issue Detection section
- GitHub issue [#51](https://github.com/pkuppens/my_chat_gpt/issues/51) — validation tracker
