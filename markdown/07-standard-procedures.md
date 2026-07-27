# Standard procedures

<a id="initialenv"></a>
<a id="builtinchapter"></a>

<a id="initial-environment"></a>
<a id="global-environment"></a>
<a id="procedure"></a>

This chapter describes Scheme's built-in procedures.

The procedures `force`, `promise?`, and `make-promise` are intimately associated
with the expression types `delay` and `delay-force`, and are described
with them in section [force](05-expressions.md#force). In the same way, the procedure
`make-parameter` is intimately associated with the expression type
`parameterize`, and is described with it in section [make-parameter](05-expressions.md#make-parameter).

A program can use a global variable definition to bind any variable. It may
subsequently alter any such binding by an assignment (see
section [Assignments](05-expressions.md#assignment)). These operations do not modify the behavior of
any procedure defined in this report or imported from a library
(see section [Libraries](06-program-structure.md#libraries)). Altering any global binding that has
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
  (section [Storage model](04-basic-concepts.md#storagemodel)).
- *obj*₁ and *obj*₂ are procedures whose location tags are
  equal (section [lambda](05-expressions.md#lambda)).

The `eqv?` procedure returns `#f` if:

- *obj*₁ and *obj*₂ are of different types
  (section [Disjointness of types](04-basic-concepts.md#disjointness)).
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
using these floating-point standards [[IEEE](14-references.md#cite-ieee)].
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
section [Lexical structure](08-formal-syntax-and-semantics.md#numbersyntax). Note that case is not significant in numerical
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

The reader is referred to section [Entry format](02-overview.md#typeconventions) for a summary
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

```math
\sin^{-1} z = -i \log (i z + \sqrt{1 - z^2})
```

```math
\cos^{-1} z = \pi / 2 - \sin^{-1} z
```

```math
\tan^{-1} z = (\log (1 + i z) - \log (1 - i z)) / (2 i)
```

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

The above specification follows [[CLtL](14-references.md#cite-cltl)], which in turn
cites [[Penfield81](14-references.md#cite-penfield81)]; refer to these sources for more detailed
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

```math
{z_1}^{z_2} = e^{z_2 \log {z_1}}
```

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

```math
{z} = {x_{1}} + {x_{2}}{i}
 = {x_{3}} \cdot e^{i x_4}
```

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
true [[howtoprint](14-references.md#cite-howtoprint), [howtoread](14-references.md#cite-howtoread)];
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
⟨expression⟩ is also a ⟨datum⟩ (see section [External representations](08-formal-syntax-and-semantics.md#datum)).
Among other things, this permits the use of the `read` procedure to
parse Scheme programs. See section [External representations](04-basic-concepts.md#externalreps).

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
writing an identifier; see sections [Identifiers](03-lexical-conventions.md#syntaxsection)
and [Lexical structure](08-formal-syntax-and-semantics.md#identifiersyntax).

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
See UAX #44 [[uax44](14-references.md#cite-uax44)] (part of the Unicode Standard) for details.

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
$\varsigma$ at the end of a word. See UAX #44 [[uax44](14-references.md#cite-uax44)] (part of
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
For the concept of Scheme exceptions, see section [Error situations and unspecified behavior](02-overview.md#errorsituations).
See also [guard](05-expressions.md#guard) for the `guard` syntax.

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
considered as an import set, into it. (See section [Libraries](06-program-structure.md#libraries) for
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
section [make-parameter](05-expressions.md#make-parameter)). The initial bindings for these
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
⟨datum⟩ (see sections [External representations](08-formal-syntax-and-semantics.md#datum) and
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
in section [Datum labels](03-lexical-conventions.md#labelsection). Datum labels must not be used if there
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

As of 2018, a TAI-UTC offset table can be found at [[TAI](14-references.md#cite-tai)].

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
