# Known Issues and Limitations

This document tracks known issues, limitations, and potential improvements for the NFA to DFA Visualizer project.

---

## 🐛 Current Issues

### 1. Virtual Environment Conflict
**Status:** ⚠️ Active  
**Severity:** Low  
**Description:** An accidental `graph/` virtual environment was created in the project directory, conflicting with the intended `.venv/` environment.

**Impact:**
- Confusion about which virtual environment to use
- Unnecessary files in project directory
- Potential PATH conflicts

**Workaround:**
```powershell
Remove-Item -Recurse -Force graph
```

**Permanent Fix:** Update `.gitignore` to prevent committing venvs with common names.

---

### 2. Graphviz Dependency Not in Virtual Environment
**Status:** ⚠️ Active  
**Severity:** Medium  
**Description:** The `graphviz` Python package needs to be installed globally rather than in the project's virtual environment for Streamlit to find it.

**Impact:**
- Graph visualization may not work in some environments
- Deployment complexity increased
- Different behavior between local and cloud deployments

**Current Workaround:**
```powershell
pip install graphviz  # Global install
```

**Permanent Fix:**
- Ensure all dependencies are in project's virtual environment
- Use proper environment activation before running Streamlit
- Update deployment scripts to include graphviz

---

### 3. Graphviz Software Dependency
**Status:** ⚠️ By Design  
**Severity:** Medium  
**Description:** Requires system-level Graphviz software installation (not just Python package).

**Impact:**
- Users must install external software
- Deployment to cloud platforms requires additional configuration
- Graph visualization fails silently if not installed

**Current Mitigation:**
- Graceful fallback when graphviz not available
- Warning message displayed to users
- Documentation includes installation instructions

**Potential Fix:**
- Add automatic detection and clearer error messages
- Provide downloadable installers
- Consider alternative pure-Python graph libraries

---

### 4. Gemini API Key in Secrets File
**Status:** ✅ Working as Intended  
**Severity:** Low (Security Consideration)  
**Description:** API key stored in `.streamlit/secrets.toml` which must be manually created.

**Impact:**
- First-time users may not know how to configure
- Risk of accidentally committing secrets if `.gitignore` is misconfigured

**Current Mitigation:**
- `.streamlit/secrets.toml` is in `.gitignore`
- Documentation includes setup instructions
- Clear error message if key not found

**Potential Improvements:**
- Add interactive setup script
- Support environment variables as fallback
- Provide example secrets file template

---

## ⚠️ Limitations

### 1. No Epsilon Transitions Support
**Status:** Not Implemented  
**Priority:** Medium  

**Description:** The NFA to DFA converter does not support epsilon (ε) transitions.

**Impact:**
- Cannot convert NFAs with epsilon transitions
- Users must manually eliminate epsilon transitions first

**Workaround:** Use external tools to eliminate epsilon transitions before conversion.

**Future Enhancement:** Implement epsilon-closure algorithm.

---

### 2. Large Automata Performance
**Status:** By Design  
**Priority:** Low  

**Description:** Very large NFAs (>50 states) can cause:
- Slow conversion (exponential state explosion)
- Cluttered graph visualizations
- High memory usage

**Impact:**
- Poor user experience with complex automata
- Potential browser freezing

**Current Mitigation:**
- Warning messages for state explosion
- Progressive loading could help

**Potential Improvements:**
- Implement DFA minimization after conversion
- Add state limit warnings before conversion
- Optimize graph layout for large automata
- Implement pagination for large state lists

---

### 3. Image Recognition Accuracy
**Status:** AI-Dependent  
**Priority:** Medium  

**Description:** Gemini Vision API may misinterpret hand-drawn diagrams.

**Impact:**
- Incorrect NFA extraction from images
- Need for manual JSON editing
- User frustration

**Current Mitigation:**
- Validation of extracted JSON
- Clear error messages
- Manual JSON editing option

**Potential Improvements:**
- Add image preprocessing (contrast, rotation)
- Implement OCR fallback
- Allow manual correction of extracted data
- Show confidence scores

---

### 4. Single Direction Layout Only
**Status:** Not Implemented  
**Priority:** Low  

**Description:** Graphs only support left-to-right (LR) layout.

