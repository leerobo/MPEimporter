#!/usr/bin python3
# ----------------------------------------------------------------------------
# extract the T067/T068(prod),T167/T168(test) build tmpe000 table 
# the table matches the IXMPE file that is loaded into IXMPEUPD 
# selected tables are decoded into JSON for reference screen on TCS
#   NOTE: The files loaded are the output from EVRYs-mpeUNCOMPRESS.py (EVRYMPE)
# ----------------------------------------------------------------------------
#  Version 0.0.1 - April 2021  (Used as a base but redesigned feb 2022)
#     Due to IXMPUPD onlyy working from the T068 file,  the table was
#     redesigned to hold all mpe entried and not just the TCS references
#     IP0000T1 is used to compare keys and update or ignore updates.  
#     If a T068 is loaded then TEVY007 is cleared and all T067 files after
#     the T068 header will be applied
#  Version 0.0.2 - April 2022  (Used as a base but redesigned feb 2022)
#     allow for test versions
#  Version 0.1.0 - Feb 2023  
#     Moved MPE definitions to config file and included a new build section for 
#     tmpe040(IP0040T),11(IP0041T),12(IP0072) to allow for faster access on
#     the core tables.
#  Version 0.1.1 - July 2023  
#     Changed Table names to from TEVYnnn to match MPE tables under TMPEnnn
#     Change TEVY007a to TMPE000 to hold the MPE in DB media
#     Changed Common librarys to new standard within PYbatch
#  Version 1.0.0- July 2025
#     The complexity of the GUI now needs access to all fields when searching and 
#       applying to transactions, so JSON fields at TMPE table levels.
#     MPE will be tested against Pydantic structures 
#     Will use sqlalchemy to apply Pydantic to postgresql DB
#    
# ----------------------------------------------------------------------------
import sys, os, time, datetime, io, json, configparser,ctypes ,argparse 
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml
from Common import config

#sys.path.append(os.path.join(os.path.dirname(__file__), '..', os.getenv('PYBATCH'))) 
#from models.FileDecoders import decoders
#from models.FileDecoders import encoders

from Models import MPEprocessor as MPE
# from common  import connectionsV2 as EC                #  DB connections
# from data.config.Config import Config                  #  System Level Config

#DB=EC.DataBase()                                      #  Generic DB routine
args=object
gConfigParms=object  # Config.loader

# class configLoader():

#    def __init__(self,configPath='config.yml',env='PRODUCTION'):
#       self.env = env
#       with open(configPath, 'r') as file:
#          self.config = yaml.safe_load(file)

#       self.loaded = True
#       if env not in self.config:
#          print( '*************************************')
#          print( '  Config not set for Enviroment ',args.ENV)
#          print( '*************************************')
#          self.loaded = False

#    def isLoaded(self) -> bool:
#       if self.loaded : return True
#       return False

#    def get(self,fld:str,default=None) -> str:
#       if fld in self.config[self.env]:
#          return self.config[self.env][fld]
#       return default
   
#    def has(self,fld:str) -> bool:
#       if fld in self.config[self.env]:
#          return True
#       return False


def findMPEmode(tbl):
   for i in tbl:
      if 'mode' in i : return i['mode']
   return ''   



