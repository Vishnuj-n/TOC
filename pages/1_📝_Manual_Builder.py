"""Manual NFA Builder Page"""
import streamlit as st
import json
from nfa_to_dfa import validate_nfa

st.set_page_config(page_title="Manual NFA Builder", page_icon="📝", layout="wide")

def main():
    st.title("📝 Manual NFA Builder")
    st.markdown("Build your NFA step-by-step. All inputs are validated before saving.")
    
    if 'transitions_data' not in st.session_state:
        st.session_state.transitions_data = {}
    
    with st.form("nfa_builder_form", clear_on_submit=False):
        st.subheader("🎯 Step 1: Define States")
        col1, col2 = st.columns(2)
        with col1:
            states_input = st.text_input("States (comma-separated)", value="q0, q1, q2",
                                        help="Example: q0, q1, q2")
        with col2:
            alphabet_input = st.text_input("Alphabet (comma-separated)", value="a, b",
                                          help="Example: a, b, 0, 1")
        
        states = [s.strip() for s in states_input.split(',') if s.strip()]
        alphabet = [s.strip() for s in alphabet_input.split(',') if s.strip()]
        
        st.markdown("---")
        st.subheader("🏁 Step 2: Select Start and Final States")
        col1, col2 = st.columns(2)
        with col1:
            start_state = st.selectbox("Start State", options=states, help="Initial state") if states else None
            if not states:
                st.warning("⚠️ Define states first")
        with col2:
            final_states = st.multiselect("Final States", options=states, 
                                         default=[states[-1]] if states else [],
                                         help="Accepting states") if states else []
            if not states:
                st.warning("⚠️ Define states first")
        
        st.markdown("---")
        st.subheader("🔀 Step 3: Define Transitions")
        st.markdown("Specify destination states (comma-separated) for non-deterministic behavior.")
        
        transitions = {}
        if states and alphabet:
            for state in states:
                st.markdown(f"**From State: `{state}`**")
                transitions[state] = {}
                cols = st.columns(len(alphabet))
                for idx, symbol in enumerate(alphabet):
                    with cols[idx]:
                        prev = ""
                        if state in st.session_state.transitions_data:
                            if symbol in st.session_state.transitions_data[state]:
                                prev = ", ".join(st.session_state.transitions_data[state][symbol])
                        
                        dest_input = st.text_input(f"On '{symbol}'", value=prev, key=f"trans_{state}_{symbol}",
                                                   help=f"Destinations from '{state}' on '{symbol}'",
                                                   placeholder="q1, q2")
                        if dest_input.strip():
                            transitions[state][symbol] = [s.strip() for s in dest_input.split(',') if s.strip()]
                st.markdown("")
        else:
            st.warning("⚠️ Define states and alphabet first")
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            submit = st.form_submit_button("✅ Build NFA", type="primary", use_container_width=True)
        with col2:
            preview = st.form_submit_button("👁️ Preview JSON", use_container_width=True)
        with col3:
            clear = st.form_submit_button("🗑️ Clear Form", use_container_width=True)
    
    if clear:
        st.session_state.transitions_data = {}
        st.session_state.pop('nfa_data', None)
        st.rerun()
    
    if submit or preview:
        st.session_state.transitions_data = transitions
        nfa_data = {"states": states, "alphabet": alphabet, "start_state": start_state,
                    "final_states": final_states, "transitions": transitions}
        is_valid, msg = validate_nfa(nfa_data)
        
        if is_valid:
            st.success(f"✅ {msg}")
            if submit:
                st.session_state['nfa_data'] = nfa_data
                st.balloons()
                st.success("🎉 NFA built! Redirecting...")
                st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
            if preview:
                st.markdown("---")
                st.subheader("👁️ JSON Preview")
                st.json(nfa_data)
        else:
            st.error(f"❌ Invalid NFA: {msg}")
            st.info("💡 Fix errors and try again.")
    
    if 'nfa_data' in st.session_state and not submit:
        st.markdown("---")
        st.info("ℹ️ An NFA is loaded. Submit to overwrite.")
    
    with st.sidebar:
        st.header("📖 Quick Guide")
        st.markdown("""### How to Build
1. **States**: q0, q1, q2
2. **Alphabet**: a, b
3. **Start State**: Choose initial
4. **Final States**: Choose accepting
5. **Transitions**: Specify destinations
6. **Build**: Validate and save

For non-deterministic transitions, use multiple states (comma-separated).

### Example
**States**: q0, q1, q2  
**Alphabet**: a, b  
**Start**: q0, **Final**: q2  
**Transitions**:  
- q0 on 'a' → q0, q1  
- q0 on 'b' → q0  
- q1 on 'b' → q2  
- q2 on 'a' → q2  
- q2 on 'b' → q2""")

if __name__ == "__main__":
    main()
