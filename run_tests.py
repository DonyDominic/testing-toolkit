from toolkit.runner import Runner, Reporter

if __name__ == "__main__":
    runner = Runner(path="test_functions.py")    # auto-discover test/test_*.py
    results = runner.test()

    reporter = Reporter(results)
    reporter.print_summary()
