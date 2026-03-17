# Lab Design

## Purpose

This document describes the intended final design of the Lab system.

## Goal

Provide a file-native agent execution environment where:

- input begins with a brief
- Lab generates an executable plan from that brief
- execution happens through a runtime binding
- the workspace remains the canonical home for run state, logs, artifacts,
  and reports
- an orchestrator agent provisions specialized subagents as needed
- most agents work only with files, while a smaller set may use tools or
  sandboxed execution
- output ends with a run report backed by preserved logs

## Core Shape

The system has four major parts:

1. VS Code workspace
2. runtime binding
3. Optional execution environments for selected agents
4. Tool access through shell, MCP, and OpenAPI-compatible services where needed

## Workspace Role

The workspace is the canonical shared state surface.

Examples of state stored in the workspace:

- design docs
- briefs
- roadmaps
- prompts and context files
- logs
- validation outputs
- reports

The workspace is not a transient cache. It is the persistent record of a run.

In project instances, this design assumes a three-part split:

- canonical Lab source
- runtime-specific binding
- generated project-local Lab runtime state

For repo-modifying runs, project-local isolated execution checkouts should live
under `.ai-lab/benches/`.

The naming model is:

- `lab`: canonical repo
- active runtime binding: one current Lab projection for a supported runtime,
  which may live in a project, in home config, as a symlink, or as a direct
  clone
- `.ai-lab`: generated run state inside the project being worked on
- `.ai-lab/benches/<run-id>/`: isolated execution checkout for a run that
   modifies project files

Runtime state should use deterministic run-id-based subdirectories in the form
`YYYY-MM-DD-HH-MM_slug`, using a local timestamp without a timezone suffix.

## Runtime Role

The runtime binding is responsible for:

- loading reusable agent definitions
- running the orchestrator agent
- allowing the orchestrator agent to invoke specialized subagents
- enforcing per-agent permissions and tool access
- carrying out unattended execution once a plan is approved for run

The runtime binding is an instance projection, not the canonical source of Lab
behavior.

The location of that projection is flexible.

The location of `.ai-lab` is not: it belongs in the project being operated on.

## .ai-lab Contract

`.ai-lab/` is the generated runtime surface for a Lab-operated project.

Expected structure:

```text
.ai-lab/
   runs/                          # canonical run records
      <run-id>/
         run.json                   # top-level run metadata and mode
         timeline.ndjson            # ordered audit events
         brief.md                   # run input
         plan.md                    # approved execution plan
         report.md                  # final human review report
         orchestrator/              # orchestrator logs and status
         steps/                     # execution steps and their attempts
            step-001/
               worker-001/
               validator-001/
            step-002/
               worker-001/
               validator-001/
   benches/                       # isolated execution checkouts for repo-modifying runs
      <run-id>/
```

Creation rules:

- the wrapper creates `.ai-lab/`, `.ai-lab/runs/`, `.ai-lab/runs/<run-id>/`,
   `run.json`, and `timeline.ndjson`
- the wrapper creates `.ai-lab/benches/<run-id>/` only when a run needs an
   isolated repo-modifying checkout
- the brief and plan must exist before execution begins
- the orchestrator creates `orchestrator/`, `steps/`, step directories, and
   per-invocation directories as execution proceeds
- the reporter creates `report.md`

## Run Contract

Each Lab run should create a deterministic run directory under
`.ai-lab/runs/<run-id>/`.

The run directory is the canonical record of that run.

The minimum run contract is:

- `brief.md`: the brief given to Lab
- `plan.md`: the executable plan generated from the brief
- `run.json`: run metadata and top-level status
- `timeline.ndjson`: ordered run events for auditability
- `report.md`: final human review report
- `orchestrator/`: orchestrator logs and status
- `steps/`: execution steps and their worker and validator attempts

The wrapper should create the run directory itself and initialize the top-level
artifacts that exist before planning or execution begins.

At minimum, wrapper-created run artifacts are:

- `run.json`
- `timeline.ndjson`

Other top-level artifacts are created during the run lifecycle:

- `brief.md`: created or copied in when a brief is provided
- `plan.md`: created during planning
- `report.md`: created during reporting

Role-specific directories such as `orchestrator/` and `steps/` should be
created dynamically according to the directory layout and creation timing rules
above.

The run contract should preserve enough information to answer at least these
questions after the fact:

- how many agent instances were invoked
- in what order they were invoked
- which artifacts and logs were produced by each invocation
- which validation result corresponded to which worker attempt
- why a step was retried, blocked, or completed

For runs that modify project files, the run record should also identify the
corresponding bench and whether the run operated in artifact-only or
repo-modifying mode.

For artifact-only runs, no bench is required.

## Invocation Contract

Each agent invocation should have its own directory and must not overwrite a
previous invocation of the same role.

At minimum, each invocation should preserve:

