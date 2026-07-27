# Expressions

<a id="expressionchapter"></a>

Expression types are categorized as *primitive* or *derived*.
Primitive expression types include variables and procedure calls.
Derived expression types are not semantically primitive, but can instead
be defined as macros.
Suitable syntax definitions of some of the derived expressions are
given in section [Derived expression types](08-formal-syntax-and-semantics.md#derivedsection).

The procedures `force`, `promise?`, `make-promise`, and `make-parameter`
are also described in this chapter because they are intimately associated
with the `delay`, `delay-force`, and `parameterize` expression types.

## Primitive expression types

<a id="primitivexps"></a>

### Variable references

**`⟨variable⟩`** — syntax

An expression consisting of a variable
(section [Variables, syntactic keywords, and regions](04-basic-concepts.md#variablesection)) is a variable reference. The value of
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
section [External representations](04-basic-concepts.md#externalreps)). This notation is used to include literal
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

As noted in section [Storage model](04-basic-concepts.md#storagemodel), it is an error to attempt to alter a constant
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
section [Control features](07-standard-procedures.md#proceduresection)).
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
`eq?` work on procedures (see section [Equivalence predicates](07-standard-procedures.md#equivalencesection)).

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
section [Booleans](07-standard-procedures.md#booleansection)), then ⟨consequent⟩ is evaluated and
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
For reference purposes, section [Derived expression types](08-formal-syntax-and-semantics.md#derivedsection) gives syntax definitions
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
section [Booleans](07-standard-procedures.md#booleansection)). When a ⟨test⟩ evaluates to a true
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
`eqv?`; see section [eqv?](07-standard-procedures.md#eqv)) to a ⟨datum⟩, then the
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
section [Booleans](07-standard-procedures.md#booleansection)), then `#f` is returned. Any remaining
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
section [Booleans](07-standard-procedures.md#booleansection)) is returned. Any remaining expressions
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
appendix [Standard Feature Identifiers](10-feature-identifiers.md#stdfeatures).

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
see section [Library Syntax](06-program-structure.md#librarydeclarations).

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
false (see section [Booleans](07-standard-procedures.md#booleansection)), then the ⟨command⟩
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
when it is initiated and when it returns. In Scheme, `call-with-current-continuation` (section [Control features](07-standard-procedures.md#continuations)) allows
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
handler that binds the raised object (see `raise` in section [Exceptions](07-standard-procedures.md#exceptionsection))
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

See section [Exceptions](07-standard-procedures.md#exceptionsection) for a more complete discussion of
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
  see section [Variable definitions](06-program-structure.md#defines).
- If a macro transformer inserts a free reference to an
  identifier, the reference refers to the binding that was visible
  where the transformer was specified, regardless of any local
  bindings that surround the use of the macro.

In consequence, all macros
defined using the pattern language are “hygienic” and “referentially
transparent” and thus preserve Scheme's lexical scoping. [[Kohlbecker86](14-references.md#cite-kohlbecker86), [hygienic](14-references.md#cite-hygienic), [Bawden88](14-references.md#cite-bawden88), [macrosthatwork](14-references.md#cite-macrosthatwork), [syntacticabstraction](14-references.md#cite-syntacticabstraction)]
<a id="hygienic"></a><a id="referentially-transparent"></a>

Implementations may provide macro facilities of other types.

### Binding constructs for syntactic keywords

<a id="bindsyntax"></a>

The `let-syntax` and `letrec-syntax` binding constructs are
analogous to `let` and `letrec`, but they bind
syntactic keywords to macro transformers instead of binding variables
to locations that contain values. Syntactic keywords can also be
bound globally or locally with `define-syntax`;
see section [define-syntax](06-program-structure.md#define-syntax).

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
section [Derived expression types](08-formal-syntax-and-semantics.md#derivedsection) then they are hygienic (as required) and
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

`syntax-error` behaves similarly to `error` ([Exceptions](07-standard-procedures.md#exceptionsection)) except that implementations
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
