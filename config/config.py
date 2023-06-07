import json
import os

from lib.exceptions.engine_exc import EngineException


class Configuration:
    def __init__(self, filepath: str):
        try:
            os.stat(filepath)
            self.config = json.load(open(filepath, 'r'))
            self.filepath = filepath
            return None
        except:
            raise EngineException(EngineException.NOT_FOUND_ERROR("file"))
        
    def update(self, config: dict):
        for key in config.keys():
            self.config[key] = config[key]
        
    def set_value(self, name: str, value: any):
        self.config[name] = value
        
    def get_value(self, name: str):
        return self.config[name]
    
    def import_file(self, filepath: str):
        try:
            os.stat(filepath)
            config = json.load(open(filepath, 'r'))
            for key in config.keys():
                self.config[key] = config[key]
            self.filepath = filepath
            return None
        except:
            raise EngineException(EngineException.NOT_FOUND_ERROR("file"))
        
    def save(self, filepath: str=None):
        try:
            if filepath == None:
                filepath = self.filepath
            os.stat(filepath)
            f = open(filepath, 'w')
            f.write(json.dumps(self.config))
            return None
        except:
            raise EngineException(EngineException.NOT_FOUND_ERROR("file"))
    
    def __getitem__(self, name: str):
        return self.get_value(name)
    
    def __setitem__(self, name: str, value: any):
        return self.set_value(name, value)