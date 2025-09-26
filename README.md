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
- `/prd:create-engineering-plan` - Convert product requirements into actionable engineering plans
- `/prd:gather-raw-requirements` - Guide creation of detailed product requirements
- `/teaching:create-teaching-plan` - Transform projects into 10-step teaching journeys
- `/utils:configure-claude-code` - Configure Claude Code features

### Sub-Agents
- **code-researcher** - Deep codebase analysis specialist
- **web-researcher** - Documentation and technical research specialist

### Guides
- Prompting guide for effective Claude interactions
- Notebook guide for Jupyter workflows
- Research guides for code and web investigation

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