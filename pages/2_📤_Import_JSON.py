"""Import JSON Page"""
import streamlit as st
import json
from nfa_to_dfa import validate_nfa

st.set_page_config(page_title="Import NFA JSON", page_icon="📤", layout="wide")

def load_json_from_text(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"JSON parsing error: {e}"

def main():
    st.title("📤 Import NFA JSON")
    st.markdown("Import your NFA by uploading, pasting, or loading an example.")
    
    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "📋 Paste JSON", "📚 Load Example"])
    
    nfa_data, source = None, None
    
    with tab1:
        uploaded = st.file_uploader("Choose a JSON file", type=["json"], help="Select a .json file")
        if uploaded:
            try:
                nfa_data = json.load(uploaded)
                source = f"File: {uploaded.name}"
                st.success(f"✅ Loaded: {uploaded.name}")
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {e}")
    
    with tab2:
        json_text = st.text_area("Paste NFA JSON", height=400, 
                                placeholder='{"states": ["q0"], "alphabet": ["a"], ...}')
        if json_text.strip():
            result = load_json_from_text(json_text)
            if isinstance(result, tuple):
                _, error_msg = result
                st.error(f"❌ {error_msg}")
            else:
                nfa_data = result
                source = "Pasted JSON"
                st.success("✅ Parsed successfully")
    
    with tab3:
        examples = {
            "Simple NFA (a*b+)": {"states": ["q0", "q1", "q2"], "alphabet": ["a", "b"], "start_state": "q0",
                                  "final_states": ["q2"], "transitions": {"q0": {"a": ["q0", "q1"], "b": ["q0"]},
                                                                          "q1": {"b": ["q2"]}, "q2": {"a": ["q2"], "b": ["q2"]}}},
            "Binary Ending with 01": {"states": ["q0", "q1", "q2"], "alphabet": ["0", "1"], "start_state": "q0",
                                     "final_states": ["q2"], "transitions": {"q0": {"0": ["q0", "q1"], "1": ["q0"]},
                                                                            "q1": {"1": ["q2"]}, "q2": {"0": ["q1"], "1": ["q0"]}}},
            "Contains 'aba'": {"states": ["q0", "q1", "q2", "q3"], "alphabet": ["a", "b"], "start_state": "q0",
                             "final_states": ["q3"], "transitions": {"q0": {"a": ["q0", "q1"], "b": ["q0"]},
                                                                     "q1": {"b": ["q2"]}, "q2": {"a": ["q3"]},
                                                                     "q3": {"a": ["q3"], "b": ["q3"]}}}
        }
        selected = st.selectbox("Choose example", list(examples.keys()))
        if st.button("📥 Load Example", type="primary"):
            nfa_data = examples[selected]
            source = f"Example: {selected}"
            st.success(f"✅ Loaded: {selected}")
    
    if nfa_data:
        st.markdown("---")
        st.header("📋 NFA Preview")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.json(nfa_data)
        with col2:
            st.metric("States", len(nfa_data.get('states', [])))
            st.metric("Alphabet", len(nfa_data.get('alphabet', [])))
            st.metric("Final States", len(nfa_data.get('final_states', [])))
        
        st.markdown("---")
        is_valid, msg = validate_nfa(nfa_data)
        
        if is_valid:
            st.success(f"✅ {msg}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save & Convert →", type="primary", use_container_width=True):
                    st.session_state['nfa_data'] = nfa_data
                    st.balloons()
                    st.success(f"🎉 Saved from: {source}! Redirecting...")
                    st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
            with col2:
                if st.button("🏠 Home", use_container_width=True):
                    st.switch_page("main.py")
        else:
            st.error(f"❌ Invalid NFA: {msg}")
    
    if 'nfa_data' in st.session_state:
        st.markdown("---")
        st.info("ℹ️ NFA loaded. Load new one to replace.")
        if st.button("🗑️ Clear Loaded NFA", use_container_width=True):
            for key in ['nfa_data', 'dfa_data', 'conversion_logs']:
                st.session_state.pop(key, None)
            st.rerun()
    
    with st.sidebar:
        st.header("📖 JSON Format")
        st.markdown("""### Required Fields
- `states`: Array of names
- `alphabet`: Array of symbols
- `start_state`: Initial state
- `final_states`: Accepting states
- `transitions`: State→Symbol→Destinations

### Example
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
    }
  }
}
```
Destinations must be arrays. Missing transitions = ∅.""")

if __name__ == "__main__":
    main()
