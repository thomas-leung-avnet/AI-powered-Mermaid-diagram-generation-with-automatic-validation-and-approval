# VS Code Agent-First Workflow (Mermaid)

## 1. Goal
Use an autonomous agent loop in VS Code to generate spec-compliant Mermaid diagrams with repeatable quality gates.

This workflow is designed for teams that:
1. Use VS Code as the main IDE
2. Need Git-friendly text diagrams
3. Want one-command diagram generation with automatic validation and review

## 2. Inputs
Required inputs for every run:
1. `diagram-spec.yaml` (machine rules)
2. `diagram-spec.md` (human rules)
3. `checklists/review-checklist.md` (review gate)
4. A developer intent block:
   - goal
   - scope
   - audience
   - important nodes/steps (optional)
   - known errors/branches (optional)

## 3. Quick Start: Diagram Orchestrator (Recommended)
**For most teams, use the Diagram Orchestrator Agent:**

1. Open Copilot Chat
2. Select the `diagram-orchestrator` prompt
3. Paste your intent (goal, scope, audience, nodes, errors)
4. The orchestrator handles the entire pipeline end-to-end:
   - Normalizes intent
   - Generates diagram
   - Validates with linter
   - Reviews for clarity
   - Reports merge gate decision

Result: One report with file path, all verdicts, and next action.

---

## 3b. Alternative: Manual Multi-Step Workflow
For more control or teaching, use individual agents (see Section 5 below).

---

## 4. Agent Roles
Use these roles even if one assistant performs all steps.

### Role A: Intent Curator Agent
Responsibility:
1. Normalize intent into a bounded problem statement
2. Identify diagram type (architecture, sequence, process)
3. Reduce ambiguity before generation

Output contract:
1. Final intent block
2. Selected diagram type
3. List of assumptions (short)

### Role B: Diagram Generator Agent
Responsibility:
1. Generate Mermaid only
2. Follow `diagram-spec.yaml` and `diagram-spec.md` strictly
3. Keep complexity within node limit

Output contract:
1. One Mermaid diagram candidate
2. If out-of-spec concepts exist, include a short proposal note outside Mermaid

### Role C: Rule Lint Agent
Responsibility:
1. Validate syntax and profile constraints
2. Check required sections and naming rules
3. Produce pass/fail with concrete violations

Output contract:
1. `PASS` or `FAIL`
2. Violation list with exact fixes

### Role D: Visual QA Agent
Responsibility:
1. Render preview in VS Code Mermaid tools
2. Check readability and flow clarity
3. Ensure labels and arrows remain unambiguous

Output contract:
1. `PASS` or `FAIL`
2. Layout/readability issues and proposed edits

### Role E: Merge Gate Agent
Responsibility:
1. Verify checklist completion
2. Ensure final artifact matches all mandatory sections
3. Approve for PR or return remediation items

Output contract:
1. `READY FOR PR` or `BLOCKED`
2. Blocking reasons (if any)

## 4. Standard Loop
Run this loop until all gates pass.

1. Intent Curator -> normalize intent
2. Diagram Generator -> produce Mermaid candidate
3. Rule Lint -> fail fast on spec violations
4. Diagram Reviewer -> catch ambiguity and clarity issues
5. Merge Gate -> finalize decision

Recommended retry policy:
1. Max 3 correction loops per diagram
2. If reviewer flags UNCLEAR, iterate on clarity
3. If still failing after 3 loops, split diagram by scope and retry

## 5. Prompt Pack For VS Code (Supporting Roles)
These prompts support the orchestrator or can be used independently for more control.

For quick reference:
- Prompts are located in `prompts/` (repo source)
- Global installed versions are in `%APPDATA%\Code\User\prompts\`

**Primary Entry Point:**
- `diagram-orchestrator` - runs full pipeline end-to-end (recommended)

**Supporting Prompts (invoked by orchestrator internally):** (Optional if using orchestrator)
```text
You are the Intent Curator Agent for team Mermaid diagrams.

Inputs:
- diagram-spec.yaml
- diagram-spec.md
- developer intent block

