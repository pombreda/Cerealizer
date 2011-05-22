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

class MockCerealizer(object):

    def __init__(self):
        self.list_converter = None

    def updated_args(self, args):
        return args

    def convert( self, data, **kwargs ):
        if type(data) is list:
            return self.list_converter( data )
        else:
            return data

class TestListConverter(unittest.TestCase):

    def setUp(self):
        self.converter = self.create_list()

    def create_list(self, stacklimit=None):
        counter = StackCounter(stacklimit)
        cerealizer = MockCerealizer()
        converter = List( counter, cerealizer )
        cerealizer.list_converter = converter
        return converter

    def test_convert_empty_list(self):
        self.assertEquals( self.converter( [] ), [] )

    def test_convert_list_with_none(self):
        self.assertEquals( self.converter( [None] ), [None] )

    def test_convert_list_one_element(self):
        self.assertEquals( self.converter( [1] ), [1] )

    def test_convert_list_not_same_reference(self):
        l = [1,2,3]
        self.assertFalse( self.converter( l ) is l )

    def test_convert_list_multiple_integers(self):
        self.assertEquals( self.converter( [1,2,3,4,5,6,7,8,9,0] ),
                [1,2,3,4,5,6,7,8,9,0] )

    def test_convert_list_mixed_types(self):
        e = [1, 'a', None, 1.23456879, True]
        self.assertEquals( self.converter( e ), e )

    def test_convert_nested_list(self):
        e = [1,2,3, [4,5,6] ]
        self.assertEquals( self.converter( e ), e )

    def test_convert_three_nested_lists(self):
        e = [1,2,3, [4,5,6, [7,8,9] ], 10, 11, 12 ]
        self.assertEquals( self.converter( e ), e )

    def test_convert_nested_mixed_list(self):
        e = [1,'a',True, [2,'b',None, [3.123456789, 'c', False], 'abcd'], 1234, True]
        self.assertEquals( self.converter( e ), e )

    def test_convert_list_stack_limit_one(self):
        converter = self.create_list(1)
        l = [1,2,3, [4,5,6]]
        r = [1,2,3,None]
        self.assertEquals( converter( l ), r )

    def test_convert_list_stack_limit_two(self):
        converter = self.create_list(2)
        l = [1,2,3, [4,5,6, [7,8,9] ] ]
        r = [1,2,3, [4,5,6, None] ]
        self.assertEquals( converter( l ), r )

    def test_convert_list_stack_limit_dispered(self):
        converter = self.create_list(2)
        l = [ 1,2,3, [4,5,6, [7,8,9], 10, [11,12,13], 14, [ [] ] ] ]
        r = [ 1,2,3, [4,5,6, None,    10, None,       14, None,  ] ]
        self.assertEquals( converter( l ), r )

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from converters import *
    from util import StackCounter
    unittest.main()
else:
    from converters import *

