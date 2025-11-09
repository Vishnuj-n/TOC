"""Streamlit App Tests

Test suite for the NFA to DFA Visualizer multi-page app using Streamlit's app testing framework.
"""

import pytest
from streamlit.testing.v1 import AppTest


class TestMainPage:
    """Tests for the main landing page."""
    
    def test_main_page_loads(self):
        """Test that the main page loads without errors."""
        at = AppTest.from_file("main.py")
        at.run()
        assert not at.exception
        assert "NFA → DFA Visualizer" in at.title[0].value
    
    def test_navigation_buttons_exist(self):
        """Test that navigation buttons are present."""
        at = AppTest.from_file("main.py")
        at.run()
        assert len(at.button) >= 2  # Manual Builder and Convert buttons


class TestManualBuilderPage:
    """Tests for the step-based Manual Builder page."""
    
    def test_manual_builder_loads(self):
        """Test that the manual builder page loads."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        assert not at.exception
        assert "Manual NFA Builder" in at.title[0].value
    
    def test_initial_state_shows_step1_only(self):
        """Test that initially only Step 1 is accessible."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Should have progress indicators
        assert len(at.success) + len(at.info) + len(at.warning) >= 3  # 3 progress steps
        
        # Should have Step 1 form with states and alphabet inputs
        assert len(at.text_input) >= 2
    
    def test_step1_completion_unlocks_step2(self):
        """Test that completing Step 1 unlocks Step 2."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Fill in Step 1
        at.text_input[0].input("q0, q1").run()
        at.text_input[1].input("a, b").run()
        
        # Click Next button (should be first form submit button)
        at.button[0].click().run()
        
        # Check that session state was updated
        assert at.session_state["step1_completed"] == True
        assert "q0" in at.session_state["builder_states"]
        assert "a" in at.session_state["builder_alphabet"]
    
    def test_step1_reset_clears_all_data(self):
        """Test that Reset All button clears all session data."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Set some session state
        at.session_state["builder_states"] = ["q0", "q1"]
        at.session_state["step1_completed"] = True
        at.run()
        
        # Click Reset All button (should be second button in Step 1 form)
        at.button[1].click().run()
        
        # Check that session state was cleared
        assert "step1_completed" not in at.session_state or at.session_state["step1_completed"] == False
    
    def test_step1_validation_requires_states_and_alphabet(self):
        """Test that Step 1 validates required fields."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Try to submit with empty states
        at.text_input[0].input("").run()
        at.text_input[1].input("a, b").run()
        at.button[0].click().run()
        
        # Should show error
        assert len(at.error) > 0
    
    def test_step2_shows_after_step1_completion(self):
        """Test that Step 2 appears after Step 1 is completed."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Complete Step 1
        at.session_state["builder_states"] = ["q0", "q1"]
        at.session_state["builder_alphabet"] = ["a", "b"]
        at.session_state["step1_completed"] = True
        at.run()
        
        # Should have selectbox for start state and multiselect for final states
        assert len(at.selectbox) >= 1
        assert len(at.multiselect) >= 1
    
    def test_step3_shows_transition_inputs(self):
        """Test that Step 3 shows transition input fields."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Complete Steps 1 and 2
        at.session_state["builder_states"] = ["q0", "q1"]
        at.session_state["builder_alphabet"] = ["a", "b"]
        at.session_state["builder_start_state"] = "q0"
        at.session_state["builder_final_states"] = ["q1"]
        at.session_state["step1_completed"] = True
        at.session_state["step2_completed"] = True
        at.run()
        
        # Should have transition inputs (2 states × 2 symbols = 4 inputs, plus Step 1 inputs)
        assert len(at.text_input) >= 6  # 2 for Step 1 + 4 for transitions
    
    def test_transition_summary_displays(self):
        """Test that transition summary table displays correctly."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Set up completed Steps 1 and 2
        at.session_state["builder_states"] = ["q0", "q1"]
        at.session_state["builder_alphabet"] = ["a"]
        at.session_state["builder_start_state"] = "q0"
        at.session_state["builder_final_states"] = ["q1"]
        at.session_state["step1_completed"] = True
        at.session_state["step2_completed"] = True
        at.session_state["builder_transitions"] = {"q0": {"a": ["q1"]}}
        at.run()
        
        # Should have dataframe for transition summary
        assert len(at.dataframe) >= 1 or "No transitions" in str(at.warning)


