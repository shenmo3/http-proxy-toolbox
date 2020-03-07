class Setting:
    def __init__(self, loss=0, delay=0, jitter=[0, 0], acl={"default": True}, client_msg="", server_msg=""):
        # TODO: setting a range of value?
        self.loss = loss
        self.delay = delay
        self.jitter = jitter
        self.acl = acl
        self.client_msg = client_msg
        self.server_msg = server_msg
