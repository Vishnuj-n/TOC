"""Manual NFA Builder Page"""
import streamlit as st
from nfa_to_dfa import validate_nfa

st.set_page_config(page_title="Manual NFA Builder", page_icon="📝", layout="wide")

def init_state():
    """Initialize session state variables."""
    defaults = {
        'builder_states': [], 'builder_alphabet': [], 'builder_start_state': None,
        'builder_final_states': [], 'builder_transitions': {},
        'step1_completed': False, 'step2_completed': False
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)

def reset_all():
    """Reset all builder state."""
    for key in ['builder_states', 'builder_alphabet', 'builder_start_state', 
                'builder_final_states', 'builder_transitions', 'step1_completed', 'step2_completed']:
        st.session_state[key] = [] if 'states' in key or 'alphabet' in key else ({} if 'transitions' in key else (False if 'completed' in key else None))

def show_progress():
    """Display progress indicator."""
    progress = [
        ("✅ Step 1: States & Alphabet" if st.session_state.step1_completed else "⏳ Step 1: States & Alphabet", 
         st.session_state.step1_completed),
        ("✅ Step 2: Start & Final" if st.session_state.step2_completed else 
         ("⏳ Step 2: Start & Final" if st.session_state.step1_completed else "🔒 Step 2: Locked"),
         st.session_state.step2_completed or st.session_state.step1_completed),
        ("⏳ Step 3: Transitions" if st.session_state.step2_completed else "🔒 Step 3: Locked",
         st.session_state.step2_completed)
    ]
    cols = st.columns(3)
    for col, (text, is_active) in zip(cols, progress):
        with col:
            (st.success if "✅" in text else (st.info if "⏳" in text else st.warning))(text)

