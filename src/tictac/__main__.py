from tictac import joc, agent
# from tictac.solucio import agent as agent


def main():
    quatre = joc.Taulell(
        [agent.Agent("0", poda=False), agent.Agent("X", poda=False)],
        mida_taulell=(3, 3),
        dificultat=3,
    )
    quatre.comencar()


if __name__ == "__main__":
    main()
