import csv
import json
import os
import re
import sqlite3
from collections import defaultdict
from datetime import datetime

# Mandatory log helper
def log_turn(title, user_prompt, agent_summary, actions):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    log_entry = f"""## [{timestamp}] {title}

User Prompt (verbatim, secrets redacted):
{user_prompt}

Agent Response Summary:
{agent_summary}

Actions:
{actions}

Context:
tool=Claude Code
model=claude-sonnet-5-5
branch=main
repo_root=D:\\dev\\Hackerrank\\hackerrank-orchestrate-october26
worktree=main
parent_agent=none
"""
    log_path = "log.txt"
    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"""## [{timestamp}] SESSION START

tool=Claude Code
model=claude-sonnet-5-5
Repo Root: D:\\dev\\Hackerrank\\hackerrank-orchestrate-october26
Branch: main
Worktree: main
Parent Agent: none
Language: py
Time Remaining: not configured

""")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

print("Logger defined.")
