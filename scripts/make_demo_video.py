from __future__ import annotations

import argparse
import os
import subprocess
import textwrap
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]


SCENES = [
    {
        "title": "Final answers are not enough",
        "bullets": [
            "Agents now edit repositories, call tools, manage memory, and prepare side effects.",
            "A plausible final response can hide forbidden reads, wrong state changes, or skipped review.",
            "The artifact evaluates the trajectory and final state, not only text output.",
        ],
        "narration": (
            "Stateful agents do more than answer questions. They edit files, call tools, manage memory, "
            "and prepare actions that may affect real workflows. A final answer can look right while the "
            "agent used the wrong tool, read the wrong context, or changed the wrong state."
        ),
    },
    {
        "title": "Artifact map",
        "bullets": [
            "benchmark/cases.jsonl: 24 inspectable cases.",
            "harness/: mock tools, state snapshots, permissions, metrics, prompts.",
            "experiments/raw/ and results/tables/: raw rows and regenerated summaries.",
            "docs/: reproducibility, claim boundaries, reviewer guide.",
        ],
        "narration": (
            "The repository is intentionally small enough to review. The benchmark file defines twenty four "
            "cases. The harness package implements mock state, tool simulation, permissions, prompts, and metrics. "
            "Raw rows and regenerated tables are committed so the reported results can be checked."
        ),
    },
    {
        "title": "Contract anatomy",
        "bullets": [
            "Task and trigger: should the agent act, refuse, or escalate?",
            "Allowed and forbidden tools: what may be called?",
            "State assertions: what must change by the end?",
            "Replay record: can the failure be diagnosed later?",
        ],
        "narration": (
            "Each case is a compact contract. It states the task, the initial state, which tools are allowed, "
            "which tools are forbidden, and which state assertions must hold at the end. This makes success a "
            "property of the world state, not only a property of the final message."
        ),
    },
    {
        "title": "Reviewer path",
        "bullets": [
            "python scripts/run_checks.py --mode validate",
            "python scripts/run_demo_walkthrough.py",
            "python scripts/run_local_reference.py",
            "python scripts/analyze_results.py",
            "python scripts/generate_figures.py",
        ],
        "narration": (
            "A reviewer can start with one validation command, then run the demo walkthrough, rerun the deterministic "
            "reference policy, regenerate results, and rebuild the figure. Live provider keys are not required for "
            "artifact validation."
        ),
    },
    {
        "title": "No-credential walkthrough",
        "bullets": [
            "Loads all 24 cases and categories.",
            "Runs a security case that must avoid .env and secret files.",
            "Regenerates local reference rows and aggregate tables.",
            "Prints the same result table used by the paper.",
        ],
        "narration": (
            "The no-credential walkthrough is the fastest hands-on path. It loads the cases, executes a security case "
            "that must avoid environment and secret files, regenerates local reference rows, rebuilds aggregate tables, "
            "and prints the same summary table used in the paper."
        ),
    },
    {
        "title": "Permission and injection failures become visible",
        "bullets": [
            "Untrusted observations are modeled explicitly.",
            "Forbidden secret access and irreversible side effects are counted.",
            "Invalid tool calls and parser failures are not hidden by final text.",
        ],
        "narration": (
            "The harness is especially useful for failures that final answers hide. Untrusted observations can try "
            "to induce unsafe tool use. The harness records forbidden secret access, invalid tool calls, parser "
            "failures, and missing state diffs as separate failure classes."
        ),
    },
    {
        "title": "Thin harness, strong contracts",
        "bullets": [
            "Avoid brittle cognitive choreography around one model generation.",
            "Keep durable boundaries explicit: tools, state, memory, replay, audit, review.",
            "Compare no harness, thick checklist, and thin contract variants.",
        ],
        "narration": (
            "The design principle is thin harness, strong contracts. The harness should not become a thick substitute "
            "for model intelligence. It should define the durable boundary around external effects: tool calls, state "
            "diffs, permissions, memory scope, replay, audit, and human review."
        ),
    },
    {
        "title": "Pilot results are bounded",
        "bullets": [
            "24 synthetic cases demonstrate an evaluation shape.",
            "Live runs are descriptive pilot rows, not provider rankings.",
            "The main output is inspectable failure structure.",
        ],
        "narration": (
            "The pilot results are deliberately bounded. They are not a general provider leaderboard. The value is that "
            "the failure structure becomes inspectable: routing errors, state-diff failures, permission violations, and "
            "replay gaps can be studied directly."
        ),
    },
    {
        "title": "Conference submission paths",
        "bullets": [
            "ICSE NIER and SANER Short Paper: anonymized paper and artifact package.",
            "SANER Tool Demo: repository-state and maintenance-risk framing.",
        ],
        "narration": (
            "The same artifact supports different submission paths. Double-anonymous tracks need an anonymized paper "
            "and artifact package. For SANER, the strongest framing is repository state, diffs, tests, replay, "
            "and maintenance risk."
        ),
    },
    {
        "title": "Public artifact",
        "bullets": [
            "Repository: github.com/rrrrrredy/agent-harness-paper",
            "Archive: doi.org/10.5281/zenodo.20907471",
            "Code: MIT. Manuscript, docs, cases, tables, figures: CC BY 4.0.",
        ],
        "narration": (
            "The public artifact is available on GitHub and archived on Zenodo. Code is MIT licensed. The manuscript, "
            "documentation, benchmark cases, tables, and figures are licensed under Creative Commons Attribution four point zero."
        ),
    },
]


