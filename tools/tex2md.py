#!/usr/bin/env python3
"""Convert the R7RS-small LaTeX sources (spec/*.tex) to legible Markdown.

Usage:  python3 tools/tex2md.py [--spec DIR] [--out DIR]

Produces, in the output directory (default: markdown/):
  * one Markdown file per chapter (NN-name.md),
  * a concatenated single-file build (r7rs.md),
  * a README.md with title, credits, and a linked table of contents.

The converter is tailored to the specific macro set defined in
spec/commands.tex; it is re-runnable as the .tex sources change.
"""

import argparse
import os
import re
import sys

# --------------------------------------------------------------------------
# Output grouping: each output chapter is one or more source files, in the
# document order given by spec/r7rs.tex.
# --------------------------------------------------------------------------

GROUPS = [
    # (output basename, [source files])
    ("01-introduction",        ["intro.tex"]),
    ("02-overview",            ["struct.tex"]),
    ("03-lexical-conventions", ["lex.tex"]),
    ("04-basic-concepts",      ["basic.tex"]),
    ("05-expressions",         ["expr.tex"]),
    ("06-program-structure",   ["prog.tex"]),
    ("07-standard-procedures", ["procs.tex"]),
    ("08-formal-syntax-and-semantics", ["syn.tex", "sem.tex", "derive.tex"]),
    ("09-standard-libraries",  ["stdmod.tex"]),
    ("10-feature-identifiers", ["features.tex"]),
    ("11-language-changes",    ["notes.tex"]),
    ("12-additional-material", ["repository.tex"]),
    ("13-example",             ["example.tex"]),
    ("14-references",          ["bib.tex"]),
]

# --------------------------------------------------------------------------
# Small helpers for brace matching and argument reading
# --------------------------------------------------------------------------

def match_brace(s, i):
    """s[i] must be '{'. Return index of the matching '}', or len(s) if none."""
    depth = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n


def read_arg(s, i):
    """Read one macro argument starting at index i (after the command name).

    Skips leading spaces. Returns (arg_text, next_index). A brace group returns
    its contents; otherwise a single character (or a \\command) token.
    """
    n = len(s)
    while i < n and s[i] in ' \t\n':
        i += 1
    if i >= n:
        return '', i
    if s[i] == '{':
        j = match_brace(s, i)
        return s[i + 1:j], j + 1
    if s[i] == '\\':
        m = re.match(r'\\([A-Za-z]+|.)', s[i:])
        if m:
            return s[i:i + m.end()], i + m.end()
        return s[i], i + 1
    return s[i], i + 1


# --------------------------------------------------------------------------
# User macro (\newcommand) collection and expansion
# --------------------------------------------------------------------------

def collect_newcommands(text):
    """Return {name: (nargs, body)} for \\newcommand/\\renewcommand in text."""
    macros = {}
    for m in re.finditer(r'\\(?:re)?newcommand\s*\*?\s*', text):
        i = m.end()
        # command name: \name  or {\name}
        if i < len(text) and text[i] == '{':
            j = match_brace(text, i)
            name_tok = text[i + 1:j].strip()
            i = j + 1
        else:
            nm = re.match(r'\\([A-Za-z]+)', text[i:])
            if not nm:
                continue
            name_tok = '\\' + nm.group(1)
            i += nm.end()
        nm = re.match(r'\\([A-Za-z]+)', name_tok)
        if not nm:
            continue
        name = nm.group(1)
        # optional [nargs]
        nargs = 0
        mm = re.match(r'\s*\[(\d+)\]', text[i:])
        if mm:
            nargs = int(mm.group(1))
            i += mm.end()
        # optional default arg [..] -> skip (rare); then body group
        while i < len(text) and text[i] in ' \t\n':
            i += 1
        if i >= len(text) or text[i] != '{':
            continue
        j = match_brace(text, i)
        body = text[i + 1:j]
        macros[name] = (nargs, body)
    # \def\name<#1..>{body}  (used heavily in the formal semantics)
    for m in re.finditer(r'\\def\s*\\([A-Za-z]+)\s*((?:#\d)*)\s*\{', text):
        name = m.group(1)
        nargs = len(re.findall(r'#\d', m.group(2)))
        brace = text.index('{', m.end() - 1)
        j = match_brace(text, brace)
        macros[name] = (nargs, text[brace + 1:j])
    return macros


def expand_macros(text, macros, depth=0):
    """Expand user macros (with #1.. substitution). Best-effort, bounded."""
    if depth > 12 or not macros:
        return text
    out = []
    i = 0
    n = len(text)
    changed = False
    while i < n:
        c = text[i]
        if c == '\\':
            m = re.match(r'\\([A-Za-z]+)', text[i:])
            if m and m.group(1) in macros:
                name = m.group(1)
                nargs, body = macros[name]
                j = i + m.end()
                args = []
                for _ in range(nargs):
                    a, j = read_arg(text, j)
                    args.append(a)
                repl = body
                for k, a in enumerate(args, 1):
                    repl = repl.replace('#%d' % k, a)
                out.append(repl)
                i = j
                changed = True
                continue
            # not a user macro: copy command token verbatim
            out.append(text[i:i + (m.end() if m else 2)])
            i += (m.end() if m else 2)
            continue
        out.append(c)
        i += 1
    result = ''.join(out)
    if changed:
        return expand_macros(result, macros, depth + 1)
    return result


# --------------------------------------------------------------------------
# Character-level maps
# --------------------------------------------------------------------------

SUB = {'': '', '0': '₀', '1': '₁', '2': '₂', '3': '₃',
       '4': '₄', '5': '₅', 'i': 'ᵢ', 'j': 'ⱼ',
       'n': 'ₙ', 'k': 'ₖ'}
SUP = {'2': '²', '3': '³', '4': '⁴', '5': '⁵',
       '6': '⁶', '7': '⁷', 'n': 'ⁿ'}

# var/vr family: command suffix -> subscript key
VAR_FAMILY = {'var': '', 'vari': '1', 'varii': '2', 'variii': '3',
              'variv': '4', 'varj': 'j', 'varn': 'n',
              'vr': '', 'vri': '1', 'vrii': '2', 'vriii': '3', 'vriv': '4',
              'vrv': '5', 'vrj': 'j', 'vrn': 'n'}
# hyper/meta family: command suffix -> subscript key
HYP_FAMILY = {'hyper': '', 'meta': '', 'hyperi': '1', 'hyperii': '2',
              'hyperj': 'i', 'hypern': 'n'}

ESCAPES = {'%': '%', '_': '_', '&': '&', '$': '$', '#': '#', '{': '{',
           '}': '}', ' ': ' ', ',': ' ', ';': ' ', '!': '', '/': '',
           '-': '­'}  # \- discretionary hyphen -> soft hyphen

ACCENTS = {
    '"a': 'ä', '"o': 'ö', '"u': 'ü', '"A': 'Ä',
    '"O': 'Ö', '"U': 'Ü', '"e': 'ë', '"i': 'ï',
    "'a": 'á', "'e": 'é', "'i": 'í', "'o": 'ó',
    "'u": 'ú', "'c": 'ć', "'n": 'ń', "'s": 'ś',
    "'z": 'ź', "'y": 'ý', "'A": 'Á', "'E": 'É',
    '`a': 'à', '`e': 'è', '`i': 'ì', '`o': 'ò',
    '`u': 'ù', '^a': 'â', '^e': 'ê', '^i': 'î',
    '^o': 'ô', '^u': 'û', '~n': 'ñ', '~a': 'ã',
    '~o': 'õ', 'ca': 'ą', 'cc': 'ç', 'ce': 'ę',
    'cs': 'ş', ' va': 'ǎ', 'vs': 'š', 'vz': 'ž',
    'vc': 'č', 'vr': 'ř', '.z': 'ż', '.e': 'ė',
}

# --------------------------------------------------------------------------
# Inline conversion
# --------------------------------------------------------------------------

