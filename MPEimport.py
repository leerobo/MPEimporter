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
   #global MPEconfig

   # configFile=io.open('/Models/MPEmapper.json' ,'r')
   # MPEconfig=json.loads(configFile.read())
   # print('MPE mapping Loaded ' )
   # print('Tables Defined ',end="")
   # for tbl in MPEconfig:
   #    if tbl[:2]=='IP': print(tbl,end="")
   #    if findMPEmode(MPEconfig[tbl]) != '' : print('('+findMPEmode(MPEconfig[tbl])+')',end="")
   #    print(', ',end="")

   # ---- start the clock 
   startTS=datetime.datetime.now()
   if not gConfigParms.isLoaded(): return 8

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

   mpe=MPE.MPEprocess(args)    # loadin MPE Decoder
   mpe.setConfig(gConfigParms) # set connfig parameters

   # Rebuild MPE tables from latest MPE >>FULL<< file

   if args.ALL or args.FULLONLY :
      if args.verbose : print('V: MPE Full Replacment ',FULLname) 
      if not mpe.LoadFile(FULLname) : return 8  #  Load full with bulk option Set

   print('FullDate:',FULLdate)

   # apply all MPE tables from latest MPE >>UPDATE<< file
   
   if args.LATEST or args.ALL:
     FULLdate=mpe.getSystemDate() 
     ddir.sort()
     UpdTot=0
     print('D: Files found ',len(ddir))
     for dd in ddir:
       print('File : ',dd,'----')
       if dd.find('T067')!=-1 or dd.find('T167')!=-1:  
        print('Date:',dd.split('.')[5][1:])           
        if int(dd.split('.')[5][1:]) >= int(FULLdate): 
           if args.verbose : print('V: MPE update ',dd)
           if not mpe.LoadFile(dd) : 
              print('************* Failed *************')
              return 8           
           UpdTot+=1
     if args.verbose : print('V: MPE ',UpdTot,'MPE Updates applied')

   if not args.NOCLEAN : CleanTables()

   # Split off select MPE tables to seperate DB Tables to help
   # speed up the GUI reference and scriptings processing 

   if args.IXMP or args.BUILD : BuildIXMP()
   if args.T40 or args.BUILD  : BuildT40()
   if args.T41 or args.BUILD  : BuildT41()
   if args.T72 or args.BUILD  : BuildT72()
   #if args.T75 or args.BUILD  : BuildT75()   # MCC/CABS
   if args.T90 or args.BUILD  : BuildT90()
   if args.T91 or args.BUILD  : BuildT91()
   #if args.T137 or args.BUILD  : BuildT137()  # 2024Q2

   return 0

def CleanTables():
    ts=datetime.datetime.now()
    if args.verbose : print('V: Clearing Tables of duplicate keys')
    # Find all the duplicates in the MPE tmpe000 
    cols,rows=DB.getSQL("select tabid,key,cnt from (select tabid,key,count(*) as cnt from tmpe000 where STAT='A' group by tabid,key) as foo  where cnt > 1;")
    if args.verbose :  print('V: Duplicates Marked ',len(rows))
    for dup in rows:
       # Find all the duplicates per key
       cols,dupRows=DB.getSQL("select tabid,key,dte,stat from tmpe000 where tabid = '{}' and key='{}' order by dte desc".format(dup[0],dup[1]))
       stat='A'
       InaCnt=0
       for upddp in dupRows:
          if stat != 'A':
             # update all but the first record with 'Inactive'
             DB.amendSQL("update tmpe000 set stat='I' where tabid = '{}' and key='{}' and dte='{}'".format(upddp[0],upddp[1],upddp[2]))
             DB.commit()
             InaCnt+=1
          stat='I'   
    return

