# Screencast Upload Checklist

Use this for SANER Tool Demo.

## Generated Files

After running:

```powershell
python scripts/make_demo_video.py --track saner-tool-demo
```

Expected files:

- `dist/videos/saner-tool-demo/agent-harness-demo.mp4`
- `dist/videos/saner-tool-demo/thumbnail.png`

The `dist/` directory is intentionally ignored by Git. SANER allows an optional
3-5 minute screencast via YouTube or a tool website, so the public GitHub
Release asset is sufficient for the current strategy.

## Published Backup Assets

Public GitHub Release screencast assets are available:

- SANER demo video:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-saner-tool-demo-video.mp4
- SANER thumbnail:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-saner-tool-demo-thumbnail.png

The GitHub Release video is acceptable for SANER's optional tool website/video
path.

## Upload Settings

- Title: `Replayable Harnesses for Stateful Agent Contracts`
- Visibility: `Unlisted` for review.
- Audience: `No, it is not made for kids`.
- Description: use `submissions/video/demo_script.md`.
- Playlist: none required.
- Tags: `software engineering`, `AI agents`, `agent harness`, `evaluation`,
  `replay`, `tool use`, `stateful agents`, `SANER`.

Do not publish as Public without an explicit final confirmation from the author.
