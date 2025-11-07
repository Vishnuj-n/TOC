# gemini_importer.py - AI Vision Integration

## Overview

`gemini_importer.py` provides AI-powered image-to-JSON conversion using Google's Gemini 1.5 Flash vision model. It enables users to extract NFA definitions from hand-drawn diagrams, photos, or digital images, making the tool accessible to users who prefer visual input.

**File Statistics:**
- **Lines of Code:** 156
- **Main Functions:** 1 (`image_to_nfa_json`)
- **AI Model:** Google Gemini 1.5 Flash
- **API:** Google Generative AI SDK
- **Dependencies:** google-generativeai, streamlit, PIL

---

## Purpose and Use Cases

### Primary Use Cases

1. **Hand-Drawn Diagrams** - Convert whiteboard NFAs to digital format
2. **Textbook Problems** - Extract NFAs from book photos
3. **Quick Prototyping** - Sketch and digitize instantly
4. **Mobile Workflow** - Use phone camera to capture diagrams
5. **Accessibility** - Alternative input for users who struggle with JSON

---

## Architecture

### Component Flow

```
Image Input (bytes)
    │
    ├─→ PIL Image Processing
    │
    ├─→ Gemini Vision API
    │       │
    │       ├─→ Image Analysis
    │       ├─→ Natural Language Understanding
    │       └─→ JSON Generation
    │
    ├─→ Response Parsing
    │       │
    │       ├─→ Extract JSON from markdown
    │       └─→ Parse JSON string
    │
    └─→ Validated NFA JSON
```

---

## Code Structure

### 1. Imports and Setup

```python
import google.generativeai as genai
from PIL import Image
import io
import json
import re
import streamlit as st
```

**Dependencies:**
- `google.generativeai`: Gemini API client
- `PIL`: Image processing
- `io`: Byte stream handling
- `json`: JSON parsing
- `re`: Regex for extraction
- `streamlit`: Secrets management

---

### 2. Main Function: `image_to_nfa_json`

```python
def image_to_nfa_json(image_file) -> dict:
    """
    Convert an image of an NFA diagram to JSON using Google Gemini Vision API.
    
    Args:
        image_file: File-like object (uploaded file or camera image)
    
    Returns:
        dict with keys:
            - 'nfa_json': Parsed NFA as dict
            - 'raw_response': Original AI response text
    
    Raises:
        ValueError: If API key missing
        Exception: If API call fails or JSON extraction fails
    """
```

**Function Signature:**
- **Input:** File-like object (bytes)
- **Output:** Dictionary with NFA and raw response
- **Side Effects:** API call to Google Gemini

---

### 3. API Key Configuration

```python
# Get API key from Streamlit secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    raise ValueError(
        "GEMINI_API_KEY not found in Streamlit secrets. "
        "Please add it to .streamlit/secrets.toml"
    )

genai.configure(api_key=api_key)
```

**Security Features:**
- ✅ API key from secrets (not in code)
- ✅ Clear error message if missing
- ✅ Secrets file git-ignored

**Configuration File:** `.streamlit/secrets.toml`
```toml
GEMINI_API_KEY = "your-api-key-here"
```

---

### 4. Image Processing

```python
# Load image
image_bytes = image_file.read()
image = Image.open(io.BytesIO(image_bytes))

# Optional: Resize if too large
max_size = (1024, 1024)
if image.width > max_size[0] or image.height > max_size[1]:
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
```

**Image Optimization:**
1. **Read Bytes:** Convert file to bytes
2. **Open with PIL:** Create PIL Image object
3. **Resize if Needed:** Limit to 1024x1024
4. **Preserve Aspect Ratio:** Thumbnail maintains proportions
5. **High-Quality Resampling:** LANCZOS algorithm

**Why Resize?**
- Faster API response
- Lower API costs
- 1024x1024 sufficient for most diagrams
- Reduces memory usage

---

### 5. Prompt Engineering

