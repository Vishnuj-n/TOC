# NFA/DFA JSON Format Specification

## Overview

This document provides the complete technical specification for the JSON format used to represent Non-deterministic Finite Automata (NFAs) and Deterministic Finite Automata (DFAs) in the Automaton Visualizer application.

---

## JSON Schema

### Root Object Structure

```typescript
{
  "states": string[],           // Array of state identifiers
  "alphabet": string[],         // Array of input symbols
  "start_state": string,        // Single start state identifier
  "final_states": string[],     // Array of accepting state identifiers
  "transitions": {              // Transition function
    [state: string]: {
      [symbol: string]: string[] | string
    }
  }
}
```

---

## Field Specifications

### 1. `states` (Required)

**Type:** `Array<string>`

**Description:** Complete list of all states in the automaton.

**Constraints:**
- Must be non-empty array
- Each state identifier must be unique
- State identifiers are case-sensitive
- Recommended naming: `"q0"`, `"q1"`, `"q2"`, etc.

**Examples:**
```json
"states": ["q0", "q1", "q2"]
"states": ["start", "middle", "end"]
"states": ["s0", "s1", "s2", "s3"]
```

**Validation Rules:**
```python
assert isinstance(states, list)
assert len(states) > 0
assert len(states) == len(set(states))  # No duplicates
```

---

### 2. `alphabet` (Required)

**Type:** `Array<string>`

**Description:** Complete set of input symbols that the automaton can process.

**Constraints:**
- Must be non-empty array
- Each symbol must be unique
- Symbols are typically single characters but can be strings
- Common symbols: `"a"`, `"b"`, `"0"`, `"1"`

**Examples:**
```json
"alphabet": ["a", "b"]
"alphabet": ["0", "1"]
"alphabet": ["x", "y", "z"]
"alphabet": ["read", "write", "delete"]  // Multi-character symbols allowed
```

**Validation Rules:**
```python
assert isinstance(alphabet, list)
assert len(alphabet) > 0
assert len(alphabet) == len(set(alphabet))  # No duplicates
```

---

### 3. `start_state` (Required)

**Type:** `string`

**Description:** The initial state where the automaton begins processing.

**Constraints:**
- Must be a single state identifier
- Must exist in the `states` array
- Every automaton has exactly one start state

**Examples:**
```json
"start_state": "q0"
"start_state": "start"
"start_state": "initial"
```

**Validation Rules:**
```python
assert isinstance(start_state, str)
assert start_state in states
```

---

### 4. `final_states` (Required)

**Type:** `Array<string>`

**Description:** Set of accepting/final states. If the automaton ends in any of these states, the input is accepted.

**Constraints:**
- Can be empty array (no accepting states)
- Each state must exist in the `states` array
- Multiple final states are allowed
- Duplicates should be avoided

**Examples:**
```json
"final_states": ["q2"]
"final_states": ["accept1", "accept2"]
"final_states": []  // No accepting states (rejects all input)
```

**Validation Rules:**
```python
assert isinstance(final_states, list)
for state in final_states:
    assert state in states
```

---

### 5. `transitions` (Required)

**Type:** `Object<string, Object<string, Array<string> | string>>`

**Description:** The transition function defining how the automaton moves between states.

#### Structure

```json
"transitions": {
  "source_state": {
    "input_symbol": ["dest_state1", "dest_state2"]  // NFA: multiple destinations
  }
}
```

or for DFA:

```json
"transitions": {
  "source_state": {
    "input_symbol": "dest_state"  // DFA: single destination
  }
}
```

**Constraints:**
- Source states must exist in `states` array
- Input symbols must exist in `alphabet` array
- Destination states must exist in `states` array
- **NFA:** Destinations are arrays (can have 0, 1, or more states)
- **DFA:** Destinations are single strings (exactly 1 state per symbol)

**NFA Example:**
```json
"transitions": {
  "q0": {
    "a": ["q0", "q1"],  // Non-deterministic: 'a' goes to both q0 and q1
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
```

**DFA Example:**
```json
"transitions": {
  "q0": {
    "a": "q1",  // Deterministic: 'a' goes to exactly q1
    "b": "q0"
  },
  "q1": {
    "a": "q1",
    "b": "q2"
  },
  "q2": {
    "a": "q1",
    "b": "q0"
  }
}
```

