# graph_visualizer.py - State Diagram Generation

## Overview

`graph_visualizer.py` provides visual representation capabilities for finite automata using the Graphviz library. It generates professional-quality state diagrams with proper formatting, making NFAs and DFAs easy to understand and analyze visually.

**File Statistics:**
- **Lines of Code:** 269
- **Main Functions:** 5
- **Output Formats:** SVG, PNG, PDF, DOT
- **Dependencies:** graphviz (Python package + system software)

---

## Purpose and Use Cases

### Primary Use Cases

1. **Educational Visualization** - Help students understand automata structure
2. **Algorithm Verification** - Visually verify NFA→DFA conversion correctness
3. **Documentation** - Generate diagrams for reports and presentations
4. **Debugging** - Spot errors in automaton definitions
5. **Comparison** - Side-by-side NFA/DFA analysis

---

## Architecture

### Component Flow

```
Automaton Data (JSON)
    │
    ├─→ create_nfa_graph() / create_dfa_graph()
    │       │
    │       ├─→ Parse states, transitions
    │       ├─→ Create Graphviz Digraph
    │       ├─→ Add nodes (states)
    │       └─→ Add edges (transitions)
    │
    ├─→ get_graph_svg() [for web display]
    │       └─→ Pipe to SVG bytes
    │
    ├─→ render_automaton_graph() [for file export]
    │       └─→ Save to PNG/PDF/SVG
    │
    └─→ compare_graphs() [for side-by-side]
            └─→ Create clustered subgraphs
```

---

## Code Structure

### 1. Imports and Type Hints

```python
from typing import Dict, List, Union
import graphviz
```

**Dependencies:**
- `graphviz`: Python bindings for Graphviz software
- `typing`: Type annotations for clarity

**System Requirement:** Graphviz software must be installed separately.

---

### 2. Function: `create_nfa_graph`

```python
def create_nfa_graph(nfa_data: dict, title: str = "NFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of an NFA."""
```

**Purpose:** Generate a Graphviz Digraph object from NFA JSON data.

---

#### Step 1: Initialize Graph

```python
graph = graphviz.Digraph(name=title, comment=title)
graph.attr(rankdir='LR')  # Left to right layout
graph.attr('node', shape='circle')
```

**Graph Attributes:**
- `rankdir='LR'`: Horizontal layout (left → right)
- `node shape='circle'`: Default circular states

**Alternative Layouts:**
- `'TB'`: Top to bottom (vertical)
- `'BT'`: Bottom to top
- `'RL'`: Right to left

**Design Choice:** Left-to-right mimics reading direction and is standard in automata theory.

---

#### Step 2: Extract Data

```python
states = nfa_data["states"]
start_state = nfa_data["start_state"]
final_states = nfa_data["final_states"]
transitions = nfa_data["transitions"]
```

**Extraction:** Unpack NFA components for easy access.

---

#### Step 3: Add Start Indicator

```python
graph.node('', shape='none', width='0', height='0')
graph.edge('', start_state, label='start')
```

**Visual Representation:**
```
→ q0
```

**Technique:**
- Invisible node (`shape='none'`)
- Zero dimensions
- Arrow to start state
- Labeled "start"

**Why?** Standard automata notation: arrow pointing to initial state.

---

#### Step 4: Add State Nodes

```python
for state in states:
    if state in final_states:
        # Final states have double circle
        graph.node(state, shape='doublecircle')
    else:
        # Regular states
        graph.node(state, shape='circle')
```

**Node Shapes:**
- **Regular States:** `circle` (single circle)
- **Final/Accepting States:** `doublecircle` (double circle)

**Example Visual:**
```
○ q0    (regular)
◎ q1    (final)
```

**Standard Convention:** Double circles universally indicate accepting states in automata theory.

---

#### Step 5: Group Transition Labels

