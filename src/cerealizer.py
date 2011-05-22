
import converters

class Cerealizer(object):

    def __init__( self, **kwargs ):

        conserve = converters.Conserve()
        self.converters = { int : conserve,
                float : conserve,
                bool : conserve,
                str : converters.UnicodeString()
                unicode : conserve

        self.args = {
            'nulls' : False,
            'recursive' : False,
            'stacklimit' : None
        }

        self.args.update( kwargs )

    def updated_args( self, args ):
        new_args = dict( self.args )
        new_args.update( args )
        return new_args

    def find_converter( self, datatype ):
        return self.converters.get( datatype )

    def convert( self, *data, **kwargs ):
        args = self.updated_args( kwargs )
        converter = self.find_converter( type( data ) )
        if not converter:
            raise TypeError("could not find converter for type %s" % type( data ) )
        return converter( data, args )


