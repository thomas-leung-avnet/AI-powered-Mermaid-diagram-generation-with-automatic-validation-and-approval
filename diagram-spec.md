# Diagram Spec v1

## 1. Purpose
This spec standardizes shared/project diagrams for readability, consistency, and reviewability.

## 2. Scope
Allowed diagram types:
1. Architecture (C4-lite)
2. Sequence (UML-lite)
3. Process Flow (Flowchart/BPMN-lite)

Personal/private notes are out of scope.

## 3. Authoring Format
1. Primary format: Mermaid
2. Stored in: `/docs/diagrams/`
3. Shared diagrams must be committed as text (`.md` or `.mmd`)
4. Developers may use AI to draft diagrams, but the final output must still pass this spec

## 4. Developer Workflow
To generate a shared diagram:
1. Provide a small intent block: goal, scope, audience, important nodes/steps, and known errors/branches
2. Give the AI this spec bundle: `diagram-spec.yaml`, `diagram-spec.md`, and either `prompt-template.md` (single prompt) or the `prompts/` agent pack
3. Ask the AI to output Mermaid only (generator step)
4. Validate the result against the machine rules and checklist
5. Commit only spec-compliant diagrams

## 5. Mandatory Structure
Every shared diagram must include:
1. Title
2. Legend
3. System boundary/scope
4. Main flow
5. Error/exception flow (if applicable)
6. Assumptions/notes (short)

## 6. Approved Notation (Core Set)
Use only these core symbols/arrows in v1:
1. Actor (user/external system)
2. Service/API
3. Process/step
4. Decision
5. Data store
6. Queue/event bus
7. External dependency
8. Boundary/group
9. Solid arrow = synchronous call
10. Dashed arrow = async/event
11. Dotted arrow = optional/conditional
12. Error arrow = failure path

Any new symbol requires extension approval.

## 7. Naming Rules
1. Node ID: `kebab-case`
2. Labels: concise noun/noun phrase
3. Edges: verb phrase (e.g., "validates token", "publishes event")
4. Avoid ambiguous labels like "handle", "process", "do stuff"

## 8. Layout Rules
1. Direction: Left-to-right by default
2. Group by bounded context/module
3. Max 12-15 nodes per diagram (split if larger)
4. Avoid crossing lines when possible

## 9. Mermaid Usage Rules (v1 Profile)
1. Allowed diagram declarations: `flowchart LR`, `sequenceDiagram`
2. Disallow styling/interactivity in shared diagrams: `style`, `classDef`, `click`, image/icon nodes
3. Include frontmatter config in shared diagrams:
   - `theme: neutral`
   - `look: classic`
   - `layout: dagre`
4. For flowcharts, avoid lowercase `end` as node text
5. Quote labels containing special characters

## 10. Compliance Rules
A shared diagram fails if:
1. Uses unapproved symbols
2. Missing legend/title/scope
3. Missing main flow
4. Violates naming/layout rules
5. Contains unexplained custom notation

## 11. Extension Process
To add notation:
1. Submit symbol proposal (meaning, usage, example)
2. Reviewer approves/rejects within 48 hours
3. If approved, update spec version (v1.x)

## 12. Review & Merge Gate
1. Shared diagrams must pass diagram-lint/checklist
2. PR reviewer enforces this spec
3. Non-compliant diagrams are not merged
4. PRs should use `.github/pull_request_template.md` and include intent + agent evidence
5. CI enforces lint via `.github/workflows/diagram-lint.yml`

## 13. Agent-First Workflow (VS Code)
For teams using VS Code, the recommended operating model is an agent-first loop:
1. Curate intent
2. Generate Mermaid candidate
3. Lint against machine/human rules
4. Perform visual QA
5. Apply merge gate decision

Use `vscode-agent-workflow.md` for role definitions, prompt pack, and loop details.
