# AI Sync Context (MENUMAT - MENUMAESTRO AKTUAL)

Tento priečinok je **zdieľaná pamäť pre AI** (Claude Code, Codex, Lovable cez GitHub sync).

## Canonical repository
- **Oficiálny názov repo:** `MENUMAT-MENUMAESTRO-AKTUAL`
- Všetky AI pracujú iba v tomto jednom repozitári.
- Ak sa objaví nové auto-generated repo, nepoužívať ho ako zdroj pravdy.

## Princíp
- GitHub repo je jeden zdroj pravdy.
- Každá AI číta rovnaký kontext pred začiatkom práce.
- Každá AI zapíše výsledok na konci session.

## Povinný workflow pri každej session
1. **SESSION ŠTART**
   - prečítaj `current-sprint.md`
   - over, že pracuješ v canonical repo `MENUMAT-MENUMAESTRO-AKTUAL`
   - over posledný Lovable push
2. **POČAS PRÁCE**
   - zmeny rob cez branch + PR
   - nevykonávaj priame zásahy do `main`
3. **SESSION KONIEC**
   - aktualizuj `current-sprint.md`
   - podľa potreby aktualizuj `architecture.md`, `decisions.md`, `KNOWN_ISSUES.md`
   - commitni kontext update správou: `chore: update ai-context after session`

## Governance (schvaľovanie zmien)
- Pluginy/AI môžu navrhnúť zmeny, ale **merge je len po výslovnom schválení vlastníkom**.
- Preferovaný režim: PR-only workflow (žiadny direct push do `main`).
- Ak GitHub plán neumožní plnú branch protection, pravidlo sa vynucuje procesne (manual owner approval).

## Súbory a zodpovednosť
| Súbor | Claude Code | Codex | Lovable |
|---|---|---|---|
| `README.md` | číta | číta | — |
| `current-sprint.md` | číta + píše | číta + píše | — |
| `architecture.md` | číta + píše | číta + píše | — |
| `decisions.md` | píše | píše | — |
| `KNOWN_ISSUES.md` | číta + píše | číta + píše | — |

## Cloud knowledge (operating agreement)
- Detailná spolupráca Lovable + Codex + Claude je v `.ai-context/cloud-knowledge.md`.
- Pred väčšími zásahmi do štruktúry alebo configu tento dokument prečítať.
