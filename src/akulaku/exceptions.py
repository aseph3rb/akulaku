
class AkulakuError(Exception):

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif other.args == self.args:
            return True
        return False
