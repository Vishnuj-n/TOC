# 🚀 Quick Start Guide - NFA to DFA Visualizer v3.0

## Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Install Graphviz for Visualization
Download from: https://graphviz.org/download/

### 3. Run the Application
```bash
streamlit run main.py
```

### 4. Open Browser
Navigate to: http://localhost:8501

## 📝 Quick Tutorial

### Method 1: Manual Builder (Recommended for Learning)

1. Click **"📝 Start Manual Builder"** on the home page
2. Enter states: `q0, q1, q2`
3. Enter alphabet: `a, b`
4. Select start state: `q0`
5. Select final states: `q2`
6. Define transitions:
   - From q0 on 'a': `q0, q1` (non-deterministic!)
   - From q0 on 'b': `q0`
   - From q1 on 'b': `q2`
   - From q2 on 'a': `q2`
   - From q2 on 'b': `q2`
7. Click **"✅ Build NFA"**
8. Click **"🔄 Convert to DFA →"**
9. View the conversion results!

### Method 2: Import Example (Fastest)

1. Click **"📤 Import JSON"** on the home page
2. Go to the **"📚 Load Example"** tab
3. Select **"Simple NFA (a*b+)"**
4. Click **"📥 Load Example"**
5. Click **"🔄 Convert to DFA →"**
6. Done!

### Method 3: Paste JSON

1. Click **"📤 Import JSON"**
2. Go to **"📋 Paste JSON"** tab
3. Paste this example:
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": {
    "q0": {"a": ["q1"], "b": ["q0"]},
    "q1": {"a": ["q1"], "b": ["q1"]}
  }
}
```
4. Click **"💾 Save NFA"**
5. Click **"🔄 Convert to DFA →"**

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/test_app.py -v

# Expected output: 21 passed
```

## 📖 Learning Resources

- Visit **"ℹ️ About & Help"** page for:
  - Detailed documentation
  - More examples
  - FAQ
  - Technical details

## 🎯 Tips

- Start with the **Manual Builder** to understand NFA structure
- Use **Import JSON** for complex NFAs
- Check the **Algorithm Trace** in conversion results
- Download your DFA as JSON for later use
- Use the sidebar to track loaded NFAs

## ⚡ Common Issues

**Graph not showing?**
- Install Graphviz from https://graphviz.org/download/
- Add to system PATH
- Restart the Streamlit app

**Invalid NFA error?**
- Check that all states are defined
- Ensure transitions use arrays: `["q1"]` not `"q1"`
- Verify start_state is in states list

## 🎉 You're Ready!

Enjoy exploring NFA to DFA conversion!
