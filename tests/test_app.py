"""Streamlit App Tests

Test suite for the NFA to DFA Visualizer multi-page app using Streamlit's app testing framework.
"""

import pytest
from streamlit.testing.v1 import AppTest
import json


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
        
        # Check that buttons exist (in main content and sidebar)
        assert len(at.button) >= 4  # At least 4 navigation buttons
    
    def test_example_nfa_displayed(self):
        """Test that example NFA is shown."""
        at = AppTest.from_file("main.py")
        at.run()
        
        # Check that JSON is rendered
        assert len(at.json) >= 1


class TestManualBuilderPage:
    """Tests for the Manual Builder page."""
    
    def test_manual_builder_loads(self):
        """Test that the manual builder page loads."""
        at = AppTest.from_file("pages/1_📝_Manual_Builder.py")
        at.run()
        assert not at.exception
        assert "Manual NFA Builder" in at.title[0].value
    
    def test_form_exists(self):
        """Test that the NFA builder form exists."""
        at = AppTest.from_file("pages/1_📝_Manual_Builder.py")
        at.run()
        
        # Form should exist
        assert len(at.text_input) >= 2  # At least states and alphabet inputs
    
    def test_build_simple_nfa(self):
        """Test building a simple NFA through the form."""
        at = AppTest.from_file("pages/1_📝_Manual_Builder.py")
        at.run()
        
        # Fill in states (first text input)
        at.text_input[0].input("q0, q1").run()
        
        # Fill in alphabet (second text input)
        at.text_input[1].input("a, b").run()
        
        # Submit form - use button instead of form_submit_button
        # Find the Build NFA button
        for i, button in enumerate(at.button):
            if "Build NFA" in button.label:
                at.button[i].click().run()
                break
        
        # Check that no exception occurred
        assert not at.exception


class TestImportJSONPage:
    """Tests for the Import JSON page."""
    
    def test_import_page_loads(self):
        """Test that the import page loads."""
        at = AppTest.from_file("pages/2_📤_Import_JSON.py")
        at.run()
        assert not at.exception
        assert "Import NFA JSON" in at.title[0].value
    
    def test_tabs_exist(self):
        """Test that import tabs are present."""
        at = AppTest.from_file("pages/2_📤_Import_JSON.py")
        at.run()
        
        # Should have tabs for different input methods
        assert len(at.tabs) >= 1
    
    def test_paste_valid_json(self):
        """Test pasting valid NFA JSON."""
        at = AppTest.from_file("pages/2_📤_Import_JSON.py")
        at.run()
        
        valid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"]},
                "q1": {"b": ["q1"]}
            }
        }
        
        # Find text area and input JSON
        if len(at.text_area) > 0:
            at.text_area[0].input(json.dumps(valid_nfa)).run()
            assert not at.exception
    
    def test_load_example(self):
        """Test loading an example NFA."""
        at = AppTest.from_file("pages/2_📤_Import_JSON.py")
        at.run()
        
        # Should have selectbox for examples
        assert len(at.selectbox) >= 1
        
        # Click load example button if it exists
        if len(at.button) > 0:
            # Find the load example button
            for i, button in enumerate(at.button):
                if "Load Example" in button.label:
                    at.button[i].click().run()
                    assert not at.exception
                    break


class TestConvertPage:
    """Tests for the Convert & Visualize page."""
    
    def test_convert_page_loads(self):
        """Test that the convert page loads."""
        at = AppTest.from_file("pages/3_🔄_Convert_NFA_DFA.py")
        at.run()
        assert not at.exception
        assert "Convert NFA to DFA" in at.title[0].value
    
    def test_no_nfa_warning(self):
        """Test that warning is shown when no NFA is loaded."""
        at = AppTest.from_file("pages/3_🔄_Convert_NFA_DFA.py")
        at.run()
        
        # Should show warning when no NFA is loaded
        assert len(at.warning) >= 1
    
    def test_convert_with_nfa(self):
        """Test conversion when NFA is in session state."""
        at = AppTest.from_file("pages/3_🔄_Convert_NFA_DFA.py")
        
        # Set NFA in session state
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
        
        # Should not show warning
        # Should have convert button
        assert len(at.button) >= 1
        
        # Click convert button (first button)
        at.button[0].click().run()
        
        # Check that conversion succeeded (should have DFA in session state)
        assert "dfa_data" in at.session_state
        assert "conversion_logs" in at.session_state


class TestAboutPage:
    """Tests for the About & Help page."""
    
    def test_about_page_loads(self):
        """Test that the about page loads."""
        at = AppTest.from_file("pages/4_ℹ️_About.py")
        at.run()
        assert not at.exception
        assert "About & Help" in at.title[0].value
    
    def test_tabs_exist(self):
        """Test that documentation tabs exist."""
        at = AppTest.from_file("pages/4_ℹ️_About.py")
        at.run()
        
        # Should have multiple tabs
        assert len(at.tabs) >= 1
    
    def test_examples_shown(self):
        """Test that examples are displayed."""
        at = AppTest.from_file("pages/4_ℹ️_About.py")
        at.run()
        
        # Should have JSON examples
        assert len(at.json) >= 1


class TestNFAValidation:
    """Tests for NFA validation logic."""
    
    def test_valid_nfa(self):
        """Test validation of a valid NFA."""
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
    
    def test_missing_keys(self):
        """Test validation fails with missing keys."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"]
            # Missing start_state, final_states, transitions
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "Missing required key" in message
    
    def test_invalid_start_state(self):
        """Test validation fails with invalid start state."""
        from nfa_to_dfa import validate_nfa
        
        invalid_nfa = {
            "states": ["q0", "q1"],
            "alphabet": ["a", "b"],
            "start_state": "q2",  # Not in states
            "final_states": ["q1"],
            "transitions": {
                "q0": {"a": ["q1"]},
                "q1": {"b": ["q1"]}
            }
        }
        
        is_valid, message = validate_nfa(invalid_nfa)
        assert not is_valid
        assert "not in states list" in message


class TestNFAToDFAConversion:
    """Tests for NFA to DFA conversion logic."""
    
    def test_simple_conversion(self):
        """Test conversion of a simple NFA."""
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
        
        # Check DFA structure
        assert "states" in dfa
        assert "alphabet" in dfa
        assert "start_state" in dfa
        assert "final_states" in dfa
        assert "transitions" in dfa
        
        # Check logs were generated
        assert len(logs) > 0
    
    def test_nondeterministic_conversion(self):
        """Test conversion of a nondeterministic NFA."""
        from nfa_to_dfa import convert_nfa_to_dfa
        
        nfa = {
            "states": ["q0", "q1", "q2"],
            "alphabet": ["a", "b"],
            "start_state": "q0",
            "final_states": ["q2"],
            "transitions": {
                "q0": {
                    "a": ["q0", "q1"],  # Nondeterministic!
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
        
        # DFA should have more states due to subset construction
        assert len(dfa["states"]) >= len(nfa["states"])
        
        # Check that conversion log is detailed
        assert any("STEP" in log for log in logs)


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
