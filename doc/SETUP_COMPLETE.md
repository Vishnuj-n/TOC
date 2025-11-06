# Quick Setup Guide - Graph Visualization

## ✅ Status: WORKING

Both components of graph visualization are now properly installed:

1. ✅ **Graphviz Software** (dot command) - Installed globally
2. ✅ **Python graphviz Package** - Installed in Python environment

---

## Verification

### 1. Graphviz Software (Installed ✅)
```powershell
PS C:\Users\vishn> dot -V
dot - graphviz version 14.0.2 (20251019.1705)
```

### 2. Python Package (Installed ✅)
```powershell
PS C:\Users\vishn\PROJECT\TOC> pip install graphviz
Successfully installed graphviz-0.21
```

---

## Application Status

**Streamlit App Running:** http://localhost:8501

### Features Now Available:

✅ **NFA Graph Visualization**
- View your input NFA as a state diagram
- States shown as circles (double circles for final states)
- Transitions labeled with input symbols
- Start state indicated with arrow

✅ **DFA Graph Visualization**
- View the converted DFA as a state diagram
- See deterministic transitions clearly
- Compare complexity with NFA

✅ **Side-by-Side Comparison**
- NFA and DFA graphs displayed together
- Visual understanding of the conversion
- See how states combine in subset construction

✅ **Enhanced Metrics**
- State count comparison
- DFA/NFA ratio calculation
- State explosion warnings
- Compact DFA indicators

---

## How to Use

### 1. Load an NFA
Choose any input method:
- Paste JSON
- Upload JSON file
- Upload image (uses Gemini AI)
- Take photo with camera

### 2. View NFA Graph
Click the **"📊 Graph"** tab to see your NFA visualized as a state diagram.

### 3. Convert to DFA
Click **"🚀 Convert to DFA"** button.

### 4. Explore DFA Results
Navigate through tabs:
- **📊 Graph** - See the DFA state diagram
- **🔄 Comparison** - View NFA and DFA side-by-side
- **📋 JSON** - Download the DFA
- **📈 Summary** - See detailed metrics

---

## Example Workflow

Try this with `examples/sample_nfa_1.json`:

1. **Load the file:**
   - Click "Upload JSON" in sidebar
   - Select `examples/sample_nfa_1.json`

2. **View NFA Graph:**
   - Click "📊 Graph" tab
   - See the NFA with 3 states (q0, q1, q2)
   - Notice non-deterministic transition from q0 on 'a'

3. **Convert:**
   - Click "🚀 Convert to DFA"
   - See step-by-step logs

4. **Compare Graphs:**
   - Click "🔄 Comparison" tab in DFA section
   - See both automata side-by-side
   - Understand how subset construction works

---

## Troubleshooting

### If graphs don't appear:

**Issue:** Module not found error
**Solution:** Already fixed! graphviz is installed.

**Issue:** Graphviz not found (even with package installed)
**Solution:** 
1. Verify dot is in PATH: `dot -V`
2. If not found, add to PATH: `C:\Program Files\Graphviz\bin`
3. Restart terminal and Streamlit

**Issue:** Permission errors
**Solution:** Run as administrator or use user installation (already done)

---

## Architecture

### Two Components Required:

1. **Graphviz Software** (System Level)
   - Provides `dot` command
   - Generates actual graph layouts
   - Location: `C:\Program Files\Graphviz\`

2. **Python graphviz Package** (Python Level)
   - Python wrapper around dot command
   - Installed via pip
   - Location: Python site-packages

### How It Works:

```
Python Code
    ↓
graphviz.Digraph
    ↓
Generates DOT syntax
    ↓
Calls 'dot' command
    ↓
Produces SVG/PNG/PDF
    ↓
Displayed in Streamlit
```

---

## Technical Details

### Installation Locations:

**Graphviz Software:**
- Global installation
- Path: System PATH includes Graphviz\bin
- Version: 14.0.2 (20251019.1705)

**Python Package:**
- User installation: `C:\Users\vishn\AppData\Roaming\Python\Python313\`
- Version: 0.21
- Used by: Streamlit app

### Streamlit Location:
```
C:\Users\vishn\AppData\Roaming\Python\Python313\Scripts\streamlit.exe
```

---

## What You Can Do Now

### 1. Visualize Any Automaton
Load any NFA/DFA JSON and see it as a graph instantly.

### 2. Export Graphs
Right-click on graph → Save image (SVG format, scalable)

### 3. Compare Automata
Use comparison view to understand conversions visually.

### 4. Learn Algorithms
See how subset construction creates DFA states from NFA state sets.

### 5. Debug Automata
Visual inspection makes it easy to spot errors in transitions.

---

## Next Steps

### Try These:

1. **Load `sample_nfa_1.json`** - See strings ending in "ab"
2. **Load `sample_nfa_2.json`** - See contains '1' pattern
3. **Load `sample_nfa_3.json`** - See even 'a's (already a DFA)

### Experiment:

1. **Create your own NFA** - Paste JSON directly
2. **Draw an NFA** - Upload image, let Gemini extract it
3. **Compare complexity** - See when DFAs explode in size

---

## Documentation

For detailed information, see:

- **`JSON_FORMAT_SPECIFICATION.md`** - JSON format reference
- **`GRAPH_VISUALIZATION_GUIDE.md`** - Complete graph guide
- **`README.md`** - General usage instructions

---

## Summary

✅ **Graphviz Software** - Installed (v14.0.2)
✅ **Python Package** - Installed (v0.21)
✅ **Streamlit App** - Running
✅ **Graph Visualization** - WORKING

**Access the app:** http://localhost:8501

Enjoy visualizing automata! 🎉
