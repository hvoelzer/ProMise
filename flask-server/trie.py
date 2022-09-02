
class Trie(object):
    def __init__(self):
        self.child = {}

    def insert(self, operations):
        current = self.child
        for operation in operations:
            if operation not in current:
                current[operation] = {}
            current = current[operation]
        current['#'] = 1

    def search(self, operations):
        current = self.child
        for operation in operations:
            if operation not in current:
                return False
            current = current[operation]
        return '#' in current

    def startsWith(self, prefix):
        current = self.child
        for l in prefix:
            if l not in current:
                return False
            current = current[l]
        return True

    def __repr__(self) -> str:
        return str(self.child)
