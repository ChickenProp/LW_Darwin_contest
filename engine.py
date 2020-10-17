import sys

import cloneBot
import incomprehensibot
import abstract_spy_tree_bot
import jailer
import jailbreaker

import extra

bots = \
    { 'clone': (cloneBot.CloneBot, 'cloneBot.py')
    , 'incomprehensibot': (incomprehensibot.CloneBot, 'incomprehensibot.py')
    , 'ast': (abstract_spy_tree_bot.AbstractSpyTreeBot, 'abstract_spy_tree_bot.py')
    , 'jailer': (jailer.Jailer, 'jailer.py')
    , 'jailbreaker': (jailbreaker.JailBreaker, 'jailbreaker.py')
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
        print('ENGINE: running bot 1')
        setup_extra(meClass, meSource, opSource)
        meTurn = meBot.move(opPrev)

        print('ENGINE: running bot 2')
        setup_extra(opClass, opSource, meSource)
        opTurn = opBot.move(mePrev)

        mePrev = meTurn
        opPrev = opTurn
        if meTurn + opTurn <= 5:
            meScore += meTurn
            opScore += opTurn
        print(f'Turn {turn}. Play {meTurn} - {opTurn}. Scores {meScore} - {opScore}')

if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
