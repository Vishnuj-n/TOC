"""NFA to DFA conversion using subset construction algorithm.

This module provides the core conversion logic that is independent of any UI framework.
"""

from typing import Dict, List, Tuple, Set, FrozenSet


def convert_nfa_to_dfa(nfa_data: dict) -> Tuple[dict, List[str]]:
    """Convert an NFA to a DFA using the subset construction algorithm.
    
    Args:
        nfa_data: Dictionary containing NFA specification with keys:
            - states: list[str] - List of state names
            - alphabet: list[str] - Input alphabet symbols
            - start_state: str - Initial state
            - final_states: list[str] - Accepting states
            - transitions: dict[str, dict[str, list[str]]] - Transition function
    
    Returns:
        Tuple containing:
            - dfa_data: Dictionary with same structure as NFA but with deterministic transitions
            - log_lines: List of strings describing each step of the conversion
    
    Raises:
        ValueError: If NFA data is invalid or malformed
    
    Example:
        >>> nfa = {
        ...     "states": ["q0", "q1"],
        ...     "alphabet": ["a", "b"],
        ...     "start_state": "q0",
        ...     "final_states": ["q1"],
        ...     "transitions": {
        ...         "q0": {"a": ["q0", "q1"]},
        ...         "q1": {"b": ["q1"]}
        ...     }
        ... }
        >>> dfa, logs = convert_nfa_to_dfa(nfa)
    """
    logs: List[str] = []
    
    # Validate input
    try:
        states = nfa_data["states"]
        alphabet = nfa_data["alphabet"]
        start_state = nfa_data["start_state"]
        final_states = nfa_data["final_states"]
        transitions = nfa_data["transitions"]
    except KeyError as e:
        raise ValueError(f"Invalid NFA data: missing key {e}")
    
    logs.append("=" * 60)
    logs.append("NFA TO DFA CONVERSION - SUBSET CONSTRUCTION ALGORITHM")
    logs.append("=" * 60)
    logs.append("")
    logs.append(f"Input NFA has {len(states)} states: {states}")
    logs.append(f"Alphabet: {alphabet}")
    logs.append(f"Start state: {start_state}")
    logs.append(f"Final states: {final_states}")
    logs.append("")
    
    # DFA state tracking
    # Each DFA state is a frozenset of NFA states
    dfa_states: Dict[FrozenSet[str], str] = {}
    dfa_transitions: Dict[str, Dict[str, str]] = {}
    dfa_final_states: List[str] = []
    
    # Queue of DFA states to process
    queue: List[FrozenSet[str]] = []
    
    # Helper function to get or create DFA state name
    def get_dfa_state_name(nfa_state_set: FrozenSet[str]) -> str:
        """Convert a set of NFA states to a DFA state name."""
        if not nfa_state_set:
            return "∅"  # Empty set (dead state)
        
        if nfa_state_set not in dfa_states:
            # Create new DFA state name
            sorted_states = sorted(nfa_state_set)
            dfa_state_name = "{" + ",".join(sorted_states) + "}"
            dfa_states[nfa_state_set] = dfa_state_name
            logs.append(f"  → Created new DFA state: {dfa_state_name}")
        
        return dfa_states[nfa_state_set]
    
    # Helper function to compute transition from a set of NFA states
    def compute_transition(nfa_state_set: FrozenSet[str], symbol: str) -> FrozenSet[str]:
        """Compute the set of NFA states reachable from a set via a symbol."""
        result_states: Set[str] = set()
        
        for nfa_state in nfa_state_set:
            if nfa_state in transitions and symbol in transitions[nfa_state]:
                result_states.update(transitions[nfa_state][symbol])
        
        return frozenset(result_states)
    
    # Initialize with start state
    initial_set = frozenset([start_state])
    queue.append(initial_set)
    initial_dfa_state = get_dfa_state_name(initial_set)
    
    logs.append("STEP 1: Initialize DFA")
    logs.append(f"  Initial DFA state: {initial_dfa_state} (from NFA state {start_state})")
    logs.append("")
    
    step_counter = 2
    
    # Process queue
    while queue:
        current_nfa_set = queue.pop(0)
        current_dfa_state = get_dfa_state_name(current_nfa_set)
        
        logs.append(f"STEP {step_counter}: Processing DFA state {current_dfa_state}")
        logs.append(f"  (represents NFA states: {sorted(current_nfa_set)})")
        
        # Initialize transitions for this DFA state
        if current_dfa_state not in dfa_transitions:
            dfa_transitions[current_dfa_state] = {}
        
        # For each symbol in alphabet
        for symbol in alphabet:
            next_nfa_set = compute_transition(current_nfa_set, symbol)
            next_dfa_state = get_dfa_state_name(next_nfa_set)
            
            # Record transition
            dfa_transitions[current_dfa_state][symbol] = next_dfa_state
            
            logs.append(f"  On input '{symbol}': {current_dfa_state} → {next_dfa_state}")
            
            # Add to queue if new state
            if next_nfa_set and next_nfa_set not in dfa_states:
                queue.append(next_nfa_set)
                logs.append(f"    (New state discovered, added to queue)")
        
        logs.append("")
        step_counter += 1
    
    # Determine final states
    logs.append(f"STEP {step_counter}: Determine final states")
    logs.append(f"  NFA final states: {final_states}")
    
    for nfa_state_set, dfa_state_name in dfa_states.items():
        # A DFA state is final if it contains any NFA final state
        if any(nfa_final in nfa_state_set for nfa_final in final_states):
            dfa_final_states.append(dfa_state_name)
            logs.append(f"  {dfa_state_name} is final (contains {[s for s in nfa_state_set if s in final_states]})")
    
    logs.append("")
    logs.append("=" * 60)
    logs.append("CONVERSION COMPLETE")
    logs.append("=" * 60)
    logs.append(f"DFA has {len(dfa_states)} states: {list(dfa_states.values())}")
    logs.append(f"DFA final states: {dfa_final_states}")
    logs.append("")
    
    # Build DFA output
    dfa_data = {
        "states": list(dfa_states.values()),
        "alphabet": alphabet,
        "start_state": get_dfa_state_name(frozenset([start_state])),
        "final_states": dfa_final_states,
        "transitions": dfa_transitions
    }
    
    return dfa_data, logs


