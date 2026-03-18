# Lab Roadmap

This roadmap tracks the work milestones and release milestones between the current Lab scaffold and the design vision described in `DESIGN.md`.

## Open Questions

- Should planning be owned by the orchestrator or a dedicated planner role?

## POC (`0.0.1`)

Goal: a fresh clone of the template can be configured, run end to end, and produce a usable report.

- [x] Define the initial brief contract and document the required meanings.
- [x] Define the initial plan contract and required sections.
- [x] Define the deterministic `.ai-lab` run directory contract.
- [x] Define minimal validator result levels and decision policy.
- [x] Define the minimum final report rubric for objective, changes, validation status, evidence, unresolved questions, and next action.
- [x] Define the wrapper, orchestrator, and subagent boundary contract for run setup, state updates, delegation, and stopping behavior.
- [x] Tighten the first-pass agent prompts so each role has explicit read/write targets and stop conditions.
- [ ] Implement the first `ai-lab` wrapper around OpenCode.
  - [ ] Mask the OpenCode process filesystem so the repo is readable but writes are limited to the current run directory and bench when applicable.
- [ ] Make `ai-lab plan <brief>` generate a plan artifact from a brief.
- [ ] Make `ai-lab run <plan>` execute an approved plan and write run artifacts.
- [ ] Produce a usable end-to-end run report from a fresh-clone template run.

## Local Hardening

Goal: make the template reliable enough for repeated local use and clearer iteration.

- [ ] Refine the plan artifact format.
- [ ] Define the run metadata format.
- [ ] Define the validator result format.
- [ ] Define the report format for human review.
- [ ] Add a lightweight preflight registry for env requirements, protected paths, and mutation guardrails.
- [ ] Add a structured validation registry for default result handling and recommended checks.
- [ ] Add schemas for stable Lab registries once their shapes settle.
- [ ] Revise orchestrator, worker, validator, and reporter prompts based on POC findings.

## Template Readiness (`0.1.0`)

Goal: first experimental release of the template for others to instantiate and try.

- [ ] Make the template structure and instance model clear for other users.
- [ ] Make wrapper usage understandable without private context.
- [ ] Define the minimum setup steps for a new instance.
- [ ] Decide which narrow operator-facing commands belong beyond `plan` and `run`.
- [ ] Document current limitations and rough edges explicitly.
- [ ] Verify repeatable end-to-end use outside the original development environment.

## External Trial

Goal: learn from use in more than one downstream environment and project shape.

- [ ] Validate Lab against more than one project shape.
- [ ] Identify which parts of the agent roster are genuinely shared.
- [ ] Identify which parts should remain project-specific.
- [ ] Refine template guidance for project-level `.opencode` instances.
- [ ] Capture issues that only emerge outside the original development context.

## Release Hardening

Goal: turn lessons from downstream experimentation into a stronger template.

- [ ] Define the project-local server lifecycle for Lab runs.
- [ ] Improve continuity across editor restarts.
- [ ] Refine logging and artifact preservation.
- [ ] Add safer defaults for execution-capable roles.
- [ ] Add cleanup behavior for noisy runs.

## Portability Boundary

Goal: keep Lab canon portable while making runtime bindings clearer.

- [ ] Separate Lab canon from runtime-specific binding concerns more explicitly if needed.
- [ ] Document the minimum binding contract for additional runtimes.
- [ ] Decide whether runtime adapters should remain handwritten or become generated.

## Stable Release (`1.0.0`)

Goal: first stable, full-featured release of the template after local and downstream testing.

- [ ] Stabilize the command surface.
- [ ] Stabilize the instance model.
- [ ] Stabilize the run lifecycle and report expectations.
- [ ] Finalize the minimum supported template capabilities.
- [ ] Close the largest known gaps between the implementation and `DESIGN.md`.