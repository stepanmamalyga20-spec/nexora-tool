# Nexora Tool

Nexora Tool is a lightweight OSINT-style CLI utility designed for Termux and Linux environments. It focuses on public, non-invasive intelligence checks and helps gather metadata from publicly accessible resources.

## Features

- IP intelligence lookup
- Telegram username availability and profile URL checks
- Domain/DNS checking
- Person name query builder for open-web searches
- Phone and email pattern validation
- Quick OSINT-style search automation

## Legal / ethical use

This project is for legitimate research, defensive investigations, and authorized audits only. It does not perform password attacks, credential stuffing, or any privacy-intrusive behavior.

## Installation on Termux

```bash
pkg update
pkg install -y python git curl
cd /data/data/com.termux/files/home
git clone https://github.com/your-user/nexora-tool.git
cd nexora-tool
python3 -m pip install -r requirements.txt
python3 nexora.py
```

## Run

```bash
python3 nexora.py
```

Or use direct commands:

```bash
python3 nexora.py --ip 8.8.8.8
python3 nexora.py --telegram username
python3 nexora.py --domain example.com
python3 nexora.py --name "John Doe"
python3 nexora.py --phone "+1 555 123 4567"
python3 nexora.py --email "user@example.com"
```

## Important note

Most lookups are based on public endpoints and search URLs. Availability and results may vary depending on network access and source restrictions.
