# Lab Design

## Purpose

This document describes the intended design of Lab as a containerized, remote-execution agent laboratory. Lab takes a brief, generates an executable plan, carries out the work inside an isolated bench within a containerized runtime, validates results as the run progresses, loops through revised attempts when needed, and preserves a durable run record for review in the project workspace.

## Goal

Provide a file-native agent laboratory where:

- input begins with a brief
- Lab generates an executable plan from that brief
- Lab ships as a Docker image and all real Lab functionality lives inside the container
- the client does not need OpenCode installed locally
- execution happens inside a containerized Lab runtime rooted in a prepared bench
- OpenCode is used as the per-process execution substrate inside the run root
- the container is accessed over SSH
- a thin client-side wrapper handles ingress, egress, and operator convenience without owning Lab functionality
- the real workspace remains the durable operator-facing home for exported run state, logs, artifacts, and reports
- an orchestrator agent provisions specialized subagents as needed
- agents operate inside a controlled in-container developer work surface
- most agents work only with files, while a smaller set may use tools or contained shell execution
- output ends with a run report backed by preserved logs

## Architecture Overview

Lab is a remote execution system packaged as a Docker image.

- the Lab runtime lives inside a Docker container
- the container is reachable over SSH
- the client-side wrapper copies workspace inputs into the runtime
- the Lab runtime executes entirely inside the container
- the wrapper copies the run directory back out into the real workspace after execution

The system has five major parts:

1. client-side project workspace
2. client-side wrapper and transfer surface
3. Python Lab control layer inside the container
4. containerized Lab runtime
5. internal agent runtime assembled from OpenCode inside the run-scoped container workspace

The container boundary provides the execution environment:

- execution-capable work happens entirely inside the container
- the runtime can expose broad execution capability without exposing the client environment
- the container can run anywhere as long as it is SSH-reachable
- the client remains responsible only for transport and durable workspace synchronization

## System Boundaries

The client-side wrapper is a transport surface, not a second Lab runtime.

Its responsibilities are:

- copying project contents and config surfaces into the containerized runtime
- invoking the remote Lab command surface over SSH
- copying run outputs back into the real workspace
- optionally exposing remote inspection paths for the operator

It must not own planning, orchestration, validation policy, or run-state semantics.

It must not require direct access to the contained runtime's internal control flow beyond remote invocation and file transfer.

The wrapper boundary is tested by reduction to standard transport primitives. If a wrapper function cannot be reduced to remote invocation or file transfer over `ssh`, `scp`, or equivalent mechanisms, it does not belong to the wrapper.

The contained Lab runtime owns all real Lab functionality.

Its responsibilities are:

- creating and managing runs inside the container
- executing planning and run workflows
- invoking OpenCode per process inside each run root
- preserving run state, logs, and artifacts until they are exported

It must not depend on direct access to the client environment.

Lab ends at the SSH-reachable container boundary. Host-specific scaffolding such as Lima, host mounts, and local port-forward arrangements are environment details.

## Workspace And Run Surfaces

The project workspace is the durable operator-facing state surface.

Examples of state stored in the workspace:

- design docs
- briefs
- roadmaps
- prompts and context files
- logs
- validation outputs
- reports

The project workspace is not a transient cache. It is the persistent exported record of a run after synchronization from the contained runtime.

During execution, the live run state exists inside the container. The durable operator-facing record exists in the real workspace after export.

For the POC:

- the whole project workspace is copied into the container for simplicity
- the copied project root becomes the bench root for the run
- Lab operates directly on that copied tree
- the whole remote run directory is copied back out to `.ai-lab/<run-id>/` when the run ends
- there is no bidirectional sync during execution

In project instances, this design assumes a three-part split:

- canonical Lab source
- user-editable runtime definitions
- contained Lab runtime plus durable run state

Every run gets a run-rooted workspace. Each run directory contains both the durable run record and the bench work surface.

The naming model is:

- `lab`: canonical repo
- `lab` CLI: the user-facing command surface
- user-editable `.opencode/`: runtime definitions, custom agents, and related OpenCode-native configuration consumed by Lab
- client-side wrapper: optional convenience layer for SSH-based ingress, egress, and inspection
- Python control layer: the in-container component that owns run setup, execution, and artifact exposure
- `.ai-lab`: durable run state and exported artifacts for operator inspection
- `.ai-lab/<run-id>/record/`: durable run record for a run
- `.ai-lab/<run-id>/bench/`: isolated execution checkout and agent workspace for a run
- `.ai-lab/<run-id>/artifacts/`: exported outputs and other preserved run products