**Validation Rules:**
```python
assert isinstance(transitions, dict)
for source_state, trans_map in transitions.items():
    assert source_state in states
    assert isinstance(trans_map, dict)
    for symbol, dest in trans_map.items():
        assert symbol in alphabet
        if isinstance(dest, list):  # NFA
            for d in dest:
                assert d in states
        else:  # DFA
            assert dest in states
```

---

## NFA vs DFA Differences

### Non-deterministic Finite Automaton (NFA)

**Characteristics:**
- Transitions map to **arrays** of states
- A state can have multiple transitions on the same symbol
- A state can have no transitions on some symbols (implicit trap state)
- More flexible, often more compact representation

**Example:**
```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q2"],
  "transitions": {
    "q0": {
      "a": ["q0", "q1"],  // Multiple destinations
      "b": ["q0"]
    },
    "q1": {
      "b": ["q2"]         // No 'a' transition (implicitly empty)
    }
  }
}
```

### Deterministic Finite Automaton (DFA)

**Characteristics:**
- Transitions map to **single strings**
- Each state has exactly one transition per alphabet symbol
- More verbose but simpler to execute
- Generated from NFA using subset construction

**Example:**
```json
{
  "states": ["{q0}", "{q0,q1}", "{q0,q1,q2}"],
  "alphabet": ["a", "b"],
  "start_state": "{q0}",
  "final_states": ["{q0,q1,q2}"],
  "transitions": {
    "{q0}": {
      "a": "{q0,q1}",     // Single destination
      "b": "{q0}"
    },
    "{q0,q1}": {
      "a": "{q0,q1}",
      "b": "{q0,q1,q2}"
    },
    "{q0,q1,q2}": {
      "a": "{q0,q1}",
      "b": "{q0,q1,q2}"
    }
  }
}
```

---

## Complete Examples

### Example 1: Simple NFA (Strings ending in "ab")

```json
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
      "a": ["q0", "q1"],
      "b": ["q0"]
    }
  }
}
```

**Language:** L = {w ∈ {a,b}* | w ends with "ab"}

**Accepted strings:** `"ab"`, `"aab"`, `"bab"`, `"aaab"`
**Rejected strings:** `"a"`, `"b"`, `"aa"`, `"ba"`

---

### Example 2: DFA (Even number of 'a's)

```json
{
  "states": ["even", "odd"],
  "alphabet": ["a", "b"],
  "start_state": "even",
  "final_states": ["even"],
  "transitions": {
    "even": {
      "a": "odd",
      "b": "even"
    },
    "odd": {
      "a": "even",
      "b": "odd"
    }
  }
}
```

**Language:** L = {w ∈ {a,b}* | w contains an even number of 'a's}

**Accepted strings:** `""`, `"aa"`, `"bab"`, `"aabaa"`
**Rejected strings:** `"a"`, `"aaa"`, `"baba"`

---

### Example 3: NFA (Contains substring "101")

```json
{
  "states": ["q0", "q1", "q2", "q3"],
  "alphabet": ["0", "1"],
  "start_state": "q0",
  "final_states": ["q3"],
  "transitions": {
    "q0": {
      "0": ["q0"],
      "1": ["q0", "q1"]
    },
    "q1": {
      "0": ["q2"]
    },
    "q2": {
      "1": ["q3"]
    },
    "q3": {
      "0": ["q3"],
      "1": ["q3"]
    }
  }
}
```

**Language:** L = {w ∈ {0,1}* | w contains "101" as a substring}

**Accepted strings:** `"101"`, `"0101"`, `"1010"`, `"11011"`
**Rejected strings:** `"0"`, `"1"`, `"00"`, `"110"`

---

## Edge Cases and Special Scenarios

### 1. Empty Transitions (Trap State)

**NFA can omit transitions:**
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": {
    "q0": {
      "a": ["q1"]
      // No 'b' transition - implicitly goes nowhere
    },
    "q1": {
      "a": ["q1"],
      "b": ["q1"]
    }
  }
}
```

### 2. Self-loops

**State transitions to itself:**
```json
"transitions": {
  "q0": {
    "a": ["q0"],  // Self-loop on 'a'
    "b": ["q1"]
  }
}
```

### 3. Multiple Transitions (NFA only)

**Multiple destinations on same symbol:**
```json
"transitions": {
  "q0": {
    "a": ["q0", "q1", "q2"]  // Three possible destinations
  }
}
```

### 4. No Final States

**Automaton that rejects all input:**
```json
{
  "states": ["q0"],
  "alphabet": ["a"],
  "start_state": "q0",
  "final_states": [],  // Empty: no strings accepted
  "transitions": {
    "q0": {
      "a": ["q0"]
    }
  }
}
```

### 5. Start State is Final

**Accepts empty string:**
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a"],
  "start_state": "q0",
  "final_states": ["q0"],  // Start = Final: accepts ""
  "transitions": {
    "q0": {
      "a": ["q1"]
    }
  }
}
```