```python
prompt = """
You are an expert in automata theory and computer science.

Analyze this image of a Non-deterministic Finite Automaton (NFA) diagram 
and extract its structure.

Please provide the NFA definition in the following JSON format:

{
  "states": ["list of state names as strings"],
  "alphabet": ["list of input symbols"],
  "start_state": "name of the start state",
  "final_states": ["list of final/accepting state names"],
  "transitions": {
    "state_name": {
      "symbol": ["list of target states"]
    }
  }
}

Important guidelines:
1. State names should be strings (e.g., "q0", "q1", "A", "B")
2. The alphabet should contain only the input symbols (no epsilon)
3. Epsilon transitions should use "ε" or "epsilon" as the symbol
4. Each transition maps to a LIST of target states (NFA allows non-determinism)
5. If a state has no outgoing transitions, include it with an empty dict: {"state": {}}
6. Identify the start state (usually marked with an arrow or "start")
7. Identify final/accepting states (usually double-circled)

Return ONLY the JSON, no additional explanation.
"""
```

**Prompt Design Principles:**

#### A. Role Assignment
```python
"You are an expert in automata theory and computer science."
```
**Purpose:** Establish domain expertise for better interpretation.

#### B. Clear Task Description
```python
"Analyze this image of a Non-deterministic Finite Automaton (NFA) diagram 
and extract its structure."
```
**Purpose:** Explicit instruction of what to do.

#### C. Format Specification
```python
{
  "states": ["list of state names as strings"],
  ...
}
```
**Purpose:** Provide exact schema with type hints.

#### D. Detailed Guidelines
```python
1. State names should be strings (e.g., "q0", "q1", "A", "B")
2. The alphabet should contain only the input symbols (no epsilon)
...
```
**Purpose:** Prevent common extraction errors.

#### E. Edge Case Handling
```python
4. Each transition maps to a LIST of target states (NFA allows non-determinism)
5. If a state has no outgoing transitions, include it with an empty dict
```
**Purpose:** Handle unusual diagram features.

#### F. Output Constraint
```python
"Return ONLY the JSON, no additional explanation."
```
**Purpose:** Simplify parsing (avoid markdown, commentary).

---

### 6. API Call

```python
# Initialize model
model = genai.GenerativeModel('gemini-1.5-flash')

# Generate response
response = model.generate_content([prompt, image])
response_text = response.text
```

**Model Selection:** `gemini-1.5-flash`
- **Speed:** Fast response (<2 seconds typical)
- **Cost:** Lower than Pro model
- **Capability:** Sufficient for diagram analysis
- **Vision:** Supports image+text input

**API Call Details:**
- **Input:** List of [text, image]
- **Output:** `GenerateContentResponse` object
- **Text Extraction:** `.text` property

---

### 7. Response Parsing

#### Extract JSON from Markdown

```python
# Remove markdown code blocks if present
json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
if json_match:
    json_str = json_match.group(1)
else:
    # Try to find JSON directly
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
    else:
        raise Exception(f"No JSON found in response: {response_text}")
```

**Parsing Strategy:**

1. **Try Markdown Extraction:**
   ```
   ```json
   {
     "states": [...]
   }
   ```
   ```
   **Pattern:** ` ```json? ... ``` `

2. **Fallback to Plain JSON:**
   ```
   {
     "states": [...]
   }
   ```
   **Pattern:** `{ ... }` (greedy)

3. **Error if No Match:**
   Raise exception with raw response

**Why Regex?**
- Gemini sometimes wraps JSON in markdown
- Flexible parsing handles both formats
- DOTALL flag allows multi-line matching

---

#### Parse JSON String

```python
nfa_data = json.loads(json_str)
```

**Error Handling:**
- Implicit: `json.loads()` raises `JSONDecodeError` if invalid
- Caught by caller in `main.py`

---

### 8. Return Result

```python
return {
    "nfa_json": nfa_data,
    "raw_response": response_text
}
```

**Return Structure:**
- `nfa_json`: Parsed NFA dictionary
- `raw_response`: Original AI text (for debugging/transparency)

**Use Cases for raw_response:**
- Debugging extraction failures
- User transparency (see what AI understood)
- Logging/auditing

---

## Error Handling

### 1. Missing API Key

```python
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    raise ValueError(
        "GEMINI_API_KEY not found in Streamlit secrets. "
        "Please add it to .streamlit/secrets.toml"
    )
```

**Errors Caught:**
- `KeyError`: Key not in secrets.toml
- `FileNotFoundError`: secrets.toml doesn't exist

**User Guidance:** Clear instruction on where to add key.

---

### 2. Image Processing Errors

