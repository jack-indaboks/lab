# Lab Roadmap

This roadmap tracks the work milestones and release milestones between the current Lab scaffold and the design vision described in `DESIGN.md`.

## POC (`0.0.1`)

Goal: a fresh clone of the template can be configured, run end to end, and produce a usable report.

- [x] Define the initial brief contract and document the required meanings.
- [x] Define the initial plan contract and required sections.
- [x] Define the deterministic `.ai-lab` run directory contract.
- [x] Define minimal validator result levels and decision policy.
- [x] Define the minimum final report rubric for objective, changes, validation status, evidence, unresolved questions, and next action.
- [x] Define the CLI, control layer, orchestrator, and subagent boundary contract for run setup, state updates, delegation, and stopping behavior.
- [x] Tighten the first-pass agent prompts so each role has explicit read/write targets and stop conditions.
- [x] Implement the first `ai-lab` command surface around OpenCode.
- [x] Reframe the canon around the bench-first laboratory model.
- [x] Define the run-rooted workspace layout with `record/` and `bench/` subdirectories.
- [x] Converge architecture and containment.
  - Reflect the contained, bench-first runtime direction in canon.
  - Keep Lab's container setup separate from downstream project containers.
  - Keep track of the runtime requirements that will define Lab's canonical container surface later.
  - Reduce the remaining work in this phase to contained implementation rather than unresolved architecture.
  - [x] Establish Lab repo structure and docs for the POC implementation work.
    - [x] Define the minimal standalone repo shape for Lab as an application repo rather than a project-local `.opencode` projection.
    - [x] Add the Python project surface needed to run Lab directly after clone.
    - [x] Move the Lab executable into the Python control-layer entrypoint.
    - [x] Relocate Lab-owned OpenCode files into a repo-owned surface that does not assume project-root `.opencode` placement.
    - [x] Update docs to describe the standalone clone-install-run path.
- [ ] Establish the runtime and POC execution surface.
  - Put the contained Lab runtime in place as a real execution surface.
  - Make the CLI surface, contained runtime, and run-rooted workspace sufficient to support a bounded slice attempt.
  - Keep implementation work focused on the contained runtime path rather than later transport or packaging.
  - Use the run root and bench as the real execution boundary from the first unattended run.
  - Keep Lab's container setup isolated from downstream project infrastructure during implementation.
  - Record the concrete runtime requirements that will define Lab's canonical container surface later.
  - [x] Tighten the first-pass agent prompts so each role has explicit read/write targets and stop conditions.
  - [x] Implement the first `ai-lab` command surface around OpenCode.
  - [ ] Put the Python control layer in place around the run-rooted workspace layout.
    - [ ] Launch OpenCode per process from the run root.
    - [ ] Add projection-drift checks before unattended launch.
    - [ ] Make the run directory the workspace root for unattended runs.
    - [ ] Make the bench the execution boundary for unattended runs.
    - [ ] Keep the control path cross-platform rather than bash-dependent.
  - [ ] Define the unattended tool contract for contained runs.
    - [ ] Replace `ask`-based capability discovery with declared allow/deny profiles.
    - [ ] Fail before launch when the effective runtime capability profile is insufficient.
  - [ ] Assemble the MVP developer toolbox from the OpenCode ecosystem.
    - [ ] Evaluate which built-ins, plugins, MCP servers, commands, and skills are required for unattended Lab runs.
    - [ ] Define the minimum blessed toolbox for planning, validation, reporting, and bench-scoped implementation work.
    - [ ] Identify which required capabilities are already available from the ecosystem and which remain genuine gaps.
    - [ ] Keep the MVP toolbox curated and explicit rather than relying on ambient capability.
    - [ ] Prefer cross-platform capabilities in the blessed toolbox rather than bash-only assumptions.
    - [ ] If a workspace-scoped shell-like capability already exists in the ecosystem, evaluate it; do not build a bespoke one for MVP.
  - [ ] Produce a usable end-to-end run report from a fresh-clone template run.
    - [ ] Validate the Python control layer in a project-local `.opencode` instance.
    - [ ] Produce a usable `record/plan.md` from `ai-lab plan <brief>`.
    - [ ] Produce a usable `record/report.md` from `ai-lab run <slug>`.
    - [ ] Preserve logs, validation outputs, and invocation artifacts under `.ai-lab/<run-id>/record/`.
- [ ] Reproduce a single Digest slice.
  - Use one bounded Digest slice as the proof that the contained POC works on real project work.
  - Record what breaks, what generalizes, and what still belongs outside the POC.
  - [ ] Run one bounded Digest slice through Lab.
  - [ ] Produce the expected artifacts and validation outputs.
  - [ ] Document the remaining gaps to a fuller migration clearly.

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
- [ ] Refine run ingress and egress rules for copying project contents into the bench and returning result artifacts.
- [ ] Clarify the client-visible relationship between project-local `.opencode/`, `.ai-lab/`, and the contained runtime.

## Template Readiness (`0.1.0`)

Goal: first experimental release of the template for others to instantiate and try.

- [ ] Make the template structure and instance model clear for other users.
- [ ] Make CLI usage understandable without private context.
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

- [ ] Define the client-to-runtime transport for Lab runs.
- [ ] Capture the canonical container surface for a future turnkey Lab image.
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