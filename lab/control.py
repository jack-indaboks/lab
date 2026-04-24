from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


PROGRAM_NAME = "lab"
REPO_DIR = Path(__file__).resolve().parent.parent
OPENCODE_CONFIG_PATH = REPO_DIR / "opencode" / "opencode.json"
OPENCODE_AGENTS_DIR = REPO_DIR / "opencode" / "agents"
REQUIRED_AGENT_NAMES = (
    "lab-orchestrator",
    "lab-worker",
    "lab-validator",
    "lab-reporter",
)


class LabError(RuntimeError):
    pass


@dataclass
class RunContext:
    project_dir: Path
    run_id: str
    run_dir: Path
    record_dir: Path
    bench_dir: Path
    run_json_path: Path
    timeline_path: Path
    brief_path: Path
    plan_path: Path
    report_path: Path


def fail(message: str) -> "NoReturn":
    raise LabError(message)


def usage() -> str:
    return (
        "Usage:\n"
        "  lab plan <brief>\n"
        "  lab run <slug>\n\n"
        "Current POC behavior:\n"
        "  - runs from a git project root\n"
        "  - resolves repo-owned OpenCode assets through opencode/opencode.json\n"
        "  - creates runtime state under .ai-lab/<run-id>/record and bench\n"
        "  - uses git worktree for bench-mode runs\n"
    )


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        fail(f"required command not found: {name}")


def resolve_project_dir() -> Path:
    project_dir = Path.cwd().resolve()
    if not (project_dir / ".git").exists():
        fail("run lab from a git project root")
    return project_dir


def iso_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def run_id_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M")


def slugify(value: str) -> str:
    slug = []
    last_dash = False
    for char in value.lower():
        if char.isalnum():
            slug.append(char)
            last_dash = False
        elif not last_dash:
            slug.append("-")
            last_dash = True
    normalized = "".join(slug).strip("-")
    return normalized or "run"


def abspath_file(input_path: str) -> Path:
    path = Path(input_path).expanduser().resolve()
    if not path.is_file():
        fail(f"file not found: {input_path}")
    return path


