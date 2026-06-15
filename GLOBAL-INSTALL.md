# Global Installation Guide

Install the diagram orchestrator agent **once** and use it on any project. No per-project setup required.

## What You Get (Global)

✅ **Diagram Orchestrator Agent** — Full pipeline (generate → validate → review → approve)
✅ **Any Project** — Works on repos with or without diagram-spec files
✅ **Fallback Standards** — Built-in v1 profile if project rules not found
✅ **No Syntax Errors** — Pre-lint validation catches common mistakes
❌ **No CI/CD** — CI/CD is per-project (add separately if you want merge gates)
❌ **No PR Templates** — PR templates are per-project

## Prerequisites

- VS Code installed
- Copilot Chat extension (free account required)
- PowerShell (Windows) or Bash (Mac/Linux)
- Python 3.8+ (if validating locally—optional)

## Installation (One Command)

### Windows
```powershell
# Copy & paste this entire line into PowerShell
powershell -ExecutionPolicy Bypass -Command "iex (irm 'https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/scripts/GLOBAL-INSTALL.ps1')"
```

### Mac / Linux
```bash
# Copy & paste this into Terminal
curl -sSL https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/scripts/GLOBAL-INSTALL.sh | bash
```

**What it does:**
- Downloads `diagram-orchestrator.agent.md` from this repo
- Copies to your VS Code user prompts folder
- Creates backup of any existing file
- Verifies installation

**Installation folder:**
- Windows: `%APPDATA%\Code\User\prompts\diagram-orchestrator.agent.md`
- Mac: `~/.config/Code/User/prompts/diagram-orchestrator.agent.md`
- Linux: `~/.config/Code/User/prompts/diagram-orchestrator.agent.md`

## Quick Start (After Install)

### In Any Project

1. **Open VS Code Chat**
   ```
   Ctrl+I (Windows/Linux) or Cmd+I (Mac)
   ```

2. **Select orchestrator agent**
   ```
   Type: @diagram-orchestrator
   Or select from dropdown if visible
   ```

3. **Paste your diagram intent**
   ```
   Create sequence diagram for payment processing.
   Goal: show interaction between client, gateway, processor.
   Scope: payment initiation through settlement.
   Audience: developers.
   Key nodes: client, gateway, processor.
   Error cases: declined card, expired card, timeout.
   ```

4. **Agent executes full pipeline**
   - ✅ Normalizes intent
   - ✅ Generates Mermaid
   - ✅ Validates syntax
   - ✅ Lints spec compliance
   - ✅ Reviews clarity
   - ✅ Approves for PR or reports issues

5. **Agent reports final verdict**
   ```
   === DIAGRAM ORCHESTRATOR FINAL REPORT ===
   Diagram File: docs/diagrams/payment-processing-flow.mmd
   
   Step 1 - Intent: ✅ NORMALIZED
   Step 2 - Generation: ✅ CREATED
   Step 3 - Lint Verdict: ✅ PASS
   Step 4 - Clarity Verdict: ✅ CLEAR
   Step 5 - Merge Gate: ✅ READY FOR PR
   ```

6. **Commit diagram**
   ```bash
   git add docs/diagrams/payment-processing-flow.mmd
   git commit -m "Add payment processing flow diagram"
   git push
   ```

## Usage Scenarios

### Scenario 1: Project Has No Diagram Rules
✅ Agent uses **fallback v1 profile**
- Diagram type: flowchart LR or sequenceDiagram
- Node limit: 15
- Naming: kebab-case
- Required: title, legend, scope, main flow, error flow

### Scenario 2: Project Has diagram-spec.yaml
✅ Agent uses **project-specific rules**
- Respects custom node limits, naming patterns, forbidden labels
- Falls back to v1 for missing rules

### Scenario 3: Project Has No docs/diagrams/ Folder
✅ Agent **creates it automatically**
- Diagram saved to `docs/diagrams/<topic>.mmd`
- Follows project folder structure if present

### Scenario 4: You Want to Validate Locally
✅ Use **Python linter** (optional)
```bash
py -3 scripts/diagram_lint.py
# Output: PASS or FAIL with violations
```