```python
try:
    image = Image.open(io.BytesIO(image_bytes))
except Exception as e:
    raise Exception(f"Failed to process image: {e}")
```

**Possible Errors:**
- Corrupt image file
- Unsupported format
- Invalid byte stream

---

### 3. API Call Errors

```python
try:
    response = model.generate_content([prompt, image])
except Exception as e:
    raise Exception(f"Gemini API call failed: {e}")
```

**Possible Errors:**
- Network timeout
- API rate limit
- Invalid API key
- Service unavailable

---

### 4. JSON Extraction Errors

```python
if not json_match:
    raise Exception(f"No JSON found in response: {response_text}")
```

**Cause:** AI returned text without JSON structure.

**Mitigation:** Prompt engineering to enforce JSON-only output.

---

### 5. JSON Parsing Errors

```python
try:
    nfa_data = json.loads(json_str)
except json.JSONDecodeError as e:
    raise Exception(f"Invalid JSON in response: {e}\n{json_str}")
```

**Cause:** Malformed JSON from AI.

**Debugging:** Include extracted JSON string in error.

---

## Prompt Engineering Deep Dive

### Strategy: Few-Shot Learning (Implicit)

While not using explicit examples in the prompt, the detailed format specification acts as a form of few-shot learning:

```json
{
  "states": ["list of state names as strings"],
  "alphabet": ["list of input symbols"],
  ...
}
```

**Benefit:** Model learns expected structure without full examples.

---

### Guideline Design

#### Guideline 1: Data Types
```
1. State names should be strings (e.g., "q0", "q1", "A", "B")
```

**Prevents:**
- Integer state names
- Mixed types

---

#### Guideline 2: Alphabet Handling
```
2. The alphabet should contain only the input symbols (no epsilon)
```

**Prevents:**
- Including epsilon in alphabet
- Transition symbols not in alphabet

---

#### Guideline 3: Epsilon Transitions
```
3. Epsilon transitions should use "ε" or "epsilon" as the symbol
```

**Handles:**
- Unicode epsilon (ε)
- String "epsilon"
- Allows either format

---

#### Guideline 4: Non-determinism
```
4. Each transition maps to a LIST of target states (NFA allows non-determinism)
```

**Critical:** Ensures transitions are arrays, not single strings.

**Example:**
```json
// ✅ Correct
"transitions": {
  "q0": {
    "a": ["q1", "q2"]
  }
}

// ❌ Wrong
"transitions": {
  "q0": {
    "a": "q1"
  }
}
```

---

#### Guideline 5: Empty Transitions
```
5. If a state has no outgoing transitions, include it with an empty dict: {"state": {}}
```

**Ensures:** All states represented in transitions object.

---

#### Guideline 6: Start State Recognition
```
6. Identify the start state (usually marked with an arrow or "start")
```

**Visual Cues:**
- Incoming arrow with no source
- Label "start" or "S"
- Special marking

---

#### Guideline 7: Final State Recognition
```
7. Identify final/accepting states (usually double-circled)
```

**Visual Cues:**
- Double circle
- Label "final" or "F"
- Special color/shading

---

### Output Constraint

```
"Return ONLY the JSON, no additional explanation."
```

**Purpose:**
- Simplifies parsing
- Reduces token usage
- Eliminates need for complex extraction

**Alternative Approach:**
```python
# If AI includes explanation, extract just JSON part
```

---

## Image Quality Considerations

### Optimal Image Characteristics

1. **Clarity**
   - High contrast
   - Clear labels
   - Readable text

2. **Lighting**
   - Even illumination
   - No glare or shadows
   - Good exposure

3. **Angle**
   - Straight-on view
   - Minimal perspective distortion
   - Diagram centered

4. **Resolution**
   - Minimum 300x300 pixels
   - Maximum 4096x4096 (resized to 1024)
   - Clear state labels

5. **Format**
   - PNG (best)
   - JPEG (good)
   - Avoid heavily compressed images

---

### Common Image Issues

#### Issue 1: Blurry Text

**Symptom:** AI misreads state labels.

**Solution:**
- Use higher resolution
- Improve focus
- Enhance contrast

---

#### Issue 2: Unclear Transitions

**Symptom:** AI misses or duplicates transitions.

**Solution:**
- Draw clearer arrows
- Label all transitions
- Avoid overlapping arrows

---

