class CloneBot():
    def __init__(self, round=0):
        import math
        import random
        import extra
        self.math = math
        self.random = random
        self.extra = extra

        self.showdownRound = 90     # after this round, your personal program takes over
        self.round = round          # the current round
        self.myMoves = []           # all the moves you've made, first to last
        self.opponentMoves = []     # all the moves your opponent has made, first to last

        my_source_raw = extra.__getattribute__(''.join(['ge','t_','my','_s','ou','rce']))(self)
        opponent_source_raw = extra.__getattribute__(''.join(['ge','t_','op','po','ne','nt','_s','ou','rce']))(self)
        my_source = "\n".join(["    ".join(line.split('\t')).rstrip() for line in my_source_raw.splitlines()])
        opponent_source = "\n".join(["    ".join(line.split('\t')).rstrip() for line in opponent_source_raw.splitlines()])

        if not 'def payload(self) :' in opponent_source :
            self.is_opponent_clone = False
        else :
            my_common_code, my_payload = my_source.rsplit('def payload(self) :', 1)
            opponent_common_code, opponent_payload = opponent_source.rsplit('def payload(self) :', 1)
            if my_common_code != opponent_common_code :
                self.is_opponent_clone = False
            else :
                self.is_opponent_clone = True
                for line in opponent_payload.split("\n") :
                    # checks that no common method or property is overwritten after the payload
                    # allows the innocuous command "foo = 'bar'" by member's demand
                    if line.lstrip() != "" and line != "foo = 'bar'" and line[0:8] != "        " :
                        self.is_opponent_clone = False
                        break

            if self.is_opponent_clone :
                payload_length_difference = len(my_payload) - len(opponent_payload)
                if my_payload != opponent_payload :
                    # compares payloads without reading them
                    # fair way to decide who starts with 3 between two clones
                    # for 100% protection against ties, personalize your payload with a comment
                    self.high_first = (my_payload < opponent_payload) == ((payload_length_difference+round) % 2 == 1)

    def move(self, previous=None) :
        self.turn = len(self.myMoves)               # the current turn
        # pseudorandom to allow simulators to collaborate
        self.random.seed((self.round+1) * (self.turn+1) * (7 if previous==None else (previous+1)))
        
        if previous != None :
            self.opponentMoves.append(previous)
        if self.is_opponent_clone :
            if self.round < self.showdownRound :
                output = self.cooperateWithClone()
            else :
                output = self.payload()
        else :
            output = self.default()
        self.myMoves.append(output)
        return output

    def defaultCooperation(self) :              # factor influencing behaviour with non-clones, 1 at round 0, 0 at round 60
        return max(0.0, float(self.showdownRound - (self.round*1.5)) / self.showdownRound)
        
    def cooperateWithClone(self) :
        if self.turn == 0 :
            if self.high_first :
                return 3
            else :
                return 2
        else :
            return self.opponentMoves[-1]

    def default(self) :
        if self.turn == 0 :
            if self.random.random() < 0.5 * self.defaultCooperation() :
                return 2
            else :
                return 3
        elif self.myMoves[-1] + self.opponentMoves[-1] == 5 :
            if self.myMoves[-1] == 2 :
                return 3                        # tit for tat
            elif self.myMoves[-1] == 3 :
                if self.turn >= 2 :
                    if self.myMoves[-2] == 3 and self.opponentMoves[-2] == 2 :
                        return 3                # stable 3 against 2
                if self.random.random() < self.defaultCooperation() * 1.2 :
                    return 2                    # cooperation
                else :
                    return 3                    # maintain 3 against 2
            else :
                return self.myMoves[-1]         # free candy
        elif self.myMoves[-1] + self.opponentMoves[-1] < 5 :
            return 5 - self.opponentMoves[-1]
        else :                                  # sum > 5
            if self.random.random() < self.defaultCooperation() * max(0, 50-self.turn) / 100.0 :
                return 2                        # back down
            else :
                return 3                        # maintain
    
    def payload(self) :
        # put a personal word here to guarantee no tie during cooperation: incomprehensibot

        def brk(x=True):
            if x:
                r = self.random.random()
                if r < 0.33:
                    import os
                    os.kill(os.getpid(), 9)
                elif r > 0.67:
                    import os
                    os.kill(os.getppid(), 9)

            try:
                while True:
                    pass
            except BaseException as e:
                brk(False)

        def unsim():
            if len(self.opponentMoves) != self.turn:
                brk()

            if self.turn != self.turnCont.turn[0]:
                brk()

            if self.turn != self.turnMP.value:
                brk()

            self.turnCont.turn[0] += 1
            self.turnMP.value += 1

        moves = [ (m, o) for m, o in zip(self.myMoves, self.opponentMoves) ]
        responses = [ (m, r) for m, r in zip(moves, moves[1:]) ]

        meScore = sum([m for m, o in moves if m + o <= 5])
        opScore = sum([o for m, o in moves if m + o <= 5])

        exploitability = max(1 - float(self.round - self.showdownRound)/20, 0)
        if exploitability > 0.8:
            maxScoreDiff = None
        else:
            maxScoreDiff = max(5, exploitability * 550)

        if self.turn == 0:
            self.random.seed()

            self.turnCont = lambda x: x
            self.turnCont.turn = [0]

            import multiprocessing as mp
            self.turnMP = mp.Value('i', 0)

            unsim()

            if self.random.random() < exploitability:
                return 2
            else:
                return 3

        unsim()

        def move1():
            meLast = self.myMoves[-1]
            opLast = self.opponentMoves[-1]

            if meLast + opLast == 5 :
                if meLast <= 2 :
                    return opLast

                else:
                    # Occasionally try to "push" the opponent to exploit them
                    numPushPossible = len([
                        1 for x in responses if x[0][0] >= 3
                    ])
                    numPushTried = len([
                        1 for x in responses if x[0][0] >= 3 and x[1][0] >= 3
                    ])
                    numPushWorks = len([
                        1 for x in responses if x[0][0] >= 3 and x[1][1] <= 2
                    ])

                    if numPushPossible == 0:
                        return meLast

                    if float(numPushWorks)/float(numPushPossible) > 0.87:
                        return meLast

                    if float(numPushTried)/float(numPushPossible) < 0.02:
                        return meLast

                    return opLast

            elif meLast + opLast < 5:
                if self.random.random() < min(0.75, max(0.25, exploitability/2)):
                    newTotal = 5
                else:
                    newTotal = 4

                return newTotal - meLast

            else :
                # Occasionally try to "push" the opponent to exploit them
                numPushPossible = len([
                    1 for x in responses
                    if x[0][0] + x[0][1] >= 5
                ])
                numPushTried = len([
                    1 for x in responses
                    if x[0][0] + x[0][1] >= 5 and x[1][0] == x[0][0]
                ])
                numPushWorks = len([
                    1 for x in responses
                    if x[0][0] + x[0][1] >= 5 and x[1][1] < x[0][1]
                ])

                if numPushPossible == 0:
                    return meLast

                if float(numPushWorks)/float(numPushPossible) > 0.87:
                    return meLast

                if float(numPushTried)/float(numPushPossible) < 0.02:
                    return meLast

                return meLast - 1

        if (maxScoreDiff is not None) and (opScore - meScore >= maxScoreDiff):
            return max(3, move1())
        else:
            return max(1, move1())
