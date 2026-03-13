# Lab Design

## Purpose

This document captures the first broad-strokes design for the Lab system.
It is intentionally lean. It records only decisions already made and leaves all
unresolved implementation detail out.

## Goal

Provide a file-native agent execution environment where:

- creative design work happens in VS Code with Copilot Chat
- execution happens through OpenCode
- the workspace remains the canonical home for sprint state, logs, artifacts,
  and reports
- an orchestrator agent provisions specialized subagents as needed
- most agents work only with files, while a smaller set may use tools or
  sandboxed execution
- final review happens from a high-level sprint report backed by preserved logs

## Core Shape

The system currently has four major parts:

1. VS Code workspace
2. OpenCode runtime
3. Optional execution environments for selected agents
4. Tool access through shell, MCP, and OpenAPI-compatible services where needed

## Workspace Role

The workspace is the canonical shared state surface.

Examples of state stored in the workspace:

- design docs
- sprint briefs
- roadmaps
- prompts and context files
- logs
- validation outputs
- reports

The workspace is not a transient cache. It is the persistent record of a sprint.

In project instances, this design assumes a three-part split:

- canonical Lab source
- runtime-specific binding
- generated project-local Lab runtime state

The current naming model is:

- `lab`: canonical repo
- active OpenCode binding: one current OpenCode-facing Lab projection, which
   may live in a project, in home config, as a symlink, or as a direct clone
- `.ai-lab`: generated run state inside the project being worked on

## Runtime Role

OpenCode is the current primary execution runtime.

OpenCode is responsible for:

- loading reusable agent definitions
- running the orchestrator agent
- allowing the orchestrator agent to invoke specialized subagents
- enforcing per-agent permissions and tool access
- carrying out unattended execution once a sprint is approved for run

The OpenCode binding is an instance projection, not the canonical source of Lab
behavior.

The location of that projection is flexible.

The location of `.ai-lab` is not: it belongs in the project being operated on.

## Agent Model

The orchestrator is itself an agent.

The orchestrator agent is expected to:

- read the sprint definition from workspace files
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

Project work should keep sprint-specific state local to the workspace, while
shared patterns and templates can live in repo-owned canon.

This design prefers repo-owned canon with disposable live instances.

Runtime-specific bindings may differ across runtimes in the future, but the Lab
repo should remain the canonical home for the portable parts of the system.

## Execution Isolation

Parallel agents should not share the same writable execution environment.

Where agents need real execution capability, each parallel execution unit should
have its own isolated working area and should write logs and artifacts only to
its designated output locations.

## Review Flow

The intended high-level flow is:

1. Design sprint in VS Code with Copilot Chat.
2. Save approved design/sprint files in the workspace.
3. Launch the current execution runtime against the same workspace.
4. Let the orchestrator agent execute the sprint using subagents.
5. Preserve logs, artifacts, and validation outputs in the workspace.
6. Produce a final sprint report in the workspace for review.

## Non-Goals For This Draft

This draft does not define:

- exact directory layouts
- exact file naming conventions
- exact agent roster
- exact gate rules
- exact cleanup policy
- exact sandbox implementation
- exact MCP/OpenAPI tool inventory
- the exact portability boundary between Lab canon and runtime-specific binding

Those belong in later design passes.

## Current Open Questions

- What should the first sprint filesystem contract look like?
- Which agent roles should be part of the initial shared canon?
- Which validators should be artifact-only versus execution-capable?
- How much cleanup should happen automatically after a sprint?
- What minimum reporting schema is needed for next-morning review?