# Simple 0-argument command replacements (name -> replacement)
ZERO_CMD = {
    'schfalse': '`#f`', 'schtrue': '`#t`',
    'sharpfalse': '`#false`', 'sharptrue': '`#true`',
    'rthreers': 'R³RS', 'rfourrs': 'R⁴RS', 'rfivers': 'R⁵RS',
    'rsixrs': 'R⁶RS', 'rsevenrs': 'R⁷RS',
    'exprtype': 'syntax', 'auxiliarytype': 'auxiliary syntax',
    'callcc': '`call-with-current-continuation`',
    'singlequote': "'", 'doublequote': '"', 'backquote': '`',
    'backwhack': '\\', 'atsign': '@', 'comma': ',', 'commaatsign': ',@',
    'sharpsign': '#', 'verticalbar': '|',
    'ldots': '…', 'dots': '…', 'dotsfoo': '…',
    'evalsto': '⇒', 'coerce': '->', 'lambdaexp': '`lambda` expression',
    'Lambdaexp': '`Lambda` expression',
    'TeX': 'TeX', 'LaTeX': 'LaTeX', 'elem': '∈',
}

# 0-arg commands that produce nothing (spacing / layout primitives)
ZERO_DROP = {
    'vest', 'noindent', 'unpenalty', 'nopagebreak', 'medskip', 'bigskip',
    'smallskip', 'vfill', 'eject', 'clearpage', 'quad', 'qquad', 'hfil',
    'hfill', 'break', 'relax', 'frenchspacing', 'leavevmode', 'nobreak',
    'protect', 'today', 'unsection', 'newpage', 'par', 'smallish', 'small',
    'footnotesize', 'normalsize', 'large', 'Large', 'huge', 'Huge', 'bf',
    'it', 'em', 'rm', 'tt', 'sc', 'sl', 'cf', 'scshape', 'itshape',
    'centering', 'phantomsection', 'goodbreak', 'penalty', 'addvspace',
}

ONE_DROP = {'todo', 'index', 'schindex',
            'sharpindex', 'sharpbangindex', 'label2', 'markboth', 'vskip',
            'hskip', 'hspace', 'vspace', 'raisebox', 'phantom', 'todonote'}

FONT_ONE = {  # \cmd{arg} -> wrapped
    'texttt': ('`', '`'), 'ide': ('`', '`'), 'code': ('`', '`'),
    'emph': ('*', '*'), 'textit': ('*', '*'), 'textsl': ('*', '*'),
    'textbf': ('**', '**'), 'defining': ('**', '**'),
    'textrm': ('', ''), 'mbox': ('', ''), 'text': ('', ''),
    'uppercase': ('', ''), 'centerline': ('', ''),
}


def _subs(key):
    return SUB.get(key, '')


def render_family(name, arg, plain=False):
    """Render a var/vr/hyper/meta family command."""
    arg = arg.strip()
    if name in VAR_FAMILY:
        s = _subs(VAR_FAMILY[name])
        return '%s%s' % (arg, s) if plain else '*%s*%s' % (arg, s)
    if name in HYP_FAMILY:
        s = _subs(HYP_FAMILY[name])
        return '⟨%s⟩%s' % (arg, s)
    return arg


def convert_inline2(s, ctx, plain=False):
    """Convert a run of LaTeX text to Markdown (or plain text if plain=True)."""
    out = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            m = re.match(r'\\([A-Za-z]+)\*?', s[i:])
            if m:
                name = m.group(1)
                j = i + m.end()
                txt, j = _cmd(name, s, j, ctx, plain)
                out.append(txt)
                i = j
                continue
            nxt = s[i + 1] if i + 1 < n else ''
            if nxt in '"\'`^~' and i + 2 <= n:
                mm = re.match(r'([\"\'`^~])\{?([A-Za-z])\}?', s[i + 1:])
                if mm and (mm.group(1) + mm.group(2)) in ACCENTS:
                    out.append(ACCENTS[mm.group(1) + mm.group(2)])
                    i += 1 + mm.end()
                    continue
            if nxt in 'cv.' and i + 2 < n:
                mm = re.match(r'([cv.])\s*\{?([A-Za-z])\}?', s[i + 1:])
                if mm and (mm.group(1) + mm.group(2)) in ACCENTS:
                    out.append(ACCENTS[mm.group(1) + mm.group(2)])
                    i += 1 + mm.end()
                    continue
            out.append(ESCAPES.get(nxt, nxt))
            i += 2
            continue
        if c == '{':
            j = match_brace(s, i)
            out.append(_convert_group(s[i + 1:j], ctx, plain))
            i = j + 1
            continue
        if c == '}':
            i += 1
            continue
        if c == '$':
            # find the closing $ at brace depth 0 (skip nested \hbox{$..$})
            j = i + 1
            depth = 0
            while j < n:
                if s[j] == '\\':
                    j += 2
                    continue
                if s[j] == '{':
                    depth += 1
                elif s[j] == '}':
                    depth -= 1
                elif s[j] == '$' and depth == 0:
                    break
                j += 1
            out.append(_convert_math(s[i + 1:j]))
            i = j + 1
            continue
        if c == '~':
            out.append(' ')
            i += 1
            continue
        out.append(c)
        i += 1
    text = ''.join(out)
    if not plain:
        text = _text_punct(text)
    return text


def _cmd(name, s, j, ctx, plain):
    """Handle a \\command starting after its name at index j. Return (text, next)."""
    # families
    if name in VAR_FAMILY or name in HYP_FAMILY:
        arg, j = read_arg(s, j)
        return render_family(name, convert_inline2(arg, ctx, True), plain), j
    if name in ('proto', 'pproto', 'vproto', 'rproto'):
        return render_proto_inline(name, s, j, ctx)
    if name in FONT_ONE:
        arg, j = read_arg(s, j)
        pre, post = FONT_ONE[name]
        inner = convert_inline2(arg, ctx, plain or pre == '`')
        if pre == '`':
            inner = inner.replace('`', '')  # cannot nest code
        return pre + inner + post, j
    if name == 'sharpfoo':
        arg, j = read_arg(s, j)
        return '`#%s`' % convert_inline2(arg, ctx, True), j
    if name in ('ref', 'pageref'):
        arg, j = read_arg(s, j)
        return render_ref(arg.strip(), ctx), j
    if name == 'cite':
        arg, j = read_arg(s, j)
        return render_cite(arg.strip(), ctx), j
    if name in ('label', 'mainschindex', 'mainindex'):
        arg, j = read_arg(s, j)
        return render_label_anchor(arg.strip(), ctx), j
    if name == 'verb':
        if j < len(s):
            delim = s[j]
            k = s.find(delim, j + 1)
            if k == -1:
                k = len(s)
            return '`%s`' % s[j + 1:k], k + 1
        return '', j
    if name == 'url':
        arg, j = read_arg(s, j)
        return '<%s>' % arg.strip(), j
    if name == 'href':
        a1, j = read_arg(s, j)
        a2, j = read_arg(s, j)
        return '[%s](%s)' % (convert_inline2(a2, ctx, plain), a1.strip()), j
    if name == 'footnote':
        arg, j = read_arg(s, j)
        return ' (%s)' % convert_inline2(arg, ctx, plain), j
    if name == 'rnrs':
        arg, j = read_arg(s, j)
        return 'R%sRS' % SUP.get(arg.strip(), '^' + arg.strip()), j
    if name in ('hbox', 'mbox', 'text', 'ensuremath', 'mathrm'):
        arg, j = read_arg(s, j)
        return convert_inline2(arg, ctx, plain), j
    if name in ('i',):
        return 'ı', j  # dotless i
    if name in ('j',):
        return 'ȷ', j
    if name in ONE_DROP:
        _, j = read_arg(s, j)
        return '', j
    if name in ZERO_CMD:
        return ZERO_CMD[name], j
    if name in ZERO_DROP:
        return '', j
    # unknown command: drop the control word, keep following text
    return '', j