def validate_nfa(nfa_data: dict) -> Tuple[bool, str]:
    """Validate NFA data structure.
    
    Args:
        nfa_data: Dictionary containing NFA specification
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_keys = ["states", "alphabet", "start_state", "final_states", "transitions"]
    
    # Check required keys
    for key in required_keys:
        if key not in nfa_data:
            return False, f"Missing required key: {key}"
    
    states = nfa_data["states"]
    alphabet = nfa_data["alphabet"]
    start_state = nfa_data["start_state"]
    final_states = nfa_data["final_states"]
    transitions = nfa_data["transitions"]
    
    # Validate types
    if not isinstance(states, list):
        return False, "'states' must be a list"
    
    if not isinstance(alphabet, list):
        return False, "'alphabet' must be a list"
    
    if not isinstance(start_state, str):
        return False, "'start_state' must be a string"
    
    if not isinstance(final_states, list):
        return False, "'final_states' must be a list"
    
    if not isinstance(transitions, dict):
        return False, "'transitions' must be a dictionary"
    
    # Validate start state
    if start_state not in states:
        return False, f"Start state '{start_state}' not in states list"
    
    # Validate final states
    for final_state in final_states:
        if final_state not in states:
            return False, f"Final state '{final_state}' not in states list"
    
    # Validate transitions
    for state, trans_dict in transitions.items():
        if state not in states:
            return False, f"Transition source state '{state}' not in states list"
        
        if not isinstance(trans_dict, dict):
            return False, f"Transitions for state '{state}' must be a dictionary"
        
        for symbol, dest_states in trans_dict.items():
            if symbol not in alphabet:
                return False, f"Transition symbol '{symbol}' not in alphabet"
            
            if not isinstance(dest_states, list):
                return False, f"Destination states for '{state}' on '{symbol}' must be a list"
            
            for dest_state in dest_states:
                if dest_state not in states:
                    return False, f"Destination state '{dest_state}' not in states list"
    
    return True, "Valid NFA"
