import treys
from treys import Card, Deck, Evaluator
import time
import random
from random import shuffle as rshuffle

random.seed(time.time())


def odds(hand, board, num_players):
    my_hand = hand
    print("HAND: " + str(my_hand))
    remove_cards = hand

    my_board = board
    
    for i in range(len(board)):
        remove_cards.append(board[i])

    my_deck = Deck()
    
    for i in range(len(remove_cards)):
        my_deck.cards.remove(remove_cards[i])
        
    my_players = [my_hand]
    evaluator = Evaluator()

    count = 0;
    for b in range(2000):
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

        print(f"BOARD: {board}\nPLAYERS: {players}")

        if evaluator.hand_summary(board, players) == 0:
            count += 1
        
    return count/2000.0

#-------------------------------------------------------------
if __name__ == "__main__":
    start = time.time()

    chance = odds(['As', 'Ad'], [], 10)
    end = time.time()
    print (end-start)
    print("Pre-Flop Ace: " + str(chance))
