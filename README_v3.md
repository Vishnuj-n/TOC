# NFA to DFA Visualizer v3.0 🔄

A modern, multi-page web application for converting Non-deterministic Finite Automata (NFA) to Deterministic Finite Automata (DFA) using the Subset Construction Algorithm.

## ✨ Features

- **🏠 Landing Page**: Beautiful welcome page with quick navigation
- **📝 Manual Builder**: Form-based NFA builder with interactive inputs
- **📤 Import JSON**: Upload, paste, or load example NFAs
- **🔄 Convert & Visualize**: See NFA to DFA conversion with graphs
- **ℹ️ About & Help**: Comprehensive documentation and examples
- **📊 Graph Visualization**: Visual automata diagrams (requires Graphviz)
- **📝 Detailed Logging**: Step-by-step algorithm trace
- **✅ Validation**: Automatic NFA validation
- **💾 Export**: Download results as JSON
- **🧪 Testing**: Full test suite using Streamlit app testing

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Graphviz (optional, for graph visualization):**
   - Download from: https://graphviz.org/download/
   - Add to system PATH

4. **Run the app:**
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
TOC/
├── main.py                          # Landing page
├── pages/
│   ├── 1_📝_Manual_Builder.py      # Form-based NFA builder
│   ├── 2_📤_Import_JSON.py         # JSON import page
│   ├── 3_🔄_Convert_NFA_DFA.py     # Conversion & visualization
│   └── 4_ℹ️_About.py               # Documentation & help
├── nfa_to_dfa.py                    # Core conversion algorithm
├── graph_visualizer.py              # Graph generation
├── tests/
│   ├── test_app.py                  # Streamlit app tests
│   ├── test_nfa_to_dfa.py          # Algorithm tests
│   └── fixtures.py                  # Test fixtures
├── examples/
│   ├── sample_nfa_1.json
│   ├── sample_nfa_2.json
│   └── sample_nfa_3.json
└── requirements.txt
```

## 🎯 Usage

### Method 1: Manual Builder

1. Navigate to **📝 Manual Builder**
2. Enter states: `q0, q1, q2`
3. Enter alphabet: `a, b`
4. Select start and final states
5. Define transitions in the grid
6. Click **Build NFA**
7. Click **Convert to DFA**

### Method 2: Import JSON

1. Navigate to **📤 Import JSON**
2. Choose import method:
   - Upload a `.json` file
   - Paste JSON directly
   - Load a pre-built example
3. Click **Save NFA**
4. Navigate to **🔄 Convert & Visualize**

### Method 3: Load Examples

1. Go to **📤 Import JSON**
2. Select the **Load Example** tab
3. Choose from:
   - Simple NFA (a*b+)
   - Binary String Ending with 01
   - Contains 'aba' Substring
4. Click **Load Example**

## 📋 NFA JSON Format

```json
{
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
```

### Required Fields

- `states`: Array of state names (strings)
- `alphabet`: Array of input symbols (strings)
- `start_state`: String (must be in states)
- `final_states`: Array of state names
- `transitions`: Object mapping states to symbols to destination states

### Notes

- Destination states must be **arrays** (even for single states)
- Non-determinism: Use multiple destination states
- Missing transitions are treated as ∅ (dead state)

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/test_app.py -v

# Run specific test class
pytest tests/test_app.py::TestManualBuilderPage -v

# Run with coverage
pytest tests/test_app.py --cov=. --cov-report=html
```

All 21 tests should pass! ✅

### Test Coverage

- ✅ Main page loads correctly
- ✅ Navigation buttons work
- ✅ Manual builder form functions
- ✅ JSON import (upload, paste, examples)
- ✅ NFA validation
- ✅ NFA to DFA conversion
- ✅ Graph visualization
- ✅ Session state management

## 🔧 Technical Details

### Algorithm: Subset Construction

The app uses the **Subset Construction Algorithm** (Powerset Construction):

1. **Initialize**: Start with ε-closure of NFA start state
2. **Process Queue**: For each DFA state (set of NFA states):
   - For each alphabet symbol:
     - Compute reachable NFA states
     - Create new DFA state if needed
3. **Mark Final States**: DFA states containing NFA final states
4. **Complete**: Continue until all states processed

**Complexity:**
- Time: O(2^n × |Σ|)
- Space: O(2^n)
- Where n = NFA states, |Σ| = alphabet size

### Technology Stack

- **Framework**: Streamlit
- **Language**: Python 3.8+
- **Visualization**: Graphviz
- **Testing**: pytest + Streamlit app testing
- **Algorithm**: Subset Construction

## 📖 Documentation

Comprehensive documentation is available in the **ℹ️ About & Help** page, including:

- Detailed usage instructions
- Example NFAs with explanations
- FAQ
- Technical specifications
- JSON format guide

## 🎨 Features Walkthrough

### Landing Page (main.py)
- Hero section with gradient banner
- Three-column quick start guide
- Feature highlights
- Example NFA with explanation
- Algorithm overview
- Session state indicator in sidebar

### Manual Builder
- Form-based interface for building NFAs
- Real-time validation
- Grid-based transition input
- Preview JSON before building
- Direct navigation to conversion

### Import JSON
- Three tabs: Upload, Paste, Examples
- JSON validation with detailed error messages
- Visual preview with metrics
- Transition table display
- One-click example loading

### Convert & Visualize
- NFA graph visualization
- DFA graph visualization
- Side-by-side comparison
- Algorithm trace logs
- State complexity analysis
- Download DFA as JSON

### About & Help
- Four tabs: Documentation, Examples, FAQ, Technical
- Detailed examples with descriptions
- Common questions answered
- Complete technical specification

## 🤝 Contributing

To add new features:

1. Create new page in `pages/` directory
2. Follow naming convention: `N_emoji_Name.py`
3. Add tests in `tests/test_app.py`
4. Update documentation in About page
5. Run test suite to verify

## 📝 Version History

- **v3.0**: Multi-page architecture, form-based builder, comprehensive testing
- **v2.0**: Graph visualization support
- **v1.0**: Initial release with JSON import

## 🐛 Known Issues

- Graph visualization requires Graphviz installation
- Large NFAs (>10 states) may cause slow rendering
- Epsilon (ε) transitions not currently supported

## 🔮 Future Enhancements

- [ ] Epsilon transition support
- [ ] DFA minimization
- [ ] Regex to NFA conversion
- [ ] Animation of algorithm steps
- [ ] Export graphs as PNG/SVG
- [ ] String testing (check if string is accepted)
- [ ] Dark mode support

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built with ❤️ using Streamlit

---

**💡 Tip**: NFAs can have multiple transitions per input, DFAs have exactly one!
