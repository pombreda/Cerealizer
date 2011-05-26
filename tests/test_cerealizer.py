import unittest

class TestCerealizerSimpleTypes( unittest.TestCase ):

    def setUp(self):
        self.cerealizer = Cerealizer()

    def test_cerealize_none(self):
        
        self.assertEquals( self.cerealizer.convert( None ), None )

    def test_cerealize_empty_string(self):

        self.assertEquals( self.cerealizer.convert(""), "")

    def test_cerealize_string(self):

        self.assertEquals( self.cerealizer.convert("bla"), u"bla" )

    def test_cerealize_number_zero(self):

        self.assertEquals( self.cerealizer.convert(0), 0 )

    def test_cerealize_boolean(self):

        self.assertFalse( self.cerealizer.convert(False) )
        self.assertTrue( self.cerealizer.convert(True) )

    def test_cerealize_integer(self):

        self.assertEquals( self.cerealizer.convert( 123456789 ), 123456789  )

    def test_cerealize_float(self):

        self.assertEquals( self.cerealizer.convert( 1.23456789 ), 1.23456789 )

    def test_cerealize_list(self):

        l = [1,'a',True, [2,'b', 1.1234567, [3,'c', False], 4, [None, 5, 'd'], 6 ], 7, True ]
        self.assertEquals( self.cerealizer.convert( l ), l )

    def test_cerealize_list_stacklimit(self):
        c = Cerealizer(stacklimit=2)
        l = [ 1,2,3, [4,5,6, [7,8,9], 10, [11,12,13], 14, [ [] ] ] ]
        r = [ 1,2,3, [4,5,6, None,    10, None,       14, None,  ] ]
        self.assertEquals( c.convert( l ), r )

    def test_cerealize_dict(self):
        d = {'a' : 1, 'b' : '2', 'c' : None, 'd' : True, 'e' : {'f' : 2, 'g' : False, 'h' : {'i' : 3} } }
        self.assertEquals( self.cerealizer.convert( d ), d )

    def test_cerealize_dict_stacklimit_removekeys(self):
        stacklimit=2
        remove = {'c' : True, 'd' : { 'e' : True } }
        c = Cerealizer( stacklimit = stacklimit, removekeys = remove )
        d = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : { 'e' : 4, 'f' : 5 }, 'g' : { 'h' : 6, 'i' : { 'j' : 7 } } }
        r = {'a' : 1, 'b' : 2, 'd' : { 'f' : 5 }, 'g' : { 'h' : 6, 'i' : None } }
        self.assertEquals( c.convert( d ), r )

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from cerealizer import *
    unittest.main()
else:
    from cerealizer import *
