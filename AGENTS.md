# AGENTS.md

Guidance for AI agents working in this repository.

## What this is

An Obsidian vault holding the notes for a D&D campaign set on the continent of Menei Vorios. There is no code, no build, no lint, no tests — every file is a markdown note, and "correctness" means consistency with established lore/characters, not compiling or passing checks.

This file is a normal, non-hidden, git-tracked file at the repo root — deliberately so, since agent tooling discovers `AGENTS.md` by scanning for that exact filename by convention. It will show up in Obsidian's file explorer like any other root file; don't move it into a dotfolder or rename it to hide it, that would break discovery. (Obsidian's "Excluded files" setting was tried for this and doesn't actually hide items from the file explorer sidebar despite documentation suggesting otherwise — it only affects search/indexing.)

## Structure

- `Characters/PCs/` — player characters
- `Characters/NPCs/` — non-player characters
- `Lore/` — worldbuilding notes, split into `Places/`, `Mythology/` (named gods only), `Creatures/` (monsters, hazards, and minor fey spirits alike), `Factions/`, and `Events/`. No top-level catch-all — everything gets filed into the category it fits, even one-offs.
- `Sessions/` — chronological play logs (`Session 0.md`, `Session 1.md`, ...)
- `Templates/` — one template per note type (see below), wired up as the core Templates plugin's template folder
- `.scripts/` — tooling (see Tooling below); dot-prefixed so Obsidian's file explorer hides it, same as `.obsidian`/`.git` — still fully visible to any IDE/terminal, just not in Obsidian's own sidebar

## Setting, briefly

The continent was Taeltoranou until the Sundering — a god-war roughly 800 years ago — shattered it into three disconnected landmasses, now collectively called Menei Vorios. The `Lore/Places/` notes for the three regions carry a parenthetical color matching their color on the campaign's physical map (Symmiach of Epolais = purple, Kainogian Coast = yellow, Kremnis Isles = red; Thialodias Highlands = green is a fourth area within reach). Noble bloodlines carry the Sevistheixi, a divine mark. `Lore/Mythology/` covers the gods and the war; `Lore/Events/Sundering of Taeltoranou.md` is the central event most other lore notes trace back to.

## Conventions

- Cross-reference everything with wikilinks: `[[Note Name]]`. Use `[[Note Name|Display Text]]` when the visible text needs to differ (possessives, nicknames, mid-sentence grammar).
- Notes are deliberately terse — usually one sentence to a short paragraph, not exhaustive stat blocks or lore dumps.
- Session logs are written in first person, in-character, in an informal/unedited voice — typos and lowercase are left as-is deliberately, it's a player's voice, not prose to copyedit. A fight is broken out under a `### Combat` (or `### combat`) subheading with turn-by-turn bullets.
- Some notes are intentionally empty stubs (placeholders for content not yet written, not broken files) — don't fill them in with invented content.
- Renaming a note inside Obsidian auto-updates every `[[link]]` to it across the vault (and can offer to add the old name as an alias). Renaming or moving a note outside Obsidian (raw `mv`, `git mv`, scripts) does **not** update links — fix them by hand if you do this.

### Templates and frontmatter

Every note type has a template in `Templates/`, each using frontmatter, an `%% Obsidian comment %%` in place of write-up instructions, and a collapsed `> [!note]-`/`> [!danger]-` callout for secondary detail. Existing notes outside `Templates/` generally follow their type's template already; match the template's shape for anything new.

- `Templates/NPC.md` — `tags`, `aliases`, `race`, `status`, `location`, `affiliation`, plus a quote callout and a collapsed "GM Secrets & Hooks" callout.
- `Templates/PC.md` — `tags`, `aliases`, `player`, `race`, `class`, `status`, plus a quote callout, Backstory/Relationships sections, and a collapsed "GM Secrets & Hooks" callout.
- `Templates/Session.md` — `tags`, `session`, `date`, `pcs`, plus NPCs Encountered / Loot & Rewards sections, a collapsed "Hooks for Next Session" callout, and an AutoTag button (see Tooling).
- `Templates/Place.md` — `tags`, `aliases`, `type`, `region`, `common-races`, plus a collapsed "Notable Locations" callout.
- `Templates/Deity.md` — `tags`, `aliases`, `domain`, `symbol`, plus a collapsed "Marked Bloodlines & Followers" callout.
- `Templates/Creature.md` — `tags`, `aliases`, `type`, `threat`, `weaknesses`, plus a collapsed "Abilities & Weaknesses" callout. Flexible enough to cover both monster-stat-block entries and one-line minor spirits — leave `threat`/`weaknesses`/the callout blank for the latter.
- `Templates/Faction.md` — `tags`, `aliases`, `patrons`, plus a collapsed "Notable Members" callout.