Runtime state should use deterministic run-id-based subdirectories in the form `YYYY-MM-DD-HH-MM_slug`, using a local timestamp without a timezone suffix.

## Runtime Model

The Python control layer inside the container is responsible for:

- loading user-editable runtime definitions
- creating runs, benches, and top-level run artifacts
- materializing source context into the in-container bench
- running the orchestrator agent
- allowing the orchestrator agent to invoke specialized subagents
- establishing the run-scoped execution workspace
- carrying out unattended execution once a plan is approved for run
- exposing logs, bench state, and run artifacts for operator inspection after execution

The Lab command surface is exposed through `lab` inside the container. A client-side `lab` wrapper may mirror that command surface, but it remains a remote transport surface.

The contained run workspace provides the full execution surface for the run. Execution is default-enabled inside the container and constrained by the run-scoped workspace rooted at the current `/runs/<run-id>/` directory.

The containment boundary is the containerized Lab runtime and its in-container bench. Unattended execution relies on that container boundary plus the run-scoped execution root.

OpenCode is the internal execution substrate for Lab. Lab invokes OpenCode per process inside the current run root.

The current execution model assumes broad tool availability, including shell access, inside the container. The controlling safety boundary is the disposable container plus the requirement that OpenCode operates inside `/runs/<run-id>/` for the active run.

## Canonical POC Runtime Model

The canonical POC runtime model is:

- copy the whole project workspace into the container
- place the copied project directly at the allocated bench root for the run
- execute Lab directly against that copied tree
- copy the whole run directory back out to `.ai-lab/<run-id>/` in the real workspace when the run ends
- reuse a long-lived container across runs when convenient during development
- keep the container disposable; the architecture must not depend on long-lived container state
- allow multiple runs in one running container as long as each run is isolated under its own `/runs/<run-id>/` root
- keep execution process-per-run even when the container is shared across runs
- prefer a general troubleshooting shell over a forced `lab`-only SSH target during development
- reserve a more locked-down `lab`-first SSH surface for later hardening
- default-enable tools inside the container rather than curating a narrow toolbox
- scope OpenCode execution to `/runs/<run-id>/` for the active run

For the POC, there is no bidirectional sync during execution. Inspection can happen over SSH, but run-state export happens at the end of the run.

The remote runtime is architecture-first and location-agnostic. The container may run locally, in a VM, or in cloud infrastructure as long as the wrapper can reach it over SSH.

User-editable OpenCode-native configuration remains important because operators need to define custom agents and similar behavior without rebuilding the container image.

Lab exposes `.ai-lab` as the durable run surface visible to the operator.

The bench is the laboratory work surface.
Execution takes place in the contained bench.

## Wrapper Invocation Contract

For the POC, the client-side wrapper is expected to drive runs through a simple SSH and SCP sequence.

### Planning Sequence

1. Allocate or resolve the `run-id`.
2. Ensure the remote `/runs/<run-id>/` root exists.
3. Copy the whole workspace, including the brief, into `/runs/<run-id>/bench/`.
4. Invoke `lab plan <run-id>` over SSH.
5. Await completion by polling remote run state.
6. Copy the generated plan back into the real workspace as a review artifact.

### Execution Sequence

1. Re-copy the whole workspace into `/runs/<run-id>/bench/`, including the approved plan and any host-side changes made during plan review.
2. Invoke `lab run <run-id>` over SSH.
3. Await completion by polling remote run state.
4. Copy the full remote `/runs/<run-id>/` directory back into `.ai-lab/<run-id>/` in the real workspace.

### Required Wrapper Behaviors

- planning and execution use the same `run-id`
- the wrapper treats the remote run root as the source of truth during execution
- polling should read explicit remote run-state artifacts such as `record/run.json` and `record/timeline.ndjson`, rather than relying only on process attachment
- the second workspace copy is authoritative for execution and is expected to include plan-review changes
- for the POC, no mid-run synchronization is required

### POC Transfer Scope

For the POC, transfer behavior is intentionally coarse-grained:

- ingress copies the whole workspace into the bench
- plan egress copies the generated plan out for review
- final egress copies the whole run root out for inspection and retention

Future optimizations may narrow transfer scope, but the POC assumes whole-workspace ingress and whole-run export.

## .ai-lab Contract

`.ai-lab/` is the generated runtime surface for a Lab-operated project.

Expected structure:

```text
.ai-lab/
   <run-id>/
      record/                     # durable run record
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
      bench/                      # mandatory isolated execution checkout and agent workspace
      artifacts/                  # exported outputs and preserved run products
```

