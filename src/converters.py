
class Converter(object):

    def __init__( self ):
        pass

    def __call__( self, data, **kwargs ):
        raise NotImplementedError("__call__ must be reimplemented by child classes")

class Conserve( Converter ):

    def __call__( self, data, **kwargs ):
        return data

class UnicodeString( Converter ):

    def __init__( self, encoding='utf8' ):
        Converter.__init__( self )
        self.encoding = encoding

    def __call__( self, data, **kwargs ):
        return unicode( data, kwargs.get( 'encoding', self.encoding ) )

class List( Converter ):

    def __init__(self, stack_counter, cerealizer ):
        self.stack_counter = stack_counter
        self.cerealizer = cerealizer

    def __call__(self, data, **kwargs):
        if( self.stack_counter.can_increase() ):

            args = self.cerealizer.updated_args( kwargs )

            self.stack_counter.increase()
            result = [ self.cerealizer.convert( x, **args ) for x in data ]
            self.stack_counter.decrease()

            return result

        else:
            return None

