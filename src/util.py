
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
