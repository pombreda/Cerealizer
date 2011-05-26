
class StackCounter(object):

    def __init__(self, stacklimit=None):
        self.stacklimit = stacklimit
        self.stack = 0

    def increase(self):
        self.stack += 1

    def decrease(self):
        if self.stack == 0:
            raise ValueError("stack counter cannot go below 0")
        self.stack -= 1

    def can_increase(self):
        return (self.stacklimit is None) or (self.stack < self.stacklimit)

class KeyRemover(object):

    def __init__( self, removekeys={} ):
        self.removestack = [ removekeys ]

    @property
    def keys(self):
        return self.removestack[-1]

    def filter(self, all_keys):
        return [ x for x in all_keys if x not in self.keys or self.keys[x] is not True ]

    def enter_key(self, key):
        context = self.keys.get(key, {})
        if type(context) is not dict:
            raise ValueError("remove context when entering key %s was not a dict" % key )
        self.removestack.append( context )

    def leave_key(self):
        if len( self.removestack ) == 1:
            raise IndexError("cannot remove last context from stack")
        self.removestack.pop()

