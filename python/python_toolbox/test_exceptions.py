import exceptions
import unittest
import time
from func_timeout import FunctionTimedOut

class TestExceptions(unittest.TestCase):

    def test_without_timeout(self):    
        @exceptions.try_and_catch_exception()
        def workwork():
            print("workwork!")
        workwork()

    def test_timeout_succeed(self):   
        @exceptions.try_and_catch_exception(set_timeout=True, timeout=6)
        def workwork_sleep5secs():
            print("workwork!")
            time.sleep(5)
        workwork_sleep5secs()

    def test_timeout_fail(self):   
        @exceptions.try_and_catch_exception(set_timeout=True, timeout=2)
        def workwork_sleep5secs():
            print("workwork!")
            time.sleep(5)
        self.assertRaises(FunctionTimedOut, workwork_sleep5secs)

if __name__ == '__main__':
    unittest.main()