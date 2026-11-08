---
tags:
  - session
session: 6
date: 2026-11-08
pcs:
  -
---

%% Recap goes here: first-person, in-character, present as it happened (typos and all — this is a player's voice, not prose to be polished). Break out any fight inline with a "### Combat" subheading and turn-by-turn bullets, same as previous sessions.

If a generic word in this session should link somewhere more specific than its own page (e.g. "shrine" meaning [[Shrine of Thandrios]] just for this session, without touching shrine.md itself or any other session), add a local-aliases list to the frontmatter above before running AutoTag:
local-aliases:
  - "shrine -> Shrine of Thandrios"
This only affects this note. It's a flat list (not a mapping) so Obsidian's Properties panel doesn't flag it as a type mismatch. Omit the field entirely when not needed. %%

The invisible NPC Dmia bumps into is a duergar. He and a second duergar look startled and then shut the door and shout for guards to come help. Slippery bitches. I try to force the door open and it doesnt budge. We look round quickly for another way out and find a secret passage open in the office the hobgoblins came from. We go in and pull the lever inside to close the passageway. I light a torch and we start travelling down the tunnel. It seems to be well trodden, theres lots of footprints going each direction. We travel down it for about an hour before we run into some stairs. They lead up to another doorway with a lever. 

## NPCs Encountered

- 

## Loot & Rewards

- 

> [!note]- Hooks for Next Session
> 

%% AutoTag button: runs .scripts/tag_entities.py --apply against this note, via the "Tag Entities" shell command in .obsidian/plugins/obsidian-shellcommands/data.json (user-owned config, id g5z3njeko3). Asks for confirmation before each run since --apply writes to the note.

The button block below has no colons after its field names, and action refers to the shell command by its command-palette label ("Shell commands: Execute: Tag Entities"), not its raw id — a colon-separated/id-based version looks identical but silently fails to render as a real button. Don't "fix" this without testing.

If editing the shell command itself in Settings → Shell commands: never wrap a {{variable}} in your own quotes. It already backslash-escapes every special character (including / and spaces) in each variable, expecting to be inserted unquoted — quoting on top breaks that, since bash doesn't collapse \/ inside double quotes. %%
```button
name AutoTag
type command
action Shell commands: Execute: Tag Entities
```
^button-autotag
