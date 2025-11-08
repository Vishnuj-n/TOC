"""Import JSON Page

Upload or paste NFA JSON files.
"""

import streamlit as st
import json
from nfa_to_dfa import validate_nfa

st.set_page_config(
    page_title="Import NFA JSON",
    page_icon="📤",
    layout="wide"
)


def load_json_from_text(text: str):
    """Parse JSON text into a dictionary."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"JSON parsing error: {e}"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def main():
    """Import JSON page."""
    
    st.title("📤 Import NFA JSON")
    st.markdown("""
    Import your NFA by uploading a JSON file or pasting JSON directly.
    The NFA will be automatically validated.
    """)
    
    # Tabs for different import methods
    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "📋 Paste JSON", "📚 Load Example"])
    
    nfa_data = None
    source = None
    
    # Tab 1: Upload File
    with tab1:
        st.markdown("### Upload NFA JSON File")
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=["json"],
            help="Select a .json file containing your NFA specification"
        )
        
        if uploaded_file is not None:
            try:
                nfa_data = json.load(uploaded_file)
                source = f"File: {uploaded_file.name}"
                st.success(f"✅ File loaded: {uploaded_file.name}")
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON file: {e}")
            except Exception as e:
                st.error(f"❌ Failed to read file: {e}")
    
    # Tab 2: Paste JSON
    with tab2:
        st.markdown("### Paste NFA JSON")
        
        json_text = st.text_area(
            "Paste your NFA JSON here",
            height=400,
            placeholder='''{
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
}''',
            help="Paste your NFA in JSON format"
        )
        
        if json_text.strip():
            result = load_json_from_text(json_text)
            if isinstance(result, tuple):
                nfa_data, error_msg = result
                st.error(f"❌ {error_msg}")
            else:
                nfa_data = result
                source = "Pasted JSON"
                st.success("✅ JSON parsed successfully")
    
    # Tab 3: Load Example
    with tab3:
        st.markdown("### Load Example NFA")
        
        examples = {
            "Simple NFA (a*b+)": {
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
            },
            "Binary String Ending with 01": {
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
            },
            "Contains 'aba' Substring": {
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
        }
        
        selected_example = st.selectbox(
            "Choose an example NFA",
            options=list(examples.keys()),
            help="Select a pre-built example to load"
        )
        
        if st.button("📥 Load Example", type="primary"):
            nfa_data = examples[selected_example]
            source = f"Example: {selected_example}"
            st.success(f"✅ Loaded: {selected_example}")
    
    # Process and validate NFA data
    if nfa_data is not None:
        st.markdown("---")
        st.header("📋 NFA Preview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("JSON Structure")
            st.json(nfa_data)
        
        with col2:
            st.subheader("Summary")
            try:
                st.metric("States", len(nfa_data.get('states', [])))
                st.metric("Alphabet Size", len(nfa_data.get('alphabet', [])))
                st.metric("Final States", len(nfa_data.get('final_states', [])))
                
                transitions = nfa_data.get('transitions', {})
                total_transitions = sum(len(trans) for trans in transitions.values())
                st.metric("Transitions", total_transitions)
            except:
                st.warning("⚠️ Could not compute summary")
        
        st.markdown("---")
        
        # Validate NFA
        st.subheader("✅ Validation")
        
        is_valid, message = validate_nfa(nfa_data)
        
        if is_valid:
            st.success(f"✅ {message}")
            
            # Save button
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save NFA", type="primary", use_container_width=True):
                    st.session_state['nfa_data'] = nfa_data
                    st.balloons()
                    st.success(f"🎉 NFA saved from: {source}")
            
            with col2:
                if st.button("🔄 Convert to DFA →", use_container_width=True):
                    st.session_state['nfa_data'] = nfa_data
                    st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
            
            with col3:
                if st.button("🏠 Back to Home", use_container_width=True):
                    st.switch_page("main.py")
            
            # Show detailed information
            st.markdown("---")
            st.subheader("📊 Detailed Information")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**States:**")
                st.code(", ".join(nfa_data.get('states', [])))
                
                st.markdown("**Alphabet:**")
                st.code(", ".join(nfa_data.get('alphabet', [])))
            
            with col2:
                st.markdown(f"**Start State:** `{nfa_data.get('start_state', 'N/A')}`")
                
                st.markdown("**Final States:**")
                st.code(", ".join(nfa_data.get('final_states', [])))
            
            # Transition table
            st.markdown("**Transition Function:**")
            
            transitions = nfa_data.get('transitions', {})
            if transitions:
                # Create a markdown table
                alphabet = nfa_data.get('alphabet', [])
                table_header = "| State | " + " | ".join(alphabet) + " |"
                table_separator = "|-------|" + "|".join(["-------"] * len(alphabet)) + "|"
                
                table_rows = [table_header, table_separator]
                
                for state in nfa_data.get('states', []):
                    row = f"| {state} |"
                    for symbol in alphabet:
                        if state in transitions and symbol in transitions[state]:
                            dest = ", ".join(transitions[state][symbol])
                            row += f" {dest} |"
                        else:
                            row += " ∅ |"
                    table_rows.append(row)
                
                st.markdown("\n".join(table_rows))
            else:
                st.warning("No transitions defined")
        
        else:
            st.error(f"❌ Invalid NFA: {message}")
            st.info("💡 Please fix the errors in your NFA and try again.")
            
            # Still offer to view the data
            with st.expander("🔍 View Raw Data"):
                st.json(nfa_data)
    
    # Show current session state
    if 'nfa_data' in st.session_state:
        st.markdown("---")
        st.info("ℹ️ An NFA is already loaded in memory. Load a new one to replace it.")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗑️ Clear Loaded NFA", use_container_width=True):
                del st.session_state['nfa_data']
                if 'dfa_data' in st.session_state:
                    del st.session_state['dfa_data']
                if 'conversion_logs' in st.session_state:
                    del st.session_state['conversion_logs']
                st.rerun()
    
    # Sidebar
    with st.sidebar:
        st.header("📖 JSON Format Guide")
        
        st.markdown("""
        ### Required Fields
        
        Your NFA JSON must contain:
        
        - `states`: Array of state names
        - `alphabet`: Array of input symbols
        - `start_state`: String (must be in states)
        - `final_states`: Array of state names
        - `transitions`: Object mapping states to symbols to destination states
        
        ### Example Structure
        
        ```json
        {
          "states": ["q0", "q1"],
          "alphabet": ["a", "b"],
          "start_state": "q0",
          "final_states": ["q1"],
          "transitions": {
            "q0": {
              "a": ["q0", "q1"],
              "b": ["q0"]
            },
            "q1": {
              "a": ["q1"],
              "b": ["q1"]
            }
          }
        }
        ```
        
        ### Tips
        - Destination states must be arrays (even for a single state)
        - Non-determinism: Use multiple destination states
        - Missing transitions are allowed (equivalent to ∅)
        """)


if __name__ == "__main__":
    main()