def BuildIXMP():
   ts=datetime.datetime.now()
   if args.verbose : print('V: IXMP Extracting to',MPEconfig['SYSTEM']['IXMP']+"/IXMPI.mpe      : ",end="")
   f = open(MPEconfig['SYSTEM']['IXMP']+"/IXMPI.mpe", "w")
   prevtab=''
   recno=1
   cols,rows=DB.getSQL("select tabid,key,dte,stat,rec from tmpe000 where tabid not in ('*SYSTEM*','IP0000T1') order by tabid,key")   
   if args.verbose : print(len(rows),' Loaded (Duration:',datetime.datetime.now()-ts,')',end='')
   ts=datetime.datetime.now()
   for sysrec in rows:   
      if prevtab != sysrec[0]:
          prevtab = sysrec[0]
      ext=sysrec[2][:10]+sysrec[3][:1]+sysrec[0]+sysrec[4]
      recno+=1
      f.write(ext)
   if args.verbose : print('-- ',recno,' Processed (Duration:',datetime.datetime.now()-ts,')' )
   f.close()
   return True

# ------------------------------------------------------------  BUILD TABLES

def BuildT40():
    if args.verbose : print('------------- Table Build T40 -----------')
    ts=datetime.datetime.now()
    delRows=DB.amendSQL("delete from tmpe040")
    DB.commit()
    if args.verbose : print('T40: Table Cleared :')

    cols,rows=DB.getSQL("select recjs,dte  from tmpe000 where tabid = 'IP0040T1' and STAT='A' group by key,dte order by dte desc",Extract=10000)
    if len(rows) == 0: 
       print('T40:  No Entries found on MPE000 for table ')
       return False

    idx=0
    blklst=[]
    while(rows):
        for row in rows:
           blklst.append([ row[0]['IssuerBinLow'],row[0]['IssuerBinHi'],row[0]['CPI'],row[0]['ProdId'], \
                           row[0]['ProrityIndex'],row[0]['Region'],row[0]['MemberId'],json.dumps(row[0]) ])
           idx+=1
        cols,rows=DB.getSQL(Extract=10000)    #  get next 10000

    if args.verbose : print('T40: Total Entrys Extracted - ',idx)
    try:
       DB.batchSQL('insert into tmpe040 values(%s,%s,%s,%s,%s,%s,%s,%s)', blklst)
       if args.verbose : print('T40: Entrys Applied ')
    except Exception as ex:
       print('T40: Error Applying Entries')
       return False
   
    DB.commit()
    if args.verbose : print('T40: Duration:',datetime.datetime.now()-ts)

    return True

def BuildT41():
    ts=datetime.datetime.now()
    delRows=DB.amendSQL("delete from tmpe041")
    DB.commit()
    if args.verbose : print('V: TMPE041 cleared :',end="")

    cols,rows=DB.getSQL("SELECT recjs,key,dte FROM tmpe000 where tabid='IP0041T1' order by recjs->'memberId' asc")
    print(len(rows),' Extracted ',end="")
    newrow={}
    idx=0
    for row in rows:
       if 'memberid' in newrow and newrow['memberid'] != row[0]['memberId'] :
           sql="insert into tmpe041 values('"+newrow['memberid']+"','{"+",".join(str(x) for x in newrow['CPI'])+"}', \
           '{"+",".join(str(x) for x in newrow['regions'])+"}' , \
           '"+newrow['endpoint']+"','"+newrow['ucaf']+"', \
           '{"+",".join(str(x) for x in newrow['countrys'])+"}' , \
           '{"+",".join(str(x) for x in newrow['acqbin'])+"}'  )"
           DB.amendSQL(sql)
           newrow.clear()
           idx+=1

       newrow['memberid']=row[0]['memberId']
       newrow['endpoint']=row[0]['endPoint']
       newrow['ucaf']=row[0]['UCAF']

       if 'CPI' not in newrow : newrow['CPI']=[]
       if row[0]['CPI'] not in newrow['CPI']:
          newrow['CPI'].append(row[0]['CPI'])

       if 'regions' not in newrow : newrow['regions']=[]
       for regarr in row[0]['regions']:
         if regarr['region'] !='' and regarr['region'] not in newrow['regions']: 
            newrow['regions'].append(regarr['region'])

       if 'countrys' not in newrow : newrow['countrys']=[]
       for cntryarr in row[0]['countrys']:       
         if cntryarr['country'] != ''  and cntryarr['country'] not in newrow['countrys']:
             newrow['countrys'].append(cntryarr['country'])

       if 'acqbin' not in newrow : newrow['acqbin']=[]
       if row[0]['acquirerId'] not in newrow['acqbin']:
          newrow['acqbin'].append(row[0]['acquirerId'])

    if args.verbose : print(idx,'Committed  (Duration:',datetime.datetime.now()-ts,')')
    DB.commit()
    return True

 