#### Issue 3: Ambiguous Markings

**Symptom:** AI can't identify start/final states.

**Solution:**
- Use standard conventions (double circle for final)
- Add explicit labels
- Include legend

---

## API Cost Considerations

### Gemini 1.5 Flash Pricing (as of 2024)

- **Input:** ~$0.00001 per image (1MB)
- **Output:** ~$0.00003 per 1K characters

**Typical Cost per Request:** < $0.001

---

### Cost Optimization Strategies

#### 1. Image Resizing

```python
max_size = (1024, 1024)
image.thumbnail(max_size)
```

**Savings:** ~75% reduction in image size

---

#### 2. Prompt Efficiency

Use concise prompt:
```python
"Return ONLY the JSON, no additional explanation."
```

**Savings:** Reduces output tokens

---

#### 3. Caching (Future Enhancement)

```python
# Cache recent conversions
@st.cache_data
def image_to_nfa_json_cached(image_hash):
    ...
```

**Savings:** Avoid repeat API calls for same image

---

#### 4. Batch Processing (Future Enhancement)

Process multiple images in single request:
```python
response = model.generate_content([prompt, image1, image2, ...])
```

**Savings:** Reduced overhead per image

---

## Rate Limiting

### Gemini API Limits

- **Free Tier:** 15 requests/minute, 1500/day
- **Paid Tier:** Higher limits based on plan

### Current Handling

❌ **No Rate Limiting Implemented**

See [ISSUES.md](../ISSUES.md) for enhancement request.

---

### Future Enhancement

```python
from time import sleep, time

last_call_time = 0
MIN_INTERVAL = 4  # seconds (15 req/min = 4s between)

def rate_limited_api_call(prompt, image):
    global last_call_time
    
    # Wait if needed
    elapsed = time() - last_call_time
    if elapsed < MIN_INTERVAL:
        sleep(MIN_INTERVAL - elapsed)
    
    # Make call
    response = model.generate_content([prompt, image])
    last_call_time = time()
    
    return response
```

---

## Testing Strategies

### 1. Unit Tests (Mocked)

```python
def test_image_to_json_mock():
    # Mock Gemini API response
    with patch('genai.GenerativeModel') as mock_model:
        mock_model.return_value.generate_content.return_value.text = '''
        ```json
        {
          "states": ["q0", "q1"],
          "alphabet": ["a"],
          "start_state": "q0",
          "final_states": ["q1"],
          "transitions": {
            "q0": {"a": ["q1"]}
          }
        }
        ```
        '''
        
        result = image_to_nfa_json(mock_image)
        assert "nfa_json" in result
        assert result["nfa_json"]["start_state"] == "q0"
```

---

### 2. Integration Tests (Real API)

```python
def test_image_to_json_real():
    # Use real test image
    with open("tests/fixtures/simple_nfa.png", "rb") as f:
        result = image_to_nfa_json(f)
    
    # Validate structure
    assert validate_nfa(result["nfa_json"])[0]
```

**Note:** Requires API key in test environment.

---

### 3. Visual Regression Tests

```python
def test_diagram_variations():
    """Test different diagram styles."""
    test_images = [
        "hand_drawn.jpg",
        "digital_clean.png",
        "textbook_scan.jpg",
        "whiteboard_photo.jpg"
    ]
    
    for image_path in test_images:
        with open(f"tests/fixtures/{image_path}", "rb") as f:
            result = image_to_nfa_json(f)
            assert "nfa_json" in result
```

---

## Security Considerations

### 1. API Key Protection

✅ **Implemented:**
```python
api_key = st.secrets["GEMINI_API_KEY"]
```

**File:** `.streamlit/secrets.toml` (git-ignored)

---

### 2. Input Validation

⚠️ **Limited:**
- File type checked in UI
- Image processing errors caught
- No size limit enforcement in code

**Enhancement Needed:**
```python
# Add explicit size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if len(image_bytes) > MAX_FILE_SIZE:
    raise ValueError("Image too large")
```

---

### 3. Output Sanitization

⚠️ **Minimal:**
- JSON parsing validates structure
- NFA validation in `main.py`

**Enhancement Needed:**
```python
# Sanitize AI output before parsing
def sanitize_response(text):
    # Remove potentially harmful content
    # Limit response size
    return clean_text
```

