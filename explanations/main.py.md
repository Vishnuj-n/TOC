# main.py - Streamlit Application Entry Point

## Overview

`main.py` is the core Streamlit web application that provides the user interface for NFA to DFA conversion. It orchestrates all components of the system including input handling, conversion processing, visualization, and result presentation.

**File Statistics:**
- **Lines of Code:** 241
- **Main Functions:** 3
- **UI Components:** 4 input methods, 2 tabbed views
- **Dependencies:** streamlit, nfa_to_dfa, gemini_importer, graph_visualizer (optional)

---

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────┐
│              Streamlit Application                  │
├─────────────────────────────────────────────────────┤
│  1. Page Configuration                              │
│  2. Input Selection (Sidebar)                       │
│  3. Input Processing                                │
│  4. NFA Display (Graph + JSON)                      │
│  5. Conversion Button                               │
│  6. DFA Display (Graph + JSON)                      │
│  7. Comparison View                                 │
│  8. Export Options                                  │
└─────────────────────────────────────────────────────┘
```

### Component Interactions

```
User Input
    │
    ├─→ JSON (Paste/Upload)
    │       └─→ JSON Parser
    │              └─→ Validation
    │
    ├─→ Image (Upload/Camera)
    │       └─→ Gemini Vision API
    │              └─→ JSON Extraction
    │                     └─→ Validation
    │
    └─→ Validated NFA JSON
            │
            ├─→ Graph Visualizer (NFA Diagram)
            │
            └─→ NFA to DFA Converter
                    │
                    ├─→ Conversion Logs
                    │
                    ├─→ DFA JSON
                    │
                    └─→ Graph Visualizer (DFA Diagram)
```

---

## Code Structure

### 1. Imports and Configuration

```python
import streamlit as st
import json
from nfa_to_dfa import convert_nfa_to_dfa, validate_nfa
from gemini_importer import image_to_nfa_json

