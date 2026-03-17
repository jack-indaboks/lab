# Lab Docs

This document defines the roles of the core project documents and the rules for
maintaining them.

## Document Roles

- `README.md`: current state and current usage surface
- `DESIGN.md`: intended final design of the system
- `ROADMAP.md`: live work milestones and release milestones between the current
  state and the design vision
- `CHANGELOG.md`: completed changes, including roadmap updates
- `DOCS.md`: maintainer-facing documentation rules and document boundaries

## Update Discipline

- Public-facing project content belongs in the project documents, not in
  maintainer notes.
- Maintainer guidance about how to update the docs belongs here.
- Final decisions belong in `DESIGN.md`.
- Confirmed intermediate steps belong in `ROADMAP.md`.
- Completed changes belong in `CHANGELOG.md`.

## Changelog Rules

- `CHANGELOG.md` is append-only.
- Add new entries; do not rewrite prior history except to correct clear factual
  errors.
- Do not add changelog entries for routine roadmap checkbox changes or wording
  cleanup unless they reflect a substantive project decision or completed body
  of work.

## Roadmap Rules

- `ROADMAP.md` is a live checklist, not a historical record.
- Tasks are checked off in `ROADMAP.md` as they are completed.
- Completed work and roadmap updates are recorded in `CHANGELOG.md`.
- Completed phases do not remain in `ROADMAP.md`.
- When a phase is complete, remove it from `ROADMAP.md` and release if
  applicable.

### Open Questions

- Questions always begin in chat.
- Only explicitly tabled unresolved decisions belong in the `Open Questions`
  section of `ROADMAP.md`.
- Nothing is added to `Open Questions` without explicit direction from the
  project owner.
- Random ideas, clarifications, and speculative branches do not belong there.