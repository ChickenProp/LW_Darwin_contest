# LW_Darwin_contest
draft of a bot submission


# How does cloneBot work?
CloneBot has 2 different behaviours:
- after round X, it just executes a payload. The payload is your personal code. At this moment, we hope competition outside the clique will have been eliminated, so we can settle it between ourselves.
- before round X, CloneBot perfectly collaborates with its clones (us clique members), and gradually defects against outsiders.
To do so, CloneBot compares its own code and opponent's code. Doing that, it ignores the payload. This way, it guarantees that until round X, all clique members act as one, and nobody gets an unfair advantage by collaborating with outsiders more than the others clique members.

# How do I use it?
The payload is where you put your own program. Feel free to modify it as you wish.
Actually, you should personalize your payload with a unique comment, to be 100% sure that you do not tie with clique members during the early rounds of cooperation.
**Do not modify the rest, as it would exclude you from the clique!**
Feel free to use the data provided by the common methods:
- self.showdownRound  the round after which the payload is active
- self.round          the current round
- self.myMoves        all the moves you played this round, from first to last
- self.opponentMoves  all the moves your opponent played this round, from first to last
- self.turn           the current turn

