# Revised⁷ Report on the Algorithmic Language Scheme

**Editors:** Alex Shinn, John Cowan, Arthur A. Gleckler

Steven Ganz, Alexey Radul, Olin Shivers, Aaron W. Hsu, Jeffrey T. Read,
Alaric Snell-Pym, Bradley Lucier, David Rush, Gerald J. Sussman,
Emmanuel Medernach, Benjamin L. Russel

*Richard Kelsey, William Clinger, and Jonathan Rees (Editors, Revised⁵ Report)*

*Michael Sperber, R. Kent Dybvig, Matthew Flatt, and Anton van Straaten
(Editors, Revised⁶ Report)*

*Dedicated to the memory of John McCarthy and Daniel Weinreb*

## Summary

The report gives a defining description of the programming language
Scheme. Scheme is a statically scoped and properly tail recursive
dialect of the Lisp programming language [[McCarthy](#cite-mccarthy)] invented by Guy Lewis
Steele Jr. and Gerald Jay Sussman. It was designed to have
exceptionally clear and simple semantics and few different ways to
form expressions. A wide variety of programming paradigms, including
imperative, functional, and object-oriented styles, find convenient
expression in Scheme.


The introduction offers a brief history of the language and of
the report.


The first three chapters present the fundamental ideas of the
language and describe the notational conventions used for describing the
language and for writing programs in the language.


Chapters [Expressions](#expressionchapter) and [Program structure](#programchapter) describe
the syntax and semantics of expressions, definitions, programs, and libraries.


Chapter [Standard procedures](#builtinchapter) describes Scheme's built-in
procedures, which include all of the language's data manipulation and
input/output primitives.


Chapter [Formal syntax and semantics](#formalchapter) provides a formal syntax for Scheme
written in extended BNF, along with a formal denotational semantics.
An example of the use of the language follows the formal syntax and
semantics.


Appendix [Standard Libraries](#stdlibraries) provides a list of the standard libraries
and the identifiers that they export.


Appendix [Standard Feature Identifiers](#stdfeatures) provides a list of optional but standardized
implementation feature names.



The report concludes with a list of references and an
alphabetic index.



> **Note:** The editors of the R⁵RS and R⁶RS reports are
> listed as authors of this report in recognition of the substantial
> portions of this report that are copied directly from R⁵RS and R⁶RS.
> There is no intended implication that those editors, individually or
> collectively, support or do not support this report.

## Contents

- [Introduction](#introduction)
- [Overview of Scheme](#overview-of-scheme)
- [Lexical conventions](#lexical-conventions)
- [Basic concepts](#basic-concepts)
- [Expressions](#expressions)
- [Program structure](#program-structure)
- [Standard procedures](#standard-procedures)
- [Formal syntax and semantics](#formal-syntax-and-semantics)
- [Standard Libraries](#standard-libraries)
- [Standard Feature Identifiers](#standard-feature-identifiers)
- [Language changes](#language-changes)
- [Additional material](#additional-material)
- [Example](#example)
- [References](#references)


# Introduction

<a id="historysection"></a>

Programming languages should be designed not by piling feature on top of
feature, but by removing the weaknesses and restrictions that make additional
features appear necessary. Scheme demonstrates that a very small number
of rules for forming expressions, with no restrictions on how they are
composed, suffice to form a practical and efficient programming language
that is flexible enough to support most of the major programming
paradigms in use today.

Scheme
was one of the first programming languages to incorporate first-class
procedures as in the lambda calculus, thereby proving the usefulness of
static scope rules and block structure in a dynamically typed language.
Scheme was the first major dialect of Lisp to distinguish procedures
from lambda expressions and symbols, to use a single lexical
environment for all variables, and to evaluate the operator position
of a procedure call in the same way as an operand position. By relying
entirely on procedure calls to express iteration, Scheme emphasized the
fact that tail-recursive procedure calls are essentially GOTOs that
pass arguments, thus allowing a programming style that is both coherent
and efficient. Scheme was the first widely used programming language to
embrace first-class escape procedures, from which all previously known
sequential control structures can be synthesized. A subsequent
version of Scheme introduced the concept of exact and inexact numbers,
an extension of Common Lisp's generic arithmetic.
More recently, Scheme became the first programming language to support
hygienic macros, which permit the syntax of a block-structured language
to be extended in a consistent and reliable manner.

## Background

The first description of Scheme was written in
1975 [[Scheme75](#cite-scheme75)]. A revised report [[Scheme78](#cite-scheme78)]
appeared in 1978, which described the evolution
of the language as its MIT implementation was upgraded to support an
innovative compiler [[Rabbit](#cite-rabbit)]. Three distinct projects began in
1981 and 1982 to use variants of Scheme for courses at MIT, Yale, and
Indiana University [[Rees82](#cite-rees82), [MITScheme](#cite-mitscheme), [Scheme311](#cite-scheme311)]. An introductory
computer science textbook using Scheme was published in
1984 [[SICP](#cite-sicp)].

As Scheme became more widespread,
local dialects began to diverge until students and researchers
occasionally found it difficult to understand code written at other
sites.
Fifteen representatives of the major implementations of Scheme therefore
met in October 1984 to work toward a better and more widely accepted
standard for Scheme.
Their report, the RRRS [[RRRS](#cite-rrrs)],
was published at MIT and Indiana University in the summer of 1985.
Further revision took place in the spring of 1986, resulting in the
R³RS [[R3RS](#cite-r3rs)].
Work in the spring of 1988 resulted in R⁴RS [[R4RS](#cite-r4rs)],
which became the basis for the
IEEE Standard for the Scheme Programming Language in 1991 [[IEEEScheme](#cite-ieeescheme)].
In 1998, several additions to the IEEE standard, including high-level
hygienic macros, multiple return values, and `eval`, were finalized
as the R⁵RS [[R5RS](#cite-r5rs)].

In the fall of 2006, work began on a more ambitious standard,
including many new improvements and stricter requirements made in the
interest of improved portability. The resulting standard, the
R⁶RS, was completed in August 2007 [[R6RS](#cite-r6rs)], and was organized
as a core language and set of mandatory standard libraries.
Several new implementations of Scheme conforming to it were created.
However, most existing R⁵RS implementations (even excluding those
which are essentially unmaintained) did not adopt R⁶RS, or adopted
only selected parts of it.

In consequence, the Scheme Steering Committee decided in August 2009 to divide the
standard into two separate but compatible languages — a “small”
language, suitable for educators, researchers, and users of embedded languages,
focused on R⁵RS compatibility, and a “large” language focused
on the practical needs of mainstream software development,
intended to become a replacement for R⁶RS.
The present report describes the “small” language of that effort:
therefore it cannot be considered in isolation as the successor
to R⁶RS.

We intend this report to belong to the entire Scheme community, and so
we grant permission to copy it in whole or in part without fee. In
particular, we encourage implementers of Scheme to use this report as
a starting point for manuals and other documentation, modifying it as
necessary.

## Acknowledgments

We would like to thank the members of the Steering Committee, William
Clinger, Marc Feeley, Chris Hanson, Jonathan Rees, and Olin Shivers, for
their support and guidance.

This report is very much a community effort, and we'd like to
thank everyone who provided comments and feedback, including
the following people: David Adler, Eli Barzilay, Taylan Ulrich
Bayırlı/Kammer, Marco Benelli, Pierpaolo Bernardi,
Peter Bex, Per Bothner, John Boyle, Taylor Campbell, Raffael Cavallaro,
Ray Dillinger, Biep Durieux, Sztefan Edwards, Helmut Eller, Justin
Ethier, Jay Reynolds Freeman, Tony Garnock-Jones, Alan Manuel Gloria,
Steve Hafner, Sven Hartrumpf, Brian Harvey, Moritz Heidkamp, Jean-Michel
Hufflen, Aubrey Jaffer, Takashi Kato, Shiro Kawai, Richard Kelsey, Oleg
Kiselyov, Pjotr Kourzanov, Jonathan Kraut, Daniel Krueger, Christian
Stigen Larsen, Noah Lavine, Stephen Leach, Larry D. Lee, Kun Liang,
Thomas Lord, Vincent Stewart Manis, Perry Metzger, Michael Montague,
Mikael More, Vitaly Magerya, Vincent Manis, Vassil Nikolov, Joseph
Wayne Norton, Yuki Okumura, Daichi Oohashi, Jeronimo Pellegrini, Jussi
Piitulainen, Alex Queiroz, Jim Rees, Grant Rettke, Andrew Robbins, Devon
Schudy, Bakul Shah, Robert Smith, Arthur Smyles, Michael Sperber, John
David Stone, Jay Sulzberger, Malcolm Tredinnick, Sam Tobin-Hochstadt,
Andre van Tonder, Daniel Villeneuve, Denis Washington, Alan Watson,
Mark H. Weaver, Göran Weinholt, David A. Wheeler, Andy Wingo, James
Wise, Jörg F. Wittenberger, Kevin A. Wortman, Sascha Ziemann.

In addition we would like to thank all the past editors, and the
people who helped them in turn: Hal Abelson, Norman Adams, David
Bartley, Alan Bawden, Michael Blair, Gary Brooks, George Carrette,
Andy Cromarty, Pavel Curtis, Jeff Dalton, Olivier Danvy, Betty Dexter, Ken Dickey,
Bruce Duba, Robert Findler, Andy Freeman, Richard Gabriel, Yekta
Gürsel, Ken Haase, Robert Halstead, Robert Hieb, Paul Hudak, Morry
Katz, Eugene Kohlbecker, Chris Lindblad, Jacob Matthews, Mark Meyer,
Jim Miller, Don Oxley, Jim Philbin, Kent Pitman, John Ramsdell,
Guillermo Rozas, Mike Shaff, Jonathan Shapiro, Guy Steele, Julie
Sussman, Perry Wagle, Mitchel Wand, Daniel Weise, Henry Wu, and Ozan
Yigit. We thank Carol Fessenden, Daniel Friedman, and Christopher
Haynes for permission to use text from the Scheme 311 version 4
reference manual. We thank Texas Instruments, Inc. for permission to
use text from the *TI Scheme Language Reference
Manual* [[TImanual85](#cite-timanual85)]. We gladly acknowledge the influence of
manuals for MIT Scheme [[MITScheme](#cite-mitscheme)], T [[Rees84](#cite-rees84)], Scheme
84 [[Scheme84](#cite-scheme84)], Common Lisp [[CLtL](#cite-cltl)], and Algol 60 [[Naur63](#cite-naur63)],
as well as the following SRFIs: 0, 1, 4, 6, 9, 11, 13, 16, 30, 34, 39, 43, 46, 62, and 87,
all of which are available at `http://srfi.schemers.org`.


# Overview of Scheme

## Semantics

<a id="semanticsection"></a>

This section gives an overview of Scheme's semantics. A
detailed informal semantics is the subject of
chapters [Basic concepts](#basicchapter) through [Standard procedures](#builtinchapter). For reference
purposes, section [Formal semantics](#formalsemanticssection) provides a formal
semantics of Scheme.

Scheme is a statically scoped programming
language. After macros are expanded, each use of a variable is associated
with a lexically apparent binding of that variable.

Scheme is a dynamically typed language. Types
are associated with values (also called objects<a id="object"></a>) rather than
with variables.
Statically typed languages, by contrast, associate types with
variables and expressions as well as with values.

All objects created in the course of a Scheme computation, including
procedures and continuations, have unlimited extent.
No Scheme object is ever destroyed. The reason that
implementations of Scheme do not (usually!) run out of storage is that
they are permitted to reclaim the storage occupied by an object if
they can prove that the object cannot possibly matter to any future
computation.

Implementations of Scheme are required to be properly tail-recursive.
This allows the execution of an iterative computation in constant space,
even if the iterative computation is described by a syntactically
recursive procedure. Thus with a properly tail-recursive implementation,
iteration can be expressed using the ordinary procedure-call
mechanics, so that special iteration constructs are useful only as
syntactic sugar. See section [Proper tail recursion](#proper-tail-recursion).

Scheme procedures are objects in their own right. Procedures can be
created dynamically, stored in data structures, returned as results of
procedures, and so on.

One distinguishing feature of Scheme is that continuations, which
in most other languages only operate behind the scenes, also have
“first-class” status. Continuations are useful for implementing a
wide variety of advanced control constructs, including non-local exits,
backtracking, and coroutines. See section [Control features](#continuations).

Arguments to Scheme procedures are always passed by value, which
means that the actual argument expressions are evaluated before the
procedure gains control, regardless of whether the procedure needs the
result of the evaluation.

Scheme's model of arithmetic is designed to remain as independent as
possible of the particular ways in which numbers are represented within a
computer. In Scheme, every integer is a rational number, every rational is a
real, and every real is a complex number. Thus the distinction between integer
and real arithmetic, so important to many programming languages, does not
appear in Scheme. In its place is a distinction between exact arithmetic,
which corresponds to the mathematical ideal, and inexact arithmetic on
approximations. Exact arithmetic is not limited to integers.

## Syntax

Scheme, like most dialects of Lisp, employs a fully parenthesized prefix
notation for programs and other data; the grammar of Scheme generates a
sublanguage of the language used for data. An important
consequence of this simple, uniform representation is that
Scheme programs and data can easily be treated uniformly by other Scheme programs.
For example, the `eval` procedure evaluates a Scheme program expressed
as data.

The `read` procedure performs syntactic as well as lexical decomposition of
the data it reads. The `read` procedure parses its input as data
(section [External representations](#datumsyntax)), not as program.

The formal syntax of Scheme is described in section [Formal syntax](#bnf).

## Notation and terminology

### Base and optional features

<a id="qualifiers"></a>

Every identifier defined in this report appears in one or more of several
**libraries**. Identifiers defined in the **base library**
are not marked specially in the body of the report.
This library includes the core syntax of Scheme
and generally useful procedures that manipulate data. For example, the
variable `abs` is bound to a
procedure of one argument that computes the absolute value of a
number, and the variable `+` is bound to a procedure that computes
sums. The full list
all the standard libraries and the identifiers they export is given in
Appendix [Standard Libraries](#stdlibraries).

All implementations of Scheme:

- Must provide the base library and all the identifiers
  exported from it.
- May provide or omit the other
  libraries given in this report, but each library must either be provided
  in its entirety, exporting no additional identifiers, or else omitted
  altogether.
- May provide other libraries not described in this report.
- May also extend the function of any identifier in this
  report, provided the extensions are not in conflict with the language
  reported here.
- Must support portable
  code by providing a mode of operation in which the lexical syntax does
  not conflict with the lexical syntax described in this report.

### Error situations and unspecified behavior

<a id="errorsituations"></a>

<a id="error"></a>
When speaking of an error situation, this report uses the phrase “an
error is signaled” to indicate that implementations must detect and
report the error.
An error is signaled by raising a non-continuable exception, as if by
the procedure `raise` as described in section [Exceptions](#exceptionsection). The object raised is implementation-dependent
and need not be distinct from objects previously used for the same purpose.
In addition to errors signaled in situations described in this
report, programmers can signal their own errors and handle signaled errors.

The phrase “an error that satisfies *predicate* is signaled” means that an error is
signaled as above. Furthermore, if the object that is signaled is
passed to the specified predicate (such as `file-error?` or `read-error?`), the predicate returns `#t`.

If such wording does not appear in the discussion of
an error, then implementations are not required to detect or report the
error, though they are encouraged to do so.
Such a situation is sometimes, but not always, referred to with the phrase
“an error.”
In such a situation, an implementation may or may not signal an error;
if it does signal an error, the object that is signaled may or may not
satisfy the predicates `error-object?`, `file-error?`, or
`read-error?`.
Alternatively, implementations may provide non-portable extensions.

For example, it is an error for a procedure to be passed an argument of a type that
the procedure is not explicitly specified to handle, even though such
domain errors are seldom mentioned in this report. Implementations may
signal an error,
extend a procedure's domain of definition to include such arguments,
or fail catastrophically.

This report uses the phrase “may report a violation of an
implementation restriction” to indicate circumstances under which an
implementation is permitted to report that it is unable to continue
execution of a correct program because of some restriction imposed by the
implementation. Implementation restrictions are discouraged,
but implementations are encouraged to report violations of implementation
restrictions.<a id="implementation-restriction"></a>

For example, an implementation may report a violation of an
implementation restriction if it does not have enough storage to run a
program,
or if an arithmetic operation would produce an exact number that is
too large for the implementation to represent.

If the value of an expression is said to be “unspecified,” then
the expression must evaluate to some object without signaling an error,
but the value depends on the implementation; this report explicitly does
not say what value is returned. <a id="unspecified"></a>

Finally, the words and phrases “must,” “must not,” “shall,”
“shall not,” “should,” “should not,” “may,” “required,”
“recommended,” and “optional,” although not capitalized in this
report, are to be interpreted as described in RFC 2119 [[rfc2119](#cite-rfc2119)].
They are used only with reference to implementer or implementation behavior,
not with reference to programmer or program behavior.

### Entry format

Chapters [Expressions](#expressionchapter) and [Standard procedures](#builtinchapter) are organized
into entries. Each entry describes one language feature or a group of
related features, where a feature is either a syntactic construct or a
procedure. An entry begins with one or more header lines of the form

**`template`** — *category*

for identifiers in the base library, or

**`template`** — *name* library *category*

where *name* is the short name of a library
as defined in Appendix [Standard Libraries](#stdlibraries).

If *category* is “syntax,” the entry describes an expression
type, and the template gives the syntax of the expression type.
Components of expressions are designated by syntactic variables, which
are written using angle brackets, for example ⟨expression⟩ and
⟨variable⟩. Syntactic variables are intended to denote segments of
program text; for example, ⟨expression⟩ stands for any string of
characters which is a syntactically valid expression. The notation

⟨thing⟩₁ $\dots$  

indicates zero or more occurrences of a ⟨thing⟩, and

⟨thing⟩₁ ⟨thing⟩₂ $\dots$  

indicates one or more occurrences of a ⟨thing⟩.

If *category* is “auxiliary syntax,” then the entry describes a
syntax binding that occurs only as part of specific surrounding
expressions. Any use as an independent syntactic construct or
variable is an error.

If *category* is “procedure,” then the entry describes a procedure, and
the header line gives a template for a call to the procedure. Argument
names in the template are *italicized*. Thus the header line

**`(vector-ref vector k)`** — procedure

indicates that the procedure bound to the `vector-ref` variable takes
two arguments, a vector *vector* and an exact non-negative integer
*k* (see below). The header lines

**`(make-vector k)`** — procedure
**`(make-vector k fill)`** — procedure

indicate that the `make-vector` procedure must be defined to take
either one or two arguments.

<a id="typeconventions"></a>
It is an error for a procedure to be presented with an argument that it
is not specified to handle. For succinctness, we follow the convention
that if an argument name is also the name of a type listed in
section [Disjointness of types](#disjointness), then it is an error if that argument is not of the named type.
For example, the header line for `vector-ref` given above dictates that the
first argument to `vector-ref` is a vector. The following naming
conventions also imply type restrictions:

| *alist* | association list (list of pairs) |
| --- | --- |
| *boolean* | boolean value (`#t` or `#f`) |
| *byte* | exact integer $0 \leq byte < 256$ |
| *bytevector* | bytevector |
| *char* | character |
| *end* | exact non-negative integer |
| *k*, *k*₁, $\dots$ *k*ⱼ, $\dots$ | exact non-negative integer |
| *letter* | alphabetic character |
| *list*, *list*₁, $\dots$ *list*ⱼ, $\dots$ | list (see section [Pairs and lists](#listsection)) |
| *n*, *n*₁, $\dots$ *n*ⱼ, $\dots$ | integer |
| *obj* | any object |
| *pair* | pair |
| *port* | port |
| *proc* | procedure |
| *q*, *q*₁, $\dots$ *q*ⱼ, $\dots$ | rational number |
| *start* | exact non-negative integer |
| *string* | string |
| *symbol* | symbol |
| *thunk* | zero-argument procedure |
| *vector* | vector |
| *x*, *x*₁, $\dots$ *x*ⱼ, $\dots$ | real number |
| *y*, *y*₁, $\dots$ *y*ⱼ, $\dots$ | real number |
| *z*, *z*₁, $\dots$ *z*ⱼ, $\dots$ | complex number |

The names *start* and *end* are used as indexes into strings,
vectors, and bytevectors. Their use implies the following:

- It is an error if *start* is greater than *end*.
- It is an error if *end* is greater than the length of the
  string, vector, or bytevector.
- If *start* is omitted, it is assumed to be zero.
- If *end* is omitted, it assumed to be the length of the string,
  vector, or bytevector.
- The index *start* is always inclusive and the index *end* is always
  exclusive. As an example, consider a string. If
  *start* and *end* are the same, an empty
  substring is referred to, and if *start* is zero and *end* is
  the length of *string*, then the entire string is referred to.

### Evaluation examples

The symbol “⇒” used in program examples is read
“evaluates to.” For example,

```scheme
(* 5 8)        =>  40
```

means that the expression `(* 5 8)` evaluates to the object `40`.
Or, more precisely: the expression given by the sequence of characters
“`(* 5 8)`” evaluates, in an environment containing the base library, to an object
that can be represented externally by the sequence of characters “`40`.” See section [External representations](#externalreps) for a discussion of external
representations of objects.

### Naming conventions

By convention, `?` is the final character of the names
of procedures that always return a boolean value.
Such procedures are called **predicates**.
Predicates are generally understood to be side-effect free, except that they
may raise an exception when passed the wrong type of argument.

Similarly, `!` is the final character of the names
of procedures that store values into previously
allocated locations (see section [Storage model](#storagemodel)).
Such procedures are called **mutation procedures**.
The value returned by a mutation procedure is unspecified.

By convention, “`->`” appears within the names of procedures that
take an object of one type and return an analogous object of another type.
For example, `list->vector` takes a list and returns a vector whose
elements are the same as those of the list.

A **command** is a procedure that does not return useful values
to its continuation.

A **thunk** is a procedure that does not accept arguments.


# Lexical conventions

This section gives an informal account of some of the lexical
conventions used in writing Scheme programs. For a formal syntax of
Scheme, see section [Formal syntax](#bnf).

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

See section [Lexical structure](#extendedalphas) for the formal syntax of identifiers.

Identifiers have two uses within Scheme programs:

- Any identifier can be used as a variable
   or as a syntactic keyword
  (see sections [Variables, syntactic keywords, and regions](#variablesection) and [Macros](#macrosection)).
- When an identifier appears as a literal or within a literal
  (see section [quote](#quote)), it is being used to denote a *symbol*
  (see section [Symbols](#symbolsection)).

In contrast with earlier revisions of the report [[R5RS](#cite-r5rs)], the
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
as if by `string-foldcase` (see section [Strings](#stringsection)).
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
(cf. section [External representations](#datumsyntax)) with `#;` and optional
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
section [Numbers](#numbersection).

- **`. + -`** — These are used in numbers, and can also occur anywhere in an identifier.
A delimited plus or minus sign by itself
is also an identifier.
A delimited period (not occurring within a number or identifier) is used
in the notation for pairs (section [Pairs and lists](#listsection)), and to indicate a
rest-parameter in a formal parameter list (section [lambda](#lambda)).
Note that a sequence of two or more periods *is* an identifier.
- **( )** — Parentheses are used for grouping and to notate lists
(section [Pairs and lists](#listsection)).
- **'** — The apostrophe (single quote) character is used to indicate literal data (section [quote](#quote)).
- **`** — The grave accent (backquote) character is used to indicate partly constant
data (section [quasiquote](#quasiquote)).
- **, ,@** — The character comma and the sequence comma at-sign are used in conjunction
with quasiquotation (section [quasiquote](#quasiquote)).
- **"** — The quotation mark character is used to delimit strings (section [Strings](#stringsection)).
- **\** — Backslash is used in the syntax for character constants
(section [Characters](#charactersection)) and as an escape character within string
constants (section [Strings](#stringsection)) and identifiers
(section [Lexical structure](#extendedalphas)). 0 `[` `]` `{` `}`
- **0** — Left and right square and curly brackets (braces)
are reserved for possible future extensions to the language.
- **#** — The number sign is used for a variety of purposes depending on
the character that immediately follows it:
- **`#t` `#f`** — These are the boolean constants (section [Booleans](#booleansection)),
along with the alternatives `#true` and `#false`.
- **#\** — This introduces a character constant (section [Characters](#charactersection)).
- **#(** — This introduces a vector constant (section [Vectors](#vectorsection)). Vector constants
are terminated by `)` .
- **# u8(** — This introduces a bytevector constant (section [Bytevectors](#bytevectorsection)). Bytevector constants
are terminated by `)` .
- **`#e #i #b #o #d #x`** — These are used in the notation for numbers (section [Syntax of numerical constants](#numbernotations)).
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
(see section [Equivalence predicates](#equivalencesection)).

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
it is an error for `quasiquote` (section [quasiquote](#quasiquote)) to contain them.

```scheme
#1=(begin (display #x) #1#)
                         => error
```


# Basic concepts

<a id="basicchapter"></a>

## Variables, syntactic keywords, and regions

<a id="specialformsection"></a>
<a id="variablesection"></a>

An identifier can name either a type of syntax or
a location where a value can be stored. An identifier that names a type
of syntax is called a *syntactic keyword*<a id="syntactic-keyword"></a>
and is said to be *bound* to a transformer for that syntax. An identifier that names a
location is called a *variable*<a id="variable"></a> and is said to be
*bound* to that location. The set of all visible
bindings<a id="binding"></a> in effect at some point in a program is
known as the *environment* in effect at that point. The value
stored in the location to which a variable is bound is called the
variable's value. By abuse of terminology, the variable is sometimes
said to name the value or to be bound to the value. This is not quite
accurate, but confusion rarely results from this practice.

Certain expression types are used to create new kinds of syntax
and to bind syntactic keywords to those new syntaxes, while other
expression types create new locations and bind variables to those
locations. These expression types are called *binding constructs*.
<a id="binding-construct"></a>
Those that bind syntactic keywords are listed in section [Macros](#macrosection).
The most fundamental of the variable binding constructs is the
`lambda` expression, because all other variable binding constructs
(except top-level bindings)
can be explained in terms of `lambda` expressions. The other
variable binding constructs are `let`, `let*`, `letrec`,
`letrec*`, `let-values`, `let*-values`,
and `do` expressions (see sections [lambda](#lambda), [letrec](#letrec), and
[do](#do)).

Scheme is a language with
block structure. To each place where an identifier is bound in a program
there corresponds a **region** of the program text within which
the binding is visible. The region is determined by the particular
binding construct that establishes the binding; if the binding is
established by a `lambda` expression, for example, then its region
is the entire `lambda` expression. Every mention of an identifier
refers to the binding of the identifier that established the
innermost of the regions containing the use. If there is no binding of
the identifier whose region contains the use, then the use refers to the
binding for the variable in the global environment, if any
(chapters [Expressions](#expressionchapter) and [Standard procedures](#initialenv)); if there is no
binding for the identifier,
it is said to be **unbound**.<a id="bound"></a>

## Disjointness of types

<a id="disjointness"></a>

No object satisfies more than one of the following predicates:

```scheme
boolean?          bytevector?
char?             eof-object?
null?             number?
pair?             port?
procedure?        string?
symbol?           vector?
```

and all predicates created by `define-record-type`.

These predicates define the types
*boolean, bytevector, character*, the empty list object,
*eof-object, number, pair, port, procedure, string, symbol, vector*,
and all record types.
<a id="type"></a>

Although there is a separate boolean type,
any Scheme value can be used as a boolean value for the purpose of a
conditional test. As explained in section [Booleans](#booleansection), all
values count as true in such a test except for `#f`.
This report uses the word “true” to refer to any
Scheme value except `#f`, and the word “false” to refer to
`#f`. <a id="true"></a> <a id="false"></a>

## External representations

<a id="externalreps"></a>

An important concept in Scheme (and Lisp) is that of the *external
representation* of an object as a sequence of characters. For example,
an external representation of the integer 28 is the sequence of
characters “`28`”, and an external representation of a list consisting
of the integers 8 and 13 is the sequence of characters “`(8 13)`”.

The external representation of an object is not necessarily unique. The
integer 28 also has representations “`#e28.000`” and “`#x1c`”, and the
list in the previous paragraph also has the representations “`( 08 13
)`” and “`(8 . (13 . ()))`” (see section [Pairs and lists](#listsection)).

Many objects have standard external representations, but some, such as
procedures, do not have standard representations (although particular
implementations may define representations for them).

An external representation can be written in a program to obtain the
corresponding object (see `quote`, section [quote](#quote)).

External representations can also be used for input and output. The
procedure `read` (section [read](#read)) parses external
representations, and the procedure `write` (section [write](#write))
generates them. Together, they provide an elegant and powerful
input/output facility.

Note that the sequence of characters “`(+ 2 6)`” is *not* an
external representation of the integer 8, even though it *is* an
expression evaluating to the integer 8; rather, it is an external
representation of a three-element list, the elements of which are the symbol
`+` and the integers 2 and 6. Scheme's syntax has the property that
any sequence of characters that is an expression is also the external
representation of some object. This can lead to confusion, since it is not always
obvious out of context whether a given sequence of characters is
intended to denote data or program, but it is also a source of power,
since it facilitates writing programs such as interpreters and
compilers that treat programs as data (or vice versa).

The syntax of external representations of various kinds of objects
accompanies the description of the primitives for manipulating the
objects in the appropriate sections of chapter [Standard procedures](#initialenv).

## Storage model

<a id="storagemodel"></a>

Variables and objects such as pairs, strings, vectors, and bytevectors implicitly
denote locations<a id="location"></a> or sequences of locations. A string, for
example, denotes as many locations as there are characters in the string.
A new value can be
stored into one of these locations using the `string-set!` procedure, but
the string continues to denote the same locations as before.

An object fetched from a location, by a variable reference or by
a procedure such as `car`, `vector-ref`, or `string-ref`, is
equivalent in the sense of `eqv?`
(section [Equivalence predicates](#equivalencesection))
to the object last stored in the location before the fetch.

Every location is marked to show whether it is in use.
No variable or object ever refers to a location that is not in use.

Whenever this report speaks of storage being newly allocated for a variable
or object, what is meant is that an appropriate number of locations are
chosen from the set of locations that are not in use, and the chosen
locations are marked to indicate that they are now in use before the variable
or object is made to denote them.
Notwithstanding this,
it is understood that the empty list cannot be newly allocated, because
it is a unique object. It is also understood that empty strings, empty
vectors, and empty bytevectors, which contain no locations, may or may
not be newly allocated.

Every object that denotes locations is
either mutable or
immutable. Literal constants, the strings
returned by `symbol->string`,
and possibly the environment returned by `scheme-report-environment`
are immutable objects. All objects
created by the other procedures listed in this report are mutable.
It is an
error to attempt to store a new value into a location that is denoted by an
immutable object.

These locations are to be understood as conceptual, not physical.
Hence, they do not necessarily correspond to memory addresses,
and even if they do, the memory address might not be constant.

> **Rationale:** In many systems it is desirable for constants (i.e. the values of
> literal expressions) to reside in read-only memory.
> Making it an error to alter constants permits this implementation strategy,
> while not requiring other systems to distinguish between
> mutable and immutable objects.

## Proper tail recursion

<a id="proper-tail-recursion"></a>

Implementations of Scheme are required to be
*properly tail-recursive*.
Procedure calls that occur in certain syntactic
contexts defined below are *tail calls*. A Scheme implementation is
properly tail-recursive if it supports an unbounded number of active
tail calls. A call is *active* if the called procedure might still
return. Note that this includes calls that might be returned from either
by the current continuation or by continuations captured earlier by
`call-with-current-continuation` that are later invoked.
In the absence of captured continuations, calls could
return at most once and the active calls would be those that had not
yet returned.
A formal definition of proper tail recursion can be found
in [[propertailrecursion](#cite-propertailrecursion)].

> **Rationale:** Intuitively, no space is needed for an active tail call because the
> continuation that is used in the tail call has the same semantics as the
> continuation passed to the procedure containing the call. Although an improper
> implementation might use a new continuation in the call, a return
> to this new continuation would be followed immediately by a return
> to the continuation passed to the procedure. A properly tail-recursive
> implementation returns to that continuation directly.
>
>
> Proper tail recursion was one of the central ideas in Steele and
> Sussman's original version of Scheme. Their first Scheme interpreter
> implemented both functions and actors. Control flow was expressed using
> actors, which differed from functions in that they passed their results
> on to another actor instead of returning to a caller. In the terminology
> of this section, each actor finished with a tail call to another actor.
>
>
> Steele and Sussman later observed that in their interpreter the code
> for dealing with actors was identical to that for functions and thus
> there was no need to include both in the language.

A *tail call*<a id="tail-call"></a> is a procedure call that occurs
in a *tail context*. Tail contexts are defined inductively. Note
that a tail context is always determined with respect to a particular lambda
expression.

- The last expression within the body of a lambda expression,
   shown as ⟨tail expression⟩ below, occurs in a tail context.
   The same is true of all the bodies of `case-lambda` expressions.

  ```bnf
  (lambda ⟨formals⟩
        ⟨definition⟩* ⟨expression⟩* ⟨tail expression⟩)

  (case-lambda (⟨formals⟩ ⟨tail body⟩)*)
  ```
- If one of the following expressions is in a tail context,
  then the subexpressions shown as ⟨tail expression⟩ are in a tail context.
  These were derived from rules in the grammar given in
  chapter [Formal syntax and semantics](#formalchapter) by replacing some occurrences of ⟨body⟩
  with ⟨tail body⟩, some occurrences of ⟨expression⟩
  with ⟨tail expression⟩, and some occurrences of ⟨sequence⟩
  with ⟨tail sequence⟩. Only those rules that contain tail contexts
  are shown here.

  ```bnf
  (if ⟨expression⟩ ⟨tail expression⟩ ⟨tail expression⟩)
  (if ⟨expression⟩ ⟨tail expression⟩)

  (cond ⟨cond clause⟩⁺)
  (cond ⟨cond clause⟩* (else ⟨tail sequence⟩))

  (case ⟨expression⟩
        ⟨case clause⟩⁺)
  (case ⟨expression⟩
        ⟨case clause⟩*
        (else ⟨tail sequence⟩))

  (and ⟨expression⟩* ⟨tail expression⟩)
  (or ⟨expression⟩* ⟨tail expression⟩)

  (when ⟨test⟩ ⟨tail sequence⟩)
  (unless ⟨test⟩ ⟨tail sequence⟩)

  (let (⟨binding spec⟩*) ⟨tail body⟩)
  (let ⟨variable⟩ (⟨binding spec⟩*) ⟨tail body⟩)
  (let* (⟨binding spec⟩*) ⟨tail body⟩)
  (letrec (⟨binding spec⟩*) ⟨tail body⟩)
  (letrec* (⟨binding spec⟩*) ⟨tail body⟩)
  (let-values (⟨mv binding spec⟩*) ⟨tail body⟩)
  (let*-values (⟨mv binding spec⟩*) ⟨tail body⟩)

  (let-syntax (⟨syntax spec⟩*) ⟨tail body⟩)
  (letrec-syntax (⟨syntax spec⟩*) ⟨tail body⟩)

  (begin ⟨tail sequence⟩)

  (do (⟨iteration spec⟩*)
              (⟨test⟩ ⟨tail sequence⟩)
        ⟨expression⟩*)

   where

  ⟨cond clause⟩  ⟶  (⟨test⟩ ⟨tail sequence⟩)
  ⟨case clause⟩  ⟶  ((⟨datum⟩*) ⟨tail sequence⟩)

  ⟨tail body⟩  ⟶  ⟨definition⟩* ⟨tail sequence⟩
  ⟨tail sequence⟩  ⟶  ⟨expression⟩* ⟨tail expression⟩
  ```
- If a `cond` or `case` expression is in a tail context, and has
  a clause of the form `(⟨expression⟩₁ => ⟨expression⟩₂)`
  then the (implied) call to
  the procedure that results from the evaluation of ⟨expression⟩₂ is in a
  tail context. ⟨expression⟩₂ itself is not in a tail context.

Certain procedures defined in this report are also required to perform tail calls.
The first argument passed to `apply` and to
`call-with-current-continuation`, and the second argument passed to
`call-with-values`, must be called via a tail call.
Similarly, `eval` must evaluate its first argument as if it
were in tail position within the `eval` procedure.

In the following example the only tail call is the call to `f`.
None of the calls to `g` or `h` are tail calls. The reference to
`x` is in a tail context, but it is not a call and thus is not a
tail call.

```scheme
(lambda ()
  (if (g)
      (let ((x (h)))
        x)
      (and (g) (f))))
```

> **Note:** Implementations may
> recognize that some non-tail calls, such as the call to `h`
> above, can be evaluated as though they were tail calls.
> In the example above, the `let` expression could be compiled
> as a tail call to `h`. (The possibility of `h` returning
> an unexpected number of values can be ignored, because in that
> case the effect of the `let` is explicitly unspecified and
> implementation-dependent.)


# Expressions

<a id="expressionchapter"></a>

Expression types are categorized as *primitive* or *derived*.
Primitive expression types include variables and procedure calls.
Derived expression types are not semantically primitive, but can instead
be defined as macros.
Suitable syntax definitions of some of the derived expressions are
given in section [Derived expression types](#derivedsection).

The procedures `force`, `promise?`, `make-promise`, and `make-parameter`
are also described in this chapter because they are intimately associated
with the `delay`, `delay-force`, and `parameterize` expression types.

## Primitive expression types

<a id="primitivexps"></a>

### Variable references

**`⟨variable⟩`** — syntax

An expression consisting of a variable
(section [Variables, syntactic keywords, and regions](#variablesection)) is a variable reference. The value of
the variable reference is the value stored in the location to which the
variable is bound. It is an error to reference an
unbound variable.

```scheme
(define x 28)
x     =>  28
```

### Literal expressions

<a id="literalsection"></a>

<a id="quote"></a>
**`(quote ⟨datum⟩)`** — syntax  
**`'⟨datum⟩`** — syntax  
**`⟨constant⟩`** — syntax

`(quote ⟨datum⟩)` evaluates to ⟨datum⟩.<a id="x-2"></a>
⟨Datum⟩
can be any external representation of a Scheme object (see
section [External representations](#externalreps)). This notation is used to include literal
constants in Scheme code.

```scheme
(quote a)                       =>  a
(quote #(a b c))       =>  #(a b c)
(quote (+ 1 2))                 =>  (+ 1 2)
```

`(quote ⟨datum⟩)` can be abbreviated as
'⟨datum⟩. The two notations are equivalent in all
respects.

```scheme
'a                     =>  a
'#(a b c)             =>  #(a b c)
'()                    =>  ()
'(+ 1 2)               =>  (+ 1 2)
'(quote a)             =>  (quote a)
''a                    =>  (quote a)
```

Numerical constants, string constants, character constants, vector
constants, bytevector constants, and boolean constants evaluate to
themselves; they need not be quoted.

```scheme
'145932      =>  145932
145932       =>  145932
'"abc"       =>  "abc"
"abc"        =>  "abc"
'#a     =>  #a
#a     =>  #a
'#(a 10)    =>  #(a 10)
#(a 10)    =>  #(a 10)
'#u8(64 65)    =>  #u8(64 65)
#u8(64 65)    =>  #u8(64 65)
'#t    =>  #t
#t     =>  #t
```

As noted in section [Storage model](#storagemodel), it is an error to attempt to alter a constant
(i.e. the value of a literal expression) using a mutation procedure like
`set-car!` or `string-set!`.

### Procedure calls

**`(⟨operator⟩ ⟨operand⟩₁ …)`** — syntax

A procedure call is written by enclosing in parentheses an
expression for the procedure to be called followed by expressions for the arguments to be
passed to it. The operator and operand expressions are evaluated (in an
unspecified order) and the resulting procedure is passed the resulting
arguments.<a id="call"></a><a id="procedure-call"></a>

```scheme
(+ 3 4)                            =>  7
((if #f + *) 3 4)           =>  12
```

The procedures in this document are available as the values of variables exported by the
standard libraries. For example, the addition and multiplication
procedures in the above examples are the values of the variables `+`
and `*` in the base library. New procedures are created by evaluating `lambda` expressions
(see section [lambda](#lambda)).

Procedure calls can return any number of values (see `values` in
section [Control features](#proceduresection)).
Most of the procedures defined in this report return one
value or, for procedures such as `apply`, pass on the values returned
by a call to one of their arguments.
Exceptions are noted in the individual descriptions.

> **Note:** evaluation is unspecified, and the operator expression and the operand
> expressions are always evaluated with the same evaluation rules.

> **Note:** Although the order of evaluation is otherwise unspecified, the effect of
> any concurrent evaluation of the operator and operand expressions is
> constrained to be consistent with some sequential order of evaluation.
> The order of evaluation may be chosen differently for each procedure call.

> **Note:** (), is a legitimate expression evaluating to itself. In Scheme, it is an error.

### Procedures

<a id="lamba"></a>

<a id="lambda"></a>
**`(lambda ⟨formals⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Formals⟩ is a formal arguments list as described below,
and ⟨body⟩ is a sequence of zero or more definitions
followed by one or more expressions.

*Semantics:*
 A `lambda` expression evaluates to a procedure. The environment in
effect when the `lambda` expression was evaluated is remembered as part of the
procedure. When the procedure is later called with some actual
arguments, the environment in which the `lambda` expression was evaluated will
be extended by binding the variables in the formal argument list to
fresh locations, and the corresponding actual argument values will be stored
in those locations.
(A **fresh** location is one that is distinct from every previously
existing location.)
Next, the expressions in the
body of the lambda expression (which, if it contains definitions,
represents a `letrec*` form — see section [Binding constructs](#letrecstar))
will be evaluated sequentially in the extended environment.
The results of the last expression in the body will be returned as
the results of the procedure call.

```scheme
(lambda (x) (+ x x))        =>  a procedure
((lambda (x) (+ x x)) 4)    =>  8

(define reverse-subtract
  (lambda (x y) (- y x)))
(reverse-subtract 7 10)           =>  3

(define add4
  (let ((x 4))
    (lambda (y) (+ x y))))
(add4 6)                          =>  10
```

⟨Formals⟩ have one of the following forms:

- `(⟨variable⟩₁ …)`:
  The procedure takes a fixed number of arguments; when the procedure is
  called, the arguments will be stored in fresh locations
  that are bound to the corresponding variables.
- ⟨variable⟩:
  The procedure takes any number of arguments; when the procedure is
  called, the sequence of actual arguments is converted into a newly
  allocated list, and the list is stored in a fresh location
  that is bound to
  ⟨variable⟩.
- `(⟨variable⟩₁ … ⟨variable$_{n}$⟩ **.**
  ⟨variable$_{n+1}$⟩)`:
  If a space-delimited period precedes the last variable, then
  the procedure takes $n$ or more arguments, where $n$ is the
  number of formal arguments before the period (it is an error if there is not
  at least one).
  The value stored in the binding of the last variable will be a
  newly allocated
  list of the actual arguments left over after all the other actual
  arguments have been matched up against the other formal arguments.

It is an error for a ⟨variable⟩ to appear more than once in
⟨formals⟩.

```scheme
((lambda x x) 3 4 5 6)            =>  (3 4 5 6)
((lambda (x y . z) z)
 3 4 5 6)                         =>  (5 6)
```

Each procedure created as the result of evaluating a `lambda` expression is
(conceptually) tagged
with a storage location, in order to make `eqv?` and
`eq?` work on procedures (see section [Equivalence predicates](#equivalencesection)).

### Conditionals

<a id="if"></a>
**`(if ⟨test⟩ ⟨consequent⟩ ⟨alternate⟩)`** — syntax  
**`(if ⟨test⟩ ⟨consequent⟩)`** — syntax

*Syntax:*
⟨Test⟩, ⟨consequent⟩, and ⟨alternate⟩ are
expressions.

*Semantics:*
An `if` expression is evaluated as follows: first,
⟨test⟩ is evaluated. If it yields a true value (see
section [Booleans](#booleansection)), then ⟨consequent⟩ is evaluated and
its values are returned. Otherwise ⟨alternate⟩ is evaluated and its
values are returned. If ⟨test⟩ yields a false value and no
⟨alternate⟩ is specified, then the result of the expression is
unspecified.

```scheme
(if (> 3 2) 'yes 'no)             =>  yes
(if (> 2 3) 'yes 'no)             =>  no
(if (> 3 2)
    (- 3 2)
    (+ 3 2))                      =>  1
```

### Assignments

<a id="assignment"></a>

<a id="set"></a>
**`(set! ⟨variable⟩ ⟨expression⟩)`** — syntax

*Semantics:*
⟨Expression⟩ is evaluated, and the resulting value is stored in
the location to which ⟨variable⟩ is bound. It is an error if ⟨variable⟩ is not
bound either in some region enclosing the `set!` expression
or else globally.
The result of the `set!` expression is
unspecified.

```scheme
(define x 2)
(+ x 1)                   =>  3
(set! x 4)                =>  unspecified
(+ x 1)                   =>  5
```

### Inclusion

<a id="inclusion"></a>

<a id="include"></a>
**`(include ⟨string⟩₁ ⟨string⟩₂ …)`** — syntax  
**`(include-ci ⟨string⟩₁ ⟨string⟩₂ …)`** — syntax

*Semantics:*
Both `include` and
`include-ci` take one or more filenames expressed as string literals,
apply an implementation-specific algorithm to find corresponding files,
read the contents of the files in the specified order as if by repeated applications
of `read`,
and effectively replace the `include` or `include-ci` expression
with a `begin` expression containing what was read from the files.
The difference between the two is that `include-ci` reads each file
as if it began with the `#!fold-case` directive, while `include`
does not.

> **Note:** Implementations are encouraged to search for files in the directory
> which contains the including file, and to provide a way for users to
> specify other directories to search.

## Derived expression types

<a id="derivedexps"></a>

The constructs in this section are hygienic, as discussed in
section [Macros](#macrosection).
For reference purposes, section [Derived expression types](#derivedsection) gives syntax definitions
that will convert most of the constructs described in this section
into the primitive constructs described in the previous section.

### Conditionals

<a id="cond"></a>
**`(cond ⟨clause⟩₁ ⟨clause⟩₂ …)`** — syntax  
**`else`** — auxiliary syntax  
**`=>`** — auxiliary syntax

*Syntax:*
⟨Clauses⟩ take one of two forms, either

```scheme
(⟨test⟩ ⟨expression⟩₁ ...)
```

where ⟨test⟩ is any expression, or

```scheme
(⟨test⟩ => ⟨expression⟩)
```

The last ⟨clause⟩ can be
an “else clause,” which has the form

```scheme
(else ⟨expression⟩₁ ⟨expression⟩₂ ...).
```

<a id="else"></a>
<a id="x-3"></a>

*Semantics:*
A `cond` expression is evaluated by evaluating the ⟨test⟩
expressions of successive ⟨clause⟩s in order until one of them
evaluates to a true value (see
section [Booleans](#booleansection)). When a ⟨test⟩ evaluates to a true
value, the remaining ⟨expression⟩s in its ⟨clause⟩ are
evaluated in order, and the results of the last ⟨expression⟩ in the
⟨clause⟩ are returned as the results of the entire `cond`
expression.

If the selected ⟨clause⟩ contains only the
⟨test⟩ and no ⟨expression⟩s, then the value of the
⟨test⟩ is returned as the result. If the selected ⟨clause⟩ uses the
`=>` alternate form, then the ⟨expression⟩ is evaluated.
It is an error if its value is not a procedure that accepts one argument. This procedure is then
called on the value of the ⟨test⟩ and the values returned by this
procedure are returned by the `cond` expression.

If all ⟨test⟩s evaluate
to `#f`, and there is no else clause, then the result of
the conditional expression is unspecified; if there is an else
clause, then its ⟨expression⟩s are evaluated in order, and the values of
the last one are returned.

```scheme
(cond ((> 3 2) 'greater)
      ((< 3 2) 'less))           =>  greater

(cond ((> 3 3) 'greater)
      ((< 3 3) 'less)
      (else 'equal))              =>  equal

(cond ((assv 'b '((a 1) (b 2))) => cadr)
      (else #f))           =>  2
```

<a id="case"></a>
**`(case ⟨key⟩ ⟨clause⟩₁ ⟨clause⟩₂ …)`** — syntax

*Syntax:*
⟨Key⟩ can be any expression. Each ⟨clause⟩ has
the form

```scheme
((⟨datum⟩₁ ...) ⟨expression⟩₁ ⟨expression⟩₂ ...),
```

where each ⟨datum⟩ is an external representation of some object.
It is an error if any of the ⟨datum⟩s are the same anywhere in the expression.
Alternatively, a ⟨clause⟩ can be of the form

```scheme
((⟨datum⟩₁ ...) => ⟨expression⟩)
```

The last ⟨clause⟩ can be an “else clause,” which has one of the forms

```scheme
(else ⟨expression⟩₁ ⟨expression⟩₂ ...)
```

or

```scheme
(else => ⟨expression⟩).
```

*Semantics:*
A `case` expression is evaluated as follows. ⟨Key⟩ is
evaluated and its result is compared against each ⟨datum⟩. If the
result of evaluating ⟨key⟩ is the same (in the sense of
`eqv?`; see section [eqv?](#eqv)) to a ⟨datum⟩, then the
expressions in the corresponding ⟨clause⟩ are evaluated in order
and the results of the last expression in the ⟨clause⟩ are
returned as the results of the `case` expression.

If the result of
evaluating ⟨key⟩ is different from every ⟨datum⟩, then if
there is an else clause, its expressions are evaluated and the
results of the last are the results of the `case` expression;
otherwise the result of the `case` expression is unspecified.

If the selected ⟨clause⟩ or else clause uses the
`=>` alternate form, then the ⟨expression⟩ is evaluated.
It is an error if its value is not a procedure accepting one argument.
This procedure is then
called on the value of the ⟨key⟩ and the values returned by this
procedure are returned by the `case` expression.

```scheme
(case (* 2 3)
  ((2 3 5 7) 'prime)
  ((1 4 6 8 9) 'composite))       =>  composite
(case (car '(c d))
  ((a) 'a)
  ((b) 'b))                       =>  unspecified
(case (car '(c d))
  ((a e i o u) 'vowel)
  ((w y) 'semivowel)
  (else => (lambda (x) x)))       =>  c
```

<a id="and"></a>
**`(and ⟨test⟩₁ …)`** — syntax

*Semantics:*
The ⟨test⟩ expressions are evaluated from left to right, and if
any expression evaluates to `#f` (see
section [Booleans](#booleansection)), then `#f` is returned. Any remaining
expressions are not evaluated. If all the expressions evaluate to
true values, the values of the last expression are returned. If there
are no expressions, then `#t` is returned.

```scheme
(and (= 2 2) (> 2 1))             =>  #t
(and (= 2 2) (< 2 1))             =>  #f
(and 1 2 'c '(f g))               =>  (f g)
(and)                             =>  #t
```

<a id="or"></a>
**`(or ⟨test⟩₁ …)`** — syntax

*Semantics:*
The ⟨test⟩ expressions are evaluated from left to right, and the value of the
first expression that evaluates to a true value (see
section [Booleans](#booleansection)) is returned. Any remaining expressions
are not evaluated. If all expressions evaluate to `#f`
or if there are no expressions, then `#f` is returned.

```scheme
(or (= 2 2) (> 2 1))              =>  #t
(or (= 2 2) (< 2 1))              =>  #t
(or #f #f #f)   =>  #f
(or (memq 'b '(a b c))
    (/ 3 0))                      =>  (b c)
```

<a id="when"></a>
**`(when ⟨test⟩ ⟨expression⟩₁ ⟨expression⟩₂ …)`** — syntax

*Syntax:*
The ⟨test⟩ is an expression.

*Semantics:*
The test is evaluated, and if it evaluates to a true value,
the expressions are evaluated in order. The result of the `when`
expression is unspecified.

```scheme
(when (= 1 1.0)
  (display "1")
  (display "2"))    =>  unspecified
 and prints  12
```

<a id="unless"></a>
**`(unless ⟨test⟩ ⟨expression⟩₁ ⟨expression⟩₂ …)`** — syntax

*Syntax:*
The ⟨test⟩ is an expression.

*Semantics:*
The test is evaluated, and if it evaluates to `#f`,
the expressions are evaluated in order. The result of the `unless`
expression is unspecified.

```scheme
(unless (= 1 1.0)
  (display "1")
  (display "2"))    =>  unspecified
 and prints nothing
```

<a id="cond-expand"></a>
**`(cond-expand ⟨ce-clause⟩₁ ⟨ce-clause⟩₂ …)`** — syntax

*Syntax:*
The `cond-expand` expression type
provides a way to statically
expand different expressions depending on the
implementation. A
⟨ce-clause⟩ takes the following form:

`(⟨feature requirement⟩ ⟨expression⟩ …)`

The last clause can be an “else clause,” which has the form

`(else ⟨expression⟩ …)`

A ⟨feature requirement⟩ takes one of the following forms:

- `⟨feature identifier⟩`
- `(library ⟨library name⟩)`
- `(and ⟨feature requirement⟩ …)`
- `(or ⟨feature requirement⟩ …)`
- `(not ⟨feature requirement⟩)`

*Semantics:*
Each implementation maintains a list of feature identifiers which are
present, as well as a list of libraries which can be imported. The
value of a ⟨feature requirement⟩ is determined by replacing
each ⟨feature identifier⟩ and `(library ⟨library name⟩)`
on the implementation's lists with `#t`, and all other feature
identifiers and library names with `#f`, then evaluating the
resulting expression as a Scheme boolean expression under the normal
interpretation of `and`, `or`, and `not`.

A `cond-expand` is then expanded by evaluating the
⟨feature requirement⟩s of successive ⟨ce-clause⟩s
in order until one of them returns `#t`. When a true clause is
found, the corresponding ⟨expression⟩s are expanded to a
`begin`, and the remaining clauses are ignored.
If none of the ⟨feature requirement⟩s evaluate to `#t`, then
if there is an else clause, its ⟨expression⟩s are
included. Otherwise, the behavior of the `cond-expand` is unspecified.
Unlike `cond`, `cond-expand` does not depend on the value
of any variables.

The exact features provided are implementation-defined, but for
portability a core set of features is given in
appendix [Standard Feature Identifiers](#stdfeatures).

### Binding constructs

<a id="bindingsection"></a>

The binding constructs `let`, `let*`, `letrec`, `letrec*`,
`let-values`, and `let*-values`
give Scheme a block structure, like Algol 60. The syntax of the first four
constructs is identical, but they differ in the regions they establish
for their variable bindings. In a `let` expression, the initial
values are computed before any of the variables become bound; in a
`let*` expression, the bindings and evaluations are performed
sequentially; while in `letrec` and `letrec*` expressions,
all the bindings are in
effect while their initial values are being computed, thus allowing
mutually recursive definitions.
The `let-values` and `let*-values` constructs are analogous to `let` and `let*`
respectively, but are designed to handle multiple-valued expressions, binding
different identifiers to the returned values.

<a id="let"></a>
**`(let ⟨bindings⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Bindings⟩ has the form

```scheme
((⟨variable⟩₁ ⟨init⟩₁) ...),
```

where each ⟨init⟩ is an expression, and ⟨body⟩ is a
sequence of zero or more definitions followed by a
sequence of one or more expressions as described in section [lambda](#lambda). It is
an error for a ⟨variable⟩ to appear more than once in the list of variables
being bound.

*Semantics:*
The ⟨init⟩s are evaluated in the current environment (in some
unspecified order), the ⟨variable⟩s are bound to fresh locations
holding the results, the ⟨body⟩ is evaluated in the extended
environment, and the values of the last expression of ⟨body⟩
are returned. Each binding of a ⟨variable⟩ has ⟨body⟩ as its
region.

```scheme
(let ((x 2) (y 3))
  (* x y))                        =>  6

(let ((x 2) (y 3))
  (let ((x 7)
        (z (+ x y)))
    (* z x)))                     =>  35
```

See also “named `let`,” section [Iteration](#namedlet).

<a id="let-2"></a>
**`(let* ⟨bindings⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Bindings⟩ has the form

```scheme
((⟨variable⟩₁ ⟨init⟩₁) ...),
```

and ⟨body⟩ is a sequence of
zero or more definitions followed by
one or more expressions as described in section [lambda](#lambda).

*Semantics:*
The `let*` binding construct is similar to `let`, but the bindings are performed
sequentially from left to right, and the region of a binding indicated
by `(⟨variable⟩ ⟨init⟩)` is that part of the `let*`
expression to the right of the binding. Thus the second binding is done
in an environment in which the first binding is visible, and so on.
The ⟨variable⟩s need not be distinct.

```scheme
(let ((x 2) (y 3))
  (let* ((x 7)
         (z (+ x y)))
    (* z x)))               =>  70
```

<a id="letrec"></a>
**`(letrec ⟨bindings⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Bindings⟩ has the form

```scheme
((⟨variable⟩₁ ⟨init⟩₁) ...),
```

and ⟨body⟩ is a sequence of
zero or more definitions followed by
one or more expressions as described in section [lambda](#lambda). It is an error for a ⟨variable⟩ to appear more
than once in the list of variables being bound.

*Semantics:*
The ⟨variable⟩s are bound to fresh locations holding unspecified
values, the ⟨init⟩s are evaluated in the resulting environment (in
some unspecified order), each ⟨variable⟩ is assigned to the result
of the corresponding ⟨init⟩, the ⟨body⟩ is evaluated in the
resulting environment, and the values of the last expression in
⟨body⟩ are returned. Each binding of a ⟨variable⟩ has the
entire `letrec` expression as its region, making it possible to
define mutually recursive procedures.

```scheme
(letrec ((even?
          (lambda (n)
            (if (zero? n)
                #t
                (odd? (- n 1)))))
         (odd?
          (lambda (n)
            (if (zero? n)
                #f
                (even? (- n 1))))))
  (even? 88))
		  =>  #t
```

One restriction on `letrec` is very important: if it is not possible
to evaluate each ⟨init⟩ without assigning or referring to the value of any
⟨variable⟩, it is an error. The
restriction is necessary because
`letrec` is defined in terms of a procedure
call where a `lambda` expression binds the ⟨variable⟩s to the values
of the ⟨init⟩s.
In the most common uses of `letrec`, all the ⟨init⟩s are
`lambda` expressions and the restriction is satisfied automatically.

<a id="letrec-2"></a>
**`(letrec* ⟨bindings⟩ ⟨body⟩)`** — syntax

<a id="letrecstar"></a>

*Syntax:*
⟨Bindings⟩ has the form

```scheme
((⟨variable⟩₁ ⟨init⟩₁) ...),
```

and ⟨body⟩ is a sequence of
zero or more definitions followed by
one or more expressions as described in section [lambda](#lambda). It is an error for a ⟨variable⟩ to appear more
than once in the list of variables being bound.

*Semantics:*
The ⟨variable⟩s are bound to fresh locations,
each ⟨variable⟩ is assigned in left-to-right order to the
result of evaluating the corresponding ⟨init⟩
(interleaving evaluations and assignments),
the ⟨body⟩ is
evaluated in the resulting environment, and the values of the last
expression in ⟨body⟩ are returned.
Despite the left-to-right evaluation and assignment order, each binding of
a ⟨variable⟩ has the entire `letrec*` expression as its
region, making it possible to define mutually recursive
procedures.

If it is not possible to evaluate each ⟨init⟩ without assigning or
referring to the value of the corresponding ⟨variable⟩ or the
⟨variable⟩ of any of the bindings that follow it in
⟨bindings⟩, it is an error.
Another restriction is that it is an error to invoke the continuation
of an ⟨init⟩ more than once.

```scheme
;; Returns the arithmetic, geometric, and
;; harmonic means of a nested list of numbers
(define (means ton)
  (letrec*
     ((mean
        (lambda (f g)
          (f (/ (sum g ton) n))))
      (sum
        (lambda (g ton)
          (if (null? ton)
            (+)
            (if (number? ton)
                (g ton)
                (+ (sum g (car ton))
                   (sum g (cdr ton)))))))
      (n (sum (lambda (x) 1) ton)))
    (values (mean values values)
            (mean exp log)
            (mean / /))))
```

Evaluating `(means '(3 (1 4)))` returns three values:
8/3, 2.28942848510666 (approximately), and 36/19.

<a id="let-values"></a>
**`(let-values ⟨mv binding spec⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Mv binding spec⟩ has the form

```scheme
((⟨formals⟩₁ ⟨init⟩₁) ...),
```

where each ⟨init⟩ is an expression, and ⟨body⟩ is
zero or more definitions followed by a sequence of one or
more expressions as described in section [lambda](#lambda). It is an error for a variable to appear more than
once in the set of ⟨formals⟩.

*Semantics:*
The ⟨init⟩s are evaluated in the current environment (in some
unspecified order) as if by invoking `call-with-values`, and the
variables occurring in the ⟨formals⟩ are bound to fresh locations
holding the values returned by the ⟨init⟩s, where the
⟨formals⟩ are matched to the return values in the same way that
the ⟨formals⟩ in a `lambda` expression are matched to the
arguments in a procedure call. Then, the ⟨body⟩ is evaluated in
the extended environment, and the values of the last expression of
⟨body⟩ are returned. Each binding of a ⟨variable⟩ has
⟨body⟩ as its region.

It is an error if the ⟨formals⟩ do not match the number of
values returned by the corresponding ⟨init⟩.

```scheme
(let-values (((root rem) (exact-integer-sqrt 32)))
  (* root rem))                  =>  35
```

<a id="let-values-2"></a>
**`(let*-values ⟨mv binding spec⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Mv binding spec⟩ has the form

```scheme
((⟨formals⟩ ⟨init⟩) ...),
```

and ⟨body⟩ is a sequence of zero or more
definitions followed by one or more expressions as described in section [lambda](#lambda). In each ⟨formals⟩,
it is an error if any variable appears more than once.

*Semantics:*
The `let*-values` construct is similar to `let-values`, but the
⟨init⟩s are evaluated and bindings created sequentially from
left to right, with the region of the bindings of each ⟨formals⟩
including the ⟨init⟩s to its right as well as ⟨body⟩. Thus the
second ⟨init⟩ is evaluated in an environment in which the first
set of bindings is visible and initialized, and so on.

```scheme
(let ((a 'a) (b 'b) (x 'x) (y 'y))
  (let*-values (((a b) (values x y))
                ((x y) (values a b)))
    (list a b x y)))       => (x y x y)
```

### Sequencing

<a id="sequencing"></a>

Both of Scheme's sequencing constructs are named `begin`, but the two
have slightly different forms and uses:

<a id="begin"></a>
**`(begin ⟨expression or definition⟩ …)`** — syntax

This form of `begin` can appear as part of a ⟨body⟩, or at the
outermost level of a ⟨program⟩, or at the REPL, or directly nested
in a `begin` that is itself of this form.
It causes the contained expressions and definitions to be evaluated
exactly as if the enclosing `begin` construct were not present.

> **Rationale:** This form is commonly used in the output of
> macros (see section [Macros](#macrosection))
> which need to generate multiple definitions and
> splice them into the context in which they are expanded.

**`(begin ⟨expression⟩₁ ⟨expression⟩₂ …)`** — syntax

This form of `begin` can be used as an ordinary expression.
The ⟨expression⟩s are evaluated sequentially from left to right,
and the values of the last ⟨expression⟩ are returned. This
expression type is used to sequence side effects such as assignments
or input and output.

```scheme
(define x 0)

(and (= x 0)
     (begin (set! x 5)
            (+ x 1)))                =>  6

(begin (display "4 plus 1 equals ")
       (display (+ 4 1)))        =>  unspecified
 and prints  4 plus 1 equals 5
```

Note that there is a third form of `begin` used as a library declaration:
see section [Library Syntax](#librarydeclarations).

### Iteration

**`(do ((⟨variable⟩₁ ⟨init⟩₁ ⟨step⟩₁)`** — syntax
<a id="do"></a>`…)\
 (⟨test⟩ ⟨expression⟩ …)\
 ⟨command⟩ …)`

*Syntax:*
All of ⟨init⟩, ⟨step⟩, ⟨test⟩, and ⟨command⟩
are expressions.

*Semantics:*
A `do` expression is an iteration construct. It specifies a set of variables to
be bound, how they are to be initialized at the start, and how they are
to be updated on each iteration. When a termination condition is met,
the loop exits after evaluating the ⟨expression⟩s.

A `do` expression is evaluated as follows:
The ⟨init⟩ expressions are evaluated (in some unspecified order),
the ⟨variable⟩s are bound to fresh locations, the results of the
⟨init⟩ expressions are stored in the bindings of the
⟨variable⟩s, and then the iteration phase begins.

Each iteration begins by evaluating ⟨test⟩; if the result is
false (see section [Booleans](#booleansection)), then the ⟨command⟩
expressions are evaluated in order for effect, the ⟨step⟩
expressions are evaluated in some unspecified order, the
⟨variable⟩s are bound to fresh locations, the results of the
⟨step⟩s are stored in the bindings of the
⟨variable⟩s, and the next iteration begins.

If ⟨test⟩ evaluates to a true value, then the
⟨expression⟩s are evaluated from left to right and the values of
the last ⟨expression⟩ are returned. If no ⟨expression⟩s
are present, then the value of the `do` expression is unspecified.

The region of the binding of a ⟨variable⟩
consists of the entire `do` expression except for the ⟨init⟩s.
It is an error for a ⟨variable⟩ to appear more than once in the
list of `do` variables.

A ⟨step⟩ can be omitted, in which case the effect is the
same as if `(⟨variable⟩ ⟨init⟩ ⟨variable⟩)` had
been written instead of `(⟨variable⟩ ⟨init⟩)`.

```scheme
(do ((vec (make-vector 5))
     (i 0 (+ i 1)))
    ((= i 5) vec)
  (vector-set! vec i i))            =>  #(0 1 2 3 4)

(let ((x '(1 3 5 7 9)))
  (do ((x x (cdr x))
       (sum 0 (+ sum (car x))))
      ((null? x) sum)))               =>  25
```

**`(let ⟨variable⟩ ⟨bindings⟩ ⟨body⟩)`** — syntax

<a id="namedlet"></a>
*Semantics:*
“Named `let`” is a variant on the syntax of `let` which provides
a more general looping construct than `do` and can also be used to express
recursion.
It has the same syntax and semantics as ordinary `let`
except that ⟨variable⟩ is bound within ⟨body⟩ to a procedure
whose formal arguments are the bound variables and whose body is
⟨body⟩. Thus the execution of ⟨body⟩ can be repeated by
invoking the procedure named by ⟨variable⟩.

```scheme
(let loop ((numbers '(3 -2 1 6 -5))
           (nonneg '())
           (neg '()))
  (cond ((null? numbers) (list nonneg neg))
        ((>= (car numbers) 0)
         (loop (cdr numbers)
               (cons (car numbers) nonneg)
               neg))
        ((< (car numbers) 0)
         (loop (cdr numbers)
               nonneg
               (cons (car numbers) neg)))))
  =>  ((6 1 3) (-5 -2))
```

### Delayed evaluation

<a id="delay"></a>
**`(delay ⟨expression⟩)`** — lazy library syntax

*Semantics:*
The `delay` construct is used together with the procedure `force` to
implement **lazy evaluation** or **call by need**.
`(delay ⟨expression⟩)` returns an object called a
**promise** which at some point in the future can be asked (by
the `force` procedure) to evaluate
⟨expression⟩, and deliver the resulting value.

The effect of ⟨expression⟩ returning multiple values
is unspecified.

<a id="delay-force"></a>
**`(delay-force ⟨expression⟩)`** — lazy library syntax

*Semantics:*
The expression `(delay-force expression)` is conceptually similar to
`(delay (force expression))`,
with the difference that forcing the result
of `delay-force` will in effect result in a tail call to
`(force expression)`,
while forcing the result of
`(delay (force expression))`
might not. Thus
iterative lazy algorithms that might result in a long series of chains of
`delay` and `force`
can be rewritten using `delay-force` to prevent consuming
unbounded space during evaluation.

<a id="force"></a>
**`(force promise)`** — lazy library procedure

The `force` procedure forces the value of a *promise* created
by `delay`, `delay-force`, or `make-promise`.
If no value has been computed for the promise, then a value is
computed and returned. The value of the promise must be cached (or
“memoized”) so that if it is forced a second time, the previously
computed value is returned.
Consequently, a delayed expression is evaluated using the parameter
values and exception handler of the call to `force` which first
requested its value.
If *promise* is not a promise, it may be returned unchanged.

```scheme
(force (delay (+ 1 2)))     =>  3
(let ((p (delay (+ 1 2))))
  (list (force p) (force p)))
                                 =>  (3 3)

(define integers
  (letrec ((next
            (lambda (n)
              (delay (cons n (next (+ n 1)))))))
    (next 0)))
(define head
  (lambda (stream) (car (force stream))))
(define tail
  (lambda (stream) (cdr (force stream))))

(head (tail (tail integers)))
                                 =>  2
```

The following example is a mechanical transformation of a lazy
stream-filtering algorithm into Scheme. Each call to a constructor is
wrapped in `delay`, and each argument passed to a deconstructor is
wrapped in `force`. The use of `(delay-force ...)` instead of `(delay (force ...))` around the body of the procedure ensures that an
ever-growing sequence of pending promises does not
exhaust available storage,
because `force` will in effect force such sequences iteratively.

```scheme
(define (stream-filter p? s)
  (delay-force
   (if (null? (force s))
       (delay '())
       (let ((h (car (force s)))
             (t (cdr (force s))))
         (if (p? h)
             (delay (cons h (stream-filter p? t)))
             (stream-filter p? t))))))

(head (tail (tail (stream-filter odd? integers))))
                                 => 5
```

The following examples are not intended to illustrate good programming
style, as `delay`, `force`, and `delay-force` are mainly intended
for programs written in the functional style.
However, they do illustrate the property that only one value is
computed for a promise, no matter how many times it is forced.

```scheme
(define count 0)
(define p
  (delay (begin (set! count (+ count 1))
                (if (> count x)
                    count
                    (force p)))))
(define x 5)
p                       =>  a promise
(force p)               =>  6
p                       =>  a promise, still
(begin (set! x 10)
       (force p))       =>  6
```

Various extensions to this semantics of `delay`, `force` and
`delay-force` are supported in some implementations:

- Calling `force` on an object that is not a promise may simply
  return the object.
- It may be the case that there is no means by which a promise can be
  operationally distinguished from its forced value. That is, expressions
  like the following may evaluate to either `#t` or to `#f`,
  depending on the implementation:

  ```scheme
  (eqv? (delay 1) 1)            =>  unspecified
  (pair? (delay (cons 1 2)))    =>  unspecified
  ```
- Implementations may implement “implicit forcing,” where
  the value of a promise is forced by procedures
  that operate only on arguments of a certain type, like `cdr`
  and `*`. However, procedures that operate uniformly on their
  arguments, like `list`, must not force them.

  ```scheme
  (+ (delay (* 3 7)) 13)    =>  unspecified
  (car
    (list (delay (* 3 7)) 13))      => a promise
  ```

<a id="promise"></a>
**`(promise? obj)`** — lazy library procedure

The `promise?` procedure returns
`#t` if its argument is a promise, and `#f` otherwise. Note
that promises are not necessarily disjoint from other Scheme types such
as procedures.

<a id="make-promise"></a>
**`(make-promise obj)`** — lazy library procedure

The `make-promise` procedure returns a promise which, when forced, will return
*obj*. It is similar to `delay`, but does not delay
its argument: it is a procedure rather than syntax.
If *obj* is already a promise, it is returned.

### Dynamic bindings

The **dynamic extent** of a procedure call is the time between
when it is initiated and when it returns. In Scheme, `call-with-current-continuation` (section [Control features](#continuations)) allows
reentering a dynamic extent after its procedure call has returned.
Thus, the dynamic extent of a call might not be a single, continuous time
period.

This sections introduces **parameter objects**, which can be
bound to new values for the duration of a dynamic extent. The set of
all parameter bindings at a given time is called the **dynamic
 environment**.

<a id="make-parameter"></a>
**`(make-parameter init)`** — procedure  
**`(make-parameter init converter)`** — procedure

Returns a newly allocated parameter object,
which is a procedure that accepts zero arguments and
returns the value associated with the parameter object.
Initially, this value is the value of
`(converter init)`, or of *init*
if the conversion procedure *converter* is not specified.
The associated value can be temporarily changed
using `parameterize`, which is described below.

The effect of passing arguments to a parameter object is
implementation-dependent.

**`(parameterize ((⟨param⟩₁ ⟨value⟩₁) …)`** — syntax

<a id="parameterize"></a>

*Syntax:*
Both ⟨param⟩₁ and ⟨value⟩₁ are expressions.

It is an error if the value of any ⟨param⟩ expression is not a parameter object.
*Semantics:*
A `parameterize` expression is used to change the values returned by
specified parameter objects during the evaluation of the body.

The ⟨param⟩ and ⟨value⟩ expressions
are evaluated in an unspecified order. The ⟨body⟩ is
evaluated in a dynamic environment in which calls to the
parameters return the results of passing the corresponding values
to the conversion procedure specified when the parameters were created.
Then the previous values of the parameters are restored without passing
them to the conversion procedure.
The results of the last
expression in the ⟨body⟩ are returned as the results of the entire
`parameterize` expression.

> **Note:** If the conversion procedure is not idempotent, the results of
> `(parameterize ((x (x))) ...)`,
> which appears to bind the parameter *x* to its current value,
> might not be what the user expects.

If an implementation supports multiple threads of execution, then
`parameterize` must not change the associated values of any parameters
in any thread other than the current thread and threads created
inside ⟨body⟩.

Parameter objects can be used to specify configurable settings for a
computation without the need to pass the value to every
procedure in the call chain explicitly.

```scheme
(define radix
  (make-parameter
   10
   (lambda (x)
     (if (and (exact-integer? x) (<= 2 x 16))
         x
         (error "invalid radix")))))

(define (f n) (number->string n (radix)))

(f 12)                                         => "12"
(parameterize ((radix 2))
  (f 12))                                      => "1100"
(f 12)                                         => "12"

(radix 16)                                     => unspecified

(parameterize ((radix 0))
  (f 12))                                      => error
```

### Exception handling

**`(guard (⟨variable⟩`** — syntax

<a id="guard"></a>

*Syntax:*
Each ⟨cond clause⟩ is as in the specification of `cond`.

*Semantics:*
The ⟨body⟩ is evaluated with an exception
handler that binds the raised object (see `raise` in section [Exceptions](#exceptionsection))
to ⟨variable⟩ and, within the scope of
that binding, evaluates the clauses as if they were the clauses of a
`cond` expression. That implicit `cond` expression is evaluated with the
continuation and dynamic environment of the `guard` expression. If every
⟨cond clause⟩'s ⟨test⟩ evaluates to `#f` and there
is no else clause, then
`raise-continuable` is invoked on the raised object within the dynamic
environment of the original call to `raise`
or `raise-continuable`, except that the current
exception handler is that of the `guard` expression.

See section [Exceptions](#exceptionsection) for a more complete discussion of
exceptions.

```scheme
(guard (condition
         ((assq 'a condition) => cdr)
         ((assq 'b condition)))
  (raise (list (cons 'a 42))))
  => 42

(guard (condition
         ((assq 'a condition) => cdr)
         ((assq 'b condition)))
  (raise (list (cons 'b 23))))
  => (b . 23)
```

### Quasiquotation

<a id="quasiquotesection"></a>

<a id="quasiquote"></a>
**`(quasiquote ⟨qq template⟩)`** — syntax  
**`⟨qq template⟩`** — syntax  
**`unquote`** — auxiliary syntax  
**`,`** — auxiliary syntax  
**`unquote-splicing`** — auxiliary syntax  
**`,@`** — auxiliary syntax

“Quasiquote” expressions are useful
for constructing a list or vector structure when some but not all of the
desired structure is known in advance. If no
commas appear within the ⟨qq template⟩, the result of
evaluating
`⟨qq template⟩ is equivalent to the result of evaluating
'⟨qq template⟩. If a comma<a id="x-4"></a> appears within the
⟨qq template⟩, however, the expression following the comma is
evaluated (“unquoted”) and its result is inserted into the structure
instead of the comma and the expression. If a comma appears followed
without intervening whitespace by a commercial at-sign (@),<a id="x-5"></a> then it is an error if the following
expression does not evaluate to a list; the opening and closing parentheses
of the list are then “stripped away” and the elements of the list are
inserted in place of the comma at-sign expression sequence. A comma
at-sign normally appears only within a list or vector ⟨qq template⟩.

> **Note:** In order to unquote an identifier beginning with `@`, it is necessary
> to use either an explicit `unquote` or to put whitespace after the comma,
> to avoid colliding with the comma at-sign sequence.

```scheme
`(list ,(+ 1 2) 4)    =>  (list 3 4)
(let ((name 'a)) `(list ,name ',name))
          =>  (list a (quote a))
`(a ,(+ 1 2) ,@(map abs '(4 -5 6)) b)
          =>  (a 3 4 5 6 b)
`((foo ,(- 10 3)) ,@(cdr '(c)) . ,(car '(cons)))
          =>  ((foo 7) . cons)
`#(10 5 ,(sqrt 4) ,@(map sqrt '(16 9)) 8)
          =>  #(10 5 2 4 3 8)
(let ((foo '(foo bar)) (@baz 'baz))
  `(list ,@foo , @baz))
          =>  (list foo bar baz)
```

Quasiquote expressions can be nested. Substitutions are made only for
unquoted components appearing at the same nesting level
as the outermost quasiquote. The nesting level increases by one inside
each successive quasiquotation, and decreases by one inside each
unquotation.

```scheme
`(a `(b ,(+ 1 2) ,(foo ,(+ 1 3) d) e) f)
          =>  (a `(b ,(+ 1 2) ,(foo 4 d) e) f)
(let ((name1 'x)
      (name2 'y))
  `(a `(b ,,name1 ,',name2 d) e))
          =>  (a `(b ,x ,'y d) e)
```

A quasiquote expression may return either newly allocated, mutable objects or
literal structure for any structure that is constructed at run time
during the evaluation of the expression. Portions that do not need to
be rebuilt are always literal. Thus,

```scheme
(let ((a 3)) `((1 2) ,a ,4 ,'five 6))
```

may be treated as equivalent to either of the following expressions:

```scheme
`((1 2) 3 4 five 6)

(let ((a 3))
  (cons '(1 2)
        (cons a (cons 4 (cons 'five '(6))))))
```

However, it is not equivalent to this expression:

```scheme
(let ((a 3)) (list (list 1 2) a 4 'five 6))
```

The two notations
 `⟨qq template⟩ and `(quasiquote ⟨qq template⟩)`
 are identical in all respects.
 `,⟨expression⟩` is identical to `(unquote ⟨expression⟩)`,
 and
 `,@⟨expression⟩` is identical to `(unquote-splicing ⟨expression⟩)`.
The `write` procedure may output either format.
<a id="x-6"></a>

```scheme
(quasiquote (list (unquote (+ 1 2)) 4))
          =>  (list 3 4)
'(quasiquote (list (unquote (+ 1 2)) 4))
          =>  `(list ,(+ 1 2) 4)
     i.e., (quasiquote (list (unquote (+ 1 2)) 4))
```

It is an error if any of the identifiers `quasiquote`, `unquote`,
or `unquote-splicing` appear in positions within a ⟨qq template⟩
otherwise than as described above.

### Case-lambda

<a id="caselambdasection"></a>

<a id="case-lambda"></a>
**`(case-lambda ⟨clause⟩ …)`** — case-lambda library syntax

*Syntax:*
Each ⟨clause⟩ is of the form
(⟨formals⟩ ⟨body⟩),
where ⟨formals⟩ and ⟨body⟩ have the same syntax
as in a `lambda` expression.

*Semantics:*
A `case-lambda` expression evaluates to a procedure that accepts
a variable number of arguments and is lexically scoped in the same
manner as a procedure resulting from a `lambda` expression. When the procedure
is called, the first ⟨clause⟩ for which the arguments agree
with ⟨formals⟩ is selected, where agreement is specified as for
the ⟨formals⟩ of a `lambda` expression. The variables of ⟨formals⟩ are
bound to fresh locations, the values of the arguments are stored in those
locations, the ⟨body⟩ is evaluated in the extended environment,
and the results of ⟨body⟩ are returned as the results of the
procedure call.

It is an error for the arguments not to agree with
the ⟨formals⟩ of any ⟨clause⟩.

```scheme
(define range
  (case-lambda
   ((e) (range 0 e))
   ((b e) (do ((r '() (cons e r))
               (e (- e 1) (- e 1)))
              ((< e b) r)))))

(range 3)      => (0 1 2)
(range 3 5)    => (3 4)
```

## Macros

<a id="macrosection"></a>

Scheme programs can define and use new derived expression types,
 called *macros*.<a id="macro"></a>
Program-defined expression types have the syntax

```scheme
(⟨keyword⟩ ⟨datum⟩ ...)
```

where ⟨keyword⟩ is an identifier that uniquely determines the
expression type. This identifier is called the *syntactic
keyword*, or simply *keyword*, of the macro. The
number of the ⟨datum⟩s, and their syntax, depends on the
expression type.

Each instance of a macro is called a *use*
of the macro.
The set of rules that specifies
how a use of a macro is transcribed into a more primitive expression
is called the *transformer*
of the macro.

The macro definition facility consists of two parts:

- A set of expressions used to establish that certain identifiers
  are macro keywords, associate them with macro transformers, and control
  the scope within which a macro is defined, and
- a pattern language for specifying macro transformers.

The syntactic keyword of a macro can shadow variable bindings, and local
variable bindings can shadow syntactic bindings.
Two mechanisms are provided to prevent unintended conflicts:

- If a macro transformer inserts a binding for an identifier
  (variable or keyword), the identifier will in effect be renamed
  throughout its scope to avoid conflicts with other identifiers.
  Note that a global variable definition may or may not introduce a binding;
  see section [Variable definitions](#defines).
- If a macro transformer inserts a free reference to an
  identifier, the reference refers to the binding that was visible
  where the transformer was specified, regardless of any local
  bindings that surround the use of the macro.

In consequence, all macros
defined using the pattern language are “hygienic” and “referentially
transparent” and thus preserve Scheme's lexical scoping. [[Kohlbecker86](#cite-kohlbecker86), [hygienic](#cite-hygienic), [Bawden88](#cite-bawden88), [macrosthatwork](#cite-macrosthatwork), [syntacticabstraction](#cite-syntacticabstraction)]
<a id="hygienic"></a><a id="referentially-transparent"></a>

Implementations may provide macro facilities of other types.

### Binding constructs for syntactic keywords

<a id="bindsyntax"></a>

The `let-syntax` and `letrec-syntax` binding constructs are
analogous to `let` and `letrec`, but they bind
syntactic keywords to macro transformers instead of binding variables
to locations that contain values. Syntactic keywords can also be
bound globally or locally with `define-syntax`;
see section [define-syntax](#define-syntax).

<a id="let-syntax"></a>
**`(let-syntax ⟨bindings⟩ ⟨body⟩)`** — syntax

*Syntax:*
⟨Bindings⟩ has the form

```scheme
((⟨keyword⟩ ⟨transformer spec⟩) ...)
```

Each ⟨keyword⟩ is an identifier,
each ⟨transformer spec⟩ is an instance of `syntax-rules`, and
⟨body⟩ is a sequence of zero or more definitions followed
by one or more expressions. It is an error
for a ⟨keyword⟩ to appear more than once in the list of keywords
being bound.

*Semantics:*
The ⟨body⟩ is expanded in the syntactic environment
obtained by extending the syntactic environment of the
`let-syntax` expression with macros whose keywords are
the ⟨keyword⟩s, bound to the specified transformers.
Each binding of a ⟨keyword⟩ has ⟨body⟩ as its region.

```scheme
(let-syntax ((given-that (syntax-rules ()
                     ((given-that test stmt1 stmt2 ...)
                      (if test
                          (begin stmt1
                                 stmt2 ...))))))
  (let ((if #t))
    (given-that if (set! if 'now))
    if))                             =>  now

(let ((x 'outer))
  (let-syntax ((m (syntax-rules () ((m) x))))
    (let ((x 'inner))
      (m))))                         =>  outer
```

<a id="letrec-syntax"></a>
**`(letrec-syntax ⟨bindings⟩ ⟨body⟩)`** — syntax

*Syntax:*
Same as for `let-syntax`.

*Semantics:*
 The ⟨body⟩ is expanded in the syntactic environment obtained by
extending the syntactic environment of the `letrec-syntax`
expression with macros whose keywords are the
⟨keyword⟩s, bound to the specified transformers.
Each binding of a ⟨keyword⟩ has the ⟨transformer spec⟩s
as well as the ⟨body⟩ within its region,
so the transformers can
transcribe expressions into uses of the macros
introduced by the `letrec-syntax` expression.

```scheme
(letrec-syntax
    ((my-or (syntax-rules ()
              ((my-or) #f)
              ((my-or e) e)
              ((my-or e1 e2 ...)
               (let ((temp e1))
                 (if temp
                     temp
                     (my-or e2 ...)))))))
  (let ((x #f)
        (y 7)
        (temp 8)
        (let odd?)
        (if even?))
    (my-or x
           (let temp)
           (if y)
           y)))          =>  7
```

### Pattern language

<a id="patternlanguage"></a>

A ⟨transformer spec⟩ has one of the following forms:

**`(syntax-rules (⟨pattern literal⟩ …)`** — syntax  
**`(syntax-rules ⟨ellipsis⟩ (⟨pattern literal⟩ …)`** — syntax  
**`_`** — auxiliary syntax  
**`…`** — auxiliary syntax

<a id="x-7"></a>

*Syntax:*
It is an error if any of the ⟨pattern literal⟩s, or the ⟨ellipsis⟩ in the second form,
is not an identifier.
It is also an error if
⟨syntax rule⟩ is not of the form

```scheme
(⟨pattern⟩ ⟨template⟩)
```

The ⟨pattern⟩ in a ⟨syntax rule⟩ is a list ⟨pattern⟩
whose first element is an identifier.

A ⟨pattern⟩ is either an identifier, a constant, or one of the
following

```scheme
(⟨pattern⟩ ...)
(⟨pattern⟩ ⟨pattern⟩ ... . ⟨pattern⟩)
(⟨pattern⟩ ... ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩ ...)
(⟨pattern⟩ ... ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩ ...
  . ⟨pattern⟩)
#(⟨pattern⟩ ...)
#(⟨pattern⟩ ... ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩ ...)
```

and a ⟨template⟩ is either an identifier, a constant, or one of the following

```scheme
(⟨element⟩ ...)
(⟨element⟩ ⟨element⟩ ... . ⟨template⟩)
(⟨ellipsis⟩ ⟨template⟩)
#(⟨element⟩ ...)
```

where an ⟨element⟩ is a ⟨template⟩ optionally
followed by an ⟨ellipsis⟩.
An ⟨ellipsis⟩ is the identifier specified in the second form
of `syntax-rules`, or the default identifier `...`
(three consecutive periods) otherwise.

*Semantics:* An instance of `syntax-rules` produces a new macro
transformer by specifying a sequence of hygienic rewrite rules. A use
of a macro whose keyword is associated with a transformer specified by
`syntax-rules` is matched against the patterns contained in the
⟨syntax rule⟩s, beginning with the leftmost ⟨syntax rule⟩.
When a match is found, the macro use is transcribed hygienically
according to the template.

An identifier appearing within a ⟨pattern⟩ can be an underscore
(`_`), a literal identifier listed in the list of ⟨pattern literal⟩s,
or the ⟨ellipsis⟩.
All other identifiers appearing within a ⟨pattern⟩ are
*pattern variables*.

The keyword at the beginning of the pattern in a
⟨syntax rule⟩ is not involved in the matching and
is considered neither a pattern variable nor a literal identifier.

Pattern variables match arbitrary input elements and
are used to refer to elements of the input in the template.
It is an error for the same pattern variable to appear more than once in a
⟨pattern⟩.

Underscores also match arbitrary input elements but are not pattern variables
and so cannot be used to refer to those elements. If an underscore appears
in the ⟨pattern literal⟩s list, then that takes precedence and
underscores in the ⟨pattern⟩ match as literals.
Multiple underscores can appear in a ⟨pattern⟩.

Identifiers that appear in `(⟨pattern literal⟩ …)` are
interpreted as literal
identifiers to be matched against corresponding elements of the input.
An element in the input matches a literal identifier if and only if it is an
identifier and either both its occurrence in the macro expression and its
occurrence in the macro definition have the same lexical binding, or
the two identifiers are the same and both have no lexical binding.

A subpattern followed by ⟨ellipsis⟩ can match zero or more elements of
the input, unless ⟨ellipsis⟩ appears in the ⟨pattern literal⟩s, in which
case it is matched as a literal.

More formally, an input expression $E$ matches a pattern $P$ if and only if:

- $P$ is an underscore (`_`).
- $P$ is a non-literal identifier; or
- $P$ is a literal identifier and $E$ is an identifier with the same
   binding; or
- $P$ is a list `($P_1$ $\dots$ $P_n$)` and $E$ is a
   list of $n$
   elements that match $P_1$ through $P_n$, respectively; or
- $P$ is an improper list
   `($P_1$ $P_2$ $\dots$ $P_n$ . $P_{n+1}$)`
   and $E$ is a list or
   improper list of $n$ or more elements that match $P_1$ through $P_n$,
   respectively, and whose $n$th tail matches $P_{n+1}$; or
- $P$ is of the form
   `($P_1$ $\dots$ $P_k$ $P_e$ ⟨ellipsis⟩ $P_{m+1}$ … $P_n$)`
   where $E$ is
   a proper list of $n$ elements, the first $k$ of which match
   $P_1$ through $P_k$, respectively,
   whose next $m-k$ elements each match $P_e$,
   whose remaining $n-m$ elements match $P_{m+1}$ through $P_n$; or
- $P$ is of the form
   `($P_1$ $\dots$ $P_k$ $P_{e}$ ⟨ellipsis⟩ $P_{m+1}$ … $P_n$ . $P_x$)`
   where $E$ is
   a list or improper list of $n$ elements, the first $k$ of which match
   $P_1$ through $P_k$,
   whose next $m-k$ elements each match $P_e$,
   whose remaining $n-m$ elements match $P_{m+1}$ through $P_n$,
   and whose $n$th and final cdr matches $P_x$; or
- $P$ is a vector of the form `#($P_1$ $\dots$ $P_n$)`
   and $E$ is a vector
   of $n$ elements that match $P_1$ through $P_n$; or
- $P$ is of the form
   `#($P_1$ $\dots$ $P_k$ $P_{e}$ ⟨ellipsis⟩ $P_{m+1}$ … $P_n$)`
   where $E$ is a vector of $n$
   elements the first $k$ of which match $P_1$ through $P_k$,
   whose next $m-k$ elements each match $P_e$,
   and whose remaining $n-m$ elements match $P_{m+1}$ through $P_n$; or
- $P$ is a constant and $E$ is equal to $P$ in the sense of
   the `equal?` procedure.

It is an error to use a macro keyword, within the scope of its
binding, in an expression that does not match any of the patterns.

When a macro use is transcribed according to the template of the
matching ⟨syntax rule⟩, pattern variables that occur in the
template are replaced by the elements they match in the input.
Pattern variables that occur in subpatterns followed by one or more
instances of the identifier
⟨ellipsis⟩ are allowed only in subtemplates that are
followed by as many instances of ⟨ellipsis⟩.
They are replaced in the
output by all of the elements they match in the input, distributed as
indicated. It is an error if the output cannot be built up as
specified.

Identifiers that appear in the template but are not pattern variables
or the identifier
⟨ellipsis⟩ are inserted into the output as literal identifiers. If a
literal identifier is inserted as a free identifier then it refers to the
binding of that identifier within whose scope the instance of
`syntax-rules` appears.
If a literal identifier is inserted as a bound identifier then it is
in effect renamed to prevent inadvertent captures of free identifiers.

A template of the form
`(⟨ellipsis⟩ ⟨template⟩)` is identical to ⟨template⟩,
except that
ellipses within the template have no special meaning.
That is, any ellipses contained within ⟨template⟩ are
treated as ordinary identifiers.
In particular, the template `(⟨ellipsis⟩ ⟨ellipsis⟩)` produces
a single ⟨ellipsis⟩.
This allows syntactic abstractions to expand into code containing
ellipses.

```scheme
(define-syntax be-like-begin
  (syntax-rules ()
    ((be-like-begin name)
     (define-syntax name
       (syntax-rules ()
         ((name expr (... ...))
          (begin expr (... ...))))))))

(be-like-begin sequence)
(sequence 1 2 3 4)   => 4
```

As an example, if `let` and `cond` are defined as in
section [Derived expression types](#derivedsection) then they are hygienic (as required) and
the following is not an error.

```scheme
(let ((=> #f))
  (cond (#t => 'ok)))             => ok
```

The macro transformer for `cond` recognizes `=>`
as a local variable, and hence an expression, and not as the
base identifier `=>`, which the macro transformer treats
as a syntactic keyword. Thus the example expands into

```scheme
(let ((=> #f))
  (if #t (begin => 'ok)))
```

instead of

```scheme
(let ((=> #f))
  (let ((temp #t))
    (if temp ('ok temp))))
```

which would result in an invalid procedure call.

### Signaling errors in macro transformers

**`(syntax-error ⟨message⟩ ⟨args⟩ …)`** — syntax

<a id="syntax-error"></a>

`syntax-error` behaves similarly to `error` ([Exceptions](#exceptionsection)) except that implementations
with an expansion pass separate from evaluation should signal an error
as soon as `syntax-error` is expanded. This can be used as
a `syntax-rules` ⟨template⟩ for a ⟨pattern⟩ that is
an invalid use of the macro, which can provide more descriptive error
messages. ⟨message⟩ is a string literal, and ⟨args⟩
arbitrary expressions providing additional information.
Applications cannot count on being able to catch syntax errors with
exception handlers or guards.

```scheme
(define-syntax simple-let
  (syntax-rules ()
    ((simple-let ((x . y) val) body1 body2 ...)
     (syntax-error "expected an identifier" (x . y)))
    ((simple-let (name val) body1 body2 ...)
```


# Program structure

<a id="programchapter"></a>

## Programs

A Scheme program consists of
one or more import declarations followed by a sequence of
expressions and definitions.
Import declarations specify the libraries on which a program or library depends;
a subset of the identifiers exported by the libraries are made available to
the program.
Expressions are described in chapter [Expressions](#expressionchapter).
Definitions are either variable definitions, syntax definitions, or
record-type definitions, all of which are explained in this chapter.
They are valid in some, but not all, contexts where expressions
are allowed, specifically at the outermost level of a ⟨program⟩
and at the beginning of a ⟨body⟩.
<a id="definition"></a>

At the outermost level of a program, `(begin ⟨expression or definition⟩₁ …)` is
equivalent to the sequence of expressions and definitions
in the `begin`.
Similarly, in a ⟨body⟩, `(begin ⟨definition⟩₁ …)` is equivalent
to the sequence ⟨definition⟩₁ ….
Macros can expand into such `begin` forms.
For the formal definition, see [Sequencing](#sequencing).

Import declarations and definitions
cause bindings to be created in the global
environment or modify the value of existing global bindings.
The initial environment of a program is empty,
so at least one import declaration is needed to introduce initial bindings.

Expressions occurring at the outermost level of a program
do not create any bindings. They are
executed in order when the program is
invoked or loaded, and typically perform some kind of initialization.

Programs and libraries are typically stored in files, although
in some implementations they can be entered interactively into a running
Scheme system. Other paradigms are possible.
Implementations which store libraries in files should document the
mapping from the name of a library to its location in the file system.

## Import declarations

<a id="import"></a>

An import declaration takes the following form:

```scheme
(import ⟨import-set⟩ ...)
```

An import declaration provides a way to import identifiers
exported by a library. Each ⟨import set⟩ names a set of bindings
from a library and possibly specifies local names for the
imported bindings. It takes one of the following forms:

- `⟨library name⟩`
- `(only ⟨import set⟩ ⟨identifier⟩ …)`
- `(except ⟨import set⟩ ⟨identifier⟩ …)`
- `(prefix ⟨import set⟩ ⟨identifier⟩)`
- `(rename ⟨import set⟩\

  (⟨identifier⟩₁ ⟨identifier⟩₂) …)`

In the first form, all of the identifiers in the named library's export
clauses are imported with the same names (or the exported names if
exported with `rename`). The additional ⟨import set⟩
forms modify this set as follows:

- `only` produces a subset of the given
   ⟨import set⟩ including only the listed identifiers (after any
   renaming). It is an error if any of the listed identifiers are
   not found in the original set.
- `except` produces a subset of the given
   ⟨import set⟩, excluding the listed identifiers (after any
   renaming). It is an error if any of the listed identifiers are not
   found in the original set.
- `rename` modifies the given ⟨import set⟩,
   replacing each instance of ⟨identifier⟩₁ with
   ⟨identifier⟩₂. It is an error if any of the listed
   ⟨identifier⟩₁s are not found in the original set.
- `prefix` automatically renames all identifiers in
   the given ⟨import set⟩, prefixing each with the specified
   ⟨identifier⟩.

In a program or library declaration, it is an error to import the same
identifier more than once with different bindings, or to redefine or
mutate an imported binding with a definition
or with `set!`, or to refer to an identifier before it is imported.
However, a REPL should permit these actions.

## Variable definitions

<a id="defines"></a>
<a id="variable-definition"></a>

A variable definition binds one or more identifiers and specifies an initial
value for each of them.
The simplest kind of variable definition
takes one of the following forms:<a id="define"></a>

- `(define ⟨variable⟩ ⟨expression⟩)`
- `(define (⟨variable⟩ ⟨formals⟩) ⟨body⟩)`

  ⟨Formals⟩ are either a
  sequence of zero or more variables, or a sequence of one or more
  variables followed by a space-delimited period and another variable (as
  in a lambda expression). This form is equivalent to

  ```scheme
  (define ⟨variable⟩
    (lambda (⟨formals⟩) ⟨body⟩)).
  ```
- `(define (⟨variable⟩ . ⟨formal⟩) ⟨body⟩)`

  ⟨Formal⟩ is a single
  variable. This form is equivalent to

  ```scheme
  (define ⟨variable⟩
    (lambda ⟨formal⟩ ⟨body⟩)).
  ```

### Top level definitions

At the outermost level of a program, a definition

```scheme
(define ⟨variable⟩ ⟨expression⟩)
```

has essentially the same effect as the assignment expression

```scheme
(set! ⟨variable⟩ ⟨expression⟩)
```

if ⟨variable⟩ is bound to a non-syntax value. However, if
⟨variable⟩ is not bound,
or is a syntactic keyword,
then the definition will bind
⟨variable⟩ to a new location before performing the assignment,
whereas it would be an error to perform a `set!` on an
unbound variable.

```scheme
(define add3
  (lambda (x) (+ x 3)))
(add3 3)                              =>  6
(define first car)
(first '(1 2))                        =>  1
```

### Internal definitions

<a id="internaldefines"></a>

Definitions can occur at the
beginning of a ⟨body⟩ (that is, the body of a `lambda`,
`let`, `let*`, `letrec`, `letrec*`,
`let-values`, `let*-values`, `let-syntax`, `letrec-syntax`,
`parameterize`, `guard`, or `case-lambda`). Note that
such a body might not be apparent until after expansion of other syntax.
Such definitions are known as *internal definitions* as opposed to the global definitions described above.
The variables defined by internal definitions are local to the
⟨body⟩. That is, ⟨variable⟩ is bound rather than assigned,
and the region of the binding is the entire ⟨body⟩. For example,

```scheme
(let ((x 5))
  (define foo (lambda (y) (bar x y)))
  (define bar (lambda (a b) (+ (* a b) a)))
  (foo (+ x 3)))                  =>  45
```

An expanded ⟨body⟩ containing internal definitions
can always be
converted into a completely equivalent `letrec*` expression. For
example, the `let` expression in the above example is equivalent
to

```scheme
(let ((x 5))
  (letrec* ((foo (lambda (y) (bar x y)))
            (bar (lambda (a b) (+ (* a b) a))))
    (foo (+ x 3))))
```

Just as for the equivalent `letrec*` expression, it is an error if it is not
possible to evaluate each ⟨expression⟩ of every internal
definition in a ⟨body⟩ without assigning or referring to
the value of the corresponding ⟨variable⟩ or the ⟨variable⟩
of any of the definitions that follow it in ⟨body⟩.

It is an error to define the same identifier more than once in the
same ⟨body⟩.

Wherever an internal definition can occur,
`(begin ⟨definition⟩₁ …)`
is equivalent to the sequence of definitions
that form the body of the `begin`.

### Multiple-value definitions

Another kind of definition is provided by `define-values`,
which creates multiple definitions from a single
expression returning multiple values.
It is allowed wherever `define` is allowed.

<a id="define-values"></a>
**`(define-values ⟨formals⟩ ⟨expression⟩)`** — syntax

It is an error if a variable appears more than once in the set of ⟨formals⟩.

⟨Expression⟩ is evaluated, and the ⟨formals⟩ are bound
to the return values in the same way that the ⟨formals⟩ in a
`lambda` expression are matched to the arguments in a procedure
call.

```scheme
(define-values (x y) (exact-integer-sqrt 17))
(list x y)   => (4 1)

(let ()
  (define-values (x y) (values 1 2))
  (+ x y))       => 3
```

## Syntax definitions

<a id="syntax-definition"></a>
Syntax definitions have this form:<a id="define-syntax"></a>

`(define-syntax ⟨keyword⟩ ⟨transformer spec⟩)`

⟨Keyword⟩ is an identifier, and
the ⟨transformer spec⟩ is an instance of `syntax-rules`.
Like variable definitions, syntax definitions can appear at the outermost level or
nested within a `body`.

If the `define-syntax` occurs at the outermost level, then the global
syntactic environment is extended by binding the
⟨keyword⟩ to the specified transformer, but previous expansions
of any global binding for ⟨keyword⟩ remain unchanged.
Otherwise, it is an **internal syntax definition**, and is local to the
⟨body⟩ in which it is defined.
Any use of a syntax keyword before its corresponding definition is an error.
In particular, a use that precedes an inner definition will not apply an outer
definition.

```scheme
(let ((x 1) (y 2))
  (define-syntax swap!
    (syntax-rules ()
      ((swap! a b)
       (let ((tmp a))
         (set! a b)
         (set! b tmp)))))
  (swap! x y)
  (list x y))                  => (2 1)
```

Macros can expand into definitions in any context that permits
them. However, it is an error for a definition to define an
identifier whose binding has to be known in order to determine the meaning of the
definition itself, or of any preceding definition that belongs to the
same group of internal definitions. Similarly, it is an error for an
internal definition to define an identifier whose binding has to be known
in order
to determine the boundary between the internal definitions and the
expressions of the body it belongs to. For example, the following are
errors:

```scheme
(define define 3)

(begin (define begin list))

(let-syntax
    ((foo (syntax-rules ()
            ((foo (proc args ...) body ...)
             (define proc
               (lambda (args ...)
                 body ...))))))
  (let ((x 3))
    (foo (plus x y) (+ x y))
    (define foo x)
    (plus foo x)))
```

## Record-type definitions

<a id="usertypes"></a>

Like other definitions, they can appear either at the outermost level or in a body.
The values of a record type are called **records** and are
aggregations of zero or more **fields**, each of which holds a single location.
A predicate, a constructor, and field accessors and
mutators are defined for each record type.

<a id="define-record-type"></a>
**`(define-record-type ⟨name⟩`** — syntax

⟨name⟩ and ⟨pred⟩ are identifiers.
The ⟨constructor⟩ is of the form

```scheme
(⟨constructor name⟩ ⟨field name⟩ ...)
```

and each ⟨field⟩ is either of the form

```scheme
(⟨field name⟩ ⟨accessor name⟩)
```

or of the form

```scheme
(⟨field name⟩ ⟨accessor name⟩ ⟨modifier name⟩)
```

It is an error for the same identifier to occur more than once as a
field name.
It is also an error for the same identifier to occur more than once
as an accessor or mutator name.

The `define-record-type` construct is generative: each use creates a new record
type that is distinct from all existing types, including Scheme's
predefined types and other record types — even record types of
the same name or structure.

An instance of `define-record-type` is equivalent to the following
definitions:

- ⟨name⟩ is bound to a representation of the record type itself.
  This may be a run-time object or a purely syntactic representation.
  The representation is not utilized in this report, but it serves as a
  means to identify the record type for use by further language extensions.
- ⟨constructor name⟩ is bound to a procedure that takes as
   many arguments as there are ⟨field name⟩s in the
   `(⟨constructor name⟩ …)` subexpression and returns a
   new record of type ⟨name⟩. Fields whose names are listed with
   ⟨constructor name⟩ have the corresponding argument as their
   initial value. The initial values of all other fields are
   unspecified. It is an error for a field name to appear in
   ⟨constructor⟩ but not as a ⟨field name⟩.
- ⟨pred⟩ is bound to a predicate that returns `#t` when given a
   value returned by the procedure bound to ⟨constructor name⟩ and `#f` for
   everything else.
- Each ⟨accessor name⟩ is bound to a procedure that takes a record of
   type ⟨name⟩ and returns the current value of the corresponding
   field. It is an error to pass an accessor a value which is not a
   record of the appropriate type.
- Each ⟨modifier name⟩ is bound to a procedure that takes a record of
   type ⟨name⟩ and a value which becomes the new value of the
   corresponding field; an unspecified value is returned. It is an
   error to pass a modifier a first argument which is not a record of
   the appropriate type.

For instance, the following record-type definition

```scheme
(define-record-type <pare>
  (kons x y)
  pare?
  (x kar set-kar!)
  (y kdr))
```

defines `kons` to be a constructor, `kar` and `kdr`
to be accessors, `set-kar!` to be a modifier, and `pare?`
to be a predicate for instances of `<pare>`.

```scheme
  (pare? (kons 1 2))          => #t
  (pare? (cons 1 2))          => #f
  (kar (kons 1 2))            => 1
  (kdr (kons 1 2))            => 2
  (let ((k (kons 1 2)))
    (set-kar! k 3)
    (kar k))                  => 3
```

## Libraries

<a id="libraries"></a>

Libraries provide a way to organize Scheme programs into reusable parts
with explicitly defined interfaces to the rest of the program. This
section defines the notation and semantics for libraries.

### Library Syntax

A library definition takes the following form:
<a id="define-library"></a>

```scheme
(define-library ⟨library name⟩
  ⟨library declaration⟩ ...)
```

⟨library name⟩ is a list whose members are identifiers and exact non-negative integers. It is used to
identify the library uniquely when importing from other programs or
libraries.
Libraries whose first identifier is `scheme` are reserved for use by this
report and future versions of this report.
Libraries whose first identifier is `srfi` are reserved for libraries
implementing Scheme Requests for Implementation.
It is inadvisable, but not an error, for identifiers in library names to
contain any of the characters `| \ ? * < " : > + [ ] /`
or control characters after escapes are expanded.

<a id="librarydeclarations"></a>
A ⟨library declaration⟩ is any of:

- `(export ⟨export spec⟩ …)`
- `(import ⟨import set⟩ …)`
- `(begin ⟨command or definition⟩ …)`
- `(include ⟨filename⟩₁ ⟨filename⟩₂ …)`
- `(include-ci ⟨filename⟩₁ ⟨filename⟩₂ …)`
- `(include-library-declarations ⟨filename⟩₁ ⟨filename⟩₂ …)`
- `(cond-expand ⟨ce-clause⟩₁ ⟨ce-clause⟩₂ …)`

An `export` declaration specifies a list of identifiers which
can be made visible to other libraries or programs.
An ⟨export spec⟩ takes one of the following forms:

- ⟨identifier⟩
- `(rename ⟨identifier⟩₁ ⟨identifier⟩₂)`

In an ⟨export spec⟩, an ⟨identifier⟩ names a single
binding defined within or imported into the library, where the
external name for the export is the same as the name of the binding
within the library. A `rename` spec exports the binding
defined within or imported into the library and named by
⟨identifier⟩₁ in each
`(⟨identifier⟩₁ ⟨identifier⟩₂)` pairing,
using ⟨identifier⟩₂ as the external name.

An `import` declaration provides a way to import the identifiers
exported by another library. It has the same syntax and semantics as
an import declaration used in a program or at the REPL (see section [import](#import)).

The `begin`, `include`, and `include-ci` declarations are
used to specify the body of
the library. They have the same syntax and semantics as the corresponding
expression types.
This form of `begin` is analogous to, but not the same as, the
two types of `begin` defined in section [Sequencing](#sequencing).

The `include-library-declarations` declaration is similar to
`include` except that the contents of the file are spliced directly into the
current library definition. This can be used, for example, to share the
same `export` declaration among multiple libraries as a simple
form of library interface.

The `cond-expand` declaration has the same syntax and semantics as
the `cond-expand` expression type, except that it expands to
spliced-in library declarations rather than expressions enclosed in `begin`.

One possible implementation of libraries is as follows:
After all `cond-expand` library declarations are expanded, a new
environment is constructed for the library consisting of all
imported bindings. The expressions
from all `begin`, `include` and `include-ci`
library declarations are expanded in that environment in the order in which
they occur in the library.
Alternatively, `cond-expand` and `import` declarations may be processed
in left to right order interspersed with the processing of other
declarations, with the environment growing as imported bindings are
added to it by each `import` declaration.

When a library is loaded, its expressions are executed
in textual order.
If a library's definitions are referenced in the expanded form of a
program or library body, then that library must be loaded before the
expanded program or library body is evaluated. This rule applies
transitively. If a library is imported by more than one program or
library, it may possibly be loaded additional times.

Similarly, during the expansion of a library `(foo)`, if any syntax
keywords imported from another library `(bar)` are needed to expand
the library, then the library `(bar)` must be expanded and its syntax
definitions evaluated before the expansion of `(foo)`.

Regardless of the number of times that a library is loaded, each
program or library that imports bindings from a library must do so from a
single loading of that library, regardless of the number of import
declarations in which it appears.
That is, `(import (only (foo) a))` followed by `(import (only (foo) b))`
has the same effect as `(import (only (foo) a b))`.

### Library example

The following example shows
how a program can be divided into libraries plus a relatively small
main program [[life](#cite-life)].
If the main program is entered into a REPL, it is not necessary to import
the base library.

```scheme
(define-library (example grid)
  (export make rows cols ref each
          (rename put! set!))
  (import (scheme base))
  (begin
    ;; Create an NxM grid.
    (define (make n m)
      (let ((grid (make-vector n)))
        (do ((i 0 (+ i 1)))
            ((= i n) grid)
          (let ((v (make-vector m #false)))
            (vector-set! grid i v)))))
    (define (rows grid)
      (vector-length grid))
    (define (cols grid)
      (vector-length (vector-ref grid 0)))
    ;; Return #false if out of range.
    (define (ref grid n m)
      (and (< -1 n (rows grid))
           (< -1 m (cols grid))
           (vector-ref (vector-ref grid n) m)))
    (define (put! grid n m v)
      (vector-set! (vector-ref grid n) m v))
    (define (each grid proc)
      (do ((j 0 (+ j 1)))
          ((= j (rows grid)))
        (do ((k 0 (+ k 1)))
            ((= k (cols grid)))
          (proc j k (ref grid j k)))))))

(define-library (example life)
  (export life)
  (import (except (scheme base) set!)
          (scheme write)
          (example grid))
  (begin
    (define (life-count grid i j)
      (define (count i j)
        (if (ref grid i j) 1 0))
      (+ (count (- i 1) (- j 1))
         (count (- i 1) j)
         (count (- i 1) (+ j 1))
         (count i (- j 1))
         (count i (+ j 1))
         (count (+ i 1) (- j 1))
         (count (+ i 1) j)
         (count (+ i 1) (+ j 1))))
    (define (life-alive? grid i j)
      (case (life-count grid i j)
        ((3) #true)
        ((2) (ref grid i j))
        (else #false)))
    (define (life-print grid)
      (display "x1B;[1Hx1B;[J")  ; clear vt100
      (each grid
       (lambda (i j v)
         (display (if v "*" " "))
         (when (= j (- (cols grid) 1))
           (newline)))))
    (define (life grid iterations)
      (do ((i 0 (+ i 1))
           (grid0 grid grid1)
           (grid1 (make (rows grid) (cols grid))
                  grid0))
          ((= i iterations))
        (each grid0
         (lambda (j k v)
           (let ((a (life-alive? grid0 j k)))
             (set! grid1 j k a))))
        (life-print grid1)))))

;; Main program.
(import (scheme base)
        (only (example life) life)
        (rename (prefix (example grid) grid-)
                (grid-make make-grid)))

;; Initialize a grid with a glider.
(define grid (make-grid 24 24))
(grid-set! grid 1 1 #true)
(grid-set! grid 2 2 #true)
(grid-set! grid 3 0 #true)
(grid-set! grid 3 1 #true)
(grid-set! grid 3 2 #true)

;; Run for 80 iterations.
(life grid 80)
```

## The REPL

Implementations may provide an interactive session called a
**REPL** (Read-Eval-Print Loop), where import declarations,
expressions and definitions can be
entered and evaluated one at a time. For convenience and ease of use,
the global Scheme environment in a REPL
must not be empty, but must start out with at least the bindings provided by the
base library. This library includes the core syntax of Scheme
and generally useful procedures that manipulate data. For example, the
variable `abs` is bound to a
procedure of one argument that computes the absolute value of a
number, and the variable `+` is bound to a procedure that computes
sums. The full list of `(scheme base)` bindings can be found in
Appendix [Standard Libraries](#stdlibraries).

Implementations may provide an initial REPL environment
which behaves as if all possible variables are bound to locations, most of
which contain unspecified values. Top level REPL definitions in
such an implementation are truly equivalent to assignments,
unless the identifier is defined as a syntax keyword.

An implementation may provide a mode of operation in which the REPL
reads its input from a file. Such a file is not, in general, the same
as a program, because it can contain import declarations in places other than
the beginning.


# Standard procedures

<a id="initialenv"></a>
<a id="builtinchapter"></a>

<a id="initial-environment"></a>
<a id="global-environment"></a>
<a id="procedure"></a>

This chapter describes Scheme's built-in procedures.

The procedures `force`, `promise?`, and `make-promise` are intimately associated
with the expression types `delay` and `delay-force`, and are described
with them in section [force](#force). In the same way, the procedure
`make-parameter` is intimately associated with the expression type
`parameterize`, and is described with it in section [make-parameter](#make-parameter).

A program can use a global variable definition to bind any variable. It may
subsequently alter any such binding by an assignment (see
section [Assignments](#assignment)). These operations do not modify the behavior of
any procedure defined in this report or imported from a library
(see section [Libraries](#libraries)). Altering any global binding that has
not been introduced by a definition has an unspecified effect on the
behavior of the procedures defined in this chapter.

When a procedure is said to return a **newly allocated** object,
it means that the locations in the object are fresh.

## Equivalence predicates

<a id="equivalencesection"></a>

A **predicate** is a procedure that always returns a boolean
value (`#t` or `#f`). An **equivalence predicate** is
the computational analogue of a mathematical equivalence relation; it is
symmetric, reflexive, and transitive. Of the equivalence predicates
described in this section, `eq?` is the finest or most
discriminating, `equal?` is the coarsest, and `eqv?` is
slightly less discriminating than `eq?`.

<a id="eqv"></a>
**`(eqv? obj₁ obj₂)`** — procedure

The `eqv?` procedure defines a useful equivalence relation on objects.
Briefly, it returns `#t` if *obj*₁ and *obj*₂ are
normally regarded as the same object. This relation is left slightly
open to interpretation, but the following partial specification of
`eqv?` holds for all implementations of Scheme.

The `eqv?` procedure returns `#t` if:

- *obj*₁ and *obj*₂ are both `#t` or both `#f`.
- *obj*₁ and *obj*₂ are both symbols and are the same
  symbol according to the `symbol=?` procedure
  (section [Symbols](#symbolsection)).
- *obj*₁ and *obj*₂ are both exact numbers and
  are numerically equal (in the sense of `=`).
- *obj*₁ and *obj*₂ are both inexact numbers such that
  they are numerically equal (in the sense of `=`)
  and they yield the same results (in the sense of `eqv?`)
  when passed as arguments to any other procedure
  that can be defined as a finite composition of Scheme's standard
  arithmetic procedures, provided it does not result in a NaN value.
- *obj*₁ and *obj*₂ are both characters and are the same
  character according to the `char=?` procedure
  (section [Characters](#charactersection)).
- *obj*₁ and *obj*₂ are both the empty list.
- *obj*₁ and *obj*₂ are pairs, vectors, bytevectors, records,
  or strings that denote the same location in the store
  (section [Storage model](#storagemodel)).
- *obj*₁ and *obj*₂ are procedures whose location tags are
  equal (section [lambda](#lambda)).

The `eqv?` procedure returns `#f` if:

- *obj*₁ and *obj*₂ are of different types
  (section [Disjointness of types](#disjointness)).
- one of *obj*₁ and *obj*₂ is `#t` but the other is
  `#f`.
- *obj*₁ and *obj*₂ are symbols but are not the same
  symbol according to the `symbol=?` procedure
  (section [Symbols](#symbolsection)).
- one of *obj*₁ and *obj*₂ is an exact number but the other
  is an inexact number.
- *obj*₁ and *obj*₂ are both exact numbers and
  are numerically unequal (in the sense of `=`).
- *obj*₁ and *obj*₂ are both inexact numbers such that either
  they are numerically unequal (in the sense of `=`),
  or they do not yield the same results (in the sense of `eqv?`)
  when passed as arguments to any other procedure
  that can be defined as a finite composition of Scheme's standard
  arithmetic procedures, provided it does not result in a NaN value.
  As an exception, the behavior of `eqv?` is unspecified
  when both *obj*₁ and *obj*₂ are NaN.
- *obj*₁ and *obj*₂ are characters for which the `char=?`
  procedure returns `#f`.
- one of *obj*₁ and *obj*₂ is the empty list but the other
  is not.
- *obj*₁ and *obj*₂ are pairs, vectors, bytevectors, records,
  or strings that denote distinct locations.
- *obj*₁ and *obj*₂ are procedures that would behave differently
  (return different values or have different side effects) for some arguments.

```scheme
(eqv? 'a 'a)                       =>  #t
(eqv? 'a 'b)                       =>  #f
(eqv? 2 2)                         =>  #t
(eqv? 2 2.0)                       =>  #f
(eqv? '() '())                     =>  #t
(eqv? 100000000 100000000)         =>  #t
(eqv? 0.0 +nan.0)                  =>  #f
(eqv? (cons 1 2) (cons 1 2))       =>  #f
(eqv? (lambda () 1)
      (lambda () 2))               =>  #f
(let ((p (lambda (x) x)))
  (eqv? p p))                      =>  #t
(eqv? #f 'nil)                    =>  #f
```

The following examples illustrate cases in which the above rules do
not fully specify the behavior of `eqv?`. All that can be said
about such cases is that the value returned by `eqv?` must be a
boolean.

```scheme
(eqv? "" "")               =>  unspecified
(eqv? '#() '#())           =>  unspecified
(eqv? (lambda (x) x)
      (lambda (x) x))      =>  unspecified
(eqv? (lambda (x) x)
      (lambda (y) y))      =>  unspecified
(eqv? 1.0e0 1.0f0)         =>  unspecified
(eqv? +nan.0 +nan.0)       =>  unspecified
```

Note that `(eqv? 0.0 -0.0)` will return `#f` if negative zero
is distinguished, and `#t` if negative zero is not distinguished.

The next set of examples shows the use of `eqv?` with procedures
that have local state. The `gen-counter` procedure must return a distinct
procedure every time, since each procedure has its own internal counter.
The `gen-loser` procedure, however, returns operationally equivalent procedures each time, since
the local state does not affect the value or side effects of the
procedures. However, `eqv?` may or may not detect this equivalence.

```scheme
(define gen-counter
  (lambda ()
    (let ((n 0))
      (lambda () (set! n (+ n 1)) n))))
(let ((g (gen-counter)))
  (eqv? g g))             =>  #t
(eqv? (gen-counter) (gen-counter))
                          =>  #f
(define gen-loser
  (lambda ()
    (let ((n 0))
      (lambda () (set! n (+ n 1)) 27))))
(let ((g (gen-loser)))
  (eqv? g g))             =>  #t
(eqv? (gen-loser) (gen-loser))
                          =>  unspecified

(letrec ((f (lambda () (if (eqv? f g) 'both 'f)))
         (g (lambda () (if (eqv? f g) 'both 'g))))
  (eqv? f g))
                          =>  unspecified

(letrec ((f (lambda () (if (eqv? f g) 'f 'both)))
         (g (lambda () (if (eqv? f g) 'g 'both))))
  (eqv? f g))
                          =>  #f
```

Since it is an error to modify constant objects (those returned by
literal expressions), implementations may
share structure between constants where appropriate. Thus
the value of `eqv?` on constants is sometimes
implementation-dependent.

```scheme
(eqv? '(a) '(a))                   =>  unspecified
(eqv? "a" "a")                     =>  unspecified
(eqv? '(b) (cdr '(a b)))	   =>  unspecified
(let ((x '(a)))
  (eqv? x x))                      =>  #t
```

The above definition of `eqv?` allows implementations latitude in
their treatment of procedures and literals: implementations may
either detect or fail to detect that two procedures or two literals
are equivalent to each other, and can decide whether or not to
merge representations of equivalent objects by using the same pointer or
bit pattern to represent both.

> **Note:** If inexact numbers are represented as IEEE binary floating-point numbers,
> then an implementation of `eqv?` that simply compares equal-sized
> inexact numbers for bitwise equality is correct by the above definition.

<a id="eq"></a>
**`(eq? obj₁ obj₂)`** — procedure

The `eq?` procedure is similar to `eqv?` except that in some cases it is
capable of discerning distinctions finer than those detectable by
`eqv?`. It must always return `#f` when `eqv?` also
would, but may return `#f` in some cases where `eqv?` would return `#t`.

On symbols, booleans, the empty list, pairs, and records,
and also on non-empty
strings, vectors, and bytevectors, `eq?` and `eqv?` are guaranteed to have the same
behavior. On procedures, `eq?` must return true if the arguments' location
tags are equal. On numbers and characters, `eq?`'s behavior is
implementation-dependent, but it will always return either true or
false. On empty strings, empty vectors, and empty bytevectors, `eq?` may also behave
differently from `eqv?`.

```scheme
(eq? 'a 'a)                       =>  #t
(eq? '(a) '(a))                   =>  unspecified
(eq? (list 'a) (list 'a))         =>  #f
(eq? "a" "a")                     =>  unspecified
(eq? "" "")                       =>  unspecified
(eq? '() '())                     =>  #t
(eq? 2 2)                         =>  unspecified
(eq? #A #A)   =>  unspecified
(eq? car car)                     =>  #t
(let ((n (+ 2 3)))
  (eq? n n))        =>  unspecified
(let ((x '(a)))
  (eq? x x))        =>  #t
(let ((x '#()))
  (eq? x x))        =>  #t
(let ((p (lambda (x) x)))
  (eq? p p))        =>  #t
```

> **Rationale:** more efficiently than `eqv?`, for example, as a simple pointer
> comparison instead of as some more complicated operation. One reason is
> that it is not always possible to compute `eqv?` of two numbers in
> constant time, whereas `eq?` implemented as pointer comparison will
> always finish in constant time.

<a id="equal"></a>
**`(equal? obj₁ obj₂)`** — procedure

The `equal?` procedure, when applied to pairs, vectors, strings and
bytevectors, recursively compares them, returning `#t` when the
unfoldings of its arguments into (possibly infinite) trees are equal
(in the sense of `equal?`)
as ordered trees, and `#f` otherwise. It returns the same as
`eqv?` when applied to booleans, symbols, numbers, characters,
ports, procedures, and the empty list. If two objects are `eqv?`,
they must be `equal?` as well. In all other cases, `equal?`
may return either `#t` or `#f`.

Even if its arguments are
circular data structures, `equal?` must always terminate.

```scheme
(equal? 'a 'a)                    =>  #t
(equal? '(a) '(a))                =>  #t
(equal? '(a (b) c)
        '(a (b) c))               =>  #t
(equal? "abc" "abc")              =>  #t
(equal? 2 2)                      =>  #t
(equal? (make-vector 5 'a)
        (make-vector 5 'a))       =>  #t
(equal? '#1=(a b . #1#)
        '#2=(a b a b . #2#))      =>  #t
(equal? (lambda (x) x)
        (lambda (y) y))    =>  unspecified
```

> **Note:** A rule of thumb is that objects are generally `equal?` if they print
> the same.

## Numbers

<a id="numbersection"></a>

It is important to distinguish between mathematical numbers, the
Scheme numbers that attempt to model them, the machine representations
used to implement the Scheme numbers, and notations used to write numbers.
This report uses the types , , ,
, and to refer to both mathematical numbers
and Scheme numbers.

### Numerical types

<a id="numericaltypes"></a>

Mathematically, numbers are arranged into a tower of subtypes
in which each level is a subset of the level above it:

number  
complex number  
real number  
rational number  
integer  

For example, 3 is an integer. Therefore 3 is also a rational,
a real, and a complex number. The same is true of the Scheme numbers
that model 3. For Scheme numbers, these types are defined by the
predicates `number?`, `complex?`, `real?`, `rational?`,
and `integer?`.

There is no simple relationship between a number's type and its
representation inside a computer. Although most implementations of
Scheme will offer at least two different representations of 3, these
different representations denote the same integer.

Scheme's numerical operations treat numbers as abstract data, as
independent of their representation as possible. Although an implementation
of Scheme may use multiple internal representations of
numbers, this ought not to be apparent to a casual programmer writing
simple programs.

### Exactness

<a id="exactness"></a> <a id="exactly"></a>

It is useful to distinguish between numbers that are
represented exactly and those that might not be. For example, indexes
into data structures must be known exactly, as must some polynomial
coefficients in a symbolic algebra system. On the other hand, the
results of measurements are inherently inexact, and irrational numbers
may be approximated by rational and therefore inexact approximations.
In order to catch uses of inexact numbers where exact numbers are
required, Scheme explicitly distinguishes exact from inexact numbers.
This distinction is orthogonal to the dimension of type.

A Scheme number is
 if it was written as an exact constant or was derived from
exact numbers using only exact operations. A number is
 if it was written as an inexact constant,
if it was
derived using inexact ingredients, or if it was derived using
inexact operations. Thus inexactness is a contagious
property of a number.
In particular, an **exact complex number** has an exact real part
and an exact imaginary part; all other complex numbers are **inexact
complex numbers**.

If two implementations produce exact results for a
computation that did not involve inexact intermediate results,
the two ultimate results will be mathematically equal. This is
generally not true of computations involving inexact numbers
since approximate methods such as floating-point arithmetic may be used,
but it is the duty of each implementation to make the result as close as
practical to the mathematically ideal result.

Rational operations such as `+` should always produce
exact results when given exact arguments.
If the operation is unable to produce an exact result,
then it may either report the violation of an implementation restriction
or it may silently coerce its
result to an inexact value.
However, `(/ 3 4)` must not return the mathematically incorrect value `0`.
See section [Implementation restrictions](#restrictions).

Except for `exact`, the operations described in
this section must generally return inexact results when given any inexact
arguments. An operation may, however, return an exact result if it can
prove that the value of the result is unaffected by the inexactness of its
arguments. For example, multiplication of any number by an exact zero
may produce an exact zero result, even if the other argument is
inexact.

Specifically, the expression `(* 0 +inf.0)` may return `0`,
or `+nan.0`, or report that inexact numbers are not supported,
or report that non-rational real numbers are not supported, or fail
silently or noisily in other implementation-specific ways.

### Implementation restrictions

<a id="restrictions"></a>

Implementations of Scheme are not required to implement the whole
tower of subtypes given in section [Numerical types](#numericaltypes),
but they must implement a coherent subset consistent with both the
purposes of the implementation and the spirit of the Scheme language.
For example, implementations in which all numbers are real,
or in which non-real numbers are always inexact,
or in which exact numbers are always integer,
are still quite useful.

Implementations may also support only a limited range of numbers of
any type, subject to the requirements of this section. The supported
range for exact numbers of any type may be different from the
supported range for inexact numbers of that type. For example,
an implementation that uses IEEE binary double-precision floating-point numbers to represent all its
inexact real numbers may also
support a practically unbounded range of exact integers
and rationals
while limiting the range of inexact reals (and therefore
the range of inexact integers and rationals)
to the dynamic range of the IEEE binary double format.
Furthermore,
the gaps between the representable inexact integers and
rationals are
likely to be very large in such an implementation as the limits of this
range are approached.

An implementation of Scheme must support exact integers
throughout the range of numbers permitted as indexes of
lists, vectors, bytevectors, and strings or that result from computing the length of
one of these. The `length`, `vector-length`,
`bytevector-length`, and `string-length` procedures must return an exact
integer, and it is an error to use anything but an exact integer as an
index. Furthermore, any integer constant within the index range, if
expressed by an exact integer syntax, must be read as an exact
integer, regardless of any implementation restrictions that apply
outside this range. Finally, the procedures listed below will always
return exact integer results provided all their arguments are exact integers
and the mathematically expected results are representable as exact integers
within the implementation:

```scheme
-                     *
+                     abs
ceiling               denominator
exact-integer-sqrt    expt
floor                 floor/
floor-quotient        floor-remainder
gcd                   lcm
max                   min
modulo                numerator
quotient              rationalize
remainder             round
square                truncate
truncate/             truncate-quotient
truncate-remainder
```

It is recommended, but not required, that implementations support
exact integers and exact rationals of
practically unlimited size and precision, and to implement the
above procedures and the `/` procedure in
such a way that they always return exact results when given exact
arguments. If one of these procedures is unable to deliver an exact
result when given exact arguments, then it may either report a
violation of an
implementation restriction or it may silently coerce its result to an
inexact number; such a coercion can cause an error later.
Nevertheless, implementations that do not provide exact rational
numbers should return inexact rational numbers rather than
reporting an implementation restriction.

An implementation may use floating-point and other approximate
representation strategies for inexact numbers.
This report recommends, but does not require, that
implementations that use
floating-point representations
follow the IEEE 754 standard,
and that implementations using
other representations should match or exceed the precision achievable
using these floating-point standards [[IEEE](#cite-ieee)].
In particular, the description of transcendental functions in IEEE 754-2008
should be followed by such implementations, particularly with respect
to infinities and NaNs.

Although Scheme allows a variety of written
notations for
numbers, any particular implementation may support only some of them.
For example, an implementation in which all numbers are real
need not support the rectangular and polar notations for complex
numbers. If an implementation encounters an exact numerical constant that
it cannot represent as an exact number, then it may either report a
violation of an implementation restriction or it may silently represent the
constant by an inexact number.

### Implementation extensions

Implementations may provide more than one representation of
floating-point numbers with differing precisions. In an implementation
which does so, an inexact result must be represented with at least
as much precision as is used to express any of the inexact arguments
to that operation. Although it is desirable for potentially inexact
operations such as `sqrt` to produce exact answers when
applied to exact arguments, if an exact number is operated
upon so as to produce an inexact result, then the most precise
representation available must be used. For example, the value of `(sqrt 4)` should be `2`, but in an implementation that provides both
single and double precision floating point numbers it may be the latter
but must not be the former.

It is the programmer's responsibility to avoid using inexact
number objects with magnitude or significand too large to be
represented in the implementation.

In addition, implementations may
distinguish special numbers called positive infinity,
negative infinity, NaN, and negative zero.

Positive infinity is regarded as an inexact real (but not rational)
number that represents an indeterminate value greater than the
numbers represented by all rational numbers. Negative infinity
is regarded as an inexact real (but not rational) number that
represents an indeterminate value less than the numbers represented
by all rational numbers.

Adding or multiplying an infinite value by any finite real value results
in an appropriately signed infinity; however, the sum of positive and
negative infinities is a NaN. Positive infinity is the reciprocal
of zero, and negative infinity is the reciprocal of negative zero.
The behavior of the transcendental functions is sensitive to infinity
in accordance with IEEE 754.

A NaN is regarded as an inexact real (but not rational) number
so indeterminate that it might represent any real value, including
positive or negative infinity, and might even be greater than positive
infinity or less than negative infinity.
An implementation that does not support non-real numbers may use NaN
to represent non-real values like `(sqrt -1.0)` and `(asin 2.0)`.

A NaN always compares false to any number, including a NaN.
An arithmetic operation where one operand is NaN returns NaN, unless the
implementation can prove that the result would be the same if the NaN
were replaced by any rational number. Dividing zero by zero results in
NaN unless both zeros are exact.

Negative zero is an inexact real value written `-0.0` and is distinct
(in the sense of `eqv?`) from `0.0`. A Scheme implementation
is not required to distinguish negative zero. If it does, however, the
behavior of the transcendental functions is sensitive to the distinction
in accordance with IEEE 754.
Specifically, in a Scheme implementing both complex numbers and negative zero,
the branch cut of the complex logarithm function is such that
`(imag-part (log -1.0-0.0i))` is $-\pi$ rather than $\pi$.

Furthermore, the negation of negative zero is ordinary zero and vice
versa. This implies that the sum of two or more negative zeros is negative,
and the result of subtracting (positive) zero from a negative zero is
likewise negative. However, numerical comparisons treat negative zero
as equal to zero.

Note that both the real and the imaginary parts of a complex number
can be infinities, NaNs, or negative zero.

### Syntax of numerical constants

<a id="numbernotations"></a>

The syntax of the written representations for numbers is described formally in
section [Lexical structure](#numbersyntax). Note that case is not significant in numerical
constants.

A number can be written in binary, octal, decimal, or
hexa­decimal by the use of a radix prefix. The radix prefixes are `#b` (binary), `#o` (octal), `#d` (decimal), and `#x` (hexa­decimal). With
no radix prefix, a number is assumed to be expressed in decimal.

A
numerical constant can be specified to be either exact or
inexact by a prefix. The prefixes are `#e`
for exact, and `#i` for inexact. An exactness
prefix can appear before or after any radix prefix that is used. If
the written representation of a number has no exactness prefix, the
constant is
inexact if it contains a decimal point or an
exponent.
Otherwise, it is exact.

In systems with inexact numbers
of varying precisions it can be useful to specify
the precision of a constant. For this purpose,
implementations may accept numerical constants
written with an exponent marker that indicates the
desired precision of the inexact
representation. If so, the letter `s`, `f`,
`d`, or `l`, meaning *short*, *single*,
*double*, or *long* precision, respectively,
can be used in place of `e`.
The default precision has at least as much precision
as *double*, but
implementations may allow this default to be set by the user.

```scheme
3.14159265358979F0
       Round to single --- 3.141593
0.6L0
       Extend to long --- .600000000000000
```

The numbers positive infinity, negative infinity, and NaN are written
`+inf.0`, `-inf.0` and `+nan.0` respectively.
NaN may also be written `-nan.0`.
The use of signs in the written representation does not necessarily
reflect the underlying sign of the NaN value, if any.
Implementations are not required to support these numbers, but if they do,
they must do so in general conformance with IEEE 754. However, implementations
are not required to support signaling NaNs, nor to provide a way to distinguish
between different NaNs.

There are two notations provided for non-real complex numbers:
the **rectangular notation**
*a*`+`*b*`i`,
where *a* is the real part and *b* is the imaginary part;
and the **polar notation**
*r*`@`$\theta$,
where *r* is the magnitude and $\theta$ is the phase (angle) in radians.
These are related by the equation
$a+b\mathrm{i} = r \cos\theta + (r \sin\theta) \mathrm{i}$.
All of *a*, *b*, *r*, and $\theta$ are real numbers.

### Numerical operations

The reader is referred to section [Entry format](#typeconventions) for a summary
of the naming conventions used to specify restrictions on the types of
arguments to numerical routines.
The examples used in this section assume that any numerical constant written
using an exact notation is indeed represented as an exact
number. Some examples also assume that certain numerical constants written
using an inexact notation can be represented without loss of
accuracy; the inexact constants were chosen so that this is
likely to be true in implementations that use IEEE binary doubles to represent
inexact numbers.

<a id="number"></a>
<a id="complex"></a>
<a id="real"></a>
<a id="rational"></a>
<a id="integer"></a>
**`(number? obj)`** — procedure  
**`(complex? obj)`** — procedure  
**`(real? obj)`** — procedure  
**`(rational? obj)`** — procedure  
**`(integer? obj)`** — procedure

These numerical type predicates can be applied to any kind of
argument, including non-numbers. They return `#t` if the object is
of the named type, and otherwise they return `#f`.
In general, if a type predicate is true of a number then all higher
type predicates are also true of that number. Consequently, if a type
predicate is false of a number, then all lower type predicates are
also false of that number.

If *z* is a complex number, then `(real? z)` is true if
and only if `(zero? (imag-part z))` is true.
If *x* is an inexact real number, then `(integer? x)` is true if and only if `(= x (round x))`.

The numbers `+inf.0`, `-inf.0`, and `+nan.0` are real but
not rational.

```scheme
(complex? 3+4i)           =>  #t
(complex? 3)              =>  #t
(real? 3)                 =>  #t
(real? -2.5+0i)           =>  #t
(real? -2.5+0.0i)         =>  #f
(real? #e1e10)            =>  #t
(real? +inf.0)             =>  #t
(real? +nan.0)             =>  #t
(rational? -inf.0)         =>  #f
(rational? 3.5)            =>  #t
(rational? 6/10)          =>  #t
(rational? 6/3)           =>  #t
(integer? 3+0i)           =>  #t
(integer? 3.0)            =>  #t
(integer? 8/4)            =>  #t
```

> **Note:** The behavior of these type predicates on inexact numbers
> is unreliable, since any inaccuracy might affect the result.

> **Note:** In many implementations the `complex?` procedure will be the same as
> `number?`, but unusual implementations may represent
> some irrational numbers exactly or may extend the number system to
> support some kind of non-complex numbers.

<a id="exact"></a>
<a id="inexact"></a>
**`(exact? z)`** — procedure  
**`(inexact? z)`** — procedure

These numerical predicates provide tests for the exactness of a
quantity. For any Scheme number, precisely one of these predicates
is true.

```scheme
(exact? 3.0)             =>  #f
(exact? #e3.0)           =>  #t
(inexact? 3.)            =>  #t
```

<a id="exact-integer"></a>
**`(exact-integer? z)`** — procedure

Returns `#t` if *z* is both exact and an integer;
otherwise returns `#f`.

```scheme
(exact-integer? 32)   => #t
(exact-integer? 32.0)   => #f
(exact-integer? 32/5)   => #f
```

<a id="finite"></a>
**`(finite? z)`** — inexact library procedure

The `finite?` procedure returns `#t` on all real numbers except
`+inf.0`, `-inf.0`, and `+nan.0`, and on complex
numbers if their real and imaginary parts are both finite.
Otherwise it returns `#f`.

```scheme
(finite? 3)           =>  #t
(finite? +inf.0)         =>  #f
(finite? 3.0+inf.0i)     =>  #f
```

<a id="infinite"></a>
**`(infinite? z)`** — inexact library procedure

The `infinite?` procedure returns `#t` on the real numbers
`+inf.0` and `-inf.0`, and on complex
numbers if their real or imaginary parts or both are infinite.
Otherwise it returns `#f`.

```scheme
(infinite? 3)           =>  #f
(infinite? +inf.0)         =>  #t
(infinite? +nan.0)         =>  #f
(infinite? 3.0+inf.0i)     =>  #t
```

<a id="nan"></a>
**`(nan? z)`** — inexact library procedure

The `nan?` procedure returns `#t` on `+nan.0`, and on complex
numbers if their real or imaginary parts or both are `+nan.0`.
Otherwise it returns `#f`.

```scheme
(nan? +nan.0)            =>  #t
(nan? 32)                =>  #f
(nan? +nan.0+5.0i)       =>  #t
(nan? 1+2i)              =>  #f
```

<a id="x-8"></a>
<a id="x-9"></a>
<a id="x-10"></a>
<a id="x-11"></a>
<a id="x-12"></a>
**`(= z₁ z₂ z₃ …)`** — procedure  
**`(< x₁ x₂ x₃ …)`** — procedure  
**`(> x₁ x₂ x₃ …)`** — procedure  
**`(<= x₁ x₂ x₃ …)`** — procedure  
**`(>= x₁ x₂ x₃ …)`** — procedure

These procedures return `#t` if their arguments are (respectively):
equal, monotonically increasing, monotonically decreasing,
monotonically non-decreasing, or monotonically non-increasing,
and `#f` otherwise.
If any of the arguments are `+nan.0`, all the predicates return `#f`.
They do not distinguish between inexact zero and inexact negative zero.

These predicates are required to be transitive.

> **Note:** The implementation approach
> of converting all arguments to inexact numbers
> if any argument is inexact is not transitive. For example, let
> `big` be `(expt 2 1000)`, and assume that `big` is exact and that
> inexact numbers are represented by 64-bit IEEE binary floating point numbers.
> Then `(= (- big 1) (inexact big))` and
> `(= (inexact big) (+ big 1))` would both be true with this approach,
> because of the limitations of IEEE
> representations of large integers, whereas `(= (- big 1) (+ big 1))`
> is false. Converting inexact values to exact numbers that are the same (in the sense of `=`) to them will avoid
> this problem, though special care must be taken with infinities.

> **Note:** While it is not an error to compare inexact numbers using these
> predicates, the results are unreliable because a small inaccuracy
> can affect the result; this is especially true of `=` and `zero?`.
> When in doubt, consult a numerical analyst.

<a id="zero"></a>
<a id="positive"></a>
<a id="negative"></a>
<a id="odd"></a>
<a id="even"></a>
**`(zero? z)`** — procedure  
**`(positive? x)`** — procedure  
**`(negative? x)`** — procedure  
**`(odd? n)`** — procedure  
**`(even? n)`** — procedure

These numerical predicates test a number for a particular property,
returning `#t` or `#f`. See note above.

<a id="max"></a>
<a id="min"></a>
**`(max x₁ x₂ …)`** — procedure  
**`(min x₁ x₂ …)`** — procedure

These procedures return the maximum or minimum of their arguments.

```scheme
(max 3 4)                =>  4    ; exact
(max 3.9 4)              =>  4.0  ; inexact
```

> **Note:** If any argument is inexact, then the result will also be inexact (unless
> the procedure can prove that the inaccuracy is not large enough to affect the
> result, which is possible only in unusual implementations). If `min` or
> `max` is used to compare numbers of mixed exactness, and the numerical
> value of the result cannot be represented as an inexact number without loss of
> accuracy, then the procedure may report a violation of an implementation
> restriction.

<a id="x-13"></a>
<a id="x-14"></a>
**`(+ z₁ …)`** — procedure  
**`(* z₁ …)`** — procedure

These procedures return the sum or product of their arguments.

```scheme
(+ 3 4)                   =>  7
(+ 3)                     =>  3
(+)                       =>  0
(* 4)                     =>  4
(*)                       =>  1
```

<a id="x-15"></a>
<a id="x-16"></a>
**`(- z)`** — procedure  
**`(- z₁ z₂ …)`** — procedure  
**`(/ z)`** — procedure  
**`(/ z₁ z₂ …)`** — procedure

With two or more arguments, these procedures return the difference or
quotient of their arguments, associating to the left. With one argument,
however, they return the additive or multiplicative inverse of their argument.

It is an error if any argument of `/` other than the first is an exact zero.
If the first argument is an exact zero, an implementation may return an
exact zero unless one of the other arguments is a NaN.

```scheme
(- 3 4)                   =>  -1
(- 3 4 5)                 =>  -6
(- 3)                     =>  -3
(/ 3 4 5)                 =>  3/20
(/ 3)                     =>  1/3
```

<a id="abs"></a>
**`(abs x)`** — procedure

The `abs` procedure returns the absolute value of its argument.

```scheme
(abs -7)                  =>  7
```

<a id="floor"></a>
<a id="floor-quotient"></a>
<a id="floor-remainder"></a>
<a id="truncate"></a>
<a id="truncate-quotient"></a>
<a id="truncate-remainder"></a>
**`(floor/ n₁ n₂)`** — procedure  
**`(floor-quotient n₁ n₂)`** — procedure  
**`(floor-remainder n₁ n₂)`** — procedure  
**`(truncate/ n₁ n₂)`** — procedure  
**`(truncate-quotient n₁ n₂)`** — procedure  
**`(truncate-remainder n₁ n₂)`** — procedure

These procedures implement
number-theoretic (integer) division. It is an error if *n*₂ is zero.
The procedures ending in `/` return two integers; the other
procedures return an integer. All the procedures compute a
quotient *n_q* and remainder *n_r* such that
${n_{1}} = {n_{2}} {n_q} + {n_r}$. For each of the
division operators, there are three procedures defined as follows:

```scheme
(⟨operator⟩/ n₁ n₂)               => n_q n_r
(⟨operator⟩-quotient n₁ n₂)       => n_q
(⟨operator⟩-remainder n₁ n₂)      => n_r
```

The remainder *n_r* is determined by the choice of integer
*n_q*: ${n_r} = {n_{1}} - {n_{2}} {n_q}$. Each set of
operators uses a different choice of *n_q*:

| `floor` | ${n_q} = \lfloor{n_{1}} / {n_{2}}\rfloor$ |
| --- | --- |
| `truncate` | ${n_q} = \text{truncate}({n_{1}} / {n_{2}})$ |

For any of the operators, and for integers *n*₁ and *n*₂
with *n*₂ not equal to 0,

```scheme
     (= n₁ (+ (* n₂ (⟨operator⟩-quotient n₁ n₂))
           (⟨operator⟩-remainder n₁ n₂)))
                                   =>  #t
```

provided all numbers involved in that computation are exact.

Examples:

```scheme
(floor/ 5 2)           => 2 1
(floor/ -5 2)          => -3 1
(floor/ 5 -2)          => -3 -1
(floor/ -5 -2)         => 2 -1
(truncate/ 5 2)        => 2 1
(truncate/ -5 2)       => -2 -1
(truncate/ 5 -2)       => -2 1
(truncate/ -5 -2)      => 2 -1
(truncate/ -5.0 -2)    => 2.0 -1.0
```

<a id="quotient"></a>
<a id="remainder"></a>
<a id="modulo"></a>
**`(quotient n₁ n₂)`** — procedure  
**`(remainder n₁ n₂)`** — procedure  
**`(modulo n₁ n₂)`** — procedure

The `quotient` and `remainder` procedures are equivalent to `truncate-quotient` and `truncate-remainder`, respectively, and `modulo` is equivalent to `floor-remainder`.

> **Note:** These procedures are provided for backward compatibility with earlier
> versions of this report.

<a id="gcd"></a>
<a id="lcm"></a>
**`(gcd n₁ …)`** — procedure  
**`(lcm n₁ …)`** — procedure

These procedures return the greatest common divisor or least common
multiple of their arguments. The result is always non-negative.

```scheme
(gcd 32 -36)              =>  4
(gcd)                     =>  0
(lcm 32 -36)              =>  288
(lcm 32.0 -36)            =>  288.0  ; inexact
(lcm)                     =>  1
```

<a id="numerator"></a>
<a id="denominator"></a>
**`(numerator q)`** — procedure  
**`(denominator q)`** — procedure

These procedures return the numerator or denominator of their
argument; the result is computed as if the argument was represented as
a fraction in lowest terms. The denominator is always positive. The
denominator of 0 is defined to be 1.

```scheme
(numerator (/ 6 4))    =>  3
(denominator (/ 6 4))    =>  2
(denominator
  (inexact (/ 6 4)))   => 2.0
```

<a id="floor-2"></a>
<a id="ceiling"></a>
<a id="truncate-2"></a>
<a id="round"></a>
**`(floor x)`** — procedure  
**`(ceiling x)`** — procedure  
**`(truncate x)`** — procedure  
**`(round x)`** — procedure

These procedures return integers.
 The `floor` procedure returns the largest integer not larger than *x*.
The `ceiling` procedure returns the smallest integer not smaller than *x*,
`truncate` returns the integer closest to *x* whose absolute
value is not larger than the absolute value of *x*, and `round` returns the
closest integer to *x*, rounding to even when *x* is halfway between two
integers.

> **Rationale:** The `round` procedure rounds to even for consistency with the default rounding
> mode specified by the IEEE 754 IEEE floating-point standard.

> **Note:** If the argument to one of these procedures is inexact, then the result
> will also be inexact. If an exact value is needed, the
> result can be passed to the `exact` procedure.
> If the argument is infinite or a NaN, then it is returned.

```scheme
(floor -4.3)            =>  -5.0
(ceiling -4.3)          =>  -4.0
(truncate -4.3)         =>  -4.0
(round -4.3)            =>  -4.0

(floor 3.5)             =>  3.0
(ceiling 3.5)           =>  4.0
(truncate 3.5)          =>  3.0
(round 3.5)             =>  4.0  ; inexact

(round 7/2)             =>  4    ; exact
(round 7)               =>  7
```

<a id="rationalize"></a>
**`(rationalize x y)`** — procedure

The `rationalize` procedure returns the *simplest* rational number
differing from *x* by no more than *y*. A rational number $r_1$ is
*simpler* <a id="simplest-rational"></a> than another rational number
$r_2$ if $r_1 = p_1/q_1$ and $r_2 = p_2/q_2$ (in lowest terms) and $|p_1| \leq |p_2|$ and $|q_1| \leq |q_2|$. Thus $3/5$ is simpler than $4/7$.
Although not all rationals are comparable in this ordering (consider $2/7$
and $3/5$), any interval contains a rational number that is simpler than
every other rational number in that interval (the simpler $2/5$ lies
between $2/7$ and $3/5$). Note that $0 = 0/1$ is the simplest rational of
all.

```scheme
(rationalize
  (exact .3) 1/10)    => 1/3    ; exact
(rationalize .3 1/10)          => #i1/3  ; inexact
```

<a id="exp"></a>
<a id="log"></a>
<a id="sin"></a>
<a id="cos"></a>
<a id="tan"></a>
<a id="asin"></a>
<a id="acos"></a>
<a id="atan"></a>
**`(exp z)`** — inexact library procedure  
**`(log z)`** — inexact library procedure  
**`(log z₁ z₂)`** — inexact library procedure  
**`(sin z)`** — inexact library procedure  
**`(cos z)`** — inexact library procedure  
**`(tan z)`** — inexact library procedure  
**`(asin z)`** — inexact library procedure  
**`(acos z)`** — inexact library procedure  
**`(atan z)`** — inexact library procedure  
**`(atan y x)`** — inexact library procedure

These procedures
compute the usual transcendental functions. The `log` procedure
computes the natural logarithm of *z* (not the base ten logarithm)
if a single argument is given, or the base-*z*₂ logarithm of *z*₁
if two arguments are given.
The `asin`, `acos`, and `atan` procedures compute arcsine ($\sin^{-1}$),
arc-cosine ($\cos^{-1}$), and arctangent ($\tan^{-1}$), respectively.
The two-argument variant of `atan` computes `(angle
(make-rectangular x y))` (see below), even in implementations
that don't support complex numbers.

In general, the mathematical functions log, arcsine, arc-cosine, and
arctangent are multiply defined.
The value of $\log z$ is defined to be the one whose imaginary part
lies in the range from $-\pi$ (inclusive if `-0.0` is distinguished,
exclusive otherwise) to $\pi$ (inclusive).
The value of $\log 0$ is mathematically undefined.
With $\log$ defined this way, the values of $\sin^{-1} z$, $\cos^{-1} z$,
and $\tan^{-1} z$ are according to the following formul:

$$
\sin^{-1} z = -i \log (i z + \sqrt{1 - z^2})
$$

$$
\cos^{-1} z = \pi / 2 - \sin^{-1} z
$$

$$
\tan^{-1} z = (\log (1 + i z) - \log (1 - i z)) / (2 i)
$$

However, `(log 0.0)` returns `-inf.0`
(and `(log -0.0)` returns `-inf.0+$\pi$i`) if the
implementation supports infinities (and `-0.0`).

The range of `(atan y x)` is as in the
following table. The asterisk (*) indicates that the entry applies to
implementations that distinguish minus zero.

|  | $y$ condition | $x$ condition | range of result $r$ |
| --- | --- | --- | --- |
|  | $y = 0.0$ | $x > 0.0$ | $0.0$ |
| $\ast$ | $y = +0.0$ | $x > 0.0$ | $+0.0$ |
| $\ast$ | $y = -0.0$ | $x > 0.0$ | $-0.0$ |
|  | $y > 0.0$ | $x > 0.0$ | $0.0 < r < \frac{\pi}{2}$ |
|  | $y > 0.0$ | $x = 0.0$ | $\frac{\pi}{2}$ |
|  | $y > 0.0$ | $x < 0.0$ | $\frac{\pi}{2} < r < \pi$ |
|  | $y = 0.0$ | $x < 0$ | $\pi$ |
| $\ast$ | $y = +0.0$ | $x < 0.0$ | $\pi$ |
| $\ast$ | $y = -0.0$ | $x < 0.0$ | $-\pi$ |
|  | $y < 0.0$ | $x < 0.0$ | $-\pi< r< -\frac{\pi}{2}$ |
|  | $y < 0.0$ | $x = 0.0$ | $-\frac{\pi}{2}$ |
|  | $y < 0.0$ | $x > 0.0$ | $-\frac{\pi}{2} < r< 0.0$ |
|  | $y = 0.0$ | $x = 0.0$ | undefined |
| $\ast$ | $y = +0.0$ | $x = +0.0$ | $+0.0$ |
| $\ast$ | $y = -0.0$ | $x = +0.0$ | $-0.0$ |
| $\ast$ | $y = +0.0$ | $x = -0.0$ | $\pi$ |
| $\ast$ | $y = -0.0$ | $x = -0.0$ | $-\pi$ |
| $\ast$ | $y = +0.0$ | $x = 0$ | $\frac{\pi}{2}$ |
| $\ast$ | $y = -0.0$ | $x = 0$ | $-\frac{\pi}{2}$ |

The above specification follows [[CLtL](#cite-cltl)], which in turn
cites [[Penfield81](#cite-penfield81)]; refer to these sources for more detailed
discussion of branch cuts, boundary conditions, and implementation of
these functions. When it is possible, these procedures produce a real
result from a real argument.

<a id="square"></a>
**`(square z)`** — procedure

Returns the square of *z*.
This is equivalent to `(* z z)`.

```scheme
(square 42)         => 1764
(square 2.0)       => 4.0
```

<a id="sqrt"></a>
**`(sqrt z)`** — inexact library procedure

Returns the principal square root of *z*. The result will have
either a positive real part, or a zero real part and a non-negative imaginary
part.

```scheme
(sqrt 9)    => 3
(sqrt -1)   => +i
```

<a id="exact-integer-sqrt"></a>
**`(exact-integer-sqrt k)`** — procedure

Returns two non-negative exact integers $s$ and $r$ where
${k} = s^2 + r$ and ${k} < (s+1)^2$.

```scheme
(exact-integer-sqrt 4)   => 2 0
(exact-integer-sqrt 5)   => 2 1
```

<a id="expt"></a>
**`(expt z₁ z₂)`** — procedure

Returns *z*₁ raised to the power *z*₂. For nonzero *z*₁, this is

$$
{z_1}^{z_2} = e^{z_2 \log {z_1}}
$$

The value of $0^z$ is $1$ if `(zero? z)`, $0$ if `(real-part z)`
is positive, and an error otherwise. Similarly for $0.0^z$,
with inexact results.

<a id="make-rectangular"></a>
<a id="make-polar"></a>
<a id="real-part"></a>
<a id="imag-part"></a>
<a id="magnitude"></a>
<a id="angle"></a>
**`(make-rectangular x₁ x₂)`** — complex library procedure  
**`(make-polar x₃ x₄)`** — complex library procedure  
**`(real-part z)`** — complex library procedure  
**`(imag-part z)`** — complex library procedure  
**`(magnitude z)`** — complex library procedure  
**`(angle z)`** — complex library procedure

Let *x*₁, *x*₂, *x*₃, and *x*₄ be
real numbers and *z* be a complex number such that

$$
{z} = {x_{1}} + {x_{2}}i
 = {x_{3}} \cdot e^{i x_4}
$$

Then all of

```scheme
(make-rectangular x₁ x₂)   => z
(make-polar x₃ x₄)       => z
(real-part z)                    => x₁
(imag-part z)                    => x₂
(magnitude z)                    => $|x₃|$
(angle z)                        => $x_angle$
```

are true, where $-\pi \le x_{angle} \le \pi$ with $x_{angle} = {x_{4}} + 2\pi n$
for some integer $n$.

The `make-polar` procedure may return an inexact complex number even if its
arguments are exact.
The `real-part` and `imag-part` procedures may return exact real
numbers when applied to an inexact complex number if the corresponding
argument passed to `make-rectangular` was exact.

> **Rationale:** The `magnitude` procedure is the same as `abs` for a real argument,
> but `abs` is in the base library, whereas
> `magnitude` is in the optional complex library.

<a id="inexact-2"></a>
<a id="exact-2"></a>
**`(inexact z)`** — procedure  
**`(exact z)`** — procedure

The procedure `inexact` returns an inexact representation of *z*.
The value returned is the
inexact number that is numerically closest to the argument.
For inexact arguments, the result is the same as the argument. For exact
complex numbers, the result is a complex number whose real and imaginary
parts are the result of applying `inexact` to the real
and imaginary parts of the argument, respectively.
If an exact argument has no reasonably close inexact equivalent
(in the sense of `=`),
then a violation of an implementation restriction may be reported.

The procedure `exact` returns an exact representation of
*z*. The value returned is the exact number that is numerically
closest to the argument.
For exact arguments, the result is the same as the argument. For inexact
non-integral real arguments, the implementation may return a rational
approximation, or may report an implementation violation. For inexact
complex arguments, the result is a complex number whose real and
imaginary parts are the result of applying `exact` to the
real and imaginary parts of the argument, respectively.
If an inexact argument has no reasonably close exact equivalent,
(in the sense of `=`),
then a violation of an implementation restriction may be reported.

These procedures implement the natural one-to-one correspondence between
exact and inexact integers throughout an
implementation-dependent range. See section [Implementation restrictions](#restrictions).

> **Note:** These procedures were known in R⁵RS as `exact->inexact` and
> `inexact->exact`, respectively, but they have always accepted
> arguments of any exactness. The new names are clearer and shorter,
> as well as being compatible with R⁶RS.

### Numerical input and output

<a id="number-string"></a>
**`(number->string z)`** — procedure  
**`(number->string z radix)`** — procedure

It is an error if *radix* is not one of 2, 8, 10, or 16.
The procedure `number->string` takes a
number and a radix and returns as a string an external representation of
the given number in the given radix such that

```scheme
(let ((number number)
      (radix radix))
  (eqv? number
        (string->number (number->string number
                                        radix)
                        radix)))
```

is true. It is an error if no possible result makes this expression true.
If omitted, *radix* defaults to 10.

If *z* is inexact, the radix is 10, and the above expression
can be satisfied by a result that contains a decimal point,
then the result contains a decimal point and is expressed using the
minimum number of digits (exclusive of exponent and trailing
zeroes) needed to make the above expression
true [[howtoprint](#cite-howtoprint), [howtoread](#cite-howtoread)];
otherwise the format of the result is unspecified.

The result returned by `number->string`
never contains an explicit radix prefix.

> **Note:** The error case can occur only when *z* is not a complex number
> or is a complex number with a non-rational real or imaginary part.

> **Rationale:** If *z* is an inexact number and
> the radix is 10, then the above expression is normally satisfied by
> a result containing a decimal point. The unspecified case
> allows for infinities, NaNs, and unusual representations.

<a id="string-number"></a>
**`(string->number string)`** — procedure  
**`(string->number string radix)`** — procedure

Returns a number of the maximally precise representation expressed by the
given *string*.
It is an error if *radix* is not 2, 8, 10, or 16.
If supplied, *radix* is a default radix that will be overridden
if an explicit radix prefix is present in *string* (e.g. `"#o177"`). If *radix*
is not supplied, then the default radix is 10. If *string* is not
a syntactically valid notation for a number, or would result in a
number that the implementation cannot represent, then `string->number`
returns `#f`.
An error is never signaled due to the content of *string*.

```scheme
(string->number "100")          =>  100
(string->number "100" 16)       =>  256
(string->number "1e2")          =>  100.0
```

> **Note:** The domain of `string->number` may be restricted by implementations
> in the following ways.
> If all numbers supported by an implementation are real, then
> `string->number` is permitted to return `#f` whenever
> *string* uses the polar or rectangular notations for complex
> numbers. If all numbers are integers, then
> `string->number` may return `#f` whenever
> the fractional notation is used. If all numbers are exact, then
> `string->number` may return `#f` whenever
> an exponent marker or explicit exactness prefix is used.
> If all inexact
> numbers are integers, then
> `string->number` may return `#f` whenever
> a decimal point is used.
>
>
> The rules used by a particular implementation for `string->number` must
> also be applied to `read` and to the routine that reads programs, in
> order to maintain consistency between internal numeric processing, I/O,
> and the processing of programs.
> As a consequence, the R⁵RS permission to return `#f` when
> *string* has an explicit radix prefix has been withdrawn.

## Booleans

<a id="booleansection"></a>

The standard boolean objects for true and false are written as
`#t` and `#f`.
Alternatively, they can be written `#true` and `#false`,
respectively. What really
matters, though, are the objects that the Scheme conditional expressions
(`if`, `cond`, `and`, `or`, `when`, `unless`, `do`) treat as
true or false. The phrase “a true value”
(or sometimes just “true”) means any object treated as true by the
conditional expressions, and the phrase “a false value” (or
“false”) means any object treated as false by the conditional expressions.

Of all the Scheme values, only `#f`
counts as false in conditional expressions.
All other Scheme values, including `#t`,
count as true.

> **Note:** Unlike some other dialects of Lisp,
> Scheme distinguishes `#f` and the empty list
> from each other and from the symbol `nil`.

Boolean constants evaluate to themselves, so they do not need to be quoted
in programs.

```scheme
#t           =>  #t
#f          =>  #f
'#f         =>  #f
```

<a id="not"></a>
**`(not obj)`** — procedure

The `not` procedure returns `#t` if *obj* is false, and returns
`#f` otherwise.

```scheme
(not #t)     =>  #f
(not 3)            =>  #f
(not (list 3))     =>  #f
(not #f)    =>  #t
(not '())          =>  #f
(not (list))       =>  #f
(not 'nil)         =>  #f
```

<a id="boolean"></a>
**`(boolean? obj)`** — procedure

The `boolean?` predicate returns `#t` if *obj* is either `#t` or
`#f` and returns `#f` otherwise.

```scheme
(boolean? #f)    =>  #t
(boolean? 0)            =>  #f
(boolean? '())          =>  #f
```

<a id="boolean-2"></a>
**`(boolean=? boolean₁ boolean₂ boolean₃ …)`** — procedure

Returns `#t` if all the arguments
are `#t` or all are `#f`.

## Pairs and lists

<a id="listsection"></a>

A **pair** (sometimes called a **dotted pair**) is a
record structure with two fields called the car and cdr fields (for
historical reasons). Pairs are created by the procedure `cons`.
The car and cdr fields are accessed by the procedures `car` and
`cdr`. The car and cdr fields are assigned by the procedures
`set-car!` and `set-cdr!`.

Pairs are used primarily to represent lists. A **list** can
be defined recursively as either the empty list or a pair whose
cdr is a list. More precisely, the set of lists is defined as the smallest
set *X* such that

- The empty list is in *X*.
- If *list* is in *X*, then any pair whose cdr field contains
   *list* is also in *X*.

The objects in the car fields of successive pairs of a list are the
elements of the list. For example, a two-element list is a pair whose car
is the first element and whose cdr is a pair whose car is the second element
and whose cdr is the empty list. The length of a list is the number of
elements, which is the same as the number of pairs.

The empty list<a id="empty-list"></a> is a special object of its own type.
It is not a pair, it has no elements, and its length is zero.

> **Note:** The above definitions imply that all lists have finite length and are
> terminated by the empty list.

The most general notation (external representation) for Scheme pairs is
the “dotted” notation (*c*₁ . *c*₂) where
*c*₁ is the value of the car field and *c*₂ is the value of the
cdr field. For example `(4 . 5)` is a pair whose car is 4 and whose
cdr is 5. Note that `(4 . 5)` is the external representation of a
pair, not an expression that evaluates to a pair.

A more streamlined notation can be used for lists: the elements of the
list are simply enclosed in parentheses and separated by spaces. The
empty list is written `()`. For example,

```scheme
(a b c d e)
```

and

```scheme
(a . (b . (c . (d . (e . ())))))
```

are equivalent notations for a list of symbols.

A chain of pairs not ending in the empty list is called an
**improper list**. Note that an improper list is not a list.
The list and dotted notations can be combined to represent
improper lists:

```scheme
(a b c . d)
```

is equivalent to

```scheme
(a . (b . (c . d)))
```

Whether a given pair is a list depends upon what is stored in the cdr
field. When the `set-cdr!` procedure is used, an object can be a
list one moment and not the next:

```scheme
(define x (list 'a 'b 'c))
(define y x)
y                         =>  (a b c)
(list? y)                 =>  #t
(set-cdr! x 4)            =>  unspecified
x                         =>  (a . 4)
(eqv? x y)                =>  #t
y                         =>  (a . 4)
(list? y)                 =>  #f
(set-cdr! x x)            =>  unspecified
(list? x)                 =>  #f
```

Within literal expressions and representations of objects read by the
`read` procedure, the forms '⟨datum⟩,
`⟨datum⟩, `,`⟨datum⟩, and
`,@`⟨datum⟩ denote two-ele­ment lists whose first elements are
the symbols `quote`, `quasiquote`, `unquote`, and
`unquote-splicing`, respectively. The second element in each case
is ⟨datum⟩. This convention is supported so that arbitrary Scheme
programs can be represented as lists.
That is, according to Scheme's grammar, every
⟨expression⟩ is also a ⟨datum⟩ (see section [External representations](#datum)).
Among other things, this permits the use of the `read` procedure to
parse Scheme programs. See section [External representations](#externalreps).

<a id="pair"></a>
**`(pair? obj)`** — procedure

The `pair?` predicate returns `#t` if *obj* is a pair, and otherwise
returns `#f`.

```scheme
(pair? '(a . b))          =>  #t
(pair? '(a b c))          =>  #t
(pair? '())               =>  #f
(pair? '#(a b))           =>  #f
```

<a id="cons"></a>
**`(cons obj₁ obj₂)`** — procedure

Returns a newly allocated pair whose car is *obj*₁ and whose cdr is
*obj*₂. The pair is guaranteed to be different (in the sense of
`eqv?`) from every existing object.

```scheme
(cons 'a '())             =>  (a)
(cons '(a) '(b c d))      =>  ((a) b c d)
(cons "a" '(b c))         =>  ("a" b c)
(cons 'a 3)               =>  (a . 3)
(cons '(a b) 'c)          =>  ((a b) . c)
```

<a id="car"></a>
**`(car pair)`** — procedure

Returns the contents of the car field of *pair*. Note that it is an
error to take the car of the empty list.

```scheme
(car '(a b c))            =>  a
(car '((a) b c d))        =>  (a)
(car '(1 . 2))            =>  1
(car '())                 =>  error
```

<a id="cdr"></a>
**`(cdr pair)`** — procedure

Returns the contents of the cdr field of *pair*.
Note that it is an error to take the cdr of the empty list.

```scheme
(cdr '((a) b c d))        =>  (b c d)
(cdr '(1 . 2))            =>  2
(cdr '())                 =>  error
```

<a id="set-car"></a>
**`(set-car! pair obj)`** — procedure

Stores *obj* in the car field of *pair*.

```scheme
(define (f) (list 'not-a-constant-list))
(define (g) '(constant-list))
(set-car! (f) 3)               =>  unspecified
(set-car! (g) 3)               =>  error
```

<a id="set-cdr"></a>
**`(set-cdr! pair obj)`** — procedure

Stores *obj* in the cdr field of *pair*.

0(cadr *pair*)
1procedure

<a id="caar"></a>
<a id="cadr"></a>
<a id="cdar"></a>
<a id="cddr"></a>
**`(caar pair)`** — procedure  
**`(cadr pair)`** — procedure  
**`(cdar pair)`** — procedure  
**`(cddr pair)`** — procedure

These procedures are compositions of `car` and `cdr` as follows:

```scheme
(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))
```

<a id="caaar"></a>
<a id="caadr"></a>
<a id="cdddar"></a>
<a id="cddddr"></a>
<a id="cadar"></a>
<a id="caddr"></a>
<a id="cdaar"></a>
<a id="cdadr"></a>
<a id="cddar"></a>
<a id="cdddr"></a>
<a id="caaaar"></a>
<a id="caaadr"></a>
<a id="caadar"></a>
<a id="caaddr"></a>
<a id="cadaar"></a>
<a id="cadadr"></a>
<a id="caddar"></a>
<a id="cadddr"></a>
<a id="cdaaar"></a>
<a id="cdaadr"></a>
<a id="cdadar"></a>
<a id="cdaddr"></a>
<a id="cddaar"></a>
<a id="cddadr"></a>
**`(caaar pair)`** — cxr library procedure  
**`(caadr pair)`** — cxr library procedure  
**`to 10 $\vdots$`** — to 11 $\vdots$  
**`(cdddar pair)`** — cxr library procedure  
**`(cddddr pair)`** — cxr library procedure

These twenty-four procedures are further compositions of `car` and `cdr`
on the same principles.
For example, `caddr` could be defined by

```scheme
(define caddr (lambda (x) (car (cdr (cdr x))))).
```

Arbitrary compositions up to four deep are provided.

<a id="null"></a>
**`(null? obj)`** — procedure

Returns `#t` if *obj* is the empty list,
otherwise returns `#f`.

<a id="list"></a>
**`(list? obj)`** — procedure

Returns `#t` if *obj* is a list. Otherwise, it returns `#f`.
By definition, all lists have finite length and are terminated by
the empty list.

```scheme
        (list? '(a b c))       =>  #t
        (list? '())            =>  #t
        (list? '(a . b))       =>  #f
        (let ((x (list 'a)))
          (set-cdr! x x)
          (list? x))           =>  #f
```

<a id="make-list"></a>
**`(make-list k)`** — procedure  
**`(make-list k fill)`** — procedure

Returns a newly allocated list of *k* elements. If a second
argument is given, then each element is initialized to *fill*.
Otherwise the initial contents of each element is unspecified.

```scheme
(make-list 2 3)     =>   (3 3)
```

<a id="list-2"></a>
**`(list obj …)`** — procedure

Returns a newly allocated list of its arguments.

```scheme
(list 'a (+ 3 4) 'c)              =>  (a 7 c)
(list)                            =>  ()
```

<a id="length"></a>
**`(length list)`** — procedure

Returns the length of *list*.

```scheme
(length '(a b c))                 =>  3
(length '(a (b) (c d e)))         =>  3
(length '())                      =>  0
```

<a id="append"></a>
**`(append list …)`** — procedure

The last argument, if there is one, can be of any type.
Returns a list consisting of the elements of the first *list*
followed by the elements of the other *list*s.
If there are no arguments, the empty list is returned.
If there is exactly one argument, it is returned.
Otherwise the resulting list is always newly allocated, except that it shares
structure with the last argument.
An improper list results if the last argument is not a
proper list.

```scheme
(append '(x) '(y))                =>  (x y)
(append '(a) '(b c d))            =>  (a b c d)
(append '(a (b)) '((c)))          =>  (a (b) (c))
```

```scheme
(append '(a b) '(c . d))          =>  (a b c . d)
(append '() 'a)                   =>  a
```

<a id="reverse"></a>
**`(reverse list)`** — procedure

Returns a newly allocated list consisting of the elements of *list*
in reverse order.

```scheme
(reverse '(a b c))                =>  (c b a)
(reverse '(a (b c) d (e (f))))  =>  ((e (f)) d (b c) a)
```

<a id="list-tail"></a>
**`(list-tail list k)`** — procedure

It is an error if *list* has fewer than *k* elements.
Returns the sublist of *list* obtained by omitting the first *k*
elements.
The `list-tail` procedure could be defined by

```scheme
(define list-tail
  (lambda (x k)
    (if (zero? k)
        x
        (list-tail (cdr x) (- k 1)))))
```

<a id="list-ref"></a>
**`(list-ref list k)`** — procedure

The *list* argument can be circular, but
it is an error if *list* has *k* or fewer elements.
Returns the *k*th element of *list*. (This is the same
as the car of `(list-tail list k)`.)

```scheme
(list-ref '(a b c d) 2)                   =>  c
(list-ref '(a b c d)
          (exact (round 1.8))) =>  c
```

<a id="list-set"></a>
**`(list-set! list k obj)`** — procedure

It is an error if *k* is not a valid index of *list*.
The `list-set!` procedure stores *obj* in element *k* of *list*.

```scheme
(let ((ls (list 'one 'two 'five!)))
  (list-set! ls 2 'three)
  ls)      =>  (one two three)

(list-set! '(0 1 2) 1 "oops")  =>  error  ; constant list
```

<a id="memq"></a>
<a id="memv"></a>
<a id="member"></a>
**`(memq obj list)`** — procedure  
**`(memv obj list)`** — procedure  
**`(member obj list)`** — procedure  
**`(member obj list compare)`** — procedure

These procedures return the first sublist of *list* whose car is
*obj*, where the sublists of *list* are the non-empty lists
returned by `(list-tail list k)` for *k* less
than the length of *list*. If
*obj* does not occur in *list*, then `#f` (not the empty list) is
returned. The `memq` procedure uses `eq?` to compare *obj* with the elements of
*list*, while `memv` uses `eqv?` and
`member` uses *compare*, if given, and `equal?` otherwise.

```scheme
(memq 'a '(a b c))                =>  (a b c)
(memq 'b '(a b c))                =>  (b c)
(memq 'a '(b c d))                =>  #f
(memq (list 'a) '(b (a) c))       =>  #f
(member (list 'a)
        '(b (a) c))               =>  ((a) c)
(member "B"
        '("a" "b" "c")
        string-ci=?)              =>  ("b" "c")
(memq 101 '(100 101 102))         =>  unspecified
(memv 101 '(100 101 102))         =>  (101 102)
```

<a id="assq"></a>
<a id="assv"></a>
<a id="assoc"></a>
**`(assq obj alist)`** — procedure  
**`(assv obj alist)`** — procedure  
**`(assoc obj alist)`** — procedure  
**`(assoc obj alist compare)`** — procedure

It is an error if *alist* (for “association list”) is not a list of
pairs.
These procedures find the first pair in *alist* whose car field is *obj*,
and returns that pair. If no pair in *alist* has *obj* as its
car, then `#f` (not the empty list) is returned. The `assq` procedure uses
`eq?` to compare *obj* with the car fields of the pairs in *alist*,
while `assv` uses `eqv?` and `assoc` uses *compare* if given
and `equal?` otherwise.

```scheme
(define e '((a 1) (b 2) (c 3)))
(assq 'a e)       =>  (a 1)
(assq 'b e)       =>  (b 2)
(assq 'd e)       =>  #f
(assq (list 'a) '(((a)) ((b)) ((c))))
                  =>  #f
(assoc (list 'a) '(((a)) ((b)) ((c))))
                             =>  ((a))
(assoc 2.0 '((1 1) (2 4) (3 9)) =)
                             => (2 4)
(assq 5 '((2 3) (5 7) (11 13)))
                             =>  unspecified
(assv 5 '((2 3) (5 7) (11 13)))
                             =>  (5 7)
```

> **Rationale:** Although they are often used as predicates,
> `memq`, `memv`, `member`, `assq`, `assv`, and `assoc` do not
> have question marks in their names because they return
> potentially useful values rather than just `#t` or `#f`.

<a id="list-copy"></a>
**`(list-copy obj)`** — procedure

Returns a newly allocated copy of the given *obj* if it is a list.
Only the pairs themselves are copied; the cars of the result are
the same (in the sense of `eqv?`) as the cars of *list*.
If *obj* is an improper list, so is the result, and the final
cdrs are the same in the sense of `eqv?`.
An *obj* which is not a list is returned unchanged.
It is an error if *obj* is a circular list.

```scheme
(define a '(1 8 2 8)) ; a may be immutable
(define b (list-copy a))
(set-car! b 3)        ; b is mutable
b   => (3 8 2 8)
a   => (1 8 2 8)
```

## Symbols

<a id="symbolsection"></a>

Symbols are objects whose usefulness rests on the fact that two
symbols are identical (in the sense of `eqv?`) if and only if their
names are spelled the same way. For instance, they can be used
the way enumerated values are used in other languages.

The rules for writing a symbol are exactly the same as the rules for
writing an identifier; see sections [Identifiers](#syntaxsection)
and [Lexical structure](#identifiersyntax).

It is guaranteed that any symbol that has been returned as part of
a literal expression, or read using the `read` procedure, and
subsequently written out using the `write` procedure, will read back
in as the identical symbol (in the sense of `eqv?`).

> **Note:** Some implementations have values known as “uninterned symbols,”
> which defeat write/read invariance, and also violate the rule that two
> symbols are the same if and only if their names are spelled the same.
> This report does not specify the behavior of
> implementation-dependent extensions.

<a id="symbol"></a>
**`(symbol? obj)`** — procedure

Returns `#t` if *obj* is a symbol, otherwise returns `#f`.

```scheme
(symbol? 'foo)            =>  #t
(symbol? (car '(a b)))    =>  #t
(symbol? "bar")           =>  #f
(symbol? 'nil)            =>  #t
(symbol? '())             =>  #f
(symbol? #f)       =>  #f
```

<a id="symbol-2"></a>
**`(symbol=? symbol₁ symbol₂ symbol₃ …)`** — procedure

Returns `#t` if all the arguments all have the same
names in the sense of `string=?`.

> **Note:** The definition above assumes that none of the arguments
> are uninterned symbols.

<a id="symbol-string"></a>
**`(symbol->string symbol)`** — procedure

Returns the name of *symbol* as a string, but without adding escapes.
It is an error
to apply mutation procedures like `string-set!` to strings returned
by this procedure.

```scheme
(symbol->string 'flying-fish)
                                    =>  "flying-fish"
(symbol->string 'Martin)            =>  "Martin"
(symbol->string
   (string->symbol "Malvina"))
                                    =>  "Malvina"
```

<a id="string-symbol"></a>
**`(string->symbol string)`** — procedure

Returns the symbol whose name is *string*. This procedure can
create symbols with names containing special characters that would
require escaping when written, but does not interpret escapes in its input.

```scheme
(string->symbol "mISSISSIppi")  =>
  mISSISSIppi
(eqv? 'bitBlt (string->symbol "bitBlt"))     =>  #t
(eqv? 'LollyPop
     (string->symbol
       (symbol->string 'LollyPop)))  =>  #t
(string=? "K. Harper, M.D."
          (symbol->string
            (string->symbol "K. Harper, M.D.")))  =>  #t
```

## Characters

<a id="charactersection"></a>

Characters are objects that represent printed characters such as
letters and digits.
All Scheme implementations must support at least the ASCII character
repertoire: that is, Unicode characters U+0000 through U+007F.
Implementations may support any other Unicode characters they see fit,
and may also support non-Unicode characters as well.
Except as otherwise specified, the result of applying any of the
following procedures to a non-Unicode character is implementation-dependent.

Characters are written using the notation #\⟨character⟩
or #\⟨character name⟩ or
#\x⟨hex scalar value⟩.

The following character names must be supported
by all implementations with the given values.
Implementations may add other names
provided they cannot be interpreted as hex scalar values preceded by `x`.

| `#\alarm` | ; U+0007 |
| --- | --- |
| `#\backspace` | ; U+0008 |
| `#\delete` | ; U+007F |
| `#\escape` | ; U+001B |
| `#\newline` | ; the linefeed character, U+000A |
| `#\null` | ; the null character, U+0000 |
| `#\return` | ; the return character, U+000D |
| `#\space` | ; the preferred way to write a space |
| `#\tab` | ; the tab character, U+0009 |

Here are some additional examples:

| `#\a` | ; lower case letter |
| --- | --- |
| `#\A` | ; upper case letter |
| `#\(` | ; left parenthesis |
| `#\` | ; the space character |
| `#\x03BB` | ; $\lambda$ (if character is supported) |
| `#\iota` | ; $\iota$ (if character and name are supported) |

Case is significant in #\⟨character⟩, and in
#\$⟨$character name$⟩$,
but not in `#\x`⟨hex scalar value⟩.
If ⟨character⟩ in
#\⟨character⟩ is alphabetic, then any character
immediately following ⟨character⟩ cannot be one that can appear in an identifier.
This rule resolves the ambiguous case where, for
example, the sequence of characters “`#\ space`”
could be taken to be either a representation of the space character or a
representation of the character “`#\ s`” followed
by a representation of the symbol “`pace`.”

Characters written in the #\ notation are self-evaluating.
That is, they do not have to be quoted in programs.

Some of the procedures that operate on characters ignore the
difference between upper case and lower case. The procedures that
ignore case have “`-ci`” (for “case
insensitive”) embedded in their names.

<a id="char"></a>
**`(char? obj)`** — procedure

Returns `#t` if *obj* is a character, otherwise returns `#f`.

<a id="char-2"></a>
<a id="char-3"></a>
<a id="char-4"></a>
<a id="char-5"></a>
<a id="char-6"></a>
**`(char=? char₁ char₂ char₃ …)`** — procedure  
**`(char<? char₁ char₂ char₃ …)`** — procedure  
**`(char>? char₁ char₂ char₃ …)`** — procedure  
**`(char<=? char₁ char₂ char₃ …)`** — procedure  
**`(char>=? char₁ char₂ char₃ …)`** — procedure

<a id="characterequality"></a>

These procedures return `#t` if
the results of passing their arguments to `char->integer`
are respectively
equal, monotonically increasing, monotonically decreasing,
monotonically non-decreasing, or monotonically non-increasing.

These predicates are required to be transitive.

<a id="char-ci"></a>
<a id="char-ci-2"></a>
<a id="char-ci-3"></a>
<a id="char-ci-4"></a>
<a id="char-ci-5"></a>
**`(char-ci=? char₁ char₂ char₃ …)`** — char library procedure  
**`(char-ci<? char₁ char₂ char₃ …)`** — char library procedure  
**`(char-ci>? char₁ char₂ char₃ …)`** — char library procedure  
**`(char-ci<=? char₁ char₂ char₃ …)`** — char library procedure  
**`(char-ci>=? char₁ char₂ char₃ …)`** — char library procedure

These procedures are similar to `char=?` et cetera, but they treat
upper case and lower case letters as the same. For example, `(char-ci=? #\A #\a)` returns `#t`.

Specifically, these procedures behave as if `char-foldcase` were
applied to their arguments before they were compared.

<a id="char-alphabetic"></a>
<a id="char-numeric"></a>
<a id="char-whitespace"></a>
<a id="char-upper-case"></a>
<a id="char-lower-case"></a>
**`(char-alphabetic? char)`** — char library procedure  
**`(char-numeric? char)`** — char library procedure  
**`(char-whitespace? char)`** — char library procedure  
**`(char-upper-case? letter)`** — char library procedure  
**`(char-lower-case? letter)`** — char library procedure

These procedures return `#t` if their arguments are alphabetic,
numeric, whitespace, upper case, or lower case characters, respectively,
otherwise they return `#f`.

Specifically, they must return `#t` when applied to characters with
the Unicode properties Alphabetic, Numeric_Type=Decimal,
White_Space, Uppercase, and
Lowercase respectively, and `#f` when applied to any other Unicode
characters. Note that many Unicode characters are alphabetic but neither
upper nor lower case.

<a id="digit-value"></a>
**`(digit-value char)`** — char library procedure

This procedure returns the numeric value (0 to 9) of its argument
if it is a numeric digit (that is, if `char-numeric?` returns `#t`),
or `#f` on any other character.

```scheme
(digit-value #3)   => 3
(digit-value #x0664)   => 4
(digit-value #x0AE6)   => 0
(digit-value #x0EA6)   => #f
```

<a id="char-integer"></a>
<a id="integer-char"></a>
**`(char->integer char)`** — procedure  
**`(integer->char n)`** — procedure

Given a Unicode character,
`char->integer` returns an exact integer
between 0 and `#xD7FF` or
between `#xE000` and `#x10FFFF`
which is equal to the Unicode scalar value of that character.
Given a non-Unicode character,
it returns an exact integer greater than `#x10FFFF`.
This is true independent of whether the implementation uses
the Unicode representation internally.

Given an exact integer that is the value returned by
a character when `char->integer` is applied to it, `integer->char`
returns that character.

<a id="char-upcase"></a>
<a id="char-downcase"></a>
<a id="char-foldcase"></a>
**`(char-upcase char)`** — char library procedure  
**`(char-downcase char)`** — char library procedure  
**`(char-foldcase char)`** — char library procedure

The `char-upcase` procedure, given an argument that is the
lowercase part of a Unicode casing pair, returns the uppercase member
of the pair, provided that both characters are supported by the Scheme
implementation. Note that language-sensitive casing pairs are not used. If the
argument is not the lowercase member of such a pair, it is returned.

The `char-downcase` procedure, given an argument that is the
uppercase part of a Unicode casing pair, returns the lowercase member
of the pair, provided that both characters are supported by the Scheme
implementation. Note that language-sensitive casing pairs are not used. If the
argument is not the uppercase member of such a pair, it is returned.

The `char-foldcase` procedure applies the Unicode simple
case-folding algorithm to its argument and returns the result. Note that
language-sensitive folding is not used.
If the character that results from folding
is not supported by the implementation,
the argument is returned.
See UAX #44 [[uax44](#cite-uax44)] (part of the Unicode Standard) for details.

Note that many Unicode lowercase characters do not have uppercase
equivalents.

## Strings

<a id="stringsection"></a>

Strings are sequences of characters.
 Strings are written as sequences of characters enclosed within quotation marks
(`"`). Within a string literal, various escape
sequences<a id="escape-sequence"></a> represent characters other than
themselves. Escape sequences always start with a backslash (\):

- `\a` : alarm, U+0007
- `\b` : backspace, U+0008
- `\t` : character tabulation, U+0009
- `\n` : linefeed, U+000A
- `\r` : return, U+000D
- `\“"` : double quote, U+0022
- `\\` : backslash, U+005C
- `\|` : vertical line, U+007C
- `\⟨intraline whitespace⟩⟨line ending⟩
   ⟨intraline whitespace⟩` : nothing
- `\x⟨hex scalar value⟩;` : specified character (note the
   terminating semi-colon).

The result is unspecified if any other character in a string occurs
after a backslash.

Except for a line ending, any character outside of an escape
sequence stands for itself in the string literal. A line ending which
is preceded by `\⟨intraline whitespace⟩` expands
to nothing (along with any trailing intraline whitespace), and can be
used to indent strings for improved legibility. Any other line ending
has the same effect as inserting a `\n` character into
the string.

Examples:

```scheme
"The word "recursion" has many meanings."
"Another example:ntwo lines of text"
"Here's text
   containing just one line"
"x03B1; is named GREEK SMALL LETTER ALPHA."
```

The *length* of a string is the number of characters that it
contains. This number is an exact, non-negative integer that is fixed when the
string is created. The **valid indexes** of a string are the
exact non-negative integers less than the length of the string. The first
character of a string has index 0, the second has index 1, and so on.

Some of the procedures that operate on strings ignore the
difference between upper and lower case. The names of the versions that ignore case
end with “`-ci`” (for “case insensitive”).

Implementations may forbid certain characters from appearing in strings.
However, with the exception of `#\null`, ASCII characters must
not be forbidden.
For example, an implementation might support the entire Unicode repertoire,
but only allow characters U+0001 to U+00FF (the Latin-1 repertoire
without `#\null`) in strings.

It is an error to pass such a forbidden character to
`make-string`, `string`, `string-set!`, or `string-fill!`,
as part of the list passed to `list->string`,
or as part of the vector passed to `vector->string`
(see section [Vectors](#vectortostring)),
or in UTF-8 encoded form within a bytevector passed to
`utf8->string` (see section [Bytevectors](#utf8tostring)).
It is also an error for a procedure passed to `string-map`
(see section [Control features](#stringmap)) to return a forbidden character,
or for `read-string` (see section [Input](#readstring))
to attempt to read one.

<a id="string"></a>
**`(string? obj)`** — procedure

Returns `#t` if *obj* is a string, otherwise returns `#f`.

<a id="make-string"></a>
**`(make-string k)`** — procedure  
**`(make-string k char)`** — procedure

The `make-string` procedure returns a newly allocated string of
length *k*. If *char* is given, then all the characters of the string
are initialized to *char*, otherwise the contents of the
string are unspecified.

<a id="string-2"></a>
**`(string char …)`** — procedure

Returns a newly allocated string composed of the arguments.
It is analogous to `list`.

<a id="string-length"></a>
**`(string-length string)`** — procedure

Returns the number of characters in the given *string*.

<a id="string-ref"></a>
**`(string-ref string k)`** — procedure

It is an error if *k* is not a valid index of *string*.
The `string-ref` procedure returns character *k* of *string* using zero-origin indexing.

There is no requirement for this procedure to execute in constant time.

<a id="string-set"></a>
**`(string-set! string k char)`** — procedure

It is an error if *k* is not a valid index of *string*.
The `string-set!` procedure stores *char* in element *k* of *string*.
There is no requirement for this procedure to execute in constant time.

```scheme
(define (f) (make-string 3 #*))
(define (g) "***")
(string-set! (f) 0 #?)    =>  unspecified
(string-set! (g) 0 #?)    =>  error
(string-set! (symbol->string 'immutable)
             0
             #?)    =>  error
```

<a id="string-3"></a>
**`(string=? string₁ string₂ string₃ …)`** — procedure

Returns `#t` if all the strings are the same length and contain
exactly the same characters in the same positions, otherwise returns
`#f`.

<a id="string-ci"></a>
**`(string-ci=? string₁ string₂ string₃ …)`** — char library procedure

Returns `#t` if, after case-folding, all the strings are the same
length and contain the same characters in the same positions, otherwise
returns `#f`. Specifically, these procedures behave as if
`string-foldcase` were applied to their arguments before comparing them.

<a id="string-4"></a>
<a id="string-ci-2"></a>
<a id="string-5"></a>
<a id="string-ci-3"></a>
<a id="string-6"></a>
<a id="string-ci-4"></a>
<a id="string-7"></a>
<a id="string-ci-5"></a>
**`(string<? string₁ string₂ string₃ …)`** — procedure  
**`(string-ci<? string₁ string₂ string₃ …)`** — char library procedure  
**`(string>? string₁ string₂ string₃ …)`** — procedure  
**`(string-ci>? string₁ string₂ string₃ …)`** — char library procedure  
**`(string<=? string₁ string₂ string₃ …)`** — procedure  
**`(string-ci<=? string₁ string₂ string₃ …)`** — char library procedure  
**`(string>=? string₁ string₂ string₃ …)`** — procedure  
**`(string-ci>=? string₁ string₂ string₃ …)`** — char library procedure

These procedures return `#t` if their arguments are (respectively):
monotonically increasing, monotonically decreasing,
monotonically non-decreasing, or monotonically non-increasing.

These predicates are required to be transitive.

These procedures compare strings in an implementation-defined way.
One approach is to make them the lexicographic extensions to strings of
the corresponding orderings on characters. In that case, `string<?`
would be the lexicographic ordering on strings induced by the ordering
`char<?` on characters, and if the two strings differ in length but
are the same up to the length of the shorter string, the shorter string
would be considered to be lexicographically less than the longer string.
However, it is also permitted to use the natural ordering imposed by the
implementation's internal representation of strings, or a more complex locale-specific
ordering.

In all cases, a pair of strings must satisfy exactly one of
`string<?`, `string=?`, and `string>?`, and must satisfy
`string<=?` if and only if they do not satisfy `string>?` and
`string>=?` if and only if they do not satisfy `string<?`.

The “`-ci`” procedures behave as if they applied
`string-foldcase` to their arguments before invoking the corresponding
procedures without “`-ci`”.

<a id="string-upcase"></a>
<a id="string-downcase"></a>
<a id="string-foldcase"></a>
**`(string-upcase string)`** — char library procedure  
**`(string-downcase string)`** — char library procedure  
**`(string-foldcase string)`** — char library procedure

These procedures apply the Unicode full string uppercasing, lowercasing,
and case-folding algorithms to their arguments and return the result.
In certain cases, the result differs in length from the argument.
If the result is equal to the argument in the sense of `string=?`, the argument may be returned.
Note that language-sensitive mappings and foldings are not used.

The Unicode Standard prescribes special treatment of the Greek letter
$\Sigma$, whose normal lower-case form is $\sigma$ but which becomes
$\varsigma$ at the end of a word. See UAX #44 [[uax44](#cite-uax44)] (part of
the Unicode Standard) for details. However, implementations of `string-downcase` are not required to provide this behavior, and may
choose to change $\Sigma$ to $\sigma$ in all cases.

<a id="substring"></a>
**`(substring string start end)`** — procedure

The `substring` procedure returns a newly allocated string formed from the characters of
*string* beginning with index *start* and ending with index
*end*.
This is equivalent to calling `string-copy` with the same arguments,
but is provided for backward compatibility and
stylistic flexibility.

<a id="string-append"></a>
**`(string-append string …)`** — procedure

Returns a newly allocated string whose characters are the concatenation of the
characters in the given strings.

<a id="string-list"></a>
<a id="list-string"></a>
**`(string->list string)`** — procedure  
**`(string->list string start)`** — procedure  
**`(string->list string start end)`** — procedure  
**`(list->string list)`** — procedure

It is an error if any element of *list* is not a character.
The `string->list` procedure returns a newly allocated list of the
characters of *string* between *start* and *end*.
`list->string`
returns a newly allocated string formed from the elements in the list
*list*.
In both procedures, order is preserved.
`string->list`
and `list->string` are
inverses so far as `equal?` is concerned.

<a id="string-copy"></a>
**`(string-copy string)`** — procedure  
**`(string-copy string start)`** — procedure  
**`(string-copy string start end)`** — procedure

Returns a newly allocated copy of the part of the given *string*
between *start* and *end*.

<a id="string-copy-2"></a>
**`(string-copy! to at from)`** — procedure  
**`(string-copy! to at from start)`** — procedure  
**`(string-copy! to at from start end)`** — procedure

It is an error if *at* is less than zero or greater than the length of *to*.
It is also an error if `(- (string-length to) at)`
is less than `(- end start)`.
Copies the characters of string *from* between *start* and *end*
to string *to*, starting at *at*. The order in which characters are
copied is unspecified, except that if the source and destination overlap,
copying takes place as if the source is first copied into a temporary
string and then into the destination. This can be achieved without
allocating storage by making sure to copy in the correct direction in
such circumstances.

```scheme
(define a "12345")
(define b (string-copy "abcde"))
(string-copy! b 1 a 0 2)
b   => "a12de"
```

<a id="string-fill"></a>
**`(string-fill! string fill)`** — procedure  
**`(string-fill! string fill start)`** — procedure  
**`(string-fill! string fill start end)`** — procedure

It is an error if *fill* is not a character.

The `string-fill!` procedure stores *fill*
in the elements of *string*
between *start* and *end*.

## Vectors

<a id="vectorsection"></a>

Vectors are heterogeneous structures whose elements are indexed
by integers. A vector typically occupies less space than a list
of the same length, and the average time needed to access a randomly
chosen element is typically less for the vector than for the list.

The *length* of a vector is the number of elements that it
contains. This number is a non-negative integer that is fixed when the
vector is created. The *valid indexes* of a
vector are the exact non-negative integers less than the length of the
vector. The first element in a vector is indexed by zero, and the last
element is indexed by one less than the length of the vector.

Vectors are written using the notation `#(obj …)`.
For example, a vector of length 3 containing the number zero in element
0, the list `(2 2 2 2)` in element 1, and the string `"Anna"` in
element 2 can be written as follows:

```scheme
#(0 (2 2 2 2) "Anna")
```

Vector constants are self-evaluating, so they do not need to be quoted in programs.

<a id="vector"></a>
**`(vector? obj)`** — procedure

Returns `#t` if *obj* is a vector; otherwise returns `#f`.

<a id="make-vector"></a>
**`(make-vector k)`** — procedure  
**`(make-vector k fill)`** — procedure

Returns a newly allocated vector of *k* elements. If a second
argument is given, then each element is initialized to *fill*.
Otherwise the initial contents of each element is unspecified.

<a id="vector-2"></a>
**`(vector obj …)`** — procedure

Returns a newly allocated vector whose elements contain the given
arguments. It is analogous to `list`.

```scheme
(vector 'a 'b 'c)                 =>  #(a b c)
```

<a id="vector-length"></a>
**`(vector-length vector)`** — procedure

Returns the number of elements in *vector* as an exact integer.

<a id="vector-ref"></a>
**`(vector-ref vector k)`** — procedure

It is an error if *k* is not a valid index of *vector*.
The `vector-ref` procedure returns the contents of element *k* of
*vector*.

```scheme
(vector-ref '#(1 1 2 3 5 8 13 21)
            5)  =>  8
(vector-ref '#(1 1 2 3 5 8 13 21)
            (exact
             (round (* 2 (acos -1))))) => 13
```

<a id="vector-set"></a>
**`(vector-set! vector k obj)`** — procedure

It is an error if *k* is not a valid index of *vector*.
The `vector-set!` procedure stores *obj* in element *k* of *vector*.

```scheme
(let ((vec (vector 0 '(2 2 2 2) "Anna")))
  (vector-set! vec 1 '("Sue" "Sue"))
  vec)      =>  #(0 ("Sue" "Sue") "Anna")

(vector-set! '#(0 1 2) 1 "doe")  =>  error  ; constant vector
```

<a id="vector-list"></a>
<a id="list-vector"></a>
**`(vector->list vector)`** — procedure  
**`(vector->list vector start)`** — procedure  
**`(vector->list vector start end)`** — procedure  
**`(list->vector list)`** — procedure

The `vector->list` procedure returns a newly allocated list of the objects contained
in the elements of *vector* between *start* and *end*.
The `list->vector` procedure returns a newly
created vector initialized to the elements of the list *list*.

In both procedures, order is preserved.

```scheme
(vector->list '#(dah dah didah))  =>  (dah dah didah)
(vector->list '#(dah dah didah) 1 2) => (dah)
(list->vector '(dididit dah))   =>  #(dididit dah)
```

<a id="vector-string"></a>
<a id="string-vector"></a>
**`(vector->string vector)`** — procedure  
**`(vector->string vector start)`** — procedure  
**`(vector->string vector start end)`** — procedure  
**`(string->vector string)`** — procedure  
**`(string->vector string start)`** — procedure  
**`(string->vector string start end)`** — procedure

<a id="vectortostring"></a>

It is an error if any element of *vector* between *start*
and *end* is not a character.
The `vector->string` procedure returns a newly allocated string of the objects contained
in the elements of *vector*
between *start* and *end*.
The `string->vector` procedure returns a newly
created vector initialized to the elements of the string *string*
between *start* and *end*.

In both procedures, order is preserved.

```scheme
(string->vector "ABC")    =>   #(#A #B #C)
(vector->string
  #(#1 #2 #3)   => "123"
```

<a id="vector-copy"></a>
**`(vector-copy vector)`** — procedure  
**`(vector-copy vector start)`** — procedure  
**`(vector-copy vector start end)`** — procedure

Returns a newly allocated copy of the elements of the given *vector*
between *start* and *end*.
The elements of the new vector are the same (in the sense of
`eqv?`) as the elements of the old.

```scheme
(define a #(1 8 2 8)) ; a may be immutable
(define b (vector-copy a))
(vector-set! b 0 3)   ; b is mutable
b   => #(3 8 2 8)
(define c (vector-copy b 1 3))
c   => #(8 2)
```

<a id="vector-copy-2"></a>
**`(vector-copy! to at from)`** — procedure  
**`(vector-copy! to at from start)`** — procedure  
**`(vector-copy! to at from start end)`** — procedure

It is an error if *at* is less than zero or greater than the length of *to*.
It is also an error if `(- (vector-length to) at)`
is less than `(- end start)`.
Copies the elements of vector *from* between *start* and *end*
to vector *to*, starting at *at*. The order in which elements are
copied is unspecified, except that if the source and destination overlap,
copying takes place as if the source is first copied into a temporary
vector and then into the destination. This can be achieved without
allocating storage by making sure to copy in the correct direction in
such circumstances.

```scheme
(define a (vector 1 2 3 4 5))
(define b (vector 10 20 30 40 50))
(vector-copy! b 1 a 0 2)
b   => #(10 1 2 40 50)
```

<a id="vector-append"></a>
**`(vector-append vector …)`** — procedure

Returns a newly allocated vector whose elements are the concatenation
of the elements of the given vectors.

```scheme
(vector-append #(a b c) #(d e f)) => #(a b c d e f)
```

<a id="vector-fill"></a>
**`(vector-fill! vector fill)`** — procedure  
**`(vector-fill! vector fill start)`** — procedure  
**`(vector-fill! vector fill start end)`** — procedure

The `vector-fill!` procedure stores *fill*
in the elements of *vector*
between *start* and *end*.

```scheme
(define a (vector 1 2 3 4 5))
(vector-fill! a 'smash 2 4)
a => #(1 2 smash smash 5)
```

## Bytevectors

<a id="bytevectorsection"></a>

They are fixed-length sequences of bytes, where
a **byte** is an exact integer in the range from 0 to 255 inclusive.
A bytevector is typically more space-efficient than a vector
containing the same values.

The *length* of a bytevector is the number of elements that it
contains. This number is a non-negative integer that is fixed when
the bytevector is created. The *valid indexes* of
a bytevector are the exact non-negative integers less than the length of the
bytevector, starting at index zero as with vectors.

Bytevectors are written using the notation `#u8(byte …)`.
For example, a bytevector of length 3 containing the byte 0 in element
0, the byte 10 in element 1, and the byte 5 in
element 2 can be written as follows:

```scheme
#u8(0 10 5)
```

Bytevector constants are self-evaluating, so they do not need to be quoted in programs.

<a id="bytevector"></a>
**`(bytevector? obj)`** — procedure

Returns `#t` if *obj* is a bytevector.
Otherwise, `#f` is returned.

<a id="make-bytevector"></a>
**`(make-bytevector k)`** — procedure  
**`(make-bytevector k byte)`** — procedure

The `make-bytevector` procedure returns a newly allocated bytevector of
length *k*. If *byte* is given, then all elements of the bytevector
are initialized to *byte*, otherwise the contents of each
element are unspecified.

```scheme
(make-bytevector 2 12)   => #u8(12 12)
```

<a id="bytevector-2"></a>
**`(bytevector byte …)`** — procedure

Returns a newly allocated bytevector containing its arguments.

```scheme
(bytevector 1 3 5 1 3 5)          =>  #u8(1 3 5 1 3 5)
(bytevector)                            =>  #u8()
```

<a id="bytevector-length"></a>
**`(bytevector-length bytevector)`** — procedure

Returns the length of *bytevector* in bytes as an exact integer.

<a id="bytevector-u8-ref"></a>
**`(bytevector-u8-ref bytevector k)`** — procedure

It is an error if *k* is not a valid index of *bytevector*.
Returns the *k*th byte of *bytevector*.

```scheme
(bytevector-u8-ref '#u8(1 1 2 3 5 8 13 21)
            5)  =>  8
```

<a id="bytevector-u8-set"></a>
**`(bytevector-u8-set! bytevector k byte)`** — procedure

It is an error if *k* is not a valid index of *bytevector*.
Stores *byte* as the *k*th byte of *bytevector*.

```scheme
(let ((bv (bytevector 1 2 3 4)))
  (bytevector-u8-set! bv 1 3)
  bv) => #u8(1 3 3 4)
```

<a id="bytevector-copy"></a>
**`(bytevector-copy bytevector)`** — procedure  
**`(bytevector-copy bytevector start)`** — procedure  
**`(bytevector-copy bytevector start end)`** — procedure

Returns a newly allocated bytevector containing the bytes in *bytevector*
between *start* and *end*.

```scheme
(define a #u8(1 2 3 4 5))
(bytevector-copy a 2 4))   => #u8(3 4)
```

<a id="bytevector-copy-2"></a>
**`(bytevector-copy! to at from)`** — procedure  
**`(bytevector-copy! to at from start)`** — procedure  
**`(bytevector-copy! to at from start end)`** — procedure

It is an error if *at* is less than zero or greater than the length of *to*.
It is also an error if `(- (bytevector-length to) at)`
is less than `(- end start)`.
Copies the bytes of bytevector *from* between *start* and *end*
to bytevector *to*, starting at *at*. The order in which bytes are
copied is unspecified, except that if the source and destination overlap,
copying takes place as if the source is first copied into a temporary
bytevector and then into the destination. This can be achieved without
allocating storage by making sure to copy in the correct direction in
such circumstances.

```scheme
(define a (bytevector 1 2 3 4 5))
(define b (bytevector 10 20 30 40 50))
(bytevector-copy! b 1 a 0 2)
b   => #u8(10 1 2 40 50)
```

> **Note:** This procedure appears in R⁶RS, but places the source before the destination,
> contrary to other such procedures in Scheme.

<a id="bytevector-append"></a>
**`(bytevector-append bytevector …)`** — procedure

Returns a newly allocated bytevector whose elements are the concatenation
of the elements in the given bytevectors.

```scheme
(bytevector-append #u8(0 1 2) #u8(3 4 5)) => #u8(0 1 2 3 4 5)
```

<a id="utf8tostring"></a>

<a id="utf8-string"></a>
<a id="string-utf8"></a>
**`(utf8->string bytevector)`** — procedure  
**`(utf8->string bytevector start)`** — procedure  
**`(utf8->string bytevector start end)`** — procedure  
**`(string->utf8 string)`** — procedure  
**`(string->utf8 string start)`** — procedure  
**`(string->utf8 string start end)`** — procedure

It is an error for *bytevector* to contain invalid UTF-8 byte sequences.
These procedures translate between strings and bytevectors
that encode those strings using the UTF-8 encoding.
The `utf8->string` procedure decodes the bytes of
a bytevector between *start* and *end*
and returns the corresponding string;
the `string->utf8` procedure encodes the characters of a
string between *start* and *end*
and returns the corresponding bytevector.

```scheme
(utf8->string #u8(#x41))   => "A"
(string->utf8 "$\lambda$")   => #u8(#xCE #xBB)
```

## Control features

<a id="proceduresection"></a>

This section describes various primitive procedures which control the
flow of program execution in special ways.
Procedures in this section that invoke procedure arguments
always do so in the same dynamic environment as the call of the
original procedure.
The `procedure?` predicate is also described here.

<a id="procedure-2"></a>
**`(procedure? obj)`** — procedure

Returns `#t` if *obj* is a procedure, otherwise returns `#f`.

```scheme
(procedure? car)              =>  #t
(procedure? 'car)             =>  #f
(procedure? (lambda (x) (* x x)))
                              =>  #t
(procedure? '(lambda (x) (* x x)))
                              =>  #f
(call-with-current-continuation procedure?)
                              =>  #t
```

<a id="apply"></a>
**`(apply proc arg₁ $\dots$ args)`** — procedure

The `apply` procedure calls *proc* with the elements of the list
`(append (list arg₁ …) args)` as the actual
arguments.

```scheme
(apply + (list 3 4))                =>  7

(define compose
  (lambda (f g)
    (lambda args
      (f (apply g args)))))

((compose sqrt *) 12 75)                =>  30
```

<a id="map"></a>
**`(map proc list₁ list₂ …)`** — procedure

It is an error if *proc* does not
accept as many arguments as there are *list*s
and return a single value.
The `map` procedure applies *proc* element-wise to the elements of the
*list*s and returns a list of the results, in order.
If more than one *list* is given and not all lists have the same length,
`map` terminates when the shortest list runs out.
The *list*s can be circular, but it is an error if all of them are circular.
It is an error for *proc* to mutate any of the lists.
The dynamic order in which *proc* is applied to the elements of the
*list*s is unspecified. If multiple returns occur from `map`,
the values returned by earlier returns are not mutated.

```scheme
(map cadr '((a b) (d e) (g h)))   =>  (b e h)

(map (lambda (n) (expt n n))
     '(1 2 3 4 5))                =>  (1 4 27 256 3125)

(map + '(1 2 3) '(4 5 6 7))           =>  (5 7 9)

(let ((count 0))
  (map (lambda (ignored)
         (set! count (+ count 1))
         count)
       '(a b)))                   =>  (1 2) or (2 1)
```

<a id="string-map"></a>
**`(string-map proc string₁ string₂ …)`** — procedure

<a id="stringmap"></a>

It is an error if *proc* does not
accept as many arguments as there are *string*s
and return a single character.
The `string-map` procedure applies *proc* element-wise to the elements of the
*string*s and returns a string of the results, in order.
If more than one *string* is given and not all strings have the same length,
`string-map` terminates when the shortest string runs out.
The dynamic order in which *proc* is applied to the elements of the
*string*s is unspecified.
If multiple returns occur from `string-map`,
the values returned by earlier returns are not mutated.

```scheme
(string-map char-foldcase "AbdEgH") =>  "abdegh"

(string-map
 (lambda (c)
   (integer->char (+ 1 (char->integer c))))
 "HAL")                =>  "IBM"

(string-map
 (lambda (c k)
   ((if (eqv? k #u) char-upcase char-downcase)
    c))
 "studlycaps xxx"
 "ululululul")   =>   "StUdLyCaPs"
```

<a id="vector-map"></a>
**`(vector-map proc vector₁ vector₂ …)`** — procedure

It is an error if *proc* does not
accept as many arguments as there are *vector*s
and return a single value.
The `vector-map` procedure applies *proc* element-wise to the elements of the
*vector*s and returns a vector of the results, in order.
If more than one *vector* is given and not all vectors have the same length,
`vector-map` terminates when the shortest vector runs out.
The dynamic order in which *proc* is applied to the elements of the
*vector*s is unspecified.
If multiple returns occur from `vector-map`,
the values returned by earlier returns are not mutated.

```scheme
(vector-map cadr '#((a b) (d e) (g h)))   =>  #(b e h)

(vector-map (lambda (n) (expt n n))
            '#(1 2 3 4 5))                =>  #(1 4 27 256 3125)

(vector-map + '#(1 2 3) '#(4 5 6 7))       =>  #(5 7 9)

(let ((count 0))
  (vector-map
   (lambda (ignored)
     (set! count (+ count 1))
     count)
   '#(a b)))                       =>  #(1 2) or #(2 1)
```

<a id="for-each"></a>
**`(for-each proc list₁ list₂ …)`** — procedure

It is an error if *proc* does not
accept as many arguments as there are *list*s.
The arguments to `for-each` are like the arguments to `map`, but
`for-each` calls *proc* for its side effects rather than for its
values. Unlike `map`, `for-each` is guaranteed to call *proc* on
the elements of the *list*s in order from the first element(s) to the
last, and the value returned by `for-each` is unspecified.
If more than one *list* is given and not all lists have the same length,
`for-each` terminates when the shortest list runs out.
The *list*s can be circular, but it is an error if all of them are circular.

It is an error for *proc* to mutate any of the lists.

```scheme
(let ((v (make-vector 5)))
  (for-each (lambda (i)
              (vector-set! v i (* i i)))
            '(0 1 2 3 4))
  v)                                  =>  #(0 1 4 9 16)
```

<a id="string-for-each"></a>
**`(string-for-each proc string₁ string₂ …)`** — procedure

It is an error if *proc* does not
accept as many arguments as there are *string*s.
The arguments to `string-for-each` are like the arguments to `string-map`, but `string-for-each` calls *proc* for its side
effects rather than for its values. Unlike `string-map`, `string-for-each` is guaranteed to call *proc* on the elements of
the *string*s in order from the first element(s) to the last, and the
value returned by `string-for-each` is unspecified.
If more than one *string* is given and not all strings have the same length,
`string-for-each` terminates when the shortest string runs out.
It is an error for *proc* to mutate any of the strings.

```scheme
(let ((v '()))
  (string-for-each
   (lambda (c) (set! v (cons (char->integer c) v)))
   "abcde")
  v)                           =>  (101 100 99 98 97)
```

<a id="vector-for-each"></a>
**`(vector-for-each proc vector₁ vector₂ …)`** — procedure

It is an error if *proc* does not
accept as many arguments as there are *vector*s.
The arguments to `vector-for-each` are like the arguments to `vector-map`, but `vector-for-each` calls *proc* for its side
effects rather than for its values. Unlike `vector-map`, `vector-for-each` is guaranteed to call *proc* on the elements of
the *vector*s in order from the first element(s) to the last, and
the value returned by `vector-for-each` is unspecified.
If more than one *vector* is given and not all vectors have the same length,
`vector-for-each` terminates when the shortest vector runs out.
It is an error for *proc* to mutate any of the vectors.

```scheme
(let ((v (make-list 5)))
  (vector-for-each
   (lambda (i) (list-set! v i (* i i)))
   '#(0 1 2 3 4))
  v)                                  =>  (0 1 4 9 16)
```

<a id="call-with-current-continuation"></a>
<a id="call-cc"></a>
**`(call-with-current-continuation proc)`** — procedure  
**`(call/cc proc)`** — procedure

<a id="continuations"></a> It is an error if *proc* does not accept one
argument.
The procedure `call-with-current-continuation` (or its
equivalent abbreviation `call/cc`) packages
the current continuation (see the rationale below) as an “escape
procedure”<a id="escape-procedure"></a> and passes it as an argument to
*proc*.
The escape procedure is a Scheme procedure that, if it is
later called, will abandon whatever continuation is in effect at that later
time and will instead use the continuation that was in effect
when the escape procedure was created. Calling the escape procedure
will cause the invocation of *before* and *after* thunks installed using
`dynamic-wind`.

The escape procedure accepts the same number of arguments as the continuation to
the original call to `call-with-current-continuation`.
Most continuations take only one value.
Continuations created by the `call-with-values`
procedure (including the initialization expressions of
`define-values`, `let-values`, and `let*-values` expressions),
take the number of values that the consumer expects.
The continuations of all non-final expressions within a sequence
of expressions, such as in `lambda`, `case-lambda`, `begin`,
`let`, `let*`, `letrec`, `letrec*`, `let-values`,
`let*-values`, `let-syntax`, `letrec-syntax`, `parameterize`,
`guard`, `case`, `cond`, `when`, and `unless` expressions,
take an arbitrary number of values because they discard the values passed
to them in any event.
The effect of passing no values or more than one value to continuations
that were not created in one of these ways is unspecified.

The escape procedure that is passed to *proc* has
unlimited extent just like any other procedure in Scheme. It can be stored
in variables or data structures and can be called as many times as desired.
However, like the `raise` and `error` procedures, it never
returns to its caller.

The following examples show only the simplest ways in which
`call-with-current-continuation` is used. If all real uses were as
simple as these examples, there would be no need for a procedure with
the power of `call-with-current-continuation`.

```scheme
(call-with-current-continuation
  (lambda (exit)
    (for-each (lambda (x)
                (if (negative? x)
                    (exit x)))
              '(54 0 37 -3 245 19))
    #t))                          =>  -3

(define list-length
  (lambda (obj)
    (call-with-current-continuation
      (lambda (return)
        (letrec ((r
                  (lambda (obj)
                    (cond ((null? obj) 0)
                          ((pair? obj)
                           (+ (r (cdr obj)) 1))
                          (else (return #f))))))
          (r obj))))))

(list-length '(1 2 3 4))              =>  4

(list-length '(a b . c))              =>  #f
```

> **Rationale:** A common use of `call-with-current-continuation` is for
> structured, non-local exits from loops or procedure bodies, but in fact
> `call-with-current-continuation` is useful for implementing a
> wide variety of advanced control structures.
> In fact, `raise` and `guard` provide a more structured mechanism
> for non-local exits.
>
>
> Whenever a Scheme expression is evaluated there is a
> **continuation** wanting the result of the expression. The continuation
> represents an entire (default) future for the computation. If the expression is
> evaluated at the REPL, for example, then the continuation might take the
> result, print it on the screen, prompt for the next input, evaluate it, and
> so on forever. Most of the time the continuation includes actions
> specified by user code, as in a continuation that will take the result,
> multiply it by the value stored in a local variable, add seven, and give
> the answer to the REPL's continuation to be printed. Normally these
> ubiquitous continuations are hidden behind the scenes and programmers do not
> think much about them. On rare occasions, however, a programmer
> needs to deal with continuations explicitly.
> The `call-with-current-continuation` procedure allows Scheme programmers to do
> that by creating a procedure that acts just like the current
> continuation.

<a id="values"></a>
**`(values obj $\dots$)`** — procedure

Delivers all of its arguments to its continuation.
The `values` procedure might be defined as follows:

```scheme
(define (values . things)
  (call-with-current-continuation
    (lambda (cont) (apply cont things))))
```

<a id="call-with-values"></a>
**`(call-with-values producer consumer)`** — procedure

Calls its *producer* argument with no arguments and
a continuation that, when passed some values, calls the
*consumer* procedure with those values as arguments.
The continuation for the call to *consumer* is the
continuation of the call to `call-with-values`.

```scheme
(call-with-values (lambda () (values 4 5))
                  (lambda (a b) b))
                                                     =>  5

(call-with-values * -)                               =>  -1
```

<a id="dynamic-wind"></a>
**`(dynamic-wind before thunk after)`** — procedure

Calls *thunk* without arguments, returning the result(s) of this call.
*Before* and *after* are called, also without arguments, as required
by the following rules. Note that, in the absence of calls to continuations
captured using `call-with-current-continuation`, the three arguments are
called once each, in order. *Before* is called whenever execution
enters the dynamic extent of the call to *thunk* and *after* is called
whenever it exits that dynamic extent. The dynamic extent of a procedure
call is the period between when the call is initiated and when it
returns.
The *before* and *after* thunks are called in the same dynamic
environment as the call to `dynamic-wind`.
In Scheme, because of `call-with-current-continuation`, the
dynamic extent of a call is not always a single, connected time period.
It is defined as follows:

- The dynamic extent is entered when execution of the body of the
  called procedure begins.
- The dynamic extent is also entered when execution is not within
  the dynamic extent and a continuation is invoked that was captured
  (using `call-with-current-continuation`) during the dynamic extent.
- It is exited when the called procedure returns.
- It is also exited when execution is within the dynamic extent and
  a continuation is invoked that was captured while not within the
  dynamic extent.

If a second call to `dynamic-wind` occurs within the dynamic extent of the
call to *thunk* and then a continuation is invoked in such a way that the
*after*s from these two invocations of `dynamic-wind` are both to be
called, then the *after* associated with the second (inner) call to
`dynamic-wind` is called first.

If a second call to `dynamic-wind` occurs within the dynamic extent of the
call to *thunk* and then a continuation is invoked in such a way that the
*before*s from these two invocations of `dynamic-wind` are both to be
called, then the *before* associated with the first (outer) call to
`dynamic-wind` is called first.

If invoking a continuation requires calling the *before* from one call
to `dynamic-wind` and the *after* from another, then the *after*
is called first.

The effect of using a captured continuation to enter or exit the dynamic
extent of a call to *before* or *after* is unspecified.

```scheme
(let ((path '())
      (c #f))
  (let ((add (lambda (s)
               (set! path (cons s path)))))
    (dynamic-wind
      (lambda () (add 'connect))
      (lambda ()
        (add (call-with-current-continuation
               (lambda (c0)
                 (set! c c0)
                 'talk1))))
      (lambda () (add 'disconnect)))
    (if (< (length path) 4)
        (c 'talk2)
        (reverse path))))
    => (connect talk1 disconnect
               connect talk2 disconnect)
```

## Exceptions

<a id="exceptionsection"></a>

This section describes Scheme's exception-handling and
exception-raising procedures.
For the concept of Scheme exceptions, see section [Error situations and unspecified behavior](#errorsituations).
See also [guard](#guard) for the `guard` syntax.

action the program takes when an exceptional situation is signaled.
The system implicitly maintains a current exception handler
in the dynamic environment.

The program raises an exception by
invoking the current exception handler, passing it an object
encapsulating information about the exception. Any procedure
accepting one argument can serve as an exception handler and any
object can be used to represent an exception.

<a id="with-exception-handler"></a>
**`(with-exception-handler handler thunk)`** — procedure

It is an error if *handler* does not accept one argument.
It is also an error if *thunk* does not accept zero arguments.
The `with-exception-handler` procedure returns the results of invoking
*thunk*. *Handler* is installed as the current
exception handler
in the dynamic environment used for the invocation of *thunk*.

```scheme
(call-with-current-continuation
 (lambda (k)
  (with-exception-handler
   (lambda (x)
    (display "condition: ")
    (write x)
    (newline)
    (k 'exception))
   (lambda ()
    (+ 1 (raise 'an-error))))))
          => exception
 and prints  condition: an-error

(with-exception-handler
 (lambda (x)
  (display "something went wrongn"))
 (lambda ()
  (+ 1 (raise 'an-error))))
 prints  something went wrong
```

After printing, the second example then raises another exception.

<a id="raise"></a>
**`(raise obj)`** — procedure

Raises an exception by invoking the current exception
handler on *obj*. The handler is called with the same
dynamic environment as that of the call to `raise`, except that
the current exception handler is the one that was in place when the
handler being called was installed. If the handler returns, a secondary
exception is raised in the same dynamic environment as the handler.
The relationship between *obj* and the object raised by
the secondary exception is unspecified.

<a id="raise-continuable"></a>
**`(raise-continuable obj)`** — procedure

Raises an exception by invoking the current
exception handler on *obj*. The handler is called with
the same dynamic environment as the call to
`raise-continuable`, except that: (1) the current
exception handler is the one that was in place when the handler being
called was installed, and (2) if the handler being called returns,
then it will again become the current exception handler. If the
handler returns, the values it returns become the values returned by
the call to `raise-continuable`.

```scheme
(with-exception-handler
  (lambda (con)
    (cond
      ((string? con)
       (display con))
      (else
       (display "a warning has been issued")))
    42)
  (lambda ()
    (+ (raise-continuable "should be a number")
       23)))
   prints: should be a number
     => 65
```

<a id="error"></a>
**`(error message obj $\dots$)`** — procedure

*Message* should be a string.
Raises an exception as if by calling
`raise` on a newly allocated implementation-defined object which encapsulates
the information provided by *message*,
as well as any *obj*s, known as the **irritants**.
The procedure `error-object?` must return `#t` on such objects.

```scheme
(define (null-list? l)
  (cond ((pair? l) #f)
        ((null? l) #t)
        (else
          (error
            "null-list?: argument out of domain"
            l))))
```

<a id="error-object"></a>
**`(error-object? obj)`** — procedure

Returns `#t` if *obj* is an object created by `error`
or one of an implementation-defined set of objects. Otherwise, it returns
`#f`.
The objects used to signal errors, including those which satisfy the
predicates `file-error?` and `read-error?`, may or may not
satisfy `error-object?`.

<a id="error-object-message"></a>
**`(error-object-message error-object)`** — procedure

Returns the message encapsulated by *error-object*.

<a id="error-object-irritants"></a>
**`(error-object-irritants error-object)`** — procedure

Returns a list of the irritants encapsulated by *error-object*.

<a id="read-error"></a>
<a id="file-error"></a>
**`(read-error? obj)`** — procedure  
**`(file-error? obj)`** — procedure

Error type predicates. Returns `#t` if *obj* is an
object raised by the `read` procedure or by the inability to open
an input or output port on a file, respectively. Otherwise, it
returns `#f`.

## Environments and evaluation

<a id="environment"></a>
**`(environment list₁ …)`** — eval library procedure

<a id="environments"></a>

This procedure returns a specifier for the environment that results by
starting with an empty environment and then importing each *list*,
considered as an import set, into it. (See section [Libraries](#libraries) for
a description of import sets.) The bindings of the environment
represented by the specifier are immutable, as is the environment itself.

<a id="scheme-report-environment"></a>
**`(scheme-report-environment version)`** — r5rs library procedure

If *version* is equal to `5`,
corresponding to R⁵RS,
`scheme-report-environment` returns a specifier for an
environment that contains only the bindings
defined in the R⁵RS library.
Implementations must support this value of *version*.

Implementations may also support other values of *version*, in which
case they return a specifier for an environment containing bindings corresponding to the specified version of the report.
If *version*
is neither `5` nor another value supported by
the implementation, an error is signaled.

The effect of defining or assigning (through the use of `eval`)
an identifier bound in a `scheme-report-environment` (for example
`car`) is unspecified. Thus both the environment and the bindings
it contains may be immutable.

<a id="null-environment"></a>
**`(null-environment version)`** — r5rs library procedure

If *version* is equal to `5`,
corresponding to R⁵RS,
the `null-environment` procedure returns
a specifier for an environment that contains only the
bindings for all syntactic keywords
defined in the R⁵RS library.
Implementations must support this value of *version*.

Implementations may also support other values of *version*, in which
case they return a specifier for an environment containing appropriate bindings corresponding to the specified version of the report.
If *version*
is neither `5` nor another value supported by
the implementation, an error is signaled.

The effect of defining or assigning (through the use of `eval`)
an identifier bound in a `null-environment` (for example
`car`) is unspecified. Thus both the environment and the bindings
it contains may be immutable.

<a id="interaction-environment"></a>
**`(interaction-environment)`** — repl library procedure

This procedure returns a specifier for a mutable environment that contains an
imple­men­ta­tion-defined set of bindings, typically a superset of
those exported by `(scheme base)`. The intent is that this procedure
will return the environment in which the implementation would evaluate
expressions entered by the user into a REPL.

<a id="eval"></a>
**`(eval expr-or-def environment-specifier)`** — eval library procedure

If *expr-or-def* is an expression, it is evaluated in the
specified environment and its values are returned.
If it is a definition, the specified identifier(s) are defined in the specified
environment, provided the environment is not immutable.
Implementations may extend `eval` to allow other objects.

```scheme
(eval '(* 7 3) (environment '(scheme base)))
                                                     =>  21

(let ((f (eval '(lambda (f x) (f x x))
               (null-environment 5))))
  (f + 10))
                                                     =>  20
(eval '(define foo 32)
      (environment '(scheme base)))
                                                     =>  error is signaled
```

## Input and output

### Ports

<a id="portsection"></a>

Ports represent input and output devices. To Scheme, an input port is
a Scheme object that can deliver data upon command, while an output
port is a Scheme object that can accept data.<a id="port"></a>
Whether the input and output port types are disjoint is
implementation-dependent.

Different *port types* operate on different data. Scheme
imple­men­ta­tions are required to support *textual ports*
and *binary ports*, but may also provide other port types.

A textual port supports reading or writing of individual characters
from or to a backing store containing characters
using `read-char` and `write-char` below, and it supports operations
defined in terms of characters, such as `read` and `write`.

A binary port supports reading or writing of individual bytes from
or to a backing store containing bytes using `read-u8` and `write-u8` below, as well as operations defined in terms of bytes.
Whether the textual and binary port types are disjoint is
implementation-dependent.

Ports can be used to access files, devices, and similar things on the host
system on which the Scheme program is running.

<a id="call-with-port"></a>
**`(call-with-port port proc)`** — procedure

It is an error if *proc* does not accept one argument.
The `call-with-port`
procedure calls *proc* with *port* as an argument.
If *proc* returns,
then the port is closed automatically and the values yielded by the
*proc* are returned. If *proc* does not return, then
the port must not be closed automatically unless it is possible to
prove that the port will never again be used for a read or write
operation.

> **Rationale:** Because Scheme's escape procedures have unlimited extent, it is
> possible to escape from the current continuation but later to resume it.
> If implementations were permitted to close the port on any escape from the
> current continuation, then it would be impossible to write portable code using
> both `call-with-current-continuation` and `call-with-port`.

<a id="call-with-input-file"></a>
<a id="call-with-output-file"></a>
**`(call-with-input-file string proc)`** — file library procedure  
**`(call-with-output-file string proc)`** — file library procedure

It is an error if *proc* does not accept one argument.
These procedures obtain a
textual port obtained by opening the named file for input or output
as if by `open-input-file` or `open-output-file`.
The port and *proc* are then passed to a procedure equivalent
to `call-with-port`.

<a id="input-port"></a>
<a id="output-port"></a>
<a id="textual-port"></a>
<a id="binary-port"></a>
<a id="port-2"></a>
**`(input-port? obj)`** — procedure  
**`(output-port? obj)`** — procedure  
**`(textual-port? obj)`** — procedure  
**`(binary-port? obj)`** — procedure  
**`(port? obj)`** — procedure

These procedures return `#t` if *obj* is an input port, output port,
textual port, binary port, or any
kind of port, respectively. Otherwise they return `#f`.

<a id="input-port-open"></a>
<a id="output-port-open"></a>
**`(input-port-open? port)`** — procedure  
**`(output-port-open? port)`** — procedure

Returns `#t` if *port* is still open and capable of
performing input or output, respectively, and `#f` otherwise.

<a id="current-input-port"></a>
<a id="current-output-port"></a>
<a id="current-error-port"></a>
**`(current-input-port)`** — procedure  
**`(current-output-port)`** — procedure  
**`(current-error-port)`** — procedure

Returns the current default input port, output port, or error port (an
output port), respectively. These procedures are parameter objects, which can be
overridden with `parameterize` (see
section [make-parameter](#make-parameter)). The initial bindings for these
are implementation-defined textual ports.

<a id="with-input-from-file"></a>
<a id="with-output-to-file"></a>
**`(with-input-from-file string thunk)`** — file library procedure  
**`(with-output-to-file string thunk)`** — file library procedure

The file is opened for input or output
as if by `open-input-file` or `open-output-file`,
and the new port is made to be the value returned by
`current-input-port` or `current-output-port`
(as used by `(read)`, `(write obj)`, and so forth).
The *thunk* is then called with no arguments. When the *thunk* returns,
the port is closed and the previous default is restored.
It is an error if *thunk* does not accept zero arguments.
Both procedures return the values yielded by *thunk*.
If an escape procedure
is used to escape from the continuation of these procedures, they
behave exactly as if the current input or output port had been bound
dynamically with `parameterize`.

<a id="open-input-file"></a>
<a id="open-binary-input-file"></a>
**`(open-input-file string)`** — file library procedure  
**`(open-binary-input-file string)`** — file library procedure

Takes a *string* for an existing file and returns a textual
input port or binary input port that is capable of delivering data from the
file. If the file does not exist or cannot be opened, an error that satisfies `file-error?` is signaled.

<a id="open-output-file"></a>
<a id="open-binary-output-file"></a>
**`(open-output-file string)`** — file library procedure  
**`(open-binary-output-file string)`** — file library procedure

Takes a *string* naming an output file to be created and returns a
textual output port or binary output port that is capable of writing
data to a new file by that name.

If a file with the given name already exists,
the effect is unspecified.
If the file cannot be opened,
an error that satisfies `file-error?` is signaled.

<a id="close-port"></a>
<a id="close-input-port"></a>
<a id="close-output-port"></a>
**`(close-port port)`** — procedure  
**`(close-input-port port)`** — procedure  
**`(close-output-port port)`** — procedure

Closes the resource associated with *port*, rendering the *port*
incapable of delivering or accepting data.
It is an error
to apply the last two procedures to a port which is not an input
or output port, respectively.
Scheme implementations may provide ports which are simultaneously
input and output ports, such as sockets; the `close-input-port`
and `close-output-port` procedures can then be used to close the
input and output sides of the port independently.

These routines have no effect if the port has already been closed.

<a id="open-input-string"></a>
**`(open-input-string string)`** — procedure

Takes a string and returns a textual input port that delivers
characters from the string.
If the string is modified, the effect is unspecified.

<a id="open-output-string"></a>
**`(open-output-string)`** — procedure

Returns a textual output port that will accumulate characters for
retrieval by `get-output-string`.

<a id="get-output-string"></a>
**`(get-output-string port)`** — procedure

It is an error if *port* was not created with
`open-output-string`.
Returns a string consisting of the
characters that have been output to the port so far in the order they
were output.
If the result string is modified, the effect is unspecified.

```scheme
(parameterize
    ((current-output-port
      (open-output-string)))
    (display "piece")
    (display " by piece ")
    (display "by piece.")
    (newline)
    (get-output-string (current-output-port)))
=> "piece by piece by piece.n"
```

<a id="open-input-bytevector"></a>
**`(open-input-bytevector bytevector)`** — procedure

Takes a bytevector and returns a binary input port that delivers
bytes from the bytevector.

<a id="open-output-bytevector"></a>
**`(open-output-bytevector)`** — procedure

Returns a binary output port that will accumulate bytes for
retrieval by `get-output-bytevector`.

<a id="get-output-bytevector"></a>
**`(get-output-bytevector port)`** — procedure

It is an error if *port* was not created with
`open-output-bytevector`. Returns a bytevector consisting
of the bytes that have been output to the port so far in the
order they were output.

### Input

<a id="inputsection"></a>

If *port* is omitted from any input procedure, it defaults to the
value returned by `(current-input-port)`.
It is an error to attempt an input operation on a closed port.

<a id="read"></a>
**`(read)`** — read library procedure  
**`(read port)`** — read library procedure

The `read` procedure converts external representations of Scheme objects into the
objects themselves. That is, it is a parser for the non-terminal
⟨datum⟩ (see sections [External representations](#datum) and
[Pairs and lists](#listsection)). It returns the next
object parsable from the given textual input *port*, updating
*port* to point to
the first character past the end of the external representation of the object.

Implementations may support extended syntax to represent record types or
other types that do not have datum representations.

If an end of file is encountered in the input before any
characters are found that can begin an object, then an end-of-file
object is returned. The port remains open, and further attempts
to read will also return an end-of-file object. If an end of file is
encountered after the beginning of an object's external representation,
but the external representation is incomplete and therefore not parsable,
an error that satisfies `read-error?` is signaled.

<a id="read-char"></a>
**`(read-char)`** — procedure  
**`(read-char port)`** — procedure

Returns the next character available from the textual input *port*,
updating
the *port* to point to the following character. If no more characters
are available, an end-of-file object is returned.

<a id="peek-char"></a>
**`(peek-char)`** — procedure  
**`(peek-char port)`** — procedure

Returns the next character available from the textual input *port*,
but *without* updating
the *port* to point to the following character. If no more characters
are available, an end-of-file object is returned.

> **Note:** The value returned by a call to `peek-char` is the same as the
> value that would have been returned by a call to `read-char` with the
> same *port*. The only difference is that the very next call to
> `read-char` or `peek-char` on that *port* will return the
> value returned by the preceding call to `peek-char`. In particular, a call
> to `peek-char` on an interactive port will hang waiting for input
> whenever a call to `read-char` would have hung.

<a id="read-line"></a>
**`(read-line)`** — procedure  
**`(read-line port)`** — procedure

Returns the next line of text available from the textual input
*port*, updating the *port* to point to the following character.
If an end of line is read, a string containing all of the text up to
(but not including) the end of line is returned, and the port is updated
to point just past the end of line. If an end of file is encountered
before any end of line is read, but some characters have been
read, a string containing those characters is returned. If an end of
file is encountered before any characters are read, an end-of-file
object is returned. For the purpose of this procedure, an end of line
consists of either a linefeed character, a carriage return character, or a
sequence of a carriage return character followed by a linefeed character.
Implementations may also recognize other end of line characters or sequences.

<a id="eof-object"></a>
**`(eof-object? obj)`** — procedure

Returns `#t` if *obj* is an end-of-file object, otherwise returns
`#f`. The precise set of end-of-file objects will vary among
implementations, but in any case no end-of-file object will ever be an object
that can be read in using `read`.

<a id="eof-object-2"></a>
**`(eof-object)`** — procedure

Returns an end-of-file object, not necessarily unique.

<a id="char-ready"></a>
**`(char-ready?)`** — procedure  
**`(char-ready? port)`** — procedure

Returns `#t` if a character is ready on the textual input *port* and
returns `#f` otherwise. If `char-ready` returns `#t` then
the next `read-char` operation on the given *port* is guaranteed
not to hang. If the *port* is at end of file then `char-ready?`
returns `#t`.

> **Rationale:** The `char-ready?` procedure exists to make it possible for a program to
> accept characters from interactive ports without getting stuck waiting for
> input. Any input editors associated with such ports must ensure that
> characters whose existence has been asserted by `char-ready?` cannot
> be removed from the input. If `char-ready?` were to return `#f` at end of
> file, a port at end of file would be indistinguishable from an interactive
> port that has no ready characters.

<a id="read-string"></a>
**`(read-string k)`** — procedure  
**`(read-string k port)`** — procedure

<a id="readstring"></a>

Reads the next *k* characters, or as many as are available before the end of file,
from the textual
input *port* into a newly allocated string in left-to-right order
and returns the string.
If no characters are available before the end of file,
an end-of-file object is returned.

<a id="read-u8"></a>
**`(read-u8)`** — procedure  
**`(read-u8 port)`** — procedure

Returns the next byte available from the binary input *port*,
updating the *port* to point to the following byte.
If no more bytes are
available, an end-of-file object is returned.

<a id="peek-u8"></a>
**`(peek-u8)`** — procedure  
**`(peek-u8 port)`** — procedure

Returns the next byte available from the binary input *port*,
but *without* updating the *port* to point to the following
byte. If no more bytes are available, an end-of-file object is returned.

<a id="u8-ready"></a>
**`(u8-ready?)`** — procedure  
**`(u8-ready? port)`** — procedure

Returns `#t` if a byte is ready on the binary input *port*
and returns `#f` otherwise. If `u8-ready?` returns
`#t` then the next `read-u8` operation on the given
*port* is guaranteed not to hang. If the *port* is at end of
file then `u8-ready?` returns `#t`.

<a id="read-bytevector"></a>
**`(read-bytevector k)`** — procedure  
**`(read-bytevector k port)`** — procedure

Reads the next *k* bytes, or as many as are available before the end of file,
from the binary
input *port* into a newly allocated bytevector in left-to-right order
and returns the bytevector.
If no bytes are available before the end of file,
an end-of-file object is returned.

<a id="read-bytevector-2"></a>
**`(read-bytevector! bytevector)`** — procedure  
**`(read-bytevector! bytevector port)`** — procedure  
**`(read-bytevector! bytevector port start)`** — procedure  
**`(read-bytevector! bytevector port start end)`** — procedure

Reads the next $end - start$ bytes, or as many as are available
before the end of file,
from the binary
input *port* into *bytevector* in left-to-right order
beginning at the *start* position. If *end* is not supplied,
reads until the end of *bytevector* has been reached. If
*start* is not supplied, reads beginning at position 0.
Returns the number of bytes read.
If no bytes are available, an end-of-file object is returned.

### Output

<a id="outputsection"></a>

If *port* is omitted from any output procedure, it defaults to the
value returned by `(current-output-port)`.
It is an error to attempt an output operation on a closed port.

<a id="write"></a>
**`(write obj)`** — write library procedure  
**`(write obj port)`** — write library procedure

Writes a representation of *obj* to the given textual output
*port*. Strings
that appear in the written representation are enclosed in quotation marks, and
within those strings backslash and quotation mark characters are
escaped by backslashes. Symbols that contain non-ASCII characters
are escaped with vertical lines.
Character objects are written using the `#\` notation.

If *obj* contains cycles which would cause an infinite loop using
the normal written representation, then at least the objects that form
part of the cycle must be represented using datum labels as described
in section [Datum labels](#labelsection). Datum labels must not be used if there
are no cycles.

Implementations may support extended syntax to represent record types or
other types that do not have datum representations.

The `write` procedure returns an unspecified value.

<a id="write-shared"></a>
**`(write-shared obj)`** — write library procedure  
**`(write-shared obj port)`** — write library procedure

The `write-shared` procedure is the same as `write`, except that
shared structure must be represented using datum labels for all pairs
and vectors that appear more than once in the output.

<a id="write-simple"></a>
**`(write-simple obj)`** — write library procedure  
**`(write-simple obj port)`** — write library procedure

The `write-simple` procedure is the same as `write`, except that shared structure is
never represented using datum labels. This can cause `write-simple` not to
terminate if *obj* contains circular structure.

<a id="display"></a>
**`(display obj)`** — write library procedure  
**`(display obj port)`** — write library procedure

Writes a representation of *obj* to the given textual output *port*.
Strings that appear in the written representation are output as if by
`write-string` instead of by `write`.
Symbols are not escaped. Character
objects appear in the representation as if written by `write-char`
instead of by `write`.

The `display` representation of other objects is unspecified.
However, `display` must not loop forever on
self-referencing pairs, vectors, or records. Thus if the
normal `write` representation is used, datum labels are needed
to represent cycles as in `write`.

Implementations may support extended syntax to represent record types or
other types that do not have datum representations.

The `display` procedure returns an unspecified value.

> **Rationale:** The `write` procedure is intended
> for producing mach­ine-readable output and `display` for producing
> human-readable output.

<a id="newline"></a>
**`(newline)`** — procedure  
**`(newline port)`** — procedure

Writes an end of line to textual output *port*. Exactly how this
is done differs
from one operating system to another. Returns an unspecified value.

<a id="write-char"></a>
**`(write-char char)`** — procedure  
**`(write-char char port)`** — procedure

Writes the character *char* (not an external representation of the
character) to the given textual output *port* and returns an unspecified
value.

<a id="write-string"></a>
**`(write-string string)`** — procedure  
**`(write-string string port)`** — procedure  
**`(write-string string port start)`** — procedure  
**`(write-string string port start end)`** — procedure

Writes the characters of *string*
from *start* to *end*
in left-to-right order to the
textual output *port*.

<a id="write-u8"></a>
**`(write-u8 byte)`** — procedure  
**`(write-u8 byte port)`** — procedure

Writes the *byte* to
the given binary output *port* and returns an unspecified value.

<a id="write-bytevector"></a>
**`(write-bytevector bytevector)`** — procedure  
**`(write-bytevector bytevector port)`** — procedure  
**`(write-bytevector bytevector port start)`** — procedure  
**`(write-bytevector bytevector port start end)`** — procedure

Writes the bytes of *bytevector*
from *start* to *end*
in left-to-right order to the
binary output *port*.

<a id="flush-output-port"></a>
**`(flush-output-port)`** — procedure  
**`(flush-output-port port)`** — procedure

Flushes any buffered output from the buffer of output-port to the
underlying file or device and returns an unspecified value.

## System interface

Questions of system interface generally fall outside of the domain of this
report. However, the following operations are important enough to
deserve description here.

<a id="load"></a>
**`(load filename)`** — load library procedure  
**`(load filename environment-specifier)`** — load library procedure

It is an error if *filename* is not a string.
An implementation-dependent operation is used to transform
*filename* into the name of an existing file
containing Scheme source code. The `load` procedure reads
expressions and definitions from the file and evaluates them
sequentially in the environment specified by *environment-specifier*.
If *environment-specifier* is omitted, `(interaction-environment)`
is assumed.

It is unspecified whether the results of the expressions
are printed. The `load` procedure does not affect the values
returned by `current-input-port` and `current-output-port`.
It returns an unspecified value.

> **Rationale:** For portability, `load` must operate on source files.
> Its operation on other kinds of files necessarily varies among
> implementations.

<a id="file-exists"></a>
**`(file-exists? filename)`** — file library procedure

It is an error if *filename* is not a string.
The `file-exists?` procedure returns
`#t` if the named file exists at the time the procedure is called,
and `#f` otherwise.

<a id="delete-file"></a>
**`(delete-file filename)`** — file library procedure

It is an error if *filename* is not a string.
The `delete-file` procedure deletes the
named file if it exists and can be deleted, and returns an unspecified
value. If the file does not exist or cannot be deleted, an error
that satisfies `file-error?` is signaled.

<a id="command-line"></a>
**`(command-line)`** — process-context library procedure

Returns the command line passed to the process as a list of
strings. The first string corresponds to the command name, and is
implementation-dependent. It is an error to mutate any of these strings.

<a id="exit"></a>
**`(exit)`** — process-context library procedure  
**`(exit obj)`** — process-context library procedure

Runs all outstanding dynamic-wind *after* procedures, terminates the
running program, and communicates an exit value to the operating system.
If no argument is supplied, or if *obj* is `#t`, the `exit` procedure should communicate to the operating system that the
program exited normally. If *obj* is `#f`, the `exit`
procedure should communicate to the operating system that the program
exited abnormally. Otherwise, `exit` should translate *obj* into
an appropriate exit value for the operating system, if possible.

The `exit` procedure
must not signal an exception or return to its continuation.

> **Note:** Because of the requirement to run handlers, this procedure is not just the
> operating system's exit procedure.

<a id="emergency-exit"></a>
**`(emergency-exit)`** — process-context library procedure  
**`(emergency-exit obj)`** — process-context library procedure

Terminates the program without running any
outstanding dynamic-wind *after* procedures
and communicates an exit value to the operating system
in the same manner as `exit`.

> **Note:** The `emergency-exit` procedure corresponds to the `_exit` procedure
> in Windows and Posix.

<a id="get-environment-variable"></a>
**`(get-environment-variable name)`** — process-context library procedure

Many operating systems provide each running process with an
**environment** consisting of **environment variables**.
(This environment is not to be confused with the Scheme environments that
can be passed to `eval`: see section [Environments and evaluation](#environments).)
Both the name and value of an environment variable are strings.
The procedure `get-environment-variable` returns the value
of the environment variable *name*,
or `#f` if the named
environment variable is not found. It may
use locale information to encode the name and decode the value
of the environment variable. It is an error if \
`get-environment-variable` can't decode the value.
It is also an error to mutate the resulting string.

```scheme
(get-environment-variable "PATH") => "/usr/local/bin:/usr/bin:/bin"
```

<a id="get-environment-variables"></a>
**`(get-environment-variables)`** — process-context library procedure

Returns the names and values of all the environment variables as an
alist, where the car of each entry is the name of an environment
variable and the cdr is its value, both as strings. The order of the list is unspecified.
It is an error to mutate any of these strings or the alist itself.

```scheme
(get-environment-variables) => (("USER" . "root") ("HOME" . "/"))
```

<a id="current-second"></a>
**`(current-second)`** — time library procedure

Returns an inexact number representing the current time on the International Atomic
Time (TAI) scale. The value 0.0 represents midnight
on January 1, 1970 TAI (equivalent to 8.000082 seconds before midnight Universal Time)
and the value 1.0 represents one TAI
second later. Neither high accuracy nor high precision are required; in particular,
returning Coordinated Universal Time plus a suitable constant might be
the best an implementation can do.

As of 2018, a TAI-UTC offset table can be found at [[TAI](#cite-tai)].

<a id="current-jiffy"></a>
**`(current-jiffy)`** — time library procedure

Returns the number of **jiffies** as an exact integer that have elapsed since an arbitrary,
implementation-defined epoch. A jiffy is an implementation-defined
fraction of a second which is defined by the return value of the
`jiffies-per-second` procedure. The starting epoch is guaranteed to be
constant during a run of the program, but may vary between runs.

> **Rationale:** Jiffies are allowed to be implementation-dependent so that
> `current-jiffy` can execute with minimum overhead. It
> should be very likely that a compactly represented integer will suffice
> as the returned value. Any particular jiffy size will be inappropriate
> for some implementations: a microsecond is too long for a very fast
> machine, while a much smaller unit would force many implementations to
> return integers which have to be allocated for most calls, rendering
> `current-jiffy` less useful for accurate timing measurements.

<a id="jiffies-per-second"></a>
**`(jiffies-per-second)`** — time library procedure

Returns an exact integer representing the number of jiffies per SI
second. This value is an implementation-specified constant.

```scheme
(define (time-length)
  (let ((list (make-list 100000))
        (start (current-jiffy)))
    (length list)
    (/ (- (current-jiffy) start)
       (jiffies-per-second))))
```

<a id="features"></a>
**`(features)`** — procedure

Returns a list of the feature identifiers which `cond-expand`
treats as true. It is an error to modify this list. Here is an
example of what `features` might return:

```scheme
(features)   =>
  (r7rs ratios exact-complex full-unicode
   gnu-linux little-endian
   fantastic-scheme
   fantastic-scheme-1.0
   space-ship-control-system)
```


# Formal syntax and semantics

<a id="formalchapter"></a>

This chapter provides formal descriptions of what has already been
described informally in previous chapters of this report.

## Formal syntax

<a id="bnf"></a>

This section provides a formal syntax for Scheme written in an extended
BNF.

All spaces in the grammar are for legibility. Case is not significant
except in the definitions of ⟨letter⟩, ⟨character name⟩ and ⟨mnemonic escape⟩; for example, `#x1A`
and `#X1a` are equivalent, but `foo` and `Foo`
and `#\space` and `#\Space` are distinct.
⟨empty⟩ stands for the empty string.

The following extensions to BNF are used to make the description more
concise: ⟨thing⟩ means zero or more occurrences of
⟨thing⟩; and ⟨thing⟩ means at least one
⟨thing⟩.

### Lexical structure

This section describes how individual tokens (identifiers,
numbers, etc.) are formed from sequences of characters. The following
sections describe how expressions and programs are formed from sequences
of tokens.

⟨Intertoken space⟩ can occur on either side of any token, but not
within a token.

Identifiers that do not begin with a vertical line are
terminated by a ⟨delimiter⟩ or by the end of the input.
So are dot, numbers, characters, and booleans.
Identifiers that begin with a vertical line are terminated by another vertical line.

The following four characters from the ASCII repertoire
are reserved for future extensions to the
language: `[ ] { }`

In addition to the identifier characters of the ASCII repertoire specified
below, Scheme implementations may permit any additional repertoire of
non-ASCII Unicode characters to be employed in identifiers,
provided that each such character has a Unicode general category of Lu,
Ll, Lt, Lm, Lo, Mn, Mc, Me, Nd, Nl, No, Pd, Pc, Po, Sc, Sm, Sk, So,
or Co, or is U+200C or U+200D (the zero-width non-joiner and joiner,
respectively, which are needed for correct spelling in Persian, Hindi,
and other languages).
However, it is an error for the first character to have a general category
of Nd, Mc, or Me. It is also an error to use a non-Unicode character
in symbols or identifiers.

All Scheme implementations must permit the escape sequence
`\x<hexdigits>;`
to appear in Scheme identifiers that are enclosed in vertical lines. If the character
with the given Unicode scalar value is supported by the implementation,
identifiers containing such a sequence are equivalent to identifiers
containing the corresponding character.

```bnf
⟨token⟩  ⟶  ⟨identifier⟩  |  ⟨boolean⟩  |  ⟨number⟩
       |  ⟨character⟩  |  ⟨string⟩
       |  (  |  )  |  #(  |  # u8(  |  '  |  `  |  ,  |  ,@  |  .
⟨delimiter⟩  ⟶  ⟨whitespace⟩  |  ⟨vertical line⟩
      |  (  |  )  |  "  |  ;
⟨intraline whitespace⟩  ⟶  ⟨space or tab⟩
⟨whitespace⟩  ⟶  ⟨intraline whitespace⟩  |  ⟨line ending⟩
⟨vertical line⟩  ⟶  |
⟨line ending⟩  ⟶  ⟨newline⟩  |  ⟨return⟩ ⟨newline⟩
      |  ⟨return⟩
⟨comment⟩  ⟶  ;  ⟨ all subsequent characters up to a
		          line ending⟩
      |  ⟨nested comment⟩
      |  #; ⟨intertoken space⟩ ⟨datum⟩
⟨nested comment⟩  ⟶  #|  ⟨comment text⟩
     ⟨comment cont⟩* |#
⟨comment text⟩  ⟶   ⟨ character sequence not containing
       #| or  |#⟩
⟨comment cont⟩  ⟶  ⟨nested comment⟩ ⟨comment text⟩
⟨directive⟩  ⟶  #!fold-case  |  #!no-fold-case
```

Note that it is ungrammatical to follow a ⟨directive⟩ with anything
but a ⟨delimiter⟩ or the end of file.

```bnf
⟨atmosphere⟩  ⟶  ⟨whitespace⟩  |  ⟨comment⟩  |  ⟨directive⟩
⟨intertoken space⟩  ⟶  ⟨atmosphere⟩*
```

<a id="extendedalphas"></a>
<a id="identifiersyntax"></a>

0⟨identifier⟩ $⟨$

Note that `+i`, `-i` and ⟨infnan⟩ below are exceptions to the
⟨peculiar identifier⟩ rule; they are parsed as numbers, not
identifiers.

```bnf
⟨identifier⟩  ⟶  ⟨initial⟩ ⟨subsequent⟩*
        |  ⟨vertical line⟩ ⟨symbol element⟩* ⟨vertical line⟩
        |  ⟨peculiar identifier⟩
⟨initial⟩  ⟶  ⟨letter⟩  |  ⟨special initial⟩
⟨letter⟩  ⟶  a  |  b  |  c  |  ...  |  z
      |  A  |  B  |  C  |  ...  |  Z
⟨special initial⟩  ⟶  !  |  \$  |  \%  |  \verb"&"  |  *  |  /  |  :  |  <  |  =
        |  >  |  ?  |  @  |  \verb"^"  |  \verb"_"  |  \verb"~"
⟨subsequent⟩  ⟶  ⟨initial⟩  |  ⟨digit⟩
        |  ⟨special subsequent⟩
⟨digit⟩  ⟶  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9
⟨hex digit⟩  ⟶  ⟨digit⟩  |  a  |  b  |  c  |  d  |  e  |  f
⟨explicit sign⟩  ⟶  +  |  -
⟨special subsequent⟩  ⟶  ⟨explicit sign⟩  |  .  |  @
⟨inline hex escape⟩  ⟶  \x⟨hex scalar value⟩;
⟨hex scalar value⟩  ⟶  ⟨hex digit⟩⁺
⟨mnemonic escape⟩  ⟶  \a  |  \b  |  \t  |  \n  |  \r
⟨peculiar identifier⟩  ⟶  ⟨explicit sign⟩
       |  ⟨explicit sign⟩ ⟨sign subsequent⟩ ⟨subsequent⟩*
       |  ⟨explicit sign⟩ . ⟨dot subsequent⟩ ⟨subsequent⟩*
       |  . ⟨dot subsequent⟩ ⟨subsequent⟩*

⟨dot subsequent⟩  ⟶  ⟨sign subsequent⟩  |  .
⟨sign subsequent⟩  ⟶  ⟨initial⟩  |  ⟨explicit sign⟩  |  @
⟨symbol element⟩  ⟶
      ⟨any character other than ⟨vertical line⟩ or \⟩
       |  ⟨inline hex escape⟩  |  ⟨mnemonic escape⟩  |  \|

⟨boolean⟩  ⟶  \schtrue  |  \schfalse  |  \sharptrue  |  \sharpfalse

⟨character⟩  ⟶  #\ ⟨any character⟩
        |  #\ ⟨character name⟩
        |  #\x⟨hex scalar value⟩
⟨character name⟩  ⟶  alarm  |  backspace  |  delete
      |  escape  |  newline  |  null  |  return  |  space  |  tab
\todoExplain what happens in the ambiguous case.
⟨string⟩  ⟶  " ⟨string element⟩* "
⟨string element⟩  ⟶  ⟨any character other than \doublequote or \⟩
       |  ⟨mnemonic escape⟩  |  \\doublequote  |  \\  |  \|
        |  \⟨intraline whitespace⟩*⟨line ending⟩
            ⟨intraline whitespace⟩*
        |  ⟨inline hex escape⟩
⟨bytevector⟩  ⟶  #u8(⟨byte⟩*)
⟨byte⟩  ⟶  ⟨any exact integer between 0 and 255⟩
```

<a id="numbersyntax"></a>

```bnf
⟨number⟩  ⟶  ⟨num $2$⟩  |  ⟨num $8$⟩
          |  ⟨num $10$⟩  |  ⟨num $16$⟩
```

The following rules for ⟨num $R$⟩, ⟨complex $R$⟩, ⟨real
$R$⟩, ⟨ureal $R$⟩, ⟨uinteger $R$⟩, and ⟨prefix $R$⟩
are implicitly replicated for $R = 2, 8, 10,$
and $16$. There are no rules for ⟨decimal $2$⟩, ⟨decimal
$8$⟩, and ⟨decimal $16$⟩, which means that numbers containing
decimal points or exponents are always in decimal radix.
Although not shown below, all alphabetic characters used in the grammar
of numbers can appear in either upper or lower case.

```bnf
⟨num $R$⟩  ⟶  ⟨prefix $R$⟩ ⟨complex $R$⟩
⟨complex $R$⟩  ⟶
         ⟨real $R$⟩
       |  ⟨real $R$⟩ @ ⟨real $R$⟩
         |  ⟨real $R$⟩ + ⟨ureal $R$⟩ i
       |  ⟨real $R$⟩ - ⟨ureal $R$⟩ i
         |  ⟨real $R$⟩ + i
       |  ⟨real $R$⟩ - i
       |  ⟨real $R$⟩ ⟨infnan⟩ i
         |  + ⟨ureal $R$⟩ i
       |  - ⟨ureal $R$⟩ i
         |  ⟨infnan⟩ i
       |  + i
       |  - i
⟨real $R$⟩  ⟶  ⟨sign⟩ ⟨ureal $R$⟩
         |  ⟨infnan⟩
⟨ureal $R$⟩  ⟶
         ⟨uinteger $R$⟩
         |  ⟨uinteger $R$⟩ / ⟨uinteger $R$⟩
         |  ⟨decimal $R$⟩
⟨decimal $10$⟩  ⟶
         ⟨uinteger $10$⟩ ⟨suffix⟩
         |  . ⟨digit $10$⟩⁺ ⟨suffix⟩
         |  ⟨digit $10$⟩⁺ . ⟨digit $10$⟩* ⟨suffix⟩
⟨uinteger $R$⟩  ⟶  ⟨digit $R$⟩⁺
⟨prefix $R$⟩  ⟶
         ⟨radix $R$⟩ ⟨exactness⟩
         |  ⟨exactness⟩ ⟨radix $R$⟩
⟨infnan⟩  ⟶  +inf.0  |  -inf.0  |  +nan.0  |  -nan.0
```

```bnf
⟨suffix⟩  ⟶  ⟨empty⟩
         |  ⟨exponent marker⟩ ⟨sign⟩ ⟨digit $10$⟩⁺
⟨exponent marker⟩  ⟶  e
⟨sign⟩  ⟶  ⟨empty⟩   |  +  |   -
⟨exactness⟩  ⟶  ⟨empty⟩  |  #i\sharpindexi  |  #e\sharpindexe
⟨radix 2⟩  ⟶  #b\sharpindexb
⟨radix 8⟩  ⟶  #o\sharpindexo
⟨radix 10⟩  ⟶  ⟨empty⟩  |  #d
⟨radix 16⟩  ⟶  #x\sharpindexx
⟨digit 2⟩  ⟶  0  |  1
⟨digit 8⟩  ⟶  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7
⟨digit 10⟩  ⟶  ⟨digit⟩
⟨digit 16⟩  ⟶  ⟨digit $10$⟩  |  a  |  b  |  c  |  d  |  e  |  f
```

### External representations

<a id="datumsyntax"></a>

⟨Datum⟩ is what the `read` procedure (section [read](#read))
successfully parses. Note that any string that parses as an
⟨ex­pres­sion⟩ will also parse as a ⟨datum⟩. <a id="datum"></a>

```bnf
⟨datum⟩  ⟶  ⟨simple datum⟩  |  ⟨compound datum⟩
       |  ⟨label⟩ = ⟨datum⟩  |  ⟨label⟩ #
⟨simple datum⟩  ⟶  ⟨boolean⟩  |  ⟨number⟩
       |  ⟨character⟩  |  ⟨string⟩  |   ⟨symbol⟩  |  ⟨bytevector⟩
⟨symbol⟩  ⟶  ⟨identifier⟩
⟨compound datum⟩  ⟶  ⟨list⟩  |  ⟨vector⟩  |  ⟨abbreviation⟩
⟨list⟩  ⟶  (⟨datum⟩*)  |  (⟨datum⟩⁺ . ⟨datum⟩)
⟨abbreviation⟩  ⟶  ⟨abbrev prefix⟩ ⟨datum⟩
⟨abbrev prefix⟩  ⟶  '  |  `  |  ,  |  ,@
⟨vector⟩  ⟶  #(⟨datum⟩*)
⟨label⟩  ⟶  # ⟨uinteger 10⟩
```

### Expressions

The definitions in this and the following subsections assume that all
the syntax keywords defined in this report have been properly imported
from their libraries, and that none of them have been redefined or shadowed.

```bnf
⟨expression⟩  ⟶  ⟨identifier⟩
       |  ⟨literal⟩
       |  ⟨procedure call⟩
       |  ⟨lambda expression⟩
       |  ⟨conditional⟩
       |  ⟨assignment⟩
       |  ⟨derived expression⟩
       |  ⟨macro use⟩
       |  ⟨macro block⟩
       |  ⟨includer⟩

⟨literal⟩  ⟶  ⟨quotation⟩  |  ⟨self-evaluating⟩
⟨self-evaluating⟩  ⟶  ⟨boolean⟩  |  ⟨number⟩  |  ⟨vector⟩
       |  ⟨character⟩  |  ⟨string⟩  |  ⟨bytevector⟩
⟨quotation⟩  ⟶  '⟨datum⟩  |  (quote ⟨datum⟩)
⟨procedure call⟩  ⟶  (⟨operator⟩ ⟨operand⟩*)
⟨operator⟩  ⟶  ⟨expression⟩
⟨operand⟩  ⟶  ⟨expression⟩

⟨lambda expression⟩  ⟶  (lambda ⟨formals⟩ ⟨body⟩)
⟨formals⟩  ⟶  (⟨identifier⟩*)  |  ⟨identifier⟩
       |  (⟨identifier⟩⁺ . ⟨identifier⟩)
⟨body⟩  ⟶   ⟨definition⟩* ⟨sequence⟩
⟨sequence⟩  ⟶  ⟨command⟩* ⟨expression⟩
⟨command⟩  ⟶  ⟨expression⟩

⟨conditional⟩  ⟶  (if ⟨test⟩ ⟨consequent⟩ ⟨alternate⟩)
⟨test⟩  ⟶  ⟨expression⟩
⟨consequent⟩  ⟶  ⟨expression⟩
⟨alternate⟩  ⟶  ⟨expression⟩  |  ⟨empty⟩

⟨assignment⟩  ⟶  (set! ⟨identifier⟩ ⟨expression⟩)

⟨derived expression⟩  ⟶
           (cond ⟨cond clause⟩⁺)
       |  (cond ⟨cond clause⟩* (else ⟨sequence⟩))
       |  (case ⟨expression⟩
               ⟨case clause⟩⁺)
       |  (case ⟨expression⟩
               ⟨case clause⟩*
               (else ⟨sequence⟩))
       |  (case ⟨expression⟩
               ⟨case clause⟩*
               (else => ⟨recipient⟩))
       |  (and ⟨test⟩*)
       |  (or ⟨test⟩*)
       |  (when ⟨test⟩ ⟨sequence⟩)
       |  (unless ⟨test⟩ ⟨sequence⟩)
       |  (let (⟨binding spec⟩*) ⟨body⟩)
       |  (let ⟨identifier⟩ (⟨binding spec⟩*) ⟨body⟩)
       |  (let* (⟨binding spec⟩*) ⟨body⟩)
       |  (letrec (⟨binding spec⟩*) ⟨body⟩)
       |  (letrec* (⟨binding spec⟩*) ⟨body⟩)
       |  (let-values (⟨mv binding spec⟩*) ⟨body⟩)
       |  (let*-values (⟨mv binding spec⟩*) ⟨body⟩)
       |  (begin ⟨sequence⟩)
       |  (do (⟨iteration spec⟩*)
                     (⟨test⟩ ⟨do result⟩)
               ⟨command⟩*)
       |  (delay ⟨expression⟩)
       |  (delay-force ⟨expression⟩)
       |  (parameterize ((⟨expression⟩ ⟨expression⟩)*)
                ⟨body⟩)
       |  (guard (⟨identifier⟩ ⟨cond clause⟩*) ⟨body⟩)
       |  ⟨quasiquotation⟩
       |  (case-lambda ⟨case-lambda clause⟩*)

⟨cond clause⟩  ⟶  (⟨test⟩ ⟨sequence⟩)
        |  (⟨test⟩)
        |  (⟨test⟩ => ⟨recipient⟩)
⟨recipient⟩  ⟶  ⟨expression⟩
⟨case clause⟩  ⟶  ((⟨datum⟩*) ⟨sequence⟩)
        |  ((⟨datum⟩*) => ⟨recipient⟩)
⟨binding spec⟩  ⟶  (⟨identifier⟩ ⟨expression⟩)
⟨mv binding spec⟩  ⟶  (⟨formals⟩ ⟨expression⟩)
⟨iteration spec⟩  ⟶  (⟨identifier⟩ ⟨init⟩ ⟨step⟩)
      |  (⟨identifier⟩ ⟨init⟩)
⟨case-lambda clause⟩  ⟶  (⟨formals⟩ ⟨body⟩)
⟨init⟩  ⟶  ⟨expression⟩
⟨step⟩  ⟶  ⟨expression⟩
⟨do result⟩  ⟶  ⟨sequence⟩  |  ⟨empty⟩

⟨macro use⟩  ⟶  (⟨keyword⟩ ⟨datum⟩*)
⟨keyword⟩  ⟶  ⟨identifier⟩

⟨macro block⟩  ⟶
      (let-syntax (⟨syntax spec⟩*) ⟨body⟩)
       |  (letrec-syntax (⟨syntax spec⟩*) ⟨body⟩)
⟨syntax spec⟩  ⟶  (⟨keyword⟩ ⟨transformer spec⟩)

⟨includer⟩  ⟶
      |  (include ⟨string⟩⁺)
      |  (include-ci ⟨string⟩⁺)
```

### Quasiquotations

The following grammar for quasiquote expressions is not context-free.
It is presented as a recipe for generating an infinite number of
production rules. Imagine a copy of the following rules for $D = 1, 2, 3, \dots$, where $D$ is the nesting depth.

```bnf
⟨quasiquotation⟩  ⟶  ⟨quasiquotation 1⟩
⟨qq template 0⟩  ⟶  ⟨expression⟩
⟨quasiquotation $D$⟩  ⟶  `⟨qq template $D$⟩
         |  (quasiquote ⟨qq template $D$⟩)
⟨qq template $D$⟩  ⟶  ⟨simple datum⟩
         |  ⟨list qq template $D$⟩
         |  ⟨vector qq template $D$⟩
         |  ⟨unquotation $D$⟩
⟨list qq template $D$⟩  ⟶  (⟨qq template or splice $D$⟩*)
         |  (⟨qq template or splice $D$⟩⁺ . ⟨qq template $D$⟩)
         |  '⟨qq template $D$⟩
         |  ⟨quasiquotation $D+1$⟩
⟨vector qq template $D$⟩  ⟶  #(⟨qq template or splice $D$⟩*)
⟨unquotation $D$⟩  ⟶  ,⟨qq template $D-1$⟩
         |  (unquote ⟨qq template $D-1$⟩)
⟨qq template or splice $D$⟩  ⟶  ⟨qq template $D$⟩
         |  ⟨splicing unquotation $D$⟩
⟨splicing unquotation $D$⟩  ⟶  ,@⟨qq template $D-1$⟩
         |  (unquote-splicing ⟨qq template $D-1$⟩)
```

In ⟨quasiquotation⟩s, a ⟨list qq template $D$⟩ can sometimes
be confused with either an ⟨un­quota­tion $D$⟩ or a ⟨splicing
un­quo­ta­tion $D$⟩. The interpretation as an
⟨un­quo­ta­tion⟩ or ⟨splicing
un­quo­ta­tion $D$⟩ takes precedence.

### Transformers

> **Note:** Though this grammar does not say so, a top-level `syntax-rules`
> pattern must be a list pattern, not a vector pattern or an identifier pattern.

```bnf
⟨transformer spec⟩  ⟶
     (syntax-rules (⟨identifier⟩*) ⟨syntax rule⟩*)
      |  (syntax-rules ⟨identifier⟩ (⟨identifier⟩*)
            ⟨syntax rule⟩*)
⟨syntax rule⟩  ⟶  (⟨pattern⟩ ⟨template⟩)
⟨pattern⟩  ⟶  ⟨pattern identifier⟩
       |  ⟨underscore⟩
       |  (⟨pattern⟩*)
       |  (⟨pattern⟩⁺ . ⟨pattern⟩)
       |  (⟨pattern⟩* ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩*)
       |  (⟨pattern⟩* ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩*
            . ⟨pattern⟩)
       |  #(⟨pattern⟩*)
       |  #(⟨pattern⟩* ⟨pattern⟩ ⟨ellipsis⟩ ⟨pattern⟩*)
       |  ⟨pattern datum⟩
⟨pattern datum⟩  ⟶  ⟨string⟩
       |  ⟨character⟩
       |  ⟨boolean⟩
       |  ⟨number⟩
       |  ⟨bytevector⟩
⟨template⟩  ⟶  ⟨pattern identifier⟩
       |  (⟨template element⟩*)
       |  (⟨template element⟩⁺ . ⟨template⟩)
       |  #(⟨template element⟩*)
       |  ⟨template datum⟩
⟨template element⟩  ⟶  ⟨template⟩
       |  ⟨template⟩ ⟨ellipsis⟩
⟨template datum⟩  ⟶  ⟨pattern datum⟩
⟨pattern identifier⟩  ⟶  ⟨any identifier except ...⟩
⟨ellipsis⟩  ⟶  ⟨an identifier defaulting to ...⟩
⟨underscore⟩  ⟶  ⟨the identifier \_⟩
```

### Programs and definitions

```bnf
⟨program⟩  ⟶
     ⟨import declaration⟩⁺
     ⟨command or definition⟩⁺
⟨command or definition⟩  ⟶  ⟨command⟩
      |  ⟨definition⟩
      |  (begin ⟨command or definition⟩⁺)
⟨definition⟩  ⟶  (define ⟨identifier⟩ ⟨expression⟩)
        |  (define (⟨identifier⟩ ⟨def formals⟩) ⟨body⟩)
        |  ⟨syntax definition⟩
        |  (define-values ⟨formals⟩ ⟨body⟩)
        |  (define-record-type ⟨identifier⟩
            ⟨constructor⟩ ⟨identifier⟩ ⟨field spec⟩*)
        |  (begin ⟨definition⟩*)
⟨def formals⟩  ⟶  ⟨identifier⟩*
        |  ⟨identifier⟩* . ⟨identifier⟩
⟨constructor⟩  ⟶  (⟨identifier⟩ ⟨field name⟩*)
⟨field spec⟩  ⟶  (⟨field name⟩ ⟨accessor⟩)
        |  (⟨field name⟩ ⟨accessor⟩ ⟨mutator⟩)
⟨field name⟩  ⟶  ⟨identifier⟩
⟨accessor⟩  ⟶  ⟨identifier⟩
⟨mutator⟩  ⟶  ⟨identifier⟩
⟨syntax definition⟩  ⟶
      (define-syntax ⟨keyword⟩ ⟨transformer spec⟩)
```

### Libraries

```bnf
⟨library⟩  ⟶
     (define-library ⟨library name⟩
            ⟨library declaration⟩*)
⟨library name⟩  ⟶  (⟨library name part⟩⁺)
⟨library name part⟩  ⟶  ⟨identifier⟩  |  ⟨uinteger 10⟩
⟨library declaration⟩  ⟶  (export ⟨export spec⟩*)
      |  ⟨import declaration⟩
      |  (begin ⟨command or definition⟩*)
      |  ⟨includer⟩
      |  (include-library-declarations ⟨string⟩⁺)
      |  (cond-expand ⟨cond-expand clause⟩⁺)
      |  (cond-expand ⟨cond-expand clause⟩⁺
 (else ⟨library declaration⟩*))
⟨import declaration⟩  ⟶  (import ⟨import set⟩⁺)
⟨export spec⟩  ⟶  ⟨identifier⟩
      |  (rename ⟨identifier⟩ ⟨identifier⟩)
⟨import set⟩  ⟶  ⟨library name⟩
      |  (only ⟨import set⟩ ⟨identifier⟩⁺)
      |  (except ⟨import set⟩ ⟨identifier⟩⁺)
      |  (prefix ⟨import set⟩ ⟨identifier⟩)
      |  (rename ⟨import set⟩ (⟨identifier⟩ ⟨identifier⟩)⁺)
⟨cond-expand clause⟩  ⟶
     (⟨feature requirement⟩ ⟨library declaration⟩*)
⟨feature requirement⟩  ⟶  ⟨identifier⟩
      |  (library ⟨library name⟩)
      |  (and ⟨feature requirement⟩*)
      |  (or ⟨feature requirement⟩*)
      |  (not ⟨feature requirement⟩)
```

## Formal semantics

<a id="formalsemanticssection"></a>

This section provides a formal denotational semantics for the primitive
expressions of Scheme and selected built-in procedures. The concepts
and notation used here are described in [[Stoy77](#cite-stoy77)]; the definition of
`dynamic-wind` is taken from [[GasbichlerKnauelSperberKelsey2003](#cite-gasbichlerknauelsperberkelsey2003)].
The notation is summarized below:

| $⟨\,\dots\,⟩$ | sequence formation |
| --- | --- |
| $s \downarrow k$ | $k$th member of the sequence $s$ (1-based) |
| $\#s$ | length of sequence $s$ |
| $s \;§\; t$ | concatenation of sequences $s$ and $t$ |
| $s \dagger k$ | drop the first $k$ members of sequence $s$ |
| $t \rightarrow a, b$ | McCarthy conditional “if $t$ then $a$ else $b$” |
| $\rho[x/i]$ | substitution “$\rho$ with $x$ for $i$” |
| $x\mathrm{in }{\texttt{D}}$ | injection of $x$ into domain $\texttt{D}$ |
| $x\,\vert\,\texttt{D}$ | projection of $x$ to domain $\texttt{D}$ |

The reason that expression continuations take sequences of values instead
of single values is to simplify the formal treatment of procedure calls
and multiple return values.

The boolean flag associated with pairs, vectors, and strings will be true
for mutable objects and false for immutable objects.

The order of evaluation within a call is unspecified. We mimic that
here by applying arbitrary permutations *permute* and *unpermute*, which must be inverses, to the arguments in a call before
and after they are evaluated. This is not quite right since it suggests,
incorrectly, that the order of evaluation is constant throughout a program (for
any given number of arguments), but it is a closer approximation to the intended
semantics than a left-to-right evaluation would be.

The storage allocator *new* is implementation-dependent, but it must
obey the following axiom: if $\mathit{new}\;\sigma\;\in\;\mathtt{L}$, then
$\sigma\;(\mathit{new}\;\sigma\;\vert\;\mathtt{L})\downarrow 2 = \mathit{false}$.

The definition of $\mathcal{K}$ is omitted because an accurate definition of
$\mathcal{K}$ would complicate the semantics without being very interesting.

If P is a program in which all variables are defined before being
referenced or assigned, then the meaning of P is

$$
\mathcal{E}⟦\text{\texttt{((lambda ({\textrm{I}}{*}) \textrm{P}')
{⟨ undefined ⟩} …foo)}}⟧
$$

where I is the sequence of variables defined in P, $\mathrm{P}'$
is the sequence of expressions obtained by replacing every definition
in P by an assignment, ⟨undefined⟩ is an expression that evaluates
to undefined, and
$\mathcal{E}$ is the semantic function that assigns meaning to expressions.

### Abstract syntax

|$\vert$

| c@ l@l
 K & ∈ &  Con & constants, including quotations |  |  |  |
| --- | --- | --- | --- |
| I | ∈ | Ide | identifiers (variables) |
| E | ∈ | Exp | expressions |
| $\Gamma$ | ∈ | Com $=$  Exp | commands |

0=` Exp `
1=to 10 |

```bnf
 Exp ⟶  K  |   I  |  ( E₀  E*)
  (lambda ( I*) Γ*  E₀)
  (lambda ( I* .  I) Γ*  E₀)
  (lambda  I Γ*  E₀)
  (if  E₀  E₁  E₂)  |  (if  E₀  E₁)
  (set!  I  E)
```

### Domain equations

| r@ c@ l@ l@ ll
$\alpha$   & ∈ & `L` & &          & locations |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\nu$ | ∈ | `N` |  |  | natural numbers |
|  |  | `T` | = | $\{$ false, true$\}$ | booleans |
|  |  | `Q` |  |  | symbols |
|  |  | `H` |  |  | characters |
|  |  | `R` |  |  | numbers |
|  |  | `E`$_\mathrm{p}$ | = | $\mathtt{L} \times \mathtt{L} \times \mathtt{T}$ | pairs |
|  |  | `E`$_\mathrm{v}$ | = | ${\mathtt{L}}^{*} \times \mathtt{T}$ | vectors |
|  |  | `E`$_\mathrm{s}$ | = | ${\mathtt{L}}^{*} \times \mathtt{T}$ | strings |
|  |  | `M` | = | [0pt][l]$\{$ false, true, 
                                null, undefined, unspecified$\}$ |  |
|  |  |  |  |  | miscellaneous |
| $\phi$ | ∈ | `F` | = | $\mathtt{L}\times({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C})$ | procedure values |
| $\epsilon$ | ∈ | `E` | = | [0pt][l]$\mathtt{Q}+\mathtt{H}+\mathtt{R}+\text{\texttt{E}\textrm{p}}+\text{\texttt{E}\textrm{v}}+\text{\texttt{E}\textrm{s}}+\mathtt{M}+\mathtt{F}$ |  |
|  |  |  |  |  | expressed values |
| $\sigma$ | ∈ | `S` | = | $\mathtt{L}\to(\mathtt{E}\times\mathtt{T})$ | stores |
| $\rho$ | ∈ | `U` | = | $\mathrm{Ide}\to\mathtt{L}$ | environments |
| $\theta$ | ∈ | `C` | = | $\mathtt{S}\to\mathtt{A}$ | command conts |
| $\kappa$ | ∈ | `K` | = | ${\mathtt{E}}^{*}\to\mathtt{C}$ | expression conts |
|  |  | `A` |  |  | answers |
|  |  | `X` |  |  | errors |
| $\omega$ | ∈ | P | = | $(\mathtt{F} \times \mathtt{F} \times {P}) + \{\textit{root}\}$ | dynamic points |

### Semantic functions

| r@ l
  $\mathcal{K}:$ & $\mathrm{Con}\to\mathtt{E}$ |  |
| --- | --- |
| $\mathcal{E}:$ | $\mathrm{Exp}\to\mathtt{U}\to{P}\to\mathtt{K}\to\mathtt{C}$ |
| $\mathcal{E}^{*}:$ | ${\mathrm{Exp}}^{*}\to\mathtt{U}\to{P}\to\mathtt{K}\to\mathtt{C}$ |
| $\mathcal{C}:$ | ${\mathrm{Com}}^{*}\to\mathtt{U}\to{P}\to\mathtt{C}\to\mathtt{C}$ |

Definition of $\mathcal{K}$ deliberately omitted.

$$\mathcal{E}⟦\mathrm{K}⟧ =
  \lambda\rho\omega\kappa\;.\;\mathit{send}\,(\mathcal{K}⟦\mathrm{K}⟧)\,\kappa$$

$$
\begin{aligned}
\mathcal{E}⟦\mathrm{I}⟧ = 
  \lambda\rho\omega\kappa\;.\;\mathit{hold}\;
    (\mathit{lookup}\;\rho\;\mathrm{I}) \\
(\mathit{single}(\lambda\epsilon\;.\;
        \epsilon = \mathit{undefined}\rightarrow \\
\text{}\mathit{wrong }\mathrm{\text{“}undefined variable\text{”}}, \\
\text{}\mathit{send}\;\epsilon\;\kappa))
\end{aligned}
$$

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(\textrm{E}0 {\textrm{E}}{*})}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\mathcal{E}^{*}
    (\mathit{permute}(⟨\mathrm{E}_0⟩\;§\;{\mathrm{E}}^{*})) \\
\rho\; \\
\omega\; \\
(\lambda{\epsilon}^{*}\;.\;
        ((\lambda{\epsilon}^{*}\;.\;
                 \mathit{applicate}\;({\epsilon}^{*}\downarrow 1)
                                \;({\epsilon}^{*}\dagger 1)
                                \;\omega\kappa) \\
(\mathit{unpermute}\;{\epsilon}^{*})))
\end{aligned}
$$

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(\texttt{lambda} ({\textrm{I}}{*}) {Γ}{*} \textrm{E}0)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\lambda\sigma\;.\; \\
\text{}\mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{send}\;
     (⟨
         \mathit{new}\;\sigma\,\vert\,\mathtt{L}, \\
\lambda{\epsilon}^{*}\omega^\prime\kappa^\prime\;.\;
               \#{\epsilon}^{*} = \#{{\mathrm{I}}^{*}}\rightarrow \\
\text{}\mathit{tievals}
                   (\lambda{\alpha}^{*}\;.\;
                         (\lambda\rho^\prime\;.\;\mathcal{C}⟦{\Gamma}^{*}⟧\rho^\prime\omega^\prime
                              (\mathcal{E}⟦\mathrm{E}_0⟧\rho^\prime\omega^\prime\kappa^\prime)) \\
(\mathit{extends}\;\rho\;{{\mathrm{I}}^{*}}\;{\alpha}^{*})) \\
{\epsilon}^{*}, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}⟩ \\
\mathrm{in }\mathtt{E}) \\
\kappa \\
(\mathit{update}\;(\mathit{new}\;\sigma\,\vert\,\mathtt{L})
                           \;\mathit{unspecified}
                           \;\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\;\sigma
\end{aligned}
$$

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(lambda ({\textrm{I}}{*} .\ \textrm{I}) {Γ}{*} \textrm{E}0)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\lambda\sigma\;.\; \\
\text{}\mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{send}\;
     (⟨
         \mathit{new}\;\sigma\,\vert\,\mathtt{L}, \\
\lambda{\epsilon}^{*}\omega^\prime\kappa^\prime\;.\;
               \#{\epsilon}^{*} \geq \#{\mathrm{I}}^{*}\rightarrow \\
\text{}\mathit{tievalsrest} \\
\text{}(\lambda{\alpha}^{*}\;.\;
                           (\lambda\rho^\prime\;.\;\mathcal{C}⟦{\Gamma}^{*}⟧\rho^\prime\omega^\prime
                               (\mathcal{E}⟦\mathrm{E}_0⟧\rho^\prime\omega^\prime\kappa^\prime)) \\
(\mathit{extends}\;\rho
                               \;({\mathrm{I}}^{*}\;§\;⟨\mathrm{I}⟩)
                               \;{\alpha}^{*})) \\
{\epsilon}^{*} \\
(\#{\mathrm{I}}^{*}), \\
\text{}\mathit{wrong }\mathrm{\text{“}too few arguments\text{”}}⟩\mathrm{in }\mathtt{E}) \\
\kappa \\
(\mathit{update}\;(\mathit{new}\;\sigma\,\vert\,\mathtt{L})
                           \;\mathit{unspecified}
                           \;\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\;\sigma
\end{aligned}
$$

$$\mathcal{E}⟦\text{\texttt{(lambda \textrm{I} {Γ}{*} \textrm{E}0)}}⟧ =
 \mathcal{E}⟦\text{\texttt{(lambda (.\ \textrm{I}) {Γ}{*} \textrm{E}0)}}⟧$$

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(\texttt{if} \textrm{E}0 \textrm{E}1 \textrm{E}2)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
   \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;(\mathit{single}\;(\lambda\epsilon\;.\;
    \mathit{truish}\;\epsilon\rightarrow\mathcal{E}⟦\mathrm{E}_1⟧\rho\omega\kappa, \\
\text{}\mathcal{E}⟦\mathrm{E}_2⟧\rho\omega\kappa))
\end{aligned}
$$

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(if \textrm{E}0 \textrm{E}1)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
   \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;(\mathit{single}\;(\lambda\epsilon\;.\;
    \mathit{truish}\;\epsilon\rightarrow\mathcal{E}⟦\mathrm{E}_1⟧\rho\omega\kappa, \\
\text{}\mathit{send}\;\mathit{unspecified}\;\kappa))
\end{aligned}
$$

Here and elsewhere, any expressed value other than *undefined* may
be used in place of *unspecified*.

$$
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(\texttt{set!} \textrm{I} \textrm{E})}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\mathcal{E}⟦\mathrm{E}⟧\;\rho\;\omega\;
     (\mathit{single}(\lambda\epsilon\;.\;\mathit{assign}\;
       (\mathit{lookup}\;\rho\;\mathrm{I}) \\
\epsilon \\
(\mathit{send}\;\mathit{unspecified}\;\kappa)))
\end{aligned}
$$

$$\mathcal{E}^{*}⟦\;⟧ =
  \lambda\rho\omega\kappa\;.\;\kappa⟨\;⟩$$

$$
\begin{aligned}
\mathcal{E}^{*}⟦\mathrm{E}_0\;{\mathrm{E}}^{*}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
      \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;
         (\mathit{single}
            (\lambda\epsilon_0\;.\;\mathcal{E}^{*}⟦{\mathrm{E}}^{*}⟧
                \;\rho\omega\;(\lambda{\epsilon}^{*}\;.\;
                           \kappa\;(⟨\epsilon_0⟩\;§\;{\epsilon}^{*}))))
\end{aligned}
$$

$$\mathcal{C}⟦\;⟧ = \lambda\rho\omega\theta\,.\;\theta$$

$$\mathcal{C}⟦\Gamma_0\;{\Gamma}^{*}⟧ =
  \lambda\rho\omega\theta\;.\;\mathcal{E}⟦\Gamma_0⟧\;\rho\omega\;(\lambda{\epsilon}^{*}\;.\;
   \mathcal{C}⟦{\Gamma}^{*}⟧\rho\omega\theta)$$

### Auxiliary functions

$$
\begin{aligned}
\mathit{lookup}        :  \mathtt{U} \to \mathrm{Ide} \to \mathtt{L} \\

\mathit{lookup} =
 \lambda\rho\mathrm{I}\;.\;\rho\mathrm{I}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{extends}       :  \mathtt{U} \to {\mathrm{Ide}}^{*} \to {\mathtt{L}}^{*} \to \mathtt{U} \\

\mathit{extends} = \\
\text{}\lambda\rho{\mathrm{I}}^{*}{\alpha}^{*}\;.\;
   \#{\mathrm{I}}^{*}=0\rightarrow\rho, \\
\text{}\mathit{extends}\;(\rho[({\alpha}^{*}\downarrow 1)/({\mathrm{I}}^{*}\downarrow 1)])
                               \;({\mathrm{I}}^{*}\dagger 1)
                               \;({\alpha}^{*}\dagger 1)
\end{aligned}
$$

$$\mathit{wrong}  :  \mathtt{X} \to \mathtt{C}    \text{\qquad [implementation-dependent]}$$

$$
\begin{aligned}
\mathit{send}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\

\mathit{send} =
 \lambda\epsilon\kappa\;.\;\kappa⟨\epsilon⟩
\end{aligned}
$$

$$
\begin{aligned}
\mathit{single}        :  (\mathtt{E} \to \mathtt{C}) \to \mathtt{K} \\

\mathit{single} = \\
\text{}\lambda\psi{\epsilon}^{*}\;.\;
   \#{\epsilon}^{*}=1\rightarrow\psi({\epsilon}^{*}\downarrow 1), \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of return values\text{”}}
\end{aligned}
$$

$$\mathit{new}           :  \mathtt{S} \to (\mathtt{L} + \{ \mathit{error} \})
    \text{\qquad [implementation-dependent]}$$

$$
\begin{aligned}
\mathit{hold}          :  \mathtt{L} \to \mathtt{K} \to \mathtt{C} \\

\mathit{hold} =
 \lambda\alpha\kappa\sigma\;.\;\mathit{send}\,(\sigma\alpha\downarrow 1)\kappa\sigma
\end{aligned}
$$

$$
\begin{aligned}
\mathit{assign}        :  \mathtt{L} \to \mathtt{E} \to \mathtt{C} \to \mathtt{C} \\

\mathit{assign} =
 \lambda\alpha\epsilon\theta\sigma\;.\;\theta(\mathit{update}\;\alpha\epsilon\sigma)
\end{aligned}
$$

$$
\begin{aligned}
\mathit{update}        :  \mathtt{L} \to \mathtt{E} \to \mathtt{S} \to \mathtt{S} \\

\mathit{update} =
 \lambda\alpha\epsilon\sigma\;.\;\sigma[⟨\epsilon,\mathit{true}⟩/\alpha]
\end{aligned}
$$

$$
\begin{aligned}
\mathit{tievals}       :  ({\mathtt{L}}^{*} \to \mathtt{C}) \to {\mathtt{E}}^{*} \to \mathtt{C} \\

\mathit{tievals} = \\
\text{}\lambda\psi{\epsilon}^{*}\sigma\;.\;
   \#{\epsilon}^{*}=0\rightarrow\psi⟨\;⟩\sigma, \\
\mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow\mathit{tievals}\,
       (\lambda{\alpha}^{*}\;.\;\psi(⟨\mathit{new}\;\sigma\;\vert\;\mathtt{L}⟩
                                     \;§\;{\alpha}^{*})) \\
({\epsilon}^{*}\dagger 1) \\
(\mathit{update}(\mathit{new}\;\sigma\;\vert\;\mathtt{L})
                                 ({\epsilon}^{*}\downarrow 1)
                                 \sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\sigma
\end{aligned}
$$

$$
\begin{aligned}
\mathit{tievalsrest}   :  ({\mathtt{L}}^{*} \to \mathtt{C}) \to {\mathtt{E}}^{*} \to \mathtt{N} \to \mathtt{C} \\

\mathit{tievalsrest} = \\
\text{}\lambda\psi{\epsilon}^{*}\nu\;.\;\mathit{list}\;
   (\mathit{dropfirst}\;{\epsilon}^{*}\nu) \\
(\mathit{single}(\lambda\epsilon\;.\;\mathit{tievals}\;\psi\;
           ((\mathit{takefirst}\;{\epsilon}^{*}\nu)\;§\;⟨\epsilon⟩)))
\end{aligned}
$$

$$\mathit{dropfirst} =
 \lambda l n \;.\;  n=0 \rightarrow l, \mathit{dropfirst}\,(l \dagger 1)(n - 1)$$

$$\mathit{takefirst} =
 \lambda l n \;.\; n=0 \rightarrow ⟨\;⟩,
     ⟨ l \downarrow 1⟩\;§\;(\mathit{takefirst}\,(l \dagger 1)(n - 1))$$

$$
\begin{aligned}
\mathit{truish}        :  \mathtt{E} \to \mathtt{T} \\

\mathit{truish} =
  \lambda\epsilon\;.\;

     \epsilon = \mathit{false}\rightarrow
          \mathit{false},
          \mathit{true}
\end{aligned}
$$

$$\mathit{permute}       :  {\mathrm{Exp}}^{*} \to {\mathrm{Exp}}^{*}
    \text{\qquad [implementation-dependent]}$$

$$\mathit{unpermute}     :  {\mathtt{E}}^{*} \to {\mathtt{E}}^{*}
    \text{\qquad [inverse of \textit{permute}]}$$

$$
\begin{aligned}
\mathit{applicate}     :  \mathtt{E} \to {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{applicate} = \\
\text{}\lambda\epsilon{\epsilon}^{*}\omega\kappa\;.\;
   \epsilon\;\in\;\mathtt{F}\rightarrow(\epsilon\;\vert\;\mathtt{F}\downarrow 2){\epsilon}^{*}\omega\kappa,
          \mathit{wrong }\mathrm{\text{“}bad procedure\text{”}}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{onearg}      :  (\mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\

\mathit{onearg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=1\rightarrow\zeta({\epsilon}^{*}\downarrow 1)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{twoarg}      :  (\mathtt{E} \to \mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\

\mathit{twoarg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=2\rightarrow\zeta({\epsilon}^{*}\downarrow 1)({\epsilon}^{*}\downarrow 2)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{threearg}      :  (\mathtt{E} \to \mathtt{E} \to \mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\

\mathit{threearg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=3\rightarrow\zeta({\epsilon}^{*}\downarrow 1)({\epsilon}^{*}\downarrow 2)({\epsilon}^{*}\downarrow 3)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{list}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{list} = \\
\text{}\lambda{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=0\rightarrow\mathit{send}\;\mathit{null}\;\kappa, \\
\text{}\mathit{list}\,({\epsilon}^{*}\dagger 1)
             (\mathit{single}(\lambda\epsilon\;.\;
                   \mathit{cons}⟨{\epsilon}^{*}\downarrow 1,\epsilon⟩\kappa))
\end{aligned}
$$

$$
\begin{aligned}
\mathit{cons}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{cons} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\kappa\omega\sigma\;.\;
   \mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
(\lambda\sigma^\prime\;.\;
           \mathit{new}\;\sigma^\prime\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{send}\,
               (⟨\mathit{new}\;\sigma\;\vert\;\mathtt{L},
                                            \mathit{new}\;\sigma^\prime\;\vert\;\mathtt{L},
         \mathit{true}⟩ \\
\mathrm{in }\mathtt{E}) \\
\kappa \\
(\mathit{update}(\mathit{new}\;\sigma^\prime\;\vert\;\mathtt{L})
                                     \epsilon_2
                                     \sigma^\prime), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\sigma^\prime) \\
(\mathit{update}(\mathit{new}\;\sigma\;\vert\;\mathtt{L})\epsilon_1\sigma), \\
\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\sigma)
\end{aligned}
$$

$$
\begin{aligned}
\mathit{less}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{less} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   (\epsilon_1\;\in\;\mathtt{R}\wedge\epsilon_2\;\in\;\mathtt{R})\rightarrow \\
\text{}\mathit{send}\,
               (\epsilon_1\;\vert\;\mathtt{R}<\epsilon_2\;\vert\;\mathtt{R}\rightarrow
                   \mathit{true},
                   \mathit{false})
               \kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-numeric argument to { <}\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{add}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{add} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   (\epsilon_1\;\in\;\mathtt{R}\wedge\epsilon_2\;\in\;\mathtt{R})\rightarrow \\
\text{}\mathit{send}\,
       ((\epsilon_1\;\vert\;\mathtt{R}+\epsilon_2\;\vert\;\mathtt{R})\mathrm{in }\mathtt{E})
           \kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-numeric argument to { +}\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{car}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{car} = \\
\text{}\mathit{onearg}\,(\lambda\epsilon\omega\kappa\;.\;
   \epsilon\;\in\;\text{\texttt{E}\textrm{p}}\rightarrow
          \mathit{car-internal}\;\epsilon\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-pair argument to { car}\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{car-internal}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\

\mathit{car-internal} =
 \text{}\lambda\epsilon\omega\kappa\;.\;
   \mathit{hold}\, (\epsilon\;\vert\;\text{\texttt{E}\textrm{p}}\downarrow 1) \kappa
\end{aligned}
$$

$$\mathit{cdr}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} 
\text{\qquad [similar to \textit{car}]}$$

$$\mathit{cdr-internal} :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} 
\text{\qquad [similar to \textit{car-internal}]}$$

$$
\begin{aligned}
\mathit{setcar}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{setcar} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \epsilon_1\;\in\;\text{\texttt{E}\textrm{p}}\rightarrow \\
(\epsilon_1\;\vert\;\text{\texttt{E}\textrm{p}}\downarrow 3)\rightarrow
          \mathit{assign}\,(\epsilon_1\;\vert\;\text{\texttt{E}\textrm{p}}\downarrow 1) \\
\epsilon_2 \\
(\mathit{send}\;\mathit{unspecified}\;\kappa), \\
\mathit{wrong }\mathrm{\text{“}immutable argument to { set-car!}\text{”}}, \\
\mathit{wrong }\mathrm{\text{“}non-pair argument to { set-car!}\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{eqv}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{eqv} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   (\epsilon_1\;\in\;\mathtt{M}\wedge\epsilon_2\;\in\;\mathtt{M})\rightarrow \\
\text{}\mathit{send}\,
       (\epsilon_1\;\vert\;\mathtt{M} = \epsilon_2\;\vert\;\mathtt{M}\rightarrow\mathit{true},
            \mathit{false})\kappa, \\
(\epsilon_1\;\in\;\mathtt{Q}\wedge\epsilon_2\;\in\;\mathtt{Q})\rightarrow \\
\text{}\mathit{send}\,
       (\epsilon_1\;\vert\;\mathtt{Q} = \epsilon_2\;\vert\;\mathtt{Q}\rightarrow\mathit{true},
            \mathit{false})\kappa, \\
(\epsilon_1\;\in\;\mathtt{H}\wedge\epsilon_2\;\in\;\mathtt{H})\rightarrow \\
\text{}\mathit{send}\,
       (\epsilon_1\;\vert\;\mathtt{H} = \epsilon_2\;\vert\;\mathtt{H} \rightarrow\mathit{true},
            \mathit{false})\kappa, \\
(\epsilon_1\;\in\;\mathtt{R}\wedge\epsilon_2\;\in\;\mathtt{R})\rightarrow \\
\text{}\mathit{send}\,
       (\epsilon_1\;\vert\;\mathtt{R}=\epsilon_2\;\vert\;\mathtt{R}\rightarrow\mathit{true},
            \mathit{false})\kappa, \\
(\epsilon_1\;\in\;\text{\texttt{E}\textrm{p}}\wedge\epsilon_2\;\in\;\text{\texttt{E}\textrm{p}})\rightarrow \\
\text{}\mathit{send}\,
       ((\lambda{p_1}{p_2}\;.\;
                (({p_1}\downarrow 1) = ({p_2}\downarrow 1)\wedge \\
({p_1}\downarrow 2) = ({p_2}\downarrow 2))
                     \rightarrow\mathit{true}, \\
\text{}\mathit{false}) \\
(\epsilon_1\;\vert\;\text{\texttt{E}\textrm{p}}) \\
(\epsilon_2\;\vert\;\text{\texttt{E}\textrm{p}})) \\
\kappa, \\
(\epsilon_1\;\in\;\text{\texttt{E}\textrm{v}}\wedge\epsilon_2\;\in\;\text{\texttt{E}\textrm{v}})\rightarrow

\ldots, \\
(\epsilon_1\;\in\;\text{\texttt{E}\textrm{s}}\wedge\epsilon_2\;\in\;\text{\texttt{E}\textrm{s}})\rightarrow

\ldots, \\
(\epsilon_1\;\in\;\mathtt{F}\wedge\epsilon_2\;\in\;\mathtt{F})\rightarrow \\
\text{}\mathit{send}\,
       ((\epsilon_1\;\vert\;\mathtt{F}\downarrow 1) = (\epsilon_2\;\vert\;\mathtt{F}\downarrow 1)
               \rightarrow\mathit{true},
                          \mathit{false}) \\
\kappa, \\
\text{}\mathit{send}\,\;\mathit{false}\;\kappa)
\end{aligned}
$$

$$
\begin{aligned}
\mathit{apply}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{apply} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \epsilon_1\;\in\;\mathtt{F}\rightarrow
         \mathit{valueslist}\;\epsilon_2
            (\lambda{\epsilon}^{*}\;.\;\mathit{applicate}\;\epsilon_1{\epsilon}^{*}\omega\kappa), \\
\text{}\mathit{wrong }\mathrm{\text{“}bad procedure argument to { apply}\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{valueslist}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\

\mathit{valueslist} = \\
\text{}\lambda\epsilon\kappa\;.\;
   \epsilon\;\in\;\text{\texttt{E}\textrm{p}}\rightarrow \\
\text{}\mathit{cdr-internal}\;
         \epsilon \\
(\lambda{\epsilon}^{*}\;.\;
                  \mathit{valueslist}\; \\
{\epsilon}^{*} \\
(\lambda{\epsilon}^{*}\;.\;\mathit{car-internal} \\
\;\epsilon \\
 (\mathit{single}(\lambda\epsilon\;.\;
              \kappa(⟨\epsilon⟩\;§\;{\epsilon}^{*}))))), \\
\epsilon = \mathit{null}\rightarrow\kappa⟨\;⟩, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-list argument to { values-list}\text{”}}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{cwcc}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

     \text{\qquad [\texttt{call-with-current-continuation}]} \\

\mathit{cwcc} = \\
\text{}\mathit{onearg}\,(\lambda\epsilon\omega\kappa\;.\;
   \epsilon\;\in\;\mathtt{F}\rightarrow \\
(\lambda\sigma\;.\;
       \mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{applicate}\;
           \epsilon \\
⟨⟨\mathit{new}\;\sigma\;\vert\;\mathtt{L}, \\
          \lambda{\epsilon}^{*}\omega^\prime\kappa^\prime\;.\;
                             \mathit{travel}\;\omega^\prime\omega(\kappa{\epsilon}^{*})⟩ \\
                      \mathrm{in }\mathtt{E}⟩ \\
\omega \\
\kappa \\
(\mathit{update}\,
                (\mathit{new}\;\sigma\;\vert\;\mathtt{L}) \\
\mathit{unspecified} \\
\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\,\sigma), \\
\mathit{wrong }\mathrm{\text{“}bad procedure argument\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{travel} : {P} \to {P} \to \mathtt{C} \to \mathtt{C} \\

\mathit{travel} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \mathit{travelpath}\;((\mathit{pathup}\;\omega_1(\mathit{commonancest}\;\omega_1\omega_2)) \;§\; \\
 (\mathit{pathdown}\;(\mathit{commonancest}\;\omega_1\omega_2)\omega_2))
\end{aligned}
$$

$$
\begin{aligned}
\mathit{pointdepth} : {P} \to \mathtt{N} \\

\mathit{pointdepth} =  \\
\text{}\lambda\omega\;.\; \omega = \textit{root} \rightarrow 0,
  1 + (\mathit{pointdepth}\;(\omega\;\vert\;(\mathtt{F} \times \mathtt{F} \times
  {P})\downarrow 3))
\end{aligned}
$$

$$
\begin{aligned}
\mathit{ancestors} : {P} \to \mathcal{P}{P} \\

\mathit{ancestors} =  \\
\text{}\lambda\omega\;.\; \omega = \textit{root} \rightarrow \{\omega\},
  \{\omega\}\;\cup\;(\mathit{ancestors}\;(\omega\;\vert\;(\mathtt{F} \times \mathtt{F} \times
  {P})\downarrow 3))
\end{aligned}
$$

$$
\begin{aligned}
\mathit{commonancest} : {P} \to {P} \to {P} \\

\mathit{commonancest} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \textrm{the only element of } \\
\{ \omega^\prime \;\mid\;
  \omega^\prime\in(\mathit{ancestors}\;\omega_1)\;\cap\;(\mathit{ancestors}\;\omega_2), \\
\mathit{pointdepth}\;\omega^\prime\geq \mathit{pointdepth}\;\omega^{\prime\prime} \\
\forall
  \omega^{\prime\prime}\in(\mathit{ancestors}\;\omega_1)\;\cap\;(\mathit{ancestors}\;\omega_2)\}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{pathup} : {P} \to {P} \to {({P} \times \mathtt{F})}^{*} \\

\mathit{pathup} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \omega_1=\omega_2\rightarrow⟨⟩, \\
⟨(\omega_1, \omega_1\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 2)⟩
  \;§\; \\
(\mathit{pathup}\;(\omega_1\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 3)\omega_2)
\end{aligned}
$$

$$
\begin{aligned}
\mathit{pathdown} : {P} \to {P} \to {({P} \times \mathtt{F})}^{*} \\

\mathit{pathdown} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \omega_1=\omega_2\rightarrow⟨⟩, \\
(\mathit{pathdown}\;\omega_1(\omega_2\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 3))
  \;§\; \\
⟨(\omega_2, \omega_2\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 1)⟩
\end{aligned}
$$

$$
\begin{aligned}
\mathit{travelpath} : {({P} \times \mathtt{F})}^{*} \to \mathtt{C} \to \mathtt{C} \\

\mathit{travelpath} =  \\
\text{}\lambda{\pi}^{*}\theta\;.\;
  \#{\pi}^{*}=0\rightarrow\theta, \\
(({\pi}^{*}\downarrow 1)\downarrow 2)⟨⟩(({\pi}^{*}\downarrow 1)\downarrow 1) \\
(\lambda{\epsilon}^{*}\;.\;\mathit{travelpath}\;({\pi}^{*} \dagger 1)\theta)
\end{aligned}
$$

$$
\begin{aligned}
\mathit{dynamicwind} : {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{dynamicwind} =  \\
\text{}\mathit{threearg}\,(\lambda\epsilon_1\epsilon_2\epsilon_3\omega\kappa\;.\;
  (\epsilon_1\;\in\;\mathtt{F}\wedge\epsilon_2\;\in\;\mathtt{F}\wedge\epsilon_3\;\in\;\mathtt{F})\rightarrow \\
\mathit{applicate}\;
  \epsilon_1⟨⟩\omega(\lambda{\zeta}^{*}\;.\; \\
\mathit{applicate}\;\epsilon_2⟨⟩
  ((\epsilon_1\;\vert\;\mathtt{F},\epsilon_3\;\vert\;\mathtt{F},\omega)\textrm{ in }{P}) \\
(\lambda{\epsilon}^{*}\;.\;\mathit{applicate}\;\epsilon_3⟨⟩\omega(\lambda{\zeta}^{*}\;.\;\kappa{\epsilon}^{*}))), \\
\mathit{wrong }\mathrm{\text{“}bad procedure argument\text{”}})
\end{aligned}
$$

$$
\begin{aligned}
\mathit{values}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\

\mathit{values} =
 \lambda{\epsilon}^{*}\omega\kappa\;.\;\kappa{\epsilon}^{*}
\end{aligned}
$$

$$
\begin{aligned}
\mathit{cwv}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}
    \text{\qquad [\texttt{call-with-values}]} \\

\mathit{cwv} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \mathit{applicate}\;\epsilon_1⟨\;⟩\omega
(\lambda{\epsilon}^{*}\;.\;\mathit{applicate}\;\epsilon_2\;{\epsilon}^{*}\omega))
\end{aligned}
$$

## Derived expression types

<a id="derivedsection"></a>

This section gives syntax definitions for the derived expression types in
terms of the primitive expression types (literal, variable, call, `lambda`,
`if`, and `set!`), except for `quasiquote`.

Conditional derived syntax types:

```scheme
(define-syntax cond
  (syntax-rules (else =>)
    ((cond (else result1 result2 ...))
     (begin result1 result2 ...))
    ((cond (test => result))
     (let ((temp test))
       (if temp (result temp))))
    ((cond (test => result) clause1 clause2 ...)
     (let ((temp test))
       (if temp
           (result temp)
           (cond clause1 clause2 ...))))
    ((cond (test)) test)
    ((cond (test) clause1 clause2 ...)
     (let ((temp test))
       (if temp
           temp
           (cond clause1 clause2 ...))))
    ((cond (test result1 result2 ...))
     (if test (begin result1 result2 ...)))
    ((cond (test result1 result2 ...)
           clause1 clause2 ...)
     (if test
         (begin result1 result2 ...)
         (cond clause1 clause2 ...)))))
```

```scheme
(define-syntax case
  (syntax-rules (else =>)
    ((case (key ...)
       clauses ...)
     (let ((atom-key (key ...)))
       (case atom-key clauses ...)))
    ((case key
       (else => result))
     (result key))
    ((case key
       (else result1 result2 ...))
     (begin result1 result2 ...))
    ((case key
       ((atoms ...) => result))
     (if (memv key '(atoms ...))
         (result key)))
    ((case key
       ((atoms ...) result1 result2 ...))
     (if (memv key '(atoms ...))
         (begin result1 result2 ...)))
    ((case key
       ((atoms ...) => result)
       clause clauses ...)
     (if (memv key '(atoms ...))
         (result key)
         (case key clause clauses ...)))
    ((case key
       ((atoms ...) result1 result2 ...)
       clause clauses ...)
     (if (memv key '(atoms ...))
         (begin result1 result2 ...)
         (case key clause clauses ...)))))
```

```scheme
(define-syntax and
  (syntax-rules ()
    ((and) #t)
    ((and test) test)
    ((and test1 test2 ...)
     (if test1 (and test2 ...) #f))))
```

```scheme
(define-syntax or
  (syntax-rules ()
    ((or) #f)
    ((or test) test)
    ((or test1 test2 ...)
     (let ((x test1))
       (if x x (or test2 ...))))))
```

```scheme
(define-syntax when
  (syntax-rules ()
    ((when test result1 result2 ...)
     (if test
         (begin result1 result2 ...)))))
```

```scheme
(define-syntax unless
  (syntax-rules ()
    ((unless test result1 result2 ...)
     (if (not test)
         (begin result1 result2 ...)))))
```

Binding constructs:

```scheme
(define-syntax let
  (syntax-rules ()
    ((let ((name val) ...) body1 body2 ...)
     ((lambda (name ...) body1 body2 ...)
      val ...))
    ((let tag ((name val) ...) body1 body2 ...)
     ((letrec ((tag (lambda (name ...)
                      body1 body2 ...)))
        tag)
      val ...))))
```

```scheme
(define-syntax let*
  (syntax-rules ()
    ((let* () body1 body2 ...)
     (let () body1 body2 ...))
    ((let* ((name1 val1) (name2 val2) ...)
       body1 body2 ...)
     (let ((name1 val1))
       (let* ((name2 val2) ...)
         body1 body2 ...)))))
```

The following `letrec` macro uses the symbol `<undefined>`
in place of an expression which returns something that when stored in
a location makes it an error to try to obtain the value stored in the
location. (No such expression is defined in Scheme.)
A trick is used to generate the temporary names needed to avoid
specifying the order in which the values are evaluated.
This could also be accomplished by using an auxiliary macro.

```scheme
(define-syntax letrec
  (syntax-rules ()
    ((letrec ((var1 init1) ...) body ...)
     (letrec "generate_temp_names"
       (var1 ...)
       ()
       ((var1 init1) ...)
       body ...))
    ((letrec "generate_temp_names"
       ()
       (temp1 ...)
       ((var1 init1) ...)
       body ...)
     (let ((var1 <undefined>) ...)
       (let ((temp1 init1) ...)
         (set! var1 temp1)
         ...
         body ...)))
    ((letrec "generate_temp_names"
       (x y ...)
       (temp ...)
       ((var1 init1) ...)
       body ...)
     (letrec "generate_temp_names"
       (y ...)
       (newtemp temp ...)
       ((var1 init1) ...)
       body ...))))
```

```scheme
(define-syntax letrec*
  (syntax-rules ()
    ((letrec* ((var1 init1) ...) body1 body2 ...)
     (let ((var1 <undefined>) ...)
       (set! var1 init1)
       ...
       (let () body1 body2 ...)))))
```

```scheme
(define-syntax let-values
  (syntax-rules ()
    ((let-values (binding ...) body0 body1 ...)
     (let-values "bind"
         (binding ...) () (begin body0 body1 ...)))

    ((let-values "bind" () tmps body)
     (let tmps body))

    ((let-values "bind" ((b0 e0)
         binding ...) tmps body)
     (let-values "mktmp" b0 e0 ()
         (binding ...) tmps body))

    ((let-values "mktmp" () e0 args
         bindings tmps body)
     (call-with-values
       (lambda () e0)
       (lambda args
         (let-values "bind"
             bindings tmps body))))

    ((let-values "mktmp" (a . b) e0 (arg ...)
         bindings (tmp ...) body)
     (let-values "mktmp" b e0 (arg ... x)
         bindings (tmp ... (a x)) body))

    ((let-values "mktmp" a e0 (arg ...)
        bindings (tmp ...) body)
     (call-with-values
       (lambda () e0)
       (lambda (arg ... . x)
         (let-values "bind"
             bindings (tmp ... (a x)) body))))))
```

```scheme
(define-syntax let*-values
  (syntax-rules ()
    ((let*-values () body0 body1 ...)
     (let () body0 body1 ...))

    ((let*-values (binding0 binding1 ...)
         body0 body1 ...)
     (let-values (binding0)
       (let*-values (binding1 ...)
         body0 body1 ...)))))
```

```scheme
(define-syntax define-values
  (syntax-rules ()
    ((define-values () expr)
     (define dummy
       (call-with-values (lambda () expr)
                         (lambda args #f))))
    ((define-values (var) expr)
     (define var expr))
    ((define-values (var0 var1 ... varn) expr)
     (begin
       (define var0
         (call-with-values (lambda () expr)
                           list))
       (define var1
         (let ((v (cadr var0)))
           (set-cdr! var0 (cddr var0))
           v)) ...
       (define varn
         (let ((v (cadr var0)))
           (set! var0 (car var0))
           v))))
    ((define-values (var0 var1 ... . varn) expr)
     (begin
       (define var0
         (call-with-values (lambda () expr)
                           list))
       (define var1
         (let ((v (cadr var0)))
           (set-cdr! var0 (cddr var0))
           v)) ...
       (define varn
         (let ((v (cdr var0)))
           (set! var0 (car var0))
           v))))
    ((define-values var expr)
     (define var
       (call-with-values (lambda () expr)
                         list)))))
```

```scheme
(define-syntax begin
  (syntax-rules ()
    ((begin exp ...)
     ((lambda () exp ...)))))
```

The following alternative expansion for `begin` does not make use of
the ability to write more than one expression in the body of a lambda
expression. In any case, note that these rules apply only if the body
of the `begin` contains no definitions.

```scheme
(define-syntax begin
  (syntax-rules ()
    ((begin exp)
     exp)
    ((begin exp1 exp2 ...)
     (call-with-values
         (lambda () exp1)
       (lambda args
         (begin exp2 ...))))))
```

The following syntax definition
of `do` uses a trick to expand the variable clauses.
As with `letrec` above, an auxiliary macro would also work.
The expression `(if #f #f)` is used to obtain an unspecific
value.

```scheme
(define-syntax do
  (syntax-rules ()
    ((do ((var init step ...) ...)
         (test expr ...)
         command ...)
     (letrec
       ((loop
         (lambda (var ...)
           (if test
               (begin
                 (if #f #f)
                 expr ...)
               (begin
                 command
                 ...
                 (loop (do "step" var step ...)
                       ...))))))
       (loop init ...)))
    ((do "step" x)
     x)
    ((do "step" x y)
     y)))
```

Here is a possible implementation of `delay`, `force` and `delay-force`. We define the expression

```scheme
(delay-force ⟨expression⟩)
```

to have the same meaning as the procedure call

```scheme
(make-promise #f (lambda () ⟨expression⟩))
```

as follows

```scheme
(define-syntax delay-force
  (syntax-rules ()
    ((delay-force expression)
     (make-promise #f (lambda () expression)))))
```

and we define the expression

```scheme
(delay ⟨expression⟩)
```

to have the same meaning as:

```scheme
(delay-force (make-promise #t ⟨expression⟩))
```

as follows

```scheme
(define-syntax delay
  (syntax-rules ()
    ((delay expression)
     (delay-force (make-promise #t expression)))))
```

where `make-promise` is defined as follows:

```scheme
(define make-promise
  (lambda (done? proc)
    (list (cons done? proc))))
```

Finally, we define `force` to call the procedure expressions in
promises iteratively using a trampoline technique following
[[srfi45](#cite-srfi45)] until a non-lazy result (i.e. a value created by `delay` instead of `delay-force`) is returned, as follows:

```scheme
(define (force promise)
  (if (promise-done? promise)
      (promise-value promise)
      (let ((promise* ((promise-value promise))))
        (unless (promise-done? promise)
          (promise-update! promise* promise))
        (force promise))))
```

with the following promise accessors:

```scheme
(define promise-done?
  (lambda (x) (car (car x))))
(define promise-value
  (lambda (x) (cdr (car x))))
(define promise-update!
  (lambda (new old)
    (set-car! (car old) (promise-done? new))
    (set-cdr! (car old) (promise-value new))
    (set-car! new (car old))))
```

The following implementation of `make-parameter` and `parameterize` is suitable for an implementation with no threads.
Parameter objects are implemented here as procedures, using two
arbitrary unique objects `<param-set!>` and
`<param-convert>`:

```scheme
(define (make-parameter init . o)
  (let* ((converter
          (if (pair? o) (car o) (lambda (x) x)))
         (value (converter init)))
    (lambda args
      (cond
       ((null? args)
        value)
       ((eq? (car args) <param-set!>)
        (set! value (cadr args)))
       ((eq? (car args) <param-convert>)
        converter)
       (else
        (error "bad parameter syntax"))))))
```

Then `parameterize` uses `dynamic-wind` to dynamically rebind
the associated value:

```scheme
(define-syntax parameterize
  (syntax-rules ()
    ((parameterize ("step")
                   ((param value p old new) ...)
                   ()
                   body)
     (let ((p param) ...)
       (let ((old (p)) ...
             (new ((p <param-convert>) value)) ...)
         (dynamic-wind
          (lambda () (p <param-set!> new) ...)
          (lambda () . body)
          (lambda () (p <param-set!> old) ...)))))
    ((parameterize ("step")
                   args
                   ((param value) . rest)
                   body)
     (parameterize ("step")
                   ((param value p old new) . args)
                   rest
                   body))
    ((parameterize ((param value) ...) . body)
     (parameterize ("step")
                   ()
                   ((param value) ...)
                   body))))
```

The following implementation of `guard` depends on an auxiliary
macro, here called `guard-aux`.

```scheme
(define-syntax guard
  (syntax-rules ()
    ((guard (var clause ...) e1 e2 ...)
     ((call/cc
       (lambda (guard-k)
         (with-exception-handler
          (lambda (condition)
            ((call/cc
               (lambda (handler-k)
                 (guard-k
                  (lambda ()
                    (let ((var condition))
                      (guard-aux
                        (handler-k
                          (lambda ()
                            (raise-continuable condition)))
                        clause ...))))))))
          (lambda ()
            (call-with-values
             (lambda () e1 e2 ...)
             (lambda args
               (guard-k
                 (lambda ()
                   (apply values args)))))))))))))

(define-syntax guard-aux
  (syntax-rules (else =>)
    ((guard-aux reraise (else result1 result2 ...))
     (begin result1 result2 ...))
    ((guard-aux reraise (test => result))
     (let ((temp test))
       (if temp
           (result temp)
           reraise)))
    ((guard-aux reraise (test => result)
                clause1 clause2 ...)
     (let ((temp test))
       (if temp
           (result temp)
           (guard-aux reraise clause1 clause2 ...))))
    ((guard-aux reraise (test))
     (or test reraise))
    ((guard-aux reraise (test) clause1 clause2 ...)
     (let ((temp test))
       (if temp
           temp
           (guard-aux reraise clause1 clause2 ...))))
    ((guard-aux reraise (test result1 result2 ...))
     (if test
         (begin result1 result2 ...)
         reraise))
    ((guard-aux reraise
                (test result1 result2 ...)
                clause1 clause2 ...)
     (if test
         (begin result1 result2 ...)
         (guard-aux reraise clause1 clause2 ...)))))
```

```scheme
(define-syntax case-lambda
  (syntax-rules ()
    ((case-lambda (params body0 ...) ...)
     (lambda args
       (let ((len (length args)))
         (letrec-syntax
             ((cl (syntax-rules ::: ()
                    ((cl)
                     (error "no matching clause"))
                    ((cl ((p :::) . body) . rest)
                     (if (= len (length '(p :::)))
                         (apply (lambda (p :::)
                                  . body)
                                args)
                         (cl . rest)))
                    ((cl ((p ::: . tail) . body)
                         . rest)
                     (if (>= len (length '(p :::)))
                         (apply
                          (lambda (p ::: . tail)
                            . body)
                          args)
                         (cl . rest))))))
           (cl (params body0 ...) ...)))))))
```

This definition of `cond-expand` does not interact with the
`features` procedure. It requires that each feature identifier provided
by the implementation be explicitly mentioned.

```scheme
(define-syntax cond-expand
  ;; Extend this to mention all feature ids and libraries
  (syntax-rules (and or not else r7rs library scheme base)
    ((cond-expand)
     (syntax-error "Unfulfilled cond-expand"))
    ((cond-expand (else body ...))
     (begin body ...))
    ((cond-expand ((and) body ...) more-clauses ...)
     (begin body ...))
    ((cond-expand ((and req1 req2 ...) body ...)
                  more-clauses ...)
     (cond-expand
       (req1
         (cond-expand
           ((and req2 ...) body ...)
           more-clauses ...))
       more-clauses ...))
    ((cond-expand ((or) body ...) more-clauses ...)
     (cond-expand more-clauses ...))
    ((cond-expand ((or req1 req2 ...) body ...)
                  more-clauses ...)
     (cond-expand
       (req1
        (begin body ...))
       (else
        (cond-expand
           ((or req2 ...) body ...)
           more-clauses ...))))
    ((cond-expand ((not req) body ...)
                  more-clauses ...)
     (cond-expand
       (req
         (cond-expand more-clauses ...))
       (else body ...)))
    ((cond-expand (r7rs body ...)
                  more-clauses ...)
       (begin body ...))
    ;; Add clauses here for each
    ;; supported feature identifier.
    ;; Samples:
    ;; ((cond-expand (exact-closed body ...)
    ;;               more-clauses ...)
    ;;   (begin body ...))
    ;; ((cond-expand (ieee-float body ...)
    ;;               more-clauses ...)
    ;;   (begin body ...))
    ((cond-expand ((library (scheme base))
                   body ...)
                  more-clauses ...)
      (begin body ...))
    ;; Add clauses here for each library
    ((cond-expand (feature-id body ...)
                  more-clauses ...)
       (cond-expand more-clauses ...))
    ((cond-expand ((library (name ...))
                   body ...)
                  more-clauses ...)
       (cond-expand more-clauses ...))))
```


# Standard Libraries

<a id="stdlibraries"></a>

This section lists the exports provided by the standard libraries. The
libraries are factored so as to separate features which might not be
supported by all implementations, or which might be expensive to load.

The `scheme` library prefix is used for all standard libraries, and
is reserved for use by future standards.

**Base Library**

The `(scheme base)` library exports many of the procedures and
syntax bindings that are traditionally associated with Scheme.
The division between the base library and the other standard libraries is
based on use, not on construction. In particular, some facilities that are
typically implemented as primitives by a compiler or the run-time system
rather than in terms of other standard procedures or syntax are
not part of the base library, but are defined in separate libraries.
By the same token, some exports of the base library are implementable
in terms of other exports. They are redundant in the strict sense of
the word, but they capture common patterns of usage, and are therefore
provided as convenient abbreviations.

```scheme
*                       +
-                       ...
/                       <
<=                      =
=>                      >
>=                      _
abs                     and
append                  apply
assoc                   assq
assv                    begin
binary-port?            boolean=?
boolean?                bytevector
bytevector-append       bytevector-copy
bytevector-copy!        bytevector-length
bytevector-u8-ref       bytevector-u8-set!
bytevector?             caar
cadr
call-with-current-continuation
call-with-port          call-with-values
call/cc                 car
case                    cdar
cddr                    cdr
ceiling                 char->integer
char-ready?             char<=?
char<?                  char=?
char>=?                 char>?
char?                   close-input-port
close-output-port       close-port
complex?                cond
cond-expand             cons
current-error-port      current-input-port
current-output-port     define
define-record-type      define-syntax
define-values           denominator
do                      dynamic-wind
else                    eof-object
eof-object?             eq?
equal?                  eqv?
error                   error-object-irritants
error-object-message    error-object?
even?                   exact
exact-integer-sqrt      exact-integer?
exact?                  expt
features                file-error?
floor                   floor-quotient
floor-remainder         floor/
flush-output-port       for-each
gcd                     get-output-bytevector
get-output-string       guard
if                      include
include-ci              inexact
inexact?                input-port-open?
input-port?             integer->char
integer?                lambda
lcm                     length
let                     let*
let*-values             let-syntax
let-values              letrec
letrec*                 letrec-syntax
list                    list->string
list->vector            list-copy
list-ref                list-set!
list-tail               list?
make-bytevector         make-list
make-parameter          make-string
make-vector             map
max                     member
memq                    memv
min                     modulo
negative?               newline
not                     null?
number->string          number?
numerator               odd?
open-input-bytevector   open-input-string
open-output-bytevector  open-output-string
or                      output-port-open?
output-port?            pair?
parameterize            peek-char
peek-u8                 port?
positive?               procedure?
quasiquote              quote
quotient                raise
raise-continuable       rational?
rationalize             read-bytevector
read-bytevector!        read-char
read-error?             read-line
read-string             read-u8
real?                   remainder
reverse                 round
set!                    set-car!
set-cdr!                square
string                  string->list
string->number          string->symbol
string->utf8            string->vector
string-append           string-copy
string-copy!            string-fill!
string-for-each         string-length
string-map              string-ref
string-set!             string<=?
string<?                string=?
string>=?               string>?
string?                 substring
symbol->string          symbol=?
symbol?                 syntax-error
syntax-rules            textual-port?
truncate                truncate-quotient
truncate-remainder      truncate/
u8-ready?               unless
unquote                 unquote-splicing
utf8->string            values
vector                  vector->list
vector->string          vector-append
vector-copy             vector-copy!
vector-fill!            vector-for-each
vector-length           vector-map
vector-ref              vector-set!
vector?                 when
with-exception-handler  write-bytevector
write-char              write-string
write-u8                zero?
```

**Case-Lambda Library**

The `(scheme case-lambda)` library exports the `case-lambda`
syntax.

```scheme
case-lambda
```

**Char Library**

The `(scheme char)` library provides the procedures for dealing with
characters that involve potentially large tables when supporting all of Unicode.

```scheme
char-alphabetic?        char-ci<=?
char-ci<?               char-ci=?
char-ci>=?              char-ci>?
char-downcase           char-foldcase
char-lower-case?        char-numeric?
char-upcase             char-upper-case?
char-whitespace?        digit-value
string-ci<=?            string-ci<?
string-ci=?             string-ci>=?
string-ci>?             string-downcase
string-foldcase         string-upcase
```

**Complex Library**

The `(scheme complex)` library exports procedures which are
typically only useful with non-real numbers.

```scheme
angle                   imag-part
magnitude               make-polar
make-rectangular        real-part
```

**CxR Library**

The `(scheme cxr)` library exports twenty-four procedures which
are the compositions of from three to four `car` and `cdr`
operations. For example `caddar` could be defined by

```scheme
(define caddar
  (lambda (x) (car (cdr (cdr (car x)))))).
```

The procedures `car` and `cdr` themselves and the four
two-level compositions are included in the base library. See
section [Pairs and lists](#listsection).

```scheme
caaaar                  caaadr
caaar                   caadar
caaddr                  caadr
cadaar                  cadadr
cadar                   caddar
cadddr                  caddr
cdaaar                  cdaadr
cdaar                   cdadar
cdaddr                  cdadr
cddaar                  cddadr
cddar                   cdddar
cddddr                  cdddr
```

**Eval Library**

The `(scheme eval)` library exports procedures for evaluating Scheme
data as programs.

```scheme
environment             eval
```

**File Library**

The `(scheme file)` library provides procedures for accessing
files.

```scheme
call-with-input-file    call-with-output-file
delete-file             file-exists?
open-binary-input-file  open-binary-output-file
open-input-file         open-output-file
with-input-from-file    with-output-to-file
```

**Inexact Library**

The `(scheme inexact)` library exports procedures which are
typically only useful with inexact values.

```scheme
acos                    asin
atan                    cos
exp                     finite?
infinite?               log
nan?                    sin
sqrt                    tan
```

**Lazy Library**

The `(scheme lazy)` library exports procedures and syntax keywords for lazy evaluation.

```scheme
delay                   delay-force
force                   make-promise
promise?
```

**Load Library**

The `(scheme load)` library exports procedures for loading
Scheme expressions from files.

```scheme
load
```

**Process-Context Library**

The `(scheme process-context)` library exports procedures for
accessing with the program's calling context.

```scheme
command-line            emergency-exit
exit
get-environment-variable
get-environment-variables
```

**Read Library**

The `(scheme read)` library provides procedures for reading
Scheme objects.

```scheme
read
```

**Repl Library**

The `(scheme repl)` library exports the `interaction-environment` procedure.

```scheme
interaction-environment
```

**Time Library**

The `(scheme time)` library provides access to time-related values.

```scheme
current-jiffy           current-second
jiffies-per-second
```

**Write Library**

The `(scheme write)` library provides procedures for writing
Scheme objects.

```scheme
display                 write
write-shared            write-simple
```

**R5RS Library**

The `(scheme r5rs)` library provides the identifiers defined by
R⁵RS, except that
`transcript-on` and `transcript-off` are not present.
Note that
the `exact` and `inexact` procedures appear under their R⁵RS names
`inexact->exact` and `exact->inexact` respectively.
However, if an implementation does not provide a particular library such as the
complex library, the corresponding identifiers will not appear in this
library either.

```scheme
*                       +
-                       ...
/                       <
<=                      =
=>                      >
>=                      _
abs                     acos
and                     angle
append                  apply
asin                    assoc
assq                    assv
atan                    begin
boolean?                caaaar
caaadr                  caaar
caadar                  caaddr
caadr                   caar
cadaar                  cadadr
cadar                   caddar
cadddr                  caddr
cadr
call-with-current-continuation
call-with-input-file    call-with-output-file
call-with-values        car
case                    cdaaar
cdaadr                  cdaar
cdadar                  cdaddr
cdadr                   cdar
cddaar                  cddadr
cddar                   cdddar
cddddr                  cdddr
cddr                    cdr
ceiling                 char->integer
char-alphabetic?        char-ci<=?
char-ci<?               char-ci=?
char-ci>=?              char-ci>?
char-downcase           char-lower-case?
char-numeric?           char-ready?
char-upcase             char-upper-case?
char-whitespace?        char<=?
char<?                  char=?
char>=?                 char>?
char?                   close-input-port
close-output-port       complex?
cond                    cons
cos                     current-input-port
current-output-port     define
define-syntax           delay
denominator             display
do                      dynamic-wind
else                    eof-object?
eq?                     equal?
eqv?                    eval
even?                   exact->inexact
exact?                  exp
expt                    floor
for-each                force
gcd                     if
imag-part               inexact->exact
inexact?                input-port?
integer->char           integer?
interaction-environment lambda
lcm                     length
let                     let*
let-syntax              letrec
letrec-syntax           list
list->string            list->vector
list-ref                list-tail
list?                   load
log                     magnitude
make-polar              make-rectangular
make-string             make-vector
map                     max
member                  memq
memv                    min
modulo                  negative?
newline                 not
null-environment        null?
number->string          number?
numerator               odd?
open-input-file         open-output-file
or                      output-port?
pair?                   peek-char
positive?               procedure?
quasiquote              quote
quotient                rational?
rationalize             read
read-char               real-part
real?                   remainder
reverse                 round
scheme-report-environment
set!                    set-car!
set-cdr!                sin
sqrt                    string
string->list            string->number
string->symbol          string-append
string-ci<=?            string-ci<?
string-ci=?             string-ci>=?
string-ci>?             string-copy
string-fill!            string-length
string-ref              string-set!
string<=?               string<?
string=?                string>=?
string>?                string?
substring               symbol->string
symbol?                 syntax-rules
tan                     truncate
values                  vector
vector->list            vector-fill!
vector-length           vector-ref
vector-set!             vector?
with-input-from-file    with-output-to-file
write                   write-char
zero?
```


# Standard Feature Identifiers

<a id="stdfeatures"></a>

An implementation may provide any or all of the feature identifiers
listed below for use by `cond-expand` and `features`,
but must not provide a feature identifier if it does not
provide the corresponding feature.

<a id="standard-features"></a>

r7rsAll R⁷RS Scheme implementations have this feature.
exact-closedThe algebraic operations
 `+`, `-`, `*`, and `expt` where the second argument
 is a non-negative integer produce
 exact values given exact inputs.
exact-complexExact complex numbers are provided.
ieee-floatInexact numbers are IEEE 754 binary floating point
 values.
full-unicodeAll Unicode characters present in Unicode version 6.0 are supported as Scheme characters.
ratios`/` with exact arguments produces an exact result
 when the divisor is nonzero.
posixThis implementation is running on a POSIX
 system.
windowsThis implementation is running on Windows.
unix, darwin, gnu-linux, bsd, freebsd, solaris, ...Operating
 system flags (perhaps more than one).
i386, x86-64, ppc, sparc, jvm, clr, llvm, ...CPU architecture flags.
ilp32, lp64, ilp64, ...C memory model flags.
big-endian, little-endianByte order flags.
⟨name⟩The name of this implementation.
⟨name-version⟩The name and version of this
 implementation.


# Language changes

## Incompatibilities with R⁵RS

<a id="incompatibilities"></a>

This section enumerates the incompatibilities between this report and
the “Revised$^5$ report” [[R5RS](#cite-r5rs)].

*This list is not authoritative, but is believed to be correct and complete.*

- Case sensitivity is now the default in symbols and character names.
  This means that code written under the assumption that symbols could be
  written `FOO` or `Foo` in some contexts and `foo` in other contexts
  can either be changed, be marked with the new `#!fold-case` directive,
  or be included in a library using the `include-ci` library declaration.
  All standard identifiers are entirely in lower case.
- The `syntax-rules` construct now recognizes *_* (underscore)
  as a wildcard, which means it cannot be used as a syntax variable.
  It can still be used as a literal.
- The R⁵RS procedures `exact->inexact` and `inexact->exact`
  have been renamed to their R⁶RS names, `inexact` and `exact`,
  respectively, as these names are shorter and more correct.
  The former names are still available in the R⁵RS library.
- The guarantee that string comparison (with `string<?` and the
  related predicates) is a lexicographical extension of character comparison
  (with `char<?` and the related predicates) has been removed.
- Support for the # character in numeric literals is no longer required.
- Support for the letters `s`, `f`, `d`, and `l`
  as exponent markers is no longer required.
- Implementations of `string->number` are no longer permitted
  to return `#f` when the argument contains an explicit radix prefix,
  and must be compatible with `read` and the syntax of numbers in programs.
- The procedures `transcript-on` and `transcript-off` have been removed.

## Other language changes since R⁵RS

<a id="differences"></a>
This section enumerates the additional differences between this report and
the “Revised$^5$ report” [[R5RS](#cite-r5rs)].

*This list is not authoritative, but is believed to be correct and complete.*

- Various minor ambiguities and unclarities in R⁵RS have been cleaned up.
- Libraries have been added as a new program structure to improve
  encapsulation and sharing of code. Some existing and new identifiers
  have been factored out into separate libraries.
  Libraries can be imported into other libraries or main programs, with
  controlled exposure and renaming of identifiers.
  The contents of a library can be made conditional on the features of
  the implementation on which it is to be used.
  There is an R⁵RS compatibility library.
- The expressions types `include`, `include-ci`, and `cond-expand`
  have been added to the base library; they have the same semantics as the
  corresponding library declarations.
- Exceptions can now be signaled explicitly with `raise`,
  `raise-continuable` or `error`, and can be handled with `with-exception-handler` and the `guard` syntax.
  Any object can specify an error condition; the implementation-defined
  conditions signaled by `error` have a predicate to detect them and accessor functions to
  retrieve the arguments passed to `error`.
  Conditions signaled by `read` and by file-related procedures
  also have predicates to detect them.
- New disjoint types supporting access to multiple fields can be
  generated with the `define-record-type` of SRFI 9 [[srfi9](#cite-srfi9)]
- Parameter objects can be created with `make-parameter`, and
  dynamically rebound with `parameterize`.
  The procedures `current-input-port` and `current-output-port` are now
  parameter objects, as is the newly introduced `current-error-port`.
- Support for promises has been enhanced based on SRFI 45 [[srfi45](#cite-srfi45)].
- *Bytevectors*, vectors of exact integers in the range
  from 0 to 255 inclusive, have been added as a new disjoint type.
  A subset of the vector procedures is provided. Bytevectors
  can be converted to and from strings in accordance with the UTF-8 character encoding.
  Bytevectors have a datum representation and evaluate to themselves.
- Vector constants evaluate to themselves.
- The procedure `read-line` is provided to make line-oriented textual input
  simpler.
- The procedure `flush-output-port` is provided to allow minimal
  control of output port buffering.
- *Ports* can now be designated as *textual* or *binary* ports, with new procedures for reading and writing binary
  data.
  The new predicates `input-port-open?` and `output-port-open?` return whether a port is open or closed.
  The new procedure `close-port` now closes a port; if the port
  has both input and output sides, both are closed.
- *String ports* have been added as a way to read and write
  characters to and from strings, and *bytevector ports* to read
  and write bytes to and from bytevectors.
- There are now I/O procedures specific to strings and bytevectors.
- The `write` procedure now generates datum labels when applied to
  circular objects. The new procedure `write-simple` never generates
  labels; `write-shared` generates labels for all shared and circular
  structure.
  The `display` procedure must not loop on circular objects.
- The R⁶RS procedure `eof-object` has been added.
  Eof-objects are now required to be a disjoint type.
- Syntax definitions are now allowed wherever variable definitions are.
- The `syntax-rules` construct now allows
  the ellipsis symbol to be specified explicitly instead of the default
  `...`, allows template escapes with an ellipsis-prefixed list, and
  allows tail patterns to follow an ellipsis pattern.
- The `syntax-error` syntax has been added as a way to signal immediate
  and more informative errors when a macro is expanded.
- The `letrec*` binding construct has been added, and internal `define`
  is specified in terms of it.
- Support for capturing multiple values has been enhanced with `define-values`, `let-values`, and `let*-values`.
  Standard expression types which contain a sequence of expressions now
  permit passing zero or more than one value to the continuations of all
  non-final expressions of the sequence.
- The `case` conditional now supports `=>` syntax
  analogous to `cond` not only in regular clauses but in the `else` clause as well.
- To support dispatching on the number of arguments passed to a
  procedure, `case-lambda` has been added in its own library.
- The convenience conditionals `when` and `unless` have been added.
- The behavior of `eqv?` on inexact numbers now conforms to the
  R⁶RS definition.
- When applied to procedures, `eq?` and `eqv?` are permitted to
  return different answers.
- The R⁶RS procedures `boolean=?` and `symbol=?` have been added.
- Positive infinity, negative infinity, NaN, and negative inexact zero have been added
  to the numeric tower as inexact values with the written
  representations `+inf.0`, `-inf.0`, `+nan.0`, and `-0.0`
  respectively. Support for them is not required.
  The representation `-nan.0` is synonymous with `+nan.0`.
- The `log` procedure now accepts a second argument specifying
  the logarithm base.
- The procedures `map` and `for-each` are now required to terminate on
  the shortest argument list.
- The procedures `member` and `assoc` now take an optional third argument
  specifying the equality predicate to be used.
- The numeric procedures `finite?`, `infinite?`, `nan?`,
  `exact-integer?`, `square`, and `exact-integer-sqrt`
  have been added.
- The `-` and `/` procedures
  and the character and string comparison
  predicates are now required to support more than two arguments.
- The forms `#true` and `#false` are now supported
  as well as `#t` and `#f`.
- The procedures `make-list`, `list-copy`, `list-set!`,
  `string-map`, `string-for-each`, `string->vector`,
  `vector-append`,
  `vector-copy`, `vector-map`, `vector-for-each`,
  `vector->string`, `vector-copy!`, and `string-copy!`
  have been added to round out the sequence operations.
- Some string and vector procedures support processing of part of a string or vector using
  optional *start* and *end* arguments.
- Some list procedures are now defined on circular lists.
- Implementations may provide any subset of the full Unicode
  repertoire that includes ASCII, but implementations must support any
  such subset in a way consistent with Unicode.
  Various character and string procedures have been extended accordingly,
  and case conversion procedures added for strings.
  String comparison is no longer
  required to be consistent with character comparison, which is based
  solely on Unicode scalar values.
  The new `digit-value` procedure has been added to obtain the numerical
  value of a numeric character.
- There are now two additional comment syntaxes: `#;` to
  skip the next datum, and `#| ... |#`
  for nestable block comments.
- Data prefixed with datum labels `#<n>=` can be referenced
  with `#<n>#`, allowing for reading and writing of data with
  shared structure.
- Strings and symbols now allow mnemonic and numeric escape
  sequences, and the list of named characters has been extended.
- The procedures `file-exists?` and `delete-file` are available in the
  `(scheme file)` library.
- An interface to the system environment, command line, and process exit status is
  available in the `(scheme process-context)` library.
- Procedures for accessing time-related values are available in the
  `(scheme time)` library.
- A less irregular set of integer division operators is provided
  with new and clearer names.
- The `load` procedure now accepts a second argument specifying the environment to
  load into.
- The `call-with-current-continuation` procedure now has the synonym
  `call/cc`.
- The semantics of read-eval-print loops are now partly prescribed,
  requiring the redefinition of procedures, but not syntax keywords, to have retroactive effect.
- The formal semantics now handles `dynamic-wind`.

## Incompatibilities with R⁶RS

This section enumerates the incompatibilities between R⁷RS and
the “Revised$^6$ report” [[R6RS](#cite-r6rs)] and its accompanying Standard Libraries document.

*This list is not authoritative, and is possibly incomplete.*

- R⁷RS libraries begin with the keyword `define-library`
  rather than `library` in order to make them syntactically
  distinguishable from R⁶RS libraries.
  In R⁷RS terms, the body of an R⁶RS library consists
  of a single export declaration followed by a single import declaration,
  followed by commands and definitions. In R⁷RS, commands and
  definitions are not permitted directly within the body: they have to be wrapped in a `begin`
  library declaration.
- There is no direct R⁶RS equivalent of the `include`, `include-ci`,
  `include-library-declarations`, or `cond-expand` library declarations.
  On the other hand, the R⁷RS library syntax does not support phase or version specifications.
- The grouping of standardized identifiers into libraries is different from the R⁶RS
  approach. In particular, procedures which are optional in R⁵RS either expressly
  or by implication, have been removed from the base library.
  Only the base library itself is an absolute requirement.
- No form of identifier syntax is provided.
- Internal syntax definitions are allowed, but uses of a syntax form
  cannot appear before its definition; the `even`/`odd` example given in
  R⁶RS is not allowed.
- The R⁶RS exception system was incorporated as-is, but the condition
  types have been left unspecified. In particular, where R⁶RS requires
  a condition of a specified type to be signaled, R⁷RS says only
  “it is an error”, leaving the question of signaling open.
- Full Unicode support is not required.
  Normalization is not provided.
  Character comparisons are
  defined by Unicode, but string comparisons are implementation-dependent.
  Non-Unicode characters are permitted.
- The full numeric tower is optional as in R⁵RS, but optional support for IEEE
  infinities, NaN, and -0.0 was adopted from R⁶RS. Most clarifications on
  numeric results were also adopted, but the semantics of the R⁶RS procedures `real?`,
  `rational?`, and `integer`? were not adopted.
  (Note that the R⁵RS/R⁷RS semantics are available in R⁶RS using
  `real-valued?`, `rational-valued?`, and `integer-valued?`).
  The R⁶RS division operators `div`, `mod`, `div-and-mod`, `div0`, `mod0` and `div0-and-mod0` are not provided.
- When a result is unspecified, it is still required to be a single value.
  However, non-final expressions
  in a body can return any number of values.
- The semantics of `map` and `for-each` have been changed to use
  the SRFI 1 [[srfi1](#cite-srfi1)] early termination behavior. Likewise,
  `assoc` and `member` take an optional `equal?` argument as in SRFI 1,
  instead of the separate `assp` and `memp` procedures of R⁶RS.
- The R⁶RS `quasiquote` clarifications have been adopted, with the
  exception of multiple-argument `unquote` and
  `unquote-splicing`.
- The R⁶RS method of specifying mantissa widths was not adopted.
- String ports are compatible with SRFI 6 [[srfi6](#cite-srfi6)] rather than R⁶RS.
- R⁶RS-style bytevectors are included, but
  only the unsigned byte (`u8`) procedures have been provided.
  The lexical syntax uses `#u8` for compatibility
  with SRFI 4 [[srfi4](#cite-srfi4)], rather than the R⁶RS `#vu8` style.
- The utility macros `when` and `unless` are provided, but
  their result is left unspecified.
- The remaining features of the Standard Libraries document were
  left to future standardization efforts.


# Additional material

The Scheme community website at
`http://schemers.org`
contains additional resources for learning and programming, job and
event postings, and Scheme user group information.

A bibliography of Scheme-related research at
`http://library.readscheme.org`
links to technical papers and theses related to the Scheme language,
including both classic papers and recent research.

On-line Scheme discussions are held using IRC
on the `#scheme` channel at `irc.freenode.net`
and on the Usenet discussion group `comp.lang.scheme`.


# Example

The procedure `integrate-system` integrates the system

$$
y_k^\prime = f_k(y_1, y_2, \dots, y_n), \; k = 1, \dots, n
$$

of differential equations with the method of Runge-Kutta.

The parameter `system-derivative` is a function that takes a system
state (a vector of values for the state variables $y_1, \dots, y_n$)
and produces a system derivative (the values $y_1^\prime, \dots, y_n^\prime$). The parameter `initial-state` provides an initial
system state, and `h` is an initial guess for the length of the
integration step.

The value returned by `integrate-system` is an infinite stream of
system states.

```scheme
(define (integrate-system system-derivative
                          initial-state
                          h)
  (let ((next (runge-kutta-4 system-derivative h)))
    (letrec ((states
              (cons initial-state
                    (delay (map-streams next
                                        states)))))
      states)))
```

The procedure `runge-kutta-4` takes a function, `f`, that produces a
system derivative from a system state. It
produces a function that takes a system state and
produces a new system state.

```scheme
(define (runge-kutta-4 f h)
  (let ((*h (scale-vector h))
        (*2 (scale-vector 2))
        (*1/2 (scale-vector (/ 1 2)))
        (*1/6 (scale-vector (/ 1 6))))
    (lambda (y)
      ;; y is a system state
      (let* ((k0 (*h (f y)))
             (k1 (*h (f (add-vectors y (*1/2 k0)))))
             (k2 (*h (f (add-vectors y (*1/2 k1)))))
             (k3 (*h (f (add-vectors y k2)))))
        (add-vectors y
          (*1/6 (add-vectors k0
                             (*2 k1)
                             (*2 k2)
                             k3)))))))

(define (elementwise f)
  (lambda vectors
    (generate-vector
     (vector-length (car vectors))
     (lambda (i)
       (apply f
              (map (lambda (v) (vector-ref  v i))
                   vectors))))))

(define (generate-vector size proc)
  (let ((ans (make-vector size)))
    (letrec ((loop
              (lambda (i)
                (cond ((= i size) ans)
                      (else
                       (vector-set! ans i (proc i))
                       (loop (+ i 1)))))))
      (loop 0))))

(define add-vectors (elementwise +))

(define (scale-vector s)
  (elementwise (lambda (x) (* x s))))
```

The `map-streams` procedure is analogous to `map`: it applies its first
argument (a procedure) to all the elements of its second argument (a
stream).

```scheme
(define (map-streams f s)
  (cons (f (head s))
        (delay (map-streams f (tail s)))))
```

Infinite streams are implemented as pairs whose car holds the first
element of the stream and whose cdr holds a promise to deliver the rest
of the stream.

```scheme
(define head car)
(define (tail stream)
  (force (cdr stream)))
```

The following illustrates the use of `integrate-system` in
integrating the system

$$
C {dv_C \over dt} = -i_L - {v_C \over R}
$$

$$
L {di_L \over dt} = v_C
$$

which models a damped oscillator.

```scheme
(define (damped-oscillator R L C)
  (lambda (state)
    (let ((Vc (vector-ref state 0))
          (Il (vector-ref state 1)))
      (vector (- 0 (+ (/ Vc (* R C)) (/ Il C)))
              (/ Vc L)))))

(define the-states
  (integrate-system
     (damped-oscillator 10000 1000 .001)
     '#(1 0)
     .01))
```


# References

<a id="cite-sicp"></a>
**[SICP]** Harold Abelson and Gerald Jay Sussman with Julie Sussman. *Structure and Interpretation of Computer Programs, second edition.* MIT Press, Cambridge, 1996.

<a id="cite-bawden88"></a>
**[Bawden88]** Alan Bawden and Jonathan Rees. Syntactic closures. In *Proceedings of the 1988 ACM Symposium on Lisp and Functional Programming*, pages 86–95.

<a id="cite-rfc2119"></a>
**[rfc2119]** S. Bradner. Key words for use in RFCs to Indicate Requirement Levels. <http://www.ietf.org/rfc/rfc2119.txt>, 1997.

<a id="cite-howtoprint"></a>
**[howtoprint]** Robert G. Burger and R. Kent Dybvig. Printing floating-point numbers quickly and accurately. In *Proceedings of the ACM SIGPLAN '96 Conference on Programming Language Design and Implementation*, pages 108–116.

<a id="cite-howtoread"></a>
**[howtoread]** William Clinger. How to read floating point numbers accurately. In *Proceedings of the ACM SIGPLAN '90 Conference on Programming Language Design and Implementation*, pages 92–101. Proceedings published as *SIGPLAN Notices* 25(6), June 1990.

<a id="cite-propertailrecursion"></a>
**[propertailrecursion]** William Clinger. Proper Tail Recursion and Space Efficiency. In *Proceedings of the 1998 ACM Conference on Programming Language Design and Implementation*, June 1998.

<a id="cite-srfi6"></a>
**[srfi6]** William Clinger. SRFI 6: Basic String Ports. <http://srfi.schemers.org/srfi-6/>, 1999.

<a id="cite-rrrs"></a>
**[RRRS]** William Clinger, editor. The revised revised report on Scheme, or an uncommon Lisp. MIT Artificial Intelligence Memo 848, August 1985. Also published as Computer Science Department Technical Report 174, Indiana University, June 1985.

<a id="cite-macrosthatwork"></a>
**[macrosthatwork]** William Clinger and Jonathan Rees. Macros that work. In *Proceedings of the 1991 ACM Conference on Principles of Programming Languages*, pages 155–162.

<a id="cite-r4rs"></a>
**[R4RS]** William Clinger and Jonathan Rees, editors. The revised$^4$ report on the algorithmic language Scheme. In *ACM Lisp Pointers* 4(3), pages 1–55, 1991.

<a id="cite-uax44"></a>
**[uax44]** Mark Davis. Unicode Standard Annex #44, Unicode Character Database. <http://unicode.org/reports/tr44/>, 2010.

<a id="cite-syntacticabstraction"></a>
**[syntacticabstraction]** R. Kent Dybvig, Robert Hieb, and Carl Bruggeman. Syntactic abstraction in Scheme. *Lisp and Symbolic Computation* 5(4):295–326, 1993.

<a id="cite-srfi4"></a>
**[srfi4]** Marc Feeley. SRFI 4: Homogeneous Numeric Vector Datatypes. <http://srfi.schemers.org/srfi-4/>, 1999.

<a id="cite-scheme311"></a>
**[Scheme311]** Carol Fessenden, William Clinger, Daniel P. Friedman, and Christopher Haynes. Scheme 311 version 4 reference manual. Indiana University Computer Science Technical Report 137, February 1983. Superseded by [[Scheme84](#cite-scheme84)].

<a id="cite-scheme84"></a>
**[Scheme84]** D. Friedman, C. Haynes, E. Kohlbecker, and M. Wand. Scheme 84 interim reference manual. Indiana University Computer Science Technical Report 153, January 1985.

<a id="cite-life"></a>
**[life]** Martin Gardner. Mathematical Games: The fantastic combinations of John Conway's new solitaire game “Life.” In *Scientific American*, 223:120–123, October 1970.

<a id="cite-ieee"></a>
**[IEEE]** *IEEE Standard 754-2008. IEEE Standard for Floating-Point Arithmetic.* IEEE, New York, 2008.

<a id="cite-ieeescheme"></a>
**[IEEEScheme]** *IEEE Standard 1178-1990. IEEE Standard for the Scheme Programming Language.* IEEE, New York, 1991.

<a id="cite-srfi9"></a>
**[srfi9]** Richard Kelsey. SRFI 9: Defining Record Types. <http://srfi.schemers.org/srfi-9/>, 1999.

<a id="cite-r5rs"></a>
**[R5RS]** Richard Kelsey, William Clinger, and Jonathan Rees, editors. The revised$^5$ report on the algorithmic language Scheme. *Higher-Order and Symbolic Computation*, 11(1):7-105, 1998.

<a id="cite-kohlbecker86"></a>
**[Kohlbecker86]** Eugene E. Kohlbecker Jr. *Syntactic Extensions in the Programming Language Lisp.* PhD thesis, Indiana University, August 1986.

<a id="cite-hygienic"></a>
**[hygienic]** Eugene E. Kohlbecker Jr., Daniel P. Friedman, Matthias Felleisen, and Bruce Duba. Hygienic macro expansion. In *Proceedings of the 1986 ACM Conference on Lisp and Functional Programming*, pages 151–161.

<a id="cite-mccarthy"></a>
**[McCarthy]** John McCarthy. Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I. *Communications of the ACM* 3(4):184–195, April 1960.

<a id="cite-mitscheme"></a>
**[MITScheme]** MIT Department of Electrical Engineering and Computer Science. Scheme manual, seventh edition. September 1984.

<a id="cite-naur63"></a>
**[Naur63]** Peter Naur et al. Revised report on the algorithmic language Algol 60. *Communications of the ACM* 6(1):1–17, January 1963.

<a id="cite-penfield81"></a>
**[Penfield81]** Paul Penfield, Jr. Principal values and branch cuts in complex APL. In *APL '81 Conference Proceedings,* pages 248–256. ACM SIGAPL, San Francisco, September 1981. Proceedings published as *APL Quote Quad* 12(1), ACM, September 1981.

<a id="cite-rees82"></a>
**[Rees82]** Jonathan A. Rees and Norman I. Adams IV. T: A dialect of Lisp or, lambda: The ultimate software tool. In *Conference Record of the 1982 ACM Symposium on Lisp and Functional Programming*, pages 114–122.

<a id="cite-rees84"></a>
**[Rees84]** Jonathan A. Rees, Norman I. Adams IV, and James R. Meehan. The T manual, fourth edition. Yale University Computer Science Department, January 1984.

<a id="cite-r3rs"></a>
**[R3RS]** Jonathan Rees and William Clinger, editors. The revised$^3$ report on the algorithmic language Scheme. In *ACM SIGPLAN Notices* 21(12), pages 37–79, December 1986.

<a id="cite-srfi1"></a>
**[srfi1]** Olin Shivers. SRFI 1: List Library. <http://srfi.schemers.org/srfi-1/>, 1999.

<a id="cite-scheme78"></a>
**[Scheme78]** Guy Lewis Steele Jr. and Gerald Jay Sussman. The revised report on Scheme, a dialect of Lisp. MIT Artificial Intelligence Memo 452, January 1978.

<a id="cite-rabbit"></a>
**[Rabbit]** Guy Lewis Steele Jr. Rabbit: a compiler for Scheme. MIT Artificial Intelligence Laboratory Technical Report 474, May 1978.

<a id="cite-r6rs"></a>
**[R6RS]** Michael Sperber, R. Kent Dybvig, Mathew Flatt, and Anton van Straaten, editors. *The revised$^6$ report on the algorithmic language Scheme.* Cambridge University Press, 2010.

<a id="cite-cltl"></a>
**[CLtL]** Guy Lewis Steele Jr. *Common Lisp: The Language, second edition.* Digital Press, Burlington MA, 1990.

<a id="cite-scheme75"></a>
**[Scheme75]** Gerald Jay Sussman and Guy Lewis Steele Jr. Scheme: an interpreter for extended lambda calculus. MIT Artificial Intelligence Memo 349, December 1975.

<a id="cite-stoy77"></a>
**[Stoy77]** Joseph E. Stoy. *Denotational Semantics: The Scott-Strachey Approach to Programming Language Theory.* MIT Press, Cambridge, 1977.

<a id="cite-timanual85"></a>
**[TImanual85]** Texas Instruments, Inc. TI Scheme Language Reference Manual. Preliminary version 1.0, November 1985.

<a id="cite-srfi45"></a>
**[srfi45]** Andre van Tonder. SRFI 45: Primitives for Expressing Iterative Lazy Algorithms. <http://srfi.schemers.org/srfi-45/>, 2002.

<a id="cite-gasbichlerknauelsperberkelsey2003"></a>
**[GasbichlerKnauelSperberKelsey2003]** Martin Gasbichler, Eric Knauel, Michael Sperber and Richard Kelsey. How to Add Threads to a Sequential Language Without Getting Tangled Up. *Proceedings of the Fourth Workshop on Scheme and Functional Programming*, November 2003.

<a id="cite-tai"></a>
**[TAI]** International Earth Rotation Service. Historical table of TAI-UTC offsets. <http://maia.usno.navy.mil/ser7/tai-utc.dat>


## Alphabetic index of procedures and keywords

- [`'`](#x-2)
- [`*`](#x-14)
- [`+`](#x-13)
- [`,`](#x-4)
- [`,@`](#x-5)
- [`-`](#x-15)
- [`/`](#x-16)
- [`;`](#x)
- [`<`](#x-9)
- [`<=`](#x-11)
- [`=`](#x-8)
- [`=>`](#x-3)
- [`>`](#x-10)
- [`>=`](#x-12)
- [`_`](#x-7)
- [```](#x-6)
- [`abs`](#abs)
- [`acos`](#acos)
- [`and`](#and)
- [`angle`](#angle)
- [`append`](#append)
- [`apply`](#apply)
- [`asin`](#asin)
- [`assoc`](#assoc)
- [`assq`](#assq)
- [`assv`](#assv)
- [`atan`](#atan)
- [`begin`](#begin)
- [`binary-port?`](#binary-port)
- [`boolean=?`](#boolean-2)
- [`boolean?`](#boolean)
- [`bytevector`](#bytevector-2)
- [`bytevector-append`](#bytevector-append)
- [`bytevector-copy`](#bytevector-copy)
- [`bytevector-copy!`](#bytevector-copy-2)
- [`bytevector-length`](#bytevector-length)
- [`bytevector-u8-ref`](#bytevector-u8-ref)
- [`bytevector-u8-set!`](#bytevector-u8-set)
- [`bytevector?`](#bytevector)
- [`caaaar`](#caaaar)
- [`caaadr`](#caaadr)
- [`caaar`](#caaar)
- [`caadar`](#caadar)
- [`caaddr`](#caaddr)
- [`caadr`](#caadr)
- [`caar`](#caar)
- [`cadaar`](#cadaar)
- [`cadadr`](#cadadr)
- [`cadar`](#cadar)
- [`caddar`](#caddar)
- [`cadddr`](#cadddr)
- [`caddr`](#caddr)
- [`cadr`](#cadr)
- [`call-with-current-continuation`](#call-with-current-continuation)
- [`call-with-input-file`](#call-with-input-file)
- [`call-with-output-file`](#call-with-output-file)
- [`call-with-port`](#call-with-port)
- [`call-with-values`](#call-with-values)
- [`call/cc`](#call-cc)
- [`car`](#car)
- [`case`](#case)
- [`case-lambda`](#case-lambda)
- [`cdaaar`](#cdaaar)
- [`cdaadr`](#cdaadr)
- [`cdaar`](#cdaar)
- [`cdadar`](#cdadar)
- [`cdaddr`](#cdaddr)
- [`cdadr`](#cdadr)
- [`cdar`](#cdar)
- [`cddaar`](#cddaar)
- [`cddadr`](#cddadr)
- [`cddar`](#cddar)
- [`cdddar`](#cdddar)
- [`cddddr`](#cddddr)
- [`cdddr`](#cdddr)
- [`cddr`](#cddr)
- [`cdr`](#cdr)
- [`ceiling`](#ceiling)
- [`char->integer`](#char-integer)
- [`char-alphabetic?`](#char-alphabetic)
- [`char-ci<=?`](#char-ci-4)
- [`char-ci<?`](#char-ci-2)
- [`char-ci=?`](#char-ci)
- [`char-ci>=?`](#char-ci-5)
- [`char-ci>?`](#char-ci-3)
- [`char-downcase`](#char-downcase)
- [`char-foldcase`](#char-foldcase)
- [`char-lower-case?`](#char-lower-case)
- [`char-numeric?`](#char-numeric)
- [`char-ready?`](#char-ready)
- [`char-upcase`](#char-upcase)
- [`char-upper-case?`](#char-upper-case)
- [`char-whitespace?`](#char-whitespace)
- [`char<=?`](#char-5)
- [`char<?`](#char-3)
- [`char=?`](#char-2)
- [`char>=?`](#char-6)
- [`char>?`](#char-4)
- [`char?`](#char)
- [`close-input-port`](#close-input-port)
- [`close-output-port`](#close-output-port)
- [`close-port`](#close-port)
- [`command-line`](#command-line)
- [`complex?`](#complex)
- [`cond`](#cond)
- [`cond-expand`](#cond-expand)
- [`cons`](#cons)
- [`cos`](#cos)
- [`current-error-port`](#current-error-port)
- [`current-input-port`](#current-input-port)
- [`current-jiffy`](#current-jiffy)
- [`current-output-port`](#current-output-port)
- [`current-second`](#current-second)
- [`define`](#define)
- [`define-library`](#define-library)
- [`define-record-type`](#define-record-type)
- [`define-syntax`](#define-syntax)
- [`define-values`](#define-values)
- [`delay`](#delay)
- [`delay-force`](#delay-force)
- [`delete-file`](#delete-file)
- [`denominator`](#denominator)
- [`digit-value`](#digit-value)
- [`display`](#display)
- [`do`](#do)
- [`dynamic-wind`](#dynamic-wind)
- [`else`](#else)
- [`emergency-exit`](#emergency-exit)
- [`environment`](#environment)
- [`eof-object`](#eof-object-2)
- [`eof-object?`](#eof-object)
- [`eq?`](#eq)
- [`equal?`](#equal)
- [`eqv?`](#eqv)
- [`error-object-irritants`](#error-object-irritants)
- [`error-object-message`](#error-object-message)
- [`error-object?`](#error-object)
- [`eval`](#eval)
- [`even?`](#even)
- [`exact`](#exact-2)
- [`exact-integer-sqrt`](#exact-integer-sqrt)
- [`exact-integer?`](#exact-integer)
- [`exact?`](#exact)
- [`exit`](#exit)
- [`exp`](#exp)
- [`expt`](#expt)
- [`features`](#features)
- [`file-error?`](#file-error)
- [`file-exists?`](#file-exists)
- [`finite?`](#finite)
- [`floor`](#floor-2)
- [`floor-quotient`](#floor-quotient)
- [`floor-remainder`](#floor-remainder)
- [`floor/`](#floor)
- [`flush-output-port`](#flush-output-port)
- [`for-each`](#for-each)
- [`force`](#force)
- [`gcd`](#gcd)
- [`get-environment-variable`](#get-environment-variable)
- [`get-environment-variables`](#get-environment-variables)
- [`get-output-bytevector`](#get-output-bytevector)
- [`get-output-string`](#get-output-string)
- [`guard`](#guard)
- [`if`](#if)
- [`imag-part`](#imag-part)
- [`import`](#import)
- [`include`](#include)
- [`inexact`](#inexact-2)
- [`inexact?`](#inexact)
- [`infinite?`](#infinite)
- [`input-port-open?`](#input-port-open)
- [`input-port?`](#input-port)
- [`integer->char`](#integer-char)
- [`integer?`](#integer)
- [`interaction-environment`](#interaction-environment)
- [`jiffies-per-second`](#jiffies-per-second)
- [`lambda`](#lambda)
- [`lcm`](#lcm)
- [`length`](#length)
- [`let`](#let)
- [`let*`](#let-2)
- [`let*-values`](#let-values-2)
- [`let-syntax`](#let-syntax)
- [`let-values`](#let-values)
- [`letrec`](#letrec)
- [`letrec*`](#letrec-2)
- [`letrec-syntax`](#letrec-syntax)
- [`list`](#list-2)
- [`list->string`](#list-string)
- [`list->vector`](#list-vector)
- [`list-copy`](#list-copy)
- [`list-ref`](#list-ref)
- [`list-set!`](#list-set)
- [`list-tail`](#list-tail)
- [`list?`](#list)
- [`load`](#load)
- [`log`](#log)
- [`magnitude`](#magnitude)
- [`make-bytevector`](#make-bytevector)
- [`make-list`](#make-list)
- [`make-parameter`](#make-parameter)
- [`make-polar`](#make-polar)
- [`make-promise`](#make-promise)
- [`make-rectangular`](#make-rectangular)
- [`make-string`](#make-string)
- [`make-vector`](#make-vector)
- [`map`](#map)
- [`max`](#max)
- [`member`](#member)
- [`memq`](#memq)
- [`memv`](#memv)
- [`min`](#min)
- [`modulo`](#modulo)
- [`nan?`](#nan)
- [`negative?`](#negative)
- [`newline`](#newline)
- [`not`](#not)
- [`null-environment`](#null-environment)
- [`null?`](#null)
- [`number->string`](#number-string)
- [`number?`](#number)
- [`numerator`](#numerator)
- [`odd?`](#odd)
- [`open-binary-input-file`](#open-binary-input-file)
- [`open-binary-output-file`](#open-binary-output-file)
- [`open-input-bytevector`](#open-input-bytevector)
- [`open-input-file`](#open-input-file)
- [`open-input-string`](#open-input-string)
- [`open-output-bytevector`](#open-output-bytevector)
- [`open-output-file`](#open-output-file)
- [`open-output-string`](#open-output-string)
- [`or`](#or)
- [`output-port-open?`](#output-port-open)
- [`output-port?`](#output-port)
- [`pair?`](#pair)
- [`parameterize`](#parameterize)
- [`peek-char`](#peek-char)
- [`peek-u8`](#peek-u8)
- [`port?`](#port-2)
- [`positive?`](#positive)
- [`procedure?`](#procedure-2)
- [`promise?`](#promise)
- [`quasiquote`](#quasiquote)
- [`quote`](#quote)
- [`quotient`](#quotient)
- [`raise`](#raise)
- [`raise-continuable`](#raise-continuable)
- [`rational?`](#rational)
- [`rationalize`](#rationalize)
- [`read`](#read)
- [`read-bytevector`](#read-bytevector)
- [`read-bytevector!`](#read-bytevector-2)
- [`read-char`](#read-char)
- [`read-error?`](#read-error)
- [`read-line`](#read-line)
- [`read-string`](#read-string)
- [`read-u8`](#read-u8)
- [`real-part`](#real-part)
- [`real?`](#real)
- [`remainder`](#remainder)
- [`reverse`](#reverse)
- [`round`](#round)
- [`scheme-report-environment`](#scheme-report-environment)
- [`set!`](#set)
- [`set-car!`](#set-car)
- [`set-cdr!`](#set-cdr)
- [`sin`](#sin)
- [`sqrt`](#sqrt)
- [`square`](#square)
- [`string`](#string-2)
- [`string->list`](#string-list)
- [`string->number`](#string-number)
- [`string->symbol`](#string-symbol)
- [`string->utf8`](#string-utf8)
- [`string->vector`](#string-vector)
- [`string-append`](#string-append)
- [`string-ci<=?`](#string-ci-4)
- [`string-ci<?`](#string-ci-2)
- [`string-ci=?`](#string-ci)
- [`string-ci>=?`](#string-ci-5)
- [`string-ci>?`](#string-ci-3)
- [`string-copy`](#string-copy)
- [`string-copy!`](#string-copy-2)
- [`string-downcase`](#string-downcase)
- [`string-fill!`](#string-fill)
- [`string-foldcase`](#string-foldcase)
- [`string-for-each`](#string-for-each)
- [`string-length`](#string-length)
- [`string-map`](#string-map)
- [`string-ref`](#string-ref)
- [`string-set!`](#string-set)
- [`string-upcase`](#string-upcase)
- [`string<=?`](#string-6)
- [`string<?`](#string-4)
- [`string=?`](#string-3)
- [`string>=?`](#string-7)
- [`string>?`](#string-5)
- [`string?`](#string)
- [`substring`](#substring)
- [`symbol->string`](#symbol-string)
- [`symbol=?`](#symbol-2)
- [`symbol?`](#symbol)
- [`syntax-error`](#syntax-error)
- [`tan`](#tan)
- [`textual-port?`](#textual-port)
- [`truncate`](#truncate-2)
- [`truncate-quotient`](#truncate-quotient)
- [`truncate-remainder`](#truncate-remainder)
- [`truncate/`](#truncate)
- [`u8-ready?`](#u8-ready)
- [`unless`](#unless)
- [`utf8->string`](#utf8-string)
- [`values`](#values)
- [`vector`](#vector-2)
- [`vector->list`](#vector-list)
- [`vector->string`](#vector-string)
- [`vector-append`](#vector-append)
- [`vector-copy`](#vector-copy)
- [`vector-copy!`](#vector-copy-2)
- [`vector-fill!`](#vector-fill)
- [`vector-for-each`](#vector-for-each)
- [`vector-length`](#vector-length)
- [`vector-map`](#vector-map)
- [`vector-ref`](#vector-ref)
- [`vector-set!`](#vector-set)
- [`vector?`](#vector)
- [`when`](#when)
- [`with-exception-handler`](#with-exception-handler)
- [`with-input-from-file`](#with-input-from-file)
- [`with-output-to-file`](#with-output-to-file)
- [`write`](#write)
- [`write-bytevector`](#write-bytevector)
- [`write-char`](#write-char)
- [`write-shared`](#write-shared)
- [`write-simple`](#write-simple)
- [`write-string`](#write-string)
- [`write-u8`](#write-u8)
- [`zero?`](#zero)
