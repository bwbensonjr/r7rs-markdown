# Lexical conventions

This section gives an informal account of some of the lexical
conventions used in writing Scheme programs. For a formal syntax of
Scheme, see section [Formal syntax](08-formal-syntax-and-semantics.md#bnf).

## Identifiers

<a id="syntaxsection"></a>

An identifier<a id="identifier"></a> is any sequence of letters, digits, and
“extended identifier characters” provided that it does not have a prefix
which is a valid number.
However, the `.` token (a single period) used in the list syntax
is not an identifier.

All implementations of Scheme must support the following extended identifier
characters:

```scheme
! $ % & * + - . / : < = > ? @ ^ _ ~
```

Alternatively, an identifier can be represented by a sequence of zero or more
characters enclosed within vertical lines (`$|$`), analogous to
string literals. Any character, including whitespace characters, but
excluding the backslash and vertical line characters,
can appear verbatim in such an identifier.
In addition, characters can be
specified using either an ⟨inline hex escape⟩ or
the same escapes
available in strings.

For example, the
identifier `|H\x65;llo|` is the same identifier as
`Hello`, and in an implementation that supports the appropriate
Unicode character the identifier `|\x3BB;|` is the same as the
identifier $\lambda$.
What is more, `|\t\t|` and `|\x9;\x9;|` are the
same.
Note that `||` is a valid identifier that is different from any other
identifier.

Here are some examples of identifiers:

```scheme
...                      +
+soup+                   <=?
->string                 a34kTMNs
lambda                   list->vector
q                        V17a
|two words|              |twox20;words|
the-word-recursion-has-many-meanings
```

See section [Lexical structure](08-formal-syntax-and-semantics.md#extendedalphas) for the formal syntax of identifiers.

Identifiers have two uses within Scheme programs:

- Any identifier can be used as a variable
   or as a syntactic keyword
  (see sections [Variables, syntactic keywords, and regions](04-basic-concepts.md#variablesection) and [Macros](05-expressions.md#macrosection)).
- When an identifier appears as a literal or within a literal
  (see section [quote](05-expressions.md#quote)), it is being used to denote a *symbol*
  (see section [Symbols](07-standard-procedures.md#symbolsection)).

In contrast with earlier revisions of the report [[R5RS](14-references.md#cite-r5rs)], the
syntax distinguishes between upper and lower case in
identifiers and in characters specified using their names. However, it
does not distinguish between upper and lower case in numbers,
nor in ⟨inline hex escapes⟩ used
in the syntax of identifiers, characters, or strings.
None of the identifiers defined in this report contain upper-case
characters, even when they appear to do so as a result
of the English-language convention of capitalizing the first word of
a sentence.

The following directives give explicit control over case
folding.

These directives can appear anywhere comments are permitted (see
section [Whitespace and comments](#wscommentsection)) but must be followed by a delimiter.
They are treated as comments, except that they affect the reading
of subsequent data from the same port. The `#!fold-case` directive causes
subsequent identifiers and character names to be case-folded
as if by `string-foldcase` (see section [Strings](07-standard-procedures.md#stringsection)).
It has no effect on character
literals. The `#!no-fold-case` directive
causes a return to the default, non-folding behavior.

## Whitespace and comments

<a id="wscommentsection"></a>

(Implementations may provide additional whitespace characters such
as page break.) Whitespace is used for improved readability and
as necessary to separate tokens from each other, a token being an
indivisible lexical unit such as an identifier or number, but is
otherwise insignificant. Whitespace can occur between any two tokens,
but not within a token. Whitespace occurring inside a string
or inside a symbol delimited by vertical lines
is significant.

The lexical syntax includes several comment forms.
Comments are treated exactly like whitespace.

A semicolon (`;`) indicates the start of a line
comment.<a id="comment"></a><a id="x"></a> The comment continues to the
end of the line on which the semicolon appears.

Another way to indicate a comment is to prefix a ⟨datum⟩
(cf. section [External representations](08-formal-syntax-and-semantics.md#datumsyntax)) with `#;` and optional
⟨whitespace⟩. The comment consists of
the comment prefix `#;`, the space, and the ⟨datum⟩ together. This
notation is useful for “commenting out” sections of code.

Block comments are indicated with properly nested `#|`
and `|#` pairs.

```scheme
#|
   The FACT procedure computes the factorial
   of a non-negative integer.
|#
(define fact
  (lambda (n)
    (if (= n 0)
        #;(= n 1)
        1        ;Base case: return 1
        (* n (fact (- n 1))))))
```

## Other notations

For a description of the notations used for numbers, see
section [Numbers](07-standard-procedures.md#numbersection).

- **`. + -`** — These are used in numbers, and can also occur anywhere in an identifier.
A delimited plus or minus sign by itself
is also an identifier.
A delimited period (not occurring within a number or identifier) is used
in the notation for pairs (section [Pairs and lists](07-standard-procedures.md#listsection)), and to indicate a
rest-parameter in a formal parameter list (section [lambda](05-expressions.md#lambda)).
Note that a sequence of two or more periods *is* an identifier.
- **( )** — Parentheses are used for grouping and to notate lists
(section [Pairs and lists](07-standard-procedures.md#listsection)).
- **'** — The apostrophe (single quote) character is used to indicate literal data (section [quote](05-expressions.md#quote)).
- **`** — The grave accent (backquote) character is used to indicate partly constant
data (section [quasiquote](05-expressions.md#quasiquote)).
- **, ,@** — The character comma and the sequence comma at-sign are used in conjunction
with quasiquotation (section [quasiquote](05-expressions.md#quasiquote)).
- **"** — The quotation mark character is used to delimit strings (section [Strings](07-standard-procedures.md#stringsection)).
- **\** — Backslash is used in the syntax for character constants
(section [Characters](07-standard-procedures.md#charactersection)) and as an escape character within string
constants (section [Strings](07-standard-procedures.md#stringsection)) and identifiers
(section [Lexical structure](08-formal-syntax-and-semantics.md#extendedalphas)). 0 `[` `]` `{` `}`
- **0** — Left and right square and curly brackets (braces)
are reserved for possible future extensions to the language.
- **#** — The number sign is used for a variety of purposes depending on
the character that immediately follows it:
- **`#t` `#f`** — These are the boolean constants (section [Booleans](07-standard-procedures.md#booleansection)),
along with the alternatives `#true` and `#false`.
- **#\** — This introduces a character constant (section [Characters](07-standard-procedures.md#charactersection)).
- **#(** — This introduces a vector constant (section [Vectors](07-standard-procedures.md#vectorsection)). Vector constants
are terminated by `)` .
- **# u8(** — This introduces a bytevector constant (section [Bytevectors](07-standard-procedures.md#bytevectorsection)). Bytevector constants
are terminated by `)` .
- **`#e #i #b #o #d #x`** — These are used in the notation for numbers (section [Syntax of numerical constants](07-standard-procedures.md#numbernotations)).
- **#⟨n⟩= #⟨n⟩#** — These are used for labeling and referencing other literal data (section [Datum labels](#labelsection)).

## Datum labels

<a id="labelsection"></a>

**`#⟨n⟩=⟨datum⟩`** — lexical syntax  
**`#⟨n⟩#`** — lexical syntax

The lexical syntax
`#⟨n⟩=⟨datum⟩` reads the same as ⟨datum⟩, but also
results in ⟨datum⟩ being labelled by ⟨n⟩.
It is an error if ⟨n⟩ is not a sequence of digits.

The lexical syntax `#⟨n⟩#` serves as a reference to some
object labelled by `#⟨n⟩=`; the result is the same
object as the `#⟨n⟩`=
(see section [Equivalence predicates](07-standard-procedures.md#equivalencesection)).

Together, these syntaxes permit the notation of
structures with shared or circular substructure.

```scheme
(let ((x (list 'a 'b 'c)))
  (set-cdr! (cddr x) x)
  x)                         => #0=(a b c . #0#)
```

The scope of a datum label is the portion of the outermost datum in which it appears
that is to the right of the label.
Consequently, a reference `#⟨n⟩#` can occur only after a label
`#⟨n⟩=`; it is an error to attempt a forward reference. In
addition, it is an error if the reference appears as the labelled object itself
(as in `#⟨n⟩= #⟨n⟩#`),
because the object labelled by `#⟨n⟩=` is not well
defined in this case.

It is an error for a ⟨program⟩ or ⟨library⟩ to include
circular references except in literals. In particular,
it is an error for `quasiquote` (section [quasiquote](05-expressions.md#quasiquote)) to contain them.

```scheme
#1=(begin (display #x) #1#)
                         => error
```