# Optional graph visualization
try:
    from graph_visualizer import (
        create_nfa_graph, create_dfa_graph,
        get_graph_svg, render_automaton_graph,
        compare_graphs
    )
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False
```

**Purpose:**
- Import core modules
- Attempt to import graph visualization (graceful fallback if unavailable)
- Set availability flag for conditional UI rendering

**Design Decision:** Optional graphviz dependency allows app to run even without visualization capabilities, improving user experience.

---

### 2. Page Configuration

```python
st.set_page_config(
    page_title="NFA to DFA Converter",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Configuration Options:**
- `page_title`: Browser tab title
- `page_icon`: Emoji favicon
- `layout`: Wide layout for side-by-side comparisons
- `initial_sidebar_state`: Sidebar open by default for input selection

**Why Wide Layout?** Enables side-by-side display of NFA and DFA graphs for easy comparison.

---

### 3. Input Methods (Sidebar)

#### Method 1: Paste JSON

```python
if input_method == "📝 Paste JSON":
    nfa_text = st.sidebar.text_area(
        "Paste NFA JSON:",
        height=300,
        help="Paste your NFA in JSON format"
    )
    if nfa_text:
        try:
            nfa_data = json.loads(nfa_text)
            st.session_state.nfa_data = nfa_data
            st.sidebar.success("✅ JSON loaded!")
        except json.JSONDecodeError as e:
            st.sidebar.error(f"❌ Invalid JSON: {e}")
```

**Features:**
- Large text area for easy pasting
- Real-time JSON validation
- Error handling with user-friendly messages
- Immediate feedback (success/error)

**Session State:** Stores parsed NFA in `st.session_state.nfa_data` for persistence across reruns.

---

#### Method 2: Upload JSON File

```python
elif input_method == "📁 Upload JSON File":
    uploaded_file = st.sidebar.file_uploader(
        "Choose a JSON file",
        type=["json"],
        help="Upload a file containing your NFA"
    )
    if uploaded_file:
        try:
            nfa_data = json.load(uploaded_file)
            st.session_state.nfa_data = nfa_data
            st.sidebar.success(f"✅ Loaded {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
```

**Features:**
- File type restriction (`.json` only)
- Automatic JSON parsing
- Displays filename on success
- Exception handling for malformed files

**Security:** File type validation prevents execution of arbitrary files.

---

#### Method 3: Upload Image

```python
elif input_method == "📷 Upload Image":
    uploaded_image = st.sidebar.file_uploader(
        "Upload diagram image",
        type=["png", "jpg", "jpeg"],
        help="Upload an image of your NFA diagram"
    )
    if uploaded_image and st.sidebar.button("🧠 Extract with AI"):
        with st.spinner("Analyzing image with Gemini..."):
            try:
                result = image_to_nfa_json(uploaded_image)
                nfa_data = result["nfa_json"]
                st.session_state.nfa_data = nfa_data
                st.sidebar.success("✅ Extracted NFA from image!")
                st.sidebar.info(result["raw_response"][:200] + "...")
            except Exception as e:
                st.sidebar.error(f"❌ AI extraction failed: {e}")
```

**Features:**
- Image type validation (common formats)
- Explicit "Extract" button (prevents accidental API calls)
- Loading spinner for async operation
- Shows AI response preview
- Comprehensive error handling

**AI Integration:** Uses Google Gemini Vision API to parse hand-drawn or digital diagrams.

**Cost Consideration:** Button prevents automatic API calls on every rerun, saving API quota.

---

#### Method 4: Camera Capture

```python
elif input_method == "📸 Take Photo":
    camera_image = st.sidebar.camera_input("Capture NFA diagram")
    if camera_image and st.sidebar.button("🧠 Extract with AI"):
        with st.spinner("Analyzing photo with Gemini..."):
            try:
                result = image_to_nfa_json(camera_image)
                nfa_data = result["nfa_json"]
                st.session_state.nfa_data = nfa_data
                st.sidebar.success("✅ Extracted NFA from photo!")
                st.sidebar.info(result["raw_response"][:200] + "...")
            except Exception as e:
                st.sidebar.error(f"❌ AI extraction failed: {e}")
```

**Features:**
- Live camera access (with user permission)
- Mobile-friendly
- Same AI processing as image upload
- Instant capture and analysis

**Use Case:** Quickly digitize NFAs from textbooks, whiteboards, or paper diagrams.

---

### 4. Main Application Area

#### NFA Display Section

```python
st.title("🔄 NFA to DFA Converter")

if nfa_data:
    st.success("✅ NFA Loaded")
    
    # Validate NFA
    is_valid, error_msg = validate_nfa(nfa_data)
    
    if not is_valid:
        st.error(f"❌ Invalid NFA: {error_msg}")
        st.stop()
```

**Validation Flow:**
1. Check if NFA data exists in session state
2. Run validation using `validate_nfa()` from `nfa_to_dfa.py`
3. Display error and halt execution if invalid
4. Proceed to display if valid

**Validation Checks:**
- All required fields present
- Start state exists in states list
- Final states are subset of states
- Transitions reference valid states
- Alphabet matches transition symbols

---

#### Tabbed Interface for NFA

```python
nfa_tab1, nfa_tab2 = st.tabs(["📊 Graph", "📄 JSON"])

with nfa_tab1:
    if GRAPHVIZ_AVAILABLE:
        st.subheader("NFA State Diagram")
        try:
            nfa_graph = create_nfa_graph(nfa_data)
            svg_content = get_graph_svg(nfa_graph)
            st.image(svg_content, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to render graph: {e}")
    else:
        st.warning("⚠️ Graph visualization unavailable...")

with nfa_tab2:
    st.subheader("NFA JSON Structure")
    st.json(nfa_data)
```

**Tab 1: Graph Visualization**
- Conditional rendering based on graphviz availability
- Error handling for graph generation failures
- SVG rendering with responsive width

**Tab 2: JSON Display**
- Pretty-printed JSON with syntax highlighting
- Collapsible tree structure
- Copy-friendly format

**User Experience:** Tabs allow viewing both representations without scrolling, improving workflow efficiency.

---

#### Conversion Button

```python
if st.button("🚀 Convert to DFA", type="primary"):
    with st.spinner("Converting NFA to DFA..."):
        dfa_result = convert_nfa_to_dfa(nfa_data)
        st.session_state.dfa_result = dfa_result
```

**Button Features:**
- Primary styling (highlighted)
- Spinner for visual feedback during processing
- Result stored in session state for persistence

**State Management:** Storing in `session_state` prevents re-conversion on every interaction.

---

#### Conversion Logs Display

```python
if dfa_result:
    st.success("✅ Conversion Complete!")
    
    with st.expander("📋 Conversion Steps", expanded=False):
        for i, log in enumerate(dfa_result["logs"], 1):
            st.text(f"{i}. {log}")
```

**Features:**
- Collapsible expander (not expanded by default)
- Numbered logs for easy reference
- Step-by-step process visibility

**Educational Value:** Shows the subset construction algorithm in action, helping users understand the process.

---

#### DFA Display Section

```python
st.markdown("---")
st.subheader("📤 DFA Output")

dfa_data = dfa_result["dfa"]

dfa_tab1, dfa_tab2 = st.tabs(["📊 Graph", "📄 JSON"])

with dfa_tab1:
    if GRAPHVIZ_AVAILABLE:
        try:
            dfa_graph = create_dfa_graph(dfa_data)
            svg_content = get_graph_svg(dfa_graph)
            st.image(svg_content, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to render DFA graph: {e}")
    else:
        st.warning("⚠️ Graph visualization unavailable...")

with dfa_tab2:
    st.json(dfa_data)
```

**Mirror Structure:** Same tabbed interface as NFA for consistency.

**Comparison Aid:** Parallel structure makes it easy to compare input and output.

---

#### Comparison View

```python
st.markdown("---")
st.subheader("📊 Comparison")

col1, col2 = st.columns(2)

with col1:
    st.metric("NFA States", len(nfa_data["states"]))
    st.metric("NFA Transitions", sum(len(v) for v in nfa_data["transitions"].values()))

with col2:
    st.metric("DFA States", len(dfa_data["states"]))
    st.metric("DFA Transitions", sum(len(v) for v in dfa_data["transitions"].values()))

if len(dfa_data["states"]) > len(nfa_data["states"]) * 2:
    st.warning("⚠️ State explosion detected! DFA has significantly more states than NFA.")
```

**Metrics:**
- State count comparison
- Transition count comparison
- State explosion warning

**Educational Insight:** Highlights the potential exponential growth in DFA state space.

---

#### Side-by-Side Graph Comparison

```python
if GRAPHVIZ_AVAILABLE:
    st.markdown("---")
    st.subheader("🔄 Side-by-Side Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**NFA**")
        nfa_graph = create_nfa_graph(nfa_data)
        svg_nfa = get_graph_svg(nfa_graph)
        st.image(svg_nfa, use_container_width=True)
    
    with col2:
        st.markdown("**DFA**")
        dfa_graph = create_dfa_graph(dfa_data)
        svg_dfa = get_graph_svg(dfa_graph)
        st.image(svg_dfa, use_container_width=True)
```

**Layout:** Two-column layout for direct visual comparison.

**Visual Learning:** Helps users see the structural differences between NFA and DFA.

---

#### Export Functionality

```python
st.markdown("---")
st.subheader("💾 Export")

col1, col2 = st.columns(2)

with col1:
    dfa_json = json.dumps(dfa_data, indent=2)
    st.download_button(
        label="📥 Download DFA JSON",
        data=dfa_json,
        file_name="dfa_output.json",
        mime="application/json"
    )

with col2:
    if GRAPHVIZ_AVAILABLE:
        st.download_button(
            label="📥 Download DFA Graph (SVG)",
            data=svg_dfa,
            file_name="dfa_graph.svg",
            mime="image/svg+xml"
        )
```

**Export Options:**
- JSON format (for programmatic use)
- SVG format (for presentations)
- Descriptive filenames
- Proper MIME types

**Workflow Integration:** Allows users to integrate results into other tools or documentation.

---

## Session State Management

### State Variables

```python
st.session_state.nfa_data      # Stores loaded NFA JSON
st.session_state.dfa_result    # Stores conversion results
```

**Purpose:** Persist data across Streamlit reruns (every interaction triggers a rerun).

**Why Needed?** Without session state:
- NFA would be lost after clicking "Convert"
- DFA would be recalculated on every interaction
- User experience would be poor

---

## Error Handling Strategy

### 1. JSON Parsing Errors

```python
try:
    nfa_data = json.loads(nfa_text)
except json.JSONDecodeError as e:
    st.sidebar.error(f"❌ Invalid JSON: {e}")
```

**Handles:** Syntax errors in pasted JSON.

---

### 2. File Upload Errors

```python
try:
    nfa_data = json.load(uploaded_file)
except Exception as e:
    st.sidebar.error(f"❌ Error: {e}")
```

**Handles:** File reading errors, encoding issues, non-JSON files.

---

### 3. AI Extraction Errors

```python
try:
    result = image_to_nfa_json(uploaded_image)
except Exception as e:
    st.sidebar.error(f"❌ AI extraction failed: {e}")
```

**Handles:** API errors, rate limits, invalid images, network issues.

---

### 4. Graph Rendering Errors

```python
try:
    nfa_graph = create_nfa_graph(nfa_data)
    svg_content = get_graph_svg(nfa_graph)
except Exception as e:
    st.error(f"Failed to render graph: {e}")
```

**Handles:** Graphviz errors, invalid state diagrams, rendering failures.

---

### 5. Validation Errors

```python
is_valid, error_msg = validate_nfa(nfa_data)
if not is_valid:
    st.error(f"❌ Invalid NFA: {error_msg}")
    st.stop()
```

**Handles:** Structural NFA errors, missing fields, invalid references.

---

## Design Patterns Used

### 1. Graceful Degradation

**Pattern:** Optional graphviz import with fallback UI.

```python
try:
    from graph_visualizer import ...
    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

# Later...
if GRAPHVIZ_AVAILABLE:
    # Render graphs
else:
    st.warning("Graph visualization unavailable")
```

**Benefit:** App remains functional even without optional dependencies.

---

### 2. Lazy Execution

**Pattern:** AI extraction only on button click.

```python
if uploaded_image and st.sidebar.button("🧠 Extract with AI"):
    # Expensive API call here
```

**Benefit:** Prevents accidental API calls, saves costs, improves performance.

---

### 3. State Preservation

**Pattern:** Using `st.session_state` for data persistence.

```python
st.session_state.nfa_data = nfa_data
st.session_state.dfa_result = dfa_result
```

**Benefit:** Data survives Streamlit reruns, better UX.

---

### 4. Separation of Concerns

**Pattern:** UI logic separated from business logic.

- `main.py`: UI and orchestration
- `nfa_to_dfa.py`: Conversion algorithm
- `gemini_importer.py`: AI integration
- `graph_visualizer.py`: Graph rendering

**Benefit:** Maintainable, testable, reusable code.

---

## Performance Considerations

### 1. Avoid Redundant Computations

✅ **Good:** Store DFA result in session state
```python
st.session_state.dfa_result = convert_nfa_to_dfa(nfa_data)
```

❌ **Bad:** Recompute on every rerun
```python
dfa_result = convert_nfa_to_dfa(nfa_data)  # Runs on every interaction!
```

---

### 2. Conditional Rendering

Only render graphs if graphviz is available:
```python
if GRAPHVIZ_AVAILABLE:
    # Render graphs
else:
    # Show warning
```

---

### 3. Lazy Loading

Don't convert until user clicks button:
```python
if st.button("🚀 Convert to DFA"):
    # Only now run conversion
```

---

## User Experience Enhancements

### 1. Visual Feedback

- ✅ Success messages (green)
- ❌ Error messages (red)
- ⚠️ Warnings (yellow)
- ℹ️ Info messages (blue)
- 🔄 Loading spinners

---

### 2. Helpful Icons

- 📝 Paste JSON
- 📁 Upload File
- 📷 Upload Image
- 📸 Take Photo
- 🚀 Convert Button
- 📊 Graph Tab
- 📄 JSON Tab
- 💾 Export Section

**Purpose:** Visual hierarchy and easy scanning.

---

### 3. Informative Help Text

```python
st.sidebar.text_area(
    "Paste NFA JSON:",
    help="Paste your NFA in JSON format"
)
```

**Benefit:** Contextual guidance without cluttering UI.

---

### 4. Responsive Layout

```python
st.set_page_config(layout="wide")
```

**Benefit:** Better use of screen space for graph comparisons.

---

## Security Considerations

### 1. File Type Validation

```python
uploaded_file = st.sidebar.file_uploader(
    "Choose a JSON file",
    type=["json"]
)
```

**Protection:** Prevents execution of malicious file types.

---

### 2. API Key Protection

```python
# In gemini_importer.py
api_key = st.secrets["GEMINI_API_KEY"]
```

**Protection:** API keys in `.streamlit/secrets.toml`, never in code.

---

### 3. Input Validation

```python
is_valid, error_msg = validate_nfa(nfa_data)
if not is_valid:
    st.error(error_msg)
    st.stop()
```

**Protection:** Validates all user input before processing.

---

## Common Issues and Solutions

### Issue 1: Graphviz Not Available

**Symptom:** Graphs don't render, warning message shown.

**Solution:**
1. Install Graphviz software: `choco install graphviz` (Windows)
2. Install Python package: `pip install graphviz`
3. Restart Streamlit

---

### Issue 2: State Not Persisting

**Symptom:** Data lost after interactions.

**Cause:** Not using session state.

**Solution:** Always store in `st.session_state`:
```python
st.session_state.nfa_data = nfa_data
```

---

### Issue 3: JSON Parse Errors

**Symptom:** "Invalid JSON" error.

**Cause:** Malformed JSON syntax.

**Solution:** Validate JSON in external tool first, or use examples from `examples/` folder.

---

### Issue 4: AI Extraction Fails

**Symptom:** "AI extraction failed" error.

**Possible Causes:**
- Missing API key in secrets
- Rate limit exceeded
- Poor image quality
- Network issues

**Solutions:**
- Check `.streamlit/secrets.toml`
- Wait and retry
- Use clearer image
- Check internet connection

---

## Testing Recommendations

### Unit Tests Needed

```python
# test_main.py (not yet implemented)

def test_validate_uploaded_file():
    # Test file type validation
    pass

def test_session_state_persistence():
    # Test state management
    pass

def test_error_handling():
    # Test various error scenarios
    pass
```

---

### Integration Tests Needed

```python
# test_integration.py (not yet implemented)

def test_full_conversion_workflow():
    # Test complete NFA -> DFA flow
    pass

def test_graph_generation_integration():
    # Test graph visualization integration
    pass
```

---

## Future Enhancements

### 1. Batch Processing

Allow users to upload multiple NFAs at once:
```python
uploaded_files = st.sidebar.file_uploader(
    "Choose JSON files",
    type=["json"],
    accept_multiple_files=True
)
```

---

### 2. Export to Other Formats

Add PDF, PNG export options:
```python
st.download_button(
    label="Download as PDF",
    data=pdf_bytes,
    file_name="dfa.pdf",
    mime="application/pdf"
)
```

---

### 3. Undo/Redo Functionality

Track history in session state:
```python
if 'history' not in st.session_state:
    st.session_state.history = []

if st.button("Undo"):
    st.session_state.nfa_data = st.session_state.history.pop()
```

---

### 4. String Acceptance Testing

Allow users to test strings:
```python
test_string = st.text_input("Test string:")
if st.button("Test"):
    result = test_string_acceptance(dfa_data, test_string)
    st.success(f"String {'accepted' if result else 'rejected'}")
```

---

### 5. Dark Mode Support

Detect and adapt to theme:
```python
theme = st.get_option("theme.base")
if theme == "dark":
    # Use dark theme colors for graphs
```

---

## Dependencies

### Required

- **streamlit** - Web framework
- **json** - JSON parsing (built-in)

### Core Modules

- **nfa_to_dfa** - Conversion algorithm
- **gemini_importer** - AI vision integration

### Optional

- **graph_visualizer** - Graph visualization

---

## Configuration

### Streamlit Config

Located in `.streamlit/config.toml` (if exists):

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
port = 8501
enableCORS = false
```

---

### Secrets Config

Located in `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-api-key-here"
```

**Never commit this file to version control!**

---

## Running the Application

### Development Mode

```powershell
streamlit run main.py
```

### Debug Mode

```powershell
streamlit run main.py --logger.level=debug
```

### Custom Port

```powershell
streamlit run main.py --server.port=8080
```

### Network Access

```powershell
streamlit run main.py --server.address=0.0.0.0
```

---

## Conclusion

`main.py` is the heart of the NFA to DFA Visualizer, providing an intuitive, feature-rich web interface for automata conversion. Its design prioritizes:

- **User Experience** - Clear UI, helpful feedback, responsive layout
- **Robustness** - Comprehensive error handling, validation
- **Flexibility** - Multiple input methods, optional features
- **Performance** - Efficient state management, lazy execution
- **Maintainability** - Clean separation of concerns, extensible architecture

The modular design makes it easy to add new features, while the graceful degradation pattern ensures reliability even when optional components are unavailable.
