---
name: "ai_docker"
description: "Wrapper for docker commands using sudo ai_docker prefix. Invoke when user wants to run docker commands (ps, run, build, etc.)"
---

# AI Docker Skill

This skill provides a convenient wrapper for docker commands by using `sudo ai_docker` as the prefix instead of `docker`.

## Usage

When you need to run docker commands, replace `docker` with `ai_docker`:

| Original Command | Wrapped Command |
|------------------|------------------|
| `docker ps` | `sudo ai_docker ps` |
| `docker run ...` | `sudo ai_docker run ...` |
| `docker build ...` | `sudo ai_docker build ...` |
| `docker exec ...` | `sudo ai_docker exec ...` |
| `docker images` | `sudo ai_docker images` |
| `docker logs ...` | `sudo ai_docker logs ...` |

## How It Works

The skill automatically prepends `sudo ai_docker` to any docker command the user wants to execute. This is useful in environments where direct docker access requires sudo privileges and a specific wrapper script.

## Example

If the user asks to list running containers, you would execute:

```bash
sudo ai_docker ps
```

Or if the user wants to run a container:

```bash
sudo ai_docker run -it ubuntu /bin/bash
```