def main():
   FULLname=''

   ts=datetime.datetime.now()           # Ready Steady Go
   if not gConfigParms.isLoaded():   return 8

   # Find the latest T*68 Full replacement based on MC file name
   if os.path.exists(gConfigParms.get('working')):
      ddir=os.listdir(gConfigParms.get('working'))
      FULLdate = 0
   else:
      print('** Error : Working Path',gConfigParms.get('working'),'Does not Exist')
      return 8

   for dd in ddir:
      if dd.find('T068')!=-1 or dd.find('T168')!=-1:  
       if int(dd.split('.')[5][1:]) > FULLdate: 
          FULLdate=int(dd.split('.')[5][1:])
          FULLname=dd

   # MPEprocess handles the decoding to JSON and storing the MPE into the TMPE tables
   #   MPEmapper holds the sequencal decoders for each MPE field within selected tables
   #   TMPEsql holds the SQLalchemy definition models 
   #  -- Note keep the fiels inline between MPEmapping and SQLalchemy settings --
   mpe=MPE.MPEprocess(gConfigParms)  # loadin MPE Decoder
   mpe.setVerbose(args.verbose)
   # mpe.setConfig(gConfigParms)       # set Decoder config parameters


   if not args.NO_MPEUPD:
      tsmpe=datetime.datetime.now()
      # Rebuild MPE tables in TMPE9999 from latest MPE >>FULL<< file if set to RELOAD
      if args.RELOAD:
         if args.verbose : print('V: MPE Full Replacment ',FULLname) 
         if not mpe.clearTMPE9999()      : return 8   # Clear TMPE9999 table which holds all MPE rows
         if not mpe.LoadMPE(FULLname)    : return 8   # Reload TMPE9999 of all mapped Tables MPEmapping

   # apply all MPE tables from latest MPE >>UPDATE<< file
      FULLdate = mpe.getLastLoadDate()                # Get Systems 'last applied MPE' date
      ddir.sort()
      for dd in ddir:
         if dd.find('T067')!=-1 or dd.find('T167')!=-1:  
            if int(dd.split('.')[5][1:]) > int(FULLdate): 
               if args.verbose : print('V: MPE update ',dd)
               if not mpe.LoadMPE(dd) :
                  print('************* Failed *************')
                  return 8           
      print('MPEimport : MPE load - Duration ',datetime.datetime.now() - tsmpe)               

   # Build an Seq IXMP (See Config) for Batch processing 
   # This is a mirror of the MPE but only select mapped tables
   if not args.NO_IXMP or args.RELOAD  :  
      tsmpe=datetime.datetime.now()
      mpe.LoadIXMP()
      print('MPEimport : IXMP Build - Duration ',datetime.datetime.now() - tsmpe)               

   # TMPE tables are used on GUI/API services (Not Batch) and 
   # are indexed for speed
   if not args.NO_TMPE or args.RELOAD  :  
      tsmpe=datetime.datetime.now()
      mpe.LoadTABLES()
      print('MPEimport : TMPE Table Build - Duration ',datetime.datetime.now() - tsmpe)               


   print('MPEimport : Duration ',datetime.datetime.now() - ts)

   return 0

# MPE processor 

if __name__=="__main__":
   parser = argparse.ArgumentParser(description='MPE Importer',epilog='Version : 1.0')          

   parser.add_argument('-v',      '--verbose',action='store_true',help='Show Processing Summary')   
   parser.add_argument('-d',      '--debug',action='store_true',  help='Show Detailed Processing')   

   parser.add_argument('--RELOAD',    action='store_true',  help='Reload from latest Full MPE and all Updates')
   parser.add_argument('--NO_MPEUPD', action='store_true',  help='Do not Apply MPE files to TMPE9999')
   parser.add_argument('--NO_TMPE',   action='store_true',  help='Do not Rebuild the TMPE Sub Tables')
   parser.add_argument('--NO_IXMP',   action='store_true', help='Do not Rebuild the IXMPI Extract File')

   parser.add_argument('--ENV',       nargs='?',  help='Config Level (PRODUCTION/TEST)',default='PRODUCTION')
   
   # parser.add_argument('--VALIDATE', action='store_true',  help='Validate The Extract Details After Process')

   args = parser.parse_args()
   print(args)
   
   # Check configs and models are present
   if not os.path.exists( './Models/MPEmapper.json' ):
      print( '*************************************')
      print( 'MPE Mapping JSON is not present  ')
      print(' Target : /Models/MPEmapper.json ' )
      print( '*************************************')
      exit(8)

   if not os.path.exists( './config.yml' ):
      print( '*************************************')
      print( 'Config Parameters are Missing  ')
      print(' Target : /config.yml ' )
      print( '*************************************')
      exit(8)

   gConfigParms=config.Loader(env=args.ENV)

   exit(main())

    