```python
edge_labels: Dict[tuple, List[str]] = {}

for source_state, trans_map in transitions.items():
    for symbol, dest_states in trans_map.items():
        # NFA: dest_states is a list
        if isinstance(dest_states, list):
            for dest_state in dest_states:
                key = (source_state, dest_state)
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
```

**Purpose:** Combine multiple transitions between same states.

**Example:**
```json
// Input transitions:
"q0": {
  "a": ["q1"],
  "b": ["q1"]
}

// Grouped:
edge_labels = {
  ("q0", "q1"): ["a", "b"]
}
```

**Visualization:**
```
Before grouping:
q0 --a--> q1
q0 --b--> q1

After grouping:
q0 --a,b--> q1
```

**Benefit:** Cleaner diagrams with fewer arrows.

---

#### Step 6: Handle DFA Format

```python
else:
    # DFA: dest_states is a string
    key = (source_state, dest_states)
    if key not in edge_labels:
        edge_labels[key] = []
    edge_labels[key].append(symbol)
```

**Flexibility:** Function handles both NFA (list targets) and DFA (string target) formats.

---

#### Step 7: Add Edges

```python
for (source, dest), symbols in edge_labels.items():
    label = ', '.join(sorted(symbols))
    graph.edge(source, dest, label=label)
```

**Edge Creation:**
- Source → Destination
- Label: Comma-separated symbols
- Sorted for consistency

**Example Label:** `"a, b, c"` for transitions on symbols a, b, and c.

---

#### Step 8: Return Graph

```python
return graph
```

**Return Type:** `graphviz.Digraph` object ready for rendering.

---

### 3. Function: `create_dfa_graph`

```python
def create_dfa_graph(dfa_data: dict, title: str = "DFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of a DFA."""
    return create_nfa_graph(dfa_data, title)
```

**Implementation:** Delegates to `create_nfa_graph`.

**Why?** 
- DFA visualization identical to NFA
- Only data structure differs (single vs multiple targets)
- Code reuse via delegation

