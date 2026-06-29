# YouTube Upload Checklist

Use this for ICSE Tool Demonstration and Data Showcase and SANER Tool Demo.

## Generated Files

After running:

```powershell
python scripts/make_demo_video.py --track icse-tool-demo
```

Expected files:

- `dist/videos/icse-tool-demo/agent-harness-demo.mp4`
- `dist/videos/icse-tool-demo/thumbnail.png`

The `dist/` directory is intentionally ignored by Git. Upload the MP4 to
YouTube and use the PNG as the thumbnail if YouTube allows a custom thumbnail.

## Upload Settings

- Title: `Replayable Harnesses for Stateful Agent Contracts`
- Visibility: `Unlisted` for review.
- Audience: `No, it is not made for kids`.
- Description: use `submissions/video/demo_script.md`.
- Playlist: none required.
- Tags: `software engineering`, `AI agents`, `agent harness`, `evaluation`,
  `replay`, `tool use`, `stateful agents`, `ICSE`, `SANER`.

Do not publish as Public without an explicit final confirmation from the author.

