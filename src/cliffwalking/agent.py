import numpy as np
import random

from iaLib import agent

class AgentSARSA(agent.Agent):
    def __init__(self, alpha, gamma, eps, seed=0):
        super().__init__(long_memoria=0)

        self.__alpha = alpha
        self.__gamma = gamma
        self.__eps = eps
        self.__nrows = 4
        self.__ncols = 12
        self.__nactions = 4
        self.q = np.zeros((self.__nrows * self.__ncols, self.__nactions), dtype="float")

        # np.random.seed(seed)
        # random.seed(seed)

    def train(self, env):
        s, _ = env.reset()
        a = self.actua(s)
        term, trunc = False, False

        while not (term or trunc):
            sn, r, term, trunc, _ = env.step(a)
            an = self.actua(sn)
            self.q[s, a] = self.q[s, a] + self.__alpha * (r + self.__gamma * self.q[sn, an] - self.q[s, a])
            s, a = sn, an

    def actua(self, estat: int) -> int:
        return np.random.choice(self.__nactions) if np.random.rand() < self.__eps else self.q[estat].argmax()

class AgentQL(agent.Agent):
    def __init__(self, alpha, gamma, eps, seed=0):
        super().__init__(long_memoria=0)

        self.__alpha = alpha
        self.__gamma = gamma
        self.__eps = eps
        self.__nrows = 4
        self.__ncols = 12
        self.__nactions = 4
        self.q = np.zeros((self.__nrows * self.__ncols, self.__nactions), dtype="float")

        # np.random.seed(seed)
        # random.seed(seed)

    def train(self, env):
        s, _ = env.reset()
        term, trunc = False, False

        while not (term or trunc):
            a = self.actua(s)
            sn, r, term, trunc, _ = env.step(a)
            self.q[s, a] = self.q[s, a] + self.__alpha * (r + self.__gamma * self.q[sn].max() - self.q[s, a])
            s = sn

    def actua(self, estat: int) -> int:
        return np.random.choice(self.__nactions) if np.random.rand() < self.__eps else self.q[estat].argmax()