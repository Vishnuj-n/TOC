# Graph Visualization Guide

## Overview

The Automaton Visualizer now includes powerful graph visualization capabilities using **Graphviz**. You can view your NFAs and DFAs as beautiful state diagrams with nodes, edges, and labels.

---

## Features

### 1. NFA Graph Visualization
- View your input NFA as a directed graph
- States shown as circles
- Final states shown as double circles  
- Start state indicated with incoming arrow
- Transitions labeled with input symbols

### 2. DFA Graph Visualization
- View the converted DFA as a directed graph
- Same visual style as NFA for easy comparison
- Clearly shows deterministic transitions

### 3. Side-by-Side Comparison
- View NFA and DFA graphs together
- Compare structure and complexity
- Understand the conversion visually

---

## How to Use

### In the Streamlit App

After loading an NFA and converting to DFA, you'll see multiple tabs:

#### For NFA (Input):
- **📊 Graph Tab** - Visual diagram of the NFA
- **📋 JSON Tab** - Raw JSON data
- **📈 Summary Tab** - Statistics and metrics

#### For DFA (Output):
- **📊 Graph Tab** - Visual diagram of the DFA
- **🔄 Comparison Tab** - NFA and DFA side-by-side
- **📋 JSON Tab** - Raw JSON data with download
- **📈 Summary Tab** - Statistics and comparison metrics

### Programmatic Usage

```python
from graph_visualizer import (
    create_nfa_graph,
    create_dfa_graph,
    get_graph_svg,
    render_automaton_graph,
    compare_graphs
)

# Load your NFA
nfa = {
    "states": ["q0", "q1", "q2"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "final_states": ["q2"],
    "transitions": {
        "q0": {"a": ["q0", "q1"], "b": ["q0"]},
        "q1": {"b": ["q2"]}
    }
}

# Generate SVG for web display
svg_string = get_graph_svg(nfa, title="My NFA")

# Or save to file
render_automaton_graph(
    nfa,
    output_path="output/my_nfa",
    format="png",
    title="My NFA"
)
```

---

## Graph Elements

### Nodes (States)

#### Regular State
```
┌─────┐
│ q0  │
└─────┘
```
- Circle shape
- State name inside

#### Final State
```
╔═════╗
║ q2  ║
╚═════╝
```
- Double circle (doublecircle shape)
- Indicates accepting/final state

#### Start State
```
→ ┌─────┐
  │ q0  │
  └─────┘
```
- Arrow pointing to it from nowhere
- Labeled "start"

### Edges (Transitions)

#### Single Transition
```
┌─────┐    a    ┌─────┐
│ q0  │ ──────→ │ q1  │
└─────┘         └─────┘
```
- Directed arrow
- Labeled with input symbol

#### Multiple Symbols (Same Transition)
```
┌─────┐   a, b   ┌─────┐
│ q0  │ ───────→ │ q1  │
└─────┘          └─────┘
```
- Symbols combined with commas
- Single arrow for efficiency

#### Self-Loop
```
    ┌─ a ─┐
    ↓     │
┌─────┐   │
│ q0  │───┘
└─────┘
```
- Arrow from state to itself
- Common for "stay in state" transitions

#### Multiple Transitions (NFA)
```
         a
    ┌────────→ q1
q0 ─┤
    └────────→ q2
         a
```
- Multiple arrows from same state on same symbol
- Indicates non-determinism

---

## Graph Formats

The visualizer supports multiple output formats:

### Supported Formats

| Format | Extension | Use Case |
|--------|-----------|----------|
| **SVG** | `.svg` | Web display, scalable |
| **PNG** | `.png` | Images, presentations |
| **PDF** | `.pdf` | Documents, printing |
| **DOT** | `.dot` | Source code, editing |
| **JPEG** | `.jpg` | Photos, compression |

### Choosing a Format

```python
# For web display (best quality)
render_automaton_graph(nfa, "output/graph", format="svg")

# For presentations
render_automaton_graph(nfa, "output/graph", format="png")

# For documents
render_automaton_graph(nfa, "output/graph", format="pdf")

# For editing/source
render_automaton_graph(nfa, "output/graph", format="dot")
```

