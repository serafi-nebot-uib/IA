from typing import Self
from copy import deepcopy
from itertools import product, starmap
from functools import cached_property, cache

class Estat:
    # having a simple cache greatly improves performance (22.5x): 45s to 2s for evaluating the initial state
    __cache: dict[int, Self] = {}

    def __new__(cls, taulell: list[list[str]], mida: tuple[int, int], torn: str):
        key = cls.__hash(taulell, mida, torn)
        obj = cls.__cache.get(key, None)
        if obj is None:
            obj = super().__new__(cls)
            cls.__cache[key] = obj
        return obj

    def __del__(self): del Estat.__cache[Estat.__hash(self.taulell, self.mida, self.torn)]

    def __init__(self, taulell: list[list[str]], mida: tuple[int, int], torn: str):
        if not hasattr(self, "__init"):
            self.taulell, self.mida, self.torn = taulell, mida, torn
            self.__init = True
            self.__locked = True

    @cached_property
    def fills(self) -> list[tuple[Self, tuple[int, int]]]:
        if self.guanyador is None:
            return [(p, c) for c in product(*map(range, self.mida)) if (p := self.posar(*c))]
        return []

    @cached_property
    def guanyador(self) -> int | None:
        # very generic function, perhaps overkill for this use case
        # because of the game's simplicity, various improvements can be introduced to make it more efficient (remove redundant checks)
        desp = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
        for px, py in product(*map(range, self.mida)):
            for dx, dy in desp:
                idxs = [(py+dy*i, px+dx*i) for i in range(3)] # TODO: should difficulty (3) be parametrized?
                if all(starmap(self.__bounds, idxs)):
                    symbols = {self.taulell[x][y] for x, y in idxs}
                    if len(symbols) == 1 and " " not in symbols:
                        return next(iter(symbols))
        return None

    @cached_property
    def meta(self) -> bool: return self.guanyador is not None or len(self.fills) == 0

    @cache
    def value(self, torn: str) -> int:
        if self.meta:
            if self.guanyador is None:
                return 0
            return 1 if self.guanyador == torn else -1
        torn_seg = "0" if torn == "X" else "X"
        fvals = [f.value(torn_seg) for f, _ in self.fills]
        return max(fvals) if self.torn == torn else min(fvals)

    def posar(self, x: int, y: int) -> Self | None:
        if self.__bounds(x, y) and self.taulell[x][y] == " ":
            taulell = deepcopy(self.taulell)
            taulell[x][y] = self.torn
            return self.__class__(taulell, self.mida, "0" if self.torn == "X" else "X")
        return None

    def __bounds(self, x: int, y: int) -> bool: return all(0 <= a < b for a, b in zip((x, y), self.mida))
    def __setattr__(self, key, value):
        if getattr(self, "__locked", False): raise AttributeError("object is immutable")
        super().__setattr__(key, value)
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__): return NotImplemented
        return all(getattr(self, a) == getattr(other, b) for a, b in ("taulell", "mida", "torn", "torn_max"))
    @staticmethod
    def __hash(taulell, mida, torn) -> int: return hash(tuple(x for f in taulell for x in f) + mida + (torn,))
    def __hash__(self) -> int: return Estat.__hash(self.taulell, self.mida, self.torn)
    def __repr__(self) -> str: return str(self)
    def __str__(self) -> str: return "\n━╋━╋━\n".join(map("┃".join, self.taulell))