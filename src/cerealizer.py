import converters
from types import NoneType
from util import StackCounter

class Cerealizer(object):

    def __init__( self, **kwargs ):

        self.args = {
            'nulls' : False,
            'stacklimit' : None
        }

        self.args.update( kwargs )

        stack_counter = StackCounter( self.args['stacklimit'] )
        conserve = converters.Conserve()

        self.converters = { int : conserve,
                float : conserve,
                bool : conserve,
                str : converters.UnicodeString(),
                unicode : conserve,
                NoneType : conserve,
                list : converters.List( stack_counter, self )
            }

    def updated_args( self, args ):
        new_args = dict( self.args )
        new_args.update( args )
        return new_args

    def find_converter( self, datatype ):
        return self.converters.get( datatype )

    def convert( self, data, **kwargs ):
        args = self.updated_args( kwargs )
        converter = self.find_converter( type( data ) )
        if not converter:
            raise TypeError("could not find converter for type %s" % type( data ) )
        return converter( data, **args )


