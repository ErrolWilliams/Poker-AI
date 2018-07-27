import tflearn
import numpy as np
import poker.odds as calc
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from poker.ai import AI

#------------------------------------------------------------------

class BlackPanther():           
    def __init__(self, ai):
       self.ai = ai
       self.attached = False
	  
    def receive_info(self, info, public_state):                                      
       
       if not self.attached:
           self.ai.attach(info.person_state.id)

       self.ai.roomai_update(info, public_state)

       self.avalible_actions = info.person_state.available_actions
       print(f'AVAILABLE ACTIONS {info.person_state.available_actions}')
                                             
       my_id = info.person_state.id
       num_player = len (public_state.chips)
       pot = sum (public_state.bets)   # the pot value
       bets = public_state.bets        # each player's bets
       chips = public_state.chips      # each player's chips
       folded = public_state.is_fold   # player's fold status
       
       hand = [info.person_state.hand_cards[0].key, \
               info.person_state.hand_cards[1].key]
       
       community = []
       state = 0
       if len(public_state.public_cards) == 3:
           state = 1
           community = [public_state.public_cards[0].key, \
                        public_state.public_cards[1].key, \
                        public_state.public_cards[2].key]
       elif len(public_state.public_cards) == 4:
           state = 2
           community = [public_state.public_cards[0].key, \
                             public_state.public_cards[1].key, \
                             public_state.public_cards[2].key, \
                             public_state.public_cards[3].key]
       elif len(public_state.public_cards) == 5:
           state = 3
           community = [public_state.public_cards[0].key, \
                        public_state.public_cards[1].key, \
                        public_state.public_cards[2].key, \
                        public_state.public_cards[3].key, \
                        public_state.public_cards[4].key]
       else:
           pass
              
#my_odds = calc.odds(hand, community, num_player)
       my_odds = 0.3
       my_stake = bets[my_id]
       my_chips = chips[my_id]
       my_cost = max(bets) - my_stake

       self.my_score = ((pot*my_odds) - my_stake) + 3 * (1 - my_odds) * num_player * (sum(folded))

       bet_percent = []
       chips_percent = []
       for i in range(len(chips)):
           bet_percent.append(bets[i] / chips[i])
           chips_percent.append(chips[i] / sum(chips))

       self.input_data = np.zeros((10,10), dtype=np.float32)
            
       self.input_data[0, 0] = my_odds
       self.input_data[1, 0] = my_stake / my_chips
       self.input_data[2, 0] = my_chips / sum(chips)
       self.input_data[3, 0] = my_cost  / my_chips
       self.input_data[4, 0] = state
       self.input_data[5, 0] = pot / my_chips
       self.input_data[6, 0] = num_player
       self.input_data[7, :num_player] = bet_percent
       self.input_data[8, :num_player] = chips_percent
       self.input_data[9, :num_player] = folded

    def take_action(self):

       #------
       # Decision Engine HERE
       #------
       idx = 1
       my_action = list(self.avalible_actions.values())[idx]
# my_action = self.ai.request_action().to_roomai()
       save_data = [self.input_data, my_action.key, self.my_score]
       #log = open("training_data.txt", "a")
       #log.write(str(save_data))
       return save_data, my_action

    def reset(self):
       self.ai.new_round()

#------------------------------------------------------------------

def neural_network_model(input_size):
    network = input_data(shape = [1, 10, 10, 1], name='input')
	
    network = fully_connected(network, 128, activation = 'relu')
    network = dropout(network, 0.8)
    
    network = fully_connected(network, 256, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 512, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 256, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 128, activation = 'relu')
    network = dropout(network, 0.8)

    network = fully_connected(network, 5, activation = 'softmax')
    network = dropout(network, 0.8)

    network = regression(network, optimizer='adam', learning_rate = 1e-3, \
                         loss = 'categorical_crossentropy', name = 'targets')
    model = tflearn.DNN(network, tensorboard_dir = 'dir')

    return model

def train_model(training_data, model=False):
        
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0], 1))
    Y = np.array([j[1] for j in training_data])

    if not model:
        model = neural_network_model(len(X[0]))
        
        model.fit({'input': X}, {'targets': Y}, n_epochs = 5, snapshot_step = 500,\
                  show_metric = True, run_id = 'Texas')

def filter(training_data):
    score_delta = []
    index = []
    for i in range(len(training_data) - 1):
        score.append(training_data[i+1][3] - training_data[i][3])
