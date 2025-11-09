# NFA to DFA Visualizer - Overview

## Project Description

A modern, multi-page Streamlit web application for converting Non-deterministic Finite Automata (NFA) 
to Deterministic Finite Automata (DFA) using the Subset Construction Algorithm.

## Features

- **Multi-page Architecture**: Clean separation using Streamlit's native page system
- **Manual NFA Builder**: Form-based interactive builder with real-time validation
- **JSON Import**: Upload files, paste JSON, or load pre-built examples
- **Visual Graphs**: Beautiful automata visualizations using Graphviz
- **Algorithm Trace**: Step-by-step conversion logs
- **Export Results**: Download DFA as JSON
- **Comprehensive Testing**: Full test suite with 100% pass rate

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Visualization**: Graphviz
- **Testing**: pytest, Streamlit app testing
- **Algorithm**: Subset Construction (Powerset Construction)

## Project Structure

```
TOC/
├── main.py                      # Landing page
├── nfa_to_dfa.py               # Core conversion algorithm
├── graph_visualizer.py         # Graph generation
├── pages/                      # Multi-page app pages
│   ├── 1_📝_Manual_Builder.py
│   ├── 2_📤_Import_JSON.py
│   ├── 3_🔄_Convert_NFA_DFA.py
│   └── 4_ℹ️_About.py
├── tests/                      # Test suite
│   ├── test_app.py
│   ├── test_nfa_to_dfa.py
│   └── fixtures.py
├── examples/                   # Sample NFA files
├── doc/                        # Documentation
└── requirements.txt           # Dependencies
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py

# Run tests
pytest tests/ -v
```

## Version

**v3.0** - Multi-page architecture with optimized codebase (60% line reduction)

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [GRAPH_VISUALIZATION_GUIDE.md](GRAPH_VISUALIZATION_GUIDE.md) - Graph setup and usage
- [JSON_FORMAT_SPECIFICATION.md](JSON_FORMAT_SPECIFICATION.md) - NFA/DFA JSON format
- [V3_IMPLEMENTATION_SUMMARY.md](V3_IMPLEMENTATION_SUMMARY.md) - v3.0 implementation details
- [OPTIMIZATION_SUMMARY.md](OPTIMIZATION_SUMMARY.md) - Code optimization details

## License

Educational use only.
