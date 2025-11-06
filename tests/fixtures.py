"""Test fixtures and sample NFA data."""

# Sample NFA that accepts strings ending in 'ab'
SAMPLE_NFA_1 = {
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
            "a": ["q0", "q1"],
            "b": ["q0"]
        }
    }
}

# Simple NFA with 2 states
SAMPLE_NFA_2 = {
    "states": ["q0", "q1"],
    "alphabet": ["0", "1"],
    "start_state": "q0",
    "final_states": ["q1"],
    "transitions": {
        "q0": {
            "0": ["q0"],
            "1": ["q0", "q1"]
        },
        "q1": {
            "0": ["q1"],
            "1": ["q1"]
        }
    }
}

# NFA that accepts even number of 'a's
SAMPLE_NFA_3 = {
    "states": ["even", "odd"],
    "alphabet": ["a", "b"],
    "start_state": "even",
    "final_states": ["even"],
    "transitions": {
        "even": {
            "a": ["odd"],
            "b": ["even"]
        },
        "odd": {
            "a": ["even"],
            "b": ["odd"]
        }
    }
}
