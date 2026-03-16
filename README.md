# Lab Scaffold

This directory is the first-pass control surface for the Lab system.

This README describes the current repo shape and current usage surface.

## Current Repository Contents

- a design document
- a roadmap
- a changelog
- an OpenCode-shaped canonical config layout
- a first-pass local agent roster
- a sprint template directory
- a documented intended command lifecycle

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

## Current Lab Roles

The initial local roster lives in `agents/`.

- `lab-orchestrator`
- `lab-worker`
- `lab-validator`
- `lab-reporter`

These are intentionally broad first-pass definitions.

## Current Command Lifecycle

The current intended command lifecycle is:

1. `ai-lab plan <brief>`
2. human review of the generated plan
3. `ai-lab run <plan>`
4. human review of the generated report

The exact wrapper behavior is still to be implemented, but this is the current
shape of the interface Lab is aiming toward.

## Runtime Notes

Typing `opencode` starts the TUI. That is useful for manual interaction, but it
is not the primary Lab path.

The intended Lab interface is an `ai-lab` wrapper around OpenCode.

The exact wrapper behavior and server lifecycle are still to be implemented.

## Sprint Template

Use `templates/sprint/` as the starting point for a new sprint directory.

It defines only the broad file structure needed for:

- design input
- roadmap and feedback
- artifacts
- logs
- reports
- status

In real project instances, runtime state should live under deterministic
run-id-based directories in `.ai-lab/runs/`.