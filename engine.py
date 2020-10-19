import sys

import cloneBot
import incomprehensibot
import abstract_spy_tree_bot
import jailer
import jailbreaker
import simple
import payload

import extra

bots = \
    { 'clone': (cloneBot.CloneBot, 'cloneBot.py')
    , 'incomprehensibot': (incomprehensibot.CloneBot, 'incomprehensibot.py')
    , 'payload': (payload.PayloadBot, 'payload.py')
    , 'ast': (abstract_spy_tree_bot.AbstractSpyTreeBot, 'abstract_spy_tree_bot.py')
    , 'jailer': (jailer.Jailer, 'jailer.py')
    , 'jailbreaker': (jailbreaker.JailBreaker, 'jailbreaker.py')
    , '0': (simple.ConstBot0, 'simple.py')
    , '1': (simple.ConstBot1, 'simple.py')
    , '2': (simple.ConstBot2, 'simple.py')
    , '3': (simple.ConstBot3, 'simple.py')
    , '4': (simple.ConstBot4, 'simple.py')
    , '5': (simple.ConstBot5, 'simple.py')
    , 'tft': (simple.SimpleTFTBot, 'simple.py')
    , 'random': (simple.RandomBot, 'simple.py')
    , 'ast-fallback': (simple.ASTFallbackBot, 'simple.py')
    }

def setup_extra(bot1, bot1_source, bot2_source):
    extra.bot1 = bot1
    extra.bot1_source = bot1_source
    extra.bot2_source = bot2_source

def main(round, me, op):
    meClass, meFile = bots[me]
    opClass, opFile = bots[op]

    meSource = open(meFile).read()
    opSource = open(opFile).read()

    setup_extra(meClass, meSource, opSource)
    meBot = meClass(round)

    setup_extra(opClass, opSource, meSource)
    opBot = opClass(round)

    mePrev = None
    meScore = 0
    opPrev = None
    opScore = 0
    for turn in range(1, 151):
        # print('ENGINE: running bot 1')
        setup_extra(meClass, meSource, opSource)
        meTurn = meBot.move(opPrev)

        # print('ENGINE: running bot 2')
        setup_extra(opClass, opSource, meSource)
        opTurn = opBot.move(mePrev)

        mePrev = meTurn
        opPrev = opTurn
        if meTurn + opTurn <= 5:
            meScore += meTurn
            opScore += opTurn
        print(f'Turn {turn}. Play {meTurn} - {opTurn}. Scores {meScore} - {opScore}')

def test_compat():
    meClass, meFile = bots['clone']
    opClass, opFile = bots['incomprehensibot']

    meSource = open(meFile).read()
    opSource = open(opFile).read()

    setup_extra(meClass, meSource, opSource)
    extra.testCloneCompatibility(meClass, opClass)

if __name__ == '__main__':
    if sys.argv[1] == '-t':
        test_compat()
    else:
        main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