`aliases` is Obsidian's own recognized frontmatter property (search/quick-switcher/link-suggestions all read it); it's the place to record a nickname used in prose (e.g. "Dmia" for D'mia Vuurhand). It's sparse by design — only add it to a note when a real nickname is in use, don't add an empty `aliases:` just for schema completeness. `.scripts/tag_entities.py` matches titles and aliases case-insensitively, so an alias only needs to cover genuinely different spellings, not casing variants.

`Gods.md` and `Events/Sundering of Taeltoranou.md` are deliberately plain prose with no frontmatter — they're overviews, not single-entity entries, so no template applies to them.

## Editing guidance

- Preserve the in-character voice and existing typos in `Sessions/` logs; don't "fix" them.
- When a session log mentions an entity, place, or item that doesn't have a note yet, it's fine to create one via the wikilink target, following the existing terse one-liner style.
- Don't invent plot, lore, or character details beyond what's already in the vault or what the user tells you directly — this is a living record of an actual game, not fiction to extend on your own.

## Tooling

- `.scripts/tag_entities.py` scans a note for plain-text mentions of known entities (titles/aliases from `Characters/PCs`, `Characters/NPCs`, and `Lore/`) and wraps untagged ones in `[[...]]`, preserving the exact text as written via `[[Title|as written]]` whenever it doesn't match the title's casing/spelling exactly. Pure stdlib, no dependencies. Skips fenced code blocks and anything already inside a wikilink. Defaults to a dry-run diff; pass `--apply` to write. Run directly: `python3 .scripts/tag_entities.py "Sessions/Session N.md"`.

- **`local-aliases`**: a note can declare its own `local-aliases:` frontmatter list to override the global entity map for that file only. Each entry is a string in `"word -> Target Page Title"` form:
  ```yaml
  local-aliases:
    - "shrine -> Unknown Darkling Shrine"
  ```
  Use this when a generic term used in one note's prose (e.g. "shrine") should resolve to a more specific page than its own name suggests, without adding a permanent global alias or renaming/rewording the prose. It's a flat list rather than a mapping because Obsidian's Properties panel has no UI for arbitrary key/value frontmatter and will flag a mapping as a type mismatch. Field is opt-in and sparse — omit it entirely on notes that don't need it, and don't add it as a blank key to `Templates/Session.md`.

- **AutoTag button**: `Templates/Session.md` and existing session notes have a button that runs the script against the current note. The **Shell commands** (`obsidian-shellcommands`) and **Buttons** (`buttons`) community plugins provide this. The exact button syntax matters — a colon-separated / command-id-based version looks identical in raw markdown but silently fails to render as a real button:
  ```button
  name AutoTag
  type command
  action Shell commands: Execute: Tag Entities
  ```
  ^button-autotag

  No colons after the field names. `action` refers to the shell command by its **command-palette display label** ("Shell commands: Execute: Tag Entities"), not its raw registered id — don't "fix" this to an id-based form without testing. The underlying shell command (configured in `.obsidian/plugins/obsidian-shellcommands/data.json`, user-owned — diff before editing) runs `/usr/bin/python3 {{vault_path}}/.scripts/tag_entities.py --apply {{file_path:absolute}}` with `confirm_execution: true`.

  **Never wrap a `{{variable}}` in your own quotes in a Shell commands string.** The plugin's escaper already backslash-escapes every special character (including `/` and spaces) in a variable's value, expecting it to be inserted unquoted. Adding `"..."` around it breaks that — bash doesn't treat `\/` as an escape inside double quotes, so the backslashes stay literal and corrupt the value.

## Version control

- The vault is synced to git via the Obsidian Git plugin (`.obsidian/plugins/obsidian-git`) as well as manual commits — don't assume every commit was made by a human typing `git commit`.
- `.gitignore` excludes `Private/`, `exclude*`, `.DS_Store`, and Obsidian's per-session workspace state. `Private/` is reserved for GM-only material that shouldn't be shared with players; treat that exclusion boundary as intentional even though the folder doesn't exist yet.
