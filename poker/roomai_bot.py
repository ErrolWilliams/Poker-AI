"""
for _ in range(games)
    # Do action
    # infos, public_state ... = env.step(action)
    
    # All actions saved to Data.txt

    # calculate state_score here and save to .txt?

    # Before an action happens, record the state for the action
    # Filter by player to get all state_score and action sequence for a player
    # [score, score, score, score]
    # [action, action, action, action]

    # score[0] -> action[0] -> score[1]
    # since we can have multiple players, we can have multiple agents and collect data on all of them

    # filter by highest scores
    # train network: given state "do" action that resulted in the greatest improvements in score.

    score formula: ((pot*odds)-my_stake + (1-odds)*num_player*player_fold

"""
from treys import Card
import poker.ai
import roomai
#----------------------------------------------------------------
class RoomAIBot(roomai.common.AbstractPlayer):
    def __init__(self):
        self.ai = ai.AI()

    def receive_info(self, infos, public_state):
        text = open("P1.txt", "a")
        self.avalible_actions = info.person_state.avalible_actions
        id = info.person_state.id       # my player id
        pot = sum (public_state.bets)   # the pot value
        bets = public_state.bets        # each player's bets
        chips = public_state.chips      # each player's chips
        my_hand = infos.person_state.hand_cards # my hand
        community = public_state.public_cards   # community cards
        my_stake = bets[id]             # amount this player has put into the pot
        my_chips = chips[id]            # my chips
        num_player = len (public_state.chips)   # number of players
        num_folded = sum (public_state.isfolds) # number of players who have folded
        #my_odds = somefunction(hole, community, num_player)    # my odds of winning with current cards
        my_score = ((pot*odds)-my_stake) + (1-odds)*num_player*num_folded  # numerical score of the current state of the game

        text.write("Public State: \r\n"                     \
                   "Number of Players: " + str(num_player) +\
                   "Number of Folded:  " + str(num_folded) +\
                   "Chips:             " + str(chips) +     \
                   "Bets:              " + str(bets) +      \
                   "Pot:               " + str(pot) +       \
#                   "Community Cards:   %s\r\n"%("| ".join([c.key for c in community])) "\r\n" + \
                   "Private State: \r\n"                    \
                   "ID:                " + str(id) +        \
                   "My Chips:          " + str(my_chips) +    \
#                   "My Total Bet:      " + str(my_stake)    \
#                   "My Odds:           " + str(my_odds)     \
#                   "My Hand:           %s\r\n"%("| ".join([c.key for c in my_hand])) + "\r\n" + \
                   "State Score:       " + str(my_score)
           )
    def take_action():
        pass
        
    def reset():
		self.ai = AI()
        pass
        # code

def card_obj(cardname):
    return Card.new(cardname[0] + cardname[1].lower())
