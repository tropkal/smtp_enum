#!/usr/bin/env python3
"""
SMTP User enumeration tool

Enumerates valid users on an SMTP server by attempting to send emails
and observing whether the server accepts or rejects the recipient.

Usage:
    ./smtp_enum_users.py <wordlist> <smtp_server>

Example:
    ./smtp_enum_users.py users.txt target.com

Author's github: https://github.com/tropkal
Version: 1.0
Date: 3/18/2026
"""

import sys
import re
import smtplib
import socket
import shutil

from_addr = "a@a.com"

if len(sys.argv) < 3:
    print("Usage: ./smtp_enum_users.py <wordlist> <smtp_server>")
    print("Make sure the target is a domain, not an IP, i.e. target.com")
    exit(-1)

wordlist = sys.argv[1]
target = sys.argv[2]

# dynamically calculating the terminal width, i.e. number of columns
# just because I want the output to be c00l
term_width = shutil.get_terminal_size().columns

try:
    server = smtplib.SMTP(target)
except ConnectionRefusedError:
    print(f"[!] Connected refused on {target}")
    exit(-1)
except TimeoutError:
    print(f"[!] Connected timed out on {target}")
    exit(-1)
except socket.gaierror:
    print(f"[!] Couldn't resolve host {target}")
    exit(-1)
except smtplib.SMTPException as e:
    print(f"[!] SMTP error: {e}.")
    exit(-1)


def read_wordlist(filename):
    with open(wordlist, "r") as f:
        for user in f:
            yield user


def count_lines(filename):
    with open(filename, "r") as f:
        return sum(1 for _ in f)


total = count_lines(wordlist)
user_gen = read_wordlist(wordlist)
valid_users = []

for i, user in enumerate(user_gen, start=1):
    # server.set_debuglevel(1)
    user = re.sub(r"[^\x00-\x7f]", "", user.strip())
    if not user:
        continue

    to_addr = user + "@" + target
    percent = (i / total) * 100
    prefix = f"\r[*] Testing user: {i}/{total} ({percent:.1f}%) - "
    print(
        f"{prefix}{user:<{term_width - len(prefix)}}",
        end="",
        flush=True
    )

    try:
        server.sendmail(from_addr, to_addr, "")
        valid_users.append(user)
        print(f"\n[+] Valid user found: {user}")
    except KeyboardInterrupt:
        print("\n[*] Captured CTRL+C, aborting..")
        exit(0)
    except smtplib.SMTPRecipientsRefused:
        pass


print(f"\n[+] Done. Found {len(valid_users)} valid user(s).")

if valid_users:
    print("[+] Valid users:")
    for user in valid_users:
        print(f"    -> {user}")
