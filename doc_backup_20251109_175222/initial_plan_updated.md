# NFA to DFA Visual Converter - Updated Plan for Streamlit

That's a fantastic idea. Using Gemini's vision capabilities to bridge the gap between a hand-drawn diagram and a usable JSON object is a perfect "add-on" feature.

Here is the updated project plan for your core application using **Streamlit** instead of Tkinter, with proper API key management through `.streamlit\secrets.toml`.

-----

## 1. 📋 Project Prompt: NFA to DFA Visual Converter

**Project Title:** Automaton Visualizer

**Objective:** Create a Python **Streamlit** web application that converts a Non-deterministic Finite Automaton (NFA) into an equivalent Deterministic Finite Automaton (DFA) using the Subset Construction algorithm. The tool will accept an NFA from multiple input sources (JSON text, JSON file, or image), display the step-by-step conversion process in a human-readable format, and allow the user to download the resulting DFA as a JSON file.

**Core Features (MVP):**

1.  **Web UI:** A clean and responsive web interface built with **Streamlit**.
    * Automatically handles layout, responsiveness, and state management
    * Easy to deploy and share via Streamlit Cloud or local hosting
    * Run with: `streamlit run main.py`

2.  **Multiple Input Methods:**
    * **Paste JSON:** Text area for direct JSON input
    * **Upload JSON:** File uploader for `.json` files
    * **Upload Image:** File uploader for hand-drawn NFA diagrams (`.png`, `.jpg`, `.jpeg`, `.bmp`)
    * **Camera Input:** Live camera capture for mobile/tablet users
    * Radio buttons in sidebar to switch between input modes

3.  **Core Logic (Separate Module - `nfa_to_dfa.py`):**
    * A Python function `convert_nfa_to_dfa(nfa_data)` that is completely independent of the Streamlit UI.
    * This function takes one argument: a Python dictionary (from the parsed JSON) representing the NFA.
    * It returns two items:
      1.  A dictionary representing the final DFA.
      2.  A list of strings, where each string is a log of one step in the algorithm (e.g., "Processing state {q0, q1}...", "On input 'a', new set is {q1, q2}").

4.  **UI Display Features:**
    * **NFA Input Preview:** Code block showing the loaded NFA JSON with syntax highlighting
    * **Convert Button:** Triggers the conversion algorithm
    * **Conversion Log:** Displays step-by-step process as text lines
    * **DFA Output:** Shows final DFA JSON with syntax highlighting
    * **Download Button:** Allows users to download the DFA as a JSON file
    * **Spinner:** Loading indicator during image processing via Gemini API

**Technology Stack:**

  * **Language:** Python 3.11+
  * **UI Framework:** Streamlit
  * **Data Format:** `json` (built-in)
  * **Image Processing:** Pillow (PIL)
  * **AI Vision:** Google Generative AI (Gemini)
  * **Testing:** pytest

**Dependencies (pyproject.toml):**
```toml
dependencies = [
    "streamlit",
    "pillow",
    "google-generativeai",
    "pytest",
]
```

-----

## 2. ✨ Feature Add-on: Gemini API for Image-to-JSON

This is your "add-on" that implements the Gemini Vision API. You will design this as a **separate module** (`gemini_importer.py`) so it doesn't break your core logic.

### How It Works (Streamlit Version):

Your main Streamlit application will have multiple input options in the sidebar. When the user selects "Upload Image" or "Camera":

1.  Streamlit's `file_uploader()` or `camera_input()` widget captures the image as **bytes**.
2.  The app calls `image_to_nfa_json(img_bytes)` from your `gemini_importer.py` module.
3.  This function uses the `google-generativeai` library to send the image bytes and a specific text prompt to the Gemini API.
4.  The Gemini API (using a vision model like `gemini-1.5-flash` or `gemini-1.5-pro`) analyzes the image and returns a JSON string.
5.  Your function parses this JSON string into a Python dictionary and returns it.
6.  Your main app treats this dictionary *exactly as if it had been loaded from a JSON file*.

### API Key Configuration (Critical Change):

**DO NOT hardcode the API key in your code.** Instead, use Streamlit's secrets management:

**File Structure:**
```
.streamlit/
    secrets.toml
```

**`.streamlit\secrets.toml` contents:**
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

**Accessing the key in code:**
```python
import streamlit as st

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
```

### Python Implementation (Updated for Streamlit):

**Installation:**
```bash
pip install google-generativeai pillow streamlit
```

**Module: `gemini_importer.py`**

