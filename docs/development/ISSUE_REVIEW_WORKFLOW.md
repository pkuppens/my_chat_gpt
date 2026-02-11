# GitHub Issue Review Workflow with LLM

## Overview

This document describes the comprehensive AI-powered GitHub issue review workflow that automatically reviews newly opened GitHub issues to ensure quality, clarity, and completeness.

## Current State

The repository already has a functional issue analysis workflow (`issue-analyzer.yml`) that:
- Triggers on issue opened/edited events
- Uses OpenAI GPT-4o-mini for analysis
- Classifies issues by type, priority, and complexity
- Provides review feedback based on SMART criteria
- Adds labels automatically
- Posts analysis as a comment

### Current Workflow Components

1. **Workflow File**: `.github/workflows/issue-analyzer.yml`
2. **Analysis Script**: `.github/scripts/analyze_issue.py`
3. **Core Logic**: `my_chat_gpt_utils/analyze_issue.py`
4. **Prompts**: `SuperPrompt/analyze_issue_system_prompt.txt` and `analyze_issue_user_prompt.txt`
5. **GitHub Integration**: `my_chat_gpt_utils/github_utils.py`

## Requirements Analysis

Based on the issue requirements, the review should evaluate:

### Core Requirements (Already Implemented)
- ✅ **Title Clarity**: Is the title clear and concise?
- ✅ **Title/Description Match**: Do the title and description align?
- ✅ **SMART Criteria**: Is the description Specific, Measurable, Achievable, Relevant, Time-bound?

### Optional Enhancements (Proposed)
- 🔄 **Multi-stage Workflow**: First determine issue type, then apply type-specific review
- 🔄 **Type-specific Reviews**: Different review criteria for bugs vs EPICs vs Subtasks
- 🔄 **Enhanced Feedback**: More detailed suggestions and improvement recommendations

## Workflow Architecture

### Stage 1: Issue Classification (Current)
```yaml
Trigger: Issue Opened/Edited
  ↓
Extract: Title + Body
  ↓
LLM Analysis: Classify Type, Priority, Complexity
  ↓
Output: Classification Labels
```

### Stage 2: Type-Specific Review (Enhanced)
```yaml
Issue Type Determined
  ↓
Apply Type-Specific Prompt
  ↓
- Bug Report: Requires reproduction steps, environment, expected/actual behavior
- Feature Request: Requires use case, acceptance criteria, mockups/examples
- Epic: Requires goals, scope, sub-issues breakdown, timeline
- Task: Requires actionable description, clear deliverables
- Question: Requires context, attempted solutions, specific query
  ↓
Generate Detailed Review
  ↓
Post Comment with Suggestions
```

### Stage 3: Continuous Improvement (Future)
```yaml
Collect Feedback
  ↓
Analyze Issue Lifecycle
  ↓
Improve Prompts and Criteria
```

## Best Practices

### Global GitHub Best Practices

1. **Issue Templates**: Use issue templates to guide users
2. **Labels**: Consistent labeling scheme (Type, Priority, Complexity, Status)
3. **Automation**: Automated workflows reduce manual triage
4. **Feedback Loop**: Comment-based feedback educates users
5. **Timeliness**: Immediate automated review on issue creation

### Project-Specific Best Practices

1. **LLM Configuration**:
   - Use appropriate model (gpt-4o-mini for cost-effective, gpt-4 for complex analysis)
   - Low temperature (0.1) for consistent, deterministic outputs
   - Sufficient max_tokens (4096) for detailed analysis

2. **Prompt Engineering**:
   - Clear, structured prompts with specific instructions
   - Request structured output (JSON/YAML) for easy parsing
   - Include examples and edge cases in prompts

3. **Error Handling**:
   - Graceful degradation when LLM unavailable
   - Clear error messages in issue comments
   - Logging for debugging

4. **Security**:
   - API keys stored as GitHub Secrets
   - Rate limiting awareness
   - No sensitive data in prompts

5. **Cost Management**:
   - Use smaller models for simple tasks
   - Cache common responses
   - Monitor API usage

## Implementation Plan

### Phase 1: Enhanced Review Criteria ✅ (Already Complete)
- Current system already implements all core requirements
- Prompts check title clarity, title/description match, SMART criteria
- Structured YAML response includes all necessary fields

### Phase 2: Multi-Stage Workflow (Optional Enhancement)

#### Option A: Single Workflow with Conditional Logic
```yaml
jobs:
  analyze-issue:
    steps:
      - Classify issue type
      - Load type-specific prompt template
      - Perform type-specific analysis
      - Post combined results
```

#### Option B: Multiple Workflows with Dependencies
```yaml
jobs:
  classify:
    - Determine issue type
    - Add type label

  review:
    needs: classify
    - Load type-specific review criteria
    - Perform detailed review
    - Post feedback
```

#### Recommendation: Option A
- Simpler to maintain
- Faster execution (single job)
- Better user experience (one comprehensive comment)

### Phase 3: Type-Specific Review Templates

Create specialized review criteria for each issue type:

**Bug Report Review:**
- ✓ Reproduction steps provided?
- ✓ Environment details included?
- ✓ Expected vs actual behavior clear?
- ✓ Error messages/logs attached?
- ✓ Screenshots/videos for UI issues?

**Feature Request Review:**
- ✓ Use case clearly described?
- ✓ User story format used?
- ✓ Acceptance criteria defined?
- ✓ Mockups or examples provided?
- ✓ Business value explained?

