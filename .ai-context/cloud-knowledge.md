# Cloud Knowledge: Lovable + Codex + Claude spolupráca

Tento dokument je spoločná prevádzková dohoda pre AI nástroje, aby sa zmeny navzájom neblokovali.

## 1) Lovable — ako pracuje a čo potrebuje
- Lovable typicky generuje/mení frontend štruktúru (komponenty, stránky, štýly, wiring).
- Potrebuje stabilné API kontrakty, názvy env premenných a predvídateľnú štruktúru priečinkov.
- Potrebuje, aby neboli priebežne prepisované jeho auto-generated časti bez koordinácie.

### Lovable guardrails
- Pred refaktorom core UI súborov najprv zapísať plán do `current-sprint.md`.
- Nemení sa bezdôvodne naming konvencia route/komponentov, ak na ňu nadväzuje Lovable.
- Pri zmene env/config vždy doplniť migration poznámku do `decisions.md`.

## 2) Codex/Claude — ako pracujú a čo potrebujú
- Codex/Claude robia presné kódové zásahy, testy, fixy, architektonické úpravy a dokumentáciu.
- Potrebujú jasné acceptance kritériá, stabilný cieľový branch workflow a single source of truth.
- Potrebujú vedieť, ktoré súbory sú auto-generated vs. manuálne spravované.

### Codex/Claude guardrails
- Pred zásahom overiť posledný Lovable push + otvorené PR.
- Pri zmenách, ktoré môžu rozbiť UI generation flow, najprv zapísať dopad do `decisions.md`.
- Nevykonávať rozsiahly rename/move bez explicitného owner súhlasu.

## 3) Spoločné pravidlá kompatibility
- **Najprv Lovable push (ak beží UI iterácia), potom Codex/Claude nadväzujúci zásah.**
- Všetko cez branch + PR; merge iba po owner approval.
- Každá session musí skončiť update `current-sprint.md`.
- Breaking zmeny musia mať:
  1. dôvod,
  2. dopad,
  3. rollback poznámku.

## 4) Konfliktné situácie (playbook)
- Ak Lovable a Codex upravili rovnaký modul:
  1. preferovať zachovanie funkčného user-flow,
  2. vybrať minimálny diff,
  3. konflikt rozhodnutie zapísať do `decisions.md`.
- Ak vznikne neistota, freeze merge a počkať na owner rozhodnutie.

## 5) Chránený kód bez obmedzenia tempa práce
- Chránenie sa robí procesne: PR-only + owner approval.
- Rýchlosť sa zachová tým, že Lovable pokračuje v UI iterácii a Codex/Claude robia cielené fixy v samostatných branchoch.
- Každá AI dodrží handoff checklist v `current-sprint.md`.
