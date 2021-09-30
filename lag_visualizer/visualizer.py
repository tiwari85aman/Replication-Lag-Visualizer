from modes import WebMode, MatplotlibMode


class Visualizer:

    def __init__(self, pg):
        self.__supported_mode = {
            "matplotlib": MatplotlibMode,
            "web": WebMode
        }
        self.pg = pg

    def start(self, mode):
        if mode in self.__supported_mode:
            self.__supported_mode.get(mode)(self.pg)
        else:
            raise Exception(f"{','.join(list(self.__supported_mode.keys()))} are the only supported modes")
