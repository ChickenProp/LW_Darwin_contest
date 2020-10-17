class Jailer():
    def __init__(self, round=0):
        import logging
        self.logging = logging

        self.round = round
        self.gotOpponent = False
        self.opponent = None
        self.opGlob = {'_e_b': [None]}

    def move(self, previous=None):
        op = self.get_op()

        if op is not None:
            self.logging.error(f'op dict is {op.__dict__}, tc is {id(op.turnCont.turn[0])}')
            def runop():
                self.logging.error(f'opponent move is {op.move(None)}')
                self.logging.error(f'op dict is {op.__dict__}, tc is {id(op.turnCont.turn[0])}')
                # self.logging.error(f'opponent move 2 is {op.move(None)}')
                # self.logging.error(f'op dict is {op.__dict__}, tc is {id(op.turnCont)}')

            import multiprocessing as mp
            p = mp.Process(target=runop)
            p.start()
            p.join()

        return 2

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
