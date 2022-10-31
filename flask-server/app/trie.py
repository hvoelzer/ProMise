
class Trie(object):
    def __init__(self):
        self.child = {"#": 0}

    def insert(self, operations, new_id):

        current = self.child
        for n, operation in enumerate(operations):
            if operation not in current:
                if n == len(operations) - 1:
                    current[operation] = {"#": new_id}
                    break
                else:
                    current[operation] = {}
            current = current[operation]

    def search(self, operations):
        current = self.child
        for operation in operations:
            if operation not in current:
                return False
            current = current[operation]
        return current["#"]

    def startsWith(self, prefix):
        current = self.child
        for l in prefix:
            if l not in current:
                return False
            current = current[l]
        return True

    def getElement(self, prefix, ret):
        current = self.child
        for l in prefix:
            if l not in current:
                return False, ret
            current = current[l]
        return True, current["#"]

    def __repr__(self) -> str:
        return str(self.child)
