# Contributing Diagrams

Thank you for contributing! This guide explains how to add or improve diagrams using the orchestrator workflow.

## Before You Start

- Have VS Code installed with Copilot Chat
- Diagram intent ready (goal, scope, audience, key participants)
- Familiarity with the [specification](diagram-spec.md)

## Step 1: Open Chat & Invoke Orchestrator

In VS Code Chat (Cmd+I):

```
@diagram-orchestrator

Create [flowchart|sequence] diagram for [topic].
Goal: [what should the diagram explain?]
Scope: [what actors/components/steps?]
Audience: [developers|managers|mixed?]
Key nodes: [important elements]
Error cases: [failure paths to show]
```

**Example:**
```
@diagram-orchestrator

Create sequence diagram for API authentication.
Goal: show the interaction between client, API gateway, and auth service during login.
Scope: credential submission, validation, token issuance, and error handling.
Audience: developers integrating with the API.
Key nodes: user client, API gateway, auth service, user database.
Error cases: invalid credentials, user not found, database timeout.
```

## Step 2: Let Agent Execute Full Pipeline

The orchestrator will:

1. **Parse intent** → Ask clarifying questions if needed
2. **Generate diagram** → Create `.mmd` file in `docs/diagrams/`
3. **Validate syntax** → Check for Mermaid parse errors
4. **Lint** → Verify naming, complexity, required sections
5. **Review clarity** → Assess for ambiguities and context gaps
6. **Approve** → Report READY FOR PR or BLOCKED

Wait for the **FINAL REPORT** before proceeding.

## Step 3: If BLOCKED

The agent will tell you exactly what's wrong. Example:

```
Step 3 - Lint Verdict: FAIL
- missing legend section
- node count (20) exceeds max (15)

Step 4 - Clarity Verdict: UNCLEAR
- "process payment" is ambiguous (charge card? settle transaction?)
- missing error flow for timeout

Next Action: Simplify diagram, add legend comment, clarify labels, re-run orchestrator
```

**Fix and re-run:** Copy the updated intent back to `@diagram-orchestrator` with fixes.

## Step 4: If READY FOR PR

Agent output:

```
=== DIAGRAM ORCHESTRATOR FINAL REPORT ===

Diagram File: docs/diagrams/api-authentication.mmd

Step 1 - Intent: NORMALIZED ✅
Step 2 - Generation: CREATED ✅
Step 3 - Lint Verdict: PASS ✅
Step 4 - Clarity Verdict: CLEAR ✅
Step 5 - Merge Gate: READY FOR PR ✅

Next Action: Create PR with diagram file and verdicts
```

Now you can commit!

## Step 5: Create Pull Request

1. **Stage the diagram file:**
   ```bash
   git add docs/diagrams/api-authentication.mmd
   ```

2. **Commit with intent block:**
   ```
   Add API authentication sequence diagram

   **Intent:**
   - Goal: Show interaction between client, gateway, auth service
   - Scope: Credential submission → token issuance, error cases
   - Audience: Developers
   - Key nodes: Client, Gateway, Auth Service, Database

   **Verdicts:**
   - Lint: PASS
   - Clarity: CLEAR
   - Merge Gate: READY FOR PR
   ```

3. **Push and create PR**
   ```bash
   git push origin feature/add-api-auth-diagram
   ```

4. **CI/CD validates automatically** → GitHub Actions runs linter on PR

5. **Merge when CI passes** ✅

## Guidelines

### Do's
- ✅ Use simple, descriptive labels: `"submit"`, `"authorize"`, `"timeout"`
- ✅ Include error flows (declined, expired, timeout, etc.)
- ✅ Use kebab-case for node IDs: `user-client`, `payment-gateway`
- ✅ Keep diagrams ≤15 nodes (split if larger)
- ✅ Add explicit legend or comment
- ✅ Test locally: `py -3 scripts/diagram_lint.py`

### Don'ts
- ❌ Don't use `<br>` in sequence diagram labels (use simple text)
- ❌ Don't use dashes as separators in labels: `"authorize - check"` → use `"authorize check"`
- ❌ Don't put parentheses in sequence labels: `"check (status)"` → use `"check status"`
- ❌ Don't use forbidden edge labels: "handle", "process", "do stuff"
- ❌ Don't create self-referential messages in sequences (A→A)
- ❌ Don't nest alt/else blocks deeply (max 1 level)

### Diagram Types Supported

**Flowchart LR** (Architecture)
- Shows component interaction
- Node IDs: `user-client`, `auth-service`, etc.
- Edges: `-->` (sync), `-.->` (async), `--x` (error)
- Nodes: `[]` square, `()` rounded, `{}` diamond, `(())` circle

**Sequence Diagram** (Interaction)
- Shows message flow over time
- Participants: `Client`, `Gateway`, `Processor`
- Arrows: `->>` (sync), `-->>` (async), `--x` (error)
- Blocks: `alt` (if/else), `loop`, `par` (parallel)
- **Constraints:** Simple labels only, no special characters

## Quick Reference

| Task | Command |
|------|---------|
| Validate locally | `py -3 scripts/diagram_lint.py` |
| Validate changed only | `py -3 scripts/diagram_lint.py --changed` |
| View spec | `cat diagram-spec.md` |
| View YAML rules | `cat diagram-spec.yaml` |
| Lint one file | `py -3 scripts/diagram_lint.py` (auto-finds all) |

## Troubleshooting

### Agent generates diagram but then reports syntax errors
- Agent has syntax validation (Step 2.5) but sometimes misses edge cases
- Run Step 2.5 checks manually: search for `<br>`, dashes, parentheses in labels
- Fix and re-run orchestrator

### Linter fails but diagram looks correct
- Run: `py -3 scripts/diagram_lint.py` to see exact violations
- Common: missing kebab-case ID, forbidden label, missing legend
- See [Syntax Error Prevention](README.md#-common-issues)

### PR blocked by CI
- GitHub Actions ran linter and found violations
- Click "Details" to see exact errors
- Fix diagram and push again

### Can't find orchestrator agent
- Agent must be installed (global or workspace)
- Try: type `@diagram` and see if autocomplete shows options
- Or use `@diagram-orchestrator` directly if installed globally

## Examples

See working diagrams:
- `docs/diagrams/login-system-architecture.mmd` (flowchart LR)
- `docs/diagrams/payment-processing-flow.mmd` (sequenceDiagram)

## Questions?

- **Read:** [vscode-agent-workflow.md](vscode-agent-workflow.md) (complete guide)
- **Reference:** [diagram-spec.md](diagram-spec.md) (full specification)
- **Linter:** [scripts/diagram_lint.py](scripts/diagram_lint.py) (source code)

---

**Happy diagramming! 📊**
