#!/usr/bin python3

"""
   MPE (model) : Extract out MPE tables based on the MPE.json config 

    Change : Lero - 2023-7-17 : Import new decoders 
    Change : Lero - 2023-7-20 : New PYbatch standard

"""

import datetime ,io, configparser,json,os,sys
from Common import config

from sqlalchemy import create_engine, Column, Integer, String, delete, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base

import Models.sqlAlchemy.TMPEsql as TMPEsql

# from common  import connections as EC   #  DB connections

class MPEprocess(object):
   def __init__(self,args):
     self.args=args
     print('MPEprocess',args)
     self.Rsrc   = 'UNK'
     self.Frec   = ''
     self.mpeName = ''
     self.TABkey = ''
     self.tabcnt = 1                    # Amount of rows in a Table
     self.KYofs  = 0
     self.KYofe  = 0
     self.status = 'Connected'
     self.TSsrt  = datetime.datetime.now()
     self.bulkRec = []*50000
     self.useBulk = False
     self.FullReplacement=False
     self.stub='' 
     # self.DB=EC.DataBase()                        #  Generic DB routine
     #self.MPEconfig=MPE.json
     MPEmapper=io.open('./Models/MPEmapper.json','r')
     self.MPEmapper=json.loads(MPEmapper.read())
     self.verbose=False

     DATABASE_URL = "postgresql://postgres:1970Terry@localhost:5432/postgres"   
     self.engine = create_engine(DATABASE_URL, echo=False)  # True shows log
     self.session = Session(bind=self.engine)
     try:
        connection = self.engine.connect()
        print("DB Connection successful!")
        connection.close()
        sqlAbase = declarative_base()
        sqlAbase.metadata.create_all(self.engine)
     except Exception as e:
        print(f"Connection failed: {e}")
        
     self.metadata = MetaData()
     self.metadata.reflect(bind=self.engine)



  
 
   def setConfig(self,runParms:config.Loader) -> bool:
      self.runParms = runParms
      return True
   def setVerbose(self,verbose:bool):
      self.verbose=verbose

   def getREC(self):
     return self.Frec[19:]
   def getRecDate(self):
     return self.Frec[:10]
   def getRecordStatus(self):
     return self.Frec[10:11]
   def getTAB(self,msk='0000'):
     tabid=list(self.Frec[11:19])
     idx=2
     for mskchar in msk :
        if mskchar != '0' : tabid[idx]=mskchar
        idx+=1
     return "".join(tabid)

   def getFULL(self):
     return self.Frec
   
   def getSYSTEM(self) -> TMPEsql.TMPE000:    # Return System record 
     systemrec=self.session.query( TMPEsql.TMPE000).filter_by(tableid='*SYSTEM*').one_or_none()
     if not systemrec :  return None
     return systemrec
   
   def getSystemDate(self) -> int:   # Return MPE last applied system date
     systemrec=self.session.query( TMPEsql.TMPE000).filter_by(tableid='*SYSTEM*').one_or_none()
     print('getSystemDate : ',systemrec.createdate)
     if not systemrec :  return 0
     return systemrec.createdate
   
   def getTABLEname(self,tabName:str) -> TMPEsql.TMPE000:
     systemrec=self.session.query(TMPEsql.TMPE000).filter_by(tableid=tabName).one_or_none()
     return systemrec.TMPEsql.TMPE000

  #  def addSYSTEMtag(self,tag,val):
     
  #    cols,rows=self.DB.getSQL("select dte,recjs from tmpe000 where key ='*SYSTEM*'")
  #    print(val,':ADD tag:',tag,'-',rows[0],':',cols)
  #    if rows[0][1]==None: 
  #      sysdte = 0
  #      sysval = {}
  #    else:
  #      sysdte = rows[0][0]
  #      sysval = rows[0][1]
  #    if tag == 'LSTupd' : sysdte = val
  #    sysval[tag]=val
  #    self.DB.amendSQL("update tmpe000 set recjs='{}' , dte='{}' where key ='*SYSTEM*'".format(json.dumps(sysval),sysdte) )
  #    return True

   ''' Load MPE file and decode based on MPEmapper.json and IO via TMPEsql settings '''
   def LoadFile(self,mpeName):
     self.mpeName=mpeName
     ts=datetime.datetime.now()
     
     try:
        if self.verbose : print('V: Loading MPE - ',mpeName)
        tableCnt=0
        fileCnt=0
        
        with open(self.runParms.get('working')+'/'+mpeName,"rb") as mpeFile:

          for mpeRecBytes in mpeFile:
            if mpeRecBytes.find(b'\n')  > 0 :
               eol='\n'
            else:
               raise IOError("Check File {} Format, No CRLF/EOL Found".format(mpeName))
            
            mpeRec=mpeRecBytes.decode('utf-8')
            status=mpeRec[10:11]
            tableid=mpeRec[11:19]
            fileCnt+=1

            # Check Headers and trailers
            if tableid == ' FILE IP' :
                print(tableid,' :FILEIP: ',mpeRec)
                if mpeRec[:19].find('UPDATE') > -1:
                  if self.verbose : print('Loading UPDATE MPE file')
                  self.FullReplacement=False
                elif mpeRec[:19].find('REPLACE') > -1:
                  if self.verbose : print('Loading Full Replacement MPE file')
                  self.session.query(TMPEsql.TMPE000).delete()
                  self.FullReplacement=True

            elif mpeRec[:19].find('TRAILER') > -1:
                  if tableCnt > 0:
                    self.session.merge(TMPEsql.TMPE000(tableid=tableid,processedrows=tableCnt,mpename=mpeName) )
                  tableCnt=0
                  self.session.commit()
              
            elif tableid == 'IP0000T1' and status == 'A' :
              decodedRec=self.__decodeEntry(tableid,mpeRec)
              if self.verbose : print(tableid,'--',decodedRec)
              self.session.add(TMPEsql.TMPE000(**decodedRec) )
              tableCnt+=1

            elif tableid in self.MPEmapper and status == 'A' :
              tableObj=TMPEsql.get_model_by_tableid(tableid)
              if tableObj != None:
                decodedRec=self.__decodeEntry(tableid,mpeRec)
                DBdecoded = {k.lower(): v for k, v in decodedRec.items()}
                self.session.merge(tableObj(**DBdecoded) )
                
              tableCnt+=1
            
     except Exception as ex:
       raise IOError(ex) from ex

     self.session.commit()
     
     if self.verbose : print(' File',mpeName,'Processed    Records:',fileCnt,'    Duration:',datetime.datetime.now()-ts )
     print(' File ',mpeName,'   Records:',fileCnt,'    Duration:',datetime.datetime.now()-ts )

     # Flag System Tag as last MPE processed and applied 
     self.session.merge(TMPEsql.TMPE000(tableid='*SYSTEM*',description="system level row",createdate=mpeName.split('.')[5][1:],mpename=mpeName,processedrows=fileCnt) )
     self.session.commit()

     return True

  #  def __processRecord(self,MPErec):

  #    # Check Headers and trailers
  #    if MPErec[:19].find(b'UPDATE') > -1:
  #       ts = datetime.datetime.now()
  #       self.FileTS=MPErec[15:27].decode('utf-8')
  #       return True

  #    if MPErec[:19].find(b'REPLACE') > -1:
  #       ts = datetime.datetime.now()
  #       self.__newBuild()
  #       self.FullReplacement=True
  #       return True

  #    if MPErec[:19].find(b'TRAILER') > -1:
  #    #  check table counters here
  #       if (self.verbose and self.tabcnt > 1 ): 
  #          extracted='** Extracted {} Entries **'.format(self.tabcnt-1)
  #          print('VD: MPE Table-',self.getTABLEname(MPErec[15:23].decode('utf-8')),':  Count:',MPErec[25:33].decode('utf-8'),\
  #                ' ( Dur:',(datetime.datetime.now()-self.TSsrt),')' ,extracted)
  #       self.TSsrt=datetime.datetime.now()
  #       self.tabcnt = 1
  #       return True

  #   # Process MPE table entry - Pre Validation
  #    self.Frec   = self.__preMPErec(MPErec)

  #    self.status = 'Loaded'
  #    if len(self.Frec) < 4:    # allow for EOL marker 
  #       print('End of MPE Reached')
  #       return False
  #    else: 
  #      if self.getRecDate()[0:2] not in ('20','19','21') : self.status = 'Invalid Date' 
  #      if self.getTAB()[0:2] != 'IP'                     : self.status = 'Invalid Table'
  #      if self.getRecordStatus()[0:2] not in ('A','I')   : self.status = 'Invalid Status'
  #      if self.status != 'Loaded': 
  #         print('False:001-Loaded :',self.status)
  #         print('>>',self.Frec,'<<')
  #         return False

  #    #  Get Table Key and off set details from TMPE000 table list  
  #   #  try:
  #   #      decodedKey = self.session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid == self.getTAB() ).one_or_none()
  #   #      if not decodedKey :
  #   #         print('Table Not in IP0000T1 List',self.getTAB() )
  #   #         return False
  #   #  except Exception as ex:
  #   #      print('Table IP0000T1 error',ex )
  #   #      return False


  #    #  Decode the MPE table entry 
  #    decodedRec={}
  #    if self.getTAB() in self.config:     #     based on config (only save table if set)
  #       decodedRec=self.__decodeEntry()

  #       # TODO : Decoder for B-8 Ps-7 in extractor could be by wrong IP0053T array is out of line  

  #    # Table list Control IP0000T1
  #    if (self.getTAB() == 'IP0000T1'):
  #       try:
  #           print('Add TMPE000 :',json.dumps(decodedRec) )
  #           self.session.add(TMPEsql.TMPE000(**decodedRec) )
  #           self.session.commit()
  #       except Exception as ex:
  #           print('/n------------------ TMPE000 Error ------------------')
  #           print('IP0000T1 Insert error ',ex)
  #           print('JS :',decodedRec)
  #           return False
  #   #  else:
  #   #     try:
  #   #         print('Add TMPE000 :',json.dumps(decodedRec))
  #   #         self.session.add(TMPEsql.TMPE000(**decodedRec) )
  #   #         self.session.commit()
  #   #     except Exception as ex:
  #   #         print('/n------------------ TMPE000 Error ------------------')
  #   #         print('IP0000T1 Insert error ',ex)
  #   #         print('JS :',decodedRec)
  #   #         return False
         

  #    return True

   def __decodeEntry(self,tableid,mpeRec:bytes) -> dict|None:
     # Decode the MPE table based on MPEmapper JSON seq settings
     recJS={}
     tabMap=self.MPEmapper[tableid]  #  Extract the JSON definition from MPEmapper
     # stub=mpeRec[:19]
     ofs=19                          # Skip over Stub for Date,status,table id
     try:
          for entry in tabMap:
            if   'startOfset' in entry :
              ofs+=entry['startOfset']
            elif 'seq'      in entry: # extract seq from stub
               recJS[entry['seq']]=self.tabcnt

            elif 'field'      in entry:
              ln=int(entry['length'])
              recJS[entry['field']]=mpeRec[ofs:ofs+ln].strip()
              ofs+=ln

            elif 'array' in entry :
              # If its a field then accept the field for the loop times
              # otherwise its a number .
              if entry['array']['times'] in recJS:    # Fixed Loop Counter
                    loopTot=int(recJS[entry['array']['times']])
              else: loopTot=entry['array']['times']   # Based on field setting

              if 'name' in entry['array']:  loopName=entry['array']['name']
              else: loopName='Array'

              loopIdx=0
              loop=[{}]*loopTot
              while loopIdx < loopTot and ofs < len(mpeRec)-3: # +3 is the CLFD
                loop[loopIdx]={}
                for loopEntry in entry['array']['loop']:
                  ln=int(loopEntry['length'])
                  loop[loopIdx][loopEntry['field']]=mpeRec[ofs:ofs+ln].strip()
                  ofs+=ln
                loopIdx+=1
              #if self.verbose :  print(loopIdx,'--',loop[:loopIdx],self.Frec)
              recJS[loopName]=loop[:loopIdx]

     except Exception as ex:
          print('------------------------------ Error ----------------------')
          print('Error :', ex)
          print('Ofset :',ofs,':  Idx',loopIdx,':  Tot',loopTot)
          print('Loop  :',loop)
          print('stub  :',self.stub) 
          print('Rec   :',self.Frec) 
          return False

     return recJS

 

   # Call if this is a new build run
  #  def __newBuild(self):
  #   try:
  #       if self.verbose : print("Table TMPE000 Cleared")
  #       self.session.query(TMPEsql.TMPE000).delete()
  #       self.session.add(TMPEsql.TMPE000(tabid="*SYSTEM*",key="*SYSTEM*",createdate="20200220"))
  #       self.session.commit()
  #   except Exception as ex:
  #      print("tmpe000 Clear Error :",ex)

   def __preMPErec(self,rec):
     ln=0
     rec=rec.replace(b'\xa0',b'@')
     for chr in rec.decode('utf-8'):
       if hex(ord(chr)) == '0x0': break
       ln+=1
     if ln != len(rec):
       if self.verbose : print('D: MPE:MPErecCLS: Low-Values Found in Record')
       rec=rec[:ln]
     lv=rec.find(b"'")
     if lv >=0:
        rec=rec.replace(b"'",b" ")
     return rec.decode('utf-8')
   
  #  # Call at the end of the file to set header dates
  #  def __fileComplete(self):
  #    self.addSYSTEMtag('LSTupd',self.mpeName.split('.')[5][1:])
  #    self.addSYSTEMtag('LSTtype',self.mpeName.split('.')[2])
  #    self.addSYSTEMtag('LSTmpe',self.mpeName)
  #    # self.DB.commit()
   
   # Return key off set as defined by IP0000T1 
   def __tabkey(self) -> TMPEsql.TMPE000:
     if self.getTAB() == 'IP0000T1':   return self.getREC()[0:8]
     if self.getTAB() == self.TABkey : return self.getFULL()[self.KYofs:self.KYofe]

     try:
        results = self.session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid == self.getTAB() ).one_or_none()
        return results
     except Exception as ex:
        print('__tabkey: Error ',ex)
     
    #  # cols,rows=self.DB.getSQL("SELECT recjs from TMPE000 where tabid='IP0000T1' and key='{}'".format(self.getTAB()) )
    #  if len(results) == 0 : 
    #     self.status=self.getTAB()+' Not found in IP0000T1'
    #     return ''
    #  else:
    #     ofs=int(results[0].keyofs)+10
    #     ofe=int(results[0].keylength)
    #     self.TABkey = self.getTAB()
    #     self.KYofs = ofs
    #     self.KYofe = ofe
    #     return self.getFULL()[ofs:ofe]


