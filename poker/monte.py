import random
from random import randrange
from treys import Card
from treys import Deck
from treys import Evaluator

def monteCarlo(board, hand, numPlayers, monteN):
    deck = Deck()
    evaluator = Evaluator()
    playerHands = [None]*numPlayers
    winAmount = 0 
    board_backup = board.copy()
    for time in range(int(monteN)):
        board = board_backup.copy()
        monteDeck = [card for card in deck.cards if card not in board and card not in hand]
        for x in range(numPlayers):
            playerHands[x] = []
            for y in range(2):
                randomIndex = randrange(0, len(monteDeck))
                playerHands[x].append(monteDeck[randomIndex])
                del monteDeck[randomIndex]
        while len(board) < 5:
            randomIndex = randrange(0, len(monteDeck))
            board.append(monteDeck[randomIndex])
            del monteDeck[randomIndex]
        win = True
        
        handRank = evaluator.evaluate(board, hand)
        for x in range(numPlayers):
            otherRank = evaluator.evaluate(board, playerHands[x])
            if otherRank < handRank:
                win = False
                break
        if win:
            winAmount += 1
    return winAmount/monteN
