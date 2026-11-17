# rails-feature-review

A Claude Code skill that independently reviews and verifies AI-generated Ruby on Rails feature changes against the team's Engineering Standards.

It acts as a skeptical reviewer: it checks the real working tree, adds narrowly scoped tests, runs available checks, exercises the feature in a development browser, and produces a go/no-go report backed by evidence.

## Contents

- `SKILL.md`: the skill definition and workflow
- `references/`: test strategy, rule-review matrix, browser testing, report template and schema, and the standards snapshot
- `scripts/`: `report_gate.py` and `check_architecture_snapshot.py`
- `tests/`: tests for the scripts
- `agents/`: agent config (`openai.yaml`)
- `integrations/`: example snippets for `CLAUDE.md`, `AGENTS.md` and Cursor rules

## Install

```bash
git clone <repo-url> ~/.claude/skills/rails-feature-review
```

Then invoke it in Claude Code with `/rails-feature-review` after a feature has been implemented.

## Tests

```bash
python3 -m unittest discover tests
```
