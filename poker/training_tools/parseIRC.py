import os
import re
import random
from random import randrange
from treys import Card
from treys import Deck
from treys import Evaluator
import json

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


def makeNewRound(players, roundNum):
    round = {}
    round['eventName'] = '__new_round'
    round['data'] = {}
    round['data']['table'] = {}
    round['data']['table']['tableNumber'] = roundNum
    round['data']['table']['roundName'] = 'Deal'
    round['data']['table']['board'] = []
    round['data']['table']['roundCount'] = 1
    round['data']['table']['raiseCount'] = 0
    round['data']['table']['betCount'] = 0
    round['data']['table']['smallBlind'] = {}
    round['data']['table']['bigBlind'] = {}
    blindPlayers = []
    for player in players:
        if 'B' in player['preFlopActions']:
            blindPlayers.append(player)
    if len(blindPlayers) == 2:
        if abs(blindPlayers[0]['position'] - blindPlayers[1]['position']) == 1:
            if blindPlayers[0]['position'] < blindPlayers[1]['position']:
                round['data']['table']['smallBlind']['playerName'] = blindPlayers[0][
                    'playerName']  # players[0] has smallBlind
                round['data']['table']['bigBlind']['playerName'] = blindPlayers[1]['playerName']
            else:
                round['data']['table']['smallBlind']['playerName'] = blindPlayers[1][
                    'playerName']  # players[0] has bigBlind
                round['data']['table']['bigBlind']['playerName'] = blindPlayers[0]['playerName']
        else:
            if blindPlayers[0]['position'] < blindPlayers[1]['position']:
                round['data']['table']['smallBlind']['playerName'] = blindPlayers[1][
                    'playerName']  # players[0] has bigBlind
                round['data']['table']['bigBlind']['playerName'] = blindPlayers[0]['playerName']
            else:
                round['data']['table']['smallBlind']['playerName'] = blindPlayers[0][
                    'playerName']  # players[0] has smallBlind
                round['data']['table']['bigBlind']['playerName'] = blindPlayers[1]['playerName']
    else:
        raise ValueError('Not enough information about blinds to use this round')
    round['data']['table']['smallBlind']['amount'] = 10
    round['data']['table']['bigBlind']['amount'] = 20
    round['data']['players'] = players
    return round


def makeShowAction(action, playerName, amount, chips, table, turn, board, raiseCount, betCount, totalBet, smallBlind,
                   bigBlind, players):
    showAction = {}
    showAction['eventName'] = '__show_action'
    showAction['data'] = {}
    showAction['data']['action'] = {}
    if action == 'b':
        showAction['data']['action']['action'] = 'bet'
    elif action == 'c':
        showAction['data']['action']['action'] = 'call'
    elif action == 'f':
        showAction['data']['action']['action'] = 'fold'
    elif action == 'k':
        showAction['data']['action']['action'] = 'check'
    elif action == 'r':
        showAction['data']['action']['action'] = 'raise'
    showAction['data']['action']['playerName'] = playerName
    showAction['data']['action']['amount'] = amount
    showAction['data']['action']['chips'] = chips
    showAction['data']['table'] = table
    showAction['data']['table']['roundName'] = turn
    showAction['data']['table']['board'] = board
    showAction['data']['table']['raiseCount'] = raiseCount
    showAction['data']['table']['betCount'] = betCount
    showAction['data']['table']['totalBet'] = totalBet
    showAction['data']['table']['smallBlind'] = smallBlind
    showAction['data']['table']['bigBlind'] = bigBlind
    showAction['data']['players'] = players
    return showAction