def append_timeline(path: Path, event_type: str, message: str) -> None:
    event = {
        "timestamp": iso_timestamp(),
        "event": event_type,
        "message": message,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")


def read_created_at(path: Path) -> str:
    if not path.exists():
        return iso_timestamp()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return iso_timestamp()
    return data.get("created_at", iso_timestamp())


def write_run_json(context: RunContext, phase: str, status: str, execution_mode: str, bench_path: str) -> None:
    data = {
        "run_id": context.run_id,
        "project_dir": str(context.project_dir),
        "repo_dir": str(REPO_DIR),
        "run_dir": str(context.run_dir),
        "brief_path": str(context.brief_path),
        "plan_path": str(context.plan_path),
        "report_path": str(context.report_path),
        "bench_path": bench_path,
        "phase": phase,
        "status": status,
        "execution_mode": execution_mode,
        "created_at": read_created_at(context.run_json_path),
        "updated_at": iso_timestamp(),
    }
    context.run_json_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def ensure_ai_lab_root(project_dir: Path) -> None:
    (project_dir / ".ai-lab").mkdir(parents=True, exist_ok=True)


def run_root(project_dir: Path) -> Path:
    return project_dir / ".ai-lab"


def next_run_id(project_dir: Path, base: str) -> str:
    candidate = base
    counter = 1
    runs_root = run_root(project_dir)
    while (runs_root / candidate).exists():
        candidate = f"{base}-{counter:02d}"
        counter += 1
    return candidate


def resolve_run_id(project_dir: Path, input_name: str) -> str:
    runs_root = run_root(project_dir)
    direct = runs_root / input_name
    if direct.is_dir():
        return input_name

    normalized_slug = slugify(input_name)
    matches = sorted(
        [
            path.name
            for path in runs_root.iterdir()
            if path.is_dir()
            and (path / "record").is_dir()
            and (path.name.endswith(f"_{normalized_slug}") or path.name.endswith(f"_{normalized_slug}-01") or f"_{normalized_slug}-" in path.name)
        ],
        reverse=True,
    )
    if not matches:
        fail(f"no run found for slug: {input_name}")
    if len(matches) > 1:
        fail(f"multiple runs matched slug '{input_name}'; use the full run id")
    return matches[0]


def opencode_env(context: RunContext | None = None, mode: str | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env["OPENCODE_CONFIG"] = str(OPENCODE_CONFIG_PATH)
    env["AI_LAB_REPO_DIR"] = str(REPO_DIR)
    if context is not None and mode is not None:
        env["AI_LAB_MODE"] = mode
        env["AI_LAB_RUN_ID"] = context.run_id
        env["AI_LAB_PROJECT_DIR"] = str(context.project_dir)
        env["AI_LAB_REPO_DIR"] = str(REPO_DIR)
        env["AI_LAB_RUN_DIR"] = str(context.run_dir)
        env["AI_LAB_BRIEF_PATH"] = str(context.brief_path)
        env["AI_LAB_PLAN_PATH"] = str(context.plan_path)
        env["AI_LAB_REPORT_PATH"] = str(context.report_path)
        env["AI_LAB_BENCH_DIR"] = str(context.bench_dir) if context.bench_dir else ""
    return env


def list_available_agents(workspace_dir: Path, context: RunContext | None = None) -> list[str]:
    result = subprocess.run(
        ["opencode", "agent", "list"],
        cwd=workspace_dir,
        env=opencode_env(context),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def add_projection_drift_checks(workspace_dir: Path, context: RunContext | None = None) -> None:
    if not OPENCODE_CONFIG_PATH.is_file():
        fail(f"missing repo-owned OpenCode config: {OPENCODE_CONFIG_PATH}")
    if not OPENCODE_AGENTS_DIR.is_dir():
        fail(f"missing repo-owned OpenCode agents directory: {OPENCODE_AGENTS_DIR}")

    missing_definition_files = [
        str(OPENCODE_AGENTS_DIR / f"{agent_name}.md")
        for agent_name in REQUIRED_AGENT_NAMES
        if not (OPENCODE_AGENTS_DIR / f"{agent_name}.md").is_file()
    ]
    if missing_definition_files:
        fail(
            "repo-owned OpenCode surface is incomplete; missing agent definitions: "
            + ", ".join(missing_definition_files)
        )

    available_agents = list_available_agents(workspace_dir, context)
    missing_agents = [
        agent_name
        for agent_name in REQUIRED_AGENT_NAMES
        if not any(line.startswith(agent_name) for line in available_agents)
    ]
    if missing_agents:
        fail(
            "effective OpenCode agent surface does not match the repo-owned Lab surface; missing agents: "
            + ", ".join(missing_agents)
        )


def extract_execution_mode(plan_path: Path) -> str:
    lines = plan_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    for raw_line in lines:
        line = raw_line.rstrip("\r")
        if line.startswith("#") and line.lstrip("#").strip() == "Execution Mode":
            in_section = True
            continue
        if in_section and line.startswith("#"):
            break
        if in_section:
            candidate = line.lstrip(" -").strip().lower()
            if candidate:
                return candidate
    return ""


def ensure_bench_worktree(bench_dir: Path) -> None:
    if bench_dir.exists():
        try:
            subprocess.run(["git", "-C", str(bench_dir), "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True)
            return
        except subprocess.CalledProcessError:
            if any(bench_dir.iterdir()):
                fail(f"existing bench directory is not a valid git worktree: {bench_dir}")
            bench_dir.rmdir()
    subprocess.run(["git", "worktree", "add", str(bench_dir), "HEAD"], check=True)


def invoke_opencode(context: RunContext, mode: str, message: str, attached_file: Path) -> None:
    attached_file_arg = str(attached_file.relative_to(context.run_dir))
    subprocess.run(
        [
            "opencode",
            "run",
            "--dir",
            str(context.run_dir),
            "--agent",
            "lab-orchestrator",
            "--file",
            attached_file_arg,
            "--title",
            context.run_id,
            message,
        ],
        cwd=context.run_dir,
        env=opencode_env(context, mode),
        check=True,
    )


def planning_context(project_dir: Path, brief_source: Path) -> RunContext:
    brief_name = brief_source.stem
    brief_slug = slugify(brief_name)
    base_run_id = f"{run_id_timestamp()}_{brief_slug}"
    run_id = next_run_id(project_dir, base_run_id)
    run_dir = run_root(project_dir) / run_id
    record_dir = run_dir / "record"
    bench_dir = run_dir / "bench"
    return RunContext(
        project_dir=project_dir,
        run_id=run_id,
        run_dir=run_dir,
        record_dir=record_dir,
        bench_dir=bench_dir,
        run_json_path=record_dir / "run.json",
        timeline_path=record_dir / "timeline.ndjson",
        brief_path=record_dir / "brief.md",
        plan_path=record_dir / "plan.md",
        report_path=record_dir / "report.md",
    )


def execution_context(project_dir: Path, slug: str) -> RunContext:
    run_id = resolve_run_id(project_dir, slug)
    run_dir = run_root(project_dir) / run_id
    record_dir = run_dir / "record"
    bench_dir = run_dir / "bench"
    return RunContext(
        project_dir=project_dir,
        run_id=run_id,
        run_dir=run_dir,
        record_dir=record_dir,
        bench_dir=bench_dir,
        run_json_path=record_dir / "run.json",
        timeline_path=record_dir / "timeline.ndjson",
        brief_path=record_dir / "brief.md",
        plan_path=record_dir / "plan.md",
        report_path=record_dir / "report.md",
    )


def start_plan(project_dir: Path, brief_arg: str) -> str:
    brief_source = abspath_file(brief_arg)
    context = planning_context(project_dir, brief_source)
    context.record_dir.mkdir(parents=True, exist_ok=True)
    context.bench_dir.mkdir(parents=True, exist_ok=True)
    add_projection_drift_checks(context.run_dir, context)
    shutil.copy2(brief_source, context.brief_path)
    context.timeline_path.write_text("", encoding="utf-8")

    write_run_json(context, "planning", "initializing", "", str(context.bench_dir))
    append_timeline(context.timeline_path, "run_initialized", "created planning run directory")
    append_timeline(context.timeline_path, "brief_copied", "copied brief into run record")

    write_run_json(context, "planning", "running", "", str(context.bench_dir))
    append_timeline(context.timeline_path, "planning_started", "invoking lab-orchestrator in planning mode")

    try:
        invoke_opencode(
            context,
            "plan",
            "Planning mode for the current Lab run. Read brief.md from the run directory, produce or revise plan.md there, validate the plan before stopping, and do not begin execution.",
            context.brief_path,
        )
    except subprocess.CalledProcessError as exc:
        write_run_json(context, "planning", "failed", "", str(context.bench_dir))
        append_timeline(context.timeline_path, "planning_failed", "opencode planning invocation exited non-zero")
        fail(f"planning failed for run {context.run_id}")

    if not context.plan_path.exists():
        write_run_json(context, "planning", "failed", "", str(context.bench_dir))
        append_timeline(context.timeline_path, "planning_failed", "planning exited without producing plan.md")
        fail(f"planning did not produce plan.md for run {context.run_id}")

    write_run_json(context, "planning", "ready_for_review", "", str(context.bench_dir))
    append_timeline(context.timeline_path, "planning_completed", "plan.md is ready for review")
    return context.run_id


def start_run(project_dir: Path, slug: str) -> str:
    context = execution_context(project_dir, slug)
    if not context.run_dir.is_dir():
        fail(f"run not found under current working directory: {context.run_id}")
    if not context.plan_path.is_file():
        fail(f"run is missing plan.md: {context.run_id}")
    if not context.run_json_path.is_file():
        fail(f"run is missing run.json: {context.run_id}")
    if not context.timeline_path.is_file():
        fail(f"run is missing timeline.ndjson: {context.run_id}")
    add_projection_drift_checks(context.run_dir, context)

    execution_mode = extract_execution_mode(context.plan_path)
    if execution_mode != "bench":
        fail("plan.md must declare Execution Mode as bench for unattended runs")

    ensure_bench_worktree(context.bench_dir)
    bench_path = str(context.bench_dir)
    append_timeline(context.timeline_path, "bench_ready", "bench worktree is ready for run execution")

    write_run_json(context, "execution", "running", execution_mode, bench_path)
    append_timeline(context.timeline_path, "run_started", "invoking lab-orchestrator in run mode")

    try:
        invoke_opencode(
            context,
            "run",
            "Run mode for the current Lab run. Treat plan.md as the execution contract, execute the approved plan step by step, maintain run artifacts, and stop only when the run has reached a reviewable end state.",
            context.plan_path,
        )
    except subprocess.CalledProcessError:
        write_run_json(context, "execution", "failed", execution_mode, bench_path)
        append_timeline(context.timeline_path, "run_failed", "opencode execution invocation exited non-zero")
        fail(f"run failed for {context.run_id}")

    write_run_json(context, "execution", "stopped_for_review", execution_mode, bench_path)
    append_timeline(context.timeline_path, "run_completed", "execution invocation completed")
    return context.run_id


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(usage(), end="")
        return 1

    subcommand = args.pop(0)
    if subcommand in {"-h", "--help", "help"}:
        print(usage(), end="")
        return 0
    if subcommand == "plan":
        if len(args) != 1:
            fail("plan requires exactly one brief path")
        command = "plan"
    elif subcommand == "run":
        if len(args) != 1:
            fail("run requires exactly one slug")
        command = "run"
    else:
        print(usage(), end="")
        fail(f"unknown command: {subcommand}")

    require_command("git")
    require_command("opencode")
    project_dir = resolve_project_dir()
    ensure_ai_lab_root(project_dir)

    if command == "plan":
        print(start_plan(project_dir, args[0]))
    else:
        print(start_run(project_dir, args[0]))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LabError as exc:
        print(f"{PROGRAM_NAME}: {exc}", file=sys.stderr)
        raise SystemExit(1)