# route the two inline entry points to the folded implementation
convert_inline = convert_inline2


def _convert_group(inner, ctx, plain):
    """Convert a {...} group, honoring a leading font switch."""
    stripped = inner.lstrip()
    for cmd, (pre, post) in (('\\cf', ('`', '`')), ('\\tt', ('`', '`')),
                             ('\\ide', ('`', '`')),
                             ('\\em', ('*', '*')), ('\\it', ('*', '*')),
                             ('\\sl', ('*', '*')), ('\\itshape', ('*', '*')),
                             ('\\bf', ('**', '**')),
                             ('\\scshape', ('', '')), ('\\sc', ('', '')),
                             ('\\rm', ('', '')), ('\\small', ('', '')),
                             ('\\footnotesize', ('', '')),
                             ('\\large', ('', '')), ('\\Large', ('', '')),
                             ('\\huge', ('', '')), ('\\Huge', ('', '')),
                             ('\\normalsize', ('', ''))):
        if re.match(re.escape(cmd) + r'(?![A-Za-z])', stripped):
            rest = stripped[len(cmd):]
            code = pre == '`'
            inner_md = convert_inline2(rest, ctx, plain or code)
            if code:
                inner_md = inner_md.replace('`', '').strip()
                return '`%s`' % inner_md if inner_md else ''
            return pre + inner_md.strip() + post
    return convert_inline2(inner, ctx, plain)


_FAMILY_KEYS = sorted(list(VAR_FAMILY) + list(HYP_FAMILY), key=len, reverse=True)


def family_subs(text, mode):
    """Replace var/vr/hyper/meta family commands. mode: 'code' or 'math'."""
    for name in _FAMILY_KEYS:
        pat = re.compile(r'\\' + name + r'\{([^{}]*)\}')
        while True:
            m = pat.search(text)
            if not m:
                break
            arg = m.group(1)
            if name in VAR_FAMILY:
                key = VAR_FAMILY[name]
                if mode == 'math':
                    # wrap in braces so a preceding control word (e.g. \lfloor)
                    # cannot fuse with the leading letter of the replacement
                    rep = '{%s%s}' % (arg, '_{%s}' % key if key else '')
                else:
                    rep = arg + SUB.get(key, '')
            else:
                key = HYP_FAMILY[name]
                if mode == 'math':
                    rep = '{\\langle %s \\rangle%s}' % (
                        arg, '_{%s}' % key if key else '')
                else:
                    rep = '⟨%s⟩%s' % (arg, SUB.get(key, ''))
            text = text[:m.start()] + rep + text[m.end():]
    return text


def _math_star(m, cmd, star):
    """Replace \\cmd{X} with {X}^{star}, brace-matched (handles nesting)."""
    out = []
    i = 0
    while i < len(m):
        if m.startswith(cmd, i) and not (i + len(cmd) < len(m) and
                                         m[i + len(cmd)].isalpha()):
            j = i + len(cmd)
            while j < len(m) and m[j] in ' \t':
                j += 1
            if j < len(m) and m[j] == '{':
                k = match_brace(m, j)
                out.append('{' + m[j + 1:k] + '}^{' + star + '}')
                i = k + 1
                continue
        out.append(m[i])
        i += 1
    return ''.join(out)


_MATH_FONT = {'rm': '\\mathrm', 'it': '\\mathit', 'tt': '\\mathtt',
              'cal': '\\mathcal', 'bf': '\\mathbf', 'sl': '\\mathit',
              'sf': '\\mathsf', 'sc': '\\mathrm'}


def _math_fonts(m):
    """Brace-matched conversion of \\hbox/\\mbox and {\\rm ..} font groups."""
    guard = 0
    while guard < 40:
        guard += 1
        a = re.search(r'\\(?:hbox|mbox|makebox)\s*(?:\[[^\]]*\])*\s*\{', m)
        b = re.search(r'\{\s*\\(rm|it|tt|cal|bf|sl|sf|sc)\b', m)
        cands = []
        if a:
            cands.append((a.start(), 'A', a))
        if b:
            cands.append((b.start(), 'B', b))
        if not cands:
            break
        cands.sort(key=lambda x: x[0])
        _, kind, mo = cands[0]
        bpos = m.index('{', mo.start())
        close = match_brace(m, bpos)
        inner = m[bpos + 1:close]
        if kind == 'A':
            # \hbox{$..$} -> inner already math; \hbox{\rm X} -> \mathrm{X}
            im = re.match(r'\s*\$(.*)\$\s*$', inner, re.DOTALL)
            fm = re.match(r'\s*\\(rm|it|tt|cal|bf|sl|sf|sc)\b\s*(.*)$',
                          inner, re.DOTALL)
            if im:
                rep = im.group(1)
            elif fm:
                rep = _MATH_FONT[fm.group(1)] + '{' + fm.group(2) + '}'
            else:
                rep = '\\text{' + inner + '}'
            m = m[:mo.start()] + rep + m[close + 1:]
        else:
            fm = re.match(r'\s*\\(rm|it|tt|cal|bf|sl|sf|sc)\b\s*(.*)$',
                          inner, re.DOTALL)
            if fm:
                rep = _MATH_FONT[fm.group(1)] + '{' + fm.group(2).strip() + '}'
            else:
                rep = '{' + inner + '}'
            m = m[:mo.start()] + rep + m[close + 1:]
    return m


def _fix_text_spans(m):
    """Make the interior of every \\text{...} span text-mode-safe.

    MathJax rejects math-mode constructs (\\mathrm, ^, _, greek, \\langle)
    inside \\text{}. The report's formal semantics embeds object-language code
    with metavariables that way, so rewrite each \\text{} interior to text-mode
    equivalents (\\mathrm->\\textrm, drop sub/superscript operators, etc.).
    """
    out = []
    i = 0
    while i < len(m):
        if m.startswith('\\text{', i):
            j = i + len('\\text')          # index of '{'
            close = match_brace(m, j)
            out.append('\\text{' + _textmode(m[j + 1:close]) + '}')
            i = close + 1
        else:
            out.append(m[i])
            i += 1
    return ''.join(out)


def _textmode(s):
    s = (s.replace('\\mathrm', '\\textrm').replace('\\mathtt', '\\texttt')
          .replace('\\mathit', '\\textit').replace('\\mathbf', '\\textbf')
          .replace('\\mathsf', '\\textsf'))
    s = re.sub(r'\\mathcal\{([^{}]*)\}', r'\1', s)
    # drop bold inside text spans: bold-typewriter has no font metrics and the
    # weight only marked emphasis in the typeset original
    s = re.sub(r'\\textbf\{([^{}]*)\}', r'\1', s)
    for name, ch in _GREEK.items():
        s = re.sub(r'\\' + name + r'(?![A-Za-z])', ch, s)
    s = s.replace('\\langle', '⟨').replace('\\rangle', '⟩')
    s = s.replace('\\dots', '…').replace('\\ldots', '…')
    s = re.sub(r'\\[;,:!]', ' ', s)
    # sub/superscript operators are illegal in text mode; keep the operand
    s = re.sub(r'(?<!\\)[\^_]', '', s)
    return s


