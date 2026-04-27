# Lab Roadmap

This roadmap tracks Lab work only.

This roadmap focuses on the Lab instruction layer, role definitions, tool contracts, validation behavior, artifact expectations, and workflow described in `DESIGN.md`.

## POC (`0.0.1`)

Goal: establish the full Lab skeleton end to end.

At this phase, Lab should be able to accept a brief and start state, produce a reviewable plan, proceed from an approved plan into execution, and return artifacts plus a final report. The focus is on establishing the complete working skeleton.

- [ ] Define the minimum brief contract.
- [ ] Define the minimum start-state handoff contract.
- [ ] Define the minimum plan contract for review.
- [ ] Define the minimum plan-acceptance step between planning and execution.
- [ ] Define the minimum final report contract.
- [ ] Define the minimum artifact return contract.
- [ ] Define the minimum orchestrator instructions.
- [ ] Define the minimum worker role instructions.
- [ ] Define the minimum validator role instructions.
- [ ] Define the minimum reporter behavior.
- [ ] Define the initial tool contract by role.
- [ ] Define the minimum validation behavior needed for end-to-end runs.
- [ ] Run Lab through the complete flow: brief -> plan -> approved plan -> execution -> artifacts -> report.
- [ ] Reproduce at least one bounded real-world work slice through that flow.
- [ ] Document the work needed to carry Lab from skeleton status into real project use.

## MVP (`0.1.0`)

Goal: make Lab useful for real projects while continuing to mature toward broader rollout.

At this phase, Lab should save time through repeatable real-project use. Agent definitions and tool contracts should be reliable enough for regular use on real work while the experience continues to mature.

- [ ] Refine the brief contract until it supports real project scoping without constant reinterpretation.
- [ ] Refine the plan contract until plans are reliably reviewable and actionable.
- [ ] Refine orchestrator behavior so delegation decisions are predictable enough for repeated use.
- [ ] Refine worker role definitions so common execution tasks succeed without excessive rework.
- [ ] Refine validator behavior so findings materially improve outcomes rather than adding noise.
- [ ] Refine reporter behavior so final reports are concise, legible, and useful for handback.
- [ ] Tighten tool contracts so role capabilities are explicit and dependable.
- [ ] Define how blocked work, retries, and clarification needs are surfaced during a run.
- [ ] Verify that Lab can complete repeated real-project slices with acceptable overhead.
- [ ] Verify that Lab's outputs are organized and reviewable enough for downstream use.
- [ ] Document the operating guidance for MVP use and the improvements targeted for v1.

## v1 (`1.0.0`)

Goal: make Lab complete and stable enough to roll out to other users and support as a real offering.

At this phase, beta learning should already be complete. Lab's core behavior should be stable, teachable, supportable, and ready for broader use.

- [ ] Stabilize the Lab usage model for broader adoption.
- [ ] Stabilize the Lab instruction set and role definitions for broader use.
- [ ] Stabilize the tool-contract surface that supported Lab depends on.
- [ ] Stabilize artifact and report expectations for supported use.
- [ ] Verify that Lab can be adopted outside the original author environment.
- [ ] Document the supported operating model clearly enough for rollout and support.
- [ ] Define which parts of Lab are canonical and which parts are expected to vary by deployment.
- [ ] Close the largest remaining gaps between real behavior and `DESIGN.md`.