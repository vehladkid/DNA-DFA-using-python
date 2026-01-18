import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.dfa_engine import DFAStateMachine
from src.sequence_handler import SequenceHandler
from src.motif_database import MotifDatabase
from src.performance_analyzer import PerformanceAnalyzer

# Set page config
st.set_page_config(page_title="DNA Pattern Matcher", layout="wide", initial_sidebar_state="expanded")

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("🧬 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Pattern Search", "Motif Analysis", "Benchmarks", "About"]
)

# ---------------- Pages ----------------
if page == "Home":
    st.title("🧬 DNA Pattern Matcher")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Algorithm", "DFA")
    with col2:
        st.metric("Time Complexity", "O(n)")
    with col3:
        st.metric("Space Complexity", "O(m)")
    
    st.write("""
    This application implements a **Deterministic Finite Automaton (DFA)** for efficient DNA pattern matching.
    
    ### Key Features
    - ⚡ **O(n) Time Complexity** - Linear time pattern matching
    - 🎯 **Exact Matching** - Find all occurrences of DNA patterns
    - 🧬 **Motif Database** - Search known biological motifs (TATA box, restriction sites, etc.)
    - 📊 **Performance Analytics** - Benchmark pattern matching performance
    - ✅ **Sequence Validation** - Automatic DNA sequence validation
    
    ### How It Works
    The DFA algorithm precomputes a state machine based on the pattern, allowing it to match patterns
    in linear time O(n) with respect to the text length. This is significantly faster than naive approaches
    for long DNA sequences.
    
    ### Supported Characters
    - **A, T, C, G** - Standard DNA bases
    - **N** - Wildcard (matches any base)
    """)
    
    st.divider()
    st.subheader("Quick Start")
    st.write("1. Go to **Pattern Search** to find custom patterns")
    st.write("2. Use **Motif Analysis** for known biological sequences")
    st.write("3. Run **Benchmarks** to analyze performance")
    st.write("4. Check **About** for more details")

