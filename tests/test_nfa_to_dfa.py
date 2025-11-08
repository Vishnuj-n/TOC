"""Unit tests for NFA to DFA conversion algorithm."""

import pytest
import json
import os
from pathlib import Path
from nfa_to_dfa import convert_nfa_to_dfa, validate_nfa


def test_simple_nfa_conversion():
    """Test basic NFA to DFA conversion."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a", "b"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {"a": ["q0", "q1"]},
            "q1": {"b": ["q1"]}
        }
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    assert dfa is not None
    assert len(logs) > 0
    assert "states" in dfa
    assert "alphabet" in dfa
    assert "start_state" in dfa
    assert "final_states" in dfa
    assert "transitions" in dfa


def test_nfa_with_multiple_transitions():
    """Test NFA where a state has multiple transitions on same symbol."""
    nfa = {
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
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # DFA should have deterministic transitions
    for state, transitions in dfa["transitions"].items():
        for symbol, dest in transitions.items():
            assert isinstance(dest, str), "DFA transitions should map to single states"


def test_nfa_validation_valid():
    """Test validation of a valid NFA."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {"a": ["q1"]}
        }
    }
    
    is_valid, msg = validate_nfa(nfa)
    assert is_valid is True


def test_nfa_validation_missing_key():
    """Test validation fails on missing keys."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"]
        # Missing start_state, final_states, transitions
    }
    
    is_valid, msg = validate_nfa(nfa)
    assert is_valid is False
    assert "Missing required key" in msg


def test_nfa_validation_invalid_start_state():
    """Test validation fails when start state not in states list."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"],
        "start_state": "q99",  # Not in states
        "final_states": ["q1"],
        "transitions": {}
    }
    
    is_valid, msg = validate_nfa(nfa)
    assert is_valid is False
    assert "Start state" in msg


def test_nfa_validation_invalid_final_state():
    """Test validation fails when final state not in states list."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q99"],  # Not in states
        "transitions": {}
    }
    
    is_valid, msg = validate_nfa(nfa)
    assert is_valid is False
    assert "Final state" in msg


def test_nfa_validation_invalid_transition_symbol():
    """Test validation fails when transition uses symbol not in alphabet."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {"b": ["q1"]}  # 'b' not in alphabet
        }
    }
    
    is_valid, msg = validate_nfa(nfa)
    assert is_valid is False
    assert "not in alphabet" in msg


