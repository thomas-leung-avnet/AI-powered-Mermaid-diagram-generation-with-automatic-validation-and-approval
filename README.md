# Diagram Standardization Kit

**AI-powered Mermaid diagram generation with automatic validation, clarity review, and approval gating.**

Generate production-ready architecture and sequence diagrams in one command. The orchestrator agent handles generation, validation, clarity review, and approval—no more syntax errors or ambiguous flows.

## ✨ Quick Start

### Path 1: Global Installation (Recommended)
Install once, use the orchestrator agent on any project.

```powershell
# Windows
powershell -ExecutionPolicy Bypass -Command "iex (irm 'https://raw.githubusercontent.com/thomas-leung-avnet/diagram-spec-kit/main/scripts/GLOBAL-INSTALL.ps1')"
```

Then in VS Code:
1. Open Chat (Cmd+I / Ctrl+Shift+Alt+I)
2. Type `@diagram-orchestrator` 
3. Paste your intent:
   ```
   Create sequence diagram for payment processing flow. 
   Goal: show interaction between user client, payment gateway, processor. 
   Scope: payment initiation → authorization → settlement → confirmation. 
   Error paths: declined card, expired card, processor timeout.
   ```
4. Agent generates, validates, reviews, and approves ✅

### Path 2: Local Installation
Add enforcement to your project (GitHub CI/CD + linting).

```bash
# Copy enforcement files
cp -r .github/ ../.github/
cp -r .vscode/ ../.vscode/
cp -r scripts/ ../scripts/
cp diagram-spec.* ../
cp checklists/ ../checklists/
```

Then commit and push. Diagrams will be validated on every PR.

## 🎯 What You Get

| Feature | Benefit |
|---------|---------|
| **Orchestrator Agent** | Full pipeline: generate → validate → review → approve (one call) |
| **Syntax Validation** | Catches `<br>` in sequence diagrams, unquoted labels, dashes as operators before saving |
| **Linter** | Enforces naming (kebab-case), complexity (≤15 nodes), required sections (legend, scope) |
| **Clarity Review** | Fresh-reader assessment catches ambiguities, context gaps, unexplained flows |
| **CI/CD Enforcement** | GitHub Actions blocks PRs if diagrams don't meet spec |
| **PR Template** | Enforces intent documentation and agent evidence |
| **Spec Compliance** | YAML-driven rules (customizable per project) |

## 📋 Enforced Standards

- **Diagram Types:** `flowchart LR` (architecture) or `sequenceDiagram` (interaction)
- **Naming:** Kebab-case IDs (`user-client`, `payment-gateway`)
- **Node Limit:** Max 15 nodes per diagram
- **Required Sections:** Title, legend, scope boundary, main flow, error flow
- **Forbidden Labels:** "handle", "process", "do stuff"
- **Edge Labels:** Explicit verb phrases required (`submits`, `authorizes`, `declines`)

## 🚀 Usage

### Generate a Diagram (Global Agent)
```
@diagram-orchestrator
Create architecture flowchart for login system. 
Goal: show authentication flow from client to database.
Scope: user → API gateway → auth service → database.
Participants: user-client, api-gateway, auth-service, user-database.
Error branches: user not found, password mismatch, database timeout.
```

**Agent Output:**
1. ✅ Step 1: Normalized intent
2. ✅ Step 2: Generated Mermaid (saved to `docs/diagrams/login-system.mmd`)
3. ✅ Step 3: Linter validation (PASS)
4. ✅ Step 4: Clarity review (CLEAR)
5. ✅ Step 5: Merge gate (READY FOR PR)

### Validate Locally
```bash
# Full scan
py -3 scripts/diagram_lint.py

# Check only changed files
py -3 scripts/diagram_lint.py --changed

# Output
PASS: docs/diagrams/login-system.mmd
PASS: docs/diagrams/payment-flow.mmd
diagram-lint: all diagrams passed
```

### Add to Your Project
1. Copy `.github/workflows/diagram-lint.yml` to your repo
2. Add `diagram-spec.yaml` and `diagram-spec.md` (customize rules)
3. Diagrams are now auto-validated on PR
4. Merge blocked if validation fails

## 📂 File Structure

