"""NFA to DFA conversion using subset construction algorithm."""
from typing import Dict, List, Tuple, Set, FrozenSet

def convert_nfa_to_dfa(nfa_data: dict) -> Tuple[dict, List[str]]:
    """Convert NFA to DFA using subset construction.
    Args: nfa_data dict with states, alphabet, start_state, final_states, transitions
    Returns: Tuple of (dfa_data dict, log_lines list)
    """
    logs = []
    try:
        states, alphabet = nfa_data["states"], nfa_data["alphabet"]
        start_state, final_states = nfa_data["start_state"], nfa_data["final_states"]
        transitions = nfa_data["transitions"]
    except KeyError as e:
        raise ValueError(f"Invalid NFA data: missing key {e}")
    
    logs.extend(["=" * 60, "NFA TO DFA CONVERSION - SUBSET CONSTRUCTION ALGORITHM", "=" * 60, "",
                 f"Input NFA: {len(states)} states {states}, Alphabet: {alphabet}",
                 f"Start: {start_state}, Final: {final_states}", ""])
    
    dfa_states, dfa_transitions, dfa_final_states, queue = {}, {}, [], []
    
    def get_dfa_state_name(nfa_set: FrozenSet[str]) -> str:
        if nfa_set in dfa_states:
            return dfa_states[nfa_set]
        dfa_name = "∅" if not nfa_set else "{" + ",".join(sorted(nfa_set)) + "}"
        dfa_states[nfa_set] = dfa_name
        logs.append(f"  → Created DFA state: {dfa_name}")
        return dfa_name
    
    def compute_transition(nfa_set: FrozenSet[str], symbol: str) -> FrozenSet[str]:
        result = set()
        for state in nfa_set:
            if state in transitions and symbol in transitions[state]:
                result.update(transitions[state][symbol])
        return frozenset(result)
    
    initial_set = frozenset([start_state])
    queue.append(initial_set)
    initial_dfa = get_dfa_state_name(initial_set)
    logs.extend(["STEP 1: Initialize DFA", f"  Initial DFA state: {initial_dfa}", ""])
    
    step = 2
    while queue:
        current_nfa_set = queue.pop(0)
        current_dfa = get_dfa_state_name(current_nfa_set)
        logs.extend([f"STEP {step}: Processing {current_dfa}", f"  (NFA states: {sorted(current_nfa_set)})"])
        dfa_transitions.setdefault(current_dfa, {})
        
        for symbol in alphabet:
            next_nfa_set = compute_transition(current_nfa_set, symbol)
            is_new = next_nfa_set not in dfa_states
            next_dfa = get_dfa_state_name(next_nfa_set)
            dfa_transitions[current_dfa][symbol] = next_dfa
            logs.append(f"  On '{symbol}': {current_dfa} → {next_dfa}")
            if is_new:
                queue.append(next_nfa_set)
                logs.append(f"    (New state, queued)")
        logs.append("")
        step += 1
    
    logs.extend([f"STEP {step}: Determine final states", f"  NFA final: {final_states}"])
    for nfa_set, dfa_name in dfa_states.items():
        if any(f in nfa_set for f in final_states):
            dfa_final_states.append(dfa_name)
            logs.append(f"  {dfa_name} is final (contains {[s for s in nfa_set if s in final_states]})")
    
    logs.extend(["", "=" * 60, "CONVERSION COMPLETE", "=" * 60,
                 f"DFA: {len(dfa_states)} states {list(dfa_states.values())}",
                 f"DFA final states: {dfa_final_states}", ""])
    
    return {"states": list(dfa_states.values()), "alphabet": alphabet,
            "start_state": get_dfa_state_name(frozenset([start_state])),
            "final_states": dfa_final_states, "transitions": dfa_transitions}, logs


def validate_nfa(nfa_data: dict) -> Tuple[bool, str]:
    """Validate NFA data structure.
    Args: nfa_data dict
    Returns: Tuple of (is_valid, error_message)
    """
    required = ["states", "alphabet", "start_state", "final_states", "transitions"]
    for key in required:
        if key not in nfa_data:
            return False, f"Missing required key: {key}"
    
    states, alphabet = nfa_data["states"], nfa_data["alphabet"]
    start, finals, trans = nfa_data["start_state"], nfa_data["final_states"], nfa_data["transitions"]
    
    checks = [(states, list, "'states' must be a list"),
              (alphabet, list, "'alphabet' must be a list"),
              (start, str, "'start_state' must be a string"),
              (finals, list, "'final_states' must be a list"),
              (trans, dict, "'transitions' must be a dictionary")]
    
    for value, expected, msg in checks:
        if not isinstance(value, expected):
            return False, msg
    
    if start not in states:
        return False, f"Start state '{start}' not in states list"
    
    for f in finals:
        if f not in states:
            return False, f"Final state '{f}' not in states list"
    
    for state, trans_dict in trans.items():
        if state not in states:
            return False, f"Transition source '{state}' not in states list"
        if not isinstance(trans_dict, dict):
            return False, f"Transitions for '{state}' must be a dictionary"
        
        for symbol, dests in trans_dict.items():
            if symbol not in alphabet:
                return False, f"Symbol '{symbol}' not in alphabet"
            if not isinstance(dests, list):
                return False, f"Destinations for '{state}' on '{symbol}' must be a list"
            for dest in dests:
                if dest not in states:
                    return False, f"Destination '{dest}' not in states list"
    
    return True, "Valid NFA"