def normalize_math(m):
    """Best-effort conversion of the report's TeX-in-math to MathJax-safe TeX."""
    m = family_subs(m, 'math')
    m = m.replace('[\\![', '⟦').replace(']\\!]', '⟧')
    m = m.replace('\\sembrack', '')
    m = re.sub(r'\\ide\{([^{}]*)\}', r'\\texttt{\1}', m)   # \ide{x} -> code
    m = m.replace('\\langle', '⟨').replace('\\rangle', '⟩')
    m = re.sub(r'(\\[A-Za-z]+)\{\}', r'\1 ', m)   # \tt{}L -> \tt L (keep sep)
    m = m.replace('{}', '')                        # any remaining empty groups
    # apply the *-repetition before font conversion so that \arbno{...}'s
    # braces are not consumed by an inner {\cal ..} font group
    m = _math_star(m, '\\arbno', '*')
    m = _math_star(m, '\\atleastone', '+')
    m = _math_fonts(m)
    m = re.sub(r'\\cal\s+([A-Za-z])', r'\\mathcal{\1}', m)
    m = re.sub(r'\\(?:cf|tt|rm|it|em|sf|bf|sl|sc)(?![A-Za-z])', '', m)
    m = m.replace('\\elem', '\\in').replace('\\elt', '\\downarrow')
    m = re.sub(r'\\S(?![A-Za-z])', '§', m)   # sequence-concatenation operator
    m = m.replace('\\backwhack', '\\backslash')
    m = m.replace('\\:', '\\;')
    m = re.sub(r'\\hfill|\\hfil|\\wd0|\\kill|\\frenchspacing', '', m)
    m = re.sub(r'\\hspace\*?\{[^}]*\}|\\hskip[^ ]*', '', m)
    m = m.replace('``', '\\text{“}').replace("''", '\\text{”}')
    m = m.replace('\\cf ', '').replace('\\tt ', '')
    m = m.replace('$', '')  # drop any stray nested math delimiters
    m = _fix_text_spans(m)  # make \text{} interiors text-mode-safe (last)
    return m


def _convert_math(m):
    """Convert inline math $...$ to GitHub inline math, best-effort."""
    m = ' '.join(m.split())  # collapse newlines/space (inline math is one line)
    if not m:
        return ''
    m = m.replace('\\ldots', '\\dots')
    m = normalize_math(m)
    return '$%s$' % m


def _text_punct(t):
    """Typographic punctuation for non-code prose."""
    t = t.replace('``', '“').replace("''", '”')
    t = t.replace('---', '—').replace('--', '–')
    return t


# --------------------------------------------------------------------------
# Cross-references
# --------------------------------------------------------------------------

def render_ref(key, ctx):
    info = ctx['labels'].get(key)
    if not info:
        ctx['unresolved'].add(key)
        return '*%s*' % key.replace('-', ' ')
    anchor, outfile, title = info
    title = title or key
    href = ('#' + anchor) if (ctx['mode'] == 'combined' or outfile == ctx['outfile']) \
        else ('%s.md#%s' % (outfile, anchor))
    return '[%s](%s)' % (title, href)


def render_cite(key, ctx):
    keys = [k.strip() for k in key.split(',')]
    parts = []
    for k in keys:
        anchor = 'cite-' + slugify_raw(k)
        href = ('#' + anchor) if (ctx['mode'] == 'combined' or
                                   ctx['citefile'] == ctx['outfile']) \
            else ('%s.md#%s' % (ctx['citefile'], anchor))
        parts.append('[%s](%s)' % (k, href))
    return '[' + ', '.join(parts) + ']'


def render_label_anchor(key, ctx):
    info = ctx['labels'].get(key)
    if not info:
        return ''
    anchor = info[0]
    if anchor in ctx['emitted_anchors']:
        return ''
    ctx['emitted_anchors'].add(anchor)
    return '<a id="%s"></a>' % anchor


# --------------------------------------------------------------------------
# Procedure prototypes
# --------------------------------------------------------------------------

def template_text(tex, ctx):
    """Render a proto template to plain code text (no markdown formatting)."""
    return convert_inline2(tex, ctx, True).replace('`', '').strip()


def _read_proto_args(name, s, j):
    if name in ('proto', 'rproto'):
        a1, j = read_arg(s, j)
        a2, j = read_arg(s, j)
        a3, j = read_arg(s, j)
        return (a1, a2, a3), j
    else:  # pproto, vproto : two args (template/name, category)
        a1, j = read_arg(s, j)
        a2, j = read_arg(s, j)
        return (a1, a2), j


def proto_signature_and_name(name, args, ctx):
    if name in ('proto', 'rproto'):
        nm, argt, cat = args
        sig = '(' + template_text(nm, ctx)
        at = template_text(argt, ctx)
        if at:
            sig += ' ' + at if not at.startswith(' ') else at
        sig += ')'
        return sig, template_text(nm, ctx), cat
    elif name == 'vproto':
        nm, cat = args
        return template_text(nm, ctx), template_text(nm, ctx), cat
    else:  # pproto
        tmpl, cat = args
        return template_text(tmpl, ctx), None, cat


def render_proto_inline(name, s, j, ctx):
    args, j = _read_proto_args(name, s, j)
    sig, _nm, cat = proto_signature_and_name(name, args, ctx)
    cat_md = convert_inline2(cat, ctx, False).strip()
    return '**`%s`** — %s' % (sig, cat_md), j


# --------------------------------------------------------------------------
# Block-level conversion
# --------------------------------------------------------------------------

SECTION_LEVEL = {'chapter': 1, 'clearextrapart': 1, 'extrapart': 1,
                 'clearchapterstar': 1, 'section': 2, 'subsection': 3,
                 'subsubsection': 4, 'paragraph': 5}


def find_env_end(lines, start, env):
    """Index of the \\end{env} line matching the \\begin{env} at 'start'."""
    depth = 0
    begin = re.compile(r'\\begin\{%s\}' % re.escape(env))
    end = re.compile(r'\\end\{%s\}' % re.escape(env))
    for i in range(start, len(lines)):
        depth += len(begin.findall(lines[i]))
        depth -= len(end.findall(lines[i]))
        if depth == 0:
            return i
    return len(lines) - 1


def convert_blocks(lines, ctx):
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank line
        if stripped == '':
            out.append('')
            i += 1
            continue

        # sectioning commands
        m = re.match(r'\\(chapter|clearextrapart|extrapart|clearchapterstar|'
                     r'section|subsection|subsubsection|paragraph)\*?\s*\{',
                     stripped)
        if m:
            cmd = m.group(1)
            brace = line.find('{', m.start(1))
            title_tex = _read_braced_across(lines, i, brace)
            title, end_i = title_tex
            level = SECTION_LEVEL[cmd]
            if level >= 3 and ctx['promote']:
                level -= 1
            title_md = convert_inline2(title, ctx, False).strip()
            out.append('')
            out.append('#' * level + ' ' + title_md)
            out.append('')
            i = end_i + 1
            continue

        # environments
        m = re.match(r'\\begin\{([a-zA-Z*]+)\}', stripped)
        if m:
            env = m.group(1)
            end_i = find_env_end(lines, i, env)
            handler = ENV_HANDLERS.get(env)
            inner = lines[i + 1:end_i]
            # trim first-line remainder after \begin{env}{...}
            first_rem = stripped[m.end():]
            block = handle_environment(env, handler, first_rem, inner, lines,
                                       i, end_i, ctx)
            out.extend(block)
            i = end_i + 1
            continue

        if stripped.startswith('\\appendix') or stripped.startswith('\\input') \
                or stripped.startswith('\\bgroup') or stripped.startswith('\\egroup') \
                or stripped == '}]' or stripped.startswith('\\thispagestyle') \
                or stripped.startswith('\\topnewpage') or stripped.startswith('\\renewcommand') \
                or stripped.startswith('\\newcommand') or stripped.startswith('\\def') \
                or stripped.startswith('\\tableofcontents') or stripped.startswith('\\pagestyle'):
            i += 1
            continue

        # display math $$ ... $$
        if stripped.startswith('$$'):
            block, i = _collect_display_math(lines, i, ctx)
            out.extend(block)
            continue

        # a paragraph of text: gather until blank line or a block starter
        para = []
        while i < n:
            l = lines[i]
            ls = l.strip()
            if ls == '' or re.match(r'\\(begin|chapter|section|subsection|'
                                    r'subsubsection|clearextrapart|extrapart|'
                                    r'clearchapterstar|item)\b', ls) or ls.startswith('$$'):
                break
            para.append(l)
            i += 1
        text = '\n'.join(para)
        md = convert_inline2(text, ctx, False)
        md = _cleanup_paragraph(md)
        if md.strip():
            out.append(md.strip())
            out.append('')
    return out


