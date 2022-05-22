import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym
import random
from collections import deque
import os
from tqdm import tqdm
from game import CheckerGame
#from agents import Agent
total_rewards = []


class replay_buffer():
    '''
    A deque storing trajectories
    '''

    def __init__(self, capacity):
        self.capacity = capacity  # the size of the replay buffer
        self.memory = deque(maxlen=capacity)  # replay buffer itself

    def insert(self, state, action, reward, next_state, done):
        '''
        Insert a sequence of data gotten by the agent into the replay buffer.

        Parameter:
            state: the current state
            action: the action done by the agent
            reward: the reward agent got
            next_state: the next state
            done: the status showing whether the episode finish
        
        Return:
            None
        '''
        self.memory.append([state, action, reward, next_state, done])

    def sample(self, batch_size):
        '''
        Sample a batch size of data from the replay buffer.

        Parameter:
            batch_size: the number of samples which will be propagated through the neural network
        
        Returns:
            observations: a batch size of states stored in the replay buffer
            actions: a batch size of actions stored in the replay buffer
            rewards: a batch size of rewards stored in the replay buffer
            next_observations: a batch size of "next_state"s stored in the replay buffer
            done: a batch size of done stored in the replay buffer
        '''
        batch = random.sample(self.memory, batch_size)
        observations, actions, rewards, next_observations, done = zip(*batch)
        return observations, actions, rewards, next_observations, done


class Net(nn.Module):
    '''
    The structure of the Neural Network calculating Q values of each state.
    '''

    def __init__(self,  num_actions, hidden_layer_size=50):
        super(Net, self).__init__()
        # self.input_state = 4  # the dimension of state space
        self.input_state = 17 * 25  # the dimension of state space
        self.num_actions = num_actions  # the dimension of action space
        self.fc1 = nn.Linear(self.input_state, 32)  # input layer
        self.fc2 = nn.Linear(32, hidden_layer_size)  # hidden layer
        self.fc3 = nn.Linear(hidden_layer_size, num_actions)  # output layer

    def forward(self, states):
        '''
        Forward the state to the neural network.
        
        Parameter:
            states: a batch size of states
        
        Return:
            q_values: a batch size of q_values
        '''
        x = F.relu(self.fc1(states))
        x = F.relu(self.fc2(x))
        q_values = self.fc3(x)
        return q_values