def makeRequestAction(player, activeBet, table, roundBet, smallBlind, bigBlind, board, betCount, turn, players):
    requestAction = {}
    requestAction['eventName'] = '__action'
    if activeBet:
        requestAction['eventName'] = '__bet'
    requestAction['data'] = {}
    requestAction['data']['tableNumber'] = table['tableNumber']
    requestAction['data']['self'] = {}
    requestAction['data']['self']['playerName'] = player['playerName']
    requestAction['data']['self']['chips'] = player['chips']
    requestAction['data']['self']['folded'] = False
    requestAction['data']['self']['allIn'] = False
    requestAction['data']['self']['cards'] = player['cards']
    requestAction['data']['self']['isSurvive'] = True
    requestAction['data']['self']['roundBet'] = player['roundBet']
    if activeBet:
        requestAction['data']['self']['bet'] = roundBet
    requestAction['data']['self']['minBet'] = 50
    requestAction['data']['game'] = {}
    requestAction['data']['game']['smallBlind'] = smallBlind
    requestAction['data']['game']['bigBlind'] = bigBlind
    requestAction['data']['game']['board'] = board
    requestAction['data']['game']['betCount'] = betCount
    requestAction['data']['game']['roundName'] = turn
    requestAction['data']['game']['players'] = players
    return requestAction


def makeGoodResponse(win, action, activeBet, amount, turn):
    response = {}
    response['eventName'] = '__action'
    if win:
        if action == 'b':
            response['action'] = 'bet'
            data = 'b'
        elif action == 'c':
            response['action'] = 'call'
            data = 'c'
        elif action == 'k':
            response['action'] = 'check'
            data = 'k'
        elif action == 'r':
            response['action'] = 'raise'
            data = 'r'
        if activeBet:
            response['amount'] = amount
    else:
        if activeBet:
            if turn == 'preFlop':
                response['action'] = 'call'
                data = 'c'
            else:
                response['action'] = 'fold'
                data = 'f'
        else:
            response['action'] = 'check'
            data = 'k'
    return response, data


