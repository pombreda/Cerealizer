
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
        Converter.__init__( self, cerealizer )
        self.encoding = encoding

    def __call__( self, data, **kwargs ):
        return unicode( data, kwargs.get( 'encoding', self.encoding ) )
