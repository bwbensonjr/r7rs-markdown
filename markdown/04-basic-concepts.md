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
Those that bind syntactic keywords are listed in section [Macros](05-expressions.md#macrosection).
The most fundamental of the variable binding constructs is the
`lambda` expression, because all other variable binding constructs
(except top-level bindings)
can be explained in terms of `lambda` expressions. The other
variable binding constructs are `let`, `let*`, `letrec`,
`letrec*`, `let-values`, `let*-values`,
and `do` expressions (see sections [lambda](05-expressions.md#lambda), [letrec](05-expressions.md#letrec), and
[do](05-expressions.md#do)).

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
(chapters [Expressions](05-expressions.md#expressionchapter) and [Standard procedures](07-standard-procedures.md#initialenv)); if there is no
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
conditional test. As explained in section [Booleans](07-standard-procedures.md#booleansection), all
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
)`” and “`(8 . (13 . ()))`” (see section [Pairs and lists](07-standard-procedures.md#listsection)).

Many objects have standard external representations, but some, such as
procedures, do not have standard representations (although particular
implementations may define representations for them).

An external representation can be written in a program to obtain the
corresponding object (see `quote`, section [quote](05-expressions.md#quote)).

External representations can also be used for input and output. The
procedure `read` (section [read](07-standard-procedures.md#read)) parses external
representations, and the procedure `write` (section [write](07-standard-procedures.md#write))
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
objects in the appropriate sections of chapter [Standard procedures](07-standard-procedures.md#initialenv).

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
(section [Equivalence predicates](07-standard-procedures.md#equivalencesection))
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
in [[propertailrecursion](14-references.md#cite-propertailrecursion)].

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
  chapter [Formal syntax and semantics](08-formal-syntax-and-semantics.md#formalchapter) by replacing some occurrences of ⟨body⟩
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
