# Lab Development

This document defines maintainer-facing development workflow for the Lab source repo.

Use this file for:
- source-of-truth maintainer workflow
- source and projection workflow
- testing and debugging workflow
- document-role rules and update discipline

## Document Roles

- `README.md`: current state and current usage surface
- `DESIGN.md`: intended final design of the system
- `ROADMAP.md`: live work milestones and release milestones between the current state and the design vision
- `CHANGELOG.md`: completed changes, including roadmap updates
- `DEVELOPMENT.md`: maintainer-facing workflow, testing practice, and document boundaries

## Source And Projection Workflow

Lab development uses two surfaces:
- the canonical Lab source repo
- a disposable project-local `.opencode/` projection used to exercise Lab in a real target repo

The canonical source repo is the source of truth.
The disposable projection is a test surface, not a second canon.

Default rule:
- fix durable Lab behavior in the canonical source repo
- use the disposable projection to reproduce bugs and test behavior in realistic downstream context

When the cause of a bug is still uncertain, use this workflow:

1. Reproduce the bug in the disposable project-local projection.
2. Make the smallest experimental fix in the projection.
3. If the fix proves correct and reflects intended Lab behavior, immediately upstream the exact change to the canonical source repo.
4. Refresh the disposable projection from source.
5. Re-test from the refreshed projection, not from the hand-edited projection.

Rules:
- do not leave durable behavior changes only in a disposable projection
- do not treat projection-local success as canonical success until the refreshed projection reproduces it from source
- use projection-only edits for investigation, not as a shadow fork of the source repo

## Testing And Debugging Workflow

- prefer realistic project-local testing over abstract prompt review once a behavior reaches runtime questions
- do not resume end-to-end testing until execution-capable roles are contained by filesystem masking or an equivalent sandbox boundary
- do not treat the live project root as the normal agent workspace; the run directory is the intended laboratory surface for every run, with `record/` and `bench/` serving different roles inside it
- when a failure is ambiguous, isolate the smallest failing step before widening the fix
- treat permission failures, missing artifacts, and state-corruption issues as first-class bugs rather than operator noise
- for execution-capable Lab agents, broad standard-tool access is acceptable only inside containment; outside containment, testing stops rather than normalizing broader host access
- for unattended runs, `ask` is not an acceptable capability model; use declared allow/deny profiles and projection-drift checks instead
- preserve auditability: debugging should make the system easier to inspect, not more magical
- after confirming a fix in a projection, re-test from a refreshed projection sourced from canon

## Documentation Update Discipline

- public-facing project content belongs in the project documents, not in maintainer notes
- maintainer guidance about how to update the docs belongs here
- final decisions belong in `DESIGN.md`
- confirmed intermediate steps belong in `ROADMAP.md`
- completed changes belong in `CHANGELOG.md`

## Changelog Rules

- `CHANGELOG.md` is append-only
- add new entries; do not rewrite prior history except to correct clear factual errors
- do not add changelog entries for routine roadmap checkbox changes or wording cleanup unless they reflect a substantive project decision or completed body of work
- AI drafting workflow is: discuss the concept in chat, draft language in the document, refine the language in chat while editing the document, then add a changelog entry only after the wording is accepted

## Roadmap Rules

- `ROADMAP.md` is a live checklist, not a historical record
- tasks are checked off in `ROADMAP.md` as they are completed
- completed work and roadmap updates are recorded in `CHANGELOG.md`
- completed phases do not remain in `ROADMAP.md`
- when a phase is complete, remove it from `ROADMAP.md` and release if applicable

## Open Questions

- questions always begin in chat
- only explicitly tabled unresolved decisions belong in the `Open Questions` section of `ROADMAP.md`
- nothing is added to `Open Questions` without explicit direction from the project owner
- random ideas, clarifications, and speculative branches do not belong there