"""Streamlit-based UI for NFA to DFA conversion.

This is the main entry point for the Automaton Visualizer web application.
It provides multiple input methods and displays the conversion process.

Run with: streamlit run main.py
"""

import json
import io
from typing import Optional

import streamlit as st

from nfa_to_dfa import convert_nfa_to_dfa, validate_nfa
from gemini_importer import image_to_nfa_json

# Try to import graph visualization (optional)
try:
    from graph_visualizer import get_graph_svg, compare_graphs
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False
    st.warning("⚠️ Graph visualization not available. Install 'graphviz' package and Graphviz software for visual diagrams.")


# Page configuration
st.set_page_config(
    page_title="NFA → DFA Visualizer",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_json_from_text(text: str) -> Optional[dict]:
    """Parse JSON text into a dictionary.
    
    Args:
        text: JSON string
    
    Returns:
        Parsed dictionary or None if invalid
    """
    try:
        return json.loads(text)
    except Exception:
        return None


def main():
    """Main application entry point."""
    
    # Title and description
    st.title("🔄 NFA → DFA Visualizer")
    st.markdown("""
    Convert a **Non-deterministic Finite Automaton (NFA)** to a 
    **Deterministic Finite Automaton (DFA)** using the subset construction algorithm.
    """)
    
    # Sidebar for input
    st.sidebar.header("📥 Input")
    st.sidebar.markdown("Choose how to provide your NFA:")
    
    input_mode = st.sidebar.radio(
        "Input Method:",
        ["Paste JSON", "Upload JSON", "Upload Image", "Camera"],
        help="Select how you want to input your NFA"
    )
    
    nfa_data = None
    
    # Handle different input modes
    if input_mode == "Paste JSON":
        st.sidebar.markdown("Paste your NFA JSON below:")
        text = st.sidebar.text_area(
            "NFA JSON",
            height=300,
            placeholder='{\n  "states": ["q0", "q1"],\n  "alphabet": ["a", "b"],\n  ...\n}'
        )
        
        if text:
            nfa_data = load_json_from_text(text)
            if nfa_data is None:
                st.sidebar.error("❌ Invalid JSON format")
    
    elif input_mode == "Upload JSON":
        uploaded = st.sidebar.file_uploader(
            "Upload NFA JSON file",
            type=["json"],
            help="Select a .json file containing your NFA specification"
        )
        
        if uploaded is not None:
            try:
                nfa_data = json.load(uploaded)
            except Exception as e:
                st.sidebar.error(f"❌ Failed to read JSON: {e}")
    
    elif input_mode == "Upload Image":
        st.sidebar.markdown("Upload a photo of your NFA diagram:")
        img = st.sidebar.file_uploader(
            "NFA Diagram Image",
            type=["png", "jpg", "jpeg", "bmp"],
            help="Upload an image of a hand-drawn or computer-generated NFA diagram"
        )
        
        if img is not None:
            # Display the uploaded image
            st.sidebar.image(img, caption="Uploaded Image", use_container_width=True)
            
            img_bytes = img.read()
            
            # Process button
            if st.sidebar.button("🔍 Extract NFA from Image", type="primary"):
                with st.spinner("🤖 Analyzing image with Gemini AI..."):
                    try:
                        nfa_data = image_to_nfa_json(img_bytes)
                        st.sidebar.success("✅ NFA extracted successfully!")
                    except Exception as e:
                        st.sidebar.error(f"❌ Image import failed: {e}")
    
    elif input_mode == "Camera":
        st.sidebar.markdown("Take a photo of your NFA diagram:")
        cam = st.sidebar.camera_input("Capture NFA Diagram")
        
        if cam is not None:
            img_bytes = cam.read()
            
            # Process button
            if st.sidebar.button("🔍 Extract NFA from Photo", type="primary"):
                with st.spinner("🤖 Analyzing photo with Gemini AI..."):
                    try:
                        nfa_data = image_to_nfa_json(img_bytes)
                        st.sidebar.success("✅ NFA extracted successfully!")
                    except Exception as e:
                        st.sidebar.error(f"❌ Image import failed: {e}")
    
    # Main content area
    st.header("📋 NFA Input Preview")
    
    if nfa_data is None:
        st.info("👈 No NFA loaded yet. Choose an input method from the sidebar.")
        
        # Show example
        with st.expander("📖 Example NFA JSON Format"):
            example_nfa = {
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
            }
            st.json(example_nfa)
            st.markdown("""
            **This NFA accepts strings that:**
            - Contain at least one 'a' followed by at least one 'b'
            - Example accepted: "aaab", "aabbb", "baaab"
            - Example rejected: "aaa", "bbb", "ab" (need more symbols)
            """)
        
        st.stop()
    
    # Validate NFA
    is_valid, error_msg = validate_nfa(nfa_data)
    
    if not is_valid:
        st.error(f"❌ Invalid NFA: {error_msg}")
        st.stop()
    
    # Display NFA with Graph
    st.subheader("NFA Visualization")
    
    # Create tabs for different views
    if GRAPH_AVAILABLE:
        tab1, tab2, tab3 = st.tabs(["📊 Graph", "📋 JSON", "📈 Summary"])
        
        with tab1:
            try:
                # Generate and display NFA graph
                svg_graph = get_graph_svg(nfa_data, "Input NFA")
                st.image(svg_graph, use_container_width=True)
            except Exception as e:
                st.error(f"Failed to generate graph: {e}")
                st.info("💡 Make sure Graphviz is installed on your system: https://graphviz.org/download/")
    else:
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
            st.markdown("**States:** " + ", ".join(nfa_data["states"]))
            st.markdown("**Alphabet:** " + ", ".join(f"`{s}`" for s in nfa_data["alphabet"]))
            st.markdown("**Start State:** " + f"`{nfa_data['start_state']}`")
            st.markdown("**Final States:** " + ", ".join(f"`{s}`" for s in nfa_data["final_states"]))
    
    st.markdown("---")
    
    # Convert button
    if st.button("🚀 Convert to DFA", type="primary", use_container_width=True):
        try:
            with st.spinner("⚙️ Running subset construction algorithm..."):
                dfa, logs = convert_nfa_to_dfa(nfa_data)
            
            # Store in session state
            st.session_state.dfa = dfa
            st.session_state.logs = logs
            st.session_state.converted = True
            
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
            import traceback
            with st.expander("🐛 Error Details"):
                st.code(traceback.format_exc())
    
    # Display results if conversion has been done
    if "converted" in st.session_state and st.session_state.converted:
        st.success("✅ Conversion completed successfully!")
        
        # Conversion log
        st.header("📝 Conversion Log")
        st.markdown("Step-by-step trace of the subset construction algorithm:")
        
        log_text = "\n".join(st.session_state.logs)
        st.text_area("Algorithm Trace", log_text, height=400)
        
        st.markdown("---")
        
        # DFA output
        st.header("🎯 DFA Output")
        
        # Create tabs for DFA views
        if GRAPH_AVAILABLE:
            dfa_tab1, dfa_tab2, dfa_tab3, dfa_tab4 = st.tabs(["📊 Graph", "🔄 Comparison", "📋 JSON", "📈 Summary"])
            
            with dfa_tab1:
                try:
                    # Generate and display DFA graph
                    dfa_svg_graph = get_graph_svg(st.session_state.dfa, "Output DFA")
                    st.image(dfa_svg_graph, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to generate graph: {e}")
            
            with dfa_tab2:
                try:
                    # Generate comparison graph
                    st.subheader("Side-by-Side Comparison")
                    comparison_graph = compare_graphs(nfa_data, st.session_state.dfa)
                    comparison_svg = comparison_graph.pipe(format='svg').decode('utf-8')
                    st.image(comparison_svg, use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to generate comparison: {e}")
        else:
            dfa_tab3, dfa_tab4 = st.tabs(["📋 JSON", "📈 Summary"])
        
        with dfa_tab3:
            dfa_json = json.dumps(st.session_state.dfa, indent=2)
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
                st.metric("States", len(st.session_state.dfa["states"]))
                st.metric("Alphabet Size", len(st.session_state.dfa["alphabet"]))
                st.metric("Final States", len(st.session_state.dfa["final_states"]))
            
            with col2:
                st.markdown("**States:** " + ", ".join(st.session_state.dfa["states"]))
                st.markdown("**Start State:** " + f"`{st.session_state.dfa['start_state']}`")
                st.markdown("**Final States:** " + ", ".join(f"`{s}`" for s in st.session_state.dfa["final_states"]))
            
            # State explosion warning
            nfa_state_count = len(nfa_data["states"])
            dfa_state_count = len(st.session_state.dfa["states"])
            
            st.markdown("---")
            st.subheader("Comparison Metrics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("NFA States", nfa_state_count)
            with col2:
                st.metric("DFA States", dfa_state_count)
            with col3:
                ratio = dfa_state_count / nfa_state_count if nfa_state_count > 0 else 0
                st.metric("Ratio (DFA/NFA)", f"{ratio:.2f}x")
            
            if dfa_state_count > nfa_state_count * 2:
                st.warning(f"⚠️ State explosion detected! DFA has {dfa_state_count} states vs {nfa_state_count} in NFA")
            elif dfa_state_count < nfa_state_count:
                st.success(f"✅ DFA is more compact! {dfa_state_count} states vs {nfa_state_count} in NFA")
            else:
                st.info(f"ℹ️ Similar complexity: {dfa_state_count} DFA states vs {nfa_state_count} NFA states")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with Streamlit • Powered by Subset Construction Algorithm</p>
        <p>💡 Tip: NFAs can have multiple transitions per input, DFAs have exactly one</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
