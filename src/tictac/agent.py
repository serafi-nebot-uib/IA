""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from tictac.estat import Estat

class Agent(agent.Agent):
    cnt: int = 0
    def __init__(self, poda: bool = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__poda = poda
        Agent.cnt += 1
        self.nom = f"Agent {Agent.cnt}"

    def actua(self, percepcio):
        taulell = percepcio["taulell"]
        mida = percepcio["mida"]
        torn = percepcio["torn"]
        estat = Estat(taulell, mida, torn)

        if estat.meta:
            import sys
            sys.exit(0)
            return "E", ""

        alpha, beta = (float("-inf"), float("inf")) if self.__poda else (None, None)
        _, c = max(estat.fills, key=lambda f: f[0].value(torn, alpha, beta))
        return "P", c