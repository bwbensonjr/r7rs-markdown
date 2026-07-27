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
