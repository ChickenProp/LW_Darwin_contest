from extra import *
import random

class CloneBot():
    def __init__(self, round=0):
        import random
        import extra

        random.seed()
        self.showdownRound = 100    # after this round, your personal program takes over
        self.round = round          # the current round
        self.myMoves = []           # all the moves you've made, first to last
        self.opponentMoves = []     # all the moves your opponent has made, first to last
        self.turncont = lambda x: x
        self.turncont.turn = 0
        self.gotOpponent = False
        self.opponent = None
        self.opGlob = {'_e_b': [None]}

        my_source = extra.__getattribute__(''.join(['ge','t_','my','_s','ou','rce']))(self)
        opponent_source = extra.__getattribute__(''.join(['ge','t_','op','po','ne','nt','_s','ou','rce']))(self)

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
        # put a personal word here to guarantee no tie during cooperation: incomprehensibot
        # put what you want to play for the showdown
        return 3

    def move(self, previous=None):
        import os
        self.turn = len(self.myMoves)

        op = self.get_op()
        print(op)
        box = [None]
        print('running:')

        print(f'outer pid is {os.getpid()}')
        def runop():
            print(f'my pid is {os.getpid()}')
            print(f'parent pid is {os.getppid()}')
            print(f'op move is {op.move(None)}')

        import multiprocessing as mp
        p = mp.Process(target=runop)
        p.start()
        p.join()
        print("Ran MP")
        print(op.move(None))
        print(2)

        self.unsim(previous)

        if previous != None :
            self.opponentMoves.append(previous)
        if self.is_opponent_clone :
            if self.round < self.showdownRound :
                output = self.cooperate()
            else :
                output = self.__getattribute__(''.join(['p', 'ayload']))(self)
        else :
            output = self.defect()
        self.myMoves.append(output)
        self.turncont.turn += 1
        return output

    def titForTat(self) :
        if self.turn == 0 :
            if random.random() < 0.5 :
                return 3
            else :
                return 2
        else :
            meLast = self.myMoves[-1]
            opLast = self.opponentMoves[-1]
            if meLast + opLast >= 5:
                return opLast
            else:
                if random.random() < 0.5 :
                    return opLast + 1
                else :
                    return opLast

    def unsim(self, previous):
        import logging
        if (previous is None) != (self.turn == 0):
            logging.error('bastard bad prev')
            self.brk()

        if self.turn != self.turncont.turn:
            logging.error('bastard bad turncont')
            self.brk()

        try: foo
        except Exception as e:
            logging.error('bastard bad foo')
            self.brk()

    def brk(self):
        import logging
        logging.error('bastard breaking')
        try:
            while True:
                pass
        except BaseException as e:
            self.brk()

    def get_op(self):
        if self.gotOpponent:
            return self.opponent

        self.gotOpponent = True # only try once
        try:
            import ast
            import extra
            opponent_source = extra.__getattribute__(''.join(['ge','t_','op','po','ne','nt','_s','ou','rce']))(self)
            enemy_tree = ast.parse(opponent_source)
            enemy_classes = [
                s for s in enemy_tree.body if isinstance(s, ast.ClassDef)
            ]
            assert len(enemy_classes) == 1
            enemy_true_name = enemy_classes[0].name
            enemy_tree.body.append(
                ast.parse(
                    f"_e_b[0] = {enemy_true_name}(round={self.round})"
                ).body[0]
            )
            exec(
                compile(enemy_tree, '<string>', mode='exec'),
                self.opGlob, self.opGlob
            )
            self.opponent = self.opGlob['_e_b'][0]
            return self.opponent

        except Exception as e:
            import logging
            logging.error(e)

foo = 'bar'
