# CLAUDE.md – SmartAir Web Project

> Tento súbor je určený pre AI asistentov (Claude, Copilot, Cursor, Codex).
> Prečítaj ho celý pred akoukoľvek zmenou v repozitári.

## 🏢 O projekte

**SmartAir** je webová prezentácia a backend pre firmu SmartAir s.r.o. (Bratislava, SK).
Firma predáva a montuje klimatizácie DAIKIN, Samsung, TCL, Midea.

- **Web:** Webflow CMS (frontend) + Cloudflare Workers (API backend)
- **Jazyk:** Slovenčina (SK) – všetok obsah webu je po slovensky
- **Majiteľ:** Mgr. Norbert Považanec (SmartAir s.r.o., Kopčianska 8, 85101 Bratislava)

## 🏗️ Architektúra

```
Webflow CMS (frontend/obsah)
    ↕ Webflow API
Cloudflare Workers (API layer)
    ↕ GitHub Actions (CI/CD deploy)
GitHub repo (zdrojový kód)
```

## 📁 Štruktúra repozitára

```
/app          – FastAPI Python backend (legacy, momentálne neaktívny)
/deploy       – deployment skripty pre VPS/Cloudflare
/workers      – Cloudflare Workers kód (aktívny)
/.github      – GitHub Actions CI/CD workflow
```

## ⚙️ Technológie

- Cloudflare Workers (JavaScript/TypeScript)
- Python FastAPI (legacy backend)
- GitHub Actions pre auto-deploy
- Webflow CMS API integrácia

## 🔑 Premenné prostredia

Pozri `.env.example` – NIKDY necommituj `.env`!
Skutočné hodnoty sú len lokálne alebo v Cloudflare dashboard.

## 🚦 Pravidlá pre AI asistentov

### ✅ Povolené
- Upravovať kód v `/workers` a `/deploy`
- Opravovať chyby, pridávať features podľa zadania
- Aktualizovať dokumentáciu

### ❌ ZAKÁZANÉ
- Commitovať `.env`, API kľúče, tokeny, heslá
- Meniť `main` branch priamo – vždy cez PR
- Mazať existujúce workflow súbory bez potvrdenia
- Pridávať nové npm/pip závislosti bez schválenia majiteľom

## 📝 Konvencie

- Commit správy: `feat:`, `fix:`, `docs:`, `refactor:` (Conventional Commits)
- Jazyk kódu: angličtina
- Jazyk komentárov a dokumentácie: slovenčina alebo angličtina
- Branch naming: `feature/nazov`, `fix/nazov`, `docs/nazov`

## 🔄 Posledné zmeny (changelog pre AI)

- **2026-02-23** – Pridaný `.env` do `.gitignore` (security fix)
- **2026-02-23** – Pridaný `.env.example` template
- **2026-02-23** – Vytvorený tento CLAUDE.md
- **2026-02-23** – Prečistené staré vetvy (codex/*, revert-*)

## 🤝 Súvisiace projekty

- `menumat-ecb44ba0` – MENUMAT aplikácia (reštauračný menu systém)
- `MENUGENERATOR` – starší menu generátor
- DreamAir s.r.o. – sesterská firma (rovnaký majiteľ)

## ❓ Pri pochybnostiach

Ak si nie si istý zmenou, **opýtaj sa majiteľa** pred commitom.
Kontakt: Norbert Považanec (SmartAir s.r.o.)