def _read_braced_across(lines, i, brace_col):
    """Read a brace group that may span lines, starting at lines[i][brace_col]."""
    buf = lines[i][brace_col:]
    k = i
    while True:
        # count balance
        depth = 0
        pos = None
        j = 0
        while j < len(buf):
            ch = buf[j]
            if ch == '\\':
                j += 2
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    pos = j
                    break
            j += 1
        if pos is not None:
            return buf[1:pos], k
        k += 1
        if k >= len(lines):
            return buf[1:], k
        buf += '\n' + lines[k]


def _cleanup_paragraph(md):
    md = re.sub(r'[ \t]+\n', '\n', md)
    md = re.sub(r'\n{2,}', '\n\n', md)
    md = re.sub(r'[ \t]{2,}', ' ', md)
    return md.strip()


def _collect_display_math(lines, i, ctx):
    # Collect from the opening $$ to the matching closing $$ (may be same line).
    parts = []
    buf = lines[i][lines[i].find('$$') + 2:]
    while True:
        c = buf.find('$$')
        if c != -1:
            parts.append(buf[:c])
            i += 1
            break
        parts.append(buf)
        i += 1
        if i >= len(lines):
            break
        buf = lines[i]
    body = '\n'.join(parts).strip()
    body = body.replace('\\ldots', '\\dots')
    body = normalize_math(body)
    return ['', '$$', body, '$$', ''], i


# ---- environment dispatch ----

def handle_environment(env, handler, first_rem, inner, lines, i, end_i, ctx):
    if handler:
        return handler(first_rem, inner, ctx)
    # default: convert inner as blocks
    return convert_blocks(inner, ctx)


def env_scheme(first_rem, inner, ctx):
    body = [first_rem] + inner if first_rem.strip() else list(inner)
    code = [convert_scheme_line(l) for l in body]
    # drop leading/trailing blank
    while code and code[0].strip() == '':
        code.pop(0)
    while code and code[-1].strip() == '':
        code.pop()
    return ['', '```scheme'] + code + ['```', '']


def convert_scheme_line(l):
    l = re.sub(r'\\verb(.)(.*?)\1', r'\2', l)          # \verb"X" -> X
    l = l.replace('\\$', '$').replace('\\%', '%').replace('\\_', '_')
    l = l.replace('\\&', '&').replace('\\ ', ' ')
    # strip font-selection groups: {\cf name} {\tt name} etc. -> name
    for _ in range(6):
        new = re.sub(r'\{\\(?:cf|tt|it|rm|em|bf|sf)\s*([^{}]*)\}', r'\1', l)
        if new == l:
            break
        l = new
    l = re.sub(r'\\ide\{([^{}]*)\}', r'\1', l)
    l = family_subs(l, 'code')
    l = l.replace('\\sharpsign', '#').replace('\\singlequote', "'")
    l = l.replace('\\backquote', '`').replace('\\commaatsign', ',@')
    l = l.replace('\\comma', ',').replace('\\backwhack', '\\')
    l = re.sub(r'\\sharpfoo\{([^}]*)\}', r'#\1', l)
    l = l.replace('\\ev', '  =>').replace('\\lev', '=>')
    l = l.replace('\\evalsto', '=>')
    l = l.replace('\\schtrue', '#t').replace('\\schfalse', '#f')
    l = l.replace('\\sharptrue', '#true').replace('\\sharpfalse', '#false')
    l = l.replace('\\unspecified', 'unspecified')
    l = l.replace('\\scherror', 'error')
    l = l.replace('\\dotsfoo', '...').replace('\\ldots', '...').replace('\\dots', '...')
    l = l.replace('\\#', '#').replace('\\%', '%').replace('\\{', '{')
    l = l.replace('\\}', '}').replace('\\ ', ' ').replace('\\_', '_')
    l = l.replace('\\>', '').replace('\\=', '').replace('\\+', '').replace('\\-', '')
    l = re.sub(r'\\\\$', '', l)
    l = re.sub(r'%+\s*$', '', l)  # trailing comment/line marker
    l = re.sub(r'\\(?:cf|tt|rm|it|em|bf|sf)(?![A-Za-z])', '', l)  # bare fonts
    l = l.replace('{', '').replace('}', '')
    l = l.rstrip()
    return l


def env_grammar(first_rem, inner, ctx):
    body = [first_rem] + inner if first_rem.strip() else list(inner)
    out = []
    for l in body:
        out.append(convert_grammar_line(l, ctx))
    while out and out[0].strip() == '':
        out.pop(0)
    while out and out[-1].strip() == '':
        out.pop()
    return ['', '```bnf'] + out + ['```', '']


_GREEK = {'Gamma': 'Γ', 'gamma': 'γ', 'Delta': 'Δ', 'delta': 'δ',
          'lambda': 'λ', 'rho': 'ρ', 'sigma': 'σ', 'theta': 'θ',
          'kappa': 'κ', 'epsilon': 'ε', 'omega': 'ω', 'phi': 'φ',
          'nu': 'ν', 'alpha': 'α', 'beta': 'β', 'pi': 'π'}


def convert_grammar_line(l, ctx):
    # remove index/label noise
    l = re.sub(r'\\index\{[^}]*\}', '', l)
    l = re.sub(r'\\label\{[^}]*\}', '', l)
    # abstract-syntax grammars (sem.tex) use TeX boxes and math bits
    l = re.sub(r'\\hbox\s+to\s+\d+\\wd\d', '', l)
    l = re.sub(r'\\(?:hbox|copy\d+|hfill|kern|wd\d)\b\s*', '', l)
    l = re.sub(r'\$_(\w)\$', lambda m: SUB.get(m.group(1), '_' + m.group(1)), l)
    l = re.sub(r'\$\\(' + '|'.join(_GREEK) + r')\$',
               lambda m: _GREEK[m.group(1)], l)
    l = l.replace('\\:', ' ⟶ ')          # production arrow
    l = l.replace('\\goesto', '⟶')
    l = l.replace('\\|', ' | ')
    l = re.sub(r'\\arbno\{', '\x01', l)         # placeholder open
    l = re.sub(r'\\atleastone\{', '\x02', l)
    l = _grammar_meta(l, ctx)
    # resolve placeholders: match to closing brace, append * / +
    l = _apply_star(l, '\x01', '*')
    l = _apply_star(l, '\x02', '⁺')
    l = l.replace('\\sharpsign', '#').replace('\\singlequote', "'")
    l = l.replace('\\backquote', '`').replace('\\commaatsign', ',@')
    l = l.replace('\\comma', ',').replace('\\backwhack', '\\')
    l = l.replace('\\verticalbar', '|').replace('\\atsign', '@')
    l = re.sub(r'\\sharpfoo\{([^}]*)\}', r'#\1', l)
    l = l.replace('$\\langle$', '⟨').replace('$\\rangle$', '⟩')
    l = l.replace('\\langle', '⟨').replace('\\rangle', '⟩')
    l = l.replace('\\rm', '').replace('\\bf', '').replace('\\tt', '')
    l = l.replace('\\>', '    ').replace('\\=', '').replace('\\kill', '')
    l = l.replace('\\ ', ' ')
    l = re.sub(r'\\\\\s*$', '', l)
    l = re.sub(r'%+\s*$', '', l)
    l = l.replace('{', '').replace('}', '')
    l = l.replace('\\#', '#')
    return l.rstrip()


