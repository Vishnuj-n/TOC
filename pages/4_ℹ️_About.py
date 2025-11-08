"""About and Help Page

Documentation, examples, and help for the NFA to DFA Visualizer.
"""

import streamlit as st

st.set_page_config(
    page_title="About & Help",
    page_icon="ℹ️",
    layout="wide"
)


def main():
    """About and help page."""
    
    st.title("ℹ️ About & Help")
    st.markdown("""
    Comprehensive documentation and examples for the NFA to DFA Visualizer.
    """)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Documentation", "💡 Examples", "❓ FAQ", "🔧 Technical"])
    
    # Tab 1: Documentation
    with tab1:
        st.header("📚 Documentation")
        
        st.markdown("""
        ## What is this tool?
        
        The **NFA to DFA Visualizer** is an interactive web application that converts 
        **Non-deterministic Finite Automata (NFA)** into **Deterministic Finite Automata (DFA)** 
        using the **Subset Construction Algorithm**.
        
        ### Features
        
        - ✅ **Multiple Input Methods**: Manual builder, JSON upload, or paste
        - ✅ **Visual Graphs**: Beautiful automata visualizations using Graphviz
        - ✅ **Step-by-Step Logs**: Detailed algorithm trace
        - ✅ **Validation**: Automatic NFA validation
        - ✅ **Export**: Download DFA as JSON
        - ✅ **Comparison**: Side-by-side NFA and DFA comparison
        
        ### How to Use
        
        #### Method 1: Manual Builder
        1. Go to **📝 Manual Builder**
        2. Enter states (comma-separated): `q0, q1, q2`
        3. Enter alphabet (comma-separated): `a, b`
        4. Select start and final states
        5. Define transitions for each state-symbol pair
        6. Click **Build NFA**
        7. Click **Convert to DFA** to see results
        
        #### Method 2: Import JSON
        1. Go to **📤 Import JSON**
        2. Upload a `.json` file or paste JSON directly
        3. Or load one of the provided examples
        4. Click **Save NFA**
        5. Click **Convert to DFA** to see results
        
        #### Method 3: Direct Conversion
        1. Load or build an NFA using any method
        2. Go to **🔄 Convert & Visualize**
        3. Click **Convert to DFA**
        4. View graphs, logs, and download results
        
        ### Understanding the Results
        
        After conversion, you'll see:
        
        - **NFA Graph**: Visual representation of your input NFA
        - **DFA Graph**: Visual representation of the converted DFA
        - **Comparison Graph**: Side-by-side view of both automata
        - **Algorithm Trace**: Step-by-step log of the conversion process
        - **Metrics**: State count comparison and complexity analysis
        - **JSON Output**: Complete DFA specification (downloadable)
        
        ### NFA vs DFA
        
        | Feature | NFA | DFA |
        |---------|-----|-----|
        | **Transitions** | Multiple per state-symbol pair | Exactly one per state-symbol pair |
        | **Acceptance** | Accept if ANY path leads to final state | Accept if THE path leads to final state |
        | **States** | Usually fewer | Can be exponentially more (worst case: 2^n) |
        | **Computation** | Slower (must track multiple states) | Faster (single state at a time) |
        | **Design** | Easier to design | Harder to design directly |
        """)
    
    # Tab 2: Examples
    with tab2:
        st.header("💡 Examples")
        
        st.markdown("### Example 1: Strings Containing 'aba'")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**NFA Specification:**")
            example1_nfa = {
                "states": ["q0", "q1", "q2", "q3"],
                "alphabet": ["a", "b"],
                "start_state": "q0",
                "final_states": ["q3"],
                "transitions": {
                    "q0": {
                        "a": ["q0", "q1"],
                        "b": ["q0"]
                    },
                    "q1": {
                        "b": ["q2"]
                    },
                    "q2": {
                        "a": ["q3"]
                    },
                    "q3": {
                        "a": ["q3"],
                        "b": ["q3"]
                    }
                }
            }
            st.json(example1_nfa)
        
        with col2:
            st.markdown("""
            **Description:**
            - Accepts strings containing the substring 'aba'
            - Non-deterministic at state q0 on input 'a'
            
            **Accepted Strings:**
            - `"aba"` ✅
            - `"aaba"` ✅
            - `"abababa"` ✅
            - `"bbbababb"` ✅
            
            **Rejected Strings:**
            - `"ab"` ❌
            - `"aab"` ❌
            - `"bbb"` ❌
            """)
        
        st.markdown("---")
        
        st.markdown("### Example 2: Binary Strings Ending with '01'")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**NFA Specification:**")
            example2_nfa = {
                "states": ["q0", "q1", "q2"],
                "alphabet": ["0", "1"],
                "start_state": "q0",
                "final_states": ["q2"],
                "transitions": {
                    "q0": {
                        "0": ["q0", "q1"],
                        "1": ["q0"]
                    },
                    "q1": {
                        "1": ["q2"]
                    },
                    "q2": {
                        "0": ["q1"],
                        "1": ["q0"]
                    }
                }
            }
            st.json(example2_nfa)
        
        with col2:
            st.markdown("""
            **Description:**
            - Accepts binary strings ending with '01'
            - Non-deterministic at state q0 on input '0'
            
            **Accepted Strings:**
            - `"01"` ✅
            - `"101"` ✅
            - `"1001"` ✅
            - `"00001"` ✅
            
            **Rejected Strings:**
            - `"0"` ❌
            - `"10"` ❌
            - `"111"` ❌
            """)
        
        st.markdown("---")
        
        st.markdown("### Example 3: Simple NFA (at least one 'a' followed by at least one 'b')")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**NFA Specification:**")
            example3_nfa = {
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
            st.json(example3_nfa)
        
        with col2:
            st.markdown("""
            **Description:**
            - Accepts strings with ≥1 'a' followed by ≥1 'b'
            - Non-deterministic at state q0 on input 'a'
            
            **Accepted Strings:**
            - `"aab"` ✅
            - `"aaabbb"` ✅
            - `"baaab"` ✅
            
            **Rejected Strings:**
            - `"aaa"` ❌
            - `"bbb"` ❌
            - `"ab"` ❌ (needs more symbols)
            """)
    
    # Tab 3: FAQ
    with tab3:
        st.header("❓ Frequently Asked Questions")
        
        with st.expander("❓ What is the difference between NFA and DFA?"):
            st.markdown("""
            - **NFA (Non-deterministic Finite Automaton)**: Can have multiple transitions 
              for the same state-symbol pair. Also supports epsilon (ε) transitions (though not in this tool).
            - **DFA (Deterministic Finite Automaton)**: Has exactly one transition for each 
              state-symbol pair. Easier to implement and more efficient to execute.
            """)
        
        with st.expander("❓ What is the Subset Construction Algorithm?"):
            st.markdown("""
            The **Subset Construction Algorithm** (also called **Powerset Construction**) converts 
            an NFA to an equivalent DFA by:
            
            1. Creating DFA states from sets of NFA states
            2. For each DFA state and input symbol, computing the set of reachable NFA states
            3. Marking DFA states as final if they contain any NFA final state
            
            **Time Complexity**: O(2^n × |Σ|) where n is the number of NFA states
            **Space Complexity**: O(2^n) in the worst case
            """)
        
        with st.expander("❓ Why does my DFA have more states than the NFA?"):
            st.markdown("""
            This is called **state explosion** and is normal! In the worst case, a DFA can have 
            2^n states where n is the number of NFA states. This happens because:
            
            - Each DFA state represents a **set** of NFA states
            - The number of possible sets is 2^n (powerset)
            - In practice, not all sets are reachable, so the DFA is usually smaller
            """)
        
        with st.expander("❓ Can I convert DFA back to NFA?"):
            st.markdown("""
            Yes! Every DFA is already a valid NFA (just a special case where each state-symbol 
            pair has exactly one transition). So no conversion is needed - a DFA can be directly 
            used as an NFA.
            """)
        
        with st.expander("❓ Does this tool support epsilon (ε) transitions?"):
            st.markdown("""
            Currently, **no**. This tool focuses on NFAs without epsilon transitions. 
            Supporting epsilon transitions would require an additional epsilon-closure step 
            in the algorithm.
            """)
        
        with st.expander("❓ What happens if I don't define all transitions?"):
            st.markdown("""
            Missing transitions are treated as **implicit transitions to a dead state (∅)**. 
            The algorithm will automatically handle these cases. In the DFA, you may see an 
            empty set state (∅) representing the dead state.
            """)
        
        with st.expander("❓ How do I download my NFA or DFA?"):
            st.markdown("""
            1. For **NFA**: In the Manual Builder, click "Download JSON" after building
            2. For **DFA**: In the Convert & Visualize page, click "Download DFA JSON" after conversion
            
            The JSON files can be re-imported later using the Import JSON page.
            """)
        
        with st.expander("❓ Why isn't the graph showing?"):
            st.markdown("""
            Graph visualization requires **Graphviz** to be installed on your system:
            
            1. Download from: https://graphviz.org/download/
            2. Install Graphviz
            3. Make sure it's in your system PATH
            4. Restart the Streamlit app
            
            You can still use all other features without graphs.
            """)
    
    # Tab 4: Technical
    with tab4:
        st.header("🔧 Technical Details")
        
        st.markdown("""
        ### Technology Stack
        
        - **Frontend**: Streamlit
        - **Backend**: Python 3.8+
        - **Visualization**: Graphviz
        - **Algorithm**: Subset Construction (Powerset Construction)
        
        ### JSON Format Specification
        
        #### NFA/DFA JSON Structure
        
        ```json
        {
          "states": ["q0", "q1", "q2"],           // Array of state names (strings)
          "alphabet": ["a", "b"],                  // Array of input symbols (strings)
          "start_state": "q0",                     // Single start state (string)
          "final_states": ["q2"],                  // Array of final states (strings)
          "transitions": {                         // Object mapping states to transitions
            "q0": {                                // State name
              "a": ["q0", "q1"],                   // Symbol -> array of destination states
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
        ```
        
        #### Validation Rules
        
        1. All fields are **required**: `states`, `alphabet`, `start_state`, `final_states`, `transitions`
        2. `states` must be a non-empty array of unique strings
        3. `alphabet` must be a non-empty array of unique strings
        4. `start_state` must be in `states`
        5. All items in `final_states` must be in `states`
        6. Transition keys must be in `states`
        7. Transition symbols must be in `alphabet`
        8. Destination states must be in `states`
        9. Destination states must be arrays (even for single states)
        
        ### Algorithm Pseudocode
        
        ```
        function SubsetConstruction(NFA):
            DFA_states = {}
            queue = [epsilon_closure({NFA.start_state})]
            
            while queue is not empty:
                current_set = queue.pop()
                
                for each symbol in NFA.alphabet:
                    next_set = {}
                    for each state in current_set:
                        if transition(state, symbol) exists:
                            next_set.add(destination states)
                    
                    if next_set not in DFA_states:
                        DFA_states.add(next_set)
                        queue.add(next_set)
                    
                    DFA.transitions[current_set][symbol] = next_set
            
            for each state_set in DFA_states:
                if state_set contains any NFA final state:
                    DFA.final_states.add(state_set)
            
            return DFA
        ```
        
        ### Performance Considerations
        
        - **Best Case**: O(n) states (when NFA is already deterministic)
        - **Average Case**: O(n × log n) states
        - **Worst Case**: O(2^n) states (full powerset)
        
        **Memory Usage**: Proportional to number of DFA states
        
        ### Version History
        
        - **v3.0**: Multi-page architecture, form-based builder
        - **v2.0**: Added graph visualization
        - **v1.0**: Initial release with JSON import
        
        ### Source Code
        
        The core algorithm is implemented in `nfa_to_dfa.py`:
        
        - `convert_nfa_to_dfa()`: Main conversion function
        - `validate_nfa()`: NFA validation function
        
        Graph visualization in `graph_visualizer.py`:
        
        - `get_graph_svg()`: Generate automaton graph
        - `compare_graphs()`: Side-by-side comparison
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p><strong>NFA → DFA Visualizer v3.0</strong></p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔗 Quick Links")
        
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("main.py")
        if st.button("📝 Manual Builder", use_container_width=True):
            st.switch_page("pages/1_📝_Manual_Builder.py")
        if st.button("📤 Import JSON", use_container_width=True):
            st.switch_page("pages/2_📤_Import_JSON.py")
        if st.button("🔄 Convert & Visualize", use_container_width=True):
            st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
        
        st.markdown("---")
        
        st.header("📚 Resources")
        st.markdown("""
        - [Automata Theory](https://en.wikipedia.org/wiki/Automata_theory)
        - [Subset Construction](https://en.wikipedia.org/wiki/Powerset_construction)
        - [Graphviz](https://graphviz.org/)
        - [Streamlit Docs](https://docs.streamlit.io/)
        """)


if __name__ == "__main__":
    main()
