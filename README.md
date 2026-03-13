# Lab Scaffold

This directory is the first-pass control surface for the Lab system.

## What This Scaffold Includes

- a lean design doc
- an OpenCode-shaped canonical config layout
- a first-pass local agent roster
- a sprint template directory
- a non-TUI usage path for starting and running OpenCode

## What This Scaffold Does Not Include

- a finalized global agent canon
- hardened unattended supervision
- finalized validator tooling
- finalized cleanup behavior

## Draft Status

The current agent files are placeholders.

They are first-pass operational drafts, not finalized canon.

## Instance Model

This repository is the canonical Lab source.

OpenCode consumes an active Lab instance through an OpenCode-facing binding.

That binding may take different forms:

- `myProject/.opencode/`
- `~/.config/opencode/`
- a symlink to a canonical Lab repo
- a direct clone of a Lab repo used in place

The binding location is flexible.

The intended stable shape is:

- `lab/` repo: canonical source and templates
- active OpenCode binding: one current OpenCode-facing projection of Lab
- `myProject/.ai-lab/`: generated Lab runtime state for the project being worked on

This keeps source, binding, and generated state separate.

Projection rule:

- the active OpenCode binding may be regenerated from Lab canon
- `.ai-lab` is operational state and must not be treated as canonical source
- `.ai-lab` always belongs in the project directory, regardless of where the
  active OpenCode binding lives

## Secrets And Runtime Data

Keep secrets and runtime data out of the repo.

Current rule of thumb:

- keep API credentials in environment variables or separate local files
- let OpenCode auth/session data stay in its normal machine-local locations
- do not write generated run outputs into tracked root paths; use ignored
  project-local runtime state such as `.ai-lab/`

## Non-TUI Runtime Path

Typing `opencode` starts the TUI. That is useful for manual interaction, but it
is not the main Lab path.

For Lab work, prefer these modes:

1. Start a headless server:

```bash
cd /Users/nate.droppo/dev/Projects/lab
opencode serve --hostname 127.0.0.1 --port 4096
```

2. In another terminal, run a one-shot orchestrator session against that server:

```bash
cd /Users/nate.droppo/dev/Projects/lab
opencode run \
  --attach http://127.0.0.1:4096 \
  --agent lab-orchestrator \
  "Execute the approved sprint described in the current run directory."
```

This keeps the runtime separate from the editor while preserving the workspace
as the canonical artifact surface.

## Current Local Agent Roster

The initial local roster lives in `agents/`.

- `lab-orchestrator`
- `lab-planner`
- `lab-worker`
- `lab-validator`
- `lab-reporter`

These are intentionally broad first-pass definitions.

## Sprint Template

Use `templates/sprint/` as the starting point for a new sprint directory.

It defines only the broad file structure needed for:

- design input
- roadmap and feedback
- artifacts
- logs
- reports
- status

## Next Likely Moves

1. Tighten the agent prompts.
2. Decide which agents are artifact-only versus execution-capable.
3. Define the first real sprint input contract.
4. Decide whether to keep this repo runtime-specific or refactor it into a more
  runtime-agnostic Lab canon.