import gymnasium as gym
import numpy as np

class SARSA:
  def __init__(self, nstates: int, nactions: int, alpha: float, gamma: float):
    self.__nstates = nstates
    self.__nactions = nactions
    self.__alpha = alpha
    self.__gamma = gamma
    self.reset()

  def reset(self):
    self.q = np.zeros((self.__nstates, self.__nactions), dtype="float")

  def action(self, state: int, epsilon: float = 0.0) -> int:
    if np.random.uniform(0, 1) < epsilon: return np.random.choice(self.__nactions)
    else: return np.random.choice(np.where(self.q[state] == self.q[state].max())[0])

  def update(self, state: int, action: int, reward: float, new_state: int, new_action: int, final: bool = False):
    target = reward + self.__gamma * self.q[new_state, new_action] * (not final)
    self.q[state, action] += self.__alpha * (target - self.q[state, action])

def plot_qtable(q: np.ndarray, nrows: int, ncols: int):
  import matplotlib.pyplot as plt

  fig, ax = plt.subplots(figsize=(8, 8))

  values = q.max(axis=-1).reshape(nrows, ncols)
  ax.imshow(values, cmap="Blues")

  # apply softmax to get arrow lengths proportionate to each action's value
  shifted_q = q - q.max(axis=-1, keepdims=True) # shift for numerical stability
  exp_q = np.exp(shifted_q)
  anorm = exp_q / exp_q.sum(axis=-1, keepdims=True)
  #                 left     down    right   up
  adir = np.array([[-1, 0], [0, 1], [1, 0], [0, -1]])
  arrow = adir * anorm.reshape(nrows, ncols, -1, 1)

  for i in range(arrow.shape[0]):
    for j in range(arrow.shape[1]):
      for a in range(arrow.shape[2]):
        dx, dy = arrow[i, j, a]
        ax.arrow(i, j, dx, dy,
                 head_width=0.08, head_length=0.08,
                 fc="white", ec="black", alpha=0.8,
                 length_includes_head=True, clip_on=True)

  ax.set_xticks([])
  ax.set_yticks([])
  plt.tight_layout()
  plt.show()

def main():
  slippery = True
  env = gym.make("FrozenLake-v1", is_slippery=slippery, render_mode=None)
  nactions = env.action_space.n
  nstates = 4 * 4 # TODO: why doesn't env.state_space exist?
  nepisodes = 20000
  # nepisodes = 10000
  epsilon = 0.1

  agent = SARSA(nstates, nactions, alpha=0.1, gamma=0.9998)

  # train the agent
  for _ in range(nepisodes):
    state, _ = env.reset()
    action = agent.action(state, epsilon)

    stepi = 0
    term, trunc = False, False
    while not (term or trunc):
      new_state, reward, term, trunc, info = env.step(action)
      new_action = agent.action(new_state, epsilon)

      # TODO: is this allowed?
      stepi += 1
      # reward += -0.01 * stepi

      agent.update(state, action, reward, new_state, new_action, term)
      state, action = new_state, new_action

  # print(agent.q)
  # plot_qtable(agent.q, 4, 4)

  # test the agent
  # env = gym.make("FrozenLake-v1", is_slippery=slippery, render_mode="human")
  # state, _ = env.reset()
  # term, trunc = False, False
  # while not (term or trunc): state, _ , term, trunc, _ = env.step(agent.action(state))

if __name__ == "__main__":
  main()