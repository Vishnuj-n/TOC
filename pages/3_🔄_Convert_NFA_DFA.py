"""Convert NFA to DFA Page"""
import streamlit as st
import json
from nfa_to_dfa import convert_nfa_to_dfa, validate_nfa

try:
    from graph_visualizer import get_graph_svg, compare_graphs
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

st.set_page_config(page_title="Convert NFA to DFA", page_icon="🔄", layout="wide")

def main():
    st.title("🔄 Convert NFA to DFA")
    st.markdown("Transform your NFA into an equivalent DFA using subset construction.")
    
    if 'nfa_data' not in st.session_state:
        st.warning("⚠️ No NFA loaded yet!")
        st.info("👈 Create an NFA first using the Manual Builder.")
        st.markdown("### 📝 Manual Builder\nBuild step-by-step")
        if st.button("Go to Manual Builder →", use_container_width=True, type="primary"):
            st.switch_page("pages/1_📝_Manual_Builder.py")
        st.stop()
    
    nfa_data = st.session_state['nfa_data']
    
    st.header("📥 Input NFA")
    tabs = ["📊 Graph", "📋 JSON", "📈 Summary"] if GRAPH_AVAILABLE else ["📋 JSON", "📈 Summary"]
    tab_objs = st.tabs(tabs)
    
    if GRAPH_AVAILABLE:
        with tab_objs[0]:
            try:
                st.image(get_graph_svg(nfa_data, "Input NFA"), use_container_width=True)
            except Exception as e:
                st.error(f"Failed: {e}")
                st.info("💡 Install Graphviz: https://graphviz.org/download/")
        json_tab, summary_tab = tab_objs[1], tab_objs[2]
    else:
        st.warning("⚠️ Graph visualization unavailable. Install 'graphviz'.")
        json_tab, summary_tab = tab_objs[0], tab_objs[1]
    
    with json_tab:
        st.json(nfa_data)
    
    with summary_tab:
        col1, col2 = st.columns(2)
        with col1:
            for label, key in [("States", "states"), ("Alphabet Size", "alphabet"), ("Final States", "final_states")]:
                st.metric(label, len(nfa_data[key]))
        with col2:
            st.markdown("**States:** " + ", ".join(f"`{s}`" for s in nfa_data["states"]))
            st.markdown(f"**Start:** `{nfa_data['start_state']}`")
            st.markdown("**Finals:** " + ", ".join(f"`{s}`" for s in nfa_data["final_states"]))
    
    st.markdown("---")
    st.header("⚙️ Conversion")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Convert to DFA", type="primary", use_container_width=True):
            try:
                with st.spinner("⚙️ Running algorithm..."):
                    dfa, logs = convert_nfa_to_dfa(nfa_data)
                st.session_state.update({'dfa_data': dfa, 'conversion_logs': logs, 'converted': True})
                st.success("✅ Conversion complete!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Failed: {e}")
    
    with col2:
        if st.button("🔄 Reload NFA", use_container_width=True):
            for key in ['dfa_data', 'conversion_logs', 'converted']:
                st.session_state.pop(key, None)
            st.rerun()
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("main.py")
    
    if st.session_state.get('converted', False):
        st.markdown("---")
        st.header("📝 Conversion Log")
        with st.expander("🔍 View Algorithm Trace", expanded=False):
            st.text_area("Algorithm Trace", "\n".join(st.session_state['conversion_logs']), 
                        height=400, label_visibility="collapsed")
        
        st.markdown("---")
        st.header("🎯 DFA Output")
        dfa_data = st.session_state['dfa_data']
        
        dfa_tabs = ["📊 Graph", "🔄 Comparison", "📋 JSON", "📈 Summary"] if GRAPH_AVAILABLE else ["📋 JSON", "📈 Summary"]
        dfa_tab_objs = st.tabs(dfa_tabs)
        
        if GRAPH_AVAILABLE:
            with dfa_tab_objs[0]:
                try:
                    st.image(get_graph_svg(dfa_data, "Output DFA"), use_container_width=True)
                except Exception as e:
                    st.error(f"Failed: {e}")
            
            with dfa_tab_objs[1]:
                try:
                    comp = compare_graphs(nfa_data, dfa_data)
                    st.image(comp.pipe(format='svg').decode('utf-8'), use_container_width=True)
                except Exception as e:
                    st.error(f"Failed: {e}")
            json_tab, summary_tab = dfa_tab_objs[2], dfa_tab_objs[3]
        else:
            json_tab, summary_tab = dfa_tab_objs[0], dfa_tab_objs[1]
        
        with json_tab:
            dfa_json = json.dumps(dfa_data, indent=2)
            st.code(dfa_json, language="json")
            st.download_button("💾 Download DFA JSON", dfa_json, "dfa.json", 
                             "application/json", use_container_width=True)
        
        with summary_tab:
            col1, col2 = st.columns(2)
            with col1:
                for label, key in [("States", "states"), ("Alphabet", "alphabet"), ("Finals", "final_states")]:
                    st.metric(label, len(dfa_data[key]))
            with col2:
                st.markdown("**States:** " + ", ".join(f"`{s}`" for s in dfa_data["states"]))
                st.markdown(f"**Start:** `{dfa_data['start_state']}`")
                st.markdown("**Finals:** " + ", ".join(f"`{s}`" for s in dfa_data["final_states"]))
            
            st.markdown("---")
            st.subheader("📊 Comparison")
            nfa_cnt, dfa_cnt = len(nfa_data["states"]), len(dfa_data["states"])
            col1, col2, col3 = st.columns(3)
            col1.metric("NFA States", nfa_cnt)
            col2.metric("DFA States", dfa_cnt)
            col3.metric("Ratio", f"{dfa_cnt/nfa_cnt:.2f}x" if nfa_cnt > 0 else "N/A")
            
            if dfa_cnt > nfa_cnt * 2:
                st.warning(f"⚠️ State explosion! {dfa_cnt} vs {nfa_cnt}")
            elif dfa_cnt < nfa_cnt:
                st.success(f"✅ DFA more compact! {dfa_cnt} vs {nfa_cnt}")
            else:
                st.info(f"ℹ️ Similar: {dfa_cnt} vs {nfa_cnt}")
    
    with st.sidebar:
        st.header("🎯 Current NFA")
        if 'nfa_data' in st.session_state:
            nfa = st.session_state['nfa_data']
            st.metric("States", len(nfa.get('states', [])))
            st.metric("Alphabet", len(nfa.get('alphabet', [])))
            st.markdown("---")
            if st.button("🗑️ Clear NFA", use_container_width=True):
                for key in ['nfa_data', 'dfa_data', 'conversion_logs', 'converted']:
                    st.session_state.pop(key, None)
                st.rerun()
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.markdown("""### Subset Construction
1. Start with {initial}
2. For each state & symbol: find reachable NFA states
3. Mark DFA states with NFA finals as final

**Complexity:** O(2^n × |Σ|)""")

if __name__ == "__main__":
    main()
