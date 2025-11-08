"""
Tasca a fer:
    - Implementa la funció `generate_episode` per generar un episodi seguint una política
        epsilon-greedy.
    - Completa el bucle principal a `main` per actualitzar els valors Q utilitzant l'algorisme de
        Monte Carlo amb política epsilon-greedy.
"""
from gridworld.joc import GridWorld
import numpy as np

N = 5
A = GridWorld.actions
P = { "N": "↑", "S": "↓", "E": "→", "O": "←" }

def generate_episode(env: GridWorld, state: tuple[int, int], policy, epsilon: float):
    env.reset(state)
    episode = []
    for _ in range(50):
        action = np.random.choice(len(A)) if np.random.rand() < epsilon else policy[state]
        state_next, reward = env.step(A[action])
        episode.append((state, action, reward))
        state = state_next
    return episode

def print_policy(p): print("\n".join(" ".join(P[A[c]] for c in r) for r in p))
def print_value(v): print("\n".join(" ".join(f"{c:>6.3f}" for c in r) for r in v))

def main():
    env = GridWorld((0, 0), (N, N))

    gamma = 0.9
    eps = 0.1
    episodis = 20000

    Q = np.zeros((N, N, len(A)), dtype="float")
    C = np.zeros((N, N, len(A)), dtype="int")
    policy = np.zeros((N, N), dtype="int")

    for _ in range(episodis):
        state = np.random.randint(0, N), np.random.randint(0, N)
        episode = generate_episode(env, state, policy, eps)

        print_policy(policy)
        print()

        g = 0
        visited = set()
        for s, a, r in episode[::-1]:
            sa = (s, a)
            g += r * gamma
            if sa not in visited:
                visited.add(sa)
                # new_avg = old_avg + (new_value - old_avg) / (n + 1)
                C[s][a] += 1
                Q[s][a] += (g - Q[s][a]) / C[s][a]
                policy[s] = np.random.randint(len(A)) if np.random.rand() < eps else Q[s].argmax()

    print_policy(policy)
    print()
    print_value(Q.max(axis=-1))

if __name__ == "__main__":
    main()
