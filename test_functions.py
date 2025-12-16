# run_tests.py

# Import the necessary components from your framework file
from toolkit import _builtins
from toolkit.runner import Runner,Reporter,SkipException

# --- A. Define Your Test Functions ---
@test
def test_addition_passes():
    """Verify that 1 + 1 equals 2."""
    assert 1 + 1 == 2
    # If this line is reached, the test passes.
@test
def test_multiplication_fails():
    """Verify a deliberate failure."""
    x = 5
    y = 3
    # This assertion will fail (5 * 3 = 15, not 16)
    assert x * y == 16, "Multiplication logic is incorrect"
@test
def test_division_error():
    """Verify a test that raises a critical exception."""
    print("Attempting division by zero...")
    result = 10 / 0 # This will raise ZeroDivisionError
@test
def test_network_skip():
    """Verify a test that is skipped due to environment."""
    # Imagine a condition check here
    network_is_down = True 
    if network_is_down:
        # Use your custom exception to signal a skip
        raise SkipException("Network service is unavailable for external API call.")
    
    # ... rest of the network test code ...
    assert True # placeholder for the actual test
@skip(reason="Im bored")
def test_simple_pass():
    assert True


# --- C. Run the Tests and Report ---

if __name__ == "__main__":
    print("Starting custom test run...")
    
    # 1. Create the Runner instance
    runner = Runner("test_functions.py")
    
    # 2. Run the tests and collect results
    
    test_results = runner.test()
    
    # 3. Create the Reporter instance
    reporter = Reporter(test_results)
    
    # 4. Print the final summary
    reporter.print_summary()