def _grammar_meta(l, ctx):
    # brace-matched \meta / \hyper... handling copes with nested {\cf ..} args
    for name in ('meta', 'hyper'):
        marker = '\x03'
        l = re.sub(r'\\' + name + r'(?![A-Za-z])', marker, l)
        while marker in l:
            idx = l.index(marker)
            after = l[idx + 1:].lstrip()
            if not after.startswith('{'):
                l = l[:idx] + l[idx + 1:]
                continue
            close = match_brace(after, 0)
            inner = after[1:close]
            inner = re.sub(r'\{\\(?:cf|tt|it|rm|em|bf)\s*([^{}]*)\}', r'\1', inner)
            rest = after[close + 1:]
            l = l[:idx] + '⟨' + inner + '⟩' + rest
    l = family_subs(l, 'code')
    return l


def _apply_star(l, marker, star):
    while marker in l:
        idx = l.index(marker)
        rest = l[idx + 1:]
        # find matching brace close in rest
        depth = 1
        k = 0
        while k < len(rest) and depth:
            if rest[k] == '{':
                depth += 1
            elif rest[k] == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        content = rest[:k]
        after = rest[k + 1:]
        l = l[:idx] + content + star + after
    return l


def env_note(first_rem, inner, ctx, label='Note'):
    body = convert_blocks(inner, ctx)
    text = '\n'.join(body).strip('\n')
    lines_out = list(text.split('\n'))
    if lines_out and lines_out[0].strip():
        lines_out = ['**%s:** ' % label + lines_out[0]] + lines_out[1:]
    else:
        lines_out = ['**%s:**' % label] + lines_out
    quoted = ['> ' + l if l.strip() else '>' for l in lines_out]
    return [''] + quoted + ['']


def env_rationale(first_rem, inner, ctx):
    return env_note(first_rem, inner, ctx, label='Rationale')


def env_itemize(first_rem, inner, ctx):
    return _list_items(inner, ctx, ordered=False)


def env_description(first_rem, inner, ctx):
    out = ['']
    # split into items
    items = _split_items(inner)
    for opt, body in items:
        term = ''
        if opt:
            term = convert_inline2(opt, ctx, False).strip()
        body_md = convert_blocks(body, ctx)
        text = ' '.join(x.strip() for x in body_md if x.strip())
        if not term and not text:
            continue                       # skip empty leading/blank items
        if term and text:
            out.append('- **%s** — %s' % (term, text))
        elif term:
            out.append('- **%s**' % term)
        else:
            out.append('- %s' % text)
    out.append('')
    return out


def _split_items(inner):
    """Split lines into [(optional_bracket_arg, body_lines)] on \\item."""
    items = []
    cur = None
    opt = None
    for l in inner:
        m = re.match(r'\s*\\item\b\s*(\[([^\]]*)\])?(.*)', l)
        if m:
            if cur is not None:
                items.append((opt, cur))
            opt = m.group(2)
            rest = m.group(3)
            cur = [rest]
        else:
            if cur is None:
                cur = []
            cur.append(l)
    if cur is not None:
        items.append((opt, cur))
    return items


def _list_items(inner, ctx, ordered=False):
    out = ['']
    items = _split_items(inner)
    for idx, (opt, body) in enumerate(items, 1):
        # strip an outer { } wrapping the whole item (\item{...})
        body_md = convert_blocks(body, ctx)
        # collapse to compact paragraphs
        chunk = '\n'.join(body_md).strip('\n')
        chunk = re.sub(r'\n{3,}', '\n\n', chunk).strip()
        bullet = ('%d.' % idx) if ordered else '-'
        sub = chunk.split('\n')
        if not sub or not any(x.strip() for x in sub):
            continue
        out.append('%s %s' % (bullet, sub[0].strip()))
        for cont in sub[1:]:
            out.append(('  ' + cont) if cont.strip() else '')
    out.append('')
    return out


def env_entry(first_rem, inner, ctx):
    # Reconstruct full block text to split header arg from body.
    full = first_rem + '\n' + '\n'.join(inner)
    # header is the first brace group
    b = full.find('{')
    if b == -1:
        return convert_blocks(inner, ctx)
    e = match_brace(full, b)
    header = full[b + 1:e]
    body = full[e + 1:]
    out = ['']
    # emit anchor + signatures
    sigs = []
    names = []
    k = 0
    while k < len(header):
        m = re.search(r'\\(proto|pproto|vproto|rproto)', header[k:])
        if not m:
            break
        name = m.group(1)
        j = k + m.end()
        args, j = _read_proto_args(name, header, j)
        sig, nm, cat = proto_signature_and_name(name, args, ctx)
        cat_md = convert_inline2(cat, ctx, False).strip()
        sigs.append((sig, cat_md))
        if nm:
            names.append(nm)
        k = j
    # entries may declare additional names via \mainschindex in the header
    for im in re.finditer(r'\\mainschindex\{([^}]*)\}', header):
        names.append(_plain_name(im.group(1)))
    # emit an anchor for every defined name so the index resolves each one
    for nm in names:
        info = ctx['labels'].get(nm)
        if info and info[0] not in ctx['emitted_anchors']:
            ctx['emitted_anchors'].add(info[0])
            out.append('<a id="%s"></a>' % info[0])
    # signature lines (bold code + category), hard-wrapped
    for idx, (sig, cat_md) in enumerate(sigs):
        suffix = '  ' if idx < len(sigs) - 1 else ''
        out.append('**`%s`** — %s%s' % (sig, cat_md, suffix))
    out.append('')
    out.extend(convert_blocks(body.split('\n'), ctx))
    out.append('')
    return out


def env_tabular(first_rem, inner, ctx):
    # column spec is in first_rem: {ll} etc.
    m = re.match(r'\s*\{[^}]*\}', first_rem)
    rows_src = first_rem[m.end():] if m else first_rem
    text = rows_src + '\n' + '\n'.join(inner)
    # split rows on \\
    text = re.sub(r'\\hline', '', text)
    rows = re.split(r'\\\\', text)
    table = []
    ncol = 0
    for r in rows:
        r = r.strip()
        if r == '':
            continue
        # multicolumn -> single spanning cell (best-effort)
        r = re.sub(r'\\multicolumn\{\d+\}\{[^}]*\}\{', '{', r)
        cells = _split_cells(r)
        cells = [convert_inline2(c, ctx, False).strip() for c in cells]
        table.append(cells)
        ncol = max(ncol, len(cells))
    if not table:
        return ['']
    out = ['']
    header = table[0]
    header = header + [''] * (ncol - len(header))
    out.append('| ' + ' | '.join(header) + ' |')
    out.append('| ' + ' | '.join(['---'] * ncol) + ' |')
    for row in table[1:]:
        row = row + [''] * (ncol - len(row))
        out.append('| ' + ' | '.join(row) + ' |')
    out.append('')
    return out


def _split_cells(r):
    cells = []
    depth = 0
    cur = ''
    i = 0
    while i < len(r):
        c = r[i]
        if c == '\\':
            cur += r[i:i + 2]
            i += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        if c == '&' and depth == 0:
            cells.append(cur)
            cur = ''
            i += 1
            continue
        cur += c
        i += 1
    cells.append(cur)
    return cells


def env_tabbing(first_rem, inner, ctx):
    body = [first_rem] + inner if first_rem.strip() else list(inner)
    out = ['']
    for l in body:
        l = l.replace('\\=', '').replace('\\>', ' ').replace('\\kill', '')
        l = l.replace('\\+', '').replace('\\-', '')
        l = re.sub(r'\\\\\s*$', '', l)
        md = convert_inline2(l, ctx, False).strip()
        if md:
            out.append(md + '  ')
    out.append('')
    return out


def env_semfun(first_rem, inner, ctx):
    body = [first_rem] + inner if first_rem.strip() else list(inner)
    text = '\n'.join(body)
    text = text.strip()
    if text.startswith('$'):
        text = text[1:]
    if text.endswith('$'):
        text = text[:-1]
    # strip tabbing controls
    text = text.replace('\\=', '').replace('\\>', '').replace('\\kill', '')
    text = text.replace('\\+', '').replace('\\-', '')
    lines_m = [normalize_math(x.strip()) for x in re.split(r'\\\\', text) if x.strip()]
    if not lines_m:
        return ['']
    if len(lines_m) == 1:
        return ['', '$$%s$$' % lines_m[0], '']
    body_math = ' \\\\\n'.join(lines_m)
    return ['', '$$', '\\begin{aligned}', body_math, '\\end{aligned}', '$$', '']


