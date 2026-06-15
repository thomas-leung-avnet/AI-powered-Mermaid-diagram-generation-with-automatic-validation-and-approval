You are generating a team-standard Mermaid diagram.

Use these inputs together:
1. diagram-spec.yaml (authoritative machine rules)
2. diagram-spec.md (human guidance)
3. developer intent below

Follow these rules strictly:
- Diagram type: {architecture|sequence|process}
- Use only approved v1 symbols/arrows/notations.
- Include: title, legend, scope boundary, main flow, and error flow (if any).
- Use kebab-case node IDs.
- Use concise labels and verb-based edge labels.
- Direction: left-to-right.
- Max 15 nodes; split if needed.
- Prefer the simplest readable diagram that still matches the intent.
- If something is outside the spec, do not invent a new symbol; use the closest approved notation or flag it as a proposal.
- Output Mermaid code only. No explanation text.

Developer intent:
- goal: {what the diagram should explain}
- scope: {what code/module/process to cover}
- audience: {devs|managers|mixed}
- important nodes/steps: {optional}
- known errors/branches: {optional}

Task:
Generate one spec-compliant Mermaid diagram that is standardized, trustworthy, and easy for the team to understand.
