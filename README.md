# IT Professional Simulation Game

This project is a web-based simulation game where players experience the career path of an IT professional, progressing from T1 to T4 support roles.

## Features
- Task queue with auto-generated tasks
- XP-based level-up system
- Save/Load game functionality
- Tools simulation (Password Reset, DNS Editor, Malware Scanner, Firewall Console, DDoS Mitigator, Backup/Restore, Terminal Emulator)
- Web UI built with Flask and Bootstrap 5

## Tech Stack
- Python 3.9+
- Flask
- Gunicorn
- Docker & Docker Compose
- Nginx Proxy Manager (for domain access)

## Setup & Usage

### Running with Docker
1. Ensure Docker and Docker Compose are installed.
2. Build and run the container:
   ```bash
   docker-compose up --build