---

## Customization

### Graph Attributes

The default settings create clean, readable graphs:

```python
# Direction: Left to Right (LR)
graph.attr(rankdir='LR')

# Node shape: Circle
graph.attr('node', shape='circle')

# Final states: Double circle
graph.node(state, shape='doublecircle')
```

### Custom Styling

You can modify the graph appearance:

```python
from graph_visualizer import create_nfa_graph

nfa = {...}  # Your NFA data
graph = create_nfa_graph(nfa, title="Custom NFA")

# Customize appearance
graph.attr(rankdir='TB')  # Top to Bottom instead of Left to Right
graph.attr(bgcolor='lightblue')  # Background color
graph.attr(fontname='Arial')  # Font family
graph.attr('node', fontsize='14')  # Larger labels
graph.attr('edge', color='red')  # Red arrows

# Render
graph.render('custom_nfa', format='png')
```

---

## Examples

### Example 1: Simple NFA

**Input:**
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": {
    "q0": {"a": ["q1"]},
    "q1": {"b": ["q1"]}
  }
}
```

**Visual Output:**
```
      start
        ↓
      ┌────┐    a    ╔════╗
      │ q0 │ ──────→ ║ q1 ║
      └────┘         ╚════╝
                       ↑ b
                       └──┘
```

### Example 2: NFA with Non-determinism

**Input:**
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": {
    "q0": {"a": ["q1", "q2"]}
  }
}
```

**Visual Output:**
```
      start
        ↓
      ┌────┐    a    ┌────┐
      │ q0 │ ──────→ │ q1 │
      └────┘    a    └────┘
        │  \────────→ ╔════╗
        │             ║ q2 ║
        │             ╚════╝
```

### Example 3: DFA from Subset Construction

**Original NFA:**
- States: q0, q1, q2
- Non-deterministic on 'a'

**Resulting DFA:**
- States: {q0}, {q0,q1}, {q0,q1,q2}
- Fully deterministic

The comparison view shows both side-by-side to illustrate the conversion.

---

## Installation Requirements

### Graphviz Software

The Python `graphviz` package is a wrapper around the Graphviz software. You need both:

#### 1. Python Package (Already Installed)
```bash
uv pip install graphviz
```

#### 2. Graphviz Software

**Windows:**
1. Download from https://graphviz.org/download/
2. Run installer
3. Add to PATH: `C:\Program Files\Graphviz\bin`

**macOS:**
```bash
brew install graphviz
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install graphviz
```

**Linux (Fedora):**
```bash
sudo dnf install graphviz
```

### Verifying Installation

```bash
# Check if graphviz is installed
dot -V

# Should output something like:
# dot - graphviz version 2.50.0 (...)
```

If the command fails, Graphviz is not installed or not in PATH.

---

## Troubleshooting

### Error: "Failed to generate graph"

**Cause:** Graphviz software not installed or not in PATH

**Solution:**
1. Install Graphviz software (see Installation Requirements above)
2. Restart your terminal/IDE
3. Verify with `dot -V`
4. Restart Streamlit app

### Error: "dot: command not found"

**Cause:** Graphviz not in system PATH

**Solution (Windows):**
1. Open System Properties → Environment Variables
2. Edit PATH variable
3. Add: `C:\Program Files\Graphviz\bin`
4. Restart terminal

**Solution (Linux/macOS):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="/usr/local/bin:$PATH"
```

### Graphs not displaying in Streamlit

**Cause:** SVG rendering issue

**Solution:**
```python
# Try PNG instead of SVG
graph.format = 'png'
```

### Large graphs are slow

**Cause:** Too many states/transitions

**Solution:**
- Use simplified layout: `graph.attr(rankdir='TB')`
- Reduce font size: `graph.attr('node', fontsize='10')`
- Export to file instead of inline display

---

## Advanced Features

### 1. Exporting for LaTeX

```python
# Generate DOT source
from graph_visualizer import create_nfa_graph

