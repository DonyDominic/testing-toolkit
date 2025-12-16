import toolkit._builtins
from utils.colors import Color , _print_detail
from pathlib import Path
import time
import inspect
import importlib
from .exceptions import SkipException

class TestResult():
    '''
    Stores the outcome of a single test execution.

    Attributes:
        name (str): The name of the test function.
        duration (float): Time taken to run the test, in seconds.
        passed (bool | None): 
            True if the test passed,
            False if the test failed,
            None if not applicable (e.g., skipped).
        error (str | None): Error message when the test fails. None if no error.
        skipped (bool | None): 
            True if the test was skipped,
            False otherwise.
        reason (str | None): Reason for skipping the test, if provided.
    '''
    def __init__(self,name:str|None,duration:float|None,passed:bool|None,error:str|None,skipped:bool|None,reason:str|None) -> None:
        self.name = name
        self.duration = duration
        self.passed = passed
        self.error = error
        self.skipped = skipped
        self.reason = reason
    def __repr__(self):
        status = "PASSED" if self.passed else ("FAILED" if self.passed is False else ("SKIPPED" if self.skipped else "ERROR"))
        return f"<{self.name}: {status} in {self.duration:.4f}s>"
        

        

class Runner():
    '''
    Runs the tests for the specified folder or file.

    Attributes:
        path(str): a folder or a python file. 
            deafult : 'tests/'

    '''
    def __init__(self,path="tests") -> None:
        
        self.path = Path(path)
        self.modules = []
        self.test_functions = []
        self.results = []

        self._load_test_files()
        self._load_tests()
    
    def _load_test_files(self):
        '''load test files in folder or a specified file'''
        if not self.path.exists():
            raise ValueError(f"Path not found: {self.path}")
        
        # case 1 : user gave a folder
        if self.path.is_dir():
            # iterate over the given `folder` and find `test_*.py` files
            files = self.path.glob(pattern="test_*.py")

        # case 2 : user gave .py file
        elif self.path.is_file() and self.path.suffix == ".py":
            files = [self.path]

        # case 3 : err
        else:
            raise ValueError("Path must be a folder or a .py file.")

        for file in files:
            module_name = str(file).replace("/",".")[:-3] # strip .py
            importlib.import_module(module_name)
            self.modules.append(module_name)
        

    def _load_tests(self):
        for module_name in self.modules:
            # dynamically import `test modules` in the current process
            module = importlib.import_module(module_name)

            # inspect for functions in the module
            for name,obj in inspect.getmembers(module,inspect.isfunction):
                if getattr(obj,"_is_test",False):
                    # append into test_functions list if `test` is present
                    self.test_functions.append(obj)
                
    
    def test(self):
        for f in self.test_functions:
            start = time.time()
            passed = None
            error = None
            skipped = None
            duration = None
            reason = None
            name = getattr(f, "_test_name", f.__name__) 
            try:
                if getattr(f, "_is_skip", False):
                    skipped = True
                    reason = getattr(f, "_reason", "No reason provided")
                    duration = time.time() - start
                    self.results.append(TestResult(
                        name=name,
                        duration=duration,
                        passed=None,
                        error=None,
                        skipped=skipped,
                        reason=reason
                    ))
                    continue  # skip actual execution
                f()
                passed = True
                skipped = False
            except SkipException as e:
                skipped = True
                reason = str(e)
            except Exception as e:
                passed = False
                skipped = False
                error = f"{type(e).__name__}: {e}"
            finally:
                duration = time.time() - start
            self.results.append(TestResult(
                name=name,
                duration=duration,
                passed=passed,
                error=error,
                skipped=skipped,
                reason=reason
            ))

        return self.results

class Reporter():
    def __init__(self, results : list[TestResult]) -> None:
        self.results = results
        self.passed_list = []
        self.failed_list = []
        self.skipped_list = []
        self.total_time = .0
        self.classify()
    
    def classify(self):
        for result in self.results:
            if isinstance(result.duration,(int,float)):
                self.total_time += result.duration
            if result.skipped:
                self.skipped_list.append(result)
            elif result.passed:
                self.passed_list.append(result)
            else:
                self.failed_list.append(result)

        print("\n--- Test Results ---")
        for result in self.results:
            status = "PASS" if result.passed else ("SKIP" if result.skipped else "FAIL")

            STATUS_MAP = {
                "PASS":  (Color.BOLD , Color.FG_GREEN),
                "FAIL":  (Color.BOLD , Color.FG_RED),
                "SKIP":  (Color.THIN , Color.FG_GREY),
            
            }

            style, color = STATUS_MAP[status]

            text = f"[{status}] {result.name} ({result.duration:.4f}s)"
            _print_detail(text,style|color)
            if result.error:
                err = f" Error: {result.error}"
                _print_detail(err,style|color)

            if result.reason:
                reason = f" Reason: {result.reason}"
                _print_detail(reason,style|color)
                
            print()

    def print_summary(self):
        total = len(self.results)
        num_passed = len(self.passed_list)
        num_failed = len(self.failed_list)
        num_skipped = len(self.skipped_list)
        
        print(f"{num_passed} passed, {num_failed} failed, {num_skipped} skipped in {self.total_time:.4f}s")

