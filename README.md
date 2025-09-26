# Claude Code Setup

A production-ready Claude Code configuration with custom commands, sub-agents, and guides for efficient AI-powered development.

## Quick Start

Install the Claude Code setup in your project:

```bash
npx degit vivmagarwal/claude-code-setup/setup .
```

This will add:
- `.claude/` - Commands, agents, guides, and settings
- `.project-management/` - Directory for engineering plans
- `CLAUDE.md` - Project instructions for Claude

## What's Included

### Custom Commands
- `/presentation:architect` - Create complete presentations from any source
- `/presentation:brand-strategist` - Interactive brand guidelines builder
- `/prd:create-engineering-plan` - Convert requirements to engineering plans
- `/prd:gather-raw-requirements` - Guide for detailed requirements docs
- `/teaching:project-breakdown` - Break complex projects into 10 incremental steps
- `/utils:configure-claude-code` - Configure Claude Code features

### Sub-Agents
- **code-researcher** - Deep codebase analysis
- **web-researcher** - Documentation research

### Guides
- Prompting guide - Write effective Claude prompts
- Notebook guide - Jupyter workflow tips
- Research guides - Code and web investigation

## Philosophy

This setup follows a "simple is better" approach:
- Minimal configuration (empty settings.json by default)
- Clear project instructions without overcomplication
- Focused sub-agents for specific tasks
- Useful automation without unnecessary complexity

## Customization

- Add project-specific commands in `.claude/commands/`
- Create custom agents in `.claude/agents/`
- Update `CLAUDE.md` with your project conventions
- Store engineering plans in `.project-management/`

## Learn More

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview.md)
- [Custom Commands Guide](https://docs.claude.com/en/docs/claude-code/slash-commands)
- [Sub-Agents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)