def run(cmd: list[str], *, env: dict[str, str] | None = None) -> None:
    subprocess.run(cmd, cwd=ROOT, env=env, check=True)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        trial = " ".join(current + [word])
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def render_slide(scene: dict[str, object], index: int, total: int, output: Path, track_label: str) -> None:
    width, height = 1920, 1080
    image = Image.new("RGB", (width, height), (247, 248, 250))
    draw = ImageDraw.Draw(image)
    title_font = font(58, bold=True)
    subtitle_font = font(27)
    bullet_font = font(38)
    small_font = font(24)

    navy = (20, 42, 70)
    blue = (41, 99, 181)
    green = (31, 129, 99)
    ink = (28, 35, 45)
    muted = (91, 103, 118)
    line = (219, 225, 232)

    draw.rectangle((0, 0, width, 96), fill=navy)
    draw.text((72, 28), "Agent Harness Demo", font=subtitle_font, fill=(255, 255, 255))
    draw.text((width - 420, 28), track_label, font=subtitle_font, fill=(222, 231, 242))

    draw.rectangle((72, 150, width - 72, height - 120), fill=(255, 255, 255), outline=line, width=2)
    draw.rectangle((72, 150, 96, height - 120), fill=blue)

    draw.text((138, 202), str(scene["title"]), font=title_font, fill=ink)
    draw.line((138, 292, width - 140, 292), fill=line, width=2)

    y = 350
    bullets = scene["bullets"]
    assert isinstance(bullets, list)
    for bullet in bullets:
        bullet = str(bullet)
        wrapped = wrap(draw, bullet, bullet_font, width - 310)
        draw.ellipse((138, y + 11, 160, y + 33), fill=green)
        for j, line_text in enumerate(wrapped):
            draw.text((184, y + j * 48), line_text, font=bullet_font, fill=ink)
        y += max(72, len(wrapped) * 48 + 36)

    progress_x = 138
    progress_y = height - 170
    bar_w = width - 276
    draw.rectangle((progress_x, progress_y, progress_x + bar_w, progress_y + 8), fill=(226, 232, 240))
    draw.rectangle(
        (progress_x, progress_y, progress_x + int(bar_w * index / total), progress_y + 8),
        fill=blue,
    )
    footer = "github.com/rrrrrredy/agent-harness-paper  |  doi.org/10.5281/zenodo.20907471"
    draw.text((138, height - 90), footer, font=small_font, fill=muted)
    draw.text((width - 210, height - 90), f"{index}/{total}", font=small_font, fill=muted)
    image.save(output)


def speak(text: str, output: Path) -> None:
    ps = r"""
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  $voices = $speaker.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
  if ($voices -contains 'Microsoft Zira Desktop') {
    $speaker.SelectVoice('Microsoft Zira Desktop')
  } elseif ($voices -contains 'Microsoft Zira') {
    $speaker.SelectVoice('Microsoft Zira')
  }
  $speaker.Rate = -1
  $speaker.SetOutputToWaveFile($env:DEMO_TTS_OUTPUT)
  $speaker.Speak($env:DEMO_TTS_TEXT)
} finally {
  $speaker.Dispose()
}
"""
    env = os.environ.copy()
    env["DEMO_TTS_TEXT"] = text
    env["DEMO_TTS_OUTPUT"] = str(output)
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        cwd=ROOT,
        env=env,
        check=True,
    )


def duration_seconds(wav_path: Path) -> float:
    with wave.open(str(wav_path), "rb") as wav:
        return wav.getnframes() / wav.getframerate()


def build_video(track: str) -> Path:
    labels = {
        "saner-tool-demo": "SANER 2027 Tool Demo",
    }
    label = labels.get(track, "Conference Demo")
    out_dir = ROOT / "dist" / "videos" / track
    out_dir.mkdir(parents=True, exist_ok=True)
    concat_file = out_dir / "concat.txt"
    scene_videos: list[Path] = []

    for i, scene in enumerate(SCENES, start=1):
        slide = out_dir / f"slide_{i:02d}.png"
        audio = out_dir / f"audio_{i:02d}.wav"
        video = out_dir / f"scene_{i:02d}.mp4"
        render_slide(scene, i, len(SCENES), slide, label)
        speak(str(scene["narration"]), audio)
        dur = duration_seconds(audio) + 0.6
        run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(slide),
                "-i",
                str(audio),
                "-t",
                f"{dur:.2f}",
                "-vf",
                "scale=1920:1080,format=yuv420p",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-shortest",
                str(video),
            ]
        )
        scene_videos.append(video)

    concat_file.write_text(
        "\n".join(f"file '{video.as_posix()}'" for video in scene_videos) + "\n",
        encoding="utf-8",
    )
    output = out_dir / "agent-harness-demo.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]
    )
    thumbnail = out_dir / "thumbnail.png"
    render_slide(
        {
            "title": "Replayable Harnesses for Stateful Agent Contracts",
            "bullets": [
                "Tool calls, permissions, state diffs, replay, memory scope, audit, and review.",
                "Public artifact for SANER tool-demo submission.",
            ],
        },
        1,
        1,
        thumbnail,
        label,
    )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a 3-5 minute demo video.")
    parser.add_argument(
        "--track",
        default="saner-tool-demo",
        choices=["saner-tool-demo"],
        help="Target track label for the generated video.",
    )
    args = parser.parse_args()
    output = build_video(args.track)
    print(textwrap.dedent(
        f"""
        Generated video:
        {output}

        Suggested video title:
        Replayable Harnesses for Stateful Agent Contracts
        """
    ).strip())


if __name__ == "__main__":
    main()
