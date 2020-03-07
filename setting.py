class Setting:
    def __init__(self, loss=0, delay=0, jitter=[0, 0], black=[], white=[], client_msg="", server_msg=""):
        # TODO: setting a range of value?
        self.loss = loss
        self.delay = delay
        self.jitter = jitter
        self.black_list = black
        self.white_list = white
        self.client_msg = client_msg
        self.server_msg = server_msg
