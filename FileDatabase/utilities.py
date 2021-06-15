

class self_setup_class : 
    '''helper class to setup class which can create attributes from 
    the passed key value pairs during initalization of instance'''
    def __init__(self,**kwargs):
        self.set_inputs(**kwargs)
    def set_inputs(self,**inputs):
        for key in inputs:
            setattr(self,key,inputs.get(key))