---

## Validation Checklist

Before submitting JSON to the converter, verify:

- [ ] All required fields present: `states`, `alphabet`, `start_state`, `final_states`, `transitions`
- [ ] `states` is non-empty array with unique strings
- [ ] `alphabet` is non-empty array with unique strings
- [ ] `start_state` exists in `states`
- [ ] All states in `final_states` exist in `states`
- [ ] All keys in `transitions` exist in `states`
- [ ] All symbols in transition maps exist in `alphabet`
- [ ] All destination states exist in `states`
- [ ] For NFA: destinations are arrays
- [ ] For DFA: destinations are strings, all symbols covered

---

## Common Errors

### Error 1: Missing Required Field

❌ **Invalid:**
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a"]
  // Missing: start_state, final_states, transitions
}
```

✅ **Valid:**
```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a"],
  "start_state": "q0",
  "final_states": ["q1"],
  "transitions": {
    "q0": {"a": ["q1"]},
    "q1": {"a": ["q1"]}
  }
}
```

### Error 2: State Not in States List

❌ **Invalid:**
```json
{
  "states": ["q0", "q1"],
  "start_state": "q2"  // q2 not in states!
}
```

### Error 3: Symbol Not in Alphabet

❌ **Invalid:**
```json
{
  "alphabet": ["a"],
  "transitions": {
    "q0": {"b": ["q1"]}  // 'b' not in alphabet!
  }
}
```

### Error 4: Mixed NFA/DFA Format

❌ **Invalid:**
```json
{
  "transitions": {
    "q0": {
      "a": "q1",      // String (DFA)
      "b": ["q0"]     // Array (NFA)
    }
  }
}
```

---

## Type Definitions (TypeScript)

```typescript
// Automaton type definition
interface Automaton {
  states: string[];
  alphabet: string[];
  start_state: string;
  final_states: string[];
  transitions: TransitionMap;
}

// NFA transition map
interface NFATransitionMap {
  [sourceState: string]: {
    [symbol: string]: string[];  // Array of destination states
  };
}

// DFA transition map
interface DFATransitionMap {
  [sourceState: string]: {
    [symbol: string]: string;  // Single destination state
  };
}

type TransitionMap = NFATransitionMap | DFATransitionMap;
```

---

## Python Type Hints

```python
from typing import Dict, List, Union

# Type aliases
State = str
Symbol = str

# NFA type
NFATransitions = Dict[State, Dict[Symbol, List[State]]]

class NFA:
    states: List[State]
    alphabet: List[Symbol]
    start_state: State
    final_states: List[State]
    transitions: NFATransitions

# DFA type
DFATransitions = Dict[State, Dict[Symbol, State]]

class DFA:
    states: List[State]
    alphabet: List[Symbol]
    start_state: State
    final_states: List[State]
    transitions: DFATransitions
```

---

## Testing Your JSON

Use the provided validation function:

```python
from nfa_to_dfa import validate_nfa

nfa_data = {
    "states": ["q0", "q1"],
    "alphabet": ["a"],
    "start_state": "q0",
    "final_states": ["q1"],
    "transitions": {
        "q0": {"a": ["q1"]},
        "q1": {"a": ["q1"]}
    }
}

is_valid, message = validate_nfa(nfa_data)
print(f"Valid: {is_valid}, Message: {message}")
```

---

## References

- **Formal Definition:** [Automata Theory - Hopcroft & Ullman](https://en.wikipedia.org/wiki/Finite-state_machine)
- **JSON Specification:** [RFC 8259](https://tools.ietf.org/html/rfc8259)
- **Subset Construction:** [Powerset Construction Algorithm](https://en.wikipedia.org/wiki/Powerset_construction)

---

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Maintained By:** Automaton Visualizer Project
