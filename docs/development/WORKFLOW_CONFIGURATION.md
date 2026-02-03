# AI Issue Review Workflow Configuration Guide

This guide explains how to configure and use the AI-powered issue review workflow in your repository.

## Overview

The issue review workflow (`issue-analyzer.yml`) automatically reviews newly opened or edited GitHub issues using an LLM (Large Language Model). It evaluates:
- Title clarity and quality
- Title/description alignment
- SMART criteria compliance
- Issue structure and completeness

## Prerequisites

### Required
1. **GitHub Repository**: Public or private repository with Actions enabled
2. **OpenAI API Key**: For LLM-based analysis (or other LLM provider)
3. **GitHub Token**: Automatically provided by GitHub Actions

### Optional
- Custom LLM provider (requires code modifications)
- Alternative OpenAI models (configurable)

## Setup Instructions

### Step 1: Configure Repository Secrets

The workflow requires an OpenAI API key to function. Follow these steps:

1. **Get an OpenAI API Key**:
   - Go to https://platform.openai.com/api-keys
   - Create a new API key (if you don't have one)
   - Copy the key (it won't be shown again)

2. **Add the API Key to GitHub Secrets**:
   - Go to your repository on GitHub
   - Navigate to: **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `OPENAI_API_KEY`
   - Value: Paste your OpenAI API key
   - Click **Add secret**

3. **Verify GitHub Token**:
   - `GITHUB_TOKEN` is automatically provided by GitHub Actions
   - No manual configuration needed
   - Permissions are set in the workflow file

### Step 2: Enable GitHub Actions

If GitHub Actions are not already enabled:

1. Go to repository **Settings** → **Actions** → **General**
2. Under "Actions permissions", select:
   - **Allow all actions and reusable workflows** (recommended)
   - Or **Allow local actions only** (if you prefer)
3. Under "Workflow permissions", ensure:
   - **Read and write permissions** are enabled (for posting comments and labels)
   - **Allow GitHub Actions to create and approve pull requests** (optional)

### Step 3: Test the Workflow

1. **Create a Test Issue**:
   - Go to your repository's Issues tab
   - Click **New issue**
   - Use the example from `docs/examples/EXAMPLE_REVERSE_ENGINEERING_ISSUE.md`
   - Or create a simple test issue

2. **Monitor Workflow Execution**:
   - Go to **Actions** tab
   - Look for "Issue Analyzer" workflow
   - Click on the running workflow to see logs
   - Check that all steps complete successfully

3. **Verify Results**:
   - Go back to your test issue
   - You should see:
     - Automated comment with issue analysis
     - Labels added (Type, Priority, Complexity)
     - Review feedback and suggestions

## Configuration Options

### LLM Model Selection

You can configure which OpenAI model to use by editing `.github/workflows/issue-analyzer.yml`:

```yaml
env:
  LLM_MODEL: gpt-4o-mini  # Options: gpt-4o-mini, gpt-4, gpt-3.5-turbo
```

**Model Recommendations**:
- **gpt-4o-mini**: Cost-effective, good for most issues (default)
- **gpt-4**: More expensive, better for complex issues
- **gpt-3.5-turbo**: Fastest and cheapest, less detailed analysis

### Token Limits

Adjust the maximum tokens for longer/shorter responses:

```yaml
env:
  MAX_TOKENS: 4096  # Increase for more detailed analysis
```

### Temperature Setting

Control response creativity/consistency:

```yaml
env:
  TEMPERATURE: 0.1  # Range: 0.0 (deterministic) to 1.0 (creative)
```

**Recommendations**:
- **0.1**: Consistent, factual analysis (default, recommended)
- **0.3-0.5**: Slightly more varied responses
- **0.7+**: More creative, less consistent (not recommended)

## Customizing the Prompt

The system prompt that guides the LLM is located at:
```
SuperPrompt/analyze_issue_system_prompt.txt
```

To customize the review criteria:
1. Edit the prompt file
2. Add or modify review guidelines
3. Test with sample issues
4. Commit changes to apply

The prompt already includes best practices from `docs/development/ISSUE_BEST_PRACTICES.md`.

## Troubleshooting

### Issue: Workflow doesn't run

**Solutions**:
1. Check that GitHub Actions are enabled (Settings → Actions)
2. Verify workflow file has no syntax errors
3. Check that workflow triggers are correct (`on: issues: types: [opened, edited]`)

### Issue: "OpenAI API authentication failed"

**Solutions**:
1. Verify `OPENAI_API_KEY` secret is set correctly
2. Check that API key is valid and has credits
3. Test API key with OpenAI Playground
4. Generate a new API key if needed

### Issue: "Permission denied" or "Cannot post comment"

**Solutions**:
1. Check workflow permissions in `.github/workflows/issue-analyzer.yml`:
   ```yaml
   permissions:
     issues: write
     contents: read
   ```
2. Verify repository Actions permissions (Settings → Actions → General)
3. Check that GITHUB_TOKEN has sufficient permissions

### Issue: Analysis is incomplete or incorrect

**Solutions**:
1. Increase `MAX_TOKENS` in workflow configuration
2. Try a more powerful model (e.g., gpt-4 instead of gpt-4o-mini)
3. Review and improve the system prompt
4. Check OpenAI API status for outages

### Issue: High costs / too many API calls

**Solutions**:
1. Use cheaper model (gpt-4o-mini or gpt-3.5-turbo)
2. Reduce `MAX_TOKENS` limit
3. Consider rate limiting or caching
4. Monitor usage in OpenAI dashboard

## Cost Considerations

Typical costs per issue analysis (approximate):
- **gpt-4o-mini**: $0.001 - $0.01 per issue
- **gpt-4**: $0.05 - $0.20 per issue
- **gpt-3.5-turbo**: $0.0005 - $0.005 per issue

**Cost optimization strategies**:
1. Use gpt-4o-mini for routine issues
2. Set reasonable MAX_TOKENS limits
3. Monitor usage in OpenAI dashboard
4. Consider monthly spending limits

## Security Best Practices

### API Key Security
- ✅ **DO**: Store API keys in GitHub Secrets
- ✅ **DO**: Use repository-specific secrets
- ✅ **DO**: Rotate API keys periodically
- ✅ **DO**: Monitor API usage for anomalies
- ❌ **DON'T**: Commit API keys to code
- ❌ **DON'T**: Share API keys in issues/PRs
- ❌ **DON'T**: Use personal API keys for organization repos

### Workflow Security
- Use pinned versions for GitHub Actions (`@v3`, not `@main`)
- Review workflow changes in pull requests
- Limit workflow permissions to minimum required
- Enable branch protection rules
- Review audit logs periodically

## Advanced Configuration

### Using Alternative LLM Providers

**Note**: This requires code modifications and is left as an open issue.

To support providers other than OpenAI (e.g., Anthropic Claude, Azure OpenAI):
1. Modify `my_chat_gpt_utils/analyze_issue.py`
2. Add provider-specific configuration
3. Update workflow environment variables
4. Add corresponding secrets

### Integration with Copilot Workflow

**Note**: This is a planned enhancement and is currently an open issue.

Potential integration points:
1. Run issue review before Copilot implementation
2. Use review feedback to guide Copilot's work
3. Validate completed work against issue criteria
4. Create automated feedback loop

See: [Open Issues](#open-issues)

## Open Issues

The following items are intentionally left as open issues for future enhancement:

1. **Multiple LLM Provider Support**
   - Currently only supports OpenAI
   - Could add: Anthropic, Azure OpenAI, local models
   - Requires: Provider abstraction layer, configuration updates

2. **Copilot Workflow Integration**
   - Make issue review a step before implementation
   - Pass review feedback to Copilot agent
   - Validate implementation against criteria

3. **Cost Optimization**
   - Implement response caching for similar issues
   - Add rate limiting per user/time period
   - Create cost monitoring dashboard

4. **Enhanced Analytics**
   - Track issue quality trends over time
   - Generate reports on common issues
   - Provide team metrics and insights

5. **Custom Review Templates**
   - Type-specific review prompts (Bug, Feature, Epic)
   - Organization-specific guidelines
   - Dynamic prompt selection based on issue type

## Monitoring and Maintenance

### Regular Tasks

**Weekly**:
- Check workflow run history for failures
- Review OpenAI API usage and costs
- Read user feedback on issue comments

**Monthly**:
- Review prompt effectiveness
- Update prompt based on feedback
- Analyze issue quality trends
- Rotate API keys (security best practice)

**Quarterly**:
- Evaluate model performance (consider upgrades)
- Review and update documentation
- Assess cost vs. value
- Consider enhancements from open issues

## Support and Resources

### Documentation
- [Issue Review Workflow](./ISSUE_REVIEW_WORKFLOW.md) - Architecture and design
- [Issue Best Practices](./ISSUE_BEST_PRACTICES.md) - Writing quality issues
- [Example Issues](../examples/) - Sample issues with expected feedback

### External Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

### Getting Help
1. Check this configuration guide
2. Review troubleshooting section
3. Check workflow run logs in Actions tab
4. Open an issue in the repository
5. Contact repository maintainers

---

*Last Updated: 2026-02-03*
*Version: 1.0*
