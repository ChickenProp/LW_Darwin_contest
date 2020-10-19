# Rejected ideas:
#
# * Use a top-level declaration `foo = 'bar'`, and see if `foo` is in the global
#   namespace. This would help to catch someone who tries to parse the AST and
#   extract just the code for the class. (To play around with imports maybe?)
#   lsusr says this is forbidden. I think it was unlikely to do much anyway.
#
# * Store `os.getpid()` in `__init__` and check it in `move`. If they differ,
#   someone's using multiprocessing on us - or maybe the game engine is
#   multiprocessed. lsusr said it wasn't when I asked, but explicitly made no
#   promises, so not risking it.
#
# * Get a list of all ancestor pids (current pid, parent pid, grandparent
#   pid...) and kill one of them randomly. In case someone tries to simulate us
#   by using two levels of multiprocessing. More complicated (`os` doesn't
#   have anything to support this), marginal benefit.
#
# * Use `inspect` package to look at call stack. Not my idea. Not sure exactly
#   how it would work and didn't take the time to think about it.

class JailBreaker():
    def __init__(self, round=0):
        import os
        import logging
        import multiprocessing as mp
        self.os = os
        self.logging = logging

        self.turn = 0

        # If someone tries to use deepcopy to reset state, it won't reset this.
        # The list is probably overkill.
        self.turnCont = lambda x: x
        self.turnCont.turn = [0]

        # Protect against multiprocessing.
        self.turnMP = mp.Value('i', 0)

    def move(self, previous=None):
        if (previous is None) != (self.turn == 0):
            self.logging.error('bad previous')
            self.brk()

        if self.turn != self.turnCont.turn[0]:
            self.logging.error('bad turnCont')
            self.brk()

        if self.turn != self.turnMP.value:
            self.logging.error('bad turnMP')
            self.brk()

        self.turn += 1
        self.turnCont.turn[0] += 1
        self.turnMP.value += 1
        return 3

    def brk(self, x=True):
        # Use three different ways to break, in case an opponent mitigates one
        # of them.
        #
        # * Infinite loop: can be mitigated by having a timeout.
        #
        # * Kill self: can be mitigated by running in multiprocessing, as long
        #   as you catch errors.
        #
        # * Kill parent: if not run in multiprocessing, the engine might make
        #   this ineffective (e.g. if parent pid owned by a different user).
        #   Might also be ways to disown a process?
        self.logging.error('breaking')
        if x:
            import random
            r = random.random()
            if r < 0.33:
                self.logging.error('killing self')
                self.os.kill(self.os.getpid(), 9)
            elif r > 0.67:
                self.logging.error('killing parent')
                self.os.kill(self.os.getppid(), 9)

        self.logging.error('loop')
        try:
            while True:
                pass
        except BaseException as e:
            self.brk(False)