class DQNAgent(Agent):
    def __init__(self, epsilon=0.05, learning_rate=0.0002, GAMMA=0.97, batch_size=32, capacity=10000):
        """
        The agent learning how to control the action of the cart pole.
        
        Hyperparameters:
            epsilon: Determines the explore/expliot rate of the agent
            learning_rate: Determines the step size while moving toward a minimum of a loss function
            GAMMA: the discount factor (tradeoff between immediate rewards and future rewards)
            batch_size: the number of samples which will be propagated through the neural network
            capacity: the size of the replay buffer/memory
        """
        self.env = CheckerGame(auto=True, gui=False)
        self.n_actions = 2  # the number of actions
        self.count = 0  # recording the number of iterations

        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.gamma = GAMMA
        self.batch_size = batch_size
        self.capacity = capacity

        self.buffer = replay_buffer(self.capacity)
        self.evaluate_net = Net(self.n_actions)  # the evaluate network
        self.target_net = Net(self.n_actions)  # the target network

        self.optimizer = torch.optim.Adam(
            self.evaluate_net.parameters(), lr=self.learning_rate)  # Adam is a method using to optimize the neural network

    def learn(self):
        '''
        - Implement the learning function.
        - Here are the hints to implement.
        
        Steps:
        -----
        1. Update target net by current net every 100 times. (we have done for you)
        2. Sample trajectories of batch size from the replay buffer.
        3. Forward the data to the evaluate net and the target net.
        4. Compute the loss with MSE.
        5. Zero-out the gradients.
        6. Backpropagation.
        7. Optimize the loss function.
        -----

        Parameters:
            self: the agent itself.
            (Don't pass additional parameters to the function.)
            (All you need have been initialized in the constructor.)
        
        Returns:
            None (Don't need to return anything)
        '''
        if self.count % 100 == 0:
            self.target_net.load_state_dict(self.evaluate_net.state_dict())

        # Begin your code
        if len(self.buffer.memory) < self.batch_size:
            print("Error: Not Enough Memory")
            return
        # 2. 隨機取樣 batch_size 個 experience
        sample = self.buffer.sample(self.batch_size)
        b_observations = sample[0]
        b_actions = sample[1]
        b_rewards = sample[2]
        b_next_observations = sample[3]
        b_done = sample[4]
        b_state = torch.FloatTensor(np.array(b_observations))
        b_action = torch.LongTensor(np.array(b_actions))
        b_reward = torch.FloatTensor(np.array(b_rewards))
        b_next_state = torch.FloatTensor(np.array(b_next_observations))
        b_done = torch.BoolTensor(np.array(b_done))

        # 3. 計算現有 eval net 和 target net 得出 Q value
        action_tuple = []
        for action in b_action:
            temp = [int(action)]
            action_tuple.append(temp)
        b_action_2D = torch.LongTensor(np.array(tuple(action_tuple)))
        # 重新計算這些 experience 當下 eval net 所得出的 Q value
        q_eval = self.evaluate_net.forward(b_state).gather(1, b_action_2D)
        # detach 才不會訓練到 target net
        q_next = self.target_net.forward(b_next_state).detach()
        # q_next.max(1)[0]表示只返回每一行的最大值，不返回索引(长度为32的一维张量)
        # .view()表示把前面所得到的一维张量变成(BATCH_SIZE, 1)的形状
        max_q_next = q_next.max(1)[0].view(self.batch_size, 1)
        # use done to set q_next to 0
        final_q_next = []
        for value, done in zip(max_q_next, b_done):
            if done:
                final_q_next.append(0)
            else:
                final_q_next.append(float(value))
        next_state_values = torch.FloatTensor(np.array(final_q_next))
        q_expected = b_reward + self.gamma * next_state_values
        # 4. Compute the loss with MSE.
        loss_func = nn.MSELoss()
        # .unsqueeze(0) means a row, .unsqueeze(1) means a column
        loss = loss_func(q_eval, q_expected.unsqueeze(1))
        # 5. Zero-out the gradients
        # 6. Backpropagation
        # 7. Optimize the loss function.
        self.optimizer.zero_grad() # 清空上一步的残余更新参数值
        loss.backward() # 误差反向传播, 计算参数更新值
        self.optimizer.step() # 更新评估网络的所有参数
        # End your code

        # You can add some conditions to decide when to save your neural network model
        if self.count % 100 == 0:
            torch.save(self.target_net.state_dict(), "./Tables/DQN.pt")

    def choose_action(self, state):
        """
        - Implement the action-choosing function.
        - Choose the best action with given state and epsilon
        
        Parameters:
            self: the agent itself.
            state: the current state of the enviornment.
            (Don't pass additional parameters to the function.)
            (All you need have been initialized in the constructor.)
        
        Returns:
            action: the chosen action.
        """
        with torch.no_grad():
            # Begin your code
            random_number = np.random.uniform(0, 1)
            if random_number < self.epsilon: # 隨機
                action = self.env.action_space.sample()
            else: # 根據現有 policy 做最好的選擇
                # 以現有 eval net 得出各個 action 的分數
                tensor_state = torch.FloatTensor(state)
                # 挑選最高分的 action
                action = int(torch.argmax(self.evaluate_net.forward(tensor_state)))
            # End your code
        return action

    def check_max_Q(self):
        """
        - Implement the function calculating the max Q value of initial state(self.env.reset()).
        - Check the max Q value of initial state
        
        Parameter:
            self: the agent itself.
            (Don't pass additional parameters to the function.)
            (All you need have been initialized in the constructor.)
        
        Return:
            max_q: the max Q value of initial state(self.env.reset())
        """
        # Begin your code
        initial_state = torch.FloatTensor(self.env.reset())
        max_q = float(torch.max(self.target_net.forward(initial_state)))
        return max_q
        # End your code


def train(env):
    """
    Train the agent on the given environment.
    
    Paramenters:
        env: the given environment.
    
    Returns:
        None (Don't need to return anything)
    """
    agent = DQNAgent()
    episode = 1000
    rewards = []
    for _ in tqdm(range(episode)):
        state = env.reset()
        count = 0
        while True:
            count += 1
            agent.count += 1
            # env.render()
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            agent.buffer.insert(state, int(action), reward,
                                next_state, int(done))
            if agent.count >= 1000:
                agent.learn()
            if done:
                rewards.append(count)
                break
            state = next_state
    total_rewards.append(rewards)


def test(env):
    """
    Test the agent on the given environment.
    
    Paramenters:
        env: the given environment.
    
    Returns:
        None (Don't need to return anything)
    """
    rewards = []
    testing_agent = DQNAgent()
    testing_agent.target_net.load_state_dict(torch.load("./Tables/DQN.pt"))
    for _ in range(100):
        state = env.reset()
        count = 0
        while True:
            count += 1
            Q = testing_agent.target_net.forward(
                torch.FloatTensor(state)).squeeze(0).detach()
            action = int(torch.argmax(Q).numpy())
            next_state, _, done, _ = env.step(action)
            if done:
                rewards.append(count)
                break
            state = next_state
    print(f"reward: {np.mean(rewards)}")
    print(f"max Q:{testing_agent.check_max_Q()}")


def seed(seed=20):
    '''
    It is very IMPORTENT to set random seed for reproducibility of your result!
    '''
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


if __name__ == "__main__":
    '''
    The main funtion
    '''
    # Please change to the assigned seed number in the Google sheet
    SEED = 110
    env = CheckerGame(auto=True, gui=False, seed=SEED) # gym.make('CartPole-v0')
    seed(SEED)
    # env.seed(SEED)
    # env.action_space.seed(SEED)
        
    if not os.path.exists("./Tables"):
        os.mkdir("./Tables")

    # training section:
    for i in range(5):
        print(f"#{i + 1} training progress")
        train(env)
    # testing section:
    # test(env)
    
    if not os.path.exists("./Rewards"):
        os.mkdir("./Rewards")

    np.save("./Rewards/DQN_rewards.npy", np.array(total_rewards))

    # env.close()