def getRoundBettingActions(firstIndex, players, myPlayer, table, turn, board, smallBlind, bigBlind, pot, odds):
    global dataFile
    bettingRoundActions = []
    myActions = []
    for player in players:
        player['turnBet'] = 0
        if 'B' in player['preFlopActions']:
            player['preFlopActions'] = player['preFlopActions'][1:]
    if turn == 'preFlop':
        roundNum = 0
    elif turn == 'flop':
        roundNum = 1
    elif turn == 'turn':
        roundNum = 2
    else:
        roundNum = 3
    raiseCount = 0
    betCount = 0
    activeBet = False
    betAmount = 0
    totalBet = 0
    if turn == 'preFlop':
        betAmount = 20
        totalBet = 30
        players[-1]['roundBet'] = 20
        players[-2]['roundBet'] = 10
    loops = 0
    betsDone = False
    playersToRemove = []
    numFold = 0
    while not betsDone:
        for curPlayer in players:
            if not curPlayer['folded'] and curPlayer['isSurvive']:
                if turn == 'preFlop':
                    nextAction = curPlayer['preFlopActions']
                elif turn == 'flop':
                    nextAction = curPlayer['flopActions']
                elif turn == 'turn':
                    nextAction = curPlayer['turnActions']
                else:
                    nextAction = curPlayer['riverActions']
                if len(nextAction) > loops:
                    nextAction = nextAction[loops:][0]
                else:
                    betsDone = True
                    break
                if nextAction == 'b':
                    if curPlayer['playerName'] != myPlayer:  # make __show_action for this event
                        betCount += 1
                        betAmount += 50
                        totalBet += 50
                        pot += 50
                        curPlayer['roundBet'] += betAmount
                        curPlayer['turnBet'] += betAmount
                        curPlayer['chips'] -= betAmount
                        bettingRoundActions.append(
                            makeShowAction('b', curPlayer['playerName'], 50, curPlayer['chips'], table, turn, board,
                                           raiseCount, betCount, totalBet, smallBlind, bigBlind, players))
                        activeBet = True
                    else:  # make __send_action for this event
                        bettingRoundActions.append(
                            makeRequestAction(curPlayer, activeBet, table, betAmount, smallBlind, bigBlind, board,
                                              betCount, turn, players))
                        myResponse,shortResponse = makeGoodResponse(curPlayer['win'], 'b', activeBet, betAmount, turn)
                        myActions.append(myResponse)
                        potPercent = pot / (500.0 * (len(players) - len(playersToRemove)))
                        numPlayers = len(players) - len(playersToRemove) 
                        dataFile.write('{0},{1},{2},{3},{4},{5}\n'.format(float(potPercent), float(curPlayer['roundBet']/500.0), float(odds), numPlayers, roundNum, shortResponse))
                        betCount += 1
                        betAmount += 50
                        totalBet += 50
                        pot += 50
                        curPlayer['roundBet'] += betAmount
                        curPlayer['turnBet'] += betAmount
                        curPlayer['chips'] -= betAmount
                        activeBet = False
                elif nextAction == 'c':
                    totalBet += (betAmount - curPlayer['turnBet'])
                    curPlayer['chips'] -= (betAmount - curPlayer['turnBet'])
                    curPlayer['roundBet'] += (betAmount - curPlayer['turnBet'])
                    pot += (betAmount - curPlayer['turnBet'])
                    curPlayer['turnBet'] = betAmount
                    if curPlayer['playerName'] != myPlayer:  # make __show_action for this event
                        bettingRoundActions.append(
                            makeShowAction('c', curPlayer['playerName'], 0, curPlayer['chips'], table, turn, board,
                                           raiseCount, betCount, totalBet, smallBlind, bigBlind, players))
                        activeBet = True
                    else:
                        bettingRoundActions.append(makeRequestAction(curPlayer, activeBet, table, betAmount, smallBlind,
                                                                     bigBlind, board, betCount, turn, players))
                        myResponse, shortResponse = makeGoodResponse(curPlayer['win'], 'c', activeBet, betAmount, turn)
                        myActions.append(myResponse)
                        potPercent = pot / (500.0 * (len(players) - len(playersToRemove)))
                        numPlayers = len(players) - len(playersToRemove) 
                        dataFile.write('{0},{1},{2},{3},{4},{5}\n'.format(float(potPercent), float(curPlayer['roundBet']/500.0), float(odds), numPlayers, roundNum, shortResponse))
                        activeBet = False
                elif nextAction == 'f':
                    curPlayer['folded'] = True
                    numFold += 1
                    playersToRemove.append(curPlayer['playerName'])
                    if curPlayer['playerName'] != myPlayer:  # make __show_action for this event
                        bettingRoundActions.append(
                            makeShowAction('f', curPlayer['playerName'], 0, curPlayer['chips'], table, turn, board,
                                           raiseCount, betCount, totalBet, smallBlind, bigBlind, players))
                elif nextAction == 'k':
                    if curPlayer['playerName'] != myPlayer:  # make __show_action for this event
                        bettingRoundActions.append(
                            makeShowAction('k', curPlayer['playerName'], 0, curPlayer['chips'], table, turn, board,
                                           raiseCount, betCount, totalBet, smallBlind, bigBlind, players))
                    else:
                        bettingRoundActions.append(
                            makeRequestAction(curPlayer, activeBet, table, betAmount, smallBlind, bigBlind, board,
                                              betCount,
                                              turn, players))
                        myResponse, shortResponse = makeGoodResponse(curPlayer['win'], 'k', activeBet, betAmount, turn)
                        myActions.append(myResponse)
                        potPercent = pot / (500.0 * (len(players) - len(playersToRemove)))
                        numPlayers = len(players) - len(playersToRemove)
                        dataFile.write('{0},{1},{2},{3},{4},{5}\n'.format(float(potPercent), float(curPlayer['roundBet']/500.0), float(odds), numPlayers, roundNum, shortResponse))
                elif nextAction == 'r':
                    if curPlayer['playerName'] != myPlayer:  # make __show_action for this event
                        betCount += 1
                        totalBet += (50 + betAmount)
                        betAmount += 50
                        pot += 50
                        curPlayer['chips'] -= betAmount
                        curPlayer['roundBet'] += betAmount
                        curPlayer['turnBet'] += betAmount
                        bettingRoundActions.append(
                            makeShowAction('r', curPlayer['playerName'], 50, curPlayer['chips'], table, turn, board,
                                           raiseCount, betCount, totalBet, smallBlind, bigBlind, players))
                        activeBet = True
                    else:
                        bettingRoundActions.append(
                            makeRequestAction(curPlayer, activeBet, table, betAmount, smallBlind, bigBlind, board,
                                              betCount,
                                              turn, players))
                        myResponse, shortResponse = makeGoodResponse(curPlayer['win'], 'r', activeBet, betAmount, turn)
                        myActions.append(myResponse)
                        potPercent = pot / (500.0 * (len(players) - len(playersToRemove)))
                        numPlayers = len(players) - len(playersToRemove)
                        dataFile.write('{0},{1},{2},{3},{4},{5}\n'.format(float(potPercent), float(curPlayer['roundBet']/500.0), float(odds), numPlayers, roundNum, shortResponse))
                        betCount += 1
                        totalBet += (50 + betAmount)
                        betAmount += 50
                        pot += 50
                        curPlayer['chips'] -= betAmount
                        curPlayer['roundBet'] += betAmount
                        curPlayer['turnBet'] += betAmount
                        activeBet = False
                else:
                    curPlayer['isSurvive'] = False
                    playersToRemove.append(curPlayer['playerName'])
                    numFold += 1
        loops += 1
    return bettingRoundActions, myActions, numFold, betAmount