## Troubleshooting

### "Can't find @diagram-orchestrator"
- Restart VS Code
- Check installation folder (see above)
- Try typing `@diagram` to see options
- Or manually paste full file path if needed

### "Agent generates diagram but reports errors"
- Agent has Step 2.5 syntax validation—most caught automatically
- If linter fails: Run `py -3 scripts/diagram_lint.py` locally to debug
- See [Common Issues](README.md#-common-issues) for specific fixes

### "I want CI/CD enforcement too"
- Add per-project files to your repo:
  - `.github/workflows/diagram-lint.yml`
  - `.vscode/tasks.json`
  - `diagram-spec.yaml`
- See [CONTRIBUTING.md](CONTRIBUTING.md) for project setup

### "Orchestrator not generating files in my project"
- Check that VS Code workspace is open to your project root
- Check that `docs/diagrams/` folder exists (or will be created)
- Verify you pasted valid intent

### "Installation failed with permission error"
- Windows: Run PowerShell as Administrator
- Mac/Linux: Check folder permissions: `chmod 755 ~/.config/Code/User/prompts/`

## Updating the Agent

To get latest improvements:

### Windows
```powershell
# Re-run installation command above
# Or manually download from:
# https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/global/diagram-orchestrator.agent.md
# Save to: %APPDATA%\Code\User\prompts\
```

### Mac/Linux
```bash
# Re-run installation command above
# Or manually download from:
# https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/global/diagram-orchestrator.agent.md
# Save to: ~/.config/Code/User/prompts/
```

## What's Inside

The installed agent is **diagram-orchestrator.agent.md**, which includes:

- **Step 1:** Parse and normalize intent
- **Step 2:** Generate Mermaid with fallback v1 profile
- **Step 2.5:** Pre-lint syntax check (catches `<br>` in sequence, dashes, unquoted labels)
- **Step 3:** Linter validation (naming, complexity, spec compliance)
- **Step 4:** Clarity review (ambiguities, context gaps, logic)
- **Step 5:** Merge gate decision (READY FOR PR or BLOCKED)

All 5 steps run in **one conversation turn**.

## Advanced: Customize Fallback Profile

Edit `global/diagram-orchestrator.agent.md` to change v1 defaults:

```yaml
# In "If project rules are missing, use fallback v1 profile:"
- Max nodes: 15 → change to your preference
- Forbidden labels: "handle", "process", "do stuff" → customize
- Node ID regex: "^[a-z0-9]+(-[a-z0-9]+)*$" → modify for your naming
```

Then re-install globally.

## Uninstall

To remove the agent:

### Windows
```powershell
Remove-Item -Path "$env:APPDATA\Code\User\prompts\diagram-orchestrator.agent.md"
```

### Mac/Linux
```bash
rm ~/.config/Code/User/prompts/diagram-orchestrator.agent.md
```

## Next Steps

1. ✅ **Install:** Run command above
2. ✅ **Try it:** Open any project, use `@diagram-orchestrator`
3. 📚 **Read:** [README.md](README.md) for full documentation
4. 🤝 **Contribute:** See [CONTRIBUTING.md](CONTRIBUTING.md)
5. 🔧 **Customize:** See [diagram-spec.md](diagram-spec.md) for project rules

## Support

- **Installation issues:** See Troubleshooting section above
- **Agent not working:** Restart VS Code, check installation path
- **Feature requests:** Open issue on GitHub
- **Questions:** See [vscode-agent-workflow.md](vscode-agent-workflow.md)

---

**Ready to generate your first diagram?** Open VS Code and type `@diagram-orchestrator`! 📊
4. `scripts/diagram_lint.py`
5. `.github/workflows/diagram-lint.yml`
6. `.github/pull_request_template.md`
7. `.vscode/tasks.json`

## Recommended Distribution Model
1. Keep this repo as the source kit on GitHub.
2. Teams globally install the prompt once.
3. Each project adopts the repo-level enforcement files for CI reliability.
