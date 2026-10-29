# Comparing the LCG and Mersenne Twister algorithms in educational simulations

> **Academic integrity notice:** this work was submitted for the IB Diploma Programme (Mathematics Extended Essay) and has been assessed. It is shared as a portfolio piece only. Do not copy or submit any part of it for assessment; doing so is academic misconduct under the IB Academic Integrity Policy.
>
> © 2025 Júlia Muria Solé. All rights reserved. See [COPYRIGHT](COPYRIGHT). Not endorsed by the International Baccalaureate Organization.

My IB Diploma Extended Essay in Mathematics (December 2024, 2,687 words, written in Spanish). The full essay is in [extended-essay.pdf](extended-essay.pdf).

**Original title:** Comparativa de los algoritmos LGC y Mersenne Twister aplicados a simulaciones educativas

## Research question

How do the statistical properties of the Linear Congruential Generator (LCG) and the Mersenne Twister affect the accuracy and efficiency of simulations based on educational activities?

## Abstract

Computers cannot produce true randomness, so they use deterministic algorithms called pseudorandom number generators. This essay compares two of them, the LCG and the Mersenne Twister, and uses them to build digital simulations of activities from the Varga Box, a teaching kit for probability and combinatorics created by the Hungarian mathematician Tamás Varga.

After two warm-up simulations (the taxi-driver walk and the urn method), the essay focuses on the derangement problem. It proves the derangement formula by induction, works out the probabilities of partial derangements for n = 6, and simulates the game in Pygame with each generator. A Kolmogorov-Smirnov test and the simulation results show that the Mersenne Twister matches the theoretical probabilities much more closely. The LCG has a larger error but is accurate enough for classroom use, and its simpler structure lets students explore the limits of pseudorandom generators by changing its parameters.

## Stack

- Python and Pygame for the simulations (code from the appendices, now in [`src/`](src/))
- Kolmogorov-Smirnov test for checking the output distributions
- LaTeX for the write-up

## What I learned

- How pseudorandom number generators work and where they fall short
- Writing a proof by induction and applying it to a real problem
- Testing a generator statistically instead of trusting it
- Turning mathematics into an interactive tool that students can use

## Code

The programs from the essay's appendix (Anexo A–E), in Spanish as written:

| File | Appendix | What it does |
|---|---|---|
| `src/ks_test.py` | A | Kolmogorov-Smirnov test of the LCG and NumPy's Mersenne Twister against the uniform distribution |
| `src/taxista.py` | B | The taxi-driver walk (Viaje del Taxista) on the Varga board, 1–4 players, press Space to roll |
| `src/urnas.py` | C | Configurable urn, drawing with or without replacement |
| `src/desarreglos_mersenne.py` | D | Derangement (Varga ball box) simulation using Python's Mersenne Twister, with a live chart |
| `src/desarreglos_lcg.py` | E | The same simulation using the LCG (a = 1103515245, c = 12345, m = 2^31 − 1, seed 42) |

`src/tablero.png` is the board image for the taxi game, taken from the screenshot in the essay (so it shows one pawn and the die).

### How to run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd src
python ks_test.py
python desarreglos_mersenne.py   # or desarreglos_lcg.py, taxista.py, urnas.py
```

Run the programs from inside `src/` so the taxi game can find `tablero.png`.

To check everything without a screen, `SDL_VIDEODRIVER=dummy python tools/headless_check.py 1500` drives the games with simulated clicks and prints the results.

### Reproducing the essay's results

| | Essay | Re-run |
|---|---|---|
| KS test, LCG | D = 0.0145, p = 0.0303 | D = 0.0145, p = 0.0303 (identical, the LCG is seeded) |
| KS test, Mersenne Twister | D = 0.0086, p = 0.4503 | D between 0.005 and 0.008, p between 0.52 and 0.94 over three runs (unseeded, so it changes each run) |
| LCG derangements, 1,500 rolls (0–6 matches) | 646, 527, 239, 62, 25, 0, 1 | 646, 527, 239, 62, 25, 0, 1 (identical) |
| Mersenne derangements, 1,500 rolls | 537, 538, 314, 82, 27, 0, 2 | 544, 535, 295, 89, 32, 0, 5 (one unseeded run) |
| Theory (!6 / 6! etc.) | 0.3681, 0.3667, 0.1875, 0.0556, 0.0208, 0, 0.0014 | — |

The only changes to the appendix code were fixing what the PDF had broken: long lines that had been wrapped, lost indentation, curly quotes, and accented letters.
