"""Graph visualization for NFAs and DFAs using Graphviz.

This module provides functions to generate visual representations of finite automata
as directed graphs using the Graphviz library.
"""

from typing import Dict, List, Union, Optional
import graphviz


def create_nfa_graph(nfa_data: dict, title: str = "NFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of an NFA.
    
    Args:
        nfa_data: Dictionary containing NFA specification
        title: Title for the graph
    
    Returns:
        graphviz.Digraph object that can be rendered
    
    Example:
        >>> nfa = {"states": ["q0", "q1"], ...}
        >>> graph = create_nfa_graph(nfa)
        >>> graph.render('nfa_diagram', format='png')
    """
    # Create directed graph
    graph = graphviz.Digraph(name=title, comment=title)
    graph.attr(rankdir='LR')  # Left to right layout
    graph.attr('node', shape='circle')
    
    states = nfa_data["states"]
    start_state = nfa_data["start_state"]
    final_states = nfa_data["final_states"]
    transitions = nfa_data["transitions"]
    
    # Add invisible start node for initial arrow
    graph.node('', shape='none', width='0', height='0')
    graph.edge('', start_state, label='start')
    
    # Add all states
    for state in states:
        if state in final_states:
            # Final states have double circle
            graph.node(state, shape='doublecircle')
        else:
            # Regular states
            graph.node(state, shape='circle')
    
    # Add transitions
    # Group transitions by (source, dest) to combine labels
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
            # DFA: dest_states is a string
            else:
                key = (source_state, dest_states)
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
    
    # Add edges with combined labels
    for (source, dest), symbols in edge_labels.items():
        label = ', '.join(sorted(symbols))
        graph.edge(source, dest, label=label)
    
    return graph


def create_dfa_graph(dfa_data: dict, title: str = "DFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of a DFA.
    
    Args:
        dfa_data: Dictionary containing DFA specification
        title: Title for the graph
    
    Returns:
        graphviz.Digraph object that can be rendered
    
    Example:
        >>> dfa = {"states": ["{q0}", "{q0,q1}"], ...}
        >>> graph = create_dfa_graph(dfa)
        >>> graph.render('dfa_diagram', format='png')
    """
    # DFA graph creation is the same as NFA
    # The difference is in the data structure (single vs multiple destinations)
    return create_nfa_graph(dfa_data, title)


def render_automaton_graph(
    automaton_data: dict,
    output_path: str,
    format: str = 'png',
    title: str = "Automaton",
    view: bool = False
) -> str:
    """Render an automaton graph to a file.
    
    Args:
        automaton_data: NFA or DFA data dictionary
        output_path: Output file path (without extension)
        format: Output format ('png', 'pdf', 'svg', etc.)
        title: Graph title
        view: Whether to open the rendered file automatically
    
    Returns:
        Path to the rendered file
    
    Example:
        >>> nfa = load_nfa("example.json")
        >>> render_automaton_graph(nfa, "output/my_nfa", format='svg')
        'output/my_nfa.svg'
    """
    graph = create_nfa_graph(automaton_data, title)
    graph.format = format
    rendered_path = graph.render(output_path, view=view, cleanup=True)
    return rendered_path


def get_graph_svg(automaton_data: dict, title: str = "Automaton") -> str:
    """Generate SVG string representation of an automaton graph.
    
    This is useful for displaying graphs in web interfaces without
    saving to disk.
    
    Args:
        automaton_data: NFA or DFA data dictionary
        title: Graph title
    
    Returns:
        SVG string that can be embedded in HTML
    
    Example:
        >>> nfa = {"states": ["q0", "q1"], ...}
        >>> svg_string = get_graph_svg(nfa, "My NFA")
        >>> # Use in Streamlit: st.image(svg_string)
    """
    graph = create_nfa_graph(automaton_data, title)
    svg_bytes = graph.pipe(format='svg')
    return svg_bytes.decode('utf-8')


def _add_automaton_to_subgraph(
    automaton_data: dict,
    subgraph: graphviz.Digraph,
    prefix: str = "",
    title: str = "Automaton",
    color: str = "blue"
) -> None:
    """Add an automaton's states and transitions to a subgraph.
    
    This is a helper function to avoid code duplication between create_nfa_graph
    and compare_graphs. It adds all states, transitions, and formatting to the
    provided subgraph.
    
    Args:
        automaton_data: NFA or DFA data dictionary
        subgraph: Graphviz subgraph to add nodes and edges to
        prefix: Prefix for node IDs (e.g., 'nfa_' or 'dfa_') to avoid collisions
        title: Title/label for the subgraph
        color: Border color for the subgraph cluster
    """
    # Set subgraph attributes if it's a cluster
    if hasattr(subgraph, 'attr'):
        subgraph.attr(label=title, fontsize='16')
        subgraph.attr(style='rounded', color=color)
    
    states = automaton_data["states"]
    start_state = automaton_data["start_state"]
    final_states = automaton_data["final_states"]
    transitions = automaton_data["transitions"]
    
    # Add invisible start node for initial arrow
    start_marker_id = f'{prefix}start' if prefix else ''
    subgraph.node(start_marker_id, shape='none', width='0', height='0')
    subgraph.edge(start_marker_id, f'{prefix}{start_state}', label='start')
    
    # Add all states
    for state in states:
        node_id = f'{prefix}{state}'
        if state in final_states:
            # Final states have double circle
            subgraph.node(node_id, label=state, shape='doublecircle')
        else:
            # Regular states
            subgraph.node(node_id, label=state, shape='circle')
    
    # Add transitions
    # Group transitions by (source, dest) to combine labels
    edge_labels: Dict[tuple, List[str]] = {}
    
    for source_state, trans_map in transitions.items():
        for symbol, dest_states in trans_map.items():
            # NFA: dest_states is a list
            if isinstance(dest_states, list):
                for dest_state in dest_states:
                    key = (f'{prefix}{source_state}', f'{prefix}{dest_state}')
                    if key not in edge_labels:
                        edge_labels[key] = []
                    edge_labels[key].append(symbol)
            # DFA: dest_states is a string
            else:
                key = (f'{prefix}{source_state}', f'{prefix}{dest_states}')
                if key not in edge_labels:
                    edge_labels[key] = []
                edge_labels[key].append(symbol)
    
    # Add edges with combined labels
    for (source, dest), symbols in edge_labels.items():
        label = ', '.join(sorted(symbols))
        subgraph.edge(source, dest, label=label)


def compare_graphs(nfa_data: dict, dfa_data: dict) -> graphviz.Digraph:
    """Create a side-by-side comparison of NFA and DFA.
    
    Uses the _add_automaton_to_subgraph helper to avoid code duplication.
    
    Args:
        nfa_data: NFA data dictionary
        dfa_data: DFA data dictionary
    
    Returns:
        Combined graph showing both automata
    """
    # Create a parent graph with subgraphs
    main_graph = graphviz.Digraph(name='Comparison')
    main_graph.attr(rankdir='LR')
    main_graph.attr(label='NFA → DFA Conversion', fontsize='20')
    
    # Create NFA subgraph using helper
    with main_graph.subgraph(name='cluster_nfa') as nfa_cluster:
        _add_automaton_to_subgraph(
            nfa_data,
            nfa_cluster,
            prefix='nfa_',
            title='NFA',
            color='blue'
        )
    
    # Create DFA subgraph using helper
    with main_graph.subgraph(name='cluster_dfa') as dfa_cluster:
        _add_automaton_to_subgraph(
            dfa_data,
            dfa_cluster,
            prefix='dfa_',
            title='DFA',
            color='green'
        )
    
    return main_graph