**Epic Review:**
- ✓ High-level goals defined?
- ✓ Scope clearly bounded?
- ✓ Sub-issues identified?
- ✓ Timeline/milestones included?
- ✓ Dependencies mapped?

**Task Review:**
- ✓ Clear actionable description?
- ✓ Deliverables defined?
- ✓ Acceptance criteria clear?
- ✓ Estimated effort provided?

**Question Review:**
- ✓ Context provided?
- ✓ Attempted solutions mentioned?
- ✓ Specific question asked?
- ✓ Relevant code/examples included?

### Phase 4: Implementation Steps

1. **Create Type-Specific Prompt Templates** (if implementing multi-stage)
   ```
   SuperPrompt/
     analyze_issue_bug_prompt.txt
     analyze_issue_feature_prompt.txt
     analyze_issue_epic_prompt.txt
     analyze_issue_task_prompt.txt
     analyze_issue_question_prompt.txt
   ```

2. **Update Analysis Logic** (if implementing multi-stage)
   - Modify `my_chat_gpt_utils/analyze_issue.py`
   - Add logic to select appropriate prompt based on issue type
   - Enhance `IssueAnalysis` dataclass with type-specific fields

3. **Enhance Workflow** (if implementing multi-stage)
   - Update `.github/workflows/issue-analyzer.yml`
   - Add conditional logic or job dependencies
   - Update environment variables as needed

4. **Update Tests**
   - Add tests for type-specific review logic
   - Update existing tests to cover new scenarios
   - Add integration tests for full workflow

5. **Documentation**
   - Update README with workflow description
   - Add examples of good vs bad issues
   - Document how users can improve their issues

### Phase 5: Testing & Validation

1. **Create Test Issues**
   - One for each issue type
   - Include both good and bad examples
   - Verify workflow triggers correctly

2. **Monitor & Iterate**
   - Collect feedback from issue comments
   - Analyze false positives/negatives
   - Refine prompts based on real-world usage

3. **Performance Testing**
   - Measure API response times
   - Monitor token usage and costs
   - Optimize prompts for efficiency

## Proof of Concept: Software Reverse Engineering Documentation Issue

### Example Issue Template

**Title**: Implement automated YAML/XML documentation generator for software components

**Description**:
Create a software reverse engineering tool that generates YAML/XML documentation for components, classes, and methods by analyzing source code.

**Acceptance Criteria**:
1. Tool can parse Python/Java/JavaScript source code
2. Extracts class names, method signatures, parameters, return types
3. Generates structured YAML or XML documentation
4. Includes docstrings and inline comments in output
5. Supports multiple programming languages
6. Output follows a consistent schema

**Technical Requirements**:
- Use AST (Abstract Syntax Tree) parsing for code analysis
- Support for Python's ast module, Java's JavaParser, or Babel for JS
- Configurable output format (YAML/XML)
- Command-line interface for batch processing
- Unit tests with >80% coverage

**Expected Output Example**:
```yaml
component:
  name: UserAuthentication
  type: class
  methods:
    - name: login
      parameters:
        - username: string
        - password: string
      returns: boolean
      description: Authenticates user credentials
```

**Success Metrics**:
- Successfully parses 100% of valid source files
- Generated documentation matches manual documentation
- Processing time < 1s per file
- Tool is usable by non-technical stakeholders

### Expected Workflow Response

The LLM would analyze this issue and provide:

1. **Classification**:
   - Type: Feature Request / Change Request
   - Priority: Medium
   - Complexity: Moderate to Complex

2. **Review Feedback**:
   - Title: ✓ Clear and specific
   - Description: ✓ Well-structured with acceptance criteria
   - SMART Criteria: ✓ Specific, Measurable, Achievable, Relevant (Time-bound could be added)

3. **Suggestions**:
   - Add estimated timeline (e.g., "Complete within 2 sprints")
   - Specify priority programming languages (e.g., "Start with Python, then expand")
   - Consider adding security review for code parsing
   - Break down into sub-issues: Parser implementation, YAML generator, XML generator, CLI, Tests

4. **Planning**:
   - [ ] Research and select parsing libraries
   - [ ] Design documentation schema
   - [ ] Implement Python parser
   - [ ] Implement YAML output generator
   - [ ] Implement XML output generator
   - [ ] Create CLI interface
   - [ ] Add unit tests
   - [ ] Add integration tests
   - [ ] Write user documentation

## Maintenance & Evolution

### Regular Reviews
- Monthly review of workflow effectiveness
- Quarterly prompt optimization based on feedback
- Annual evaluation of LLM model choice

### Metrics to Track
- Issue quality improvement over time
- Time to first response on issues
- User satisfaction with automated feedback
- False positive/negative rates
- API costs and token usage

### Future Enhancements
- Integration with project management tools (Jira, Linear)
- Automated issue triage and assignment
- Duplicate issue detection (already implemented in create_issue_comment.yml)
- Issue similarity matching for related issues
- Automated sub-issue creation for Epics
- Issue quality scoring and trends

## Conclusion

The current implementation already provides a robust, production-ready issue review workflow that addresses all core requirements. The optional multi-stage enhancements can be implemented incrementally as needed based on:
- User feedback
- Issue quality trends
- Team capacity
- Cost-benefit analysis

The system follows GitHub and AI/LLM best practices, with a focus on:
- Clear, actionable feedback
- Consistent, structured output
- Cost-effective operation
- Maintainable, extensible architecture
- Security and privacy

## References

- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices-for-github-actions)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [SMART Criteria](https://en.wikipedia.org/wiki/SMART_criteria)
- [Issue Template Guidelines](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