def main():
    st.title("� Manual NFA Builder")
    st.markdown("Build your NFA step-by-step. Each step depends on the previous one.")
    init_state()
    st.markdown("---")
    show_progress()
    st.markdown("---")
    
    # STEP 1
    st.subheader("🎯 Step 1: Define States and Alphabet")
    with st.form("step1_form"):
        col1, col2 = st.columns(2)
        states_input = col1.text_input("States (comma-separated)", 
            value=", ".join(st.session_state.builder_states) or "q0, q1, q2", help="Example: q0, q1, q2")
        alphabet_input = col2.text_input("Alphabet (comma-separated)", 
            value=", ".join(st.session_state.builder_alphabet) or "a, b", help="Example: a, b")
        
        col1, col2 = st.columns(2)
        step1_submit = col1.form_submit_button("➡️ Next", type="primary", use_container_width=True)
        step1_reset = col2.form_submit_button("🔄 Reset All", use_container_width=True)
    
    if step1_reset:
        reset_all()
        st.rerun()
    
    if step1_submit:
        new_states = [s.strip() for s in states_input.split(',') if s.strip()]
        new_alphabet = [s.strip() for s in alphabet_input.split(',') if s.strip()]
        
        if not new_states or not new_alphabet:
            st.error("❌ Please define states and alphabet")
        else:
            states_changed = new_states != st.session_state.builder_states
            alphabet_changed = new_alphabet != st.session_state.builder_alphabet
            
            st.session_state.builder_states = new_states
            st.session_state.builder_alphabet = new_alphabet
            st.session_state.step1_completed = True
            
            if states_changed:
                if st.session_state.builder_start_state not in new_states:
                    st.session_state.builder_start_state = None
                st.session_state.builder_final_states = [s for s in st.session_state.builder_final_states if s in new_states]
                st.session_state.builder_transitions = {}
                st.session_state.step2_completed = False
            if alphabet_changed:
                st.session_state.builder_transitions = {}
            
            st.success("✅ Step 1 completed!")
            st.rerun()
    
    if st.session_state.step1_completed:
        st.info(f"**States:** {', '.join(st.session_state.builder_states)} | **Alphabet:** {', '.join(st.session_state.builder_alphabet)}")
    
    st.markdown("---")
    
    # STEP 2
    st.subheader("🏁 Step 2: Select Start and Final States")
    if not st.session_state.step1_completed:
        st.warning("⚠️ Complete Step 1 first")
    else:
        with st.form("step2_form"):
            col1, col2 = st.columns(2)
            start_state = col1.selectbox("Start State", st.session_state.builder_states,
                index=st.session_state.builder_states.index(st.session_state.builder_start_state) 
                if st.session_state.builder_start_state in st.session_state.builder_states else 0)
            final_states = col2.multiselect("Final States", st.session_state.builder_states,
                default=st.session_state.builder_final_states or [st.session_state.builder_states[-1]])
            
            col1, col2 = st.columns(2)
            step2_submit = col1.form_submit_button("➡️ Next", type="primary", use_container_width=True)
            step2_back = col2.form_submit_button("⬅️ Back", use_container_width=True)
        
        if step2_back:
            st.session_state.step1_completed = st.session_state.step2_completed = False
            st.rerun()
        
        if step2_submit and final_states:
            st.session_state.builder_start_state = start_state
            st.session_state.builder_final_states = final_states
            st.session_state.step2_completed = True
            st.success("✅ Step 2 completed!")
            st.rerun()
        elif step2_submit:
            st.error("❌ Select at least one final state")
        
        if st.session_state.step2_completed:
            st.info(f"**Start:** {st.session_state.builder_start_state} | **Final:** {', '.join(st.session_state.builder_final_states)}")
    
    st.markdown("---")
    
    # STEP 3
    st.subheader("🔀 Step 3: Define Transitions")
    if not st.session_state.step2_completed:
        st.warning("⚠️ Complete Step 2 first")
    else:
        st.info("💡 **Tip:** Enter comma-separated states. E.g., if `q0` on `'a'` goes to `q0, q1`, enter: `q0, q1`")
        
        with st.form("step3_form"):
            transitions = {}
            for state in st.session_state.builder_states:
                st.markdown(f"**From State: `{state}`**")
                transitions[state] = {}
                cols = st.columns(len(st.session_state.builder_alphabet))
                
                for idx, symbol in enumerate(st.session_state.builder_alphabet):
                    prev = ", ".join(st.session_state.builder_transitions.get(state, {}).get(symbol, []))
                    dest_input = cols[idx].text_input(f"On '{symbol}'", value=prev, key=f"trans_{state}_{symbol}",
                        placeholder=f"e.g., {st.session_state.builder_states[0]}")
                    
                    if dest_input.strip():
                        dest_list = [s.strip() for s in dest_input.split(',') if s.strip()]
                        invalid = [d for d in dest_list if d not in st.session_state.builder_states]
                        if invalid:
                            cols[idx].error(f"❌ Invalid: {', '.join(invalid)}")
                        else:
                            transitions[state][symbol] = dest_list
            
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            build_nfa = col1.form_submit_button("✅ Build NFA", type="primary", use_container_width=True)
            preview_json = col2.form_submit_button("👁️ Preview", use_container_width=True)
            step3_back = col3.form_submit_button("⬅️ Back", use_container_width=True)
        
        if step3_back:
            st.session_state.step2_completed = False
            st.rerun()
        
        # Show transition summary
        if transitions:
            st.markdown("---")
            st.subheader("📋 Transition Summary")
            import pandas as pd
            data = []
            for state in st.session_state.builder_states:
                for symbol in st.session_state.builder_alphabet:
                    if state in transitions and symbol in transitions[state]:
                        dests = transitions[state][symbol]
                        data.append({"From": state, "Input": symbol, "To": ", ".join(dests), "ND": "Yes" if len(dests) > 1 else "No"})
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        
        if build_nfa or preview_json:
            st.session_state.builder_transitions = transitions
            nfa_data = {"states": st.session_state.builder_states, "alphabet": st.session_state.builder_alphabet,
                       "start_state": st.session_state.builder_start_state, "final_states": st.session_state.builder_final_states,
                       "transitions": transitions}
            
            is_valid, msg = validate_nfa(nfa_data)
            if is_valid:
                st.success(f"✅ {msg}")
                if build_nfa:
                    st.session_state['nfa_data'] = nfa_data
                    st.balloons()
                    st.switch_page("pages/NFA_to_DFA_Converter.py")
                else:
                    st.json(nfa_data)
            else:
                st.error(f"❌ {msg}")
    
    if 'nfa_data' in st.session_state and st.session_state.step2_completed:
        st.info("ℹ️ An NFA is already loaded. Building a new one will overwrite it.")
    
    with st.sidebar:
        st.header("📖 Quick Guide")
        st.markdown("""**Step 1:** States & Alphabet  
**Step 2:** Start & Final  
**Step 3:** Transitions

### Example
**States**: q0, q1, q2  
**Alphabet**: a, b  
**Start**: q0 | **Final**: q2  
**Transitions**:  
- q0 + 'a' → q0, q1  
- q0 + 'b' → q0  
- q1 + 'b' → q2

### Tips
✓ Step 1 changes reset Steps 2 & 3  
✓ Use commas for non-determinism  
✓ Review transition summary""")
        
        st.markdown("---")
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("main.py")

if __name__ == "__main__":
    main()
