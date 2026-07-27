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

0`⟨identifier⟩`

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
are implicitly replicated for R = 2, 8, 10,
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

⟨Datum⟩ is what the `read` procedure (section [read](07-standard-procedures.md#read))
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
and notation used here are described in [[Stoy77](14-references.md#cite-stoy77)]; the definition of
`dynamic-wind` is taken from [[GasbichlerKnauelSperberKelsey2003](14-references.md#cite-gasbichlerknauelsperberkelsey2003)].
The notation is summarized below:

```math
\begin{array}{ll}
⟨\,\ldots\,⟩ & \text{sequence formation} \\
s \downarrow k & k\text{th member of the sequence }s\text{ (1-based)} \\
\#s & \text{length of sequence }s \\
s \;§\; t & \text{concatenation of sequences }s\text{ and }t \\
s \dagger k & \text{drop the first }k\text{ members of sequence }s \\
t \rightarrow a, b & \text{McCarthy conditional “if }t\text{ then }a\text{ else }b\text{”} \\
\rho[x/i] & \text{substitution “}\rho\text{ with }x\text{ for }i\text{”} \\
x\mathrm{ in }{\texttt{D}} & \text{injection of }x\text{ into domain }\texttt{D} \\
x\,\vert\,\texttt{D} & \text{projection of }x\text{ to domain }\texttt{D} \\
\end{array}
```

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
obey the following axiom: if new::∈:`L`, then
$\sigma\;(\mathit{new}\;\sigma\;\vert\;\mathtt{L})\downarrow 2 = \mathit{false}$.

The definition of $\mathcal{K}$ is omitted because an accurate definition of
$\mathcal{K}$ would complicate the semantics without being very interesting.

If P is a program in which all variables are defined before being
referenced or assigned, then the meaning of P is

```math
\mathcal{E}⟦\text{\texttt{((lambda ({\textrm{I}}{*}) \textrm{P}')
{⟨ undefined ⟩} …foo)}}⟧
```

where I is the sequence of variables defined in P, $\mathrm{P}'$
is the sequence of expressions obtained by replacing every definition
in P by an assignment, ⟨undefined⟩ is an expression that evaluates
to undefined, and
$\mathcal{E}$ is the semantic function that assigns meaning to expressions.

### Abstract syntax

|$\vert$

```math
\begin{array}{llll}
\mathrm{K} & \in & \text{\hboxCon} & \text{constants, including quotations} \\
\mathrm{I} & \in & \text{\hboxIde} & \text{identifiers (variables)} \\
\mathrm{E} & \in & \text{\hboxExp} & \text{expressions} \\
{\Gamma} & \in & \text{\hboxCom }=\text{ \hboxExp} & \text{commands} \\
\end{array}
```

0=` Exp `
1=to 10 |

```bnf
 Exp ⟶  K  |   I  |  ( E₀  E*)
  (lambda ( I*) \Gamma*  E₀)
  (lambda ( I* .  I) \Gamma*  E₀)
  (lambda  I \Gamma*  E₀)
  (if  E₀  E₁  E₂)  |  (if  E₀  E₁)
  (set!  I  E)
```

### Domain equations

```math
\begin{array}{llllll}
\alpha & \in & \mathtt{L} &  &  & \text{locations} \\
\nu & \in & \mathtt{N} &  &  & \text{natural numbers} \\
 &  & \mathtt{T} & = & \{\text{false, true}\} & \text{booleans} \\
 &  & \mathtt{Q} &  &  & \text{symbols} \\
 &  & \mathtt{H} &  &  & \text{characters} \\
 &  & \mathtt{R} &  &  & \text{numbers} \\
 &  & {\mathtt{E}_\mathrm{p}} & = & \mathtt{L} \times \mathtt{L} \times \mathtt{T} & \text{pairs} \\
 &  & {\mathtt{E}_\mathrm{v}} & = & {\mathtt{L}}^{*} \times \mathtt{T} & \text{vectors} \\
 &  & {\mathtt{E}_\mathrm{s}} & = & {\mathtt{L}}^{*} \times \mathtt{T} & \text{strings} \\
 &  & \mathtt{M} & = & \text{\false, true, null, undefined, unspecified\}} &  \\
 &  &  &  &  & \text{miscellaneous} \\
\phi & \in & \mathtt{F} & = & \mathtt{L}\times({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) & \text{procedure values} \\
\epsilon & \in & \mathtt{E} & = & {\mathtt{Q}+\mathtt{H}+\mathtt{R}+{\mathtt{E}_\mathrm{p}}+{\mathtt{E}_\mathrm{v}}+{\mathtt{E}_\mathrm{s}}+\mathtt{M}+\mathtt{F}} &  \\
 &  &  &  &  & \text{expressed values} \\
\sigma & \in & \mathtt{S} & = & \mathtt{L}\to(\mathtt{E}\times\mathtt{T}) & \text{stores} \\
\rho & \in & \mathtt{U} & = & \mathrm{Ide}\to\mathtt{L} & \text{environments} \\
\theta & \in & \mathtt{C} & = & \mathtt{S}\to\mathtt{A} & \text{command conts} \\
\kappa & \in & \mathtt{K} & = & {\mathtt{E}}^{*}\to\mathtt{C} & \text{expression conts} \\
 &  & \mathtt{A} &  &  & \text{answers} \\
 &  & \mathtt{X} &  &  & \text{errors} \\
\omega & \in & {P} & = & (\mathtt{F} \times \mathtt{F} \times {P}) + \{\textit{root}\} & \text{dynamic points} \\
\end{array}
```

### Semantic functions

```math
\begin{array}{ll}
\mathcal{K}: & \mathrm{Con}\to\mathtt{E} \\
\mathcal{E}: & \mathrm{Exp}\to\mathtt{U}\to{P}\to\mathtt{K}\to\mathtt{C} \\
{\mathcal{E}}^{*}: & {\mathrm{Exp}}^{*}\to\mathtt{U}\to{P}\to\mathtt{K}\to\mathtt{C} \\
\mathcal{C}: & {\mathrm{Com}}^{*}\to\mathtt{U}\to{P}\to\mathtt{C}\to\mathtt{C} \\
\end{array}
```

Definition of K deliberately omitted.

```math
\mathcal{E}⟦\mathrm{K}⟧ =
  \lambda\rho\omega\kappa\;.\;\mathit{send}\,(\mathcal{K}⟦\mathrm{K}⟧)\,\kappa
```

```math
\begin{aligned}
\mathcal{E}⟦\mathrm{I}⟧ = 
  \lambda\rho\omega\kappa\;.\;\mathit{hold}\;
    (\mathit{lookup}\;\rho\;\mathrm{I}) \\
(\mathit{single}(\lambda\epsilon\;.\;
        \epsilon = \mathit{undefined}\rightarrow \\
\text{}\mathit{wrong }\mathrm{\text{“}undefined variable\text{”}}, \\
\text{}\mathit{send}\;\epsilon\;\kappa))
\end{aligned}
```

```math
\begin{aligned}
\mathcal{E}⟦{\texttt{(\textrm{E}0 {\textrm{E}}{*})}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;{\mathcal{E}}^{*}
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
```

```math
\begin{aligned}
\mathcal{E}⟦{\texttt{(\texttt{lambda} ({\textrm{I}}{*}) {{Γ}}{*} \textrm{E}0)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\lambda\sigma\;.\; \\
\text{}\mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{send}\;
     (⟨
         \mathit{new}\;\sigma\,\vert\,\mathtt{L}, \\
\lambda{\epsilon}^{*}\omega^\prime\kappa^\prime\;.\;
               \#{\epsilon}^{*} = \#{{\mathrm{I}}^{*}}\rightarrow \\
\text{}\mathit{tievals}
                   (\lambda{\alpha}^{*}\;.\;
                         (\lambda\rho^\prime\;.\;\mathcal{C}⟦{{\Gamma}}^{*}⟧\rho^\prime\omega^\prime
                              (\mathcal{E}⟦\mathrm{E}_0⟧\rho^\prime\omega^\prime\kappa^\prime)) \\
(\mathit{extends}\;\rho\;{{\mathrm{I}}^{*}}\;{\alpha}^{*})) \\
{\epsilon}^{*}, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}⟩ \\
\mathrm{ in }\mathtt{E}) \\
\kappa \\
(\mathit{update}\;(\mathit{new}\;\sigma\,\vert\,\mathtt{L})
                           \;\mathit{unspecified}
                           \;\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\;\sigma
\end{aligned}
```

```math
\begin{aligned}
\mathcal{E}⟦{\texttt{(lambda ({\textrm{I}}{*} .\ \textrm{I}) {{Γ}}{*} \textrm{E}0)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\lambda\sigma\;.\; \\
\text{}\mathit{new}\;\sigma\;\in\;\mathtt{L}\rightarrow \\
\text{}\mathit{send}\;
     (⟨
         \mathit{new}\;\sigma\,\vert\,\mathtt{L}, \\
\lambda{\epsilon}^{*}\omega^\prime\kappa^\prime\;.\;
               \#{\epsilon}^{*} \geq \#{\mathrm{I}}^{*}\rightarrow \\
\text{}\mathit{tievalsrest} \\
\text{}(\lambda{\alpha}^{*}\;.\;
                           (\lambda\rho^\prime\;.\;\mathcal{C}⟦{{\Gamma}}^{*}⟧\rho^\prime\omega^\prime
                               (\mathcal{E}⟦\mathrm{E}_0⟧\rho^\prime\omega^\prime\kappa^\prime)) \\
(\mathit{extends}\;\rho
                               \;({\mathrm{I}}^{*}\;§\;⟨\mathrm{I}⟩)
                               \;{\alpha}^{*})) \\
{\epsilon}^{*} \\
(\#{\mathrm{I}}^{*}), \\
\text{}\mathit{wrong }\mathrm{\text{“}too few arguments\text{”}}⟩\mathrm{ in }\mathtt{E}) \\
\kappa \\
(\mathit{update}\;(\mathit{new}\;\sigma\,\vert\,\mathtt{L})
                           \;\mathit{unspecified}
                           \;\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\;\sigma
\end{aligned}
```

```math
\mathcal{E}⟦{\texttt{(lambda \textrm{I} {{Γ}}{*} \textrm{E}0)}}⟧ =
 \mathcal{E}⟦{\texttt{(lambda (.\ \textrm{I}) {{Γ}}{*} \textrm{E}0)}}⟧
```

```math
\begin{aligned}
\mathcal{E}⟦{\texttt{(\texttt{if} \textrm{E}0 \textrm{E}1 \textrm{E}2)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
   \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;(\mathit{single}\;(\lambda\epsilon\;.\;
    \mathit{truish}\;\epsilon\rightarrow\mathcal{E}⟦\mathrm{E}_1⟧\rho\omega\kappa, \\
\text{}\mathcal{E}⟦\mathrm{E}_2⟧\rho\omega\kappa))
\end{aligned}
```

```math
\begin{aligned}
\mathcal{E}⟦{\texttt{(if \textrm{E}0 \textrm{E}1)}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
   \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;(\mathit{single}\;(\lambda\epsilon\;.\;
    \mathit{truish}\;\epsilon\rightarrow\mathcal{E}⟦\mathrm{E}_1⟧\rho\omega\kappa, \\
\text{}\mathit{send}\;\mathit{unspecified}\;\kappa))
\end{aligned}
```

Here and elsewhere, any expressed value other than *undefined* may
be used in place of *unspecified*.

```math
\begin{aligned}
\mathcal{E}⟦\text{\texttt{(\texttt{set!} \textrm{I} \textrm{E})}}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;\mathcal{E}⟦\mathrm{E}⟧\;\rho\;\omega\;
     (\mathit{single}(\lambda\epsilon\;.\;\mathit{assign}\;
       (\mathit{lookup}\;\rho\;\mathrm{I}) \\
\epsilon \\
(\mathit{send}\;\mathit{unspecified}\;\kappa)))
\end{aligned}
```

```math
{\mathcal{E}}^{*}⟦\;⟧ =
  \lambda\rho\omega\kappa\;.\;\kappa⟨\;⟩
```

```math
\begin{aligned}
{\mathcal{E}}^{*}⟦\mathrm{E}_0\;{\mathrm{E}}^{*}⟧ = \\
\text{}\lambda\rho\omega\kappa\;.\;
      \mathcal{E}⟦\mathrm{E}_0⟧\;\rho\omega\;
         (\mathit{single}
            (\lambda\epsilon_0\;.\;{\mathcal{E}}^{*}⟦{\mathrm{E}}^{*}⟧
                \;\rho\omega\;(\lambda{\epsilon}^{*}\;.\;
                           \kappa\;(⟨\epsilon_0⟩\;§\;{\epsilon}^{*}))))
\end{aligned}
```

```math
\mathcal{C}⟦\;⟧ = \lambda\rho\omega\theta\,.\;\theta
```

```math
\mathcal{C}⟦{\Gamma}_0\;{{\Gamma}}^{*}⟧ =
  \lambda\rho\omega\theta\;.\;\mathcal{E}⟦{\Gamma}_0⟧\;\rho\omega\;(\lambda{\epsilon}^{*}\;.\;
   \mathcal{C}⟦{{\Gamma}}^{*}⟧\rho\omega\theta)
```

### Auxiliary functions

```math
\begin{aligned}
\mathit{lookup}        :  \mathtt{U} \to \mathrm{Ide} \to \mathtt{L} \\
\mathit{lookup} =
 \lambda\rho\mathrm{I}\;.\;\rho\mathrm{I}
\end{aligned}
```

```math
\begin{aligned}
\mathit{extends}       :  \mathtt{U} \to {\mathrm{Ide}}^{*} \to {\mathtt{L}}^{*} \to \mathtt{U} \\
\mathit{extends} = \\
\text{}\lambda\rho{\mathrm{I}}^{*}{\alpha}^{*}\;.\;
   \#{\mathrm{I}}^{*}=0\rightarrow\rho, \\
\text{}\mathit{extends}\;(\rho[({\alpha}^{*}\downarrow 1)/({\mathrm{I}}^{*}\downarrow 1)])
                               \;({\mathrm{I}}^{*}\dagger 1)
                               \;({\alpha}^{*}\dagger 1)
\end{aligned}
```

```math
\mathit{wrong}  :  \mathtt{X} \to \mathtt{C}    \text{\qquad [implementation-dependent]}
```

```math
\begin{aligned}
\mathit{send}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\
\mathit{send} =
 \lambda\epsilon\kappa\;.\;\kappa⟨\epsilon⟩
\end{aligned}
```

```math
\begin{aligned}
\mathit{single}        :  (\mathtt{E} \to \mathtt{C}) \to \mathtt{K} \\
\mathit{single} = \\
\text{}\lambda\psi{\epsilon}^{*}\;.\;
   \#{\epsilon}^{*}=1\rightarrow\psi({\epsilon}^{*}\downarrow 1), \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of return values\text{”}}
\end{aligned}
```

```math
\mathit{new}           :  \mathtt{S} \to (\mathtt{L} + \{ \mathit{error} \})
    \text{\qquad [implementation-dependent]}
```

```math
\begin{aligned}
\mathit{hold}          :  \mathtt{L} \to \mathtt{K} \to \mathtt{C} \\
\mathit{hold} =
 \lambda\alpha\kappa\sigma\;.\;\mathit{send}\,(\sigma\alpha\downarrow 1)\kappa\sigma
\end{aligned}
```

```math
\begin{aligned}
\mathit{assign}        :  \mathtt{L} \to \mathtt{E} \to \mathtt{C} \to \mathtt{C} \\
\mathit{assign} =
 \lambda\alpha\epsilon\theta\sigma\;.\;\theta(\mathit{update}\;\alpha\epsilon\sigma)
\end{aligned}
```

```math
\begin{aligned}
\mathit{update}        :  \mathtt{L} \to \mathtt{E} \to \mathtt{S} \to \mathtt{S} \\
\mathit{update} =
 \lambda\alpha\epsilon\sigma\;.\;\sigma[⟨\epsilon,\mathit{true}⟩/\alpha]
\end{aligned}
```

```math
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
```

```math
\begin{aligned}
\mathit{tievalsrest}   :  ({\mathtt{L}}^{*} \to \mathtt{C}) \to {\mathtt{E}}^{*} \to \mathtt{N} \to \mathtt{C} \\
\mathit{tievalsrest} = \\
\text{}\lambda\psi{\epsilon}^{*}\nu\;.\;\mathit{list}\;
   (\mathit{dropfirst}\;{\epsilon}^{*}\nu) \\
(\mathit{single}(\lambda\epsilon\;.\;\mathit{tievals}\;\psi\;
           ((\mathit{takefirst}\;{\epsilon}^{*}\nu)\;§\;⟨\epsilon⟩)))
\end{aligned}
```

```math
\mathit{dropfirst} =
 \lambda l n \;.\;  n=0 \rightarrow l, \mathit{dropfirst}\,(l \dagger 1)(n - 1)
```

```math
\mathit{takefirst} =
 \lambda l n \;.\; n=0 \rightarrow ⟨\;⟩,
     ⟨ l \downarrow 1⟩\;§\;(\mathit{takefirst}\,(l \dagger 1)(n - 1))
```

```math
\begin{aligned}
\mathit{truish}        :  \mathtt{E} \to \mathtt{T} \\
\mathit{truish} =
  \lambda\epsilon\;.\;
     \epsilon = \mathit{false}\rightarrow
          \mathit{false},
          \mathit{true}
\end{aligned}
```

```math
\mathit{permute}       :  {\mathrm{Exp}}^{*} \to {\mathrm{Exp}}^{*}
    \text{\qquad [implementation-dependent]}
```

```math
\mathit{unpermute}     :  {\mathtt{E}}^{*} \to {\mathtt{E}}^{*}
    \text{\qquad [inverse of \textit{permute}]}
```

```math
\begin{aligned}
\mathit{applicate}     :  \mathtt{E} \to {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{applicate} = \\
\text{}\lambda\epsilon{\epsilon}^{*}\omega\kappa\;.\;
   \epsilon\;\in\;\mathtt{F}\rightarrow(\epsilon\;\vert\;\mathtt{F}\downarrow 2){\epsilon}^{*}\omega\kappa,
          \mathit{wrong }\mathrm{\text{“}bad procedure\text{”}}
\end{aligned}
```

```math
\begin{aligned}
\mathit{onearg}      :  (\mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\
\mathit{onearg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=1\rightarrow\zeta({\epsilon}^{*}\downarrow 1)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
```

```math
\begin{aligned}
\mathit{twoarg}      :  (\mathtt{E} \to \mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\
\mathit{twoarg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=2\rightarrow\zeta({\epsilon}^{*}\downarrow 1)({\epsilon}^{*}\downarrow 2)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
```

```math
\begin{aligned}
\mathit{threearg}      :  (\mathtt{E} \to \mathtt{E} \to \mathtt{E} \to {P} \to \mathtt{K} \to \mathtt{C}) \to ({\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}) \\
\mathit{threearg} = \\
\text{}\lambda\zeta{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=3\rightarrow\zeta({\epsilon}^{*}\downarrow 1)({\epsilon}^{*}\downarrow 2)({\epsilon}^{*}\downarrow 3)\omega\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}wrong number of arguments\text{”}}
\end{aligned}
```

```math
\begin{aligned}
\mathit{list}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{list} = \\
\text{}\lambda{\epsilon}^{*}\omega\kappa\;.\;
   \#{\epsilon}^{*}=0\rightarrow\mathit{send}\;\mathit{null}\;\kappa, \\
\text{}\mathit{list}\,({\epsilon}^{*}\dagger 1)
             (\mathit{single}(\lambda\epsilon\;.\;
                   \mathit{cons}⟨{\epsilon}^{*}\downarrow 1,\epsilon⟩\kappa))
\end{aligned}
```

```math
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
\mathrm{ in }\mathtt{E}) \\
\kappa \\
(\mathit{update}(\mathit{new}\;\sigma^\prime\;\vert\;\mathtt{L})
                                     \epsilon_2
                                     \sigma^\prime), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\sigma^\prime) \\
(\mathit{update}(\mathit{new}\;\sigma\;\vert\;\mathtt{L})\epsilon_1\sigma), \\
\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\sigma)
\end{aligned}
```

```math
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
```

```math
\begin{aligned}
\mathit{add}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{add} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   (\epsilon_1\;\in\;\mathtt{R}\wedge\epsilon_2\;\in\;\mathtt{R})\rightarrow \\
\text{}\mathit{send}\,
       ((\epsilon_1\;\vert\;\mathtt{R}+\epsilon_2\;\vert\;\mathtt{R})\mathrm{ in }\mathtt{E})
           \kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-numeric argument to { +}\text{”}})
\end{aligned}
```

```math
\begin{aligned}
\mathit{car}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{car} = \\
\text{}\mathit{onearg}\,(\lambda\epsilon\omega\kappa\;.\;
   \epsilon\;\in\;{\mathtt{E}_\mathrm{p}}\rightarrow
          \mathit{car-internal}\;\epsilon\kappa, \\
\text{}\mathit{wrong }\mathrm{\text{“}non-pair argument to { car}\text{”}})
\end{aligned}
```

```math
\begin{aligned}
\mathit{car-internal}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\
\mathit{car-internal} =
 \text{}\lambda\epsilon\omega\kappa\;.\;
   \mathit{hold}\, (\epsilon\;\vert\;{\mathtt{E}_\mathrm{p}}\downarrow 1) \kappa
\end{aligned}
```

```math
\mathit{cdr}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} 
\text{\qquad [similar to \textit{car}]}
```

```math
\mathit{cdr-internal} :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} 
\text{\qquad [similar to \textit{car-internal}]}
```

```math
\begin{aligned}
\mathit{setcar}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{setcar} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \epsilon_1\;\in\;{\mathtt{E}_\mathrm{p}}\rightarrow \\
(\epsilon_1\;\vert\;{\mathtt{E}_\mathrm{p}}\downarrow 3)\rightarrow
          \mathit{assign}\,(\epsilon_1\;\vert\;{\mathtt{E}_\mathrm{p}}\downarrow 1) \\
\epsilon_2 \\
(\mathit{send}\;\mathit{unspecified}\;\kappa), \\
\mathit{wrong }\mathrm{\text{“}immutable argument to { set-car!}\text{”}}, \\
\mathit{wrong }\mathrm{\text{“}non-pair argument to { set-car!}\text{”}})
\end{aligned}
```

```math
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
(\epsilon_1\;\in\;{\mathtt{E}_\mathrm{p}}\wedge\epsilon_2\;\in\;{\mathtt{E}_\mathrm{p}})\rightarrow \\
\text{}\mathit{send}\,
       ((\lambda{p_1}{p_2}\;.\;
                (({p_1}\downarrow 1) = ({p_2}\downarrow 1)\wedge \\
({p_1}\downarrow 2) = ({p_2}\downarrow 2))
                     \rightarrow\mathit{true}, \\
\text{}\mathit{false}) \\
(\epsilon_1\;\vert\;{\mathtt{E}_\mathrm{p}}) \\
(\epsilon_2\;\vert\;{\mathtt{E}_\mathrm{p}})) \\
\kappa, \\
(\epsilon_1\;\in\;{\mathtt{E}_\mathrm{v}}\wedge\epsilon_2\;\in\;{\mathtt{E}_\mathrm{v}})\rightarrow
\ldots, \\
(\epsilon_1\;\in\;{\mathtt{E}_\mathrm{s}}\wedge\epsilon_2\;\in\;{\mathtt{E}_\mathrm{s}})\rightarrow
\ldots, \\
(\epsilon_1\;\in\;\mathtt{F}\wedge\epsilon_2\;\in\;\mathtt{F})\rightarrow \\
\text{}\mathit{send}\,
       ((\epsilon_1\;\vert\;\mathtt{F}\downarrow 1) = (\epsilon_2\;\vert\;\mathtt{F}\downarrow 1)
               \rightarrow\mathit{true},
                          \mathit{false}) \\
\kappa, \\
\text{}\mathit{send}\,\;\mathit{false}\;\kappa)
\end{aligned}
```

```math
\begin{aligned}
\mathit{apply}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{apply} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \epsilon_1\;\in\;\mathtt{F}\rightarrow
         \mathit{valueslist}\;\epsilon_2
            (\lambda{\epsilon}^{*}\;.\;\mathit{applicate}\;\epsilon_1{\epsilon}^{*}\omega\kappa), \\
\text{}\mathit{wrong }\mathrm{\text{“}bad procedure argument to { apply}\text{”}})
\end{aligned}
```

```math
\begin{aligned}
\mathit{valueslist}          :  \mathtt{E} \to \mathtt{K} \to \mathtt{C} \\
\mathit{valueslist} = \\
\text{}\lambda\epsilon\kappa\;.\;
   \epsilon\;\in\;{\mathtt{E}_\mathrm{p}}\rightarrow \\
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
```

```math
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
                      \mathrm{ in }\mathtt{E}⟩ \\
\omega \\
\kappa \\
(\mathit{update}\,
                (\mathit{new}\;\sigma\;\vert\;\mathtt{L}) \\
\mathit{unspecified} \\
\sigma), \\
\text{}\mathit{wrong }\mathrm{\text{“}out of memory\text{”}}\,\sigma), \\
\mathit{wrong }\mathrm{\text{“}bad procedure argument\text{”}})
\end{aligned}
```

```math
\begin{aligned}
\mathit{travel} : {P} \to {P} \to \mathtt{C} \to \mathtt{C} \\
\mathit{travel} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \mathit{travelpath}\;((\mathit{pathup}\;\omega_1(\mathit{commonancest}\;\omega_1\omega_2)) \;§\; \\
 (\mathit{pathdown}\;(\mathit{commonancest}\;\omega_1\omega_2)\omega_2))
\end{aligned}
```

```math
\begin{aligned}
\mathit{pointdepth} : {P} \to \mathtt{N} \\
\mathit{pointdepth} =  \\
\text{}\lambda\omega\;.\; \omega = \textit{root} \rightarrow 0,
  1 + (\mathit{pointdepth}\;(\omega\;\vert\;(\mathtt{F} \times \mathtt{F} \times
  {P})\downarrow 3))
\end{aligned}
```

```math
\begin{aligned}
\mathit{ancestors} : {P} \to \mathcal{P}{P} \\
\mathit{ancestors} =  \\
\text{}\lambda\omega\;.\; \omega = \textit{root} \rightarrow \{\omega\},
  \{\omega\}\;\cup\;(\mathit{ancestors}\;(\omega\;\vert\;(\mathtt{F} \times \mathtt{F} \times
  {P})\downarrow 3))
\end{aligned}
```

```math
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
```

```math
\begin{aligned}
\mathit{pathup} : {P} \to {P} \to {({P} \times \mathtt{F})}^{*} \\
\mathit{pathup} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \omega_1=\omega_2\rightarrow⟨⟩, \\
⟨(\omega_1, \omega_1\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 2)⟩
  \;§\; \\
(\mathit{pathup}\;(\omega_1\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 3)\omega_2)
\end{aligned}
```

```math
\begin{aligned}
\mathit{pathdown} : {P} \to {P} \to {({P} \times \mathtt{F})}^{*} \\
\mathit{pathdown} =  \\
\text{}\lambda\omega_1\omega_2\;.\;
  \omega_1=\omega_2\rightarrow⟨⟩, \\
(\mathit{pathdown}\;\omega_1(\omega_2\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 3))
  \;§\; \\
⟨(\omega_2, \omega_2\;\vert\;(\mathtt{F} \times \mathtt{F} \times {P})\downarrow 1)⟩
\end{aligned}
```

```math
\begin{aligned}
\mathit{travelpath} : {({P} \times \mathtt{F})}^{*} \to \mathtt{C} \to \mathtt{C} \\
\mathit{travelpath} =  \\
\text{}\lambda{\pi}^{*}\theta\;.\;
  \#{\pi}^{*}=0\rightarrow\theta, \\
(({\pi}^{*}\downarrow 1)\downarrow 2)⟨⟩(({\pi}^{*}\downarrow 1)\downarrow 1) \\
(\lambda{\epsilon}^{*}\;.\;\mathit{travelpath}\;({\pi}^{*} \dagger 1)\theta)
\end{aligned}
```

```math
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
```

```math
\begin{aligned}
\mathit{values}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C} \\
\mathit{values} =
 \lambda{\epsilon}^{*}\omega\kappa\;.\;\kappa{\epsilon}^{*}
\end{aligned}
```

```math
\begin{aligned}
\mathit{cwv}          :  {\mathtt{E}}^{*} \to {P} \to \mathtt{K} \to \mathtt{C}
    \text{\qquad [\texttt{call-with-values}]} \\
\mathit{cwv} = \\
\text{}\mathit{twoarg}\,(\lambda\epsilon_1\epsilon_2\omega\kappa\;.\;
   \mathit{applicate}\;\epsilon_1⟨\;⟩\omega
(\lambda{\epsilon}^{*}\;.\;\mathit{applicate}\;\epsilon_2\;{\epsilon}^{*}\omega))
\end{aligned}
```

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
[[srfi45](14-references.md#cite-srfi45)] until a non-lazy result (i.e. a value created by `delay` instead of `delay-force`) is returned, as follows:

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
