class Move:
    def __init__(self, source, dest, count = 1):
        self.source = source
        self.dest = dest
        self.count = count

    def __repr__(self):
        return f"Move({self.count} cards from {self.source} to {self.dest})"