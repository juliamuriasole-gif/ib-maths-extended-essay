# Comparing the LCG and Mersenne Twister algorithms in educational simulations

My IB Diploma Extended Essay in Mathematics (December 2024, 2,687 words, written in Spanish). The full essay is in [extended-essay.pdf](extended-essay.pdf).

**Original title:** Comparativa de los algoritmos LGC y Mersenne Twister aplicados a simulaciones educativas

## Research question

How do the statistical properties of the Linear Congruential Generator (LCG) and the Mersenne Twister affect the accuracy and efficiency of simulations based on educational activities?

## Abstract

Computers cannot produce true randomness, so they use deterministic algorithms called pseudorandom number generators. This essay compares two of them, the LCG and the Mersenne Twister, and uses them to build digital simulations of activities from the Varga Box, a teaching kit for probability and combinatorics created by the Hungarian mathematician Tamás Varga.

After two warm-up simulations (the taxi-driver walk and the urn method), the essay focuses on the derangement problem. It proves the derangement formula by induction, works out the probabilities of partial derangements for n = 6, and simulates the game in Pygame with each generator. A Kolmogorov-Smirnov test and the simulation results show that the Mersenne Twister matches the theoretical probabilities much more closely. The LCG has a larger error but is accurate enough for classroom use, and its simpler structure lets students explore the limits of pseudorandom generators by changing its parameters.

## Stack

- Python and Pygame for the simulations (code in the appendices)
- Kolmogorov-Smirnov test for checking the output distributions
- LaTeX for the write-up

## What I learned

- How pseudorandom number generators work and where they fall short
- Writing a proof by induction and applying it to a real problem
- Testing a generator statistically instead of trusting it
- Turning mathematics into an interactive tool that students can use
