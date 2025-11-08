"""Convert NFA to DFA Page

Convert loaded NFAs to DFAs and visualize the results.
"""

import streamlit as st
import json
from nfa_to_dfa import convert_nfa_to_dfa, validate_nfa

# Try to import graph visualization (optional)
try:
    from graph_visualizer import get_graph_svg, compare_graphs
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

st.set_page_config(
    page_title="Convert NFA to DFA",
    page_icon="🔄",
    layout="wide"
)


def main():
    """Convert and visualize page."""
    
    st.title("🔄 Convert NFA to DFA")
    st.markdown("""
    Transform your NFA into an equivalent DFA using the subset construction algorithm.
    """)
    
    # Check if NFA is loaded
    if 'nfa_data' not in st.session_state:
        st.warning("⚠️ No NFA loaded yet!")
        st.info("👈 Please create or import an NFA first.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Manual Builder")
            st.markdown("Build an NFA step-by-step using forms")
            if st.button("Go to Manual Builder →", use_container_width=True):
                st.switch_page("pages/1_📝_Manual_Builder.py")
        
        with col2:
            st.markdown("### 📤 Import JSON")
            st.markdown("Upload or paste an existing NFA")
            if st.button("Go to Import JSON →", use_container_width=True):
                st.switch_page("pages/2_📤_Import_JSON.py")
        
        st.stop()
    
    nfa_data = st.session_state['nfa_data']
    
    # Display NFA Information
    st.header("📥 Input NFA")
    
    # Create tabs for NFA views
    if GRAPH_AVAILABLE:
        tab1, tab2, tab3 = st.tabs(["📊 Graph", "📋 JSON", "📈 Summary"])
        
        with tab1:
            try:
                svg_graph = get_graph_svg(nfa_data, "Input NFA")
                st.image(svg_graph, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to generate graph: {e}")
                st.info("💡 Make sure Graphviz is installed on your system: https://graphviz.org/download/")
    else:
        st.warning("⚠️ Graph visualization not available. Install 'graphviz' package and Graphviz software for visual diagrams.")
        tab2, tab3 = st.tabs(["📋 JSON", "📈 Summary"])
    
    with tab2:
        st.json(nfa_data)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("States", len(nfa_data["states"]))
            st.metric("Alphabet Size", len(nfa_data["alphabet"]))
            st.metric("Final States", len(nfa_data["final_states"]))
        
        with col2:
            st.markdown("**States:** " + ", ".join(f"`{s}`" for s in nfa_data["states"]))
            st.markdown("**Alphabet:** " + ", ".join(f"`{s}`" for s in nfa_data["alphabet"]))
            st.markdown("**Start State:** " + f"`{nfa_data['start_state']}`")
            st.markdown("**Final States:** " + ", ".join(f"`{s}`" for s in nfa_data["final_states"]))
    
    st.markdown("---")
    
    # Conversion Controls
    st.header("⚙️ Conversion")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🚀 Convert to DFA", type="primary", use_container_width=True):
            try:
                with st.spinner("⚙️ Running subset construction algorithm..."):
                    dfa, logs = convert_nfa_to_dfa(nfa_data)
                
                # Store in session state
                st.session_state['dfa_data'] = dfa
                st.session_state['conversion_logs'] = logs
                st.session_state['converted'] = True
                
                st.success("✅ Conversion completed successfully!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Conversion failed: {e}")
                import traceback
                with st.expander("🐛 Error Details"):
                    st.code(traceback.format_exc())
    
    with col2:
        if st.button("🔄 Reload NFA", use_container_width=True):
            if 'dfa_data' in st.session_state:
                del st.session_state['dfa_data']
            if 'conversion_logs' in st.session_state:
                del st.session_state['conversion_logs']
            if 'converted' in st.session_state:
                del st.session_state['converted']
            st.rerun()
    
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("main.py")
    
    # Display results if conversion has been done
    if 'converted' in st.session_state and st.session_state.get('converted', False):
        
        st.markdown("---")
        
        # Conversion Log
        st.header("📝 Conversion Log")
        st.markdown("Step-by-step trace of the subset construction algorithm:")
        
        with st.expander("🔍 View Algorithm Trace", expanded=False):
            log_text = "\n".join(st.session_state['conversion_logs'])
            st.text_area("Algorithm Trace", log_text, height=400, label_visibility="collapsed")
        
        st.markdown("---")
        
        # DFA Output
        st.header("🎯 DFA Output")
        
        dfa_data = st.session_state['dfa_data']
        
        # Create tabs for DFA views
        if GRAPH_AVAILABLE:
            dfa_tab1, dfa_tab2, dfa_tab3, dfa_tab4 = st.tabs(["📊 Graph", "🔄 Comparison", "📋 JSON", "📈 Summary"])
            
            with dfa_tab1:
                try:
                    dfa_svg_graph = get_graph_svg(dfa_data, "Output DFA")
                    st.image(dfa_svg_graph, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to generate graph: {e}")
            
            with dfa_tab2:
                try:
                    st.subheader("Side-by-Side Comparison")
                    comparison_graph = compare_graphs(nfa_data, dfa_data)
                    comparison_svg = comparison_graph.pipe(format='svg').decode('utf-8')
                    st.image(comparison_svg, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to generate comparison: {e}")
        else:
            dfa_tab3, dfa_tab4 = st.tabs(["📋 JSON", "📈 Summary"])
        
        with dfa_tab3:
            dfa_json = json.dumps(dfa_data, indent=2)
            st.code(dfa_json, language="json")
            
            # Download button
            st.download_button(
                label="💾 Download DFA JSON",
                data=dfa_json,
                file_name="dfa.json",
                mime="application/json",
                use_container_width=True
            )
        
        with dfa_tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("States", len(dfa_data["states"]))
                st.metric("Alphabet Size", len(dfa_data["alphabet"]))
                st.metric("Final States", len(dfa_data["final_states"]))
            
            with col2:
                st.markdown("**States:** " + ", ".join(f"`{s}`" for s in dfa_data["states"]))
                st.markdown("**Start State:** " + f"`{dfa_data['start_state']}`")
                st.markdown("**Final States:** " + ", ".join(f"`{s}`" for s in dfa_data["final_states"]))
            
            # State explosion analysis
            st.markdown("---")
            st.subheader("📊 Comparison Metrics")
            
            nfa_state_count = len(nfa_data["states"])
            dfa_state_count = len(dfa_data["states"])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("NFA States", nfa_state_count)
            
            with col2:
                st.metric("DFA States", dfa_state_count)
            
            with col3:
                ratio = dfa_state_count / nfa_state_count if nfa_state_count > 0 else 0
                st.metric("Ratio (DFA/NFA)", f"{ratio:.2f}x")
            
            # Analysis
            if dfa_state_count > nfa_state_count * 2:
                st.warning(f"⚠️ State explosion detected! DFA has {dfa_state_count} states vs {nfa_state_count} in NFA")
            elif dfa_state_count < nfa_state_count:
                st.success(f"✅ DFA is more compact! {dfa_state_count} states vs {nfa_state_count} in NFA")
            else:
                st.info(f"ℹ️ Similar complexity: {dfa_state_count} DFA states vs {nfa_state_count} NFA states")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Current NFA")
        
        if 'nfa_data' in st.session_state:
            nfa = st.session_state['nfa_data']
            st.metric("States", len(nfa.get('states', [])))
            st.metric("Alphabet Size", len(nfa.get('alphabet', [])))
            st.metric("Final States", len(nfa.get('final_states', [])))
            
            st.markdown("---")
            
            if st.button("🗑️ Clear NFA", use_container_width=True):
                del st.session_state['nfa_data']
                if 'dfa_data' in st.session_state:
                    del st.session_state['dfa_data']
                if 'conversion_logs' in st.session_state:
                    del st.session_state['conversion_logs']
                if 'converted' in st.session_state:
                    del st.session_state['converted']
                st.rerun()
        
        st.markdown("---")
        
        st.header("ℹ️ About Conversion")
        
        st.markdown("""
        ### Subset Construction
        
        The algorithm creates DFA states from sets of NFA states:
        
        1. Start with {initial state}
        2. For each DFA state and symbol:
           - Find all reachable NFA states
           - Create new DFA state if needed
        3. Mark DFA states containing NFA final states as final
        
        ### Complexity
        - **Time**: O(2^n × |Σ|)
        - **Space**: O(2^n)
        
        where n = NFA states, |Σ| = alphabet size
        """)


if __name__ == "__main__":
    main()
