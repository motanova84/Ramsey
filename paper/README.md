# Ramsey Vibracional Formal - Paper

This directory contains the LaTeX source for the formal paper on Ramsey Vibracional theory.

## Building the Paper

To build the PDF:

```bash
cd paper
pdflatex main.tex
pdflatex main.tex  # Run twice for references
```

Or using latexmk:

```bash
cd paper
latexmk -pdf main.tex
```

## Structure

- `main.tex` - Main paper file with all content
- Includes formal definitions, theorems, and computational results
- Ready for arXiv submission

## Content

The paper includes:

1. Introduction to Vibrational Ramsey Theory
2. Formal definitions (Vibrational Graph, Resonance Operator, etc.)
3. Main theoretical results
4. Computational verification with certified bounds
5. Applications (Neural Networks, Social Networks, Cryptography)
6. Bibliography

## Certification

All results in the paper are backed by:
- Lean 4 formal certificates in `/certificates`
- SMT2 verification files
- Automated CI pipeline

## Next Steps

- Generate DOI via Zenodo
- Submit to arXiv
- Submit to peer-reviewed journal