**Design Pattern:** DRY (Don't Repeat Yourself)

---

### 4. Function: `render_automaton_graph`

```python
def render_automaton_graph(
    automaton_data: dict,
    output_path: str,
    format: str = 'png',
    title: str = "Automaton",
    view: bool = False
) -> str:
    """Render an automaton graph to a file."""
```

**Purpose:** Export graph to image file.

---

#### Parameters

- **`automaton_data`**: NFA or DFA dictionary
- **`output_path`**: Filename without extension
- **`format`**: Output format (`'png'`, `'pdf'`, `'svg'`, `'dot'`)
- **`title`**: Graph title
- **`view`**: Auto-open file after rendering

---

#### Implementation

```python
graph = create_nfa_graph(automaton_data, title)
graph.format = format
rendered_path = graph.render(output_path, view=view, cleanup=True)
return rendered_path
```

**Steps:**
1. Create graph object
2. Set output format
3. Render to file (cleanup DOT source)
4. Return path to rendered file

**`cleanup=True`:** Deletes intermediate `.dot` file, keeps only final output.

---

#### Supported Formats

- **PNG** - Raster image (good for web)
- **SVG** - Vector image (scalable, best quality)
- **PDF** - Vector document (for printing)
- **DOT** - Source code (for debugging)
- **JPEG** - Compressed raster (smaller file size)

**Recommendation:** SVG for quality, PNG for compatibility.

---

### 5. Function: `get_graph_svg`

```python
def get_graph_svg(automaton_data: dict, title: str = "Automaton") -> str:
    """Generate SVG string representation of an automaton graph."""
    graph = create_nfa_graph(automaton_data, title)
    svg_bytes = graph.pipe(format='svg')
    return svg_bytes.decode('utf-8')
```

**Purpose:** Generate SVG as string for web display (no file I/O).

---

#### Why SVG String?

**Use Case:** Streamlit and web frameworks need in-memory images.

**Benefit:**
- No disk writes
- Instant display
- Scalable in browser
- Smaller than PNG

**Streamlit Integration:**
```python
svg_content = get_graph_svg(nfa_data)
st.image(svg_content, use_container_width=True)
```

---

#### Pipe vs Render

- **`pipe()`**: Returns bytes (in-memory)
- **`render()`**: Writes to file

**Choice:** Use `pipe()` for web, `render()` for export.

---

### 6. Function: `compare_graphs`

```python
def compare_graphs(nfa_data: dict, dfa_data: dict) -> graphviz.Digraph:
    """Create a side-by-side comparison of NFA and DFA."""
```

**Purpose:** Generate single graph with both NFA and DFA for comparison.

---

#### Step 1: Create Main Graph

```python
main_graph = graphviz.Digraph(name='Comparison')
main_graph.attr(rankdir='LR')
main_graph.attr(label='NFA → DFA Conversion', fontsize='20')
```

**Attributes:**
- Horizontal layout
- Title label
- Large font for title

---

#### Step 2: Create NFA Subgraph

```python
with main_graph.subgraph(name='cluster_nfa') as nfa_cluster:
    nfa_cluster.attr(label='NFA', fontsize='16')
    nfa_cluster.attr(style='rounded', color='blue')
```

**Cluster Attributes:**
- `name='cluster_nfa'`: Prefix `cluster_` creates visible box
- `label='NFA'`: Subgraph title
- `style='rounded'`: Rounded corners
- `color='blue'`: Border color

**Visual Effect:** NFA states grouped in blue box.

---

#### Step 3: Add NFA Components

```python
# Add NFA start marker
nfa_cluster.node('nfa_start', shape='none', width='0', height='0')
nfa_cluster.edge('nfa_start', f'nfa_{start_state}', label='start')

# Add NFA states
for state in states:
    node_id = f'nfa_{state}'
    if state in final_states:
        nfa_cluster.node(node_id, label=state, shape='doublecircle')
    else:
        nfa_cluster.node(node_id, label=state, shape='circle')
```

**Node ID Prefixing:** `nfa_{state}` prevents collision with DFA states.

**Example:**
- NFA state `q0` → node ID `nfa_q0`
- DFA state `q0` → node ID `dfa_q0`

---

#### Step 4: Add NFA Transitions

```python
# Group transitions by (source, dest)
edge_labels: Dict[tuple, List[str]] = {}

for source_state, trans_map in transitions.items():
    for symbol, dest_states in trans_map.items():
        if isinstance(dest_states, list):
            for dest_state in dest_states:
                key = (f'nfa_{source_state}', f'nfa_{dest_state}')
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)

# Add edges
for (source, dest), symbols in edge_labels.items():
    label = ', '.join(sorted(symbols))
    nfa_cluster.edge(source, dest, label=label)
```

**Same logic as `create_nfa_graph`, but with prefixed node IDs.**

---

#### Step 5: Create DFA Subgraph

```python
with main_graph.subgraph(name='cluster_dfa') as dfa_cluster:
    dfa_cluster.attr(label='DFA', fontsize='16')
    dfa_cluster.attr(style='rounded', color='green')
    
    # ... (same logic as NFA but with dfa_ prefix and green color)
```

**Parallel Structure:** DFA subgraph mirrors NFA structure with green border.

---

#### Step 6: Return Comparison Graph

```python
return main_graph
```

**Result:** Single graph with two clustered subgraphs side-by-side.

**Visual Layout:**
```
┌─────────────────────────────────────────┐
│      NFA → DFA Conversion               │
├────────────────┬────────────────────────┤
│ ┌───NFA─────┐ │ ┌───DFA──────────────┐ │
│ │ → ○ q0    │ │ │ → ○ q0             │ │
│ │   ↓ a,b   │ │ │   ↓ a   ↓ b       │ │
│ │   ◎ q1    │ │ │   ◎ q1  ○ q2      │ │
│ └───────────┘ │ └────────────────────┘ │
└────────────────┴────────────────────────┘
```

---

## Graphviz Attributes Reference

### Graph Attributes

```python
graph.attr(rankdir='LR')      # Layout direction
graph.attr(label='Title')     # Graph title
graph.attr(fontsize='20')     # Title font size
graph.attr(bgcolor='white')   # Background color
```

---

### Node Attributes

```python
# Shape
graph.node('q0', shape='circle')        # Regular state
graph.node('q1', shape='doublecircle')  # Final state
graph.node('', shape='none')            # Invisible

# Size
graph.node('q0', width='0.5', height='0.5')

# Style
graph.node('q0', style='filled', fillcolor='lightblue')

# Label
graph.node('q0', label='Start State')
```

---

### Edge Attributes

```python
# Label
graph.edge('q0', 'q1', label='a, b')

# Style
graph.edge('q0', 'q1', style='dashed')
graph.edge('q0', 'q1', color='red')

# Arrow
graph.edge('q0', 'q1', arrowhead='normal')  # Default
graph.edge('q0', 'q1', arrowhead='diamond')
```

---

### Subgraph Attributes

```python
with graph.subgraph(name='cluster_0') as sub:
    sub.attr(label='Cluster')        # Subgraph label
    sub.attr(style='rounded')        # Border style
    sub.attr(color='blue')           # Border color
    sub.attr(bgcolor='lightgray')    # Background
```

---

## Design Decisions

### 1. Why Graphviz?

**Alternatives:**
- ❌ NetworkX + Matplotlib: More code, less control
- ❌ D3.js: Requires JavaScript, complex
- ✅ Graphviz: Standard, powerful, simple API

**Benefits:**
- Industry standard for graph visualization
- Automatic layout (no manual positioning)
- Multiple output formats
- High-quality rendering

---

### 2. Why SVG for Web?

**Alternatives:**
- PNG: Fixed resolution, larger files
- Canvas: Requires JavaScript
- SVG: Scalable, embeddable, smaller

**Benefits:**
- Scales without pixelation
- Smaller file size than PNG
- Works in all browsers
- Can be embedded inline

---

### 3. Edge Label Grouping

**Without Grouping:**
```
q0 --a--> q1
q0 --b--> q1
q0 --c--> q1
```

**With Grouping:**
```
q0 --a,b,c--> q1
```

**Benefits:**
- Cleaner visualization
- Fewer arrows
- Easier to read
- Standard notation

---

### 4. Node ID Prefixing in Comparisons

**Problem:** NFA and DFA might have same state names.

**Solution:** Prefix with `nfa_` and `dfa_`.

**Example:**
- NFA `q0` → `nfa_q0`
- DFA `q0` → `dfa_q0`

**Benefit:** No naming collisions.

---

## Output Format Comparison

### SVG (Scalable Vector Graphics)

**Pros:**
- ✅ Infinite zoom without quality loss
- ✅ Small file size
- ✅ Editable in Illustrator/Inkscape
- ✅ Web-friendly

**Cons:**
- ❌ Complex for very large graphs
- ❌ May not render in old browsers

**Best For:** Web display, presentations, documentation

---

### PNG (Portable Network Graphics)

**Pros:**
- ✅ Universal compatibility
- ✅ Simple format
- ✅ Transparent background support

**Cons:**
- ❌ Fixed resolution (pixelates when scaled)
- ❌ Larger file size than SVG

**Best For:** Email attachments, quick sharing

---

### PDF (Portable Document Format)

**Pros:**
- ✅ Print-ready
- ✅ Vector format
- ✅ Page layout support

**Cons:**
- ❌ Larger file size
- ❌ Requires PDF reader

**Best For:** Printing, academic papers, reports

---

### DOT (Graphviz Source)

**Pros:**
- ✅ Human-readable
- ✅ Editable
- ✅ Version control friendly

**Cons:**
- ❌ Requires Graphviz to render
- ❌ Not directly viewable

**Best For:** Debugging, manual tweaking, collaboration

---

## Edge Cases Handled

### 1. Self-Loops

```json
"q0": {
  "a": ["q0"]
}
```

**Visualization:**
```
   ⤴ a
○ q0
```

**Handling:** Graphviz automatically creates curved self-loop arrow.

---

### 2. Multiple Transitions (Non-determinism)

```json
"q0": {
  "a": ["q1", "q2"]
}
```

**Visualization:**
```
       a
○ q0 ───→ ○ q1
    ╲
     ╲a
      ╲
       ○ q2
```

**Handling:** Separate edges created for each target.

---

### 3. Bidirectional Transitions

```json
"q0": {"a": ["q1"]},
"q1": {"b": ["q0"]}
```

**Visualization:**
```
     a
○ q0 ⇄ ○ q1
     b
```

**Handling:** Graphviz curves arrows to avoid overlap.

---

### 4. Unreachable States

```json
{
  "states": ["q0", "q1", "q2"],
  "start_state": "q0",
  "transitions": {
    "q0": {"a": ["q1"]}
    // q2 is unreachable
  }
}
```

**Visualization:** All states shown, but `q2` has no incoming edges.

**Handling:** Visual clarity of unreachability.

---

### 5. Dead States

```json
"dead": {}  // No outgoing transitions
```

**Visualization:**
```
○ dead  (isolated or with only incoming edges)
```

**Handling:** Rendered normally, visually obvious as sink.

---

## Common Issues and Solutions

### Issue 1: Graphviz Not Found

**Symptom:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'dot'
```

**Cause:** Graphviz software not installed.

**Solution:**
```powershell
# Windows
choco install graphviz

# Add to PATH if needed
$env:PATH += ";C:\Program Files\Graphviz\bin"
```

---

### Issue 2: Python Package Not Found

**Symptom:**
```
ModuleNotFoundError: No module named 'graphviz'
```

**Cause:** Python package not installed.

**Solution:**
```powershell
pip install graphviz
```

---

### Issue 3: Overlapping Edges

**Symptom:** Multiple edges between states overlap and labels are unreadable.

**Solution:** Edge grouping (already implemented).

---

### Issue 4: Large Graph Layout

**Symptom:** Graph with 50+ states is cluttered.

**Solution:**
```python
graph.attr(ranksep='1.0')  # Increase vertical spacing
graph.attr(nodesep='0.5')  # Increase horizontal spacing
```

---

### Issue 5: Unicode Symbols

**Symptom:** Epsilon (ε) doesn't render correctly.

**Solution:**
```python
graph.attr('edge', fontname='DejaVu Sans')
graph.attr('node', fontname='DejaVu Sans')
```

---

## Performance Considerations

### Time Complexity

- **Graph Creation:** O(V + E)
  - V = number of states (vertices)
  - E = number of transitions (edges)

- **Rendering:** O(V² + E) typical (layout algorithm)
  - Depends on Graphviz layout engine

---

### Space Complexity

- **Memory:** O(V + E)
- **Output File:** Depends on format and size

---

### Optimization Tips

#### 1. Limit Graph Size

```python
MAX_STATES = 50

if len(automaton_data["states"]) > MAX_STATES:
    st.warning("Graph too large for visualization")
    return None
```

---

#### 2. Use Simplified Layout

```python
graph.attr('graph', layout='dot')     # Hierarchical (default)
graph.attr('graph', layout='neato')   # Spring model (faster for small graphs)
graph.attr('graph', layout='fdp')     # Force-directed (good for large graphs)
```

---

#### 3. Cache Rendered Graphs

```python
@st.cache_data
def get_cached_svg(nfa_json_str):
    nfa_data = json.loads(nfa_json_str)
    return get_graph_svg(nfa_data)
```

---

## Testing Strategies

### Unit Tests

```python
def test_create_nfa_graph():
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {"q0": {"a": ["q1"]}}
    }
    
    graph = create_nfa_graph(nfa)
    
    assert graph is not None
    assert isinstance(graph, graphviz.Digraph)
    assert 'q0' in graph.body[0] or 'q0' in str(graph)
