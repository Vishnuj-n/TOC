"""Graph visualization for NFAs and DFAs using Graphviz."""
from typing import Dict, List
import graphviz

def _add_automaton_to_subgraph(cluster: graphviz.Digraph, automaton_data: dict, prefix: str = "") -> None:
    """Add automaton states and transitions to subgraph."""
    states, start, finals = automaton_data["states"], automaton_data["start_state"], automaton_data["final_states"]
    transitions = automaton_data["transitions"]
    
    cluster.node(f'{prefix}start', shape='none', width='0', height='0')
    cluster.edge(f'{prefix}start', f'{prefix}{start}', label='start')
    
    for state in states:
        cluster.node(f'{prefix}{state}', label=state, shape='doublecircle' if state in finals else 'circle')
    
    edge_labels: Dict[tuple, List[str]] = {}
    for src, trans_map in transitions.items():
        for symbol, dests in trans_map.items():
            for dest in (dests if isinstance(dests, list) else [dests]):
                edge_labels.setdefault((f'{prefix}{src}', f'{prefix}{dest}'), []).append(symbol)
    
    for (src, dest), symbols in edge_labels.items():
        cluster.edge(src, dest, label=', '.join(sorted(symbols)))

def create_nfa_graph(nfa_data: dict, title: str = "NFA") -> graphviz.Digraph:
    """Create Graphviz directed graph of NFA/DFA."""
    graph = graphviz.Digraph(name=title, comment=title)
    graph.attr(rankdir='LR', node_shape='circle')
    _add_automaton_to_subgraph(graph, nfa_data)
    return graph

def create_dfa_graph(dfa_data: dict, title: str = "DFA") -> graphviz.Digraph:
    """Create Graphviz directed graph of DFA."""
    return create_nfa_graph(dfa_data, title)

def render_automaton_graph(automaton_data: dict, output_path: str, format: str = 'png', 
                          title: str = "Automaton", view: bool = False) -> str:
    """Render automaton graph to file."""
    graph = create_nfa_graph(automaton_data, title)
    graph.format = format
    return graph.render(output_path, view=view, cleanup=True)

def get_graph_svg(automaton_data: dict, title: str = "Automaton") -> str:
    """Generate SVG string of automaton graph."""
    return create_nfa_graph(automaton_data, title).pipe(format='svg').decode('utf-8')

def compare_graphs(nfa_data: dict, dfa_data: dict) -> graphviz.Digraph:
    """Create side-by-side comparison of NFA and DFA."""
    main = graphviz.Digraph(name='Comparison')
    main.attr(rankdir='LR', label='NFA → DFA Conversion', fontsize='20')
    
    with main.subgraph(name='cluster_nfa') as nfa:
        nfa.attr(label='NFA', fontsize='16', style='rounded', color='blue')
        _add_automaton_to_subgraph(nfa, nfa_data, prefix='nfa_')
    
    with main.subgraph(name='cluster_dfa') as dfa:
        dfa.attr(label='DFA', fontsize='16', style='rounded', color='green')
        _add_automaton_to_subgraph(dfa, dfa_data, prefix='dfa_')
    
    return main
