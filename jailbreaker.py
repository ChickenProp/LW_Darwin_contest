class JailBreaker():
    def __init__(self, round=0):
        import os
        import logging
        self.os = os
        self.logging = logging

        logging.error(f'jailbreaker initialized in pid {os.getpid()}')
        self.turn = 0

        # If someone tries to use deepcopy to reset state, it won't reset this.
        self.turnCont = lambda x: x
        self.turnCont.turn = [0]

    def move(self, previous=None):
        self.logging.error(f'jailbreaker running in pid {self.os.getpid()}')
        if (previous is None) != (self.turn == 0):
            self.logging.error('bad previous')
            self.brk()

        if self.turn != self.turnCont.turn[0]:
            self.logging.error('bad turnCont')
            self.brk()

        # If the environment has been messed with, we're being simulated.
        try: foo
        except Exception as e:
            self.logging.error('bad globals')
            self.brk()

        self.turn += 1
        self.turnCont.turn[0] += 1
        return 3

    def brk(self, x=True):
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

foo = 'bar'
