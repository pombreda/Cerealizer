import unittest

class TestConverterBaseClass( unittest.TestCase ):

    def setUp(self):
        self.converter = Converter()

    def test_base_converter_not_implemented_when_called(self):

        self.assertRaises( NotImplementedError, self.converter, 'bla' )

class TestConserveConverter( unittest.TestCase ):

    def setUp(self):
        self.converter = Conserve()

    def test_none_conversion(self):

        #self.assertIsNone( self.converter( None ) )
        self.assertEquals( self.converter( None ), None )

    def test_conversion_abstract_type_stays_same(self):

        class AbstractType:
            pass

        a = AbstractType()

        self.assertTrue( type( self.converter( a ) == type( a ) ) )

    def test_conversion_type_stays_same(self):

        value = 1234
        self.assertTrue( type( self.converter( value ) ) == type( value ) )

    def test_int_conversion(self):

        number = 1
        self.assertEquals( self.converter( number ), number )

    def test_float_conversion(self):

        number = 3.141516
        self.assertEquals( self.converter( number ), number )

    def test_bool_conversion(self):

        a = False
        self.assertEquals( self.converter( a ), a )

class TestUnicodeStringConverter( unittest.TestCase ):

    def setUp(self):
        self.converter = UnicodeString()

    def test_none_conversion_raises_error(self):
        
        self.assertRaises( TypeError, self.converter, None )

    def test_empty_string(self):

        self.assertEquals( self.converter( "" ), "" )

    def test_str_becomes_unicode(self):

        result = self.converter( "bla ")
        self.assertEquals( type(result), unicode )

    def test_encoded_string_stays_unicode(self):

        result = self.converter( "bla", encoding='iso-8859-1' )
        self.assertEquals( type(result), unicode )

    def test_encoded_string_equals_same_value(self):

        result = self.converter( "bla", encoding='iso-8859-1' )
        self.assertEquals( result, "bla" )

    def encoded_string_equals_same_value(self):

        self.assertEquals( self.converter("bla"), "bla" )

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    print sys.path
    from converters import *
    unittest.main()
else:
    from converters import *

