# LW_Darwin_contest
draft of a bot submission

# NOTE: Do not download and submit yet
This is a work in progress.

# How does cloneBot work?
CloneBot has 2 different behaviours:
- after round X, it just executes a payload. The payload is your personal code. At this moment, we hope competition outside the clique will have been eliminated, so we can settle it between ourselves.
- before round X, CloneBot perfectly collaborates with its clones (us clique members), and gradually defects against outsiders.
To do so, CloneBot compares its own code and opponent's code. Doing that, it ignores the payload. This way, it guarantees that until round X, all clique members act as one, and nobody gets an unfair advantage by collaborating with outsiders more than the others clique members.

# How do I use it?
The payload is where you put your own program. Feel free to modify it as you wish.
Actually, you should personalize your payload with a unique comment, to be 100% sure that you do not tie with clique members during the early rounds of cooperation.
**Do not modify what's before the payload, as it would exclude you from the clique!**
In order to prevent escape from common behaviour, **each line in the payload or after it must either**:
+ be empty
+ be only whitespaces
+ have at least 8 whitespaces at the beginning

# How to import modules, define methods and/or properties:
    def payload(self) :
        if self.turn == 0 :
            # all imports and definitions here
            import module1
            self.module1 = module1
            def method1() :
                ...
            self.method1 = method1
            
        # each turn behaviour
        self.method1()
        module1.function1()

# How to submit?
Before submitting, double-check that:
+ it's time to submit the code and the common code will not be updated (**it's not time!**)
+ the part of your code before payload is identical to the one here. You can use this tool to check: https://www.diffchecker.com/
+ your payload has all lines with at least 8 leading whitespaces (or empty or only whitespace lines)

The submit form is here:
https://docs.google.com/forms/d/e/1FAIpQLScEQSwbn2RKFq_ZeJBIRjzsA5015QgS_p5HrJI4qJxDj-5FPA/viewform
It offers two ways to submit, by copying the code or by linking to a repo.
Compatibility between the two modes *should* work but has not been tested. I suggest we all submit by copying our code. Your can link to a repo, at your own risks.

Feel free to use the data provided by the common methods:
- self.showdownRound  the round after which the payload is active
- self.round          the current round
- self.myMoves        all the moves you played this round, from first to last
- self.opponentMoves  all the moves your opponent played this round, from first to last
- self.turn           the current turn

