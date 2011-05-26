import converters
from types import NoneType
from util import StackCounter, KeyRemover

class Cerealizer(object):

    def __init__( self, **kwargs ):

        self.args = {
            'stacklimit' : None,
            'removekeys' : {},
        }

        self.args.update( kwargs )

        stack_counter = StackCounter( self.args['stacklimit'] )
        key_remover = KeyRemover( self.args['removekeys'] )
        conserve = converters.Conserve()

        self.converters = { int : conserve,
                float : conserve,
                bool : conserve,
                str : converters.UnicodeString(),
                unicode : conserve,
                NoneType : conserve,
                list : converters.List( self, stack_counter ),
                dict : converters.Dict( self, stack_counter, key_remover )
            }

    def updated_args( self, args ):
        new_args = dict( self.args )
        new_args.update( args )
        return new_args

    def find_converter( self, datatype ):
        return self.converters.get( datatype )

    def convert( self, data, *args, **kwargs ):
        converter = self.find_converter( type( data ) )
        if not converter:
            raise TypeError("could not find converter for type %s" % type( data ) )
        return converter( data, *args, **kwargs )


