# Lab

Lab is a file-native agent laboratory built around explicit briefs, plans, runs, benches, logs, validation, and reports.

This repository is the canonical source for Lab prompts, wrapper code, and project documentation.

Use this README for installation and current usage.
Use `DESIGN.md` for the intended end state.
Use `ROADMAP.md` for implementation status.

Lab is designed around a bench-first execution model. Agents operate inside a run-specific working surface prepared for the run rather than directly in the live project root.

## What Lab Looks Like In Use

The intended project-local shape is:

```text
myRepo/
  .git/
  .opencode/    # active Lab/OpenCode projection
  .ai-lab/      # generated Lab runtime state
    <run-id>/
      record/   # durable run record
      bench/    # run bench / agent workspace
```

## Prerequisites

Current POC usage assumes:

- `git` is installed
- `opencode` is installed and working
- the project already has a `.git/` entry at its root
- the active `.opencode/` projection exposes the Lab agent roster, including `lab-orchestrator`

## Installation

The current wrapper source lives in `bin/ai-lab` in this repo.

Current status note: the shell wrapper is an early POC launcher. The intended canonical control plane is a Python wrapper so the main Lab path is not tied to bash semantics.

For a project-local OpenCode instance, the expected shape is that this repo is instantiated into the project's `.opencode/` directory structure.

At minimum:

1. Make sure your target project has a root directory with `.git/`.
2. Make sure that project has an active `.opencode/` projection containing the Lab agents and wrapper.
3. Make the wrapper available as `.opencode/bin/ai-lab`.
4. Run `ai-lab` from the project root or from the project's `.opencode/` directory.

The wrapper resolves `.ai-lab/` at the project root and creates it if missing.

## Usage

The current operator flow is:

1. `ai-lab plan <brief>`
2. review the generated `plan.md`
3. `ai-lab run <slug>`
4. review the generated `report.md`

### `ai-lab plan <brief>`

Creates a new run under `.ai-lab/<run-id>/`, prepares `record/` and `bench/` for that run, copies the brief into the run record, initializes top-level run artifacts, and invokes the orchestrator in planning mode.

A brief does not need one rigid template, but it should make these things clear:

- the objective
- the scope boundaries
- the success criteria
- the target surface when that is not obvious from context
- the constraints or prohibitions
- the key inputs or source artifacts

The exact headings, order, and phrasing may vary. Execution will not begin until the brief is complete enough to support planning.

### `ai-lab run <slug>`

Resolves the requested slug to a run under `.ai-lab/`, reads the run's `record/plan.md`, and invokes the orchestrator in run mode. If more than one run matches the slug, use the full run id instead.

## Current Runtime Notes

- Typing `opencode` starts the TUI. That can be useful for manual interaction, but it is not the primary Lab path.
- Run the wrapper from the project root or from the sibling `.opencode/` directory.
- `.ai-lab/` always lives at the project root.
- Every Lab run is intended to be bench-scoped.
- The current shell wrapper has not yet been fully realigned to the bench-first design.
- The checked-in OpenCode permission profile still reflects an older POC baseline and is not yet the intended unattended capability contract.
- The intended unattended boundary is the run directory as workspace root, without arbitrary host-shell access.
- The wrapper fails fast when required structure or required git operations are missing.

## Current Limitations

Lab is still in early implementation.

Current limitations include:

- the wrapper is drafted but not yet fully aligned to the current bench-first architecture
- the canonical Python wrapper rewrite is still ahead
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