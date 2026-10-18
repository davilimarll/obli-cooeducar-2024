import ctypes
import json
import subprocess
import urllib.request
import urllib.error
from ctypes import wintypes

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR),
    ]

PCREDENTIAL = ctypes.POINTER(CREDENTIAL)
CredRead = ctypes.windll.advapi32.CredReadW
CredRead.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(PCREDENTIAL)]
CredRead.restype = wintypes.BOOL
CredFree = ctypes.windll.advapi32.CredFree
CredFree.argtypes = [ctypes.c_void_p]

pcred = PCREDENTIAL()
target = 'GitHub - https://api.github.com/davilimarll'
if not CredRead(target, 1, 0, ctypes.byref(pcred)):
    print("Failed to read credentials")
    exit(1)

blob = ctypes.string_at(pcred.contents.CredentialBlob, pcred.contents.CredentialBlobSize)
CredFree(pcred)
token = blob.decode('utf-8', errors='ignore').strip('\x00')

repo_name = "obli-cooeducar-2024"
repo_desc = "Portal Oficial de Resultados da OBLI 2024.2 • Cooeducar & Seleta Educação"

# 1. Create repository via GitHub API
req_data = json.dumps({
    "name": repo_name,
    "description": repo_desc,
    "private": False,
    "auto_init": False
}).encode('utf-8')

req = urllib.request.Request("https://api.github.com/user/repos", data=req_data, method="POST")
req.add_header("Authorization", f"Bearer {token}")
req.add_header("Accept", "application/vnd.github.v3+json")
req.add_header("User-Agent", "HarryAssistant")

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Repo created successfully: {res.get('html_url')}")
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    if "name already exists" in err_body:
        print(f"Repo {repo_name} already exists, proceeding to push.")
    else:
        print(f"HTTPError {e.code}: {err_body}")
        exit(1)

# 2. Configure Git, add files, commit and push
commands = [
    ["git", "config", "user.name", "davilimarll"],
    ["git", "config", "user.email", "davilimarl@gmail.com"],
    ["git", "add", "."],
    ["git", "commit", "-m", "feat: portal interativo OBLI 2024.2 Cooeducar Carlos Chagas"],
    ["git", "branch", "-M", "main"],
    ["git", "remote", "remove", "origin"], # in case it exists
]

for cmd in commands:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.stdout.strip():
        print(f"{' '.join(cmd)} -> {p.stdout.strip()}")
    if p.stderr.strip() and "error" in p.stderr.lower():
        print(f"{' '.join(cmd)} ERR -> {p.stderr.strip()}")

# Remote with token for authenticated push
push_remote = f"https://davilimarll:{token}@github.com/davilimarll/{repo_name}.git"
p_remote = subprocess.run(["git", "remote", "add", "origin", push_remote], capture_output=True, text=True)

# Push to main
print("Pushing to GitHub...")
p_push = subprocess.run(["git", "push", "-u", "origin", "main", "--force"], capture_output=True, text=True)
print("Push stdout:", p_push.stdout)
print("Push stderr:", p_push.stderr)

# Reset remote URL to clean URL without token so credentials are never exposed
clean_remote = f"https://github.com/davilimarll/{repo_name}.git"
subprocess.run(["git", "remote", "set-url", "origin", clean_remote], capture_output=True, text=True)

print("Done! Repository URL:", clean_remote)
