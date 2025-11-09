"""NFA to DFA Visualizer - Landing Page"""
import streamlit as st

st.set_page_config(page_title="NFA → DFA Visualizer", page_icon="🔄", layout="wide", initial_sidebar_state="expanded")

def main():
    st.title("🔄 NFA → DFA Visualizer")
    st.markdown("""<div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; margin-bottom: 2rem;'>
    <h2 style='margin: 0; color: white;'>Transform NFAs into DFAs</h2>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem;'>Using the <strong>Subset Construction Algorithm</strong></p>
    </div>""", unsafe_allow_html=True)
    
    st.header("🚀 Quick Start")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Manual Builder\n**Best for learning**\n\nBuild NFAs step-by-step with interactive forms and visual preview.")
        if st.button("📝 Start Manual Builder →", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📝_Manual_Builder.py")
    
    with col2:
        st.markdown("### 🔄 Convert & Visualize\n**View results**\n\nSee graphs, algorithm traces, and comparisons.")
        if st.button("🔄 Convert & Visualize →", use_container_width=True):
            st.switch_page("pages/3_🔄_Convert_NFA_DFA.py")
    
    st.markdown("---")
    st.header("✨ Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- ✅ Subset Construction Algorithm\n- ✅ Manual NFA Builder\n- ✅ Visual Graphs\n- ✅ Detailed Logging\n- ✅ Auto Validation")
    with col2:
        st.markdown("- ✅ Side-by-Side Comparison\n- ✅ Export Results\n- ✅ State Metrics\n- ✅ Interactive UI\n- ✅ Step-by-Step Forms")
    
    st.markdown("---")
    st.header("📖 Example NFA")
    st.markdown("Simple NFA accepting strings with ≥1 'a' followed by ≥1 'b':")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.json({"states": ["q0", "q1", "q2"], "alphabet": ["a", "b"], "start_state": "q0", "final_states": ["q2"],
                 "transitions": {"q0": {"a": ["q0", "q1"], "b": ["q0"]}, "q1": {"b": ["q2"]}, 
                                "q2": {"a": ["q2"], "b": ["q2"]}}})
    with col2:
        st.markdown("**Accepts:** `aab`, `aaabbb`, `baaab`\n**Rejects:** `aaa`, `bbb`, `ab`\n\n3 states, non-deterministic at q0. Use Manual Builder to create similar NFAs!")
    
    st.markdown("---")
    st.header("🧮 Subset Construction Algorithm")
    with st.expander("📚 How It Works"):
        st.markdown("1. **Initialize** with NFA start state\n2. **Process** each DFA state (set of NFA states)\n3. **Compute** reachable states for each symbol\n4. **Mark** final states containing NFA final states\n\n**Complexity:** O(2^n) worst case")
    
    st.markdown("---")
    st.markdown("""<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>NFA → DFA Visualizer v3.0</strong> • Built with Streamlit<br>
    💡 Tip: NFAs can have multiple transitions per input, DFAs have exactly one</p>
    </div>""", unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("📋 Navigation")
        for emoji, name, page in [("📝", "Manual Builder", "pages/1_📝_Manual_Builder.py"),
                                   ("", "Convert & Visualize", "pages/3_🔄_Convert_NFA_DFA.py"),
                                   ("ℹ️", "About & Help", "pages/4_ℹ️_About.py")]:
            if st.button(f"{emoji} {name}", use_container_width=True):
                st.switch_page(page)
        
        st.markdown("---")
        if 'nfa_data' in st.session_state:
            st.success("✅ NFA Loaded")
            nfa = st.session_state['nfa_data']
            st.metric("States", len(nfa.get('states', [])))
            st.metric("Alphabet Size", len(nfa.get('alphabet', [])))
            if st.button("🗑️ Clear NFA", use_container_width=True):
                for key in ['nfa_data', 'dfa_data', 'conversion_logs']:
                    st.session_state.pop(key, None)
                st.rerun()
        else:
            st.info("ℹ️ No NFA loaded yet")

if __name__ == "__main__":
    main()
