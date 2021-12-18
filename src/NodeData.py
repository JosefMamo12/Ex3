import sys


class NodeData:
    def __init__(self, key: int):
        self._key = key
        self._pos = None
        self._info = ''
        self._tag = 0
        self._weight = sys.float_info.max

    def get_key(self) -> int:
        return self._key

    def set_info(self, info: str):
        self._info = info

    def get_info(self) -> str:
        return self._info

    def get_weight(self) -> float:
        return self._weight

    def set_weight(self, weight):
        self._weight = weight

    def set_tag(self, tag: int):
        self._tag = tag

    def __eq__(self, other):
        if isinstance(other, NodeData):
            return self._pos == other._pos and self._key == other._key and self._weight == other._weight and self._info == other._info and self._key == other._key
        return False

    def get_tag(self) -> int:
        return self._tag

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self, x: float, y: float, z: float):
        self._pos = (x, y, z)

    def __repr__(self):
        return 'NodeData[Key:' + str(self._key) + ' Weight:' + str(self._weight) + ' ' + str(self._pos) + ']'
