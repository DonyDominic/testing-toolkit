from .exceptions import SkipException
def test(func=None):
    """
    Marks a function as a testcase.

    Args:
        func(Callable) : function to be tested.
    
    Returns:
        Callable : wrapper function with meta-data.
    """
    # Case 1: called as @test
    if func is not None:
        func._is_test = True
        return func

    # Case 2: called as @test()
    def wrapper(f):
        f._is_test = True
        return f
    return wrapper


def skip(reason=None):
    '''
    Marks a testcase function be to skipped.

    Args:
        func(Callable) : function to be skipped.
        reason(str) : reason for skipping.

    Returns:
        Callable : wrapper function with meta-data.
    '''
    def decorator(f):
        def wrapper():
            raise SkipException(reason or "Skipped")
        wrapper._is_test = True
        wrapper._is_skip = True
        wrapper._reason = reason
        wrapper.__name__ = f.__name__

        return wrapper
    return decorator