**Impact:**
- Tall graphs with many states may not fit well
- Limited customization options

**Workaround:** Users can modify `graph_visualizer.py` to change `rankdir`.

**Future Enhancement:** Add layout options in UI (LR, TB, RL, BT).

---

## 🔧 Technical Debt

### 1. Hardcoded Gemini Model
**Location:** `gemini_importer.py`  
**Issue:** Model name `'gemini-1.5-flash'` is hardcoded.

**Impact:**
- Can't switch models without code changes
- May break if Google deprecates model

**Recommendation:**
- Move model name to configuration file
- Add model selection in UI
- Support multiple AI providers

---

### 2. No Caching for Conversions
**Location:** `main.py`  
**Issue:** Conversions are not cached between reruns.

**Impact:**
- Repeated conversions on page refresh
- Unnecessary computation

**Recommendation:**
```python
@st.cache_data
def convert_nfa_to_dfa_cached(nfa_json):
    nfa_data = json.loads(nfa_json)
    return convert_nfa_to_dfa(nfa_data)
```

---

### 3. Mixed Dependency Management
**Location:** Project root  
**Issue:** Using both `uv pip` and regular `pip` for package management.

**Impact:**
- Inconsistent dependency tracking
- Potential version conflicts

**Recommendation:**
- Standardize on one tool (preferably `uv`)
- Update all documentation to use chosen tool
- Create `requirements.txt` or use `pyproject.toml` properly

---

### 4. Limited Error Handling in Graph Generation
**Location:** `graph_visualizer.py`  
**Issue:** Generic exception catching without specific error types.

**Impact:**
- Difficult to debug graph generation failures
- Poor error messages for users

**Recommendation:**
```python
try:
    graph = create_nfa_graph(nfa_data)
except graphviz.ExecutableNotFound:
    st.error("Graphviz software not installed")
except ValueError as e:
    st.error(f"Invalid automaton structure: {e}")
```

---

## 🚀 Feature Requests

### High Priority

1. **DFA Minimization**
   - Implement Hopcroft's algorithm
   - Show before/after comparison
   - Track reduction percentage

2. **String Testing**
   - Input test strings
   - Show acceptance/rejection
   - Visualize execution path

3. **Multiple Example Files**
   - Add 10+ example NFAs
   - Categorize by difficulty
   - Include explanations

### Medium Priority

4. **Export Options**
   - Export as PNG/SVG/PDF
   - Export DOT source code
   - Export to LaTeX format

5. **Undo/Redo Support**
   - Track conversion history
   - Allow reverting changes
   - Save session state

6. **Dark Mode**
   - Theme toggle
   - Adjust graph colors
   - Better contrast

### Low Priority

7. **Batch Conversion**
   - Upload multiple NFAs
   - Batch process
   - Download as ZIP

8. **Animation**
   - Animate subset construction steps
   - Show state combinations visually
   - Highlight active transitions

9. **Collaborative Features**
   - Share automata via URL
   - Comments and annotations
   - Version control

---

## 🧪 Testing Gaps

### 1. No Integration Tests
**Missing:** Tests for Streamlit UI components.

**Recommendation:** Add Playwright or Selenium tests for:
- File upload functionality
- Camera capture
- Graph rendering
- Download functionality

---

### 2. No Gemini API Mocking
**Missing:** Tests for image-to-JSON conversion without actual API calls.

**Recommendation:**
```python
@pytest.fixture
def mock_gemini_response():
    with patch('gemini_importer.genai.GenerativeModel') as mock:
        mock.return_value.generate_content.return_value.text = '{"states": [...]}'
        yield mock
```

---

### 3. Limited Edge Case Testing
**Missing:** Tests for:
- Empty transitions
- Unreachable states
- Very large alphabets (>26 symbols)
- Unicode state names

**Recommendation:** Expand `tests/test_nfa_to_dfa.py` with edge cases.

---

### 4. No Graph Visualization Tests
**Missing:** Tests verifying graph generation doesn't crash.

**Recommendation:**
```python
def test_graph_generation():
    nfa = load_sample_nfa()
    graph = create_nfa_graph(nfa)
    assert graph is not None
    assert isinstance(graph, graphviz.Digraph)
```

