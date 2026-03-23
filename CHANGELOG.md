# Lab Changelog

## 2026-03-13

- established the initial `lab` repository shape
- renamed the project from `Harness` to `lab`
- flattened the OpenCode-facing agent files to the repo-root config shape
- added initial `README.md` and `DESIGN.md`
- added `ROADMAP.md` and `CHANGELOG.md`
- documented the Lab canon / runtime binding / `.ai-lab` runtime state split
- documented the intended `ai-lab plan` and `ai-lab run` lifecycle
- added a lean `.gitignore`
- marked the current agent prompts as placeholder drafts
*Commit: 750b370 init*

## 2026-03-16

- clarified the roles of `README.md`, `DESIGN.md`, `ROADMAP.md`, and `CHANGELOG.md`
- refined `README.md` toward current-state and usage guidance
- refined `DESIGN.md` toward end-state architecture only
- overhauled `ROADMAP.md` into a live checklist with work milestones and release milestones
- added and refined the `Open Questions` section in `ROADMAP.md`
- added `DOCS.md` as the maintainer-facing home for document rules and update discipline
- moved maintainer-facing meta guidance out of the public-facing project documents
*Commit: f775ebe DOCS*

- replaced `sprint` terminology with `brief`, `run`, `loop`, and `report`
- removed the obsolete `templates/sprint/` scaffold
- added `templates/run/` as the canonical run-record scaffold
- documented the run contract, invocation contract, execution loop, and auditability requirements in `DESIGN.md`
- documented isolated repo-modifying execution checkouts under `.ai-lab/benches/`
- added `mode` and `bench` fields to the run metadata template
- removed the literal `templates/run/` scaffold and made wrapper-created run records the only source of run structure
- made `DESIGN.md` fully capture the top-level `.ai-lab` contract and wrapper-created versus runtime-created run artifacts
- added an explicit `.ai-lab` directory layout and creation-timing spec to `DESIGN.md`
- marked `CHANGELOG.md` as append-only in `DOCS.md`
*Commit: b597c6d cleanup*

- reviewed a reference implementation and added selected ideas to the roadmap
- defined brief invariants in `DESIGN.md` and added matching user-facing brief guidance to `README.md`
- defined the initial brief contract in `DESIGN.md`
- defined the initial plan contract in `DESIGN.md`
- updated the run directory contract in `DESIGN.md` to use step-oriented execution records under `.ai-lab/runs/<run-id>/steps/`
*Commit: cce5426 contracts*

## 2026-03-17

- defined validator result levels and default orchestration policy in `DESIGN.md`
- defined the basic validation response shape in `DESIGN.md`
- clarified the meaning of `recommended_action` for provisional validation results in `DESIGN.md`
- defined the minimum final report rubric in `DESIGN.md` and aligned `lab-reporter.md` to it
- added a wrapper-orchestrator-subagent boundary contract item to the POC roadmap ahead of prompt tightening and wrapper implementation
- defined the wrapper, orchestrator, and subagent boundary contract in `DESIGN.md` and aligned `lab-orchestrator.md` to it
- replaced the placeholder worker prompt with a scoped, artifact-aware prompt aligned to the boundary contract
- replaced the placeholder validator prompt with an evidence-driven prompt aligned to the validation policy and boundary contract
- renamed execution modes to `artifact` and `bench` and made planning mode set `Execution Mode` explicitly for wrapper bench provisioning
- replaced the placeholder reporter prompt with a synthesis-focused prompt aligned to the report contract and boundary model
- removed lab-planner.md in favor of a single orchestrator role that covers both planning and execution orchestration
*Commit: 769a6db prompts*

## 2026-03-23

- added the first shell-based `ai-lab` wrapper in `bin/ai-lab` with project-root resolution, `.ai-lab` run initialization, slug-based `run` lookup, and `git worktree` bench setup
- updated `.gitignore` to ignore project-local `.ai-lab/` runtime state
- refocused `README.md` into a user-facing installation and usage guide, including the project-local `.git` / `.opencode` / `.ai-lab` instance shape and current wrapper behavior
- revised `ROADMAP.md` so wrapper implementation is marked complete, POC remains milestone-oriented, and filesystem masking moves to Local Hardening
