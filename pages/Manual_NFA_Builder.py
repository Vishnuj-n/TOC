"""Manual NFA Builder Page"""
import streamlit as st
import json
from nfa_to_dfa import validate_nfa

st.set_page_config(page_title="Manual NFA Builder", page_icon="📝", layout="wide")

def initialize_session_state():
    """Initialize session state variables for the builder."""
    if 'builder_states' not in st.session_state:
        st.session_state.builder_states = []
    if 'builder_alphabet' not in st.session_state:
        st.session_state.builder_alphabet = []
    if 'builder_start_state' not in st.session_state:
        st.session_state.builder_start_state = None
    if 'builder_final_states' not in st.session_state:
        st.session_state.builder_final_states = []
    if 'builder_transitions' not in st.session_state:
        st.session_state.builder_transitions = {}
    if 'step1_completed' not in st.session_state:
        st.session_state.step1_completed = False
    if 'step2_completed' not in st.session_state:
        st.session_state.step2_completed = False

def main():
    st.title("📝 Manual NFA Builder")
    st.markdown("Build your NFA step-by-step. Each step depends on the previous one.")
    
    initialize_session_state()
    
    # Progress indicator
    st.markdown("---")
    progress_cols = st.columns(3)
    with progress_cols[0]:
        if st.session_state.step1_completed:
            st.success("✅ Step 1: States & Alphabet")
        else:
            st.info("⏳ Step 1: States & Alphabet")
    with progress_cols[1]:
        if st.session_state.step2_completed:
            st.success("✅ Step 2: Start & Final States")
        elif st.session_state.step1_completed:
            st.info("⏳ Step 2: Start & Final States")
        else:
            st.warning("🔒 Step 2: Locked")
    with progress_cols[2]:
        if st.session_state.step2_completed:
            st.info("⏳ Step 3: Define Transitions")
        else:
            st.warning("🔒 Step 3: Locked")
    
    st.markdown("---")
    
    # STEP 1: Define States and Alphabet
    st.subheader("🎯 Step 1: Define States and Alphabet")
    with st.form("step1_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            states_input = st.text_input(
                "States (comma-separated)", 
                value=", ".join(st.session_state.builder_states) if st.session_state.builder_states else "q0, q1, q2",
                help="Example: q0, q1, q2"
            )
        with col2:
            alphabet_input = st.text_input(
                "Alphabet (comma-separated)", 
                value=", ".join(st.session_state.builder_alphabet) if st.session_state.builder_alphabet else "a, b",
                help="Example: a, b, 0, 1"
            )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            step1_submit = st.form_submit_button("➡️ Next: Select States", type="primary", use_container_width=True)
        with col2:
            step1_reset = st.form_submit_button("🔄 Reset All", use_container_width=True)
    
    if step1_reset:
        # Reset all session state
        for key in ['builder_states', 'builder_alphabet', 'builder_start_state', 
                    'builder_final_states', 'builder_transitions', 
                    'step1_completed', 'step2_completed']:
            if key in st.session_state:
                if 'transitions' in key or 'states' in key or 'alphabet' in key:
                    st.session_state[key] = [] if 'list' in str(type(st.session_state.get(key, []))) else {}
                elif 'completed' in key:
                    st.session_state[key] = False
                else:
                    st.session_state[key] = None
        st.rerun()
    
    if step1_submit:
        new_states = [s.strip() for s in states_input.split(',') if s.strip()]
        new_alphabet = [s.strip() for s in alphabet_input.split(',') if s.strip()]
        
        if not new_states:
            st.error("❌ Please define at least one state")
        elif not new_alphabet:
            st.error("❌ Please define at least one alphabet symbol")
        else:
            # Check if states or alphabet changed
            states_changed = new_states != st.session_state.builder_states
            alphabet_changed = new_alphabet != st.session_state.builder_alphabet
            
            st.session_state.builder_states = new_states
            st.session_state.builder_alphabet = new_alphabet
            st.session_state.step1_completed = True
            
            # If states or alphabet changed, reset dependent steps
            if states_changed:
                # Reset start state if it's not in new states
                if st.session_state.builder_start_state not in new_states:
                    st.session_state.builder_start_state = None
                # Reset final states to only include states that still exist
                st.session_state.builder_final_states = [
                    s for s in st.session_state.builder_final_states if s in new_states
                ]
                # Reset transitions
                st.session_state.builder_transitions = {}
                st.session_state.step2_completed = False
                st.info("ℹ️ States changed - Step 2 and Step 3 have been reset")
            
            if alphabet_changed:
                # Reset transitions
                st.session_state.builder_transitions = {}
                st.info("ℹ️ Alphabet changed - Step 3 transitions have been reset")
            
            st.success("✅ Step 1 completed! Proceed to Step 2.")
            st.rerun()
    
    # Display current Step 1 values if completed
    if st.session_state.step1_completed:
        st.info(f"**States:** {', '.join(st.session_state.builder_states)} | **Alphabet:** {', '.join(st.session_state.builder_alphabet)}")
    
    st.markdown("---")
    
    # STEP 2: Select Start and Final States
    st.subheader("🏁 Step 2: Select Start and Final States")
    
    if not st.session_state.step1_completed:
        st.warning("⚠️ Complete Step 1 first")
    else:
        with st.form("step2_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                start_state = st.selectbox(
                    "Start State", 
                    options=st.session_state.builder_states,
                    index=st.session_state.builder_states.index(st.session_state.builder_start_state) 
                          if st.session_state.builder_start_state in st.session_state.builder_states 
                          else 0,
                    help="Initial state"
                )
            with col2:
                final_states = st.multiselect(
                    "Final States", 
                    options=st.session_state.builder_states,
                    default=st.session_state.builder_final_states if st.session_state.builder_final_states else [st.session_state.builder_states[-1]],
                    help="Accepting states"
                )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                step2_submit = st.form_submit_button("➡️ Next: Define Transitions", type="primary", use_container_width=True)
            with col2:
                step2_back = st.form_submit_button("⬅️ Back to Step 1", use_container_width=True)
        
        if step2_back:
            st.session_state.step1_completed = False
            st.session_state.step2_completed = False
            st.rerun()
        
        if step2_submit:
            if not final_states:
                st.error("❌ Please select at least one final state")
            else:
                # Check if start or final states changed
                start_changed = start_state != st.session_state.builder_start_state
                final_changed = set(final_states) != set(st.session_state.builder_final_states)
                
                st.session_state.builder_start_state = start_state
                st.session_state.builder_final_states = final_states
                st.session_state.step2_completed = True
                
                if start_changed or final_changed:
                    st.info("ℹ️ Start or Final states changed - you can update transitions in Step 3")
                
                st.success("✅ Step 2 completed! Proceed to Step 3.")
                st.rerun()
        
        # Display current Step 2 values if completed
        if st.session_state.step2_completed:
            st.info(f"**Start:** {st.session_state.builder_start_state} | **Final:** {', '.join(st.session_state.builder_final_states)}")
    
    st.markdown("---")
    
    # STEP 3: Define Transitions
    st.subheader("🔀 Step 3: Define Transitions")
    
    if not st.session_state.step2_completed:
        st.warning("⚠️ Complete Step 2 first")
    else:
        st.markdown("Specify destination states (comma-separated) for non-deterministic behavior.")
        
        with st.form("step3_form", clear_on_submit=False):
            transitions = {}
            
            for state in st.session_state.builder_states:
                st.markdown(f"**From State: `{state}`**")
                transitions[state] = {}
                cols = st.columns(len(st.session_state.builder_alphabet))
                
                for idx, symbol in enumerate(st.session_state.builder_alphabet):
                    with cols[idx]:
                        # Get previous value if exists
                        prev = ""
                        if state in st.session_state.builder_transitions:
                            if symbol in st.session_state.builder_transitions[state]:
                                prev = ", ".join(st.session_state.builder_transitions[state][symbol])
                        
                        dest_input = st.text_input(
                            f"On '{symbol}'", 
                            value=prev, 
                            key=f"trans_{state}_{symbol}",
                            help=f"Destinations from '{state}' on '{symbol}' (comma-separated)",
                            placeholder=f"e.g., {st.session_state.builder_states[0]}"
                        )
                        if dest_input.strip():
                            dest_list = [s.strip() for s in dest_input.split(',') if s.strip()]
                            # Validate destinations
                            invalid_dests = [d for d in dest_list if d not in st.session_state.builder_states]
                            if invalid_dests:
                                st.error(f"❌ Invalid state(s): {', '.join(invalid_dests)}")
                            else:
                                transitions[state][symbol] = dest_list
                st.markdown("")
            
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                build_nfa = st.form_submit_button("✅ Build NFA", type="primary", use_container_width=True)
            with col2:
                preview_json = st.form_submit_button("👁️ Preview JSON", use_container_width=True)
            with col3:
                step3_back = st.form_submit_button("⬅️ Back to Step 2", use_container_width=True)
        
        if step3_back:
            st.session_state.step2_completed = False
            st.rerun()
        
        if build_nfa or preview_json:
            st.session_state.builder_transitions = transitions
            
            nfa_data = {
                "states": st.session_state.builder_states,
                "alphabet": st.session_state.builder_alphabet,
                "start_state": st.session_state.builder_start_state,
                "final_states": st.session_state.builder_final_states,
                "transitions": transitions
            }
            
            is_valid, msg = validate_nfa(nfa_data)
            
            if is_valid:
                st.success(f"✅ {msg}")
                if build_nfa:
                    st.session_state['nfa_data'] = nfa_data
                    st.balloons()
                    st.success("🎉 NFA built successfully! Redirecting to converter...")
                    st.switch_page("pages/NFA_to_DFA_Converter.py")
                if preview_json:
                    st.markdown("---")
                    st.subheader("👁️ JSON Preview")
                    st.json(nfa_data)
            else:
                st.error(f"❌ Invalid NFA: {msg}")
                st.info("💡 Fix errors and try again.")
    
    if 'nfa_data' in st.session_state and st.session_state.step2_completed:
        st.markdown("---")
        st.info("ℹ️ An NFA is already loaded. Building a new one will overwrite it.")
    
    with st.sidebar:
        st.header("📖 Quick Guide")
        st.markdown("""### How to Build
**Step 1: States & Alphabet**
- Define your states: q0, q1, q2
- Define alphabet symbols: a, b

**Step 2: Start & Final**
- Select initial state
- Select accepting states

**Step 3: Transitions**
- Define transitions for each state
- Use comma-separated for non-determinism

### Example
**States**: q0, q1, q2  
**Alphabet**: a, b  
**Start**: q0  
**Final**: q2  
**Transitions**:  
- q0 on 'a' → q0, q1  
- q0 on 'b' → q0  
- q1 on 'b' → q2  
- q2 on 'a' → q2  
- q2 on 'b' → q2

### Tips
- Changes in Step 1 will reset Steps 2 & 3
- Changes in Step 2 will preserve Step 3
- You can go back to any step
- Invalid destinations are highlighted
""")
        
        st.markdown("---")
        st.header("🔄 Quick Actions")
        if st.button("🏠 Go to Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
