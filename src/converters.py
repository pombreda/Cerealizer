
class Converter(object):

    def __init__( self ):
        pass

    def __call__( self, data ):
        raise NotImplementedError("__call__ must be reimplemented by child classes")

class Conserve( Converter ):

    def __call__( self, data ):
        return data 

class UnicodeString( Converter ):

    def __init__( self, encoding='utf8' ):
        Converter.__init__( self )
        self.encoding = encoding

    def __call__( self, data, encoding=None ):
        return unicode( data, encoding or self.encoding )


class DepthConverter( Converter ):

    def __init__(self, cerealizer, stack_counter ):
        Converter.__init__(self)
        self.cerealizer = cerealizer
        self.stack_counter = stack_counter

    def convert( self, data ):
        raise NotImplementedError("convert must be implemented in child classes")

    def __call__( self, data, *args, **kwargs ):
        result = None

        if( self.stack_counter.can_increase() ):

            self.stack_counter.increase()
            result = self.convert( data, *args, **kwargs )
            self.stack_counter.decrease()

        return result

class List( DepthConverter ):

    def __init__(self, cerealizer, stack_counter ):
        DepthConverter.__init__( self, cerealizer, stack_counter )

    def convert( self, data ):
        return [ self.cerealizer.convert( x ) for x in data ]

class Dict( DepthConverter ):

    def __init__(self, cerealizer, stack_counter, key_remover ):
        DepthConverter.__init__( self, cerealizer, stack_counter )
        self.key_remover = key_remover

    def convert(self, data):
        result = {}
        keys = self.key_remover.filter( data.keys() )

        for key in keys:
            self.key_remover.enter_key( key )
            result[key] = self.cerealizer.convert( data[key] )
            self.key_remover.leave_key()

        return result

