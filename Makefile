# r7rs-markdown — generate a Markdown edition of R7RS-small from the
# LaTeX sources in the pinned r7rs-spec submodule.

.PHONY: markdown clean submodule update-spec

SPEC := r7rs-spec/spec
OUT  := markdown

# Generate the Markdown edition (per-chapter files + combined r7rs.md + README).
markdown: submodule
	python3 tools/tex2md.py --spec $(SPEC) --out $(OUT)

# Ensure the submodule is checked out (after a plain `git clone`).
submodule:
	@test -f $(SPEC)/r7rs.tex || git submodule update --init --recursive

# Advance the submodule to the latest upstream commit, then regenerate.
# Review and commit the resulting r7rs-spec pointer + markdown/ changes.
update-spec:
	git submodule update --remote r7rs-spec
	$(MAKE) markdown

clean:
	rm -f $(OUT)/*.md
