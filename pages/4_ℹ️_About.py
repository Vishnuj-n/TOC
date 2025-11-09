"""About and Help Page"""
import streamlit as st

st.set_page_config(page_title="About & Help", page_icon="ℹ️", layout="wide")

def main():
    st.title("ℹ️ About & Help")
    st.markdown("Documentation and examples for the NFA to DFA Visualizer.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Documentation", "💡 Examples", "❓ FAQ", "🔧 Technical"])
    
    with tab1:
        st.header("📚 Documentation")
        st.markdown("""## What is this tool?
The **NFA to DFA Visualizer** converts **Non-deterministic Finite Automata (NFA)** to **Deterministic Finite Automata (DFA)** using **Subset Construction**.

### Features
✅ Multiple Input Methods | ✅ Visual Graphs | ✅ Step-by-Step Logs | ✅ Auto Validation | ✅ Export Results | ✅ Comparison Views

### How to Use
**Method 1: Manual Builder** - Enter states, alphabet, select start/final, define transitions  
**Method 2: Import JSON** - Upload/paste JSON or load examples  
**Method 3: Direct** - Load NFA → Convert & Visualize

### NFA vs DFA
| Feature | NFA | DFA |
|---------|-----|-----|
| **Transitions** | Multiple per state-symbol | Exactly one per state-symbol |
| **Acceptance** | ANY path to final | THE path to final |
| **States** | Usually fewer | Can be 2^n (worst case) |
| **Computation** | Slower (track multiple) | Faster (single state) |
| **Design** | Easier | Harder |""")
    
    with tab2:
        st.header("💡 Examples")
        examples = [
            ("Strings Containing 'aba'", 
             {"states": ["q0", "q1", "q2", "q3"], "alphabet": ["a", "b"], "start_state": "q0",
              "final_states": ["q3"], "transitions": {"q0": {"a": ["q0", "q1"], "b": ["q0"]},
                                                      "q1": {"b": ["q2"]}, "q2": {"a": ["q3"]},
                                                      "q3": {"a": ["q3"], "b": ["q3"]}}},
             "Accepts: `aba`, `aaba`, `abababa` | Rejects: `ab`, `aab`, `bbb`"),
            ("Binary Ending with '01'",
             {"states": ["q0", "q1", "q2"], "alphabet": ["0", "1"], "start_state": "q0",
              "final_states": ["q2"], "transitions": {"q0": {"0": ["q0", "q1"], "1": ["q0"]},
                                                      "q1": {"1": ["q2"]}, "q2": {"0": ["q1"], "1": ["q0"]}}},
             "Accepts: `01`, `101`, `1001` | Rejects: `0`, `10`, `111`"),
            ("At least 1 'a' then 1 'b'",
             {"states": ["q0", "q1", "q2"], "alphabet": ["a", "b"], "start_state": "q0",
              "final_states": ["q2"], "transitions": {"q0": {"a": ["q0", "q1"], "b": ["q0"]},
                                                      "q1": {"b": ["q2"]}, "q2": {"a": ["q2"], "b": ["q2"]}}},
             "Accepts: `aab`, `aaabbb` | Rejects: `aaa`, `bbb`, `ab`")
        ]
        
        for title, nfa, desc in examples:
            st.markdown(f"### {title}")
            col1, col2 = st.columns(2)
            with col1:
                st.json(nfa)
            with col2:
                st.markdown(f"**Description:** {desc}\n\nNon-deterministic at state q0")
            st.markdown("---")
    
    with tab3:
        st.header("❓ FAQ")
        faqs = [
            ("What's the difference between NFA and DFA?",
             "**NFA:** Multiple transitions per state-symbol, epsilon transitions. **DFA:** Exactly one transition per state-symbol, no epsilon."),
            ("What is Subset Construction?",
             "Algorithm converting NFA to DFA by creating DFA states from sets of NFA states. **Complexity:** O(2^n × |Σ|)"),
            ("Why more DFA states than NFA?",
             "**State explosion** is normal. Each DFA state = set of NFA states. Worst case: 2^n states."),
            ("Can I convert DFA to NFA?",
             "Yes! Every DFA is already a valid NFA (special case). No conversion needed."),
            ("Does this support epsilon (ε) transitions?",
             "Currently **no**. Focus is on NFAs without epsilon transitions."),
            ("What if transitions are missing?",
             "Missing transitions = implicit dead state (∅). Algorithm handles automatically."),
            ("How to download NFA/DFA?",
             "**NFA:** Manual Builder → Download JSON. **DFA:** Convert page → Download DFA JSON."),
            ("Why no graph?",
             "Install **Graphviz**: https://graphviz.org/download/ and add to PATH.")
        ]
        for q, a in faqs:
            with st.expander(f"❓ {q}"):
                st.markdown(a)
    
    with tab4:
        st.header("🔧 Technical")
        st.markdown("""### Technology Stack
**Frontend:** Streamlit | **Backend:** Python 3.8+ | **Viz:** Graphviz | **Algorithm:** Subset Construction

### JSON Format
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": {
    "q0": {"a": ["q0", "q1"], "b": ["q0"]}
  }
}
```

### Validation Rules
1. All fields required: `states`, `alphabet`, `start_state`, `final_states`, `transitions`
2. `states` and `alphabet` must be non-empty arrays
3. `start_state` must be in `states`
4. All `final_states` must be in `states`
5. Transition keys must be in `states`
6. Transition symbols must be in `alphabet`
7. Destination states must be arrays and in `states`

### Algorithm Pseudocode
```
SubsetConstruction(NFA):
  DFA_states = {}, queue = [{NFA.start}]
  while queue not empty:
    current = queue.pop()
    for symbol in alphabet:
      next = compute_reachable(current, symbol)
      if next not in DFA_states:
        DFA_states.add(next), queue.add(next)
      DFA.transitions[current][symbol] = next
  for state in DFA_states:
    if contains_NFA_final(state):
      DFA.final.add(state)
```

### Performance
**Best:** O(n) | **Average:** O(n log n) | **Worst:** O(2^n)

### Version: v3.0 - Multi-page, form-based builder, comprehensive testing""")
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #666;'><p><strong>NFA → DFA Visualizer v3.0</strong><br>Built with ❤️ using Streamlit</p></div>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("🔗 Quick Links")
        for emoji, name, page in [("🏠", "Home", "main.py"),
                                   ("📝", "Manual Builder", "pages/1_📝_Manual_Builder.py"),
                                   ("📤", "Import JSON", "pages/2_📤_Import_JSON.py"),
                                   ("🔄", "Convert & Visualize", "pages/3_�_Convert_NFA_DFA.py")]:
            if st.button(f"{emoji} {name}", use_container_width=True):
                st.switch_page(page)
        
        st.markdown("---")
        st.header("📚 Resources")
        st.markdown("- [Automata Theory](https://en.wikipedia.org/wiki/Automata_theory)\n- [Subset Construction](https://en.wikipedia.org/wiki/Powerset_construction)\n- [Graphviz](https://graphviz.org/)\n- [Streamlit](https://docs.streamlit.io/)")

if __name__ == "__main__":
    main()