```

---

### Integration Tests

```python
def test_render_to_file(tmp_path):
    nfa = load_sample_nfa()
    output = tmp_path / "test_nfa"
    
    result = render_automaton_graph(nfa, str(output), format='png')
    
    assert os.path.exists(result)
    assert result.endswith('.png')
```

---

### Visual Regression Tests

```python
def test_graph_appearance():
    nfa = load_sample_nfa()
    svg1 = get_graph_svg(nfa)
    
    # Render again
    svg2 = get_graph_svg(nfa)
    
    # Should be identical (deterministic)
    assert svg1 == svg2
```

---

## Future Enhancements

### 1. Interactive Graphs

Use D3.js or Cytoscape.js for interactive web graphs:
```python
def create_interactive_graph(nfa_data):
    # Generate JSON for D3.js
    nodes = [{"id": s, "final": s in nfa_data["final_states"]} 
             for s in nfa_data["states"]]
    links = ...
    return {"nodes": nodes, "links": links}
```

---

### 2. State Highlighting

Highlight specific states:
```python
def create_nfa_graph(nfa_data, highlight_states=[]):
    for state in states:
        if state in highlight_states:
            graph.node(state, style='filled', fillcolor='yellow')
```

---

### 3. Animation Support

Generate sequence of graphs:
```python
def animate_conversion(nfa, conversion_steps):
    frames = []
    for step in conversion_steps:
        graph = create_graph_with_state(nfa, step)
        frames.append(render_to_png(graph))
    return create_gif(frames)
