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

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from cerealizer import *
    unittest.main()
else:
    from cerealizer import *
