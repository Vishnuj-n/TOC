# Claude Development Rules & Guidelines

## Project: NFA to DFA Automaton Visualizer

This document outlines the development rules, conventions, and guidelines for this project.

---

## 🔧 Package Management

### Use `uv` Instead of `pip`

**✅ Always use:**
```bash
uv pip install <package>
uv pip install -e .
uv pip list
uv pip freeze
```

**❌ Never use:**
```bash
pip install <package>
pip install -e .
```

### Why `uv`?
- **Faster:** 10-100x faster than pip
- **Better dependency resolution:** More reliable conflict detection
- **Modern:** Built with Rust, designed for speed
- **Compatible:** Drop-in replacement for pip

---

## 📁 Project Structure

```
TOC/
├── .streamlit/
│   └── secrets.toml          # API keys (NEVER commit)
├── .venv/                     # Virtual environment
├── tests/
│   ├── __init__.py
│   ├── test_nfa_to_dfa.py    # Core algorithm tests
│   └── fixtures/
│       └── sample_nfa.json   # Test data
├── main.py                    # Streamlit UI entry point
├── nfa_to_dfa.py             # Core conversion algorithm
├── gemini_importer.py        # Gemini Vision API integration
├── pyproject.toml            # Project metadata & dependencies
├── README.md                 # User documentation
├── claude.md                 # This file - development rules
├── initial_plan.md           # Original plan (archived)
├── initial_plan_updated.md   # Updated plan with Streamlit
└── PLAN_ANALYSIS.md          # Plan verification report
```

---

## 🎯 Core Principles

### 1. Separation of Concerns
- **`main.py`**: UI only, no business logic
- **`nfa_to_dfa.py`**: Pure algorithm, no UI dependencies
- **`gemini_importer.py`**: External API integration, isolated

### 2. Type Hints
Always use type hints for function signatures:
```python
def convert_nfa_to_dfa(nfa_data: dict) -> tuple[dict, list[str]]:
    ...
```

### 3. Error Handling
- Use try-except blocks for external operations (API calls, file I/O)
- Provide meaningful error messages to users
- Log errors for debugging

### 4. Security
- **NEVER** hardcode API keys
- Always use `st.secrets["KEY_NAME"]`
- Keep `.streamlit/secrets.toml` in `.gitignore`

---

## 🔐 API Key Management

### Accessing Secrets
```python
import streamlit as st

# ✅ Correct
api_key = st.secrets["GEMINI_API_KEY"]

# ❌ Wrong
api_key = "AIzaSyA..."
```

### Secrets File Location
```
.streamlit/secrets.toml
```

### Secrets File Format
```toml
GEMINI_API_KEY = "your-api-key-here"
```

---

## 🧪 Testing Standards

### Test File Naming
- Test files: `test_*.py`
- Test functions: `test_*`

### Running Tests
```bash
# Run all tests
uv pip install pytest
pytest

# Run specific test file
pytest tests/test_nfa_to_dfa.py

# Run with coverage
pytest --cov=. tests/
```

### Test Structure
```python
def test_simple_nfa_conversion():
    """Test basic NFA to DFA conversion."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a", "b"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {"a": ["q0", "q1"]},
            "q1": {"b": ["q1"]}
        }
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    assert dfa is not None
    assert len(logs) > 0
    assert "states" in dfa
```

---

## 📝 Code Style

### Docstrings
Use Google-style docstrings:
```python
def function_name(param1: str, param2: int) -> dict:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input is provided
    """
```

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

```python
import json
import io
from typing import Optional

import streamlit as st
from PIL import Image

from nfa_to_dfa import convert_nfa_to_dfa
```

### Line Length
- Max 100 characters (soft limit)
- Break long lines logically

---

## 🚀 Running the Application

### Development
```bash
# Activate virtual environment (PowerShell)
.venv\Scripts\Activate.ps1

# Run Streamlit app
streamlit run main.py
```

### Installation
```bash
# Install in development mode
uv pip install -e .
```

---

## 🐛 Debugging

### Streamlit Debug Mode
```bash
streamlit run main.py --logger.level=debug
```

