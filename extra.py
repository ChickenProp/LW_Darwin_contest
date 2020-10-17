def get_my_source(caller) :
    if caller.__class__.__module__ == "cloneBot" :
        fileName = "cloneBot.py"
    else :
        fileName = "myBot.py"
    my_file = open(fileName, 'r')
    my_code = my_file.read()
    return my_code


def get_opponent_source(caller) :
    if caller.__class__.__module__ == "cloneBot" :
        fileName = "myBot.py"
    else :
        fileName = "cloneBot.py"
    my_file = open(fileName, 'r')
    my_code = my_file.read()
    return my_code


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


