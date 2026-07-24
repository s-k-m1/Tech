#!/usr/bin/env python
"""Database backup script."""
import os
import datetime
import subprocess

DB_NAME = os.environ.get("DB_NAME", "sk_tech")
DB_USER = os.environ.get("DB_USER", "sk_tech")
DB_HOST = os.environ.get("DB_HOST", "localhost")
BACKUP_DIR = os.environ.get("BACKUP_DIR", "/backups")

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"{DB_NAME}_{timestamp}.sql"
filepath = os.path.join(BACKUP_DIR, filename)

os.makedirs(BACKUP_DIR, exist_ok=True)

cmd = f"pg_dump -U {DB_USER} -h {DB_HOST} {DB_NAME} > {filepath}"
subprocess.run(cmd, shell=True, check=True)

print(f"Backup created: {filepath}")
