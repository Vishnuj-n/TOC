"""Graph visualization for NFAs and DFAs using Graphviz.

This module provides functions to generate visual representations of finite automata
as directed graphs using the Graphviz library.
"""

from typing import Dict, List
import graphviz


def _add_automaton_to_subgraph(
    cluster: graphviz.Digraph,
    automaton_data: dict,
    prefix: str = ""
) -> None:
    """Helper function to add automaton states and transitions to a subgraph.
    
    Args:
        cluster: Graphviz subgraph to add nodes/edges to
        automaton_data: Automaton data dictionary
        prefix: Prefix for node IDs (e.g., 'nfa_' or 'dfa_')
    """
    states = automaton_data["states"]
    start_state = automaton_data["start_state"]
    final_states = automaton_data["final_states"]
    transitions = automaton_data["transitions"]
    
    # Add start marker
    cluster.node(f'{prefix}start', shape='none', width='0', height='0')
    cluster.edge(f'{prefix}start', f'{prefix}{start_state}', label='start')
    
    # Add states
    for state in states:
        node_id = f'{prefix}{state}'
        shape = 'doublecircle' if state in final_states else 'circle'
        cluster.node(node_id, label=state, shape=shape)
    
    # Group and add transitions
    edge_labels: Dict[tuple, List[str]] = {}
    for source_state, trans_map in transitions.items():
        for symbol, dest_states in trans_map.items():
            dest_list = dest_states if isinstance(dest_states, list) else [dest_states]
            for dest_state in dest_list:
                key = (f'{prefix}{source_state}', f'{prefix}{dest_state}')
                edge_labels.setdefault(key, []).append(symbol)
    
    for (source, dest), symbols in edge_labels.items():
        cluster.edge(source, dest, label=', '.join(sorted(symbols)))


def create_nfa_graph(nfa_data: dict, title: str = "NFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of an NFA.
    
    Args:
        nfa_data: Dictionary containing NFA specification
        title: Title for the graph
    
    Returns:
        graphviz.Digraph object that can be rendered
    """
    graph = graphviz.Digraph(name=title, comment=title)
    graph.attr(rankdir='LR', node_shape='circle')
    _add_automaton_to_subgraph(graph, nfa_data)
    return graph


def create_dfa_graph(dfa_data: dict, title: str = "DFA") -> graphviz.Digraph:
    """Create a Graphviz directed graph representation of a DFA.
    
    Args:
        dfa_data: Dictionary containing DFA specification
        title: Title for the graph
    
    Returns:
        graphviz.Digraph object that can be rendered
    """
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
    """
    graph = create_nfa_graph(automaton_data, title)
    graph.format = format
    return graph.render(output_path, view=view, cleanup=True)


def get_graph_svg(automaton_data: dict, title: str = "Automaton") -> str:
    """Generate SVG string representation of an automaton graph.
    
    Args:
        automaton_data: NFA or DFA data dictionary
        title: Graph title
    
    Returns:
        SVG string that can be embedded in HTML
    """
    graph = create_nfa_graph(automaton_data, title)
    return graph.pipe(format='svg').decode('utf-8')


def compare_graphs(nfa_data: dict, dfa_data: dict) -> graphviz.Digraph:
    """Create a side-by-side comparison of NFA and DFA.
    
    Args:
        nfa_data: NFA data dictionary
        dfa_data: DFA data dictionary
    
    Returns:
        Combined graph showing both automata
    """
    main_graph = graphviz.Digraph(name='Comparison')
    main_graph.attr(rankdir='LR', label='NFA → DFA Conversion', fontsize='20')
    
    # NFA subgraph
    with main_graph.subgraph(name='cluster_nfa') as nfa_cluster:
        nfa_cluster.attr(label='NFA', fontsize='16', style='rounded', color='blue')
        _add_automaton_to_subgraph(nfa_cluster, nfa_data, prefix='nfa_')
    
    # DFA subgraph
    with main_graph.subgraph(name='cluster_dfa') as dfa_cluster:
        dfa_cluster.attr(label='DFA', fontsize='16', style='rounded', color='green')
        _add_automaton_to_subgraph(dfa_cluster, dfa_data, prefix='dfa_')
    
    return main_graph
