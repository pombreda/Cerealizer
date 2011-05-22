import unittest

class TestStackCounter( unittest.TestCase ):

    def test_default_can_increase(self):
        c = StackCounter()
        self.assertTrue( c.can_increase() )

    def test_default_one_increase_can_increase(self):
        c = StackCounter()
        c.increase()
        self.assertTrue( c.can_increase() )

    def test_increase_stack_is_one(self):
        c = StackCounter()
        c.increase()
        self.assertEquals(c.stack, 1)

    def test_increase_stack_multiple_times(self):
        c = StackCounter()
        for x in range(1,10 + 1):
            c.increase()
            self.assertEquals(c.stack, x)

    def test_increase_decrease(self):
        c = StackCounter()
        c.increase()
        c.decrease()
        self.assertEquals(c.stack, 0)

    def test_increase_decrease_multiple_times(self):
        c = StackCounter()
        for x in range(1, 100 + 1):
            c.increase()
            self.assertEquals(c.stack, x)

        r = range(100)
        r.reverse()
        for x in r:
            c.decrease()
            self.assertEquals(c.stack, x)

    def test_no_stack_cannot_decrease(self):
        c = StackCounter()
        self.assertRaises( ValueError, c.decrease )

    def test_stack_limit_of_one(self):

        c = StackCounter(stacklimit=1)
        self.assertTrue( c.can_increase() )
        c.increase()
        self.assertFalse( c.can_increase() )
        c.decrease()
        self.assertTrue( c.can_increase() )

    def test_stack_limit_of_ten(self):

        c = StackCounter(stacklimit=10)
        for x in range(9):
            c.increase()
            self.assertTrue( c.can_increase() )

        c.increase()
        self.assertFalse( c.can_increase() )

        for x in range(10):
            c.decrease()
            self.assertTrue( c.can_increase() )

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from util import *
    unittest.main()
else:
    from util import *