For the POC, this exported `.ai-lab/<run-id>/` directory is a copy of the full remote `/runs/<run-id>/` directory.

The corresponding in-container run layout is:

```text
/runs/
   <run-id>/
      record/
      bench/
      artifacts/
```

Creation rules:

- the Python control layer creates `.ai-lab/`, `.ai-lab/<run-id>/`, `.ai-lab/<run-id>/record/`, `.ai-lab/<run-id>/bench/`, `record/run.json`, and `record/timeline.ndjson`
- the Python control layer creates the corresponding remote `/runs/<run-id>/record/`, `/runs/<run-id>/bench/`, and `/runs/<run-id>/artifacts/` directories inside the container
- the brief and plan must exist before execution begins
- the orchestrator creates `record/orchestrator/`, `record/steps/`, step directories, and per-invocation directories as execution proceeds
- the reporter creates `record/report.md`

## Run Contract

Each Lab run should create a deterministic run directory under `.ai-lab/<run-id>/`.

The run directory is the canonical record of that run.

The minimum run contract is:

- `record/brief.md`: the brief given to Lab
- `record/plan.md`: the executable plan generated from the brief
- `record/run.json`: run metadata and top-level status
- `record/timeline.ndjson`: ordered run events for auditability
- `record/report.md`: final human review report
- `record/orchestrator/`: orchestrator logs and status
- `record/steps/`: execution steps and their worker and validator attempts
- `bench/`: the run bench and agent work surface

 The Python control layer creates the run directory and initializes the top-level artifacts that exist before planning or execution begins.

At minimum, control-plane-created run artifacts are:

- `record/run.json`
- `record/timeline.ndjson`

Other top-level artifacts are created during the run lifecycle:

- `record/brief.md`: created or copied in when a brief is provided
- `record/plan.md`: created during planning
- `record/report.md`: created during reporting

Role-specific directories such as `record/orchestrator/` and `record/steps/` should be created dynamically according to the directory layout and creation timing rules above.

The run contract should preserve enough information to answer at least these questions after the fact:

- how many agent instances were invoked
- in what order they were invoked
- which artifacts and logs were produced by each invocation
- which validation result corresponded to which worker attempt
- why a step was retried, blocked, or completed

For runs that modify project files, the run record should identify the corresponding run bench and whether the run operated in any narrower execution sub-mode defined by the plan.

The bench is required even when the run is primarily file-native.

### Remote State Contract

The remote wrapper-facing state contract is intentionally small.

At minimum, `record/run.json` should expose:

- `run_id`: the deterministic run identifier
- `phase`: one of `planning` or `execution`
- `status`: one of `initializing`, `running`, `ready_for_review`, `completed`, `blocked`, or `failed`
- `updated_at`: last state update timestamp
- `bench_path`: the active remote bench path for the run
- `execution_mode`: present when execution has begun and the mode is known

The wrapper should treat `record/run.json` as the primary polling surface.

At minimum, `record/timeline.ndjson` should append ordered events using a stable event name plus a concise message. The minimum event vocabulary is:

- `run_initialized`
- `workspace_staged`
- `planning_started`
- `planning_completed`
- `planning_failed`
- `execution_started`
- `step_started`
- `step_completed`
- `validation_failed`
- `run_blocked`
- `run_completed`
- `run_failed`

The timeline is a supporting audit surface. It gives the wrapper and the operator progress detail beyond the top-level polling state.

### Terminal Conditions

For planning:

- terminal success is `phase=planning` and `status=ready_for_review`, with `record/plan.md` present
- terminal failure is `phase=planning` and `status=blocked` or `status=failed`

For execution:

- terminal success is `phase=execution` and `status=completed`, with `record/report.md` present
- terminal failure is `phase=execution` and `status=blocked` or `status=failed`

The wrapper should stop polling when a terminal condition is reached.

## Invocation Contract

Each agent invocation should have its own directory and must not overwrite a previous invocation of the same role.

At minimum, each invocation should preserve:

- the agent role or type
- the task-specific prompt used for that invocation
- the input artifact references or copies needed for that invocation
- a log file for that invocation
- any output artifacts created by that invocation
- a status message or status file returned to the orchestrator

This applies to worker and validator invocations alike.

The orchestrator may revise prompts between step attempts, but each revised invocation must remain separately inspectable.

The invocation layout should follow the `.ai-lab` directory rules defined above.

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

This design uses agent-driven orchestration rather than a hard-coded workflow engine.