```

---

### 4. Layout Customization

```python
def create_nfa_graph(nfa_data, layout='dot', **graph_attrs):
    graph = graphviz.Digraph()
    graph.attr('graph', layout=layout)
    for key, value in graph_attrs.items():
        graph.attr('graph', key, value)
    # ... rest of function
```

---

### 5. Export Templates

```python
def export_for_latex(nfa_data):
    # Generate TikZ code for LaTeX
    return tikz_code

def export_for_powerpoint(nfa_data):
    # Generate SVG optimized for PPT
    return svg_content
```

---

## Dependencies

### System Requirements

```powershell
# Windows
choco install graphviz

# Verify
dot -V
```

### Python Requirements

```python
graphviz>=0.20.0  # Python bindings
```

---

## Graphviz Layout Engines

### dot (Hierarchical)

**Best For:** Directed graphs, flowcharts, automata
**Characteristics:** Top-down or left-right layout

---

### neato (Spring Model)

**Best For:** Undirected graphs, small networks
**Characteristics:** Minimizes edge crossings

---

### fdp (Force-Directed)

**Best For:** Large graphs, network diagrams
**Characteristics:** Distributed layout

---

### circo (Circular)

**Best For:** Cyclic graphs, state machines
**Characteristics:** Circular arrangement

---

## Conclusion

`graph_visualizer.py` provides robust graph visualization capabilities:

- **Flexibility:** Multiple output formats (SVG, PNG, PDF)
- **Quality:** Professional-looking diagrams
- **Efficiency:** Automatic layout via Graphviz
- **Compatibility:** Works with both NFA and DFA formats
- **Comparison:** Side-by-side visualization support

The module enhances understanding of automata through visual representation, making it an essential component of the educational toolkit.

---

## Example Gallery

### Simple NFA
```
→ ○ q0 --a,b--> ◎ q1
  ↺ a
```

### Complex NFA with Non-determinism
```
     a          b
→ ○ q0 ───→ ○ q1 ───→ ◎ q2
    │
    │ a
    └───→ ○ q3
```

### Minimal DFA
```
→ ○ q0 ⇄ ◎ q1
     a,b
```

### State Explosion Example
```
NFA (3 states) → DFA (8 states showing all subsets)
```