def makeBettingEvents(players, latePlayer, myPlayer, turn, table, board, smallBlind, bigBlind, pot, odds):
    orderedPlayers = [None] * len(players)
    numPlayers = len(players)
    for player in players:
        orderedPlayers[player['position'] - 1] = player
        if player['playerName'] == latePlayer:
            firstPosition = player['position']
            if turn == 'preFlop':
                firstPosition += 1
            if firstPosition > numPlayers:
                firstPosition = firstPosition % numPlayers
    pokerOrderedPlayers = []
    for i in range(0, len(players)):
        roundPos = (firstPosition + i - 1) % len(players)
        pokerOrderedPlayers.append(orderedPlayers[roundPos])
    bettingEvents, bettingActions, numFold, totalBet = getRoundBettingActions(firstPosition - 1, pokerOrderedPlayers, myPlayer, table,
                                                           turn, board, smallBlind, bigBlind, pot, odds)
    return bettingEvents, bettingActions, numFold, totalBet


def makeDealEvent(players, table):
    deal = {}
    deal['eventName'] = '__deal'
    deal['data'] = {}
    deal['data']['players'] = players
    deal['data']['table'] = table
    return deal


def makeRoundEvents(playerEvents, roundNum, myPlayer, flop, turn, river):
    try:
        newRound = makeNewRound(playerEvents[roundNum]['players'], roundNum)
    except ValueError as e:
        raise ValueError('Unable to create events for this round')
    me = [me for me in playerEvents[roundNum]['players'] if me['playerName'] == myPlayer]
    hand = []
    board = []
    for card in me[0]['cards']:
        hand.append(Card.new(card))
    pot = 0
    numPlayers = len(playerEvents[roundNum]['players'])
    preFlopBettingEvents = []
    preFlopBettingEvents.append(newRound)
    preFlopBettingEvents2, preFlopResponses, preFlopfold, preFlopBet = makeBettingEvents(newRound['data']['players'],
                                                                newRound['data']['table']['bigBlind']['playerName'],
                                                                myPlayer, 'preFlop',
                                                                newRound['data']['table'], newRound['data']['table']['board'],
                                                                newRound['data']['table']['smallBlind'],
                                                                newRound['data']['table']['bigBlind'], pot, 0.5)
    pot += preFlopBet
    numPlayers -= preFlopfold
    for event in preFlopBettingEvents2:
        preFlopBettingEvents.append(event)
    if flop != ' ':
        for card in flop:
            board.append(Card.new(card))
            newRound['data']['table']['board'].append(card)
            newRound['data']['table']['roundName'] = 'Flop'
        flopOdds = monteCarlo(board, hand, numPlayers-1, 2000.0)
        flopBettingEvents = []
        flopBettingEvents.append(makeDealEvent(newRound['data']['players'], newRound['data']['table']))
        flopBettingEvents2, flopResponses, flopFold, flopBet = makeBettingEvents(newRound['data']['players'],
                                                             newRound['data']['table']['smallBlind']['playerName'],
                                                             myPlayer, 'flop',
                                                             newRound['data']['table'], newRound['data']['table']['board'],
                                                             newRound['data']['table']['smallBlind'],
                                                             newRound['data']['table']['bigBlind'], pot, flopOdds)
        pot += flopBet
        numPlayers -= flopFold
        for event in flopBettingEvents2:
            flopBettingEvents.append(event)
        if turn != ' ':
            newRound['data']['table']['board'].append(turn)
            board.append(Card.new(turn))
            turnOdds = monteCarlo(board, hand, numPlayers - 1, 2000.0)
            newRound['data']['table']['roundName'] = 'Turn'
            turnBettingEvents = []
            turnBettingEvents.append(makeDealEvent(newRound['data']['players'], newRound['data']['table']))
            turnBettingEvents2, turnResponses, turnFold, turnBet = makeBettingEvents(newRound['data']['players'],
                                                                 newRound['data']['table']['smallBlind']['playerName'],
                                                                 myPlayer,
                                                                 'turn', newRound['data']['table'], newRound['data']['table']['board'],
                                                                 newRound['data']['table']['smallBlind'],
                                                                 newRound['data']['table']['bigBlind'], pot, turnOdds)
            pot += turnBet
            numPlayers -= turnFold
            for event in turnBettingEvents2:
                turnBettingEvents.append(event)
            if river != ' ':
                newRound['data']['table']['board'].append(river)
                board.append(Card.new(river))
                riverOdds = monteCarlo(board, hand, numPlayers - 1, 2000.0)
                newRound['data']['table']['roundName'] = 'River'
                riverBettingEvents = []
                riverBettingEvents.append(makeDealEvent(newRound['data']['players'], newRound['data']['table']))
                riverBettingEvents2, riverResponses, riverFold, riverBet = makeBettingEvents(newRound['data']['players'],
                                                                       newRound['data']['table']['smallBlind'][
                                                                           'playerName'], myPlayer,
                                                                       'river', newRound['data']['table'], newRound['data']['table']['board'],
                                                                       newRound['data']['table']['smallBlind'],
                                                                       newRound['data']['table']['bigBlind'], pot, riverOdds)
                pot += riverBet
                for event in riverBettingEvents2:
                    riverBettingEvents.append(event)
    return preFlopBettingEvents, preFlopResponses, preFlopfold, preFlopBet, flopBettingEvents, flopResponses, flopFold, flopBet, turnBettingEvents, turnResponses, turnFold, turnBet, riverBettingEvents, riverResponses, riverBet


