# Deployment & Publishing Guide

This guide explains how to publish the diagram-spec-kit to GitHub and make it available to your team.

## Pre-Publication Checklist

- [ ] README.md created ✅
- [ ] CONTRIBUTING.md created ✅
- [ ] GLOBAL-INSTALL.md updated ✅
- [ ] diagram-orchestrator.agent.md finalized ✅
- [ ] All test diagrams pass linter ✅
- [ ] .gitignore configured ✅
- [ ] Scripts tested locally ✅
- [ ] License file added
- [ ] GitHub org/repo ready

## Step 1: Create GitHub Repository

```bash
# Create new repo on github.com
# Repo name: diagram-spec-kit
# Description: "AI-powered Mermaid diagram generation with automatic validation and approval"
# Visibility: Public (for easy agent installation)
# Add .gitignore: Python (already configured)
# License: Choose one (e.g., MIT, Apache 2.0)
```

## Step 2: Push Local Code to GitHub

```bash
cd c:\Users\069109\Dev\diagram-spec-kit

# Initialize git (if not already done)
git init

# Add remote
git remote add origin https://github.com/thomas-leung-avnet/diagram-spec-kit.git

# Stage all files
git add .

# Initial commit
git commit -m "Initial commit: diagram orchestration framework

- Master orchestrator agent for end-to-end pipeline
- Syntax validation with Mermaid parse error prevention
- Python linter for naming, complexity, spec compliance
- GitHub Actions CI/CD for PR enforcement
- VS Code tasks for local validation
- Global installation support for cross-project use
- 5-step workflow: normalize → generate → validate → review → approve"

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Update Installation URLs

Edit `GLOBAL-INSTALL.md` and `README.md` to replace placeholder URLs:

```bash
# Find and replace all instances of:
# thomas-leung-avnet → your actual GitHub organization
# diagram-spec-kit → repository name

# Example:
# Before: https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/...
# After:  https://raw.githubusercontent.com/acme-corp/diagram-spec-kit/main/...
```

## Step 4: Create GitHub Releases (Optional)

For users to find installation scripts:

```bash
# Create a release tag
git tag -a v1.0.0 -m "Initial release: Diagram Orchestration Framework

Features:
- Master orchestrator agent (5-step pipeline)
- Syntax validation (80+ patterns)
- Python linter with customizable rules
- GitHub Actions enforcement
- Global VS Code installation
- Multi-diagram support (flowchart, sequence)

Installation: See GLOBAL-INSTALL.md"

git push origin v1.0.0
```

Then on GitHub:
1. Go to Releases
2. Create release from tag v1.0.0
3. Add release notes (copy from tag message)
4. Attach any artifacts (optional)

## Step 5: Documentation Updates

### Update README with Real URLs

```markdown
# Global Installation (Recommended)
Install once, use the orchestrator agent on any project.

```powershell
# Windows
powershell -ExecutionPolicy Bypass -Command "iex (irm 'https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/scripts/GLOBAL-INSTALL.ps1')"
```

### Update GLOBAL-INSTALL.md with Real URLs

All `https://raw.githubusercontent.com/...` URLs must point to your actual repo.

## Step 6: Make Agent Discoverable

### Option A: VS Code Marketplace (Manual Discovery)
Users will find the agent when they:
1. Clone/download the repo
2. Open `global/diagram-orchestrator.agent.md`
3. Install to their prompts folder (manual)

### Option B: Workspace Installation (Shared Teams)
For teams sharing a VS Code workspace:

1. Create `.vscode/settings.json` in your repo:
   ```json
   {
     "github.copilot.chat.prompts.folder": "./.copilot-prompts"
   }
   ```

2. Users who open this workspace get automatic access to prompts in `.copilot-prompts/`

### Option C: Corporate Distribution (Best for Large Teams)
1. Host agent files on internal server
2. Share installation script that pulls from internal URLs
3. Automatically installed during onboarding

## Step 7: Announce to Team

### Slack/Teams Message Template

```
🎉 New: Diagram Standardization Kit

Generate production-ready architecture & sequence diagrams in one command.

✨ Features:
• AI-powered orchestrator agent (auto-validates, reviews, approves)
• No syntax errors (catches <br> in sequences, dashes, unquoted labels)
• Linter enforcement (kebab-case, 15-node limit, required sections)
• CI/CD integration (GitHub Actions, PR blocking)
• Works on any project (fallback standards if no rules exist)

🚀 Quick Start:
1. Install globally: powershell -ExecutionPolicy Bypass -Command "iex (irm 'https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/scripts/GLOBAL-INSTALL.ps1')"
2. Open VS Code Chat: @diagram-orchestrator
3. Paste your intent: "Create sequence diagram for..."
4. Agent handles everything ✅

📚 Learn more: https://github.com/thomas-leung-avnet/diagram-spec-kit

Questions? See CONTRIBUTING.md or open an issue.
```

## Step 8: Monitor Usage

### Track Adoption
- Watch GitHub stars/watchers
- Check clone counts (GitHub Insights)
- Monitor issues/discussions
- Track PR contributions

### Collect Feedback
- Add GitHub Discussions tab for Q&A
- Create issue template for bugs/features
- Monthly team sync: "How's the diagram workflow?"

## Maintenance

### Regular Updates
- Test new Mermaid versions
- Update syntax validation patterns
- Fix reported issues within 1 week
- Update documentation with new patterns

### Version Bumps
- **Patch (v1.0.1):** Bug fixes, syntax pattern updates
- **Minor (v1.1.0):** New features, new diagram types, new agents
- **Major (v2.0.0):** Breaking changes to workflow or API

### Communication
- Tag releases in GitHub
- Update CHANGELOG.md
- Announce in team channels
- Update installation instructions if URLs change

## Troubleshooting

### "Installation script not found"
- Verify raw.githubusercontent.com URL is correct
- Check script exists in `scripts/` folder
- Verify GitHub repo is public

### "Agent doesn't appear in VS Code"
- User may need to restart VS Code
- Check installation folder: `%APPDATA%\Code\User\prompts\`
- Verify file permissions

### "Diagram generated but CI/CD blocks it"
- If user doesn't have project files, CI won't run
- Direct them to: [CONTRIBUTING.md](CONTRIBUTING.md)
- Or: Add project files to their repo

## Next Steps

1. ✅ Create GitHub repo
2. ✅ Push code
3. ✅ Update URLs
4. ✅ Create release (optional)
5. ✅ Announce to team
6. ✅ Collect feedback
7. ✅ Iterate and improve

---

**Questions?** See [README.md](README.md), [GLOBAL-INSTALL.md](GLOBAL-INSTALL.md), or [CONTRIBUTING.md](CONTRIBUTING.md).