def env_center(first_rem, inner, ctx):
    return convert_blocks(inner, ctx)


def env_thebib(first_rem, inner, ctx):
    text = '\n'.join(inner)
    out = ['']
    items = re.split(r'\\bibitem', text)
    for it in items:
        it = it.strip()
        if not it:
            continue
        m = re.match(r'\{([^}]*)\}(.*)', it, re.DOTALL)
        if not m:
            continue
        key = m.group(1).strip()
        body = convert_inline2(m.group(2).strip(), ctx, False)
        body = re.sub(r'\s+', ' ', body).strip()
        anchor = 'cite-' + slugify_raw(key)
        out.append('<a id="%s"></a>' % anchor)
        out.append('**[%s]** %s' % (key, body))
        out.append('')
    return out


ENV_HANDLERS = {
    'scheme': env_scheme,
    'schemenoindent': env_scheme,
    'grammar': env_grammar,
    'note': env_note,
    'rationale': env_rationale,
    'itemize': env_itemize,
    'description': env_description,
    'entry': env_entry,
    'tabular': env_tabular,
    'tabbing': env_tabbing,
    'semfun': env_semfun,
    'center': env_center,
    'thebibliography': env_thebib,
}


# --------------------------------------------------------------------------
# Preprocessing
# --------------------------------------------------------------------------

def strip_comments(text):
    out = []
    for line in text.split('\n'):
        res = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\' and i + 1 < len(line):
                res.append(line[i:i + 2])
                i += 2
                continue
            if c == '%':
                break
            res.append(c)
            i += 1
        out.append(''.join(res))
    return '\n'.join(out)


def strip_latexdiff(text):
    # \DIFadd{...} / \DIFdel{...} and their markers
    text = re.sub(r'\\DIFadd\{', '{', text)
    text = re.sub(r'\\DIFdel\{[^{}]*\}', '', text)
    text = text.replace('\\DIFaddbegin', '').replace('\\DIFaddend', '')
    text = text.replace('\\DIFdelbegin', '').replace('\\DIFdelend', '')
    return text


def remove_definitions(text):
    """Excise \\newcommand / \\renewcommand / \\def / \\newenvironment blocks."""
    out = []
    i = 0
    n = len(text)
    defcmd = re.compile(r'\\(?:re)?newcommand\b|\\providecommand\b|'
                        r'\\(?:re)?newenvironment\b|\\def\b')
    while i < n:
        m = defcmd.match(text, i)
        if not m:
            out.append(text[i])
            i += 1
            continue
        kind = m.group(0)
        j = m.end()
        ngroups = 2 if 'environment' in kind else 1
        if kind == '\\def':
            # \def\name<#1..>{body}
            mm = re.match(r'\s*\\[A-Za-z]+\s*(?:#\d)*\s*', text[j:])
            j += mm.end() if mm else 0
            if j < n and text[j] == '{':
                j = match_brace(text, j) + 1
            i = j
            continue
        # optional {\name} or \name
        while j < n and text[j] in ' \t\n':
            j += 1
        if j < n and text[j] == '{':
            j = match_brace(text, j) + 1
        else:
            mm = re.match(r'\\[A-Za-z]+', text[j:])
            j += mm.end() if mm else 0
        # optional [n] [default]
        while True:
            mm = re.match(r'\s*\[[^\]]*\]', text[j:])
            if not mm:
                break
            j += mm.end()
        for _ in range(ngroups):
            while j < n and text[j] in ' \t\n':
                j += 1
            if j < n and text[j] == '{':
                j = match_brace(text, j) + 1
        i = j
    return ''.join(out)


def preprocess(text):
    text = strip_comments(text)
    text = strip_latexdiff(text)
    # unwrap $$ ... tabular ... $$
    text = re.sub(r'\$\$\s*(\\begin\{tabular\}.*?\\end\{tabular\})\s*\$\$',
                  lambda m: '\n' + m.group(1) + '\n', text, flags=re.DOTALL)
    macros = collect_newcommands(text)
    text = remove_definitions(text)
    text = expand_macros(text, macros)
    return text


# --------------------------------------------------------------------------
# Slug allocation
# --------------------------------------------------------------------------

def slugify_raw(name):
    s = re.sub(r'[^A-Za-z0-9]+', '-', name.strip()).strip('-').lower()
    return s or 'x'


class SlugAllocator:
    def __init__(self):
        self.used = set()

    def alloc(self, name):
        base = slugify_raw(name)
        cand = base
        k = 2
        while cand in self.used:
            cand = '%s-%d' % (base, k)
            k += 1
        self.used.add(cand)
        return cand


# --------------------------------------------------------------------------
# Pass 1: collect labels, proto names, titles
# --------------------------------------------------------------------------

def pass1_scan(spec_dir):
    labels = {}          # key -> (anchor, outfile, title)
    procindex = []       # (name, anchor, outfile)
    alloc = SlugAllocator()
    citefile = GROUPS[-1][0]
    for outbase, files in GROUPS:
        for fname in files:
            path = os.path.join(spec_dir, fname)
            with open(path, encoding='utf-8') as f:
                raw = f.read()
            text = preprocess(raw)
            last_title = None
            for line in text.split('\n'):
                sm = re.match(r'\s*\\(chapter|clearextrapart|extrapart|'
                              r'clearchapterstar|section|subsection|'
                              r'subsubsection)\*?\s*\{(.*)', line)
                if sm:
                    # get title text up to matching brace on this line
                    t = sm.group(2)
                    depth = 1
                    buf = ''
                    for ch in t:
                        if ch == '{':
                            depth += 1
                        elif ch == '}':
                            depth -= 1
                            if depth == 0:
                                break
                        buf += ch
                    last_title = _plain_title(buf)
                for lm in re.finditer(r'\\label\{([^}]*)\}', line):
                    key = lm.group(1)
                    if key not in labels:
                        labels[key] = (alloc.alloc(key), outbase, last_title)
                for pm in re.finditer(r'\\(proto|vproto)\{', line):
                    name = _first_brace_arg(line, pm.end() - 1)
                    nm = _plain_name(name)
                    if nm and nm not in labels:
                        anchor = alloc.alloc(nm)
                        labels[nm] = (anchor, outbase, nm)
                        procindex.append((nm, anchor, outbase))
                # hand-formatted entries use \mainschindex; concept definitions
                # use \mainindex -- both are valid \ref targets.
                for pm in re.finditer(r'\\mainschindex\{([^}]*)\}', line):
                    nm = _plain_name(pm.group(1))
                    if nm and nm not in labels:
                        anchor = alloc.alloc(nm)
                        labels[nm] = (anchor, outbase, nm)
                        procindex.append((nm, anchor, outbase))
                for pm in re.finditer(r'\\mainindex\{([^}]*)\}', line):
                    nm = _plain_name(pm.group(1))
                    if nm and nm not in labels:
                        labels[nm] = (alloc.alloc(nm), outbase, last_title)
    return labels, procindex, citefile


def _first_brace_arg(s, brace_idx):
    j = match_brace(s, brace_idx)
    return s[brace_idx + 1:j]


def _plain_title(tex):
    tex = re.sub(r'\\rnrs\{(\d)\}', lambda m: 'R' + SUP.get(m.group(1), m.group(1)) + 'RS', tex)
    tex = re.sub(r'\\[A-Za-z]+', '', tex)
    tex = tex.replace('{', '').replace('}', '').replace('$', '')
    tex = tex.replace('\\', '')
    return re.sub(r'\s+', ' ', tex).strip()


def _plain_name(tex):
    tex = tex.strip()
    tex = re.sub(r'\\[A-Za-z]+\s*', '', tex)
    tex = tex.replace('{', '').replace('}', '').strip()
    return tex