class TestConvertPage:
    """Tests for the Convert & Visualize page."""
    
    def test_convert_page_loads(self):
        """Test that the convert page loads."""
        at = AppTest.from_file("pages/NFA_to_DFA_Converter.py")
        at.run()
        assert not at.exception
        assert "Convert NFA to DFA" in at.title[0].value
    
    def test_no_nfa_shows_warning_and_redirect(self):
        """Test that warning is shown when no NFA is loaded."""
        at = AppTest.from_file("pages/NFA_to_DFA_Converter.py")
        at.run()
        
        # Should show warning and button to go to Manual Builder
        assert len(at.warning) >= 1
        assert len(at.button) >= 1  # Go to Manual Builder button
    
    def test_convert_with_valid_nfa(self):
        """Test conversion when valid NFA is in session state."""
        at = AppTest.from_file("pages/NFA_to_DFA_Converter.py", default_timeout=10)
        
        valid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"], "b": ["q0"]},
                "q1": {"a": ["q1"], "b": ["q1"]}
            }
        }
        
        at.session_state["nfa_data"] = valid_nfa
        at.run()
        
        # Should show NFA data and have convert button
        assert len(at.button) >= 1  # Convert to DFA button
        assert len(at.json) >= 1 or len(at.code) >= 1  # NFA JSON displayed


class TestAboutPage:
    """Tests for the About & Help page."""
    
    def test_about_page_loads(self):
        """Test that the about page loads."""
        at = AppTest.from_file("pages/About.py")
        at.run()
        assert not at.exception
        assert "About & Help" in at.title[0].value
    
    def test_documentation_tabs_exist(self):
        """Test that documentation tabs are present."""
        at = AppTest.from_file("pages/About.py")
        at.run()
        assert len(at.tabs) >= 1


# ============================================================================
# LOGIC TESTS - Testing core NFA/DFA conversion logic
# ============================================================================

class TestNFAValidationLogic:
    """Unit tests for NFA validation logic."""
    
    def test_valid_nfa_passes_validation(self):
        """Test that a properly structured NFA passes validation."""
        from nfa_to_dfa import validate_nfa
        
        valid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"], "b": ["q0"]},
                "q1": {"a": ["q1"], "b": ["q1"]}
            }
        }
        
        is_valid, message = validate_nfa(valid_nfa)
        assert is_valid
        assert message == "Valid NFA"
    
    def test_missing_required_keys_fails(self):
        """Test that NFA missing required keys fails validation."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {"states": ["q0"], "alphabet": ["a"]}
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "Missing required key" in message
    
    def test_invalid_start_state_fails(self):
        """Test that invalid start state fails validation."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a"],
            "start_state": "q2",  # Not in states
            "final_states": ["q1"],
            "transitions": {}
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "not in states list" in message
    
    def test_invalid_final_state_fails(self):
        """Test that invalid final state fails validation."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a"],
            "start_state": "q0",
            "final_states": ["q2"],  # Not in states
            "transitions": {}
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "not in states list" in message
    
    def test_invalid_transition_symbol_fails(self):
        """Test that transition with invalid symbol fails validation."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"b": ["q1"]}  # 'b' not in alphabet
            }
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "not in alphabet" in message
    
    def test_invalid_transition_destination_fails(self):
        """Test that transition to non-existent state fails validation."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q2"]}  # q2 not in states
            }
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "not in states list" in message


class TestNFAToDFAConversionLogic:
    """Unit tests for NFA to DFA conversion algorithm."""
    
    def test_deterministic_nfa_conversion(self):
        """Test conversion of already deterministic NFA."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"], "b": ["q0"]},
                "q1": {"a": ["q1"], "b": ["q1"]}
            }
        }
        
        dfa, logs = convert_nfa_to_dfa(nfa)
        
        # DFA should have same or similar number of states
        assert len(dfa["states"]) <= 3  # Should be compact
        assert dfa["alphabet"] == nfa["alphabet"]
        assert len(logs) > 0  # Logs should be generated
    
    def test_nondeterministic_nfa_conversion(self):
        """Test conversion of nondeterministic NFA with multiple transitions."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q2"],
            "transitions": {
                "q0": {"a": ["q0", "q1"], "b": ["q0"]},  # Non-deterministic on 'a'
                "q1": {"b": ["q2"]},
                "q2": {"a": ["q2"], "b": ["q2"]}
            }
        }
        
        dfa, logs = convert_nfa_to_dfa(nfa)
        
        # DFA should have combined states
        assert len(dfa["states"]) >= 3
        assert any("{" in state for state in dfa["states"])  # Should have combined states like {q0,q1}
        assert "STEP" in " ".join(logs)  # Should have step-by-step logs
    
    def test_conversion_preserves_alphabet(self):
        """Test that conversion preserves the alphabet."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["x", "y", "z"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"x": ["q1"], "y": ["q0"], "z": ["q0"]},
                "q1": {"x": ["q1"], "y": ["q1"], "z": ["q1"]}
            }
        }
        
        dfa, _ = convert_nfa_to_dfa(nfa)
        assert dfa["alphabet"] == ["x", "y", "z"]
    
    def test_conversion_marks_final_states_correctly(self):
        """Test that DFA final states are marked correctly."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["a"],
            "start_state": "q0",
            "final_states": ["q2"],
            "transitions": {
                "q0": {"a": ["q1"]},
                "q1": {"a": ["q2"]},
                "q2": {"a": ["q2"]}
            }
        }
        
        dfa, _ = convert_nfa_to_dfa(nfa)
        
        # Any DFA state containing q2 should be final
        for state in dfa["final_states"]:
            assert "q2" in state or state == "{q2}"
    
    def test_empty_transition_handling(self):
        """Test that conversion handles states with no outgoing transitions."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"]},
                "q1": {}  # No outgoing transitions
            }
        }
        
        dfa, logs = convert_nfa_to_dfa(nfa)
        
        # Should complete without error
        assert "states" in dfa
        assert len(logs) > 0


