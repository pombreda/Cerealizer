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

        result = self.converter( "bla" )
        self.assertEquals( type(result), unicode )

    def test_encoded_string_stays_unicode(self):

        result = self.converter( "bla", 'iso-8859-1' )
        self.assertEquals( type(result), unicode )

    def test_encoded_string_equals_same_value(self):

        result = self.converter( "bla", 'iso-8859-1' )
        self.assertEquals( result, "bla" )

    def encoded_string_equals_same_value(self):

        self.assertEquals( self.converter("bla"), "bla" )

class MockCerealizer(object):

    def __init__(self):
        self.list_converter = None

    def updated_args(self, args):
        return args

    def convert( self, data, *args, **kwargs ):
        if type(data) is list:
            return self.list_converter( data )
        elif type(data) is dict:
            return self.dict_converter( data )
        else:
            return data

class TestListConverter(unittest.TestCase):

    def setUp(self):
        self.converter = self.create_list()

    def create_list(self, stacklimit=None):
        stack_counter = StackCounter(stacklimit)
        cerealizer = MockCerealizer()
        converter = List( cerealizer, stack_counter )
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


class TestDictConverter( unittest.TestCase ):

    def setUp(self):
        self.converter = self.create_converter()

    def create_converter( self, stacklimit=None, removekeys={}):

        stack_counter = StackCounter( stacklimit )
        key_remover = KeyRemover( removekeys )

        cerealizer = MockCerealizer()

        list_converter = List( cerealizer, stack_counter )
        cerealizer.list_converter = list_converter

        converter = Dict( cerealizer, stack_counter, key_remover )
        cerealizer.dict_converter = converter

        return converter

    def test_convert_empty_dict(self):
        self.assertEquals( self.converter( {} ), {} )

    def test_convert_simple_dict(self):
        d = {'a' : 1, 'b' : 2, 'c' : 3}
        self.assertEquals( self.converter( d ), d )

    def test_convert_nested_dict(self):
        d = {'a' : 1, 'b' : True, 'c' : { 'd' : 2, 'e' : False } }
        self.assertEquals( self.converter( d ), d )

    def test_convert_nested_dict_stack_limit_one(self):
        d = {'a' : 1, 'b' : 2, 'c' : { 'd' : 3 } }
        r = {'a' : 1, 'b' : 2, 'c' : None }
        converter = self.create_converter( stacklimit = 1 )
        self.assertEquals( converter( d ), r )

    def test_convert_nested_dict_stack_limit_two(self):
        d = {
                'a' : 1, 
                'b' : 2,
                'c' : { 
                    'd' : 3,
                    'e' : 4, 
                    'f' : { 
                        'g' : 5,
                        'h' : 6 
                    }, 
                    'i' : 7,
                    'j' : { 
                        'k' : 10 
                    }, 
                    'l' : 11 
                }, 
                'm' : 12 
            }

        r = {
                'a' : 1, 
                'b' : 2,
                'c' : { 
                    'd' : 3,
                    'e' : 4, 
                    'f' : None,
                    'i' : 7,
                    'j' : None,
                    'l' : 11,
                }, 
                'm' : 12 
            }

        converter = self.create_converter( 2 )
        self.assertEquals( converter( d ), r )

    def test_convert_simple_remove(self):

        remove = {'d' : True}
        converter = self.create_converter( None, remove )
        d = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4}
        r = {'a' : 1, 'b' : 2, 'c' : 3}

        self.assertEquals( converter( d ), r )

    def test_convert_mutliple_remove(self):

        remove = {'c' : True, 'd' : True}
        converter = self.create_converter( None, remove )
        d = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4}
        r = {'a' : 1, 'b' : 2}

        self.assertEquals( converter( d ), r )

    def test_convert_nested_remove(self):

        remove = {'c' : True, 'd' : { 'e' : True } }
        converter = self.create_converter( None, remove )
        d = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : { 'e' : 4, 'f' : 5 } }
        r = {'a' : 1, 'b' : 2, 'd' : { 'f' : 5 } }

        self.assertEquals( converter( d ), r )

    def test_convert_nested_remove_and_stack_limit(self):

        stacklimit=2
        remove = {'c' : True, 'd' : { 'e' : True } }
        converter = self.create_converter( stacklimit, remove )
        d = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : { 'e' : 4, 'f' : 5 }, 'g' : { 'h' : 6, 'i' : { 'j' : 7 } } }
        r = {'a' : 1, 'b' : 2, 'd' : { 'f' : 5 }, 'g' : { 'h' : 6, 'i' : None } }

        self.assertEquals( converter( d ), r )

if __name__ == '__main__':

    import os.path
    import sys
    sys.path.insert(0, os.path.join( '..', 'src' ) )
    from converters import *
    from util import *
    unittest.main()
else:
    from converters import *

