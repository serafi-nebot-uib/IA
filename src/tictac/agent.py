""" Agent Minimax.

Mòdul en el qual es desenvolupa un agent Minimax amb poda alfa-beta per resoldre el problema del
Tic Tac Toe.

Creat per: Miquel Miró Nicolau (UIB), 2024
"""
from iaLib import agent
from graphviz import Digraph
from tictac.estat import Estat

class Agent(agent.Agent):
    pos = 0
    def __init__(self, torn: str, poda: bool = False):
        super(Agent, self).__init__(long_memoria=1)
        self.__visitats = None
        self.__cami_exit = None
        self.__poda = poda
        self.torn = torn
        self.nom = f"Agent {torn}"
        self.test = False

    def graph(self, estat_inicial: Estat):
        oberts = []
        tancats = set()
        estat: Estat | None = None

        nodes, edges = [], []
        nodes.append(estat_inicial)
        oberts.append(estat_inicial)
        while oberts:
            estat = oberts.pop(-1)

            if estat is None: break
            if estat in tancats: continue

            if estat.meta:
                continue

            for f in estat.fills:
                edges.append((estat, f))
                nodes.append(f)
                oberts.append(f)
            tancats.add(estat)
            if len(tancats) > 100: break

        dot = Digraph()
        dot.attr("node", shape="circle", style="filled", fillcolor="white")

        for estat in nodes:
            if estat is not None:
                color = "white"
                if estat.meta:
                    if estat.puntuacio == 0:
                        color = "orange"
                    elif estat.puntuacio == 1:
                        color = "lightgreen"
                    elif estat.puntuacio == -1:
                        color = "red"
                # color = "white" if len(estat.fills) > 0 else ("lightgreen" if estat.meta else "red")
                dot.node(str(hash(estat)), f"{estat} {estat.value}", fillcolor=color)

        for p, c in edges:
            dot.edge(str(hash(p)), str(hash(c)))
        dot.render("graph", format="svg", cleanup=True)

    def actua(self, percepcio):
        taulell = percepcio["taulell"]
        mida = percepcio["mida"]
        torn = percepcio["torn"]
        estat = Estat(taulell, mida, torn, torn == self.torn)
        # for f in estat.fills:
        print(estat)
        # self.graph(estat)

        import sys
        sys.exit(0)

        # print(percepcio)
        # p = Agent.pos % mida[0], Agent.pos // mida[0]
        # Agent.pos += 1
        # print(p)
        # return "P", p