# GitHub Issue Best Practices

This guide outlines best practices for creating high-quality GitHub issues that are clear, actionable, and effective for project management and collaboration.

## Why Good Issues Matter

Well-written issues:
- **Save time**: Clear issues reduce back-and-forth clarification
- **Improve collaboration**: Team members can understand and act on issues quickly
- **Enable automation**: Structured issues work better with AI tools and workflows
- **Track progress**: Clear success criteria make it easy to know when work is complete
- **Document decisions**: Good issues serve as historical record of project evolution

## Global Best Practices

These are universal best practices from the GitHub community and software development industry:

### 1. Write Clear, Descriptive Titles

**Good Examples:**
- ✅ "Add user authentication to API endpoints"
- ✅ "Fix memory leak in background worker process"
- ✅ "Update documentation for deployment procedure"

**Bad Examples:**
- ❌ "Bug" (too vague)
- ❌ "This doesn't work" (no context)
- ❌ "Question about the thing" (unclear)

**Guidelines:**
- Keep titles under 80 characters
- Use action verbs (Add, Fix, Update, Remove, Implement)
- Be specific about what component or feature is affected
- Avoid jargon or internal abbreviations

### 2. Follow the SMART Framework

Make your issues **SMART**:

**Specific**: Clear and unambiguous
- ❌ "Improve performance"
- ✅ "Reduce API response time for user search from 500ms to 200ms"

**Measurable**: Has concrete success criteria
- ❌ "Make the UI better"
- ✅ "Increase user satisfaction score from 3.5 to 4.0 on post-release survey"

**Achievable**: Realistic given resources and constraints
- ❌ "Rewrite entire application in new framework this week"
- ✅ "Migrate authentication module to new framework (estimated 2 sprints)"

**Relevant**: Aligned with project goals
- Link to project objectives, user needs, or business requirements
- Explain why this issue matters

**Time-bound**: Has target completion timeframe
- ❌ "Eventually implement caching"
- ✅ "Implement Redis caching for user sessions by end of Q2"

### 3. Structure Your Description

Use this recommended structure:

```markdown
## Problem Statement
[What problem are we solving? Why does it matter?]

## Proposed Solution
[How will we solve it? What approach will we take?]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Details
[Implementation notes, architecture decisions, constraints]

## Success Metrics
[How will we measure success?]

## Dependencies
[What needs to happen first? What blocks this?]

## Related Issues
[Links to related issues or PRs]
```

### 4. Use Issue Templates

Create and use issue templates for consistency:
- Bug report template
- Feature request template
- Epic/large initiative template
- Question/discussion template

Templates ensure all necessary information is provided upfront.

### 5. Label Appropriately

Use labels to categorize and prioritize:
- **Type**: Bug, Feature, Enhancement, Documentation, Question
- **Priority**: Critical, High, Medium, Low
- **Status**: To Do, In Progress, Blocked, Review
- **Area**: Frontend, Backend, Database, DevOps, etc.

### 6. Assign and Track

- Assign issues to specific people when work begins
- Use milestones to group related issues
- Link issues to projects for better organization
- Update issues as work progresses

## Project-Specific Best Practices

These best practices are specific to the my_chat_gpt project:

### 1. AI Review Workflow

This project uses an automated AI review workflow that:
- Analyzes every new issue
- Checks for clarity, completeness, and SMART criteria
- Suggests improvements and next steps
- Adds appropriate labels automatically

**To get the most from the AI review:**
- Provide as much detail as possible upfront
- Use the recommended structure above
- Review and address AI feedback promptly
- Iterate on the issue based on suggestions

### 2. Issue Types in This Project

This project uses these issue types:

**Epic**: Large initiatives spanning multiple issues
- Should include: Goals, scope, breakdown into sub-issues, timeline
- Example: "Implement comprehensive user management system"

**Change Request**: Significant feature additions or modifications
- Should include: Problem statement, proposed solution, acceptance criteria
- Example: "Add OAuth2 authentication support"

**Bug Fix**: Corrections to existing functionality
- Should include: Reproduction steps, expected vs actual behavior, environment
- Example: "Fix login failure with special characters in password"

**Task**: Concrete, actionable work items
- Should include: Clear description, deliverables, definition of done
- Example: "Update README with new installation instructions"

**Question**: Requests for clarification or discussion
- Should include: Context, what you've tried, specific questions
- Example: "How should we handle rate limiting for API endpoints?"

### 3. Integration with Development Workflow

Issues in this project integrate with:
- **Pre-commit hooks**: Code quality checks before commits
- **CI/CD pipelines**: Automated testing and deployment
- **Documentation**: Auto-generated docs from docstrings
- **Code review**: AI-powered code review on PRs

