# smtp_enum_users.py
SMTP User enumeration tool
Enumerates valid users on an SMTP server by attempting to send emails and observing whether the server accepts or rejects the recipient.

# Installation
No external modules need to be installed, only standard library modules were used.
```
$ git pull https://github.com/tropkal/smtp_enum
```

# Usage
```
$ cd smtp_enum
$ chmod +x ./smtp_enum_users.py
$ ./smtp_enum_users.py wordlist.txt target.com
```

# Example
```
$ ./smtp_enum_users.py users.txt winserver01.hs
[*] Testing user: 10/19 (52.6%) - alfonso
[+] Valid user found: alfonso
[*] Testing user: 14/19 (73.7%) - roger
[+] Valid user found: roger
[*] Testing user: 19/19 (100.0%) - 10
[+] Done. Found 2 valid user(s).
[+] Valid users:
    -> alfonso@winserver01.hs
    -> roger@winserver01.hs
```
