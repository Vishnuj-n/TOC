# NFA → DFA Visualizer (Streamlit)

This small project converts NFAs (in JSON) to DFAs using subset construction and shows a step-by-step log.

Usage
1. Install dependencies (example):

```powershell
pip install -r requirements.txt
# or install directly
pip install streamlit pillow pytesseract google-generativeai pytest
```

2. Run the Streamlit app:

```powershell
streamlit run main.py
```

3. In the sidebar you can:
- Paste or upload NFA JSON
- Upload an image or take a photo (the image-to-JSON step needs Gemini configured or an OCR fallback)

Gemini integration
- The `gemini_importer.py` file contains a placeholder where you can wire the Gemini Vision API.
- Set `GEMINI_API_KEY` in your environment and follow the Google Generative AI docs for the correct SDK calls.

Tests

```powershell
pytest -q
```
