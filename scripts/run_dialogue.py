#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@dataclass
class Turn:
    role: str  # system | user | assistant
    content: str


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def get_git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return None


def make_run_dir(scenario: str) -> Path:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = Path("runs") / "public" / f"{stamp}_{scenario}"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def call_llm(messages: List[Dict[str, str]], model: str, temperature: float) -> str:
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=messages,
    )
    return resp.choices[0].message.content or ""


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Synthetic Anthropology Lab: run a dialogue protocol (v1).")
    p.add_argument(
        "--scenario",
        default=os.getenv("SCENARIO", "santa_v1"),
        help="Scenario prompt file stem, e.g. santa_v1 -> prompts/santa_v1.md",
    )
    p.add_argument("--turns", type=int, default=6, help="Maximum assistant replies.")
    p.add_argument("--model", default=os.getenv("MODEL", "gpt-4o-mini"), help="OpenAI model name")
    p.add_argument("--temperature", type=float, default=float(os.getenv("TEMPERATURE", "0.7")))
    return p


def run(argv: List[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    print("⌖ synthetic-anthropology-cognition-lab: starting dialogue pipeline")

    system_path = Path("prompts") / "system_base.md"
    scenario_path = Path("prompts") / f"{args.scenario}.md"

    if not system_path.exists():
        raise SystemExit(f"Missing {system_path}")
    if not scenario_path.exists():
        raise SystemExit(f"Missing {scenario_path}")

    system_prompt = read_text_file(system_path)
    scenario_prompt = read_text_file(scenario_path)

    turns: List[Turn] = [
        Turn("system", system_prompt),
        Turn("system", scenario_prompt),
    ]

    user_prompt = input("User prompt (single line, blank to quit): ").strip()
    if not user_prompt:
        print("No input provided; exiting.")
        return 0
    turns.append(Turn("user", user_prompt))

    out_dir = make_run_dir(args.scenario)
    metadata: Dict[str, Any] = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "scenario": args.scenario,
        "model": args.model,
        "temperature": args.temperature,
        "prompt_files": {"system": str(system_path), "scenario": str(scenario_path)},
        "git_commit": get_git_commit(),
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    for i in range(args.turns):
        messages = [asdict(t) for t in turns]
        assistant_text = call_llm(messages, model=args.model, temperature=args.temperature)

        print(f"\n--- Assistant (turn {i+1}) ---")
        print(assistant_text)

        turns.append(Turn("assistant", assistant_text))

        follow_up = input("\nUser follow-up (single line; blank to stop): ").strip()
        if not follow_up:
            break
        turns.append(Turn("user", follow_up))

    transcript = {"turns": [asdict(t) for t in turns]}
    (out_dir / "transcript.json").write_text(json.dumps(transcript, indent=2), encoding="utf-8")

    print(f"\n✓ Saved run artefacts to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
