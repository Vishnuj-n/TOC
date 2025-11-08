"""NFA to DFA conversion using subset construction algorithm."""

from typing import Dict, List, Tuple, Set, FrozenSet


def convert_nfa_to_dfa(nfa_data: dict) -> Tuple[dict, List[str]]:
    """Convert an NFA to a DFA using the subset construction algorithm.
    
    Args:
        nfa_data: Dictionary with NFA specification (states, alphabet, start_state, 
                  final_states, transitions)
    
    Returns:
        Tuple of (dfa_data dict, log_lines list)
    
    Raises:
        ValueError: If NFA data is invalid
    """
    logs: List[str] = []
    
    # Extract and validate input
    try:
        states, alphabet = nfa_data["states"], nfa_data["alphabet"]
        start_state, final_states = nfa_data["start_state"], nfa_data["final_states"]
        transitions = nfa_data["transitions"]
    except KeyError as e:
        raise ValueError(f"Invalid NFA data: missing key {e}")
    
    # Log header
    logs.extend([
        "=" * 60,
        "NFA TO DFA CONVERSION - SUBSET CONSTRUCTION ALGORITHM",
        "=" * 60,
        "",
        f"Input NFA has {len(states)} states: {states}",
        f"Alphabet: {alphabet}",
        f"Start state: {start_state}",
        f"Final states: {final_states}",
        ""
    ])
    
    # DFA state tracking
    dfa_states: Dict[FrozenSet[str], str] = {}
    dfa_transitions: Dict[str, Dict[str, str]] = {}
    dfa_final_states: List[str] = []
    queue: List[FrozenSet[str]] = []
    
    def get_dfa_state_name(nfa_state_set: FrozenSet[str]) -> str:
        """Get or create the canonical name for a DFA state."""
        if nfa_state_set in dfa_states:
            return dfa_states[nfa_state_set]
        
        if not nfa_state_set:
            dfa_state_name = "∅"
        else:
            dfa_state_name = "{" + ",".join(sorted(nfa_state_set)) + "}"
        
        dfa_states[nfa_state_set] = dfa_state_name
        logs.append(f"  → Created new DFA state: {dfa_state_name}")
        return dfa_state_name
    
    def compute_transition(nfa_state_set: FrozenSet[str], symbol: str) -> FrozenSet[str]:
        """Compute the set of NFA states reachable from a set via a symbol."""
        result_states = set()
        for nfa_state in nfa_state_set:
            if nfa_state in transitions and symbol in transitions[nfa_state]:
                result_states.update(transitions[nfa_state][symbol])
        return frozenset(result_states)
    
    # Initialize with start state
    initial_set = frozenset([start_state])
    queue.append(initial_set)
    initial_dfa_state = get_dfa_state_name(initial_set)
    
    logs.extend([
        "STEP 1: Initialize DFA",
        f"  Initial DFA state: {initial_dfa_state} (from NFA state {start_state})",
        ""
    ])
    
    step_counter = 2
    
    # Process queue
    while queue:
        current_nfa_set = queue.pop(0)
        current_dfa_state = get_dfa_state_name(current_nfa_set)
        
        logs.extend([
            f"STEP {step_counter}: Processing DFA state {current_dfa_state}",
            f"  (represents NFA states: {sorted(current_nfa_set)})"
        ])
        
        dfa_transitions.setdefault(current_dfa_state, {})
        
        for symbol in alphabet:
            next_nfa_set = compute_transition(current_nfa_set, symbol)
            
            # Check if this is a new state BEFORE creating it in dfa_states
            is_new_state = next_nfa_set not in dfa_states
            
            next_dfa_state = get_dfa_state_name(next_nfa_set)
            dfa_transitions[current_dfa_state][symbol] = next_dfa_state
            
            logs.append(f"  On input '{symbol}': {current_dfa_state} → {next_dfa_state}")
            
            if is_new_state:
                queue.append(next_nfa_set)
                logs.append(f"    (New state discovered, added to queue)")
        
        logs.append("")
        step_counter += 1
    
    # Determine final states
    logs.extend([
        f"STEP {step_counter}: Determine final states",
        f"  NFA final states: {final_states}"
    ])
    
    for nfa_state_set, dfa_state_name in dfa_states.items():
        if any(nfa_final in nfa_state_set for nfa_final in final_states):
            dfa_final_states.append(dfa_state_name)
            logs.append(f"  {dfa_state_name} is final (contains {[s for s in nfa_state_set if s in final_states]})")
    
    logs.extend([
        "",
        "=" * 60,
        "CONVERSION COMPLETE",
        "=" * 60,
        f"DFA has {len(dfa_states)} states: {list(dfa_states.values())}",
        f"DFA final states: {dfa_final_states}",
        ""
    ])
    
    return {
        "states": list(dfa_states.values()),
        "alphabet": alphabet,
        "start_state": get_dfa_state_name(frozenset([start_state])),
        "final_states": dfa_final_states,
        "transitions": dfa_transitions
    }, logs


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
    
    states, alphabet = nfa_data["states"], nfa_data["alphabet"]
    start_state, final_states = nfa_data["start_state"], nfa_data["final_states"]
    transitions = nfa_data["transitions"]
    
    # Validate types
    type_checks = [
        (states, list, "'states' must be a list"),
        (alphabet, list, "'alphabet' must be a list"),
        (start_state, str, "'start_state' must be a string"),
        (final_states, list, "'final_states' must be a list"),
        (transitions, dict, "'transitions' must be a dictionary")
    ]
    
    for value, expected_type, error_msg in type_checks:
        if not isinstance(value, expected_type):
            return False, error_msg
    
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
