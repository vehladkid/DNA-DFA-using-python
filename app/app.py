import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("🧬 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Pattern Search", "Motif Analysis", "Benchmarks", "About"]
)

# ---------------- DFA Algorithm ----------------
class DFAMatcher:
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.build_dfa()

    def build_dfa(self):
        alphabet = ['A', 'C', 'G', 'T']
        self.dfa = [{} for _ in range(self.m + 1)]

        for state in range(self.m + 1):
            for char in alphabet:
                k = min(self.m, state + 1)
                while k > 0:
                    if self.pattern[:k] == (self.pattern[:state] + char)[-k:]:
                        break
                    k -= 1
                self.dfa[state][char] = k

    def match(self, text):
        state = 0
        matches = []
        for i, char in enumerate(text):
            state = self.dfa[state].get(char, 0)
            if state == self.m:
                matches.append(i - self.m + 1)
        return matches

# ---------------- Pages ----------------
if page == "Home":
    st.title("🧬 DNA Pattern Matcher")
    st.write("""
    This app finds DNA patterns using a **Deterministic Finite Automaton (DFA)**.

    ### Features
    - O(n) time pattern matching
    - Motif analysis
    - Benchmark comparison
    """)

elif page == "Pattern Search":
    st.title("🔍 Pattern Search")

    dna = st.text_area("Enter DNA Sequence", "AACGTACG")
    pattern = st.text_input("Enter Pattern", "ACG")

    if st.button("Search"):
        matcher = DFAMatcher(pattern)
        results = matcher.match(dna)

        if results:
            df = pd.DataFrame({
                "Position": results,
                "Pattern": [pattern] * len(results)
            })
            st.success(f"Found {len(results)} match(es)")
            st.table(df)
        else:
            st.warning("No matches found")

elif page == "Motif Analysis":
    st.title("🧬 Motif Analysis")

    motifs = {
        "TATA_BOX": "TATAAA",
        "EcoRI": "GAATTC"
    }

    motif = st.selectbox("Choose Motif", list(motifs.keys()))
    dna = st.text_area("Enter DNA Sequence")

    if st.button("Search Motif"):
        matcher = DFAMatcher(motifs[motif])
        matches = matcher.match(dna)
        st.write("Motif pattern:", motifs[motif])
        st.write("Matches found at positions:", matches)

elif page == "Benchmarks":
    st.title("⚡ Benchmarks")

    if st.button("Run Benchmark"):
        sizes = [100, 500, 1000, 5000]
        times = []

        for size in sizes:
            dna = "ACGT" * (size // 4)
            matcher = DFAMatcher("ACG")

            start = time.time()
            matcher.match(dna)
            times.append(time.time() - start)

        df = pd.DataFrame({
            "Text Size": sizes,
            "DFA Time (seconds)": times
        })

        st.table(df)

        plt.plot(sizes, times)
        plt.xlabel("DNA Length")
        plt.ylabel("Time (s)")
        st.pyplot(plt)

elif page == "About":
    st.title("ℹ️ About")
    st.write("""
    **DNA Pattern Matcher**

    - Algorithm: Deterministic Finite Automaton (DFA)
    - Time Complexity: O(n)
    - Tech Stack: Python, Streamlit
    - Academic Bioinformatics Project
    """)