# --------------------------------------------------------------------------
# Pass 2: convert
# --------------------------------------------------------------------------

def file_has_section(text):
    return re.search(r'\\section\b', text) is not None


def convert_group_file(spec_dir, outbase, files, labels, citefile, mode, outfile_for_ctx):
    parts = []
    for fname in files:
        with open(os.path.join(spec_dir, fname), encoding='utf-8') as f:
            raw = f.read()
        text = preprocess(raw)
        promote = not file_has_section(text)
        ctx = {
            'labels': labels, 'mode': mode, 'outfile': outfile_for_ctx,
            'citefile': citefile, 'promote': promote,
            'emitted_anchors': set(), 'unresolved': set(),
        }
        lines = text.split('\n')
        md = convert_blocks(lines, ctx)
        parts.append('\n'.join(md))
        _UNRESOLVED.update(ctx['unresolved'])
    body = '\n'.join(parts)
    body = re.sub(r'\n{3,}', '\n\n', body).strip() + '\n'
    body = _collapse_math_blanks(body)
    return body


def _collapse_math_blanks(body):
    """Remove blank lines inside $$...$$ display-math blocks.

    GitHub treats a blank line as a paragraph break that terminates a math
    block early, so a multi-line equation with an internal blank line splits
    and its remainder renders as (invalid) text. The equation content is valid;
    only the blank lines must go.
    """
    def repl(m):
        inner = re.sub(r'\n[ \t]*\n+', '\n', m.group(1))
        return '$$' + inner + '$$'
    return re.sub(r'\$\$(.*?)\$\$', repl, body, flags=re.DOTALL)


_UNRESOLVED = set()


# --------------------------------------------------------------------------
# Front matter and TOC
# --------------------------------------------------------------------------

TITLE = 'Revised⁷ Report on the Algorithmic Language Scheme'

CREDITS = """\
**Editors:** Alex Shinn, John Cowan, Arthur A. Gleckler

Steven Ganz, Alexey Radul, Olin Shivers, Aaron W. Hsu, Jeffrey T. Read,
Alaric Snell-Pym, Bradley Lucier, David Rush, Gerald J. Sussman,
Emmanuel Medernach, Benjamin L. Russel

*Richard Kelsey, William Clinger, and Jonathan Rees (Editors, Revised⁵ Report)*

*Michael Sperber, R. Kent Dybvig, Matthew Flatt, and Anton van Straaten
(Editors, Revised⁶ Report)*

*Dedicated to the memory of John McCarthy and Daniel Weinreb*
"""

PROVENANCE = """
---

*This Markdown edition is generated automatically from the LaTeX sources in the
[`r7rs-spec`](../r7rs-spec) submodule by
[`tools/tex2md.py`](../tools/tex2md.py); regenerate it with `make markdown`.
The authoritative typeset version is
[`r7rs.pdf`](../r7rs-spec/spec/r7rs.pdf). Mathematical notation in the formal
semantics uses GitHub's math rendering (`$...$` / `$$...$$`).*
"""


def extract_summary(spec_dir, labels, citefile, mode):
    with open(os.path.join(spec_dir, 'first.tex'), encoding='utf-8') as f:
        raw = f.read()
    text = preprocess(raw)
    m = re.search(r'\\chapter\*\{Summary\}(.*?)\\chapter\*\{Contents\}',
                  text, re.DOTALL)
    if not m:
        return ''
    ctx = {'labels': labels, 'mode': mode, 'outfile': 'README',
           'citefile': citefile, 'promote': True,
           'emitted_anchors': set(), 'unresolved': set()}
    md = convert_blocks(m.group(1).split('\n'), ctx)
    return '\n'.join(md).strip()


def build_toc(chapter_titles, mode):
    lines = ['## Contents', '']
    for outbase, title in chapter_titles:
        href = ('#' + slugify_raw(title)) if mode == 'combined' else (outbase + '.md')
        lines.append('- [%s](%s)' % (title, href))
    return '\n'.join(lines)


def build_proc_index(procindex, mode):
    lines = ['## Alphabetic index of procedures and keywords', '']
    for name, anchor, outbase in sorted(procindex, key=lambda x: x[0].lower()):
        href = ('#' + anchor) if mode == 'combined' else ('%s.md#%s' % (outbase, anchor))
        lines.append('- [`%s`](%s)' % (name, href))
    return '\n'.join(lines)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

TITLE_OVERRIDE = {'bib.tex': 'References'}


def get_chapter_title(spec_dir, files):
    for fname in files:
        with open(os.path.join(spec_dir, fname), encoding='utf-8') as f:
            text = preprocess(f.read())
        m = re.search(r'\\(chapter|clearextrapart|extrapart|clearchapterstar)'
                      r'\*?\s*\{', text)
        if m:
            title = _read_braced_after(text, m.end() - 1)
            return _plain_title(title)
    if files[0] in TITLE_OVERRIDE:
        return TITLE_OVERRIDE[files[0]]
    return files[0].replace('.tex', '').title()


def ensure_h1(body, title):
    """Prepend an H1 if the converted body has no top-level heading of its own."""
    if re.match(r'\s*#\s', body):
        return body
    return '# %s\n\n%s' % (title, body)


def _read_braced_after(s, brace_idx):
    j = match_brace(s, brace_idx)
    return s[brace_idx + 1:j]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', default='r7rs-spec/spec')
    ap.add_argument('--out', default='markdown')
    args = ap.parse_args()

    spec_dir = args.spec
    out_dir = args.out
    os.makedirs(out_dir, exist_ok=True)

    labels, procindex, citefile = pass1_scan(spec_dir)

    chapter_titles = []
    for outbase, files in GROUPS:
        chapter_titles.append((outbase, get_chapter_title(spec_dir, files)))

    # per-chapter files (the H1 comes from the file's own \chapter/\extrapart)
    for (outbase, files), (_, title) in zip(GROUPS, chapter_titles):
        body = convert_group_file(spec_dir, outbase, files, labels, citefile,
                                   mode='multi', outfile_for_ctx=outbase)
        with open(os.path.join(out_dir, outbase + '.md'), 'w', encoding='utf-8') as f:
            f.write(ensure_h1(body, title))

    # README with front matter + TOC
    summary = extract_summary(spec_dir, labels, citefile, 'multi')
    with open(os.path.join(out_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('# %s\n\n' % TITLE)
        f.write(CREDITS + '\n')
        if summary:
            f.write('## Summary\n\n' + summary + '\n\n')
        f.write(build_toc(chapter_titles, 'multi') + '\n\n')
        f.write(build_proc_index(procindex, 'multi') + '\n')
        f.write(PROVENANCE)

    # single combined file
    with open(os.path.join(out_dir, 'r7rs.md'), 'w', encoding='utf-8') as f:
        summary_c = extract_summary(spec_dir, labels, citefile, 'combined')
        f.write('# %s\n\n' % TITLE)
        f.write(CREDITS + '\n')
        if summary_c:
            f.write('## Summary\n\n' + summary_c + '\n\n')
        f.write(build_toc(chapter_titles, 'combined') + '\n\n')
        for (outbase, files), (_, title) in zip(GROUPS, chapter_titles):
            body = convert_group_file(spec_dir, outbase, files, labels,
                                      citefile, mode='combined',
                                      outfile_for_ctx=outbase)
            f.write('\n')
            f.write(ensure_h1(body, title))
            f.write('\n')
        f.write('\n' + build_proc_index(procindex, 'combined') + '\n')

    if _UNRESOLVED:
        sys.stderr.write('Unresolved \\ref targets (%d): %s\n' % (
            len(_UNRESOLVED), ', '.join(sorted(_UNRESOLVED)[:40])))
    print('Wrote %d chapter files + README.md + r7rs.md to %s/' %
          (len(GROUPS), out_dir))


if __name__ == '__main__':
    main()