The Lab remains as portable as practical. Runtime-specific assumptions stay near the execution layer.

## Responsibility Boundaries

The CLI surface, Python control layer, orchestrator, and subagents have distinct responsibilities. These boundaries keep ownership clear, avoid duplicated state management, and prevent prompt logic from becoming the accidental source of truth.

### CLI Responsibilities

The CLI surface owns command invocation and operator ergonomics.

The CLI stays thin and forwards the Lab command surface to the Python control layer.

### Python Control Layer Responsibilities

The Python control layer owns run setup, containment, execution, and artifact exposure.

At minimum, the Python control layer is responsible for:

- creating `.ai-lab/` and `.ai-lab/<run-id>/`
- creating `.ai-lab/<run-id>/record/` and `.ai-lab/<run-id>/bench/`
- initializing `record/run.json` and `record/timeline.ndjson`
- materializing source context into the in-container bench
- ensuring the orchestrator is launched with an unambiguous current run context
- ensuring execution happens inside the contained bench work surface
- exposing run artifacts, logs, and bench state for inspection after execution
- ensuring OpenCode execution is scoped to the active `/runs/<run-id>/` root

### Orchestrator Responsibilities

The orchestrator owns run-level interpretation, delegation, and continuity once the Python control layer has established the run.

At minimum, the orchestrator is responsible for:

- interpreting `record/brief.md` in planning mode
- producing or revising `record/plan.md`
- updating `record/run.json` and `record/timeline.ndjson` as the run progresses
- creating and managing `record/orchestrator/` and `record/steps/`
- deciding which specialized agent to invoke for each planned step
- translating validator outcomes into control-flow decisions
- recording durable clarification requests and blocked states
- ensuring `record/report.md` exists when the run completes or stops in a review-worthy state

The orchestrator maintains top-level run state unless that responsibility is explicitly delegated.

### Subagent Responsibilities

Subagents own only the scoped work assigned to them by the orchestrator.

At minimum, subagents are responsible for:

- carrying out the specific assignment they were given
- writing outputs, logs, and status artifacts for their own invocation
- staying within the designated scope of the current step
- returning enough information for the orchestrator to make the next decision

Subagents operate within the scope assigned by the orchestrator.

### Authority Model

The CLI surface invokes the run.
The Python control layer establishes the run.
The orchestrator manages the run.
The subagents execute within the run.

When responsibility is ambiguous, prefer the narrower authority boundary.

## Execution Scope

Containment is mandatory for execution-capable roles. Execution happens inside the containerized Lab runtime, rooted in the in-container bench for the current run.

The runtime exposes broad tool and shell capability inside the container, while OpenCode remains scoped to the active `/runs/<run-id>/` workspace.

The safety model is therefore:

- broad execution capability is acceptable inside the container
- the active run root is the intended writable execution boundary
- each run owns its own isolated `/runs/<run-id>/` tree
- the container is disposable and can be recreated from the image when needed

## Reusable Agent Definitions

Specialized agent definitions should be defined once and reused where useful, but different project instances may carry materially different agent rosters.

Project work should keep run-specific state local to the workspace, while shared patterns and definitions can live in repo-owned canon.

This design uses repo-owned canon with user-editable runtime definitions and disposable live instances.

Runtime-specific bindings may differ across runtimes, but the Lab repo remains the canonical home for the portable parts of the system.

The control path is Python-based. The CLI stays thin by forwarding the Lab command surface into the contained runtime.

## Planning Boundary

The design is:

- a brief is provided
- Lab produces the executable plan
- execution runs from the approved plan

Planning is owned by the orchestrator.

## Brief Contract

A brief is structurally flexible but semantically constrained.

Lab should not require one exact template, but a valid brief must make these meanings recoverable:

- objective: the outcome the run is trying to produce
- scope: what is in bounds and out of bounds
- success criteria: how completion should be judged
- target surface: the project, path, subsystem, or artifact to act on when not already obvious
- constraints: prohibitions, safety limits, or required boundaries
- inputs: the primary files, documents, or prior artifacts the run should treat as source context

These may be expressed as headings, bullets, prose, or a mixture.

If one or more required meanings are absent or materially ambiguous, Lab should request clarification rather than invent missing brief content.

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

`Execution Mode` should be stated explicitly. Execution is bench-first and the bench is mandatory for every run. If the plan distinguishes sub-modes, that distinction must not weaken the requirement that the agent operates inside the run bench.

`Execution Sequence` should describe the run as an ordered series of orchestrator-dispatched execution units rather than as generic prose steps.

