import os
import yaml


__all__ = ["Config"]


class Config:
    def __init__(self):
        try:            
            if os.path.exists("config.yml"):
                with open("config.yml","r") as conf:
                    cfg = yaml.load(conf,Loader=yaml.SafeLoader)
                    for key in cfg:
                        self.__setattr__(key,cfg[key])
                    self.audio_resources = os.path.join(os.path.curdir,*c.audio_resources)
                    self.image_resources = os.path.join(os.path.curdir,*c.image_resources)
        except Exception as ex:
            #TODO: Add logger 
            print(ex)

if __name__ == '__main__':
    c = Config()
    print(c)