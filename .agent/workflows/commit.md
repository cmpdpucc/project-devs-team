---
description: Atomic semantic commit workflow. Conventional Commits format. Account-agnostic via gh CLI.
---

# /commit — Smart Commit Protocol

Esegue commit atomico con messaggio Conventional Commits e push opzionale.

---

## Uso rapido

// turbo
```powershell
python .agent/scripts/smart_commit.py --from-plan --all --push
```

---

## Step 1: Verifica stato repository

```powershell
python .agent/scripts/smart_commit.py --status
```

Output JSON con: branch, remote URL, dirty files, user.

---

## Step 2: Commit con messaggio esplicito

```powershell
# Sintassi base
python .agent/scripts/smart_commit.py "messaggio" --type feat --scope memory --all --push

# Esempi per tipo di lavoro:
# Nuova feature
python .agent/scripts/smart_commit.py "add pre-flight validation gate" --type feat --scope pre-flight --all --push

# Fix
python .agent/scripts/smart_commit.py "handle missing npm on Windows" --type fix --scope scripts --all --push

# Documentazione / regole
python .agent/scripts/smart_commit.py "add commit protocol rule" --type docs --scope rules --all --push

# Config / tooling
python .agent/scripts/smart_commit.py "update gitignore with pycache" --type chore --all --push
```

---

## Step 3 (Prima volta): Creare repo remota

```powershell
# Crea repo pubblica su GitHub (account da gh auth status) + push
python .agent/scripts/smart_commit.py "init: initial commit" --type chore --all --create-remote --push

# Repo privata
python .agent/scripts/smart_commit.py "init: initial commit" --type chore --all --create-remote --private --push
```

---

## Step 4: Auto-commit dal piano

```powershell
# Legge ultimo [x] da ralph_plan.md, genera messaggio, commit e push
python .agent/scripts/smart_commit.py --from-plan --all --push
```

---

## Recovery se push fallisce

```powershell
# Verifica autenticazione gh
gh auth status

# Refresh token se scaduto
gh auth refresh

# Retry push manuale
git push -u origin main

# Se divergita: rebase
git pull --rebase origin main
git push
```

---

## Conventional Commits Quick Reference

```
feat(scope): descrizione      # Nuova feature
fix(scope): descrizione       # Bug fix
docs(scope): descrizione      # Regole/docs
refactor(scope): descrizione  # Refactoring
test(scope): descrizione      # Test
chore: descrizione            # Tooling/config
```