- the agent role or type
- the task-specific prompt used for that invocation
- the input artifact references or copies needed for that invocation
- a log file for that invocation
- any output artifacts created by that invocation
- a status message or status file returned to the orchestrator

This applies to worker and validator invocations alike.

The orchestrator may revise prompts between step attempts, but each revised invocation
must remain separately inspectable.

The invocation layout should follow the `.ai-lab` directory rules defined
above.

## Agent Model

The orchestrator is itself an agent.

The orchestrator agent is expected to:

- read the brief and plan files from workspace state
- generate the executable plan artifact
- decide which specialized agents to invoke
- delegate work to those agents
- collect outputs
- trigger validation work
- continue iteration until completion criteria are met
- hand off to a reporting agent at the end

This design does not assume a hard-coded workflow engine as the primary source
of orchestration logic.

The Lab should remain as portable as practical. Runtime-specific assumptions
should stay near the execution layer rather than being spread across every
artifact and prompt.

## Agent Capability Tiers

Not all agents need the same level of access.

The system assumes three broad capability tiers:

1. Artifact-only agents
   - read and write files only
2. Limited-execution agents
   - mostly file-based, with access to selected tools or commands
3. Full-execution agents
   - can use a dedicated execution environment when required

Sandboxed execution is optional and role-dependent, not universal.

## Reusable Agent Definitions

Specialized agent definitions should be defined once and reused where useful,
but different project instances may carry materially different agent rosters.

Project work should keep run-specific state local to the workspace, while
shared patterns and definitions can live in repo-owned canon.

This design prefers repo-owned canon with disposable live instances.

Runtime-specific bindings may differ across runtimes in the future, but the Lab
repo should remain the canonical home for the portable parts of the system.

## Planning Boundary

The design is:

- a brief is provided
- Lab produces the executable plan
- execution runs from the approved plan

Planning may be implemented as behavior of the orchestrator or as a dedicated
planning role.

## Brief Contract

A brief is structurally flexible but semantically constrained.

Lab should not require one exact template, but a valid brief must make these
meanings recoverable:

- objective: the outcome the run is trying to produce
- scope: what is in bounds and out of bounds
- success criteria: how completion should be judged
- target surface: the project, path, subsystem, or artifact to act on when not
   already obvious
- constraints: prohibitions, safety limits, or required boundaries
- inputs: the primary files, documents, or prior artifacts the run should treat
   as source context

These may be expressed as headings, bullets, prose, or a mixture.

If one or more required meanings are absent or materially ambiguous, Lab should
request clarification rather than invent missing brief content.

## Plan Contract

The plan is structurally standardized and should use a fixed section order.

At minimum, a valid `plan.md` should include these sections in this order:

1. Objective
2. Scope
3. Assumptions
4. Execution Mode
5. Target Surface
6. Execution Sequence
7. Success Criteria
8. Expected Final Artifacts
9. Stop Conditions

Each section must be explicit enough for human review and resumable execution.

`Execution Sequence` should describe the run as an ordered series of
orchestrator-dispatched execution units rather than as generic prose steps.

At minimum, each execution step should identify:

- the task to perform
- the target agent profile
- the required inputs
- the expected outputs
- how the step will be validated
- what should happen if validation fails

`Success Criteria` should define completion at the run level, not just at the
step level.

`Expected Final Artifacts` should identify the outputs the run is expected to
create or update by the end of execution.

`Stop Conditions` should identify when execution must pause for review,
clarification, or safety.

The plan validator may eventually enforce this structure through a schema or
equivalent machine-readable contract, but the canonical source of truth for the
plan shape is this design document.

## Execution Loop

The intended loop is:

1. the orchestrator provisions a worker invocation with role instructions,
   task-specific prompt, and required input artifacts
2. the worker produces a log, output artifacts, and a status result
3. the orchestrator provisions a validator invocation against the worker output
4. the validator produces a log, validation result, and a status result
5. if validation fails and retry conditions allow it, the orchestrator updates
   the next worker prompt and records a new attempt without overwriting
   prior attempts
6. when completion criteria are met, the reporter produces the final report

The execution loop is control flow. The run directory should still organize
work primarily by planned execution step rather than by abstract retry loop.

## Execution Isolation

Parallel agents should not share the same writable execution environment.

Where agents need real execution capability, each parallel execution unit should
have its own isolated working area and should write logs and artifacts only to
its designated output locations.

For repo-modifying runs, the preferred isolated working area is a run-specific
bench under `.ai-lab/benches/<run-id>/`.

## Review Flow

The high-level flow is:

1. A brief is provided to Lab.
2. Lab generates an executable plan from that brief.
3. The plan is reviewed.
4. Lab executes the approved plan using subagents as needed.
5. Preserve logs, artifacts, and validation outputs in the workspace.
6. Produce a final report for review.

## Open Questions

The design still leaves open:

- exact directory layouts
- exact agent roster
- exact gate rules
- exact cleanup policy
- exact sandbox implementation
- the exact portability boundary between Lab canon and runtime-specific binding