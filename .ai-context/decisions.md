# Decisions log

## 2026-02-22 — AI sync režim cez `.ai-context/`
**Decision:** Používať `.ai-context/` ako povinnú zdieľanú pamäť medzi Claude Code a Codex.

**Why:**
- kontinuita medzi session bez opakovaného vysvetľovania
- transparentný audit trail rozhodnutí

**Consequence:**
- na začiatku každej session sa číta `current-sprint.md`
- na konci každej session sa aktualizuje `current-sprint.md`
- významné zmeny sa zapisujú do `decisions.md` a `architecture.md`

## 2026-02-22 — Canonical repo je `MENUMAT-MENUMAESTRO-AKTUAL`
**Decision:** Po migrácii a rename je jediný canonical repozitár `MENUMAT-MENUMAESTRO-AKTUAL`.

**Why:**
- všetky AI musia čítať/písať jeden rovnaký zdroj pravdy
- eliminuje sa riziko splitu kontextu medzi viaceré repá

**Consequence:**
- všetky budúce AI session pokračujú len v tomto repo
- reference na staré názvy repo sa považujú za historické

## 2026-02-22 — Owner approval-only merge režim
**Decision:** Zmeny môžu byť implementované AI, ale merge do `main` iba po explicitnom schválení vlastníkom.

**Why:**
- ochrana proti nechceným automatickým zásahom pluginov/agentov
- zachovanie stabilného bodu projektu

**Consequence:**
- povinný branch + PR workflow
- aj pri absencii plnej branch protection sa pravidlo vynucuje procesne


## 2026-02-22 — Cloud knowledge dohoda pre spoluprácu AI
**Decision:** Zavedený spoločný dokument `.ai-context/cloud-knowledge.md` s guardrails pre Lovable/Codex/Claude.

**Why:**
- predísť zmenám, ktoré blokujú iný nástroj alebo rozbijú workflow
- zachovať tempo práce aj pri chránenom kóde

**Consequence:**
- pred väčšími zásahmi je povinné prečítať cloud knowledge
- konfliktné rozhodnutia sa zapisujú do `decisions.md`