nfa = {...}
graph = create_nfa_graph(nfa)

# Get DOT source code
dot_source = graph.source
print(dot_source)

# Can be included in LaTeX documents with:
# \usepackage{graphviz}
# \includegraphics{nfa.pdf}
```

### 2. Batch Processing

```python
import json
from pathlib import Path
from graph_visualizer import render_automaton_graph

# Convert all JSON files to graphs
input_dir = Path("examples")
output_dir = Path("graphs")

for json_file in input_dir.glob("*.json"):
    with open(json_file) as f:
        nfa = json.load(f)
    
    output_name = output_dir / json_file.stem
    render_automaton_graph(nfa, str(output_name), format="png")
    print(f"Generated {output_name}.png")
```

### 3. Interactive Graphs (Future)

While the current implementation generates static images, you can explore:
- **Graphviz Interactive:** Enable pan/zoom in SVG
- **D3.js:** More interactive web visualizations
- **Cytoscape.js:** Network graph library

---

## API Reference

### `create_nfa_graph(nfa_data, title="NFA")`

Create a Graphviz graph object for an NFA.

**Parameters:**
- `nfa_data` (dict): NFA specification
- `title` (str): Graph title

**Returns:** `graphviz.Digraph`

---

### `create_dfa_graph(dfa_data, title="DFA")`

Create a Graphviz graph object for a DFA.

**Parameters:**
- `dfa_data` (dict): DFA specification
- `title` (str): Graph title

**Returns:** `graphviz.Digraph`

---

### `get_graph_svg(automaton_data, title="Automaton")`

Generate SVG string representation.

**Parameters:**
- `automaton_data` (dict): NFA or DFA specification
- `title` (str): Graph title

**Returns:** `str` (SVG markup)

---

### `render_automaton_graph(automaton_data, output_path, format="png", title="Automaton", view=False)`

Render graph to file.

**Parameters:**
- `automaton_data` (dict): NFA or DFA specification
- `output_path` (str): Output path (without extension)
- `format` (str): Output format (`"png"`, `"svg"`, `"pdf"`, etc.)
- `title` (str): Graph title
- `view` (bool): Open file after rendering

**Returns:** `str` (path to rendered file)

---

### `compare_graphs(nfa_data, dfa_data)`

Create side-by-side comparison graph.

**Parameters:**
- `nfa_data` (dict): NFA specification
- `dfa_data` (dict): DFA specification

**Returns:** `graphviz.Digraph`

---

## Best Practices

### 1. Keep Graphs Readable

- **Limit states:** Graphs with >20 states become cluttered
- **Clear naming:** Use descriptive state names
- **Group symbols:** Combine multiple transitions with same source/dest

### 2. Choose Right Format

- **Web:** Use SVG (scalable, crisp)
- **Print:** Use PDF (high quality)
- **Quick view:** Use PNG (fast, universal)

### 3. Optimize Layout

- **Horizontal:** Use `rankdir='LR'` for few states
- **Vertical:** Use `rankdir='TB'` for many states
- **Hierarchical:** Good for layered automata

### 4. Performance

- **Cache graphs:** Don't regenerate unnecessarily
- **Async rendering:** Generate graphs in background for large automata
- **Progressive loading:** Show simplified graph first, then detailed

---

## Examples in Action

See the `examples/` directory for sample NFA files you can visualize:

1. **sample_nfa_1.json** - Strings ending in "ab"
2. **sample_nfa_2.json** - Contains at least one '1'
3. **sample_nfa_3.json** - Even number of 'a's

Load any of these in the Streamlit app and explore the Graph tabs!

---

## Resources

- [Graphviz Official Documentation](https://graphviz.org/documentation/)
- [Python graphviz Package](https://graphviz.readthedocs.io/)
- [DOT Language Guide](https://graphviz.org/doc/info/lang.html)
- [Gallery of Graphviz Examples](https://graphviz.org/gallery/)

---

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Part of:** Automaton Visualizer Project