```
diagram-spec-kit/
├── README.md                          # This file
├── diagram-spec.yaml                  # Machine-readable rules
├── diagram-spec.md                    # Human-readable governance
├── vscode-agent-workflow.md           # Complete workflow guide
├── GLOBAL-INSTALL.md                  # Global installation guide
│
├── global/
│   ├── diagram-orchestrator.agent.md  # Master orchestrator (use this!)
│   └── diagram-standardizer.prompt.md # Alternative: just-generate mode
│
├── prompts/                           # Supporting agents (optional)
│   ├── agent-intent-curator.md
│   ├── agent-diagram-generator.md
│   ├── agent-rule-lint.md
│   ├── agent-diagram-reviewer.md
│   └── agent-merge-gate.md
│
├── scripts/
│   ├── diagram_lint.py                # Core linter (Python)
│   └── GLOBAL-INSTALL.ps1             # PowerShell installer
│
├── .github/workflows/
│   └── diagram-lint.yml               # GitHub Actions CI/CD
│
├── .vscode/
│   ├── tasks.json                     # Lint tasks (full + changed modes)
│   └── settings.json                  # Workspace config
│
├── checklists/
│   └── review-checklist.md            # Manual review template
│
├── docs/diagrams/
│   ├── login-system-architecture.mmd  # Example: flowchart
│   └── payment-processing-flow.mmd    # Example: sequence diagram
│
└── examples/
    ├── architecture-example.mmd
    └── sequence-example.mmd
```

## 📚 Documentation

- **[diagram-spec.md](diagram-spec.md)** — Complete specification (governance rules, naming, structure)
- **[diagram-spec.yaml](diagram-spec.yaml)** — Machine-readable ruleset (linter config)
- **[vscode-agent-workflow.md](vscode-agent-workflow.md)** — Full architecture and workflow guide
- **[GLOBAL-INSTALL.md](GLOBAL-INSTALL.md)** — Installation and distribution
- **[checklists/review-checklist.md](checklists/review-checklist.md)** — Manual review template

## 🔧 Customization

### Project-Specific Rules
Create `diagram-spec.yaml` in your repo to override defaults:

```yaml
notation:
  flowchart:
    node_id_regex: "^[a-z0-9]+(-[a-z0-9]+)*$"
    max_nodes_per_diagram: 15
    forbidden_edge_labels:
      - handle
      - process
      - do stuff

mermaid_profile:
  theme: neutral
  layout: dagre
  allowed_node_shapes: []
  disallowed_features:
    - style
    - classDef
    - click
```

### Local Workflow
Add to your project:
1. Copy `diagram-spec.yaml` (customize rules)
2. Copy `.github/workflows/diagram-lint.yml`
3. Copy `.vscode/tasks.json` (lint shortcuts)
4. Run `py -3 scripts/diagram_lint.py` before commit

## 🐛 Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `Parse error: got 'INVALID'` | `<br/>` self-closing tag | Use `<br>` (no slash) |
| `Parse error: got ','` | Dashes in sequence labels | Use simple text: `"authorize"` not `"authorize - check"` |
| Unquoted label error | Missing quotes in sequence | Use `\|"text"\|` format |
| 15-node violation | Diagram too complex | Split into multiple diagrams or simplify |

See [Syntax Error Prevention](diagram-spec-kit-README.md#syntax-error-prevention) in docs for all patterns.

## ✅ Pre-Push Checklist

Before committing diagrams:

- [ ] All diagrams in `docs/diagrams/*.mmd`
- [ ] Run linter: `py -3 scripts/diagram_lint.py` (all PASS)
- [ ] For sequences: no `<br>`, no dashes as separators, simple labels
- [ ] For flowcharts: kebab-case IDs, explicit edge labels
- [ ] No forbidden edge labels ("handle", "process", "do stuff")
- [ ] Legend present (comment or box)
- [ ] Scope boundary present (subgraph or box)

## 🤝 Contributing

Diagram improvements welcome! 

When adding a new diagram:
1. Use orchestrator agent (copy intent to chat)
2. Agent generates and validates
3. Create PR with intent block and verdicts
4. Merge when CI passes

## 📄 License

[Add your license here]

## 🚀 Next Steps

1. **Try it:** `@diagram-orchestrator` in VS Code Chat
2. **Install globally:** Follow Path 1 above
3. **Add to project:** Follow Path 2 above
4. **Read full spec:** See [diagram-spec.md](diagram-spec.md)
5. **Troubleshoot:** Check [Common Issues](#-common-issues) section

---

**Questions?** See [vscode-agent-workflow.md](vscode-agent-workflow.md) for complete architecture and workflow guide.