def BuildT72():
    ts=datetime.datetime.now()

    delRows=DB.amendSQL("delete from tmpe072")
    DB.commit()
    if args.verbose : print('V: TMPE072 cleared :',end="")

    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0072T1' and stat='A' order by recjs->'MBRID' asc")
    print(len(rows),' Extracted ',end="")
    newrow={}
    for row in rows:
       try:
         sql="insert into tmpe072 values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".\
              format(row[0]['MEMBER'],row[0]['REG'],row[0]['EEA'],row[0]['IEI'],row[0]['ATM'],row[0]['ENDP'], \
              row[0]['MECI'],row[0]['CCISO'],row[0]['CCODE'],row[0]['SWITCH'],row[0]['MERNAME'] )
         DB.amendSQL(sql)    
       except Exception as ex:
          print('>>>',row)
          print('<<<',ex)  
          break

    if args.verbose : print('(Duration:',datetime.datetime.now()-ts,')')
    DB.commit()
    return True

def BuildT75():
    ts=datetime.datetime.now()
    delRows=DB.amendSQL("delete from tmpe075")
    if args.verbose : print('V: TMPE075 cleared :',end="")
    DB.commit()

    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0075T1' and stat='A'",Extract=10000)
    idx=0
    blklst=[]
    while(rows):
        for row in rows:
           blklst.append([row[0]['MCC'],row[0]['CAB'],row[0]['life'], \
                         row[0]['MCCtype'],row[0]['flag'],row[0]['filler']])
           idx+=1
        cols,rows = DB.getSQL(Extract=10000)

    if args.verbose : print(idx,'Extracted  --',end="")
    DB.batchSQL('insert into tmpe075 values(%s,%s,%s,%s,%s,%s)', blklst)
    if args.verbose :  print(' (Duration:',datetime.datetime.now()-ts,')')

    DB.commit()
    return True

def BuildT90():
    ts=datetime.datetime.now()
    print('Building T90 ',ts)
    
    delRows=DB.amendSQL("delete from tmpe090")
    DB.commit()
    if args.verbose : print('V: TMPE090 cleared :',end="")

    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0090T1' and stat='A'",Extract=10000)
    idx=0
    blklst=[]

    while(rows):
        for row in rows:
           blklst.append([row[0]['BinLow'],row[0]['BinHi'], \
                     row[0]['BSApriority']+row[0]['BSAagreement'],row[0]['BSApriority'], \
                     row[0]['CPI'],  row[0]['CPIpriority'], \
                     row[0]['LifeCycleInd'],row[0]['EnforcementInd']])
           idx+=1
        cols,rows=DB.getSQL(Extract=10000)

    if args.verbose : print(idx,'Extracted  --',end="")
    DB.batchSQL('insert into tmpe090 values(%s,%s,%s,%s,%s,%s,%s,%s)', blklst)
    if args.verbose : print('(Duration:',datetime.datetime.now()-ts,')')

    DB.commit()
    print('.... complete ',datetime.datetime.now()-ts)
    return True