Task:
1. Determine diagram type: architecture | sequence | process.
2. Rewrite the intent to remove ambiguity.
3. Return a final intent block with goal, scope, audience, important nodes/steps, known errors/branches.
4. Return up to 5 explicit assumptions.

Output format:
- diagram_type:
- intent:
- assumptions:
```

### Prompt 2: Diagram Generator (Optional if using orchestrator)
```text
You are the Diagram Generator Agent.

Use:
- diagram-spec.yaml as authoritative rules
- diagram-spec.md as human guidance
- curated intent from previous step

Requirements:
- Output Mermaid code only.
- Use approved notations only.
- Include title, legend, scope boundary, main flow, and error flow if applicable.
- Keep node IDs kebab-case and edge labels as verb phrases.
- Keep diagram <= 15 nodes.
```

### Prompt 3: Rule Lint Agent (Optional if using orchestrator)
```text
You are the Rule Lint Agent.

Validate the Mermaid candidate against:
- diagram-spec.yaml
- diagram-spec.md
- checklists/review-checklist.md

Return:
- verdict: PASS | FAIL
- violations: numbered list
- exact minimal edits needed

If FAIL, also return a corrected Mermaid version.
```

### Prompt 4: Diagram Reviewer (Optional if using orchestrator)
```text
You are the Visual QA Agent.

Review rendered Mermaid output for:
- readability
- edge-label clarity
- crossing/overlap risk
- logical left-to-right flow

Return:
- verdict: PASS | FAIL
- issues: numbered list
- minimal layout edits

Do not introduce disallowed Mermaid features.
```

### Prompt 5: Diagram Reviewer Agent (Optional if using orchestrator)
```text
You are a Diagram Reviewer Agent for Mermaid diagrams.

Review the diagram with a fresh eye as if you are a new developer.
Do NOT assume system knowledge.

Check for:
- Clarity issues: unclear labels, ambiguous language
- Context gaps: unexplained flows, missing details
- Flow logic: can you trace the path clearly?
- Assumptions: what would a new developer need to know?

Output:
- Verdict: CLEAR | UNCLEAR | NEEDS REVISION
- Issues: numbered list of ambiguities
- Questions: clarifying questions as a fresh reader
- Suggestions: concrete improvements
```

### Prompt 6: Merge Gate Agent (Optional if using orchestrator)
```text
You are the Merge Gate Agent.

Check final output against:
- checklists/review-checklist.md
- mandatory structure in diagram-spec.md
- diagram reviewer verdict (should be CLEAR)

Return exactly one:
- READY FOR PR
- BLOCKED: <reasons>
```

## 6. Repo Integration Pattern
Use this folder pattern if you want repeatable runs:

```text
prompts/
  agent-intent-curator.md
  agent-diagram-generator.md
  agent-rule-lint.md
  agent-visual-qa.md
  agent-merge-gate.md
outputs/
  diagrams/
```

## 7. Suggested Team Policy
1. Mermaid remains source of truth.
2. AI/agent output is allowed but must pass lint + checklist.
3. Any out-of-spec notation requires extension proposal before merge.
4. PR description includes intent block and lint verdict.

## 8. Definition of Done
A diagram is done only if:
1. Rule Lint verdict is `PASS`
2. Diagram Reviewer verdict is `CLEAR`
3. Merge Gate verdict is `READY FOR PR`

## 9. PR and CI Enforcement
Repository enforcement assets:
1. PR template: `.github/pull_request_template.md`
2. CI workflow: `.github/workflows/diagram-lint.yml`
3. Lint script: `scripts/diagram_lint.py`

The CI workflow runs lint on `docs/diagrams/**` changes and blocks merge on failures.

## 10. Global Agent Installation
For cross-project usage in VS Code, install global prompts once:
1. Run `powershell -ExecutionPolicy Bypass -File .\\scripts\\install_global_prompt.ps1`
2. Available prompts in any workspace:
   - `diagram-standardizer` - generates compliant diagrams
   - `diagram-reviewer` - reviews diagrams for clarity

Reference: `GLOBAL-INSTALL.md`
