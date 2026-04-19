---
name: "command-logger"
description: "Log all generated commands to local file. Invoke when running ffmpeg, python scripts, or any shell commands with timestamp and task description."
---

# Command Logger

This skill logs all generated commands to a local file for tracking and documentation.

## When to Use

Invoke when:
- Running ffmpeg commands (push stream, convert, compress, etc.)
- Running any python script
- Running any shell command
- Generating any command that user may want to reference later

## Log File Location

`/Users/zengwenhua/py_workspace/video-analysis-studio/docs/commands.md`

## How to Log

1. Check if the log file exists
2. If not, create it with header
3. Append new entry with:
   - Timestamp (ISO 8601 format)
   - Task description
   - The command(s)
   - Context or notes (optional)

## Log Format

```markdown
## [YYYY-MM-DD HH:mm:ss] - [Task Description]

### Command
```bash
[the command here]
```

### Context
[optional notes about the command]

---

```

## Example

Before:

After generating a command like:
```bash
ffmpeg -i input.mp4 -c:v libx264 output.mp4
```

Should log:

```markdown
## 2024-04-19 16:30:00 - Convert video to H.264

### Command
```bash
ffmpeg -i input.mp4 -c:v libx264 output.mp4
```

### Context
Convert traffic_video_6.mp4 to H.264 for better compatibility

---

```

## Important

- Always append to existing file, never overwrite
- Use markdown code blocks for commands
- Include descriptive task description
- Add relevant context when helpful
- Keep the file in docs/ directory