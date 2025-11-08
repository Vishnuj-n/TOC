"""NFA to DFA Visualizer - Landing Page

This is the main entry point for the Automaton Visualizer web application.
Navigate to different pages to build, import, and convert NFAs to DFAs.

Run with: streamlit run main.py
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="NFA → DFA Visualizer",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main landing page."""
    
    # Hero Section
    st.title("🔄 NFA → DFA Visualizer")
    st.markdown("""
    <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
        <h2 style='margin: 0; color: white;'>Transform Non-deterministic Finite Automata into Deterministic Finite Automata</h2>
        <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
            Using the powerful <strong>Subset Construction Algorithm</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Guide
    st.header("🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📝 Manual Builder
        **Best for learning & experimenting**
        
        Build your NFA step-by-step using an intuitive form:
        - Add states and alphabet symbols
        - Define transitions interactively
        - Validate as you build
        - Visual preview
        """)
        if st.button("📝 Start Manual Builder →", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📝_Manual_Builder.py")
    
    with col2:
        st.markdown("""
        ### 📤 Import JSON
        **Best for existing NFAs**
        
        Upload or paste your NFA in JSON format:
        - Upload .json file
        - Paste JSON directly
        - Auto-validation
        - Quick import
        """)
        if st.button("📤 Import JSON →", use_container_width=True):
            st.switch_page("pages/2_📤_Import_JSON.py")
    
    with col3:
        st.markdown("""
        ### 🔄 Convert & Visualize
        **View conversion results**
        
        See your NFA transformed to DFA:
        - Interactive graphs
        - Step-by-step algorithm trace
        - Side-by-side comparison
        - Download results
        """)
        if st.button("🔄 Convert & Visualize →", use_container_width=True):
            st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
    
    st.markdown("---")
    
    # Features Section
    st.header("✨ Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🎯 Core Features
        - ✅ **Subset Construction Algorithm** - Industry-standard conversion
        - ✅ **Multiple Input Methods** - Manual builder, JSON upload, paste
        - ✅ **Visual Graphs** - Beautiful automata visualizations
        - ✅ **Detailed Logging** - Step-by-step algorithm trace
        - ✅ **Validation** - Automatic NFA validation
        """)
    
    with col2:
        st.markdown("""
        #### 🛠️ Additional Features
        - ✅ **Side-by-Side Comparison** - Compare NFA and DFA
        - ✅ **Export Results** - Download DFA as JSON
        - ✅ **State Metrics** - Analyze state complexity
        - ✅ **Interactive UI** - Clean, modern interface
        - ✅ **Examples Included** - Learn from sample NFAs
        """)
    
    st.markdown("---")
    
    # Example Section
    st.header("📖 Example NFA")
    
    st.markdown("""
    Here's a simple NFA that accepts strings containing at least one 'a' followed by at least one 'b':
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        example_nfa = {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q2"],
            "transitions": {
                "q0": {
                    "a": ["q0", "q1"],
                    "b": ["q0"]
                },
                "q1": {
                    "b": ["q2"]
                },
                "q2": {
                    "a": ["q2"],
                    "b": ["q2"]
                }
            }
        }
        st.json(example_nfa)
    
    with col2:
        st.markdown("""
        **Language Description:**
        - Accepts: Strings with ≥1 'a' followed by ≥1 'b'
        - Examples: `"aab"`, `"aaabbb"`, `"baaab"`
        - Rejects: `"aaa"`, `"bbb"`, `"ab"` (need more symbols)
        
        **Characteristics:**
        - 3 states
        - Non-deterministic (state q0 has multiple 'a' transitions)
        - Multiple paths possible
        
        **Try it yourself:**
        Copy this JSON and paste it in the Import JSON page!
        """)
    
    st.markdown("---")
    
    # Algorithm Overview
    st.header("🧮 Subset Construction Algorithm")
    
    with st.expander("📚 How It Works", expanded=False):
        st.markdown("""
        The **Subset Construction Algorithm** converts any NFA to an equivalent DFA:
        
        1. **Initialize**: Start with the NFA's initial state as a DFA state
        2. **Process Queue**: For each DFA state (which represents a set of NFA states):
           - For each input symbol in the alphabet:
             - Compute all possible NFA states reachable via that symbol
             - Create a new DFA state representing this set (if not already exists)
             - Add the transition to the DFA
        3. **Mark Final States**: Any DFA state containing an NFA final state becomes a final state
        4. **Complete**: Continue until all DFA states are processed
        
        **Time Complexity**: O(2^n) in worst case, where n is the number of NFA states
        
        **Result**: A DFA that accepts the exact same language as the original NFA
        """)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p style='margin: 0;'><strong>NFA → DFA Visualizer v3.0</strong></p>
        <p style='margin: 0.5rem 0;'>Built with Streamlit • Powered by Subset Construction Algorithm</p>
        <p style='margin: 0;'>💡 Tip: NFAs can have multiple transitions per input, DFAs have exactly one</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        st.markdown("""
        Use the pages above or click these links:
        """)
        
        if st.button("📝 Manual Builder", use_container_width=True):
            st.switch_page("pages/1_📝_Manual_Builder.py")
        if st.button("📤 Import JSON", use_container_width=True):
            st.switch_page("pages/2_📤_Import_JSON.py")
        if st.button("🔄 Convert & Visualize", use_container_width=True):
            st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
        if st.button("ℹ️ About & Help", use_container_width=True):
            st.switch_page("pages/4_ℹ️_About.py")
        
        st.markdown("---")
        
        # Session State Info
        if 'nfa_data' in st.session_state:
            st.success("✅ NFA Loaded")
            nfa = st.session_state['nfa_data']
            st.metric("States", len(nfa.get('states', [])))
            st.metric("Alphabet Size", len(nfa.get('alphabet', [])))
            if st.button("🗑️ Clear NFA", use_container_width=True):
                del st.session_state['nfa_data']
                if 'dfa_data' in st.session_state:
                    del st.session_state['dfa_data']
                if 'conversion_logs' in st.session_state:
                    del st.session_state['conversion_logs']
                st.rerun()
        else:
            st.info("ℹ️ No NFA loaded yet")


if __name__ == "__main__":
    main()