### Print Debugging
```python
import streamlit as st

# Use st.write for debugging in Streamlit
st.write("Debug:", variable)

# Use st.json for structured data
st.json(data_dict)
```

---

## 📊 Git Workflow

### What to Commit
- ✅ Source code (`.py` files)
- ✅ Tests
- ✅ Documentation (`.md` files)
- ✅ `pyproject.toml`
- ✅ `.gitignore`

### What NOT to Commit
- ❌ `.streamlit/secrets.toml`
- ❌ `.venv/`
- ❌ `__pycache__/`
- ❌ `*.pyc`
- ❌ `.pytest_cache/`

### .gitignore Template
```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
*.log
.DS_Store
```

---

## 🔄 Development Workflow

### 1. Feature Development
1. Implement function with type hints
2. Write docstring
3. Write unit tests
4. Test manually in Streamlit UI
5. Commit changes

### 2. Testing Cycle
1. Write test first (TDD approach)
2. Implement feature
3. Run tests: `pytest`
4. Fix failures
5. Refactor if needed

### 3. API Integration
1. Test with mock data first
2. Implement real API call
3. Add error handling
4. Test with various inputs
5. Add rate limiting if needed

---

## 🎨 Streamlit Best Practices

### State Management
```python
# Initialize session state
if 'nfa_data' not in st.session_state:
    st.session_state.nfa_data = None
```

### Caching
```python
@st.cache_data
def load_expensive_data():
    return compute_something()
```

### Layout
```python
# Use columns for side-by-side content
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")
```

---

## 📦 Dependencies

### Core Dependencies
- `streamlit`: Web UI framework
- `pillow`: Image processing
- `google-generativeai`: Gemini API
- `pytest`: Testing framework

### Installation
```bash
uv pip install streamlit pillow google-generativeai pytest
```

Or:
```bash
uv pip install -e .
```

---

## 🔍 Code Review Checklist

Before committing:
- [ ] Type hints on all functions
- [ ] Docstrings for public functions
- [ ] No hardcoded API keys
- [ ] Error handling for external calls
- [ ] Tests written and passing
- [ ] No debug print statements
- [ ] Imports organized correctly
- [ ] No unused imports
- [ ] `.streamlit/secrets.toml` not committed

---

## 📚 Resources

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [Gemini API Docs](https://ai.google.dev/docs)
- [uv Documentation](https://github.com/astral-sh/uv)

### Theory
- Subset Construction Algorithm
- NFA vs DFA Theory
- Automata Theory Basics

---

## 🎯 Project Goals

### MVP (Minimum Viable Product)
- [x] Streamlit UI with multiple input modes
- [ ] Core NFA to DFA conversion algorithm
- [ ] Gemini Vision API integration
- [ ] Download DFA functionality
- [ ] Basic error handling

### Future Enhancements
- [ ] Epsilon transitions support
- [ ] DFA minimization
- [ ] Visual graph rendering
- [ ] String acceptance testing
- [ ] State diagram export (SVG/PNG)
- [ ] Multiple example NFAs

---

## 🚨 Common Pitfalls to Avoid

### 1. Don't Mix UI and Logic
```python
# ❌ Bad
def convert_nfa(nfa):
    st.write("Converting...")  # UI code in logic!
    return dfa

# ✅ Good
def convert_nfa(nfa):
    return dfa  # Pure function
```

### 2. Don't Forget Error Cases
```python
# ❌ Bad
def process_image(img_bytes):
    return image_to_nfa_json(img_bytes)

# ✅ Good
def process_image(img_bytes):
    try:
        return image_to_nfa_json(img_bytes)
    except Exception as e:
        st.error(f"Failed to process image: {e}")
        return None
```

### 3. Don't Hardcode Paths
```python
# ❌ Bad
with open("C:/Users/me/file.json") as f:

# ✅ Good
from pathlib import Path
project_root = Path(__file__).parent
with open(project_root / "data" / "file.json") as f:
```

---

**Last Updated:** November 6, 2025  
**Project Version:** 0.1.0  
**Python Version:** >=3.11