# ============================================================================
# INTEGRATION TESTS - Testing end-to-end workflows
# ============================================================================

class TestIntegrationWorkflows:
    """Integration tests for complete user workflows."""
    
    def test_all_pages_load_successfully(self):
        """Test that all pages can be loaded without errors."""
        pages = [
            "main.py",
            "pages/Manual_NFA_Builder.py",
            "pages/NFA_to_DFA_Converter.py",
            "pages/About.py"
        ]
        
        for page_path in pages:
            at = AppTest.from_file(page_path)
            at.run()
            assert not at.exception, f"Page {page_path} failed to load"
            assert len(at.title) > 0, f"Page {page_path} has no title"
    
    def test_step_based_builder_workflow(self):
        """Test the complete step-by-step builder workflow."""
        at = AppTest.from_file("pages/Manual_NFA_Builder.py")
        at.run()
        
        # Initially, only Step 1 should be accessible
        assert "step1_completed" not in at.session_state or at.session_state["step1_completed"] == False
        
        # Complete Step 1
        at.session_state["builder_states"] = ["q0", "q1"]
        at.session_state["builder_alphabet"] = ["a", "b"]
        at.session_state["step1_completed"] = True
        at.run()
        
        # Now Step 2 should be accessible
        assert len(at.selectbox) >= 1
        
        # Complete Step 2
        at.session_state["builder_start_state"] = "q0"
        at.session_state["builder_final_states"] = ["q1"]
        at.session_state["step2_completed"] = True
        at.run()
        
        # Now Step 3 should show transition inputs
        assert len(at.text_input) >= 4  # Step 1 inputs + transition inputs
    
    def test_nfa_to_dfa_conversion_workflow(self):
        """Test complete workflow from NFA creation to DFA conversion."""
        # Create a valid NFA
        valid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"], "b": ["q0"]},
                "q1": {"a": ["q1"], "b": ["q1"]}
            }
        }
        
        # Load converter page with NFA
        at = AppTest.from_file("pages/NFA_to_DFA_Converter.py")
        at.session_state["nfa_data"] = valid_nfa
        at.run()
        
        # Should show NFA and have convert button
        assert "nfa_data" in at.session_state
        assert len(at.button) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
