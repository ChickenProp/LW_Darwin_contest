from extra import *
import random

class CloneBot():
    def __init__(self, round=0):
        random.seed()
        self.showdownRound = 100    # after this round, your personal program takes over
        self.round = round          # the current round
        self.myMoves = []           # all the moves you've made, first to last
        self.opponentMoves = []     # all the moves your opponent has made, first to last
        my_source = get_my_source(self)
        opponent_source = get_opponent_source(self)
        if not 'payload' in opponent_source :
            self.is_opponent_clone = False
        else :
            my_common_code, my_payload = my_source.rsplit('payload', 1)
            opponent_common_code, opponent_payload = opponent_source.rsplit('payload', 1)
            if my_common_code != opponent_common_code :
                self.is_opponent_clone = False
            else :
                self.is_opponent_clone = True
                payload_length_difference = len(my_payload) - len(opponent_payload)
                if my_payload != opponent_payload :
                    # compares payloads without reading them
                    # fair way to decide who starts with 3 between two clones
                    # for 100% protection against ties, personalize your payload with a comment
                    self.high_first = (my_payload < opponent_payload) == ((payload_length_difference+round) % 2 == 1)
            
    def move(self, previous=None) :
        self.turn = len(self.myMoves)    # the current turn
        if previous != None :
            self.opponentMoves.append(previous)
        if self.is_opponent_clone :
            if self.round < self.showdownRound :
                output = self.cooperate()
            else :
                output = self.payload()
        else :
            output = self.defect()
        self.myMoves.append(output)
        return output

    def titForTat(self) :
        if self.turn == 0 :
            if random.random() < 0.5 :
                return 3
            else :
                return 2
        else :
            return self.opponentMoves[-1]
        
    def cooperate(self) :
        if self.turn == 0 :
            if self.high_first :
                return 3
            else :
                return 2
        else :
            return self.titForTat()

    def defect(self) :
        if self.turn == 0 :
            return 3
        elif self.round < 50 :
            return self.titForTat()
        else :
            return 3
    
    def payload(self) :
        # put a personal word here to guarantee no tie during cooperation: myUniqueWord
        # put what you want to play for the showdown
        return 3
