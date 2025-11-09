import gymnasium as gym
import numpy as np

class SARSA:
  def __init__(self, nstates: int, nactions: int, alpha: float, gamma: float):
    self.__nstates = nstates
    self.__nactions = nactions
    self.__alpha = alpha
    self.__gamma = gamma
    self.reset()

  def update(self, state: int, action: int, reward: float, new_state: int, new_action: int):
    target = reward + self.__gamma * self.q[new_state, new_action]
    self.q[state, action] += self.__alpha * (target - self.q[state, action])

  def action(self, state: int, epsilon: float = 0.0) -> int:
    if np.random.uniform(0, 1) < epsilon: return np.random.choice(self.__nactions)
    else: return np.random.choice(np.where(self.q[state] == self.q[state].max())[0])

  def reset(self):
    self.q = np.zeros((self.__nstates, self.__nactions), dtype="float")

def main():
  slippery = True
  env = gym.make("FrozenLake-v1", is_slippery=slippery, render_mode=None)
  nactions = env.action_space.n
  nstates = 4 * 4 # TODO: why doesn't env.state_space exist?
  nepisodes = 20000
  epsilon = 0.1

  agent = SARSA(nstates, nactions, alpha=0.25, gamma=0.99)

  # train the agent
  for _ in range(nepisodes):
    state, _ = env.reset()
    action = agent.action(state, epsilon)

    term, trunc = False, False
    while not (term or trunc):
      new_state, reward, term, trunc, info = env.step(action)
      new_action = agent.action(new_state, epsilon)
      agent.update(state, action, reward, new_state, new_action)
      state, action = new_state, new_action

  # test the agent
  env = gym.make("FrozenLake-v1", is_slippery=slippery, render_mode="human")
  state, _ = env.reset()
  term, trunc = False, False
  while not (term or trunc): state, _ , term, trunc, _ = env.step(agent.action(state))

if __name__ == "__main__":
  main()