import random
from random import randrange
from treys import Card
from treys import Deck
from treys import Evaluator

def monteCarlo(board, hand, numPlayers, monteN):
    deck = Deck()
    evaluator = Evaluator()
    handRank = evaluator.evaluate(board, hand)
    playerHands = [None]*numPlayers
    winAmount = 0 
    for time in range(int(monteN)):
        monteDeck = [card for card in deck.cards if card not in board and card not in hand]
        win = True
        for x in range(numPlayers):
            playerHands[x] = []
            for y in range(2):
                randomIndex = randrange(0, len(monteDeck))
                playerHands[x].append(monteDeck[randomIndex])
                del monteDeck[randomIndex]
            otherRank = evaluator.evaluate(board, playerHands[x])
            if otherRank < handRank:
                win = False
                break
        if win:
            winAmount += 1
    return winAmount/monteN
