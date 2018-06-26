from tk.utils import *

class dotdict(dict):
    def __getattr__(self, name):
        return self[name]