**Best practices:**
- Reference issue numbers in commit messages (e.g., "Fix #123")
- Link PRs to issues using keywords (e.g., "Closes #123", "Fixes #123")
- Update issue status as work progresses
- Comment on issues with progress updates

### 4. Documentation Requirements

For issues involving code changes:
- Update relevant docstrings
- Update user-facing documentation
- Add examples if applicable
- Update CHANGELOG

For issues involving new features:
- Create usage examples
- Document configuration options
- Add to API reference if applicable

### 5. Testing Requirements

All issues involving code changes must include:
- Unit tests (target: >80% coverage)
- Integration tests where applicable
- Manual testing checklist
- Performance testing for critical paths

## Issue Type-Specific Guidelines

### Bug Reports

**Required Information:**
```markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: [e.g., macOS 12.0, Ubuntu 22.04]
- Python Version: [e.g., 3.11.0]
- Package Version: [e.g., 1.2.3]

## Error Messages
```
[Full error traceback]
```

## Additional Context
[Screenshots, logs, related issues]
```

### Feature Requests

**Required Information:**
```markdown
## Feature Description
[What feature do you want?]

## Use Case
[Why do you need this feature? Who benefits?]

## Proposed Solution
[How should it work?]

## Alternative Solutions
[What alternatives have you considered?]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Success Metrics
[How will we measure success?]
```

### Epics

**Required Information:**
```markdown
## Vision
[High-level goal and why it matters]

## Scope
[What's included and what's not]

## Sub-Issues
- [ ] #123 - First task
- [ ] #124 - Second task
- [ ] #125 - Third task

## Timeline
[Estimated schedule and milestones]

## Dependencies
[What needs to happen first]

## Success Criteria
[How will we know we've succeeded?]

## Risks
[Potential problems and mitigation strategies]
```

## Common Mistakes to Avoid

### ❌ Don't

1. **Be vague**: "The app is broken" → Instead: "Login fails with 500 error when using Gmail OAuth"
2. **Skip reproduction steps**: Makes bugs hard to fix
3. **Create duplicate issues**: Search first to see if issue exists
4. **Mix multiple issues**: One issue per problem/feature
5. **Forget to update**: Keep issues current as work progresses
6. **Leave issues orphaned**: Close completed issues, update blocked ones
7. **Use unclear language**: Write for someone unfamiliar with your context
8. **Skip testing criteria**: How will reviewers verify the fix?

### ✅ Do

1. **Be specific**: Provide exact error messages, versions, steps
2. **Provide context**: Explain why this matters and what you've tried
3. **Use checklists**: Break complex issues into smaller tasks
4. **Link related items**: Connect to relevant issues, PRs, docs
5. **Update regularly**: Comment with progress, blockers, questions
6. **Close promptly**: Mark issues done when complete
7. **Write for others**: Assume reader has no prior context
8. **Define success**: Be clear about what "done" means

## Tools and Automation

### This Project's AI Tools

1. **Issue Analyzer**: Automatically reviews new issues
   - Checks SMART criteria
   - Suggests improvements
   - Adds labels
   - Posts feedback comment

2. **Duplicate Detector**: Finds similar existing issues
   - Uses ML similarity matching
   - Prevents duplicate work
   - Links related issues

3. **Code Review Bot**: Reviews pull requests
   - Checks code quality
   - Suggests improvements
   - Runs automated tests

### Using AI Feedback Effectively

When you receive AI feedback on an issue:
1. **Read carefully**: AI suggestions are often helpful
2. **Address valid points**: Update issue based on feedback
3. **Ask questions**: Comment if feedback is unclear
4. **Iterate**: AI learns from good examples
5. **Don't blindly accept**: Use judgment - AI isn't perfect

## Examples

See the [examples directory](../examples/) for:
- Well-structured issue examples
- Expected AI review feedback
- Common patterns and templates
- Test cases for the AI workflow

## References

### GitHub Official Documentation
- [Mastering Issues](https://guides.github.com/features/issues/)
- [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)
- [Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)

### Industry Best Practices
- [Wired: How to File a Good Bug Report](https://www.wired.com/story/how-to-write-good-bug-report/)
- [Mozilla: Bug Writing Guidelines](https://developer.mozilla.org/en-US/docs/Mozilla/QA/Bug_writing_guidelines)
- [SMART Criteria](https://en.wikipedia.org/wiki/SMART_criteria)

### Project-Specific Documentation
- [Issue Review Workflow](./ISSUE_REVIEW_WORKFLOW.md)
- [Example Issues](../examples/)
- [GitHub Workflows](../GITHUB.md)

---

*Last Updated: 2026-02-03*
*Maintained by: my_chat_gpt project team*
