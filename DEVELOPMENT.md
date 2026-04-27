# Lab Development

This document defines maintainer-facing development workflow for the Lab source repo.

Use this file for:
- source-of-truth maintainer workflow
- testing and debugging workflow
- document-role rules and update discipline

## Document Roles

- `README.md`: current state and public project overview
- `DESIGN.md`: intended design of Lab
- `ROADMAP.md`: live work phases and milestones toward the intended design
- `CHANGELOG.md`: completed changes, including roadmap updates
- `DEVELOPMENT.md`: maintainer-facing workflow, testing practice, and document boundaries

## Implementation Guidance

`DESIGN.md` and `ROADMAP.md` are the source of truth for the Lab surface under development.

When changing behavior:

- prefer changes that move the implementation toward the intended Lab design
- prefer subtraction over extension when code or structure no longer serves that design
- do not let incidental implementation details harden into project direction without being reflected in `DESIGN.md`

When a design question is unsettled, resolve the intended behavior in the project documents before treating an implementation detail as authoritative.

## Testing And Debugging Workflow

Favor tests and debugging steps that confirm the intended Lab behavior with the smallest useful check.

Rules:

- prefer the smallest test or inspection that confirms the current design intent
- prefer realistic end-to-end checks when validating behavior that is meant to define the supported Lab surface
- when a failure is ambiguous, isolate the smallest failing step before widening the fix
- treat permission failures, missing artifacts, and state-corruption issues as first-class bugs rather than operator noise
- when defining the Lab tool surface, prefer explicit tool contracts over ambient assumptions
- for execution-capable Lab agents, prefer ecosystem-provided capabilities over bespoke simulation work
- when an implementation detail conflicts with the current design, follow the current design
- preserve auditability: debugging should make the system easier to inspect, not more magical

## Documentation Update Discipline

- public-facing project content belongs in the project documents, not in maintainer notes
- maintainer guidance about how to update the docs belongs here
- final decisions belong in `DESIGN.md`
- confirmed intermediate steps belong in `ROADMAP.md`
- completed changes belong in `CHANGELOG.md`

## Changelog Rules

- `CHANGELOG.md` is append-only
- add new entries; do not rewrite prior history except to correct clear factual errors
- do not add changelog entries for routine roadmap checkbox changes or minor wording edits unless they reflect a substantive project decision or completed body of work
- AI drafting workflow is: discuss the concept in chat, draft language in the document, refine the language in chat while editing the document, then add a changelog entry only after the wording is accepted

## Roadmap Rules

- `ROADMAP.md` is a live checklist, not a historical record
- tasks are checked off in `ROADMAP.md` as they are completed
- completed work and roadmap updates are recorded in `CHANGELOG.md`
- completed phases do not remain in `ROADMAP.md`
- when a phase is complete, remove it from `ROADMAP.md` and release if applicable