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
        foo = 'bar'                 # line for benchmark tests

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
        # put a personal word here to guarantee no tie during cooperation: myUniqueWord
        # put what you want to play for the showdown
        # no line after 'def payload(self)' should have less than 8 whitespaces at the beginning,
        # unless it's an empty or only whitespace line
