# Lab

Lab is an instruction and tool-contract layer for autonomous agent work. It defines how a delegated agent system should turn a scoped brief and a start state into a plan, coordinated execution, validation-aware results, returned artifacts, and a final report.

Lab is defined through:

- canonical instructions
- agent role definitions
- tool contracts
- handoff expectations
- artifact expectations

Lab is expressed through the behavioral contract it imposes on the agent team carrying out the work. It currently operates on agent-platform.

## Status

Lab is transitioning from an earlier local control-layer approach to the current model described in `DESIGN.md` and phased in `ROADMAP.md`. The project is in the POC phase, and the new Lab surface is not yet operational.

At this stage, the repository should be read as the source of truth for the design, roadmap, role definitions, and implementation work for the new Lab surface.

## Intended Flow

The intended Lab flow is:

1. A person scopes a unit of work.
2. That work is handed to Lab with a brief and any required start-state files.
3. The orchestrator interprets the brief and produces a reviewable plan.
4. The plan is approved for execution.
5. The orchestrator delegates specialized work to subagents as needed.
6. Validator agents and tools assess important outputs and feed findings back into orchestration.
7. Lab returns the final artifact set and report.

The preferred long-term operator experience includes handing work off from VS Code into the agent platform without manual browser coordination.

Current POC work is focused on making this flow work end to end. `ROADMAP.md` tracks the remaining work.

## Related Documents

- `DESIGN.md` describes the intended Lab design.
- `ROADMAP.md` tracks POC, MVP, and v1 work.
- `DEVELOPMENT.md` defines maintainer-facing workflow and document roles.
- `CHANGELOG.md` records completed changes and accepted project decisions.
