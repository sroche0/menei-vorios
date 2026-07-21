#!/usr/bin/env python3
"""Auto-link plain-text mentions of known vault entities in a markdown note.

Entities are discovered from note titles under Characters/PCs, Characters/NPCs,
and Lore/ (Places, Mythology, Creatures, Factions), plus any nicknames listed in
each note's own `aliases:` frontmatter. Matching is case-insensitive, so aliases
only need to cover genuinely different spellings (e.g. "Dmia" for "D'mia
Vuurhand") — casing variants like "steely dan" for "Steely Dan" are handled
automatically. A plain-text mention that isn't already inside a wikilink gets
wrapped into [[Title]] when it matches the title's exact casing, or
[[Title|as written]] otherwise, so the original text is never altered.

A note being processed can also define its own `local-aliases:` frontmatter
list, with each entry in "word -> Target Page" form, e.g.:

    local-aliases:
      - "shrine -> Shrine of Thandrios"

This only affects that one file: "shrine" (or "Shrine", any case) links to
[[Shrine of Thandrios|shrine]] in this note, without touching shrine.md's own
aliases or any other note that mentions "shrine". It overrides a same-named
global entity for the file it's declared in. It's a flat list (like `aliases`
or `pcs` elsewhere in this vault) rather than a YAML mapping, since Obsidian's
Properties panel doesn't have a UI for arbitrary key/value frontmatter and
will flag a mapping as a type mismatch.

Usage:
    tag_entities.py "Sessions/Session 2.md"          # dry run, prints a diff
    tag_entities.py --apply "Sessions/Session 2.md"  # writes the changes
"""

import argparse
import difflib
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent

ENTITY_FOLDERS = [
    "Characters/PCs",
    "Characters/NPCs",
    "Lore/Places",
    "Lore/Mythology",
    "Lore/Creatures",
    "Lore/Factions",
]

FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[.*?\]\]")


def parse_yaml_list(frontmatter_text, key):
    """Minimal parser for a top-level `key:` YAML list. No external deps."""
    items = []
    in_section = False
    for line in frontmatter_text.splitlines():
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            in_section = True
            continue
        if in_section:
            match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if not match:
                in_section = False
                continue
            value = match.group(1).strip().strip('"').strip("'")
            if value:
                items.append(value)
    return items


def parse_aliases(frontmatter_text):
    """Parser for a top-level `aliases:` YAML list."""
    return parse_yaml_list(frontmatter_text, "aliases")


def parse_local_aliases(frontmatter_text):
    """Parser for a top-level `local-aliases:` YAML list of "word -> Target Title" entries."""
    local_aliases = {}
    for entry in parse_yaml_list(frontmatter_text, "local-aliases"):
        if "->" not in entry:
            continue
        key, _, value = entry.partition("->")
        key = key.strip().lower()
        value = value.strip()
        if key and value:
            local_aliases[key] = value
    return local_aliases


def load_entities():
    """Return {lowercased surface_form: canonical_title} for every note title and alias."""
    entities = {}
    for folder in ENTITY_FOLDERS:
        folder_path = VAULT_ROOT / folder
        if not folder_path.is_dir():
            continue
        for note_path in sorted(folder_path.glob("*.md")):
            title = note_path.stem
            entities[title.lower()] = title
            text = note_path.read_text(encoding="utf-8")
            fm_match = FRONTMATTER_RE.match(text)
            if not fm_match:
                continue
            for alias in parse_aliases(fm_match.group(1)):
                entities.setdefault(alias.lower(), title)
    return entities


def split_on(text, pattern):
    """Split text into (is_match, chunk) pairs around pattern matches."""
    chunks = []
    last_end = 0
    for m in pattern.finditer(text):
        if m.start() > last_end:
            chunks.append((False, text[last_end:m.start()]))
        chunks.append((True, m.group(0)))
        last_end = m.end()
    if last_end < len(text):
        chunks.append((False, text[last_end:]))
    return chunks


def link_entities(body, entities):
    """Wrap untagged mentions in body with [[...]], skipping code blocks/links."""
    if not entities:
        return body, 0

    surface_forms = sorted(entities, key=len, reverse=True)
    combined_re = re.compile(
        r"\b(" + "|".join(re.escape(s) for s in surface_forms) + r")\b", re.IGNORECASE
    )
    count = 0

    def repl(m):
        nonlocal count
        as_written = m.group(1)
        canonical = entities[as_written.lower()]
        count += 1
        return f"[[{canonical}]]" if as_written == canonical else f"[[{canonical}|{as_written}]]"

    out = []
    for is_code, code_chunk in split_on(body, CODE_BLOCK_RE):
        if is_code:
            out.append(code_chunk)
            continue
        for is_link, chunk in split_on(code_chunk, WIKILINK_RE):
            out.append(chunk if is_link else combined_re.sub(repl, chunk))
    return "".join(out), count


def process_file(path, entities, apply):
    text = path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_RE.match(text)
    frontmatter, body = (text[:fm_match.end()], text[fm_match.end():]) if fm_match else ("", text)

    file_entities = entities
    if fm_match:
        local_aliases = parse_local_aliases(fm_match.group(1))
        if local_aliases:
            file_entities = {**entities, **local_aliases}

    new_body, count = link_entities(body, file_entities)
    rel = path.relative_to(VAULT_ROOT)

    if count == 0:
        print(f"{rel}: no untagged mentions found")
        return

    print(f"{rel}: {count} mention(s) linked")
    if apply:
        path.write_text(frontmatter + new_body, encoding="utf-8")
    else:
        diff = difflib.unified_diff(
            body.splitlines(keepends=True),
            new_body.splitlines(keepends=True),
            fromfile="before", tofile="after",
        )
        print("".join(diff))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path, help="Markdown file(s) to process")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry run, prints a diff)")
    args = parser.parse_args()

    entities = load_entities()
    for file_path in args.files:
        process_file(file_path.resolve(), entities, args.apply)


if __name__ == "__main__":
    main()
