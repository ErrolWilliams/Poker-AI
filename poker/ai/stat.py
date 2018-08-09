from . import AI
from . import action

class StatBot(AI):
        def __init__(self):
                super().__init__()
                self.version = 0

        def request(self):
                monte_odds = self.get_odds()
                round_num = self.table.round

                # print("Using stats!")
                # print(f"monte_odds={monte_odds} round={self.table.round}")
                if monte_odds > 0.85:
                        return action.Bet(int(self.player.chips*0.5))
                elif monte_odds > 0.75:
                        return action.Bet(int(self.player.chips*0.2))
                elif monte_odds > 0.60:
                        return action.Call()
                elif monte_odds > 0.50 or (monte_odds > 0.15 and round_num == 0):
                        return action.Check()
                else:
                        return action.Fold()


class StatBot2(AI):
        def __init__(self):
                super().__init__()
                self.version = 0

        def request(self):
                """
                Constants
                """
                
                high_risk = 0.2
                med_risk = 0.1
                high_odds = 2.0
                med_odds = 1.2
        
                """
                """
                odds = self.get_odds()
                odds = odds / (1/float(self.players_active())) 
                round_num = self.table.round
                chips = self.player.chips
                cur_bet = self.player.min_bet - self.table.small_blind
                my_bet = self.player.bet + self.player.round_bet + self.player.min_bet
                round_risk = my_bet / float(my_bet + chips)
                
                if round_risk > high_risk:
                        Risk = 'high'
                elif round_risk > med_risk:
                        Risk = 'med'
                else:
                        Risk = 'low'
                if odds > high_odds:
                        Odds = 'high'
                elif odds > med_odds:
                        Odds = 'med'
                else:
                        Odds = 'low'
                # print('Risk: {0}({1})\nOdds: {2}({3}\nBet: {4})'.format(round_risk, Risk, odds, Odds, cur_bet))
                
                if round_risk > high_risk:     # high risk
                        if odds > high_odds:
                                if cur_bet > 0:
                                        return action.Raise()
                                else:
                                        return action.Bet(int(self.player.chips*0.05))
                        elif odds > med_odds:
                                if cur_bet > 0:
                                        return action.Call()
                                else:
                                        return action.Check()
                        else:
                                if cur_bet > 0:
                                        return action.Fold()
                                else:
                                        return action.Check()
                elif round_risk > med_risk:    # med risk       
                        if odds > high_odds:
                                if cur_bet > 0:
                                        return action.Raise()
                                else:
                                        return action.Bet(int(self.player.chips*0.05))
                        elif odds > med_odds:
                                if cur_bet > 0:
                                        return action.Call()
                                else:
                                        return action.Check()
                        else:
                                if cur_bet > 0:
                                        return action.Fold()
                                else:
                                        return action.Check()
                else:
                        if odds > high_odds:
                                if cur_bet > 0:
                                        return action.Raise()
                                else:
                                        return action.Bet(int(self.player.chips*0.1))
                        elif odds > med_odds:
                                if cur_bet > 0:
                                        return action.Call()
                                else:
                                        return action.Bet(int(self.player.chips*0.05))
                        else:
                                if cur_bet > 0:
                                        return action.Fold()
                                else:
                                        return action.Check()


class StatBot3(AI):
        def __init__(self):
                super().__init__()
                self.version = 0

        def request(self):
                """
                Constants
                """
                high_risk = 0.2   # betting over 20% of chips is high risk
                med_risk = 0.07   # betting over 7% of chips is med risk
                high_odds = 0.75   # winning over 80% of monte carlo is high odds
                med_odds = 0.5    # winning over 50% of monte carlo is medium odds
                
                preflop_slope = 0.6  # slope for pre flop playability 
                flop_slope = 0.5     # slope for flop playability 
                turn_slope = 0.4     # slope for turn playability 
                river_slope = 0.4    # slope for river playability  
                
                preflop_intercept = .4  # intercept for pre flop playability
                flop_intercept = 0.5   # intercept for flop playability
                turn_intercept = 0.6   # intercept for turn playability
                river_intercept = 0.6  # intercept for river playability
                """
                """
                round_num = self.table.round
                slope = preflop_slope
                intercept = preflop_intercept
                if round_num == 1:
                    slope = flop_slope
                    intercept = flop_intercept
                elif round_num == 2:
                    slope = turn_slope
                    intercept = turn_intercept 
                elif round_num == 3:
                    slope = river_slope
                    intercept = river_intercept 
                chips = self.player.chips
                cur_bet = self.player.min_bet - self.table.small_blind
                my_bet = self.player.bet + self.player.round_bet + self.player.min_bet
                
                round_risk = my_bet / float(my_bet + chips)  # percentage of chips at stake
                odds = self.get_odds()                 # percentage of winning based off monte carlo
                
                if round_risk > high_risk:
                        Risk = 'high'
                elif round_risk > med_risk:
                        Risk = 'med'
                else:
                        Risk = 'low'
                if odds > high_odds:
                        Odds = 'high'
                elif odds > med_odds:
                        Odds = 'med'
                else:
                        Odds = 'low'
                # print('Risk: {0}({1})\nOdds: {2}({3})'.format(round_risk, Risk, odds, Odds))

                if odds >= (round_risk*slope + intercept):          # if true will play this hand    
                    if round_risk > high_risk:     # high risk
                            if odds > high_odds:
                                    if cur_bet > 0:
                                            return action.Raise()
                                    else:
                                            return action.Bet(int(self.player.chips*0.05))
                            elif odds > med_odds:
                                    if cur_bet > 0:
                                            return action.Call()
                                    else:
                                            return action.Check()
                            else:
                                    return action.Check()
                    elif round_risk > med_risk:    # med risk   
                            if odds > high_odds:
                                    if cur_bet > 0:
                                            return action.Raise()
                                    else:
                                            return action.Bet(int(self.player.chips*0.05))
                            elif odds > med_odds:
                                    if cur_bet > 0:
                                            return action.Call()
                                    else:
                                            return action.Check()
                            else:
                                    return action.Check()
                    else:                        # low risk
                            if odds > high_odds:
                                    if cur_bet > 0:
                                            return action.Raise()
                                    else:
                                            return action.Bet(int(self.player.chips*0.1))
                            elif odds > med_odds:
                                    if cur_bet > 0:
                                            return action.Call()
                                    else:
                                            return action.Bet(int(self.player.chips*0.05))
                            else:
                                    return action.Check()
                else:
                    return action.Fold()
