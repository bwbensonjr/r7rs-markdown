# R7RS Markdown

A legible, complete Markdown formatting of the R7RS-small specification
(*Revised⁷ Report on the Algorithmic Language Scheme*), generated automatically
from the official LaTeX sources.

- [`markdown/README.md`](markdown/README.md) — Title page, table
  of contents, and an alphabetic index of every procedure and keyword.
- [`markdown/r7rs.md`](markdown/r7rs.md) — The whole report
  in one document.
- [`markdown/`](markdown/) - Individual files.

## Relationship to r7rs-spec

This repository references John Cowan's upstream
[`r7rs-spec`](https://github.com/johnwcowan/r7rs-spec) repository as a
pinned git submodule at [`r7rs-spec/`](r7rs-spec). The LaTeX sources
live there and remain owned upstream; this repo adds only the
converter and the generated Markdown.

```
r7rs-markdown/
├── r7rs-spec/        # submodule → johnwcowan/r7rs-spec (pinned commit)
├── tools/tex2md.py   # LaTeX → Markdown converter (stdlib Python)
├── markdown/         # generated output (committed)
└── Makefile          # `make markdown`
```

## Getting the sources

Clone with the submodule:

```bash
git clone --recurse-submodules https://github.com/bwbensonjr/r7rs-markdown.git
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

## Regenerating the Markdown

```bash
make markdown
```

This runs the converter against `r7rs-spec/spec/*.tex` and rewrites
`markdown/`. To pull newer upstream changes and regenerate:

```bash
make update-spec        # advances the submodule, then rebuilds markdown/
git add r7rs-spec markdown
git commit -m "Update to latest r7rs-spec"
```

The converter maps the report's custom LaTeX macros (procedure prototypes,
`scheme` examples, BNF grammars, cross-references, the bibliography, and the
formal denotational semantics) to GitHub-flavored Markdown, using GitHub math
(`$...$` / `$$...$$`) for the formal semantics.

## Attribution and license

The specification text is the work of the R7RS editors and the Scheme language
working group; the report grants permission to copy it in whole or in part.
See the upstream [`r7rs-spec`](https://github.com/johnwcowan/r7rs-spec)
repository for the authoritative sources and the typeset
[`r7rs.pdf`](r7rs-spec/spec/r7rs.pdf). This repository contributes only the
`tools/tex2md.py` converter and the generated Markdown.
