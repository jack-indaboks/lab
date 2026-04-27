# Lab Design

## Purpose

This document describes Lab as an instruction and tool-contract layer for autonomous agent work.

Lab defines how a delegated agent system should behave when asked to turn a scoped brief and a start state into a plan, a coordinated execution process, a validation-aware result, and a returned artifact set.

## Goal

Provide a Lab layer that produces this behavior:

- input begins with a scoped brief
- a start state is handed off with that brief
- an orchestrator turns the brief into an executable plan
- the orchestrator delegates specialized work to subagents as needed
- validator behavior is handled by validator agents and tools
- execution proceeds unattended through the agent platform Lab operates on
- output ends with returned artifacts plus a final report

## Definition

Lab is the combination of:

- canonical instructions
- agent role definitions
- tool contracts
- handoff expectations
- artifact expectations

Lab is expressed through the behavioral contract it imposes on the agent team that carries out the work.

Lab currently operates on agent-platform.

## Lab Run

A Lab run is a logical unit of work.

A Lab run begins when a scoped brief and start state are handed to Lab.

A Lab run ends when Lab returns:

- the plan produced for that work
- the generated artifacts
- the validator findings that matter for operator review
- the final report

## Canonical Flow

The intended Lab flow is:

1. A human scopes a unit of work.
2. That scoped work is handed to Lab with a brief and any required start-state files.
3. The orchestrator interprets the brief and produces a reviewable execution plan.
4. The orchestrator delegates specialized work to subagents as needed.
5. Validator agents and tools assess important outputs and feed their findings back into orchestration.
6. The orchestrator decides whether to proceed, revise, retry, or stop.
7. Lab returns the final artifact set and report.

The preferred long-term operator experience includes API-driven handoff from VS Code so a user can ask Copilot to send work to Lab without manual browser interaction.

API-driven handoff is part of the intended Lab surface, but the mechanism that enables it is not yet defined here.

## Instruction Surface

Lab's primary surface is instructions.

Those instructions should define at least:

- how briefs are interpreted
- how plans are produced
- how delegation is used
- how validator roles participate
- how artifacts are named or described for return
- how final reporting is structured
- when the orchestrator should stop, ask for clarification, or hand back results

The instructions are the main mechanism by which Lab shapes agent behavior.

## Agent Model

Lab assumes a role-based agent model.

At minimum, the design expects these logical roles:

- orchestrator
- worker
- validator
- reporter

These roles may map onto whatever execution model carries out the work.

The orchestrator is responsible for:

- interpreting the brief
- producing the plan
- deciding when to delegate
- deciding when validator input is needed
- integrating validator findings into the next decision
- deciding when the run is complete, blocked, or in need of clarification
- assembling or commissioning the final report

Worker roles are responsible for scoped execution.

Validator roles are responsible for assessing outputs with tools and evidence, then returning findings that the orchestrator can use.

Reporter behavior is responsible for producing a concise operator-facing account of the run outcome.

## Validation Model

Validation is primarily an agent-and-tool behavior.

That means:

- validator agents may be delegated like any other specialized role
- validators may call tools as needed
- validator findings inform orchestration rather than requiring a built-in workflow engine

The essential requirement is that validator output be legible enough for the orchestrator and operator to use.

## Tool Contract

Lab depends on declared tool contracts rather than ambient assumptions.

The tool layer should make clear:

- which tools are available to which Lab roles
- what each tool is for
- what output or side effects each tool is expected to produce
- what evidence a validator can rely on from those tools

The exact tool roster may vary by implementation.

The Lab design only requires that the tool contract be explicit enough to support repeatable orchestration and reviewable outcomes.

## Artifact Contract

Lab requires returnable artifacts.

At minimum, the operator should be able to retrieve:

- the brief as handed to the run, or an equivalent preserved input reference
- the plan produced from that brief
- the primary generated outputs
- the validator findings that materially shaped the outcome
- the final report

This design does not require one canonical on-disk run directory shape.

Artifact packaging and retrieval must be consistent enough for operator review, resumability, and downstream use.

## Handoff Contract

Lab assumes a handoff from a human-facing environment into the agent team carrying out the run.

The minimum handoff must include:

- the scoped brief
- the start state
- the intended objective
- any relevant constraints

The start state may be small or large.

Examples:

- one brief plus a few supporting files
- a document bundle
- a repository snapshot
- a whole project tree

The handoff may happen through:

- a UI
- an API
- an editor integration
- another platform-specific mechanism

The mechanism may vary. The canonical concern here is that the handoff preserve Lab's intended inputs and expectations.