def getAllPlayers(roundNum, numPlayers):
    for line in open('hroster'):
        if roundNum in line:
            players = re.sub('\s+', ',', line.strip()).split(',')[
                      2:]  # players contains a list of all players for this round
            if len(players) != int(numPlayers):
                print('Error: Unable to find {0} players for round number {1}'.format(numPlayers, roundNum))
                exit(1)
            return players


def getTrainingPlayers(roundNum, numPlayers):
    trainingPlayers = []
    players = getAllPlayers(roundNum, numPlayers)
    for player in players:
        for line in open('pdb/pdb.{0}'.format(player)):
            if roundNum in line:
                line = re.sub('\s+', ',', line.strip()).split(',')
                if len(line) > 11:
                    trainingPlayers.append(player)
                break
    return trainingPlayers


def getPlayerEvents(roundNum, numPlayers, trainingPlayer):
    playerEvents = {}
    playerEvents[roundNum] = {}  # makes new dictionary entry for this round
    players = getAllPlayers(roundNum, numPlayers)
    playerEvents[roundNum]['players'] = []
    for player in players:
        for line2 in open('pdb/pdb.{0}'.format(player)):
            if roundNum in line2:
                line2 = re.sub('\s+', ',', line2.strip()).split(',')
                thisPlayer = {}
                thisPlayer['playerName'] = player
                thisPlayer['chips'] = 500
                thisPlayer['folded'] = False
                thisPlayer['allIn'] = False
                thisPlayer['isSurvive'] = True
                thisPlayer['reloadCount'] = 0
                thisPlayer['roundBet'] = 0
                thisPlayer['bet'] = 0
                thisPlayer['cards'] = []
                if player == trainingPlayer:
                    thisPlayer['cards'] = [line2[11], line2[12]]
                    thisPlayer['win'] = False
                    if line2[10] != '0':
                        thisPlayer['win'] = True
                thisPlayer['winAmount'] = line2[10]
                thisPlayer['position'] = int(line2[3])
                thisPlayer['preFlopActions'] = line2[4]
                thisPlayer['flopActions'] = line2[5]
                thisPlayer['turnActions'] = line2[6]
                thisPlayer['riverActions'] = line2[7]
                if 'A' in thisPlayer['preFlopActions'] or 'A' in thisPlayer['flopActions'] or 'A' in thisPlayer[
                    'turnActions'] or 'A' in thisPlayer['riverActions']:
                    raise ValueError('Unable to process round where player went all in')
                playerEvents[roundNum]['players'].append(thisPlayer)
    return playerEvents


