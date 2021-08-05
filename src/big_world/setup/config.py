import os
import yaml

class Config(object):
    def __init__(self):
        try:
            conf_path = os.path.join(os.path.dirname(__file__),"config.yml")
            if os.path.exists(conf_path):
                with open(conf_path,"r") as conf:
                    cfg = yaml.load(conf,Loader=yaml.SafeLoader)
                    for key in cfg:
                        self.__setattr__(key,cfg[key])
                    self.audio_resources = os.path.join(*self.audio_resources)
                    self.image_resources = os.path.join(os.path.curdir,*self.image_resources)
        except Exception as ex:
            #TODO: Add logger 
            print(ex)