elif page == "Pattern Search":
    st.title("🔍 Pattern Search")

    col1, col2 = st.columns(2)
    
    with col1:
        dna = st.text_area("Enter DNA Sequence", "AACGTACG", height=150)
        pattern = st.text_input("Enter Pattern (ATCG)", "ACG")

    with col2:
        st.info("💡 Tips:\n- Use ATCG characters only\n- N is wildcard for any base")

    if st.button("🔎 Search Pattern", use_container_width=True):
        # Validate sequence and pattern
        if not SequenceHandler.validate_sequence(dna):
            st.error("❌ Invalid DNA sequence. Use only ATCG and N")
        elif not SequenceHandler.validate_sequence(pattern):
            st.error("❌ Invalid pattern. Use only ATCG and N")
        elif len(pattern) == 0:
            st.error("❌ Pattern cannot be empty")
        else:
            try:
                # Use DFA engine from backend
                dfa = DFAStateMachine(pattern)
                results = dfa.match(dna)

                if results:
                    df = pd.DataFrame(results)
                    st.success(f"✓ Found {len(results)} match(es)")
                    st.dataframe(df, use_container_width=True)
                    
                    # Visualize matches
                    st.subheader("Match Visualization")
                    seq_display = dna.upper()
                    match_positions = [r['position'] for r in results]
                    pattern_len = len(pattern)
                    
                    for i, pos in enumerate(match_positions):
                        st.write(f"Match {i+1}: Position {pos}")
                        before = seq_display[:pos]
                        match = seq_display[pos:pos+pattern_len]
                        after = seq_display[pos+pattern_len:]
                        st.code(f"{before}[{match}]{after}", language="text")
                else:
                    st.warning("⚠️ No matches found")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif page == "Motif Analysis":
    st.title("🧬 Motif Analysis")

    # Get all available motifs from database
    db = MotifDatabase()
    all_motifs = {}
    
    # Combine all motif categories
    if hasattr(db, 'PROMOTER_MOTIFS'):
        all_motifs.update(db.PROMOTER_MOTIFS)
    if hasattr(db, 'RESTRICTION_SITES'):
        all_motifs.update(db.RESTRICTION_SITES)
    if hasattr(db, 'BINDING_SITES'):
        all_motifs.update(db.BINDING_SITES)
    
    col1, col2 = st.columns(2)
    
    with col1:
        motif_name = st.selectbox("Choose Motif", list(all_motifs.keys()))
        
        if motif_name in all_motifs:
            motif_info = all_motifs[motif_name]
            st.info(f"**Sequence:** {motif_info.get('sequence', 'N/A')}\n\n"
                   f"**Function:** {motif_info.get('function', 'N/A')}\n\n"
                   f"**Description:** {motif_info.get('description', 'N/A')}")
    
    with col2:
        dna = st.text_area("Enter DNA Sequence", height=150)
    
    if st.button("🔎 Search Motif", use_container_width=True):
        if not dna:
            st.error("❌ Please enter a DNA sequence")
        else:
            motif_sequence = all_motifs[motif_name]['sequence']
            
            if not SequenceHandler.validate_sequence(dna):
                st.error("❌ Invalid DNA sequence. Use only ATCG and N")
            else:
                try:
                    dfa = DFAStateMachine(motif_sequence)
                    matches = dfa.match(dna)
                    
                    if matches:
                        df = pd.DataFrame(matches)
                        st.success(f"✓ Found {len(matches)} motif match(es)")
                        st.dataframe(df, use_container_width=True)
                        
                        # Show match context
                        st.subheader("Match Details")
                        for i, match in enumerate(matches):
                            st.write(f"**Match {i+1}:** {match['sequence']} at position {match['position']}")
                    else:
                        st.info(f"ℹ️ No matches found for motif '{motif_name}' ({motif_sequence})")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif page == "Benchmarks":
    st.title("⚡ Performance Benchmarks")

    col1, col2 = st.columns(2)
    
    with col1:
        test_sizes = st.multiselect(
            "Select sequence sizes to benchmark",
            [100, 500, 1000, 5000, 10000],
            default=[100, 500, 1000, 5000]
        )
    
    with col2:
        pattern_input = st.text_input("Enter pattern for benchmark", "ACG")
    
    if st.button("▶️ Run Benchmark", use_container_width=True):
        if not SequenceHandler.validate_sequence(pattern_input):
            st.error("❌ Invalid pattern")
        else:
            with st.spinner("Running benchmarks..."):
                sizes = sorted(test_sizes)
                times = []
                
                progress_bar = st.progress(0)
                
                for idx, size in enumerate(sizes):
                    # Generate DNA sequence
                    dna = "ACGT" * (size // 4)
                    
                    # Run DFA matching
                    dfa = DFAStateMachine(pattern_input)
                    start = time.time()
                    dfa.match(dna)
                    elapsed = time.time() - start
                    times.append(elapsed * 1000)  # Convert to milliseconds
                    
                    progress_bar.progress((idx + 1) / len(sizes))
                
                # Display results
                df = pd.DataFrame({
                    "Sequence Length (bp)": sizes,
                    "Time (milliseconds)": times,
                    "Throughput (bp/ms)": [sizes[i] / times[i] if times[i] > 0 else 0 for i in range(len(sizes))]
                })
                
                st.success("✓ Benchmark complete")
                st.dataframe(df, use_container_width=True)
                
                # Plot results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Execution Time")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.plot(sizes, times, marker='o', linewidth=2, markersize=8)
                    ax.set_xlabel("Sequence Length (bp)")
                    ax.set_ylabel("Time (ms)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("Throughput (bp/ms)")
                    fig, ax = plt.subplots(figsize=(10, 5))
                    throughput = [sizes[i] / times[i] if times[i] > 0 else 0 for i in range(len(sizes))]
                    ax.plot(sizes, throughput, marker='s', linewidth=2, markersize=8, color='green')
                    ax.set_xlabel("Sequence Length (bp)")
                    ax.set_ylabel("Throughput (bp/ms)")
                    ax.grid(True, alpha=0.3)
                    st.pyplot(fig)

elif page == "About":
    st.title("ℹ️ About This Project")
    
    st.subheader("🔬 DNA Pattern Matching using DFA")
    st.write("""
    This project demonstrates the application of the Deterministic Finite Automaton (DFA) algorithm
    for efficient DNA sequence pattern matching, a fundamental task in bioinformatics.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Algorithm Details")
        st.write("""
        - **Type:** Pattern Matching
        - **Approach:** Deterministic Finite Automaton
        - **Time Complexity:** O(n + m)
        - **Space Complexity:** O(k) where k = alphabet size
        - **Worst Case:** No backtracking required
        """)
    
    with col2:
        st.subheader("Technology Stack")
        st.write("""
        - **Language:** Python 3.8+
        - **Frontend:** Streamlit
        - **Pattern Matching:** Custom DFA Engine
        - **Sequence Processing:** BioPython
        - **Testing:** Pytest
        - **Analytics:** Pandas, Matplotlib
        """)
    
    st.divider()
    
    st.subheader("Project Structure")
    st.write("""
    ```
    src/
    ├── dfa_engine.py          # Core DFA implementation
    ├── sequence_handler.py    # DNA sequence validation & processing
    ├── motif_database.py      # Known DNA motifs (promoters, restriction sites)
    ├── aho_corasick.py        # Multi-pattern matching
    ├── benchmark.py           # Performance testing
    ├── performance_analyzer.py # Analytics
    
    app/
    └── app.py                 # Streamlit frontend
    
    tests/                     # Unit tests for all modules
    ```
    """)
    
    st.divider()
    
    st.subheader("Key Modules")
    
    tabs = st.tabs(["DFA Engine", "Sequence Handler", "Motif Database"])
    
    with tabs[0]:
        st.write("""
        **DFAStateMachine** - Core pattern matching engine
        - Builds efficient state machine from DNA pattern
        - Supports wildcards (N)
        - Returns match positions and score
        """)
    
    with tabs[1]:
        st.write("""
        **SequenceHandler** - Utility functions
        - Validates DNA sequences
        - Loads FASTA files
        - Processes large sequences efficiently
        """)
    
    with tabs[2]:
        st.write("""
        **MotifDatabase** - Biological reference data
        - Promoter motifs (TATA box, Pribnow box, Kozak sequence)
        - Restriction enzyme sites
        - Transcription factor binding sites
        """)
