"""Gemini Vision API integration for converting NFA diagrams to JSON.

This module uses Google's Gemini Vision API to parse hand-drawn or photographed
NFA diagrams and convert them to the JSON format expected by the converter.
"""

import json
import io
from typing import Dict

import streamlit as st
import google.generativeai as genai
from PIL import Image


# Prompt template for Gemini API
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
- State names should be simple strings like "q0", "q1", "q2", etc.
- The start state is usually indicated by an arrow coming from nowhere
- Final/accepting states are usually indicated by double circles
- Each transition maps: source_state -> input_symbol -> list of destination states
- If a state has no transitions on a symbol, omit that symbol from its dictionary
- Be precise with the diagram's arrows and labels
- If an arrow has multiple labels (e.g., "a,b"), create separate transitions for each symbol
- Self-loops (state to itself) should be included in transitions
- Extract ALL visible transitions from the diagram
"""


def image_to_nfa_json(img_bytes: bytes) -> Dict:
    """Convert an image of an NFA diagram to JSON using Gemini Vision API.
    
    This function takes an image (as bytes) of a hand-drawn or computer-generated
    NFA diagram and uses Google's Gemini Vision API to extract the automaton
    structure and convert it to the expected JSON format.
    
    Args:
        img_bytes: Image data as bytes (from Streamlit file_uploader or camera_input)
    
    Returns:
        Dictionary containing NFA specification with keys:
            - states: list[str]
            - alphabet: list[str]
            - start_state: str
            - final_states: list[str]
            - transitions: dict[str, dict[str, list[str]]]
    
    Raises:
        ValueError: If API key is not configured
        RuntimeError: If API call fails
        json.JSONDecodeError: If response is not valid JSON
    
    Example:
        >>> with open("nfa_diagram.png", "rb") as f:
        ...     img_bytes = f.read()
        >>> nfa_data = image_to_nfa_json(img_bytes)
        >>> print(nfa_data["states"])
        ['q0', 'q1', 'q2']
    """
    # Load API key from Streamlit secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError) as e:
        raise ValueError(
            "GEMINI_API_KEY not found in Streamlit secrets. "
            "Please add it to .streamlit/secrets.toml"
        ) from e
    
    # Configure Gemini API
    genai.configure(api_key=api_key)
    
    try:
        # Load image from bytes
        img = Image.open(io.BytesIO(img_bytes))
        
        # Use Gemini 1.5 Flash model (faster and cost-effective)
        # Alternative: 'gemini-1.5-pro' for potentially better accuracy
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Send both the prompt and the image
        response = model.generate_content([JSON_GENERATION_PROMPT, img])
        
        # Extract text from response
        response_text = response.text.strip()
        
        # Clean up the response to get raw JSON
        # Sometimes the model adds ```json ... ```, so we strip it
        json_text = response_text
        
        # Remove markdown code blocks if present
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()
        
        # Parse the JSON string into a Python dict
        nfa_data = json.loads(json_text)
        
        # Validate that we got the expected structure
        required_keys = ["states", "alphabet", "start_state", "final_states", "transitions"]
        missing_keys = [key for key in required_keys if key not in nfa_data]
        
        if missing_keys:
            raise ValueError(f"Gemini response missing required keys: {missing_keys}")
        
        return nfa_data
        
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Failed to parse Gemini response as JSON. Response was: {response_text[:200]}...",
            e.doc,
            e.pos
        ) from e
    
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}") from e


def image_to_nfa_json_with_retry(img_bytes: bytes, max_retries: int = 2) -> Dict:
    """Convert image to NFA JSON with retry logic.
    
    Sometimes the Gemini API may return malformed JSON or miss some details.
    This function retries the conversion up to max_retries times.
    
    Args:
        img_bytes: Image data as bytes
        max_retries: Maximum number of retry attempts
    
    Returns:
        Dictionary containing NFA specification
    
    Raises:
        RuntimeError: If all retry attempts fail
    """
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return image_to_nfa_json(img_bytes)
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                continue
    
    raise RuntimeError(f"Failed after {max_retries + 1} attempts. Last error: {last_error}")


def test_gemini_connection() -> bool:
    """Test if Gemini API is properly configured and accessible.
    
    Returns:
        True if connection is successful, False otherwise
    """
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Try to list available models as a connectivity test
        models = genai.list_models()
        return True
    except Exception:
        return False
