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
- `dist/videos/saner-tool-demo/agent-harness-demo.mp4`
- `dist/videos/saner-tool-demo/thumbnail.png`

The `dist/` directory is intentionally ignored by Git. Upload the MP4 to
YouTube and use the PNG as the thumbnail if YouTube allows a custom thumbnail.

## Published Backup Assets

The local Chrome session can reach Google account pages but currently fails to
open `youtube.com` and `studio.youtube.com`, so the YouTube upload is still
pending. Public GitHub Release backup assets are already available:

- ICSE/SANER generic demo video:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-icse-tool-demo-video.mp4
- ICSE thumbnail:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-icse-tool-demo-thumbnail.png
- SANER demo video:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-saner-tool-demo-video.mp4
- SANER thumbnail:
  https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-saner-tool-demo-thumbnail.png

Use YouTube for ICSE submission once the network path is available. The GitHub
Release video is acceptable as a backup artifact link and for SANER's optional
tool website/video path.

## Upload Settings

- Title: `Replayable Harnesses for Stateful Agent Contracts`
- Visibility: `Unlisted` for review.
- Audience: `No, it is not made for kids`.
- Description: use `submissions/video/demo_script.md`.
- Playlist: none required.
- Tags: `software engineering`, `AI agents`, `agent harness`, `evaluation`,
  `replay`, `tool use`, `stateful agents`, `ICSE`, `SANER`.

Do not publish as Public without an explicit final confirmation from the author.
