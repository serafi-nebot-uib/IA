""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from tictac.estat import Estat

class Agent(agent.Agent):
    def __init__(self, torn: str, poda: bool = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__visitats = None
        self.__cami_exit = None
        self.__poda = poda
        self.torn = torn
        self.nom = f"Agent {torn}"

    def actua(self, percepcio):
        taulell = percepcio["taulell"]
        mida = percepcio["mida"]
        torn = percepcio["torn"]
        estat = Estat(taulell, mida, torn)
        print(estat)

        m = max(estat.fills, key=lambda f: f.value(torn))

        print(estat.value(self.torn))

        import sys
        sys.exit(0)