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



class TestKeyRemover( unittest.TestCase ):

    def setUp(self):
        self.remover = KeyRemover()

    def test_filter_nothing(self):
        self.assertEquals( self.remover.filter([]), [] )

    def test_filter_no_remove(self):
        k = ['a', 'b', 'c', 'd']
        self.assertEquals( self.remover.filter( k ), k )

    def test_stack_size_is_one(self):
        self.assertEquals( len(self.remover.removestack), 1 )

    def test_keys_are_empty(self):
        self.assertEquals( len(self.remover.keys) , 0 )

    def test_leave_key_raises_error(self):
        self.assertRaises( IndexError, self.remover.leave_key )

    def test_enter_unknown_key_returns_full_list(self):
        k = ['a', 'b', 'c', 'd']
        self.remover.enter_key('e')
        self.assertEquals( self.remover.filter( k ), k )
        self.remover.leave_key()
        self.assertEquals( len( self.remover.removestack ), 1 )

    def test_filter_one_key(self):
        remover = KeyRemover({'a' : True})
        keys = ['a', 'b', 'c', 'd']
        result = ['b', 'c', 'd']
        self.assertEquals( remover.filter( keys ), result )

    def test_filter_two_keys(self):
        remover = KeyRemover({'a' : True, 'b' : True})
        keys = ['a', 'b', 'c', 'd']
        result = ['c', 'd']
        self.assertEquals( remover.filter( keys ), result )

    def test_filter_nested_remove(self):
        r = {'a' : True, 'b' : True, 'c' : {'d' : True} }
        remover = KeyRemover( r )
        keys = ['a', 'b', 'c', 'd']
        result = ['c', 'd']
        self.assertEquals( remover.filter( keys ), result )

    def test_entering_remove_key(self):
        k = {'a' : True, 'b' : {'c' : True} }
        r = {'c' : True}

        remover = KeyRemover( k )
        remover.enter_key( 'b' )
        self.assertEquals( remover.keys, r )
        remover.leave_key()
        self.assertEquals( remover.keys, k )

    def test_enter_remove_key_filter(self):
        remove = {'a' : True, 'b' : {'c' : True, 'd' : True} }
        keys = ['a', 'b', 'c', 'd']

        remover = KeyRemover( remove )
        self.assertEquals( remover.filter( keys ), ['b', 'c', 'd'] )

        remover.enter_key( 'b' )
        self.assertEquals( remover.filter( keys ), ['a', 'b'] )
        remover.leave_key()
        self.assertEquals( remover.filter( keys ), ['b', 'c', 'd' ] )

    def test_enter_multiple_remove_keys(self):
        remove = {'a' : True, 'b' : {'c' : True, 'd' : {'e' : True, 'f' : True } } }

        remover = KeyRemover( remove )
        self.assertEquals( remover.keys, remove )
        self.assertEquals( len( remover.removestack), 1 )

        remover.enter_key( 'b' )
        self.assertEquals( remover.keys, remove['b'] )
        self.assertEquals( len( remover.removestack), 2 )

        remover.enter_key( 'd' )
        self.assertEquals( remover.keys, remove['b']['d'] )
        self.assertEquals( len( remover.removestack), 3 )

        remover.enter_key( 'g' )
        self.assertEquals( remover.keys, {} )
        self.assertEquals( len( remover.removestack), 4 )

        remover.leave_key()
        self.assertEquals( remover.keys, remove['b']['d'] )
        self.assertEquals( len( remover.removestack), 3 )

        remover.leave_key()
        self.assertEquals( remover.keys, remove['b'] )
        self.assertEquals( len( remover.removestack), 2 )

        remover.leave_key()
        self.assertEquals( remover.keys, remove )
        self.assertEquals( len( remover.removestack), 1 )

    def test_enter_multiple_remove_filter(self):
        remove = {'a' : True, 'b' : {'c' : True, 'd' : {'e' : True, 'f' : True } } }
        keys = ['a', 'b', 'c', 'd', 'e', 'f']

        remover = KeyRemover( remove )
        self.assertEquals( remover.filter( keys ), keys[1:] )

        remover.enter_key( 'b' )
        self.assertEquals( remover.filter( keys ), keys[0:2] + keys[3:] )

        remover.enter_key( 'd' )
        self.assertEquals( remover.filter( keys ), keys[:4] )

        remover.enter_key( 'g' )
        self.assertEquals( remover.filter( keys ), keys )

        remover.leave_key()
        self.assertEquals( remover.filter( keys ), keys[:4] )

        remover.leave_key()
        self.assertEquals( remover.filter( keys ), keys[0:2] + keys[3:] )

        remover.leave_key()
        self.assertEquals( remover.filter( keys ), keys[1:] )


if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from util import *
    unittest.main()
else:
    from util import *
