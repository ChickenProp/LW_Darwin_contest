# this module does 2 things:
# emulate lsusr's extra module
# test your bot's compatibility with testCloneCompatibility()


# Replaced these with my own implementation, which is more general than the
# original.
bot1_source = ''
bot2_source = ''
bot1 = None

def get_opponent_source(me):
    if me.__class__ is bot1:
        return bot2_source
    else:
        return bot1_source

def get_my_source(me):
    if me.__class__ is bot1:
        return bot1_source
    else:
        return bot2_source

# to check that your bot will be recognized as clique member, do the following:
# in a folder, download cloneBot.py and extra.py (this file)
# copy your bot in a file called myBot.py in the same folder
# run this module
# execute testCloneCompatibility()
def testCloneCompatibility() :
    import cloneBot
    import myBot
    referenceBot = cloneBot.CloneBot()
    myBot = myBot.CloneBot()
    if referenceBot.is_opponent_clone :
        print("Reference bot successfully recognized your bot as a clone!\nYou're good to go.")
    else :
        print("Reference bot failed to recognize your bot as a clone.\nCheck that:\n  - all lines before the payload are identical to the reference\n  - all lines after the payload either are empty, only whitespaces, or start with at least 8 whitespaces")
    if myBot.is_opponent_clone :
        print("Your bot successfully recognized the reference bot as a clone.")
    else :
        print("Your bot failed to recognize the reference bot as a clone.\nThat... shouldn't have happened.")


