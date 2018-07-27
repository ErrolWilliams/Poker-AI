import treys
from treys import Card, Deck, Evaluator
import time
import random
from random import shuffle as rshuffle

random.seed(time.time())

def odds(hand, board, num_players):
    my_hand = [Card.new(hand[0]), Card.new(hand[1])]
    remove_cards = [Card.new(hand[0]), Card.new(hand[1])]

    my_board = []
    
    for i in range(len(board)):
        my_board.append(Card.new(board[i]))
        remove_cards.append(Card.new(board[i]))

    my_deck = Deck()
    
    for i in range(len(remove_cards)):
        my_deck.cards.remove(remove_cards[i])
        
    my_players = [my_hand]
    evaluator = Evaluator()

    count = 0;
    for b in range(1000):
        deck = Deck()
        cards = my_deck.cards.copy()
        rshuffle(cards)
        deck.cards = cards

        players = my_players.copy()
        for j in range(num_players-1):
            players.append(deck.draw(2))

        board = my_board.copy()
        while len(board) < 5:
            board.append(deck.draw(1))

        if evaluator.hand_summary(board, players) == 0:
            count += 1
        
    return count/1000

#-------------------------------------------------------------
'''
start = time.time()

chance = odds(['As', 'Ad'], [], 10)
end = time.time()
print (end-start)
print("Pre-Flop Ace: " + str(chance))
'''
