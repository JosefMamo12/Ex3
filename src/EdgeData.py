class EdgeData:

    def __init__(self, src: int, dest: int, weight: float):
        self._src = src
        self._dest = dest
        self._weight = weight
        self._info = ''

    def get_src(self) -> int:
        return self._src

    def get_dest(self) -> int:
        return self._dest

    def get_weight(self) -> float:
        return self._weight

    def set_weight(self, weight) -> None:
        self._weight = weight

    def get_info(self) -> str:
        return self._info

    def set_info(self, info) -> None:
        self._info = info

    def __repr__(self):
        return 'EdgeData[src:' + str(self._src) + ' dest:' + str(self._dest) + ' weight:' + str(self._weight) + ']'
