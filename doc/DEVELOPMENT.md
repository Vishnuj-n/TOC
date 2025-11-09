# Development Guide

## Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd TOC

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## Running the Application

```bash
# Start the Streamlit app
streamlit run main.py

# Access at http://localhost:8501
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_nfa_to_dfa.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run Streamlit app tests
pytest tests/test_app.py -v
```

## Code Structure

### Core Files

- **`main.py`**: Landing page with navigation and overview
- **`nfa_to_dfa.py`**: Core conversion algorithm and validation
- **`graph_visualizer.py`**: Graphviz graph generation

### Pages

- **`1_📝_Manual_Builder.py`**: Interactive form-based NFA builder
- **`2_📤_Import_JSON.py`**: JSON upload/paste/example loading
- **`3_🔄_Convert_NFA_DFA.py`**: Conversion execution and visualization
- **`4_ℹ️_About.py`**: Documentation and help

### Tests

- **`test_nfa_to_dfa.py`**: Core algorithm tests (11 tests)
- **`test_app.py`**: Streamlit app integration tests (21 tests)
- **`fixtures.py`**: Shared test fixtures

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Keep functions focused and concise
- Document complex logic with comments
- Write descriptive variable names

## Adding New Features

1. **Plan**: Document the feature in an issue
2. **Implement**: Write code with tests
3. **Test**: Ensure all tests pass
4. **Document**: Update relevant docs
5. **Review**: Check code quality

## Debugging

```bash
# Enable Streamlit debug mode
streamlit run main.py --logger.level=debug

# Use Python debugger
import pdb; pdb.set_trace()
```

## Contributing

1. Create a feature branch
2. Make changes with tests
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

## Performance Optimization

- Keep page files under 200 lines
- Minimize session state usage
- Use @st.cache_data for expensive operations
- Optimize graph rendering for large automata