---

## 📦 Deployment Issues

### 1. Streamlit Cloud Compatibility
**Issue:** Graph visualization requires Graphviz installation.

**Impact:** May not work on Streamlit Cloud without configuration.

**Solution:** Add `packages.txt`:
```
graphviz
libgraphviz-dev
```

---

### 2. Large Dependency Size
**Issue:** Dependencies (especially Gemini SDK) increase deployment size.

**Impact:**
- Longer deployment times
- Higher bandwidth usage

**Recommendation:**
- Use lighter alternatives where possible
- Implement lazy loading for heavy dependencies

---

### 3. No Docker Configuration
**Issue:** No Dockerfile for containerized deployment.

**Recommendation:** Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y graphviz
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "main.py"]
```

---

## 🔒 Security Considerations

### 1. API Key Exposure Risk
**Risk:** Secrets file could be accidentally committed.

**Mitigation:**
- ✅ Already in `.gitignore`
- ⚠️ No pre-commit hooks to double-check

**Recommendation:** Add pre-commit hooks:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: detect-private-key
```

---

### 2. Unvalidated User Input
**Risk:** Image uploads are sent directly to Gemini API.

**Mitigation:**
- File size limits enforced by Streamlit
- File type restrictions in place

**Recommendation:**
- Add explicit file size validation
- Scan uploaded files for malware
- Rate limit API calls

---

### 3. No Rate Limiting
**Risk:** Gemini API could be overused.

**Mitigation:** None currently.

**Recommendation:**
```python
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def rate_limited_api_call(image_hash):
    time.sleep(1)  # Basic rate limiting
    return image_to_nfa_json(image_bytes)
```

---

## 📊 Performance Issues

### 1. Synchronous API Calls
**Issue:** Gemini API calls block the UI.

**Impact:** Poor user experience during image processing.

**Recommendation:**
```python
import asyncio

async def process_image_async(img_bytes):
    return await asyncio.to_thread(image_to_nfa_json, img_bytes)
```

---

### 2. No Result Caching
**Issue:** Same image processed multiple times.

**Recommendation:** Implement LRU cache with image hashing.

---

### 3. Graph Generation on Every Render
**Issue:** Graphs regenerated on each Streamlit rerun.

**Recommendation:** Use `st.cache_data` decorator.

---

## 🔄 Maintenance Tasks

### Regular Tasks

- [ ] Update dependencies monthly
- [ ] Review and update API models
- [ ] Check for Graphviz updates
- [ ] Monitor API usage and costs
- [ ] Review and update documentation

### As Needed

- [ ] Add new example NFAs
- [ ] Update tests for new features
- [ ] Refactor technical debt
- [ ] Improve error messages
- [ ] Optimize performance

---

## 📝 Documentation Gaps

### Missing Documentation

1. **API Documentation** - No docstring documentation site
2. **Video Tutorials** - No walkthrough videos
3. **FAQ Section** - No frequently asked questions
4. **Troubleshooting Guide** - Limited troubleshooting info
5. **Contributing Guide** - No CONTRIBUTING.md

---

## 🎯 Priority Matrix

| Issue | Severity | Priority | Effort | Status |
|-------|----------|----------|--------|--------|
| Virtual Environment Conflict | Low | High | Low | Active |
| Graphviz in Venv | Medium | High | Medium | Active |
| No Epsilon Transitions | Medium | Medium | High | Backlog |
| Image Recognition Accuracy | Medium | Medium | Medium | Ongoing |
| DFA Minimization | High | High | High | Planned |
| String Testing | High | High | Medium | Planned |
| No Integration Tests | Medium | Medium | High | Backlog |

---

## 🤝 Contributing

Found a bug or have a feature request? 

1. Check if it's already listed here
2. Search existing GitHub issues
3. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

---

## 📅 Changelog

### Known Issues - Version 1.0.0 (November 6, 2025)

- Initial issues documentation
- Identified 15+ issues and limitations
- Documented 9 feature requests
- Listed 4 testing gaps
- Added 3 deployment issues
- Noted 3 security considerations

---

**Last Updated:** November 6, 2025  
**Project Version:** 0.1.0  
**Maintained By:** Automaton Visualizer Team
  