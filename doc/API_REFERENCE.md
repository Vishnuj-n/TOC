# API Reference

## Core Functions

### `nfa_to_dfa.py`

#### `convert_nfa_to_dfa(nfa_data: dict) -> Tuple[dict, List[str]]`

Convert NFA to DFA using subset construction algorithm.

**Parameters:**
- `nfa_data`: Dictionary with keys: `states`, `alphabet`, `start_state`, `final_states`, `transitions`

**Returns:**
- `Tuple[dict, List[str]]`: (dfa_data, conversion_logs)

**Raises:**
- `ValueError`: If NFA data is invalid

**Example:**
```python
nfa = {
    "states": ["q0", "q1"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "final_states": ["q1"],
    "transitions": {"q0": {"a": ["q0", "q1"]}}
}
dfa, logs = convert_nfa_to_dfa(nfa)
```

#### `validate_nfa(nfa_data: dict) -> Tuple[bool, str]`

Validate NFA data structure.

**Parameters:**
- `nfa_data`: Dictionary to validate

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

**Example:**
```python
is_valid, msg = validate_nfa(nfa_data)
if is_valid:
    print("Valid NFA")
else:
    print(f"Invalid: {msg}")
```

### `graph_visualizer.py`

#### `create_nfa_graph(nfa_data: dict, title: str = "NFA") -> graphviz.Digraph`

Create Graphviz directed graph of NFA/DFA.

**Parameters:**
- `nfa_data`: NFA/DFA data dictionary
- `title`: Graph title (default: "NFA")

**Returns:**
- `graphviz.Digraph`: Renderable graph object

#### `get_graph_svg(automaton_data: dict, title: str = "Automaton") -> str`

Generate SVG string of automaton graph.

**Parameters:**
- `automaton_data`: NFA/DFA data
- `title`: Graph title

**Returns:**
- `str`: SVG markup string

#### `compare_graphs(nfa_data: dict, dfa_data: dict) -> graphviz.Digraph`

Create side-by-side comparison of NFA and DFA.

**Parameters:**
- `nfa_data`: NFA data dictionary
- `dfa_data`: DFA data dictionary

**Returns:**
- `graphviz.Digraph`: Combined comparison graph

## Data Structures

### NFA/DFA JSON Format

```python
{
    "states": List[str],          # State names
    "alphabet": List[str],        # Input symbols
    "start_state": str,           # Initial state
    "final_states": List[str],    # Accepting states
    "transitions": {              # State transitions
        str: {                    # From state
            str: List[str]        # Symbol -> [to states]
        }
    }
}
```

### Example

```python
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

## Session State

Streamlit session state keys used:

- `nfa_data`: Currently loaded NFA
- `dfa_data`: Converted DFA result
- `conversion_logs`: Algorithm trace logs
- `converted`: Boolean flag for conversion status
- `transitions_data`: Temporary transition data in builder
