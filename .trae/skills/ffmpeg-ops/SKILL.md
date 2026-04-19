---
name: "ffmpeg-ops"
description: "Video streaming, conversion and FFmpeg operations. Invoke when user asks for push stream, video conversion, compression, or any media processing task."
---

# FFmpeg Operations

This skill handles all video streaming, conversion and media processing tasks using FFmpeg.

## When to Use

Invoke when user asks for:
- Push stream to RTMP server (ZLMediaKit, etc.)
- Video format conversion (MPEG4 to H.264, etc.)
- Video compression
- Audio extraction
- Video trimming/cutting
- Any video/audio processing task

## Log File Location

`/Users/zengwenhua/py_workspace/video-analysis-studio/docs/ffmpeg-log.md`

## After Execution

1. Always append command to ffmpeg-log.md after running any ffmpeg command
2. Include timestamp, task description, command, and status

## Log Format

```markdown
## [YYYY-MM-DD HH:mm:ss] - [Task Description]

### Command
```bash
[the ffmpeg command here]
```

### Input
- Source: [file path]
- Info: [resolution, codec, fps, etc.]

### Output
- Target: [output path or RTMP URL]
- Status: Running/Stopped/Error

### Notes
[any relevant notes]

---
```

## Example Log Entry

```markdown
## 2024-04-19 16:35:00 - 循环推送到 ZLMediaKit

### Command
```bash
ffmpeg -re -stream_loop -1 -i input.mp4 -c:v libx264 -preset fast -f flv rtmp://192.168.2.138:1935/live/stream
```

### Input
- Source: data/videos/20241005175608.mp4
- Info: 2560x1440, MPEG4, 25fps

### Output
- Target: rtmp://192.168.2.138:1935/live/stream
- Status: Running

### Notes
原始视频是 MPEG4 编码，需要转码为 H.264

---
```

## Common Operations

### Stream Push (Loop)
```bash
ffmpeg -re -stream_loop -1 -i [input] -c:v copy -c:a copy -f flv rtmp://[host]/[app]/[stream]
```

### Convert to H.264
```bash
ffmpeg -i [input] -c:v libx264 -preset fast -c:a aac [output]
```

### Compress Video
```bash
ffmpeg -i [input] -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k [output]
```

### Extract Audio
```bash
ffmpeg -i [input] -vn -acodec libmp3lame -q:a 2 [output].mp3
```

## Important

- Use `-stream_loop -1` for infinite loop streaming
- Always log after execution, not before
- Update status when stream stops
- Check video codec compatibility with target format