Key differences from the original plan:
- ✅ Uses `st.secrets` instead of hardcoded API key
- ✅ Works with byte streams instead of file paths (Streamlit compatibility)
- ✅ Uses updated Gemini model names (`gemini-2.5-flash` or `gemini-2.5-pro`)
- ✅ Handles bytes input from Streamlit widgets
- ✅ Better error handling and JSON extraction

**Conceptual structure:**

```python
# gemini_importer.py
import google.generativeai as genai
from PIL import Image
import json
import io
import streamlit as st

# This is the crucial prompt you send along with the image
JSON_GENERATION_PROMPT = """
Analyze the attached image of a Non-deterministic Finite Automaton (NFA).
Extract all states, the alphabet, the start state, all final states, and all transitions.

The NFA has NO EPSILON transitions.

Respond with ONLY a valid JSON object in the following exact format. Do not include
any other text, explanations, or markdown formatting.

{
  "states": ["q0", "q1", ...],
  "alphabet": ["a", "b", ...],
  "start_state": "q_start",
  "final_states": ["q_final1", ...],
  "transitions": {
    "q0": {
      "a": ["q1"],
      "b": ["q0", "q2"]
    },
    "q1": {
      "b": ["q2"]
    }
  }
}

Rules:
- State names should be simple strings like "q0", "q1", etc.
- Each transition maps: source_state -> input_symbol -> list of destination states
- If a state has no transitions on a symbol, omit that symbol from its dictionary
- Be precise with the diagram's arrows and labels
"""

def image_to_nfa_json(img_bytes: bytes) -> dict:
    """
    Uses the Gemini API to convert an image (as bytes) of an NFA into a Python dict.
    
    Args:
        img_bytes: Image data as bytes (from Streamlit file_uploader or camera_input)
    
    Returns:
        dict: NFA data structure
    
    Raises:
        Exception: If API call fails or JSON parsing fails
    """
    try:
        # Load image from bytes
        img = Image.open(io.BytesIO(img_bytes))
        
        # Configure Gemini with API key from Streamlit secrets
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Use updated model name that supports vision
        # Options: 'gemini-1.5-flash' (faster, cheaper) or 'gemini-1.5-pro' (more accurate)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Send both the prompt and the image
        response = model.generate_content([JSON_GENERATION_PROMPT, img])
        
        # Extract text from response
        response_text = response.text.strip()
        
        # Clean up the response to get raw JSON
        # Sometimes the model adds ```json ... ```, so we strip it
        json_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Parse the JSON string into a Python dict
        nfa_data = json.loads(json_text)
        
        return nfa_data
        
    except Exception as e:
        raise Exception(f"Error with Gemini API: {e}")
```

### Integration with main.py:

The main Streamlit app already has the structure in place:

```python
# In main.py (conceptual snippet)
import streamlit as st
from gemini_importer import image_to_nfa_json

# Sidebar input selection
input_mode = st.sidebar.radio("Choose input type:", 
    ["Paste JSON", "Upload JSON", "Upload Image", "Camera"])

nfa_data = None

if input_mode == "Upload Image":
    img = st.sidebar.file_uploader("Upload image (photo of NFA)", 
                                     type=["png", "jpg", "jpeg", "bmp"])
    if img is not None:
        img_bytes = img.read()
        with st.spinner("Converting image to NFA JSON (Gemini)..."):
            try:
                nfa_data = image_to_nfa_json(img_bytes)
            except Exception as e:
                st.sidebar.error(f"Image import failed: {e}")

elif input_mode == "Camera":
    cam = st.sidebar.camera_input("Take a photo of the NFA")
    if cam is not None:
        img_bytes = cam.read()
        with st.spinner("Converting image to NFA JSON (Gemini)..."):
            try:
                nfa_data = image_to_nfa_json(img_bytes)
            except Exception as e:
                st.sidebar.error(f"Image import failed: {e}")
```

-----

## 3. 🔑 Security Best Practices

### ✅ Correct: Using `.streamlit\secrets.toml`
- API key stored in `.streamlit\secrets.toml`
- File is in `.gitignore` (never commit secrets!)
- Access via `st.secrets["GEMINI_API_KEY"]`
- Works both locally and on Streamlit Cloud deployment

### ❌ Wrong: Hardcoding API Key
```python
# NEVER DO THIS:
genai.configure(api_key="AIzaSyA34ZTNkNapUCa7APLCaFMVEDLOUiWU5LE")
```

### Deployment on Streamlit Cloud:
When deploying to Streamlit Cloud, you'll need to add secrets through their web interface:
1. Go to your app settings on Streamlit Cloud
2. Navigate to "Secrets" section
3. Add: `GEMINI_API_KEY = "your-key-here"`

-----

## 4. 📝 Project Structure

