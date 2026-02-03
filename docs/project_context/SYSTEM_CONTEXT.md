# Project Context for AI Agents

**Last Updated**: February 2026  
**Purpose**: Provide persistent context for AI agents analyzing issues and making recommendations

---

## Project Identity

- **Name**: my_chat_gpt
- **Purpose**: AI-powered GitHub issue automation and LLM utilities collection
- **Primary Language**: Python 3.12+
- **Development Approach**: Experimental AI-first development with emphasis on agentic workflows
- **Repository**: pkuppens/my_chat_gpt

---

## Architecture Overview

### Core Components

1. **Issue Analyzer**: Automatically reviews GitHub issues for quality
   - Model: GPT-4o-mini (cost-effective)
   - Workflow: `.github/workflows/issue-analyzer.yml`
   - Logic: `my_chat_gpt_utils/analyze_issue.py`

2. **Duplicate Detector**: Finds similar issues using embeddings
   - Workflow: `.github/workflows/create-issue-comment.yml`
   - Uses: scikit-learn, PyGithub

3. **Review Workflow**: Posts structured feedback on new issues
   - SMART criteria evaluation
   - Type-specific guidance (Bug, Feature, Epic, Task)
   - Automated label application

---

## Technology Stack

### Core Dependencies
- **Python**: 3.12+ (primary language)
- **OpenAI**: GPT-4o-mini for LLM calls
- **PyGithub**: GitHub API integration
- **pytest**: Testing framework
- **Ruff + Black**: Code formatting and linting

### Package Management
- **UV**: Primary package manager (fast, modern)
- **pip**: Fallback for compatibility

---

## Conventions & Standards

### Issue Labels (Auto-Applied)
- **Type**: Bug Fix, Feature Request, Epic, Change Request, Task, Question, Discussion
- **Priority**: Critical, High, Medium, Low
- **Complexity**: Simple, Moderate, Complex

### Code Quality Requirements
- **Test Coverage**: >80% for new code
- **Linting**: Ruff and Black passing
- **Type Hints**: Required for public functions
- **Documentation**: Docstrings for modules, classes, functions

---

## Recent Architectural Decisions

### ADR 001: Use GPT-4o-mini for Issue Analysis (2024-11)
**Decision**: Use GPT-4o-mini as primary model  
**Rationale**: 10x cost reduction, sufficient quality for structured tasks  
**Status**: Active

### ADR 002: Cloud-First Strategy (2024-09)
**Decision**: Focus on cloud APIs (OpenAI) rather than local models  
**Rationale**: Simplicity, reliability, lower maintenance  
**Status**: Active

---

## Out of Scope (Explicitly Excluded)

- ❌ **Local LLM Deployment**: Adds complexity, hardware requirements (see ADR 002)
- ❌ **Multi-Repository Management**: Focus on single-repo workflows
- ❌ **Real-Time Chat Interfaces**: Emphasis on automation, not interactive chat

---

## User Preferences (Defaults)

### Language Preferences
- **Primary**: Python 3.12+
- **Framework**: FastAPI (Python)
- **Testing**: pytest
- **Coding Style**: Black + Ruff

---

**Note for AI Agents**: This context should inform your analysis. Check alignment with architecture, reference ADRs if issues conflict with past decisions, and respect out-of-scope boundaries.