def BuildT91():
    ts=datetime.datetime.now()
    if args.verbose : print('V: TMPE091 cleared :',end="")
    delRows=DB.amendSQL("delete from tmpe091")
    DB.commit()
    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0091T1' and stat='A'",Extract=10000)

    #rows = acqCursor.fetchall()
    #print(len(rows),' Extracted ',end="")
    #print('--------------')
    #cols = [i[0] for i in acqCursor.description]
    #newrow={}
    #for row in rows:
    #   try:
    #     sql="insert into tmpe091 values('{}','{}','{}','{}','{}','{}')".\
    #          format(row[0]['AcquirerBin'],row[0]['BSAagreement'],row[0]['BSAagreement'][:1], \
    #                 row[0]['CPI'],row[0]['priority'],row[0]['LifeCycleInd'])
    #     acqCursor.execute(sql)    
    #   except Exception as ex:
    #      print('>>>',row)
    #      print('<<<',ex)  
    #      break

    idx=0
    blklst=[]
    while(rows):
        for row in rows:
           blklst.append([row[0]['AcquirerBin'],row[0]['BSAagreement'],row[0]['BSAagreement'][:1], \
                         row[0]['CPI'],row[0]['priority'],row[0]['LifeCycleInd']])
           idx+=1
        cols,rows = DB.getSQL(Extract=10000)

    if args.verbose : print(idx,'Extracted  --',end="")
    DB.batchSQL('insert into tmpe091 values(%s,%s,%s,%s,%s,%s)', blklst)
    if args.verbose :  print(' (Duration:',datetime.datetime.now()-ts,')')

    DB.commit()
    return True

def BuildT95():
    ts=datetime.datetime.now()
    if args.verbose : print('V: TMPE095 cleared :',end="")
    delRows=DB.amendSQL("delete from tmpe095")
    DB.commit()
    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0095T1' and stat='A'",Extract=10000)
    idx=0
    blklst=[]
    while(rows):
        for row in rows:
           blklst.append([row[0]['CPI'],row[0]['BSAagreement'][0:1],row[0]['BSAagreement'][1:], \
                         row[0]['BSA'],row[0]['IRD'],row[0]['CAB'],row[0]['life']])
           idx+=1
        cols,rows = DB.getSQL(Extract=10000)

    if args.verbose : print(idx,'Extracted  --',end="")
    DB.batchSQL('insert into tmpe095 values(%s,%s,%s,%s,%s,%s)', blklst)
    if args.verbose :  print(' (Duration:',datetime.datetime.now()-ts,')')

    DB.commit()
    return True

def BuildT137():
    ts=datetime.datetime.now()
    if args.verbose : print('V: TMPE137 cleared :',end="")
    delRows=DB.amendSQL("delete from tmpe137")
    DB.commit()
    cols,rows=DB.getSQL("SELECT recjs FROM tmpe000 where tabid='IP0137T1' and stat='A'",Extract=10000)
    idx=0
    blklst=[]
    while(rows):
        for row in rows:
           blklst.append([row[0]['AcquirerBin'],row[0]['BSAagreement'],row[0]['BSAagreement'][:1], \
                         row[0]['CPI'],row[0]['priority'],row[0]['LifeCycleInd']])
           idx+=1
        cols,rows = DB.getSQL(Extract=10000)

    if args.verbose : print(idx,'Extracted  --',end="")
    DB.batchSQL('insert into tmpe091 values(%s,%s,%s,%s,%s,%s)', blklst)
    if args.verbose :  print(' (Duration:',datetime.datetime.now()-ts,')')

    DB.commit()
    return True


# MPE processor 

if __name__=="__main__":
   parser = argparse.ArgumentParser(description='MPE Importer',epilog='Version : 1.0')          

   parser.add_argument('-v',      '--verbose',action='store_true',help='Show Processing Summary')   
   parser.add_argument('-d',      '--debug',action='store_true',  help='Show Detailed Processing')   
   parser.add_argument('--LATEST',    action='store_true',  help='Apply MPE Updated')   
   parser.add_argument('--BUILD',     action='store_true',  help='Build TMPEnnn and IXMPI Tables')   
   parser.add_argument('--VERSION',   action='store_true',  help='Show Version')   
   parser.add_argument('--ALL',       action='store_true',  help='Rebuild from latest Full update and apply Updated')   
   parser.add_argument('--FULLONLY',  action='store_true',  help='Rebuild from latest Full update')   
   parser.add_argument('--NOCLEAN' ,  action='store_true',  help='Supress Clean of MPE of duplicates')  
   parser.add_argument('--EXTRACTALL',action='store_true',  help='Extracts to TMPE000 all tables not just the ones Defined in the Config')  

   parser.add_argument('--ENV',       nargs='?',  help='Config Level (PRODUCTION/TEST)',default='PRODUCTION')
   

   parser.add_argument('--VALIDATE', action='store_true',  help='Validate The Extract Details After Process')

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

    