```
PROJECT/
├── .streamlit/
│   └── secrets.toml          # API keys (git-ignored)
├── .venv/                     # Virtual environment
├── tests/
│   └── test_nfa_to_dfa.py    # Unit tests
├── main.py                    # Streamlit UI entry point
├── nfa_to_dfa.py             # Core conversion algorithm (TO BE IMPLEMENTED)
├── gemini_importer.py        # Gemini vision API integration (TO BE IMPLEMENTED)
├── pyproject.toml            # Dependencies
├── README.md                 # Documentation
├── initial_plan.md           # This document
└── plan.md                   # Current plan status
```

-----

## 5. ✅ Verification of Initial Plan Correctness

### What's Correct in the Original Plan:
1. ✅ **Core Algorithm Design:** The NFA to DFA conversion using subset construction is the correct approach
2. ✅ **JSON Structure:** The proposed JSON format for NFA/DFA is appropriate and complete
3. ✅ **Modular Architecture:** Separating UI from core logic is excellent design
4. ✅ **Gemini Vision Concept:** Using AI vision to parse hand-drawn diagrams is innovative and viable
5. ✅ **Step-by-step Logging:** Showing conversion process helps users understand the algorithm

### What Needs Updates (Now Corrected):
1. ❌ **UI Framework:** Original said Tkinter → **Updated to Streamlit** ✅
2. ❌ **API Key Management:** Original showed hardcoding → **Updated to use st.secrets** ✅
3. ❌ **Model Name:** Original used deprecated `gemini-pro-vision` → **Updated to `gemini-1.5-flash`** ✅
4. ❌ **Image Handling:** Original used file paths → **Updated to byte streams for Streamlit** ✅
5. ❌ **File I/O Pattern:** Original used file dialogs → **Updated to Streamlit widgets** ✅

### Algorithm Correctness:
The subset construction algorithm approach is **theoretically sound**:
- Create DFA states as sets of NFA states ✅
- Start with the NFA's start state (as a set) ✅
- For each DFA state and input symbol, compute the union of all reachable NFA states ✅
- Mark DFA states as final if they contain any NFA final state ✅
- Continue until no new DFA states are discovered ✅

-----

## 6. 🎯 Implementation Checklist

### Core Components:
- [ ] **`nfa_to_dfa.py`** - Implement subset construction algorithm
  - [ ] Function signature: `convert_nfa_to_dfa(nfa_data: dict) -> tuple[dict, list[str]]`
  - [ ] Input validation
  - [ ] Subset construction with detailed logging
  - [ ] Handle edge cases (unreachable states, empty alphabet)

- [ ] **`gemini_importer.py`** - Implement image-to-JSON converter
  - [ ] Function signature: `image_to_nfa_json(img_bytes: bytes) -> dict`
  - [ ] Load API key from `st.secrets`
  - [ ] Configure Gemini model
  - [ ] Send prompt + image
  - [ ] Parse and validate JSON response

- [x] **`main.py`** - Streamlit UI (already implemented)
  - [x] Multiple input modes (paste, upload, image, camera)
  - [x] NFA preview
  - [x] Convert button
  - [x] Log display
  - [x] DFA output
  - [x] Download button

### Configuration:
- [x] **`.streamlit\secrets.toml`** - API key storage
- [x] **`pyproject.toml`** - Dependencies listed
- [ ] **`.gitignore`** - Ensure `.streamlit/secrets.toml` is ignored

### Testing:
- [ ] **Unit tests** for `convert_nfa_to_dfa()`
  - [ ] Simple 2-state NFA
  - [ ] NFA with multiple transitions on same symbol
  - [ ] NFA with unreachable states
  - [ ] Empty alphabet edge case
- [ ] **Integration tests** for `image_to_nfa_json()`
  - [ ] Mock Gemini API responses
  - [ ] Invalid JSON handling
  - [ ] Network error handling

### Documentation:
- [ ] Update `README.md` with:
  - [ ] Installation instructions
  - [ ] How to set up `.streamlit\secrets.toml`
  - [ ] Usage examples
  - [ ] Example NFA JSON files

-----

## 7. 🚀 Running the Application

### Local Development:
```bash
# Install dependencies
pip install -e .

# Create secrets file
# Add GEMINI_API_KEY to .streamlit\secrets.toml

# Run the app
streamlit run main.py
```

### Access:
- Opens automatically in browser at `http://localhost:8501`
- Mobile-friendly responsive design
- Can share via network with `--server.address 0.0.0.0`

-----

This modular design is perfect. Your main Streamlit app doesn't need to know *how* it got the NFA dictionary—only that it has it. This makes your "add-on" a clean, separate feature that doesn't complicate your core converter logic.
