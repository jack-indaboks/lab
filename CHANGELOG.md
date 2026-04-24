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
*Commit: 7f7278a first-executable*

- added explicit `glob` permission in `opencode.json` so noninteractive orchestrator runs do not auto-reject common file-discovery calls
- updated `lab-orchestrator.md` to read the project-local `.opencode/DESIGN.md` contract directly instead of discovering `DESIGN.md` by glob
- added guardrails in `lab-orchestrator.md` so wrapper-populated top-level run fields are not blanked during orchestration updates
- replaced `DOCS.md` with `DEVELOPMENT.md` as the maintainer-facing canon for development workflow, projection testing workflow, and document-update discipline
*Commit: 0aa48a5 DEVELOPMENT*

- changed the local permission baseline so execution-capable Lab agents get standard workspace shell access by default instead of one-off `bash` approvals
- aligned `DESIGN.md`, `DEVELOPMENT.md`, `lab-orchestrator.md`, `lab-worker.md`, and `lab-validator.md` to that standard-tool execution model
- moved filesystem containment back into the POC gate and paused end-to-end testing until execution-capable roles run inside a masked filesystem boundary or equivalent sandbox
- revised `DESIGN.md`, `DEVELOPMENT.md`, and `ROADMAP.md` so containment, not prompt gating, is the primary safety boundary for early testing
- revised the canon to make Lab explicitly bench-first: every run gets a bench, the bench is the intended laboratory work surface, and direct live-project execution is no longer treated as the normal model
- added POC work items for bench-rooted OpenCode sessions, declared headless tool contracts, removal of `ask`-based capability discovery, and projection-drift checks
- revised the `.ai-lab` layout to make each run self-contained under `.ai-lab/<run-id>/` with sibling `record/` and `bench/` subdirectories, and updated the runtime model so OpenCode sessions are rooted at the run directory
- aligned the README, design responsibilities, roadmap state, and agent prompts to the run-rooted `record/` plus `bench/` model so the canon now matches the pivot point cleanly
*Commit: 17b2eb4 mandatory bench pivot*

## 2026-03-30

- updated the roadmap to make the Python wrapper rewrite and OpenCode-ecosystem toolbox assembly explicit POC work, and removed the stale duplicate Python-wrapper item from Local Hardening
- clarified in the canon that Lab's product requirement is a curated, cross-platform developer toolbox assembled from the runtime ecosystem, with Python as the intended canonical control plane rather than bash-dependent wrapper behavior
- resolved the stale planner question by keeping planning with the orchestrator, and tightened containment language so unattended runs are rooted at the run directory without arbitrary host-shell access while any shell-like capability must come from the existing ecosystem rather than a bespoke MVP implementation
*Commit: e8e14b3 toolbox-version*

## 2026-03-31

- refined `DESIGN.md` to the current standalone Lab model: CLI-first, Python control layer, contained runtime, project-workspace language, and run-rooted `record/` plus `bench/` state
- reshaped `ROADMAP.md` around the contained architecture, the standalone repo transition, and the runtime-focused next POC block, and marked the design/containment phase complete
- defined the minimal standalone Lab source-repo shape in `DEVELOPMENT.md`, including a Python package entrypoint under `lab/`, a project-level `pyproject.toml`, and a repo-owned `opencode/` surface
- moved the Lab-owned OpenCode files into the repo-owned `opencode/` surface by relocating `agents/` and `opencode.json` under `opencode/`
- added the initial Python project surface with `pyproject.toml` and the `lab/` package entrypoint, replacing the old shell executable in `bin/ai-lab`
- updated `README.md` and the orchestrator prompt to use the repo-owned `opencode/` surface, the standalone clone-install-run model, and the canonical run-rooted runtime shape
*Commit: b666ab8 python + docker shape*

## 2026-04-02

- realigned `lab/control.py` to the canonical run-rooted `.ai-lab/<run-id>/record/` and `bench/` layout instead of the older split `runs/` and `benches/` model
- updated run discovery, run artifact paths, and bench setup behavior so the control layer now creates `record/run.json`, `record/timeline.ndjson`, and `record/brief.md` under the canonical run directory
- changed `lab/control.py` to launch OpenCode per process from the current `.ai-lab/<run-id>/` root instead of the project root, keeping the process boundary aligned with the run directory
- added fail-closed projection-drift checks in `lab/control.py` so unattended launch now verifies the repo-owned OpenCode surface and effective agent roster before execution begins
- moved the remaining effective OpenCode workspace boundary onto the run directory by running the agent-roster preflight from `.ai-lab/<run-id>/` and passing run-local attached file paths such as `record/brief.md`
- made bench mode mandatory for unattended execution in `lab/control.py` by requiring `Execution Mode: bench` at run start and failing closed when a plan still declares `artifact`