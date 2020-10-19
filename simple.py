import random

class ConstBot0():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 0

class ConstBot1():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 1

class ConstBot2():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 2

class ConstBot3():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 3

class ConstBot4():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 4

class ConstBot5():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return 5

class RandomBot():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        return random.choice([0,1,2,3,4,5])

class SimpleTFTBot():
    def __init__(self, round=0):
        pass

    def move(self, previous=None):
        if previous == None:
            return 2
        else:
            return previous

class ASTFallbackBot():
    def __init__(self, round=0):
        self.our_previous = None

    def move(self, previous):
        if previous is not None and self.our_previous is not None:
            if self.our_previous + previous > 5:
                play = 5 - previous
            else:
                play = previous
        else:
            play = 3

        self.our_previous = play
        return play
