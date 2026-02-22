# Architecture

## High-level
- Frontend: React + Vite.
- UI styling: Tailwind CSS.
- Backend služby: Supabase (DB/Auth/API podľa implementácie v appke).
- Repo workflow: Lovable pushuje app zmeny, Claude/Codex nadväzujú cez branch/PR.

## Data flow (pracovný model)
1. Lovable pushne latest app state do canonical repo.
2. Claude/Codex načítajú `current-sprint.md` a overia posledný push.
3. Zmeny sa robia v branchi.
4. PR ide na owner review.
5. Merge do `main` iba po owner approval.

## Prevádzkové pravidlá
- Jediný zdroj pravdy: `MENUMAT-MENUMAESTRO-AKTUAL`.
- Žiadne paralelné “shadow” repo pre ten istý projekt.
- Pri zmene stacku alebo infra okamžite aktualizovať tento dokument.
