import yaml

class Loader():

   def __init__(self,configPath='config.yml',env='PRODUCTION'):
      self.env = env
      with open(configPath, 'r') as file:
         self.config = yaml.safe_load(file)

      self.loaded = True
      if env not in self.config:
         print( '*************************************')
         print( '  Config not set for Enviroment ',env)
         print( '*************************************')
         self.loaded = False

   def isLoaded(self) -> bool:
      if self.loaded : return True
      return False

   def get(self,fld:str,default=None) -> str:
      if fld in self.config[self.env]:
         return self.config[self.env][fld]
      return default
   
   def has(self,fld:str) -> bool:
      if fld in self.config[self.env]:
         return True
      return False

