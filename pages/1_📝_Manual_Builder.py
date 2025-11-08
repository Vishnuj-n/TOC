"""Manual NFA Builder Page

Build NFAs interactively using a form-based interface.
"""

import streamlit as st
import json
from nfa_to_dfa import validate_nfa

st.set_page_config(
    page_title="Manual NFA Builder",
    page_icon="📝",
    layout="wide"
)


def main():
    """Manual NFA builder page."""
    
    st.title("📝 Manual NFA Builder")
    st.markdown("""
    Build your NFA step-by-step using this interactive form. All inputs are validated before saving.
    """)
    
    # Initialize session state for transitions if not exists
    if 'transitions_data' not in st.session_state:
        st.session_state.transitions_data = {}
    
    # Main form for NFA construction
    with st.form("nfa_builder_form", clear_on_submit=False):
        st.subheader("🎯 Step 1: Define States")
        
        col1, col2 = st.columns(2)
        
        with col1:
            states_input = st.text_input(
                "States (comma-separated)",
                value="q0, q1, q2",
                help="Enter state names separated by commas. Example: q0, q1, q2"
            )
        
        with col2:
            alphabet_input = st.text_input(
                "Alphabet (comma-separated)",
                value="a, b",
                help="Enter alphabet symbols separated by commas. Example: a, b, 0, 1"
            )
        
        # Parse states and alphabet
        states = [s.strip() for s in states_input.split(',') if s.strip()]
        alphabet = [s.strip() for s in alphabet_input.split(',') if s.strip()]
        
        st.markdown("---")
        st.subheader("🏁 Step 2: Select Start and Final States")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if states:
                start_state = st.selectbox(
                    "Start State",
                    options=states,
                    help="Select the initial state of the NFA"
                )
            else:
                start_state = None
                st.warning("⚠️ Please define states first")
        
        with col2:
            if states:
                final_states = st.multiselect(
                    "Final States (can select multiple)",
                    options=states,
                    default=[states[-1]] if states else [],
                    help="Select one or more final/accepting states"
                )
            else:
                final_states = []
                st.warning("⚠️ Please define states first")
        
        st.markdown("---")
        st.subheader("🔀 Step 3: Define Transitions")
        
        st.markdown("""
        Define transitions for each state and symbol. You can specify multiple destination states 
        (comma-separated) for non-deterministic behavior.
        """)
        
        transitions = {}
        
        if states and alphabet:
            # Create a grid of inputs for transitions
            for state in states:
                st.markdown(f"**From State: `{state}`**")
                transitions[state] = {}
                
                cols = st.columns(len(alphabet))
                for idx, symbol in enumerate(alphabet):
                    with cols[idx]:
                        # Get previous value if exists
                        prev_value = ""
                        if state in st.session_state.transitions_data:
                            if symbol in st.session_state.transitions_data[state]:
                                prev_value = ", ".join(st.session_state.transitions_data[state][symbol])
                        
                        dest_input = st.text_input(
                            f"On '{symbol}'",
                            value=prev_value,
                            key=f"trans_{state}_{symbol}",
                            help=f"Destination states when reading '{symbol}' from state '{state}'. Leave empty for no transition.",
                            placeholder="q1, q2"
                        )
                        
                        if dest_input.strip():
                            dest_states = [s.strip() for s in dest_input.split(',') if s.strip()]
                            transitions[state][symbol] = dest_states
                
                st.markdown("")  # Spacing
        else:
            st.warning("⚠️ Please define states and alphabet first")
        
        st.markdown("---")
        
        # Form submission
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            submit_button = st.form_submit_button("✅ Build NFA", type="primary", use_container_width=True)
        
        with col2:
            preview_button = st.form_submit_button("👁️ Preview JSON", use_container_width=True)
        
        with col3:
            clear_button = st.form_submit_button("🗑️ Clear Form", use_container_width=True)
    
    # Handle form submission
    if clear_button:
        st.session_state.transitions_data = {}
        if 'nfa_data' in st.session_state:
            del st.session_state['nfa_data']
        st.rerun()
    
    if submit_button or preview_button:
        # Store transitions in session state
        st.session_state.transitions_data = transitions
        
        # Build NFA data structure
        nfa_data = {
            "states": states,
            "alphabet": alphabet,
            "start_state": start_state,
            "final_states": final_states,
            "transitions": transitions
        }
        
        # Validate NFA
        is_valid, error_msg = validate_nfa(nfa_data)
        
        if is_valid:
            st.success(f"✅ {error_msg}")
            
            # Save to session state
            if submit_button:
                st.session_state['nfa_data'] = nfa_data
                st.balloons()
                
                st.markdown("---")
                st.success("🎉 NFA successfully built and saved!")
                
                # Show NFA preview
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 NFA Summary")
                    st.metric("Total States", len(states))
                    st.metric("Alphabet Size", len(alphabet))
                    st.metric("Final States", len(final_states))
                    st.metric("Transitions", sum(len(trans) for trans in transitions.values()))
                
                with col2:
                    st.subheader("📋 NFA Details")
                    st.markdown(f"**States:** {', '.join(states)}")
                    st.markdown(f"**Alphabet:** {', '.join(alphabet)}")
                    st.markdown(f"**Start State:** {start_state}")
                    st.markdown(f"**Final States:** {', '.join(final_states)}")
                
                st.markdown("---")
                
                # Navigation buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Convert to DFA →", use_container_width=True, type="primary"):
                        st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
                
                with col2:
                    # Download as JSON
                    nfa_json = json.dumps(nfa_data, indent=2)
                    st.download_button(
                        label="💾 Download JSON",
                        data=nfa_json,
                        file_name="nfa.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col3:
                    if st.button("🏠 Back to Home", use_container_width=True):
                        st.switch_page("main.py")
            
            # Preview mode
            if preview_button:
                st.markdown("---")
                st.subheader("👁️ JSON Preview")
                st.json(nfa_data)
        
        else:
            st.error(f"❌ Invalid NFA: {error_msg}")
            st.info("💡 Please fix the errors above and try again.")
    
    # Show current session state
    if 'nfa_data' in st.session_state and not submit_button:
        st.markdown("---")
        st.info("ℹ️ An NFA is already loaded in memory. Submit the form to overwrite it.")
    
    # Sidebar help
    with st.sidebar:
        st.header("📖 Quick Guide")
        
        st.markdown("""
        ### How to Build an NFA
        
        1. **Define States**: Enter state names separated by commas
        2. **Define Alphabet**: Enter input symbols separated by commas
        3. **Select Start State**: Choose the initial state
        4. **Select Final States**: Choose accepting states (can be multiple)
        5. **Define Transitions**: For each state and symbol combination, specify destination states
        6. **Build**: Click "Build NFA" to validate and save
        
        ### Tips
        - For non-deterministic transitions, enter multiple states separated by commas
        - Leave transition fields empty if there's no transition
        - Use "Preview JSON" to check the structure before building
        - Click "Convert to DFA" after building to see the conversion
        """)
        
        st.markdown("---")
        
        st.header("📝 Example")
        st.markdown("""
        **States**: q0, q1, q2  
        **Alphabet**: a, b  
        **Start**: q0  
        **Final**: q2  
        
        **Transitions**:
        - q0 on 'a' → q0, q1 (non-deterministic!)
        - q0 on 'b' → q0
        - q1 on 'b' → q2
        - q2 on 'a' → q2
        - q2 on 'b' → q2
        """)


if __name__ == "__main__":
    main()