At minimum, each execution step should identify:

- the task to perform
- the target agent profile
- the required inputs
- the expected outputs
- how the step will be validated
- what should happen if validation fails

`Success Criteria` should define completion at the run level, not just at the step level.

`Expected Final Artifacts` should identify the outputs the run is expected to create or update by the end of execution.

`Stop Conditions` should identify when execution must pause for review, clarification, or safety.

The plan validator may eventually enforce this structure through a schema or equivalent machine-readable contract, but the canonical source of truth for the plan shape is this design document.

## Execution Loop

The intended loop is:

1. the orchestrator provisions a worker invocation with role instructions, task-specific prompt, and required input artifacts
2. the worker produces a log, output artifacts, and a status result
3. the orchestrator provisions a validator invocation against the worker output
4. the validator produces a log, validation result, and a status result
5. if validation fails and retry conditions allow it, the orchestrator updates the next worker prompt and records a new attempt without overwriting prior attempts
6. when completion criteria are met, the reporter produces the final report

The execution loop is control flow. The run directory should still organize work primarily by planned execution step rather than by abstract retry loop.

## Validator Result Policy

The validator should classify outcomes using these result levels:

- `approved`: criteria were checked and satisfied; proceed to the next planned step
- `provisional`: the result is acceptable to proceed in a bounded way, but explicit follow-up obligations remain
- `blocked`: the validator cannot responsibly judge or proceed because inputs, prerequisites, access, or interpretability are insufficient
- `failed`: criteria were checked and not met; the current step result is not acceptable

The distinction between `provisional` and `blocked` is important:

- `provisional` allows bounded continuation with caveats, remediation, or tighter downstream checks
- `blocked` does not allow progression until missing inputs, missing access, ambiguity, or other prerequisite gaps are resolved

The distinction between `blocked` and `failed` is also important:

- `blocked` means the validator could not make a responsible judgment
- `failed` means the validator made a judgment and the result did not satisfy the criteria

Validation history is always preserved in the run record. A `failed` result may cause the orchestrator to retry the current step with revised instructions, but it does not justify erasing or overwriting prior attempts.

At minimum, each validation result should include:

- `level`: one of `approved`, `provisional`, `blocked`, or `failed`
- `summary`: a concise judgment of the validation outcome
- `evidence`: the files, commands, observations, or other concrete basis for the judgment
- `issues`: the material problems, caveats, or missing prerequisites found
- `recommended_action`: the validator's recommended next action for the orchestrator; for `provisional` results, this is where the bounded continuation rule, remediation path, or follow-up obligation should be made explicit

The default orchestrator response is:

- `approved`: continue to the next planned step
- `provisional`: continue only with explicit caveats or bounded remediation
- `blocked`: stop progression and revise inputs, assumptions, access, or other prerequisites before retrying
- `failed`: retry the current step if retry policy allows; otherwise stop the run in failed state

## Report Contract

The final report is a human-facing decision-support artifact and should use a fixed section order.

At minimum, a valid `report.md` should include these sections in this order:

1. Outcome
2. Objective
3. Changes
4. Validation Status
5. Evidence
6. Unresolved Questions
7. Next Action

The report should be concise, operator-useful, and grounded in preserved run artifacts rather than chat memory.

In particular:

- `Outcome` should make completion, partial completion, blockage, or failure obvious in the opening lines
- `Changes` should summarize what was produced, modified, or decided
- `Validation Status` should summarize the highest-signal validation outcome across the run
- `Evidence` should point to the strongest supporting artifacts, logs, and validation outputs
- `Unresolved Questions` should identify what still needs human judgment or follow-up
- `Next Action` should recommend a specific next step for the operator with a clear rationale

## Execution Isolation

Parallel agents should not share the same writable execution environment.

Where agents need real execution capability, each parallel execution unit should have its own isolated working area and should write logs and artifacts only to its designated output locations.

For each run, the isolated working area is the run-specific `bench/` directory under `/runs/<run-id>/bench/` inside the contained Lab runtime. The exported `.ai-lab/<run-id>/bench/` directory is the copied-out durable record of that remote bench after execution.

The current isolation model is one run directory per run. Each run owns its own `record/`, `bench/`, and `artifacts/` directories, and execution-capable processes should treat that run root as their writable boundary.

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

- the exact client-visible relationship between `.opencode/`, `.ai-lab/`, and the containerized runtime
- exact agent roster
- exact gate rules
- exact cleanup policy
- the exact portability boundary between Lab canon and runtime-specific binding