def getData(round, dataFile):
    roundNum = round[0]
    numPlayers = round[3]
    playerNum = int(numPlayers)
    flop = ''
    turn = ''
    river = ''
    if len(round) > 9:
        flop = [round[8], round[9], round[10]]
    if len(round) > 11:
        turn = round[11]
    if len(round) > 12:
        river = round[12]

    trainingPlayers = getTrainingPlayers(roundNum, numPlayers)
    for player in trainingPlayers:
        try:
            playerEvents = getPlayerEvents(roundNum, numPlayers, player)
            preFlopEvents, preFlopResponses, preFlopfold, preFlopBet, flopEvents, flopResponses, flopFold, flopBet, turnEvents, turnResponses, turnFold, turnBet, riverEvents, riverResponses, riverBet= makeRoundEvents(
                playerEvents, roundNum, player, flop, turn, river)

            """
            myPlayer = [me for me in playerEvents[roundNum]['players'] if me['playerName'] == player]
            pot = preFlopBet
            hand = []
            board = []
            for card in myPlayer[0]['cards']:
                hand.append(Card.new(card))
            """
            #preFlopData
            """
            responseNum = 0
            raiseCount = 0
            risk = 0
            monteOdds = 0.75
            for pfEvent in preFlopEvents:
                if pfEvent['eventName'] != '__show_action' and pfEvent['eventName'] != '__new_round' and pfEvent['eventName'] != '__deal':
                    response = '0'
                    if preFlopResponses[responseNum]['action'] == 'call':
                        response = '1'
                    elif preFlopResponses[responseNum]['action'] == 'check':
                        response = '2'
                    elif preFlopResponses[responseNum]['action'] == 'fold':
                        response = '3'
                    elif preFlopResponses[responseNum]['action'] == 'raise':
                        response = '4'
                    responseNum += 1
                else:
                    if pfEvent['eventName'] == '__show_action':
                        if pfEvent['data']['action']['action'] == 'raise':
                            raiseCount += 1
            risk = (1-monteOdds) * raiseCount
            round = 0.0
            dataFile.write('{0},{1},{2}\n'.format(round, risk, response))

            """
            #flopData
            """
            responseNum = 0
            playerNum -= preFlopfold
            for card in flop:
                board.append(Card.new(card))
            raiseCount = 0
            risk = 0
            monteOdds = monteCarlo(board, hand, playerNum-1, 2000.0)
            for pfEvent in flopEvents:
                if pfEvent['eventName'] != '__show_action' and pfEvent['eventName'] != '__new_round' and pfEvent[
                    'eventName'] != '__deal':
                    response = '0'
                    if flopResponses[responseNum]['action'] == 'call':
                        response = '1'
                    elif flopResponses[responseNum]['action'] == 'check':
                        response = '2'
                    elif flopResponses[responseNum]['action'] == 'fold':
                        if monteOdds == 1.0:
                            monteOdds = .5
                        response = '3'
                    elif flopResponses[responseNum]['action'] == 'raise':
                        response = '4'
                    responseNum += 1
                else:
                    if pfEvent['eventName'] == '__show_action':
                        if pfEvent['data']['action']['action'] == 'raise':
                            raiseCount += 1
                        elif pfEvent['data']['action']['action'] == 'bet':
                            raiseCount +=1
            risk = (1-monteOdds) * raiseCount

            round = 1.0
            dataFile.write('{0},{1},{2}\n'.format(round, risk, response))

            """
            #turnData
            """
            responseNum = 0
            playerNum -= flopFold
            board.append(Card.new(turn))
            raiseCount = 0
            risk = 0
            monteOdds = monteCarlo(board, hand, playerNum - 1, 2000.0)
            for pfEvent in turnEvents:
                if pfEvent['eventName'] != '__show_action' and pfEvent['eventName'] != '__new_round' and pfEvent[
                    'eventName'] != '__deal':
                    response = '0'
                    if turnResponses[responseNum]['action'] == 'call':
                        response = '1'
                    elif turnResponses[responseNum]['action'] == 'check':
                        response = '2'
                    elif turnResponses[responseNum]['action'] == 'fold':
                        if monteOdds == 1.0:
                            monteOdds = .5
                        response = '3'
                    elif turnResponses[responseNum]['action'] == 'raise':
                        response = '4'
                    responseNum += 1
                else:
                    if pfEvent['eventName'] == '__show_action':
                        if pfEvent['data']['action']['action'] == 'raise':
                            raiseCount += 1
                        elif pfEvent['data']['action']['action'] == 'bet':
                            raiseCount += 1
            risk = (1-monteOdds) * raiseCount
            round = 2.0
            dataFile.write('{0},{1},{2}\n'.format(round, risk, response))

            """
            #riverData
            """
            responseNum = 0
            playerNum -= turnFold
            board.append(Card.new(river))
            raiseCount = 0
            risk = 0
            monteOdds = monteCarlo(board, hand, playerNum - 1, 2000.0)
            for pfEvent in riverEvents:
                if pfEvent['eventName'] != '__show_action' and pfEvent['eventName'] != '__new_round' and pfEvent[
                    'eventName'] != '__deal':
                    response = '0'
                    if riverResponses[responseNum]['action'] == 'call':
                        response = '1'
                    elif riverResponses[responseNum]['action'] == 'check':
                        response = '2'
                    elif riverResponses[responseNum]['action'] == 'fold':
                        if monteOdds == 1.0:
                            monteOdds = .5
                        response = '3'
                    elif riverResponses[responseNum]['action'] == 'raise':
                        response = '4'
                    responseNum += 1
                else:
                    if pfEvent['eventName'] == '__show_action':
                        if pfEvent['data']['action']['action'] == 'raise':
                            raiseCount += 1
                        elif pfEvent['data']['action']['action'] == 'bet':
                            raiseCount += 1
            risk = (1-monteOdds) * raiseCount
            round = 3.0
            dataFile.write('{0},{1},{2}\n'.format(round, risk, response))
            """
        except ValueError as e:
            raise ValueError('Unable to create events for this round')


if __name__ == '__main__':
    parseDir = os.path.dirname(os.path.realpath(__file__))
    with open('hdb') as roundsFile:
        gameRounds = [next(roundsFile) for x in range(2000)]
        testRounds = [next(roundsFile) for x in range(2000)]
    gameRounds = [re.sub('\s+', ',', x.strip()).split(',') for x in gameRounds]
    testRounds = [re.sub('\s+', ',', x.strip()).split(',') for x in testRounds]
    dataFile = open('trainData.csv', 'a')
    dataFile.write('2000,2,bet,call,check,fold,raise\n')
    for round in gameRounds:
        try:
            getData(round, dataFile)
            print('Successfully generated training data for round {0}'.format(round[0]))
        except ValueError as e:
            print('Could not generate training data for round {0}'.format(round[0]))
    dataFile = open('testData.csv', 'a')
    dataFile.write('2000,2,bet,call,check,fold,raise\n')
    for round in testRounds:
        try:
            getData(round, dataFile)
            print('Successfully generated test data for round {0}'.format(round[0]))
        except ValueError as e:
            print('Could not generate test data for round {0}'.format(round[0]))
    print('Done')
