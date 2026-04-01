# Lab Design

## Purpose

This document describes the intended final design of Lab: a CLI-first, file-native agent laboratory that takes a brief, generates an executable plan, carries out the work inside an isolated bench, validates results as the run progresses, loops through revised attempts when needed, and preserves a durable run record for review in the project workspace.

## Goal

Provide a file-native agent laboratory where:

- input begins with a brief
- Lab generates an executable plan from that brief
- Lab is provisioned and run by a Python control layer
- execution happens inside a containerized Lab runtime rooted in a prepared bench
- OpenCode is used as the per-process execution substrate inside the run root
- the project workspace remains the canonical home for run state, logs, artifacts, and reports
- an orchestrator agent provisions specialized subagents as needed
- agents operate inside a controlled in-container developer work surface
- most agents work only with files, while a smaller set may use tools or contained shell execution
- output ends with a run report backed by preserved logs

## Core Shape

The system has four major parts:

1. client-side project workspace
2. Python Lab control layer
3. containerized Lab runtime
4. internal agent runtime and toolbox assembled from OpenCode plus selected supporting capabilities

## Workspace Role

The project workspace is the canonical shared state surface.

Examples of state stored in the workspace:

- design docs
- briefs
- roadmaps
- prompts and context files
- logs
- validation outputs
- reports

The project workspace is not a transient cache. It is the persistent record of a run.

In project instances, this design assumes a three-part split:

- canonical Lab source
- user-editable runtime definitions
- contained Lab runtime plus durable run state

Every run gets a run-rooted workspace. Each run directory contains both the durable run record and the bench work surface.

The naming model is:

- `lab`: canonical repo
- `lab` CLI: the user-facing command surface
- user-editable `.opencode/`: runtime definitions, custom agents, and related OpenCode-native configuration consumed by Lab
- Python control layer: the component that owns run setup, execution, and artifact exposure
- `.ai-lab`: durable run state and exported artifacts for operator inspection
- `.ai-lab/<run-id>/record/`: durable run record for a run
- `.ai-lab/<run-id>/bench/`: isolated execution checkout and agent workspace for a run

Runtime state should use deterministic run-id-based subdirectories in the form `YYYY-MM-DD-HH-MM_slug`, using a local timestamp without a timezone suffix.

## Runtime Role

The Python control layer is responsible for:

- loading user-editable runtime definitions
- creating runs, benches, and top-level run artifacts
- materializing source context into the in-container bench
- running the orchestrator agent
- allowing the orchestrator agent to invoke specialized subagents
- enforcing per-agent permissions and tool access
- carrying out unattended execution once a plan is approved for run
- exposing logs, bench state, and run artifacts for operator inspection after execution

The Lab command surface is exposed through the `lab` CLI. The CLI remains thin and forwards operator intent from the client-side project workspace to the Python control layer without taking ownership of orchestration or run state.

The contained run workspace provides the developer toolbox for execution. Inside the container boundary, Lab may expose a broad developer toolbox, including shell access, while keeping execution confined to the in-container bench for the run.

The containment boundary is the containerized Lab runtime and its in-container bench. Unattended execution relies on that containment boundary and the declared runtime capability profile.

OpenCode is the internal execution substrate for Lab. Lab invokes OpenCode per process inside the current run root.

User-editable OpenCode-native configuration remains important because operators need to define custom agents and similar behavior without rebuilding the container image.

Lab exposes `.ai-lab` as the durable run surface visible to the operator.

The bench is the laboratory work surface.
Execution takes place in the contained bench.

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
```

Creation rules:

 the Python control layer creates `.ai-lab/`, `.ai-lab/<run-id>/`, `.ai-lab/<run-id>/record/`, `.ai-lab/<run-id>/bench/`, `record/run.json`, and `record/timeline.ndjson`
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
- failing closed when the effective runtime configuration does not match the expected unattended capability profile

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

## Agent Capability Tiers

Not all agents need the same level of access.

The system assumes three broad capability tiers:

1. Artifact agents
   - read and write files only
2. Limited-execution agents
   - mostly file-based, with an explicit declared toolbox inside the run-scoped workspace
3. Full-execution agents
   - can use a dedicated execution environment when required

Containment is mandatory for execution-capable roles. Execution happens inside the containerized Lab runtime, rooted in the in-container bench for the current run. Inside that contained environment, Lab may expose the tools and shell surface needed for the run.

For unattended runs, Lab provides a declared capability profile for the contained runtime and fails before launch when the effective runtime configuration does not match that profile.

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

For each run, the preferred isolated working area is the run-specific `bench/` directory under `.ai-lab/<run-id>/bench/` inside the contained Lab runtime.

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

- the exact client-side transport for invoking the contained runtime
- the exact mechanism for copying project contents into the bench and copying result artifacts back out
- the exact client-visible relationship between `.opencode/`, `.ai-lab/`, and the containerized runtime
- exact agent roster
- exact gate rules
- exact cleanup policy
- the exact portability boundary between Lab canon and runtime-specific binding