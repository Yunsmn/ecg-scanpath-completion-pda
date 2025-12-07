# ECG Scanpath PDA: A Formal Language Model for Hierarchical Clinical Gaze Behavior

This repository contains the code, grammars, and evaluation materials for the paper:

**“Formalizing ECG Scanpaths as a Context-Free Language:  
A Pushdown Automaton for Hierarchical Visual Reasoning in Clinical Interpretation.”**

The project introduces a **Pushdown Automaton (PDA)** capable of parsing and validating **expert ECG scanpaths** recorded through eye-tracking. Unlike traditional statistical gaze models (Markov chains, n-grams, HMMs), our approach captures **nested clinical reasoning patterns**, ensures **guideline consistency**, and provides **transparent, auditable decision traces**.

---

##  Overview

Clinical interpretation of the ECG involves structured and often nested visual routines:  
global rhythm assessment → lead-specific inspection → morphological analysis → global verification.

Traditional scanpath models cannot express these hierarchical dependencies.

This project:

- Defines a **context-free grammar** for ECG scanpaths  
- Implements a **deterministic PDA** that validates or rejects gaze sequences  
- Provides tools for:
  - parsing real scanpaths  
  - generating guideline-consistent completions  
  - detecting missing clinical reasoning steps  
- Includes experiments comparing PDA modeling with classical strategies (Markov, HMM)

---

##  Features

- **Formal grammar** representing expert ECG guidelines  
- **Stack-based PDA engine** (Python)  
- **Scanpath parser** with step-by-step traces  
- **Error detection**: missing repolarization check, skip of global overview, etc.  
- **Completion engine**: fills incomplete student / novice scanpaths to expert-consistent ones  
- **Benchmarks** against:
  - First- and higher-order Markov models  
  - Hidden Markov Models  
  - Statistical scanpath metrics  

---

## Formal Grammar (Excerpt)

We define ECG scanpaths as a **context-free language** over AOIs such as  
`{II, V1, V2, V3, V4, V5, V6, P, QRS, ST, T, QT}`.


