"""Unit tests for NFA to DFA conversion algorithm."""

import pytest
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
