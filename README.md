# Menei Vorios

This is the campaign notebook for our D&D game set on the continent of Menei Vorios — an Obsidian vault, version-controlled with git. This README covers how the vault is organized and how to use the templates and tools that have been set up for it. If you're new to Obsidian itself, the short version is: everything here is plain markdown, `[[double brackets]]` create links between notes, and the left sidebar is your file browser.

## Layout

```
Characters/
  PCs/           player characters
  NPCs/          non-player characters
Lore/
  Places/        continents, regions, cities, landmarks
  Mythology/     the gods
  Creatures/     monsters, hazards, and minor fey spirits (nymphs etc.)
  Factions/      organizations
  Events/        major historical events
Sessions/        one note per game session, in order
Templates/       starting point for every new note (see below)
```

Nothing is filed loosely — everything gets a home in the structure above, even one-off notes.

**The setting, in a sentence:** the continent used to be called Taeltoranou until a god-war called the Sundering, roughly 800 years back, shattered it into three landmasses now collectively called Menei Vorios. See [[Menei Vorios]] and [[Sundering of Taeltoranou]] for the full picture.

## Creating a new note from a template

Every note type has a matching template in `Templates/` (NPC, PC, Session, Place, Deity, Creature, Faction). To use one:

1. Create/open the note you want to fill in (e.g. a new file under `Characters/NPCs/`).
2. Open the command palette (`Ctrl/Cmd+P`) and run **Templates: Insert template**.
3. Pick the matching template from the list.

That fills in the note's frontmatter (the `---`-delimited block at the top — shows up as editable fields in the Properties panel) and section headings for you. A couple of things worth knowing about how they're set up:

- **`aliases`** is a real Obsidian feature (not something specific to this vault) — list any nicknames a character/place goes by, and Obsidian's search and link autocomplete will recognize them too. Only add it when there's an actual nickname in use; leave it off otherwise.
- Collapsed sections like **"GM Secrets & Hooks"** on NPC/PC notes render closed by default (click to expand) — useful for keeping twists out of the way without hiding them in a separate file.
- The italic text in `%% double-percent %%` blocks is an Obsidian comment — invisible in reading view, just there to remind you what goes where. Delete it or leave it, doesn't matter.

## Auto-linking entity mentions with AutoTag

It's easy to type "Crimini" or "the shrine" in a session recap and forget the `[[brackets]]`. There's a button for that.

At the bottom of every session note is an **AutoTag** button. Click it, and it scans that note for plain-text mentions of anything that already has a page — any PC, NPC, or Lore entry — and wraps them in links automatically. For example, typing:

> We take the left path. Crimini drops a glowing stone to mark our path.

and clicking AutoTag turns it into:

> We take the left path. [[Crimini]] drops a glowing stone to mark our path.

It won't touch anything already linked, won't touch code blocks, and matching isn't case-sensitive — "crimini", "CRIMINI", and "Crimini" all resolve the same way. It'll ask you to confirm before making any changes, since it edits the note directly.

You can also run it from the command palette instead of scrolling to the button: `Ctrl/Cmd+P` → **"Execute: Tag Entities"**.

### When a word means something more specific just for one session

Say a session repeatedly mentions "the shrine". There might be several shrines, and that session's plain "shrine" mentions need to point at one specific page (say, `[[Unknown Darkling Shrine]]`) without you having to type the long name every time, and without turning "shrine" into a permanent global nickname for that one page everywhere else in the vault.

That's what `local-aliases` is for. Add it to that session's frontmatter:

```yaml
local-aliases:
  - "shrine -> Unknown Darkling Shrine"
```

Now, in that note only, clicking AutoTag turns "shrine" into `[[Unknown Darkling Shrine|shrine]]` — the link points to the right page, but the visible text stays exactly as you wrote it. No other note is affected, and `Unknown Darkling Shrine.md` itself doesn't need any changes.

This field is optional — most sessions won't need it. Only add it if a generic term in that particular session needs to point somewhere more specific than its own name would suggest.

## Syncing across devices

The vault is a git repository, kept in sync with the **Obsidian Git** plugin, which auto-commits periodically ("vault backup: ..." commits) in addition to whatever you commit by hand. If you're setting this up on a new device, cloning the git repo gives you everything except your personal Obsidian workspace layout (open tabs, pane sizes) — that's intentionally not synced, since it's just per-session UI state and differs between desktop and mobile anyway.