def test_nfa_with_no_transitions():
    """Test NFA with states but no transitions."""
    nfa = {
        "states": ["q0"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q0"],
        "transitions": {}
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    assert len(dfa["states"]) >= 1


def test_nfa_state_explosion():
    """Test NFA that causes state explosion in DFA."""
    # NFA with 3 states can produce up to 2^3 = 8 DFA states
    nfa = {
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
                "a": ["q1", "q2"],
                "b": ["q1"]
            },
            "q2": {
                "a": ["q2"],
                "b": ["q2"]
            }
        }
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # DFA should be created successfully (number of states may vary)
    assert len(dfa["states"]) > 0
    assert "transitions" in dfa


def test_dfa_final_states_correct():
    """Test that DFA final states are correctly determined."""
    nfa = {
        "states": ["q0", "q1", "q2"],
        "alphabet": ["a"],
        "start_state": "q0",
        "final_states": ["q2"],
        "transitions": {
            "q0": {"a": ["q1", "q2"]},
            "q1": {"a": ["q1"]},
            "q2": {"a": ["q2"]}
        }
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # At least one DFA state should be final
    assert len(dfa["final_states"]) > 0


def test_nfa_alphabet_preserved():
    """Test that alphabet is preserved in DFA."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a", "b", "c"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {"a": ["q1"]},
            "q1": {"b": ["q1"]}
        }
    }
    
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    assert dfa["alphabet"] == nfa["alphabet"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# ============================================================================
# CORRECTNESS TESTS - Verify DFA accepts same language as NFA
# ============================================================================

def simulate_nfa(nfa: dict, input_string: str) -> bool:
    """Simulate NFA execution on an input string.
    
    Args:
        nfa: NFA specification dictionary
        input_string: String to test
    
    Returns:
        True if string is accepted, False otherwise
    """
    current_states = {nfa["start_state"]}
    
    for symbol in input_string:
        if symbol not in nfa["alphabet"]:
            return False  # Invalid symbol
        
        next_states = set()
        for state in current_states:
            if state in nfa["transitions"] and symbol in nfa["transitions"][state]:
                next_states.update(nfa["transitions"][state][symbol])
        
        current_states = next_states
        
        if not current_states:  # No valid transitions
            return False
    
    # Accept if any current state is a final state
    return any(state in nfa["final_states"] for state in current_states)


def simulate_dfa(dfa: dict, input_string: str) -> bool:
    """Simulate DFA execution on an input string.
    
    Args:
        dfa: DFA specification dictionary
        input_string: String to test
    
    Returns:
        True if string is accepted, False otherwise
    """
    current_state = dfa["start_state"]
    
    for symbol in input_string:
        if symbol not in dfa["alphabet"]:
            return False  # Invalid symbol
        
        if current_state not in dfa["transitions"]:
            return False  # No transitions from this state
        
        if symbol not in dfa["transitions"][current_state]:
            return False  # No transition for this symbol
        
        current_state = dfa["transitions"][current_state][symbol]
    
    return current_state in dfa["final_states"]


def test_nfa_dfa_equivalence_simple():
    """Test that converted DFA accepts same language as original NFA."""
    nfa = {
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
    
    dfa, _ = convert_nfa_to_dfa(nfa)
    
    # Test strings that should be ACCEPTED (contain at least one 'a' followed by 'b')
    accept_strings = ["ab", "aab", "bab", "aaab", "aabb", "baaabbb", "ababab"]
    
    for test_string in accept_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is True, f"DFA should accept '{test_string}'"
    
    # Test strings that should be REJECTED
    reject_strings = ["", "a", "b", "aa", "bb", "aaa", "bbb", "ba"]
    
    for test_string in reject_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is False, f"DFA should reject '{test_string}'"


def test_example_nfa_1_correctness():
    """Test conversion correctness using sample_nfa_1.json from examples directory.
    
    This NFA accepts strings that END with the pattern 'ab' (at least one 'a' followed by exactly one 'b' at the end).
    """
    # Load example file
    examples_dir = Path(__file__).parent.parent / "examples"
    with open(examples_dir / "sample_nfa_1.json", "r") as f:
        nfa = json.load(f)
    
    # Convert to DFA
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # Strings that should be ACCEPTED (end with 'ab')
    accept_strings = [
        "ab",           # Minimal: ends with 'ab'
        "aab",          # Two 'a's before 'b'
        "bab",          # 'b' then 'ab'
        "baab",         # Multiple 'b's before 'ab'
        "aaab",         # Multiple 'a's before 'b'
        "bbab",         # Multiple 'b's then 'ab'
        "ababab",       # Pattern that ends with 'ab'
        "baaab",        # Complex, ends with 'ab'
    ]
    
    for test_string in accept_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is True, f"Should accept '{test_string}' (ends with 'ab')"
    
    # Strings that should be REJECTED (don't end with 'ab')
    reject_strings = [
        "",             # Empty string
        "a",            # Doesn't end with 'ab'
        "b",            # Only 'b'
        "aa",           # Ends with 'a', not 'ab'
        "bb",           # Ends with 'b', not 'ab'
        "abb",          # Ends with 'bb', not 'ab'
        "aba",          # Ends with 'a', not 'ab'
        "abab" + "a",   # Ends with 'a'
        "ba",           # Ends with 'a'
    ]
    
    for test_string in reject_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is False, f"Should reject '{test_string}' (doesn't end with 'ab')"


def test_example_nfa_2_correctness():
    """Test conversion correctness using sample_nfa_2.json from examples directory.
    
    This NFA accepts strings that contain at least one '1'.
    """
    # Load example file
    examples_dir = Path(__file__).parent.parent / "examples"
    with open(examples_dir / "sample_nfa_2.json", "r") as f:
        nfa = json.load(f)
    
    # Convert to DFA
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # Strings that should be ACCEPTED (contain at least one '1')
    accept_strings = [
        "1",            # Single '1'
        "01",           # Ends with '1'
        "10",           # Starts with '1'
        "11",           # Multiple '1's
        "001",          # '1' at end
        "100",          # '1' at start
        "0101",         # Multiple '1's
        "111",          # All '1's
        "01010101",     # Many '1's
    ]
    
    for test_string in accept_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is True, f"Should accept '{test_string}' (contains '1')"
    
    # Strings that should be REJECTED (no '1')
    reject_strings = [
        "",             # Empty string
        "0",            # Single '0'
        "00",           # Multiple '0's
        "000",          # More '0's
        "0000000",      # Many '0's
    ]
    
    for test_string in reject_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is False, f"Should reject '{test_string}' (no '1')"


def test_example_nfa_3_correctness():
    """Test conversion correctness using sample_nfa_3.json from examples directory.
    
    This NFA (actually a DFA) accepts strings with an even number of 'a's.
    """
    # Load example file
    examples_dir = Path(__file__).parent.parent / "examples"
    with open(examples_dir / "sample_nfa_3.json", "r") as f:
        nfa = json.load(f)
    
    # Convert to DFA (note: input is already deterministic)
    dfa, logs = convert_nfa_to_dfa(nfa)
    
    # Strings that should be ACCEPTED (even number of 'a's: 0, 2, 4, ...)
    accept_strings = [
        "",             # 0 'a's (even)
        "b",            # 0 'a's
        "bb",           # 0 'a's
        "aa",           # 2 'a's
        "aabb",         # 2 'a's
        "baa",          # 2 'a's
        "aab",          # 2 'a's
        "aaaa",         # 4 'a's
        "baabaab",      # 4 'a's
        "aaaaaa",       # 6 'a's
    ]
    
    for test_string in accept_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        num_a = test_string.count('a')
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is True, f"Should accept '{test_string}' ({num_a} 'a's - even)"
    
    # Strings that should be REJECTED (odd number of 'a's: 1, 3, 5, ...)
    reject_strings = [
        "a",            # 1 'a'
        "ab",           # 1 'a'
        "ba",           # 1 'a'
        "aaa",          # 3 'a's
        "baaa",         # 3 'a's
        "aaab",         # 3 'a's
        "aaaaa",        # 5 'a's
        "baaabaa",      # 5 'a's
    ]
    
    for test_string in reject_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        num_a = test_string.count('a')
        assert nfa_result == dfa_result, f"Mismatch for '{test_string}': NFA={nfa_result}, DFA={dfa_result}"
        assert dfa_result is False, f"Should reject '{test_string}' ({num_a} 'a's - odd)"


def test_comprehensive_string_testing():
    """Comprehensive test: generate many strings and verify NFA/DFA equivalence."""
    nfa = {
        "states": ["q0", "q1"],
        "alphabet": ["a", "b"],
        "start_state": "q0",
        "final_states": ["q1"],
        "transitions": {
            "q0": {
                "a": ["q1"],
                "b": ["q0"]
            },
            "q1": {
                "a": ["q1"],
                "b": ["q1"]
            }
        }
    }
    
    dfa, _ = convert_nfa_to_dfa(nfa)
    
    # Generate all strings up to length 4 (2^4 = 16 strings per length)
    test_strings = [""]  # Empty string
    
    for length in range(1, 5):
        # Generate all combinations of 'a' and 'b' of given length
        from itertools import product
        for combo in product(['a', 'b'], repeat=length):
            test_strings.append(''.join(combo))
    
    # Test all strings
    mismatches = []
    for test_string in test_strings:
        nfa_result = simulate_nfa(nfa, test_string)
        dfa_result = simulate_dfa(dfa, test_string)
        
        if nfa_result != dfa_result:
            mismatches.append((test_string, nfa_result, dfa_result))
    
    assert len(mismatches) == 0, f"Found {len(mismatches)} mismatches: {mismatches}"


def test_dfa_completeness():
    """Test that converted DFA has transitions for all states and symbols."""
    nfa = {
        "states": ["q0", "q1", "q2"],
        "alphabet": ["a", "b"],
        "start_state": "q0",
        "final_states": ["q2"],
        "transitions": {
            "q0": {"a": ["q0", "q1"], "b": ["q0"]},
            "q1": {"b": ["q2"]},
            "q2": {"a": ["q2"], "b": ["q2"]}
        }
    }
    
    dfa, _ = convert_nfa_to_dfa(nfa)
    
    # Every DFA state should have a transition for every alphabet symbol
    for state in dfa["states"]:
        assert state in dfa["transitions"], f"State {state} has no transitions"
        for symbol in dfa["alphabet"]:
            assert symbol in dfa["transitions"][state], \
                f"State {state} missing transition for symbol '{symbol}'"
            # Transition should lead to exactly one state (deterministic)
            dest = dfa["transitions"][state][symbol]
            assert isinstance(dest, str), f"Transition should be to single state, got {dest}"
            assert dest in dfa["states"], f"Transition leads to invalid state {dest}"
