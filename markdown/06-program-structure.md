# Program structure

<a id="programchapter"></a>

## Programs

A Scheme program consists of
one or more import declarations followed by a sequence of
expressions and definitions.
Import declarations specify the libraries on which a program or library depends;
a subset of the identifiers exported by the libraries are made available to
the program.
Expressions are described in chapter [Expressions](05-expressions.md#expressionchapter).
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
For the formal definition, see [Sequencing](05-expressions.md#sequencing).

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
two types of `begin` defined in section [Sequencing](05-expressions.md#sequencing).

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
main program [[life](14-references.md#cite-life)].
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
Appendix [Standard Libraries](09-standard-libraries.md#stdlibraries).

Implementations may provide an initial REPL environment
which behaves as if all possible variables are bound to locations, most of
which contain unspecified values. Top level REPL definitions in
such an implementation are truly equivalent to assignments,
unless the identifier is defined as a syntax keyword.

An implementation may provide a mode of operation in which the REPL
reads its input from a file. Such a file is not, in general, the same
as a program, because it can contain import declarations in places other than
the beginning.
