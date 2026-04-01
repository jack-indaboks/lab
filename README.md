# Lab

Lab is a file-native agent laboratory built around explicit briefs, plans, runs, benches, logs, validation, and reports.

This repository is the canonical source for Lab prompts, Python control-layer code, and project documentation.

Use this README for installation and current usage.
Use `DESIGN.md` for the intended end state.
Use `ROADMAP.md` for implementation status.

Lab is designed around a bench-first execution model. Agents operate inside a run-specific working surface prepared for the run rather than directly in the live project root.

## What Lab Looks Like In Source

The current standalone source-repo shape is:

```text
lab/
  README.md
  DESIGN.md
  ROADMAP.md
  DEVELOPMENT.md
  CHANGELOG.md
  pyproject.toml
  lab/
    __main__.py
    cli.py
    control.py
  opencode/
```

## What Lab Looks Like In Use

In a target project, Lab creates runtime state like this:

```text
myRepo/
  .git/
  .ai-lab/      # generated Lab runtime state
    <run-id>/
      record/
      bench/
```

## Prerequisites

Current POC usage assumes:

- `git` is installed
- `python` is installed
- `opencode` is installed and working
- the repo checkout already has a `.git/` entry at its root
- the repo-owned `opencode/` surface exposes the Lab agent roster, including `lab-orchestrator`

## Installation

The current executable surface is the Python control layer under `lab/`.

Current status note: the Python entrypoint still carries forward early wrapper behavior and has not yet been fully realigned to the bench-first design.

At minimum:

1. Clone this repo.
2. Make sure `git`, `python`, and `opencode` are available in the environment.
3. From the repo root, run `python -m lab --help` or install the project and run `lab --help`.

The control layer resolves `.ai-lab/` at the current project root and creates it if missing. It points OpenCode at the repo-owned config in `opencode/opencode.json`.

## Usage

The current operator flow is:

1. `lab plan <brief>`
2. review the generated `plan.md`
3. `lab run <slug>`
4. review the generated `report.md`

### `lab plan <brief>`

Creates a new run under `.ai-lab/<run-id>/`, prepares `record/` and `bench/` for that run, copies the brief into the run record, initializes top-level run artifacts, and invokes the orchestrator in planning mode.

A brief does not need one rigid template, but it should make these things clear:

- the objective
- the scope boundaries
- the success criteria
- the target surface when that is not obvious from context
- the constraints or prohibitions
- the key inputs or source artifacts

The exact headings, order, and phrasing may vary. Execution will not begin until the brief is complete enough to support planning.

### `lab run <slug>`

Resolves the requested slug to a run under `.ai-lab/<run-id>/`, reads the run's `record/plan.md`, and invokes the orchestrator in run mode. If more than one run matches the slug, use the full run id instead.

## Current Runtime Notes

- Typing `opencode` starts the TUI. That can be useful for manual interaction, but it is not the primary Lab path.
- Run Lab from a git project root.
- `.ai-lab/` always lives at the project root.
- Every Lab run is intended to be bench-scoped.
- The current Python control layer has not yet been fully realigned to the bench-first design.
- The checked-in OpenCode permission profile still reflects an older POC baseline and is not yet the intended unattended capability contract.
- The intended unattended boundary is the run directory as workspace root, without arbitrary host-shell access.
- The control layer fails fast when required structure or required git operations are missing.

## Current Limitations

Lab is still in early implementation.

Current limitations include:

- the control layer is drafted but not yet fully aligned to the current bench-first architecture
- hardening work such as stronger confinement, schemas, and registries is still ahead
- the prompts are first-pass POC prompts and will likely change after runtime testing
- the current OpenCode integration still needs a declared headless tool contract rather than prompt-time capability discovery
- the MVP developer toolbox still needs to be assembled from the OpenCode ecosystem rather than assumed through ambient shell access
- if a workspace-scoped shell-like capability exists in the ecosystem, Lab may use it; Lab is not meant to ship a bespoke simulated shell
- template-readiness and downstream portability work have not happened yet

For the detailed design vision, read `DESIGN.md`.
For the implementation backlog and status, read `ROADMAP.md`.

## Secrets And Runtime Data

Keep secrets and generated runtime data out of the canonical repo.

- keep credentials in environment variables or separate local files
- keep generated run outputs in project-local `.ai-lab/`
- let OpenCode auth and session data stay in their normal local locations

For the detailed runtime contract, see `DESIGN.md`.