from typing import Self
from copy import deepcopy
from itertools import product, starmap
from functools import cached_property

class Estat:
    __cache: dict[int, Self] = {}

    def __new__(cls, taulell: list[list[str]], mida: tuple[int, int], torn: str, torn_max: bool, cami: list[tuple[int, int]] | None = None):
        cami = [] if cami is None else cami
        key = cls.__hash(taulell, mida, torn, torn_max, cami)
        obj = cls.__cache.get(key, None)
        if obj is None:
            obj = super().__new__(cls)
            cls.__cache[key] = obj
        return obj

    def __del__(self): del Estat.__cache[Estat.__hash(self.taulell, self.mida, self.torn, self.torn_max, self.cami)]

    def __init__(self, taulell: list[list[str]], mida: tuple[int, int], torn: str, torn_max: bool, cami: list[tuple[int, int]] | None = None):
        if not hasattr(self, "__init"):
            self.taulell, self.mida, self.torn, self.torn_max = taulell, mida, torn, torn_max
            self.cami = [] if cami is None else cami
            self.__init = True
            self.__locked = True

    @cached_property
    def value(self) -> int:
        if not self.meta and len(self.fills) > 0:
            fn = max if self.torn_max else min
            return fn(f.value for f in self.fills)
        return self.puntuacio

    @cached_property
    def fills(self) -> list[Self]:
        return list(filter(None, starmap(self.posar, product(*map(range, self.mida))))) if not self.meta else []

    @cached_property
    def puntuacio(self) -> int:
        # very generic function, perhaps overkill for this use case
        # because of the game's simplicity, various improvements can be introduced to make it more efficient (remove redundant checks)
        desp = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
        for px, py in product(*map(range, self.mida)):
            for dx, dy in desp:
                idxs = [(py+dy*i, px+dx*i) for i in range(3)] # TODO: should difficulty (3) be parametrized?
                if all(starmap(self.__bounds, idxs)):
                    symbols = {self.taulell[y][x] for x, y in idxs}
                    if len(symbols) == 1 and " " not in symbols:
                        return 1 if "0" in symbols else -1 # TODO: is max always 0?
        return 0

    @cached_property
    def meta(self) -> bool: return self.puntuacio != 0

    def posar(self, x: int, y: int) -> Self | None:
        if self.__bounds(x, y) and self.taulell[y][x] == " ":
            taulell = deepcopy(self.taulell)
            taulell[y][x] = self.torn
            return self.__class__(taulell, self.mida, "0" if self.torn == "X" else "X", not self.torn_max, self.cami + [(x, y)])
        return None

    def __bounds(self, x: int, y: int) -> bool: return all(0 <= a < b for a, b in zip((x, y), self.mida))
    def __setattr__(self, key, value):
        if getattr(self, "__locked", False): raise AttributeError("object is immutable")
        super().__setattr__(key, value)
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__): return NotImplemented
        return all(getattr(self, a) == getattr(other, b) for a, b in ("taulell", "mida", "torn", "torn_max"))
    @staticmethod
    def __hash(taulell, mida, torn, torn_max, cami) -> int: return hash(tuple(map(tuple, taulell)) + mida + (torn, torn_max) + tuple(cami))
    def __hash__(self) -> int: return self.__hash(self.taulell, self.mida, self.torn, self.torn_max, self.cami)
    def __repr__(self) -> str: return str(self)
    def __str__(self) -> str: return "\n━╋━╋━\n".join(map("┃".join, self.taulell))