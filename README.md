# 🧬 DNA Pattern Matching using DFA & Aho-Corasick

**Theory of Computation Project** | Slot: C1+TC1 | Faculty: Dr Amutha S

## Quick Links
- [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Testing](#-testing) • [Architecture](#-architecture)

---

## 📋 Overview

Fast, efficient DNA pattern matching using **Deterministic Finite Automaton (DFA)** and **Aho-Corasick Algorithm**. Built with a web-based frontend for easy visualization of pattern matching, motif analysis, and performance benchmarking.

### ⚡ Why This Project?
- **O(n) Linear Time Complexity** - No backtracking, process each character once
- **Real-World Applications** - Gene discovery, restriction mapping, disease detection
- **Educational** - Learn automata theory, string algorithms, and complexity analysis
- **Production-Ready** - Fully tested with 76+ test cases

---

## 🚀 Features

| Feature | Description | Algorithm |
|---------|-------------|-----------|
| **Pattern Search** | Single-pattern matching | DFA (KMP-based) |
| **Motif Analysis** | Search known DNA motifs | DFA |
| **Multi-Pattern** | Search multiple patterns simultaneously | Aho-Corasick |
| **Benchmarks** | Performance testing & O(n) verification | Custom analyzer |
| **Web Interface** | Interactive Streamlit dashboard | Frontend |
| **Validation** | DNA sequence validation (ATCG + N) | SequenceHandler |

---

## ⚙️ Tech Stack

| Layer | Tech |
|-------|------|
| **Frontend** | Streamlit, Plotly, Matplotlib |
| **Backend** | Python 3.9+, BioPython |
| **Testing** | Pytest (76+ tests), Coverage analysis |
| **Algorithms** | Custom DFA, Aho-Corasick (from scratch) |

---

## 📁 Project Structure

```
├── src/
│   ├── dfa_engine.py              # DFA pattern matching (KMP-based)
│   ├── aho_corasick.py            # Multi-pattern matching
│   ├── sequence_handler.py        # DNA validation & processing
│   ├── motif_database.py          # Biological motif database
│   ├── benchmark.py               # Performance testing
│   └── performance_analyzer.py    # Complexity verification
│
├── app/
│   └── app.py                     # Streamlit web interface (5 pages)
│
├── tests/                         # 76+ test cases ✓
│   ├── test_dfa_engine.py        # DFA tests
│   ├── test_sequence_handler.py  # Validation tests
│   ├── test_motif_database.py    # Motif tests
│   └── test_benchmark.py         # Performance tests
│
└── requirements.txt
```

---

## 🎯 Core Algorithms

### 1️⃣ DFA (Deterministic Finite Automaton)
- **Best for:** Single pattern matching
- **Time:** O(n) | **Space:** O(m)
- **Key:** KMP failure function for smart state transitions
- **No backtracking** - each character processed exactly once

### 2️⃣ Aho-Corasick Algorithm
- **Best for:** Multiple patterns simultaneously
- **Time:** O(n + m + z) | **Space:** O(m×k)
- **Key:** Trie with failure links
- **Why:** Find all motifs in one pass

### 3️⃣ Performance Comparison

| Algorithm | Single Pattern | Multiple Patterns | Space | Backtrack |
|-----------|---|---|---|---|
| **Naive** | O(n×m) | O(n×k×m) | O(1) | Yes |
| **DFA** | O(n) | O(n×k) | O(m) | No ✓ |
| **Aho-Corasick** | O(n) | O(n+z) | O(m) | No ✓ |

---

## 🏃 Getting Started

### Prerequisites
```bash
Python 3.9+
pip
Git
```

### Installation
```bash
# Clone repository
git clone <repo-url>
cd DNA-DFA-using-python

# Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Tests
```bash
# All tests (76+)
pytest tests/ -v

# Specific test file
pytest tests/test_dfa_engine.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

### Launch Web App
```bash
cd app
streamlit run app.py
# Opens: http://localhost:8501
```

---

## 📖 Usage

### Example 1: Find Pattern
```python
from src.dfa_engine import DFAStateMachine

# Create DFA for pattern
dfa = DFAStateMachine("ACG")

# Find matches in sequence
matches = dfa.match("AACGTACG")
# Output: [{'position': 1, 'sequence': 'ACG', 'score': 1.0}, ...]
```

### Example 2: Motif Analysis
```python
from src.motif_database import MotifDatabase
from src.dfa_engine import DFAStateMachine

# Get TATA box motif
motif = MotifDatabase.PROMOTER_MOTIFS['TATA_BOX']['sequence']

# Search in sequence
dfa = DFAStateMachine(motif)
results = dfa.match("ATGCTATAAACGATGC")
# Found TATAAA at position 5
```

### Example 3: Validate Sequence
```python
from src.sequence_handler import SequenceHandler

# Check if valid
is_valid = SequenceHandler.validate_sequence("ATGC")  # True
is_valid = SequenceHandler.validate_sequence("ATGCX")  # False
```

---

## 🧪 Testing

### Test Coverage

| Module | Tests | Coverage |
|--------|-------|----------|
| [test_dfa_engine.py](tests/test_dfa_engine.py) | 17 tests | DFA matching, failure function |
| [test_sequence_handler.py](tests/test_sequence_handler.py) | 21 tests | Validation, FASTA loading |
| [test_motif_database.py](tests/test_motif_database.py) | 13 tests | Motif retrieval |
| [test_benchmark.py](tests/test_benchmark.py) | 25 tests | Performance testing |
| **Total** | **76+ tests** | **✓ All passing** |

### Sample Test Output
```bash
pytest tests/ -v
========================= 76 passed in 2.34s =========================
✓ DFA pattern matching tests
✓ Sequence validation tests  
✓ Motif database tests
✓ Benchmark performance tests
```

---

## 📊 Complexity Analysis

### DFA: O(n + m)
```
Build failure function: O(m)
Scan text: O(n) - each char processed once
Total: O(n + m) ✓
```

### Aho-Corasick: O(n + m + z)
```
Trie construction: O(m)
Text scanning: O(n)
Output matches: O(z)
Total: O(n + m + z)
```

### Space Complexity
| Algorithm | Space |
|-----------|-------|
| DFA | O(m) |
| Aho-Corasick | O(m × k) |
| Naive | O(1) |

---

## 🎓 Learning Outcomes

After this project:
- ✅ Understand **DFA construction and execution**
- ✅ Master **KMP and Aho-Corasick algorithms**
- ✅ Work with **trie data structures**
- ✅ Analyze **O(n) vs O(n²) complexity**
- ✅ Apply **automata theory to real problems**
- ✅ Write **production-quality code with tests**

---

## 📝 References

**Algorithms**
- [KMP Algorithm](https://en.wikipedia.org/wiki/Knuth%E2%80%93Morris%E2%80%93Pratt_algorithm)
- [Aho-Corasick](https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm)
- [DFA](https://en.wikipedia.org/wiki/Deterministic_finite_automaton)

**Tools**
- [BioPython](https://biopython.org/)
- [Streamlit](https://streamlit.io/)
- [Pytest](https://pytest.org/)

---

## 👥 Team

| ID | Name |
|---|---|
| 24BAI1040 | Tejvir Singh |
| 24BAI1049 | Mouli Gupta |
| 24BAI1629 | Chitwan Singh |
| 24BAI1631 | Sreeansh Dash |

---

**Last Updated:** January 2026 | **Python:** 3.9+ | **License:** MIT

