# Lab

Lab is a file-native agent execution framework built around explicit briefs, plans, runs, logs, validation, and reports.

This repository is the canonical source for the Lab configuration, prompts, and project documentation.

## Draft Status

Lab is still in early implementation.

The current agent files are placeholder operational drafts, not finalized canon.

## Instance Model

OpenCode consumes an active Lab instance through an OpenCode-facing binding.

That binding may take different forms:

- `myProject/.opencode/`
- `~/.config/opencode/`
- a symlink to a canonical Lab repo
- a direct clone of a Lab repo used in place

The binding location is flexible.

The current model is:

- `lab/` repo: canonical source
- active OpenCode binding: one current OpenCode-facing projection of Lab
- `myProject/.ai-lab/`: generated Lab runtime state for the project being worked on

Lab canon and generated runtime state are intentionally separate.

`.ai-lab` belongs in the project directory, regardless of where the active OpenCode binding lives.

## Secrets And Runtime Data

Keep secrets and runtime data out of the repo.

- keep API credentials in environment variables or separate local files
- let OpenCode auth/session data stay in its normal machine-local locations
- keep generated run outputs in ignored project-local runtime state such as `.ai-lab/`

## Current Lab Roles

The initial local roster lives in `agents/`:

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

This is the intended interface Lab is aiming toward.

## Brief Guidance

A brief does not need one rigid template, but it should make these things clear:

- the objective
- the scope boundaries
- the success criteria
- the target surface when that is not obvious from context
- the constraints or prohibitions
- the key inputs or source artifacts

The exact headings, order, and phrasing may vary. Execution will not begin until the brief is complete and understood.

## Runtime Notes

Typing `opencode` starts the TUI. That is useful for manual interaction, but it is not the primary Lab path.

The intended Lab interface is an `ai-lab` wrapper around OpenCode.

## Run Records

Run records are created under `.ai-lab/runs/`.

In real project instances, runtime state should live under deterministic run-id-based directories in `.ai-lab/runs/`, using the form `YYYY-MM-DD-HH-MM_slug`.

Bench runs may also use isolated execution checkouts under `.ai-lab/benches/`.

For the detailed run contract, see `DESIGN.md`.