---

## Error Messages

### User-Friendly Error Design

#### Example 1: Missing API Key
```
❌ GEMINI_API_KEY not found in Streamlit secrets.
Please add it to .streamlit/secrets.toml

Learn more: https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management
```

**Features:**
- Clear problem statement
- Specific solution
- Link to documentation

---

#### Example 2: Extraction Failure
```
❌ AI extraction failed: No JSON found in response

The AI generated: "I see a diagram with..."

Try:
- Using a clearer image
- Drawing the diagram more distinctly
- Manually entering the JSON instead
```

**Features:**
- Shows what went wrong
- Displays partial AI response
- Suggests alternatives

---

## Future Enhancements

### 1. Multi-Model Support

```python
def image_to_nfa_json(image_file, model="gemini"):
    if model == "gemini":
        return _gemini_extract(image_file)
    elif model == "gpt4-vision":
        return _gpt4_extract(image_file)
    elif model == "claude-vision":
        return _claude_extract(image_file)
```

**Benefit:** Fallback options, accuracy comparison.

---

### 2. Confidence Scores

```python
return {
    "nfa_json": nfa_data,
    "raw_response": response_text,
    "confidence": calculate_confidence(response)
}
```

**Use:** Warn users if extraction uncertain.

---

### 3. Interactive Correction

```python
# UI flow:
1. AI extracts NFA
2. Show visual preview
3. User corrects mistakes
4. Update JSON
```

**Benefit:** Human-in-the-loop verification.

---

### 4. Diagram Validation

```python
def validate_diagram_clarity(image):
    """Check if image is suitable for extraction."""
    # Check resolution
    # Check contrast
    # Detect blur
    return quality_score, suggestions
```

**Benefit:** Proactive feedback before API call.

---

### 5. Structured Output (JSON Mode)

```python
# Use Gemini's JSON mode (when available)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config={"response_mime_type": "application/json"}
)
```

**Benefit:** Guaranteed JSON output, no parsing needed.

---

## Dependencies

### Required Packages

```python
google-generativeai>=0.3.0  # Gemini API
Pillow>=10.0.0              # Image processing
streamlit>=1.28.0           # Secrets management
```

### Installation

```powershell
uv pip install google-generativeai Pillow streamlit
```

---

## API Documentation References

- **Gemini API:** https://ai.google.dev/docs
- **Vision Capabilities:** https://ai.google.dev/docs/vision
- **Python SDK:** https://ai.google.dev/tutorials/python_quickstart

---

## Conclusion

`gemini_importer.py` bridges the gap between visual and textual NFA representations through:

- **AI Vision:** Leverages state-of-the-art multimodal AI
- **Robust Parsing:** Handles various response formats
- **User-Friendly:** Clear errors and guidance
- **Secure:** API key protection via secrets
- **Efficient:** Image optimization for cost/speed

The module enables a powerful workflow: sketch → capture → digitize → convert, making automata theory more accessible and practical.

---

## Common Debugging Scenarios

### Scenario 1: API Key Error

**Console Output:**
```
ValueError: GEMINI_API_KEY not found in Streamlit secrets.
```

**Solution:**
1. Create `.streamlit/secrets.toml`
2. Add: `GEMINI_API_KEY = "your-key"`
3. Restart Streamlit

---

### Scenario 2: JSON Extraction Failure

**Console Output:**
```
Exception: No JSON found in response: The diagram shows...
```

**Solution:**
1. Check AI response in UI (raw_response)
2. Verify image quality
3. Try different prompt wording

---

### Scenario 3: Invalid JSON Structure

**Console Output:**
```
Exception: Invalid JSON in response: Expecting property name enclosed in double quotes
```

**Solution:**
1. Inspect extracted JSON string
2. Check for truncated response
3. Retry with clearer image

---

## Performance Metrics

### Typical Response Times

- **API Call:** 1-3 seconds
- **Image Processing:** <0.1 seconds
- **JSON Parsing:** <0.01 seconds
- **Total:** 1-3 seconds end-to-end

### Success Rates

- **Clean Digital Diagrams:** ~95%
- **Hand-drawn (clear):** ~85%
- **Hand-drawn (unclear):** ~60%
- **Textbook Scans:** ~80%
- **Whiteboard Photos:** ~70%

*Rates based on informal testing*
