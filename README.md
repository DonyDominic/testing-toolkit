# 🛠️ Toolkit: Minimalist Python Testing Framework

A custom, reflection-based testing engine designed for automated discovery and execution of Python tests. This toolkit implements a full lifecycle: 
- Discovery 
- Execution 
- Result Classification 
- Colorized Reporting.



## 🎯 Features
- **Auto-Discovery:** Scans directories recursively for `test_*.py` files or targets specific files.
- **Decorator-Driven:** Uses `@test` and `@skip` decorators for clean, declarative test definitions.
- **Dynamic Module Loading:** Injects test files into the current process via `importlib`.
- **Introspection Engine:** Uses the `inspect` module to identify valid test functions at runtime.
- **Detailed Result Tracking:** Captures execution time, error traces, and skip reasons.
- **Visual Reporting:** Categorized terminal output with color-coded status maps (PASS/FAIL/SKIP).

---

## 🏗️ Project Architecture

The framework is built using an Object-Oriented approach with three primary layers:

1. **`Runner`**: The core engine. It handles path validation, module imports, and function inspection.
2. **`TestResult`**: A data transfer object (DTO) that encapsulates the outcome of a single test run.
3. **`Reporter`**: A post-processing utility that aggregates statistics and handles terminal UI logic.



---

## 🚀 How to Use

### 1. Define your Tests
Create a Python file (e.g., `test_functions.py` or test/test*.py). Mark your functions using the provided decorators.

```python
from toolkit import _builtins, SkipException

@test
def test_addition_passes():
    """Verify that 1 + 1 equals 2."""
    assert 1 + 1 == 2

@test
def test_division_error():
    """This test will catch a ZeroDivisionError and mark it as FAIL."""
    result = 10 / 0

@skip(reason="Database not connected")
@test
def test_db_query():
    assert True

@test
def test_conditional_skip():
    if True:
        raise SkipException("Skipping because condition met.")
```
### Create a run script
```python
from toolkit.runner import Runner, Reporter

if __name__ == "__main__":
    # 1. Initialize the runner (points to a file or folder)
    runner = Runner(path="test_functions.py")
    
    # 2. Run and collect results
    results = runner.test()
    
    # 3. Generate the report
    reporter = Reporter(results)
    reporter.print_summary()
```

### Run the script file
```python run_tests.py```