class Setting:
    def __init__(self, pkg_size = 4096, connection_timeout = 10, loss=0, delay=0, jitter=0, black=[], white=[]):
        # TODO: setting a range of value?
        self.pkg_size = pkg_size
        self.connection_timeout = connection_timeout
        self.loss = loss
        self.delay = delay
        self.jitter = jitter
        self.black_list = black
        self.white_list = white
