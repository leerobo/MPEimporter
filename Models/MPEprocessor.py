#!/usr/bin python3

"""
MPE (model) : Extract out MPE tables based on the MPE.json config

 Change : Lero - 2023-7-17 : Import new decoders
 Change : Lero - 2023-7-20 : New PYbatch standard

"""

import datetime, io, configparser, json, os, sys, traceback
from Common import config

from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, delete, MetaData, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base

import Models.sqlAlchemy.TMPEsql as TMPEsql

# from common  import connections as EC   #  DB connections


class MPEprocess(object):
    def __init__(self, runParms: config.Loader=None):
        # self.Rsrc = "UNK"
        # self.Frec = ""
        # self.mpeName = ""
        # self.TABkey = ""
        # self.tabcnt = 1  # Amount of rows in a Table
        # self.KYofs = 0
        # self.KYofe = 0
        # self.status = "Connected"
        # self.TSsrt = datetime.datetime.now()
        # self.bulkRec = [] * 50000
        # self.useBulk = False
        self.FullReplacement = False
        self.verbose = False        
        self.runParms = runParms
        self.engine = None
        self.blocks = 20000

        # self.stub = ""
        # self.DB=EC.DataBase()                        #  Generic DB routine
        # self.MPEconfig=MPE.json
        MPEmapper = io.open("./Models/MPEmapper.json", "r")
        self.MPEmapper = json.loads(MPEmapper.read())
        self.applyConfigs()

    def setConfig(self, runParms: config.Loader) -> bool:
        """ Load the Config.yml Settings into MPE processor """
        self.runParms = runParms
        self.applyConfigs()
        return True
    
    def applyConfigs(self):
          
          if self.runParms.get("blocks") < 1000:
             print('Config Warning : Blocks too Low to be effective')
          else:
             self.blocks=self.runParms.get("blocks")

          if self.runParms == None :
              self.engine = None
              return

          if self.engine != None : self.engine.disconnect()
          DATABASE_URL = self.runParms.get("database")
          self.engine = create_engine(DATABASE_URL, echo=False)  # True shows log
          self.Session = sessionmaker(bind=self.engine)

          # connection = self.engine.connect()
          # print("DB Connection successful!")
          # connection.close()
          # sqlAbase = declarative_base()
          # sqlAbase.metadata.create_all(self.engine)          




    def setVerbose(self, verbose: bool):
        """ Set to true to receive more log output during processing """
        self.verbose = verbose

    # def getREC(self):
    #     return self.Frec[19:]

    # def getRecDate(self):
    #     return self.Frec[:10]

    # def getRecordStatus(self):
    #     return self.Frec[10:11]

    # def getTAB(self, msk="0000"):
    #     tabid = list(self.Frec[11:19])
    #     idx = 2
    #     for mskchar in msk:
    #         if mskchar != "0":
    #             tabid[idx] = mskchar
    #         idx += 1
    #     return "".join(tabid)

    # def getFULL(self):
    #     return self.Frec

    def getLastLoadDate(self) -> int:             # Return MPE last applied system date
        try:
            with self.session_scope() as session:     # Setup a DB Session
               systemrec = session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid=="*SYSTEM*").first()
               if systemrec == None:  return 0
               return systemrec.createdate
        except Exception as ex:
          print(ex)  
          return None  
        

    # def getTABLEname(self, tabName: str) -> TMPEsql.TMPE000:
    #     with self.session_scope() as session:  # Setup a DB Session
    #         systemrec = (
    #             session.query(TMPEsql.TMPE000).filter_by(tableid=tabName).one_or_none()
    #         )
    #     return systemrec.TMPEsql.TMPE000

    """ Load MPE file and decode based on MPEmapper.json and IO via TMPEsql settings """

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as ex:
            session.rollback()
            print('/n SQLalchemy Error : MPE connection : ',ex)
            traceback.print_exc()
            raise
        finally:
            session.close()

    def clearTables(self) -> bool:
        """ Delete all Mapped MPE tables """
        with self.session_scope() as session:  # One session per Delete
            for tbl in self.MPEmapper.keys():
                tableObj = TMPEsql.get_model_by_tableid(tbl)
                if tableObj != None:
                    print("Clearing table ", tbl)
                    tableObj = TMPEsql.get_model_by_tableid(tbl)
                    session.query(tableObj).delete()
            session.commit()
        return True
    
    def clearTMPE9999(self) -> bool:
        """  Delete all MPE entries """
        with self.session_scope() as session:  # One session per Delete
             session.query(TMPEsql.TMPE9999).delete()
             session.commit()
             print("Complete MPE table Cleared  (TMPE9999)")
        return True

    def LoadMPE(self, mpeName) -> bool:
        """ ### Load the TMPE9999 MPE Tables and TMPE000 Index table
          TMPE9999 holds the tables defined within the MPEmapping json config
          for a full reload,  remove the original TMPE9999 via clearTMP9999 as the
          entrys are added to the table for speed
          for an updates,  with override the TMPE9999 entrys or add if not there 
        """
        ts = datetime.datetime.now()
        tblts = datetime.datetime.now()
        newTable = True
        keyofs=0
        keylength=0

        #showTable = 'IP0048T1'  # Set to table name to log records
        showStart=3650
        showEnd=3700
        showTable = None        # dont show any table details 

        try:
            if self.verbose:     print("V: Loading MPE - ", mpeName)
            tableCnt={'A':0,'I':0,'U':0,'D':0,'X':0,'T':0}
            fileCnt = 0
            prevKey=''

            with open(self.runParms.get("working") + "/" + mpeName, "rb") as mpeFile:  # Open MPE Decoded ASCII file

                with self.session_scope() as session:       # Setup a DB Session
                    for mpeRecBytes in mpeFile:             # Read Each MPE record and apply
                        
                        if mpeRecBytes.find(b"\n") > 0:    eol = "\n"
                        else:
                            raise IOError("Check File {} Format, No CRLF/EOL Found".format(mpeName))

                        mpeRec = mpeRecBytes.decode("utf-8")
                        status = mpeRec[10:11]
                        hdrid = mpeRec[11:19]
                        fileCnt += 1

                        # Check Headers and trailers
                        if mpeRec[:6]=="UPDATE":
                                if self.verbose:                                    print("Loading >>> UPDATE <<< ",mpeName)
                                self.FullReplacement = False

                        elif mpeRec[:7]=="REPLACE":
                                if self.verbose:                                    print("Loading >>> REPLACEMENT <<< mpeName")
                                session.query(TMPEsql.TMPE000).delete()
                                self.FullReplacement = True

                        elif mpeRec[:7]=="TRAILER":
                            if tableCnt['A'] >= 1 or tableCnt['I'] >= 1 or tableCnt['D'] >= 1 or tableCnt['U'] >= 1 :
                                print("Processed Table ",tableid,"   Duration:",datetime.datetime.now() - tblts, end="")
                                print("  Total:",str(tableCnt['T']).rjust(8),'>>',end="")
                                if tableCnt['A'] > 0 : print("     Added:",str(tableCnt['A']).rjust(8),end="")
                                if tableCnt['I'] > 0 : print("  Inactive:",str(tableCnt['I']).rjust(8),end="")
                                if tableCnt['X'] > 0 : print("   Ignored:",str(tableCnt['X']).rjust(8),end="")
                                if tableCnt['D'] > 0 : print("   Deleted:",str(tableCnt['D']).rjust(8),end="")
                                if tableCnt['U'] > 0 : print("   Updated:",str(tableCnt['U']).rjust(8),end="")
                                print("")
                            tblts = datetime.datetime.now()
                            tableCnt={'A':0,'I':0,'U':0,'D':0,'X':0,'T':0}
                            session.commit()            # Commit Table to TMPE9999
                            newTable = True
 
                        else:
                            tableid = mpeRec[11:19]

                            if tableid == "IP0000T1":                                  # Update the TMPE000 Main Index
                                tableCnt['T'] += 1
                                decodedRec = self.__decodeEntry(tableid, mpeRec)
                                if self.verbose:                                    print('V:',tableid, "--", decodedRec)
                                decodedRec['mpename']=mpeName
                                if self.FullReplacement:
                                   if status == "A":
                                      session.add(TMPEsql.TMPE000(**decodedRec))
                                      tableCnt['A'] += 1
                                   else:
                                      tableCnt['I'] += 1
                                else:
                                   if status == "A":
                                      session.merge(TMPEsql.TMPE000(**decodedRec))
                                      tableCnt['U'] += 1
                                   else:
                                      checkRec=session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid==tableid).one_or_none()
                                      if checkRec != None :
                                          session.delete(checkRec)
                                          tableCnt['D'] += 1
                                      else:    
                                          tableCnt['I'] += 1

                            else:

                              if newTable :                                             # TMPE999 Key offsets
                                cntlr=session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid==tableid).first()
                                keyofs=cntlr.keyofs+10                                  # Calculate New tables Key offset
                                keylength=cntlr.keylength
                                newTable = False

                              tableCnt['T'] += 1
                              if 'mode' in self.MPEmapper and self.MPEmapper['mode']=='skip':
                                  tableCnt['X'] += 1

                              elif tableid in self.MPEmapper   :                          # Build TMPE9999 of all rows from MPE if mapped
                                decodedRec = self.__decodeEntry(tableid, mpeRec)
                                decodedRecLC = { k.lower(): v for k, v in decodedRec.items() }

                                # -------------------------------------------------------------------------------------------------------
                                if tableid == showTable and self.verbose:                 # -- For Debuging MPE 
                                    if tableCnt['T'] > showStart and tableCnt['T'] < showEnd:
                                       print(tableCnt['T'],':Debug:',status,':',tableid,'(',mpeRec[keyofs:keylength],')',decodedRecLC)
                                # -------------------------------------------------------------------------------------------------------

                                if mpeRec[keyofs:keylength] == prevKey and self.FullReplacement   :   # Shouldnt Happen but does
                                       if self.verbose :
                                          print(tableCnt['T'],':Duplicate:',status,':',tableid,'(',mpeRec[keyofs:keylength],')',decodedRecLC)
                                       tableCnt['X'] += 1
                                
                                elif self.FullReplacement:
                                   if status == 'A':
                                      session.add(TMPEsql.TMPE9999(tableid=tableid,mpekey=mpeRec[keyofs:keylength],dte=mpeRec[:10],status=status,source=mpeName,record=mpeRec,recordjson=decodedRecLC) )
                                      tableCnt['A'] += 1
                                   else:
                                      tableCnt['I'] += 1

                                else:
                                   if 'fullonly' in self.MPEmapper[tableid] and self.MPEmapper[tableid]['fullonly']:
                                      tableCnt['X'] += 1
                                   else:
                                      if status == 'A':
                                        session.merge(TMPEsql.TMPE9999(tableid=tableid,mpekey=mpeRec[keyofs:keylength],dte=mpeRec[:10],status=status,source=mpeName,record=mpeRec,recordjson=decodedRecLC) )
                                        tableCnt['A'] += 1
                                      else:  
                                         checkRec=session.query(TMPEsql.TMPE9999).filter(TMPEsql.TMPE9999.tableid==tableid,TMPEsql.TMPE9999.mpekey==mpeRec[keyofs:keylength]).one_or_none()
                                         if checkRec == None :
                                            tableCnt['I'] += 1
                                            # print(keyofs,':',keylength,'Inactive:',mpeRec[keyofs:keylength],'>>',mpeRec[:-1])
                                         else:
                                            session.delete(checkRec)
                                            tableCnt['D'] += 1
                                prevKey=mpeRec[keyofs:keylength]                                                


                    # Update TMPE000 Main Index *SYSTEM* to hold the applied MPE file name and date
                    session.merge(TMPEsql.TMPE000(tableid="*SYSTEM*",description="system level row",createdate=mpeName.split(".")[5][1:],mpename=mpeName,processedrows=fileCnt,)
                    )

        except Exception as ex:
            print(tableid, "(", tableCnt, ") : ", ex)             # opps
            return False
            # raise IOError(ex) from ex

        if self.verbose:   print("V: File",mpeName,"Processed    Records:",fileCnt,"    Duration:", datetime.datetime.now() - ts, )
        return True

    def LoadTABLES(self) -> bool:
        """ ###Using all MPEmapping tables 
           Based on TMPE9999, Rebuild the TMPE tables as defined within MPEmapping
        """
        ts = datetime.datetime.now()
        tableCnt = 0
        try:
            if self.verbose:   print("V: Loading TMPE  Tables ")
            with self.session_scope() as session:  # Setup a DB Session
                
              for tableid in self.MPEmapper.keys():

                  tableCnt+=1
                  idxRows=session.query(TMPEsql.TMPE000).filter(TMPEsql.TMPE000.tableid==tableid).one_or_none()

                  if idxRows==None:
                      print('Table',tableid,' Not found on index - Check MPEmapping Config and --RELOAD    >> Table Load Ignored'   )
                  elif tableid!='IP0000T1':
                      print(f"\r",tableid,':',idxRows.description,'  -  Last Updated :',idxRows.createdate,'from',idxRows.mpename,end="",flush=True)
                      
                      tableObj = TMPEsql.get_model_by_tableid(tableid)
                      session.query(tableObj).delete()
                      session.commit()

                      recCnt=0
                      print(f"\r",tableid,':',idxRows.description,'  -  Last Updated :',idxRows.createdate,'from',idxRows.mpename,' ... Applying ',end="",flush=True)
                      for tmpeRow in session.query(TMPEsql.TMPE9999).filter(TMPEsql.TMPE9999.tableid==tableid).order_by(TMPEsql.TMPE9999.mpekey).yield_per(self.blocks):
                        #print('\n---------------------------------\n','JSON',tmpeRow.recordjson,'\nKEY',tmpeRow.mpekey)
                        session.add( tableObj(**tmpeRow.recordjson) )
                        recCnt+=1
                        if recCnt % self.blocks == 0:
                           print(f"\r",tableid,':',idxRows.description,'  -  Last Updated :',idxRows.createdate,'from',idxRows.mpename,' ... Applying ',recCnt,end="",flush=True)
                      session.commit()
                      print(f"\r",tableid,':',idxRows.description,'  -  Last Updated :',idxRows.createdate,'from',idxRows.mpename,' ... Complete ',recCnt)

        except Exception as ex:
            print(" Table Build Error @",tableCnt,'>>',ex)
            return False
        
        if self.verbose : print('IXMP Build  -  Tables Rebuild:',tableCnt,'     Duration:',datetime.datetime.now()-ts, )    
        return True

    def LoadIXMP(self) -> bool:
        """ ###Build the IXMPE extract file  
           Based on TMPE9999 build a new extract file for the BIN build process (IXMPEBT)
        """
        ts = datetime.datetime.now()
        recCnt=0

        try:
            if self.verbose:   print("V: Loading IXMPE Tables ")
            ixmpOut = open(self.runParms.get("working") + "/IXMPI.mpe" , "w")
            print(f"\rIXMP Build : Extracting Records ",end="",flush=True)
            with self.session_scope() as session:  # Setup a DB Session
              totalRec=session.query(TMPEsql.TMPE9999).filter(TMPEsql.TMPE9999.tableid!='*SYSTEM*',TMPEsql.TMPE9999.tableid!='IP0000T1').count()
              for ixmpRow in session.query(TMPEsql.TMPE9999).filter(TMPEsql.TMPE9999.tableid!='*SYSTEM*',TMPEsql.TMPE9999.tableid!='IP0000T1').order_by(TMPEsql.TMPE9999.tableid,TMPEsql.TMPE9999.mpekey).yield_per(self.blocks):
                ixmpOut.write(ixmpRow.dte[:10]+ixmpRow.status+ixmpRow.record)
                recCnt+=1
                if recCnt % (self.blocks * 4) == 0 :
                    print(f"\rIXMP Build : Extracting ",totalRec,"   Applied ",recCnt,end="", flush=True)

        except Exception as ex:
            print(" Table Build (", recCnt, ") : ", ex)
            return False
            # raise IOError(ex) from ex

        if self.verbose : print('\rIXMP Build : Extracted ',recCnt,'     Duration:',datetime.datetime.now()-ts )
        ixmpOut.close()
        return True
    

 


        # Flag System Tag as last MPE processed and applied
        # self.session.merge(TMPEsql.TMPE000(tableid='*SYSTEM*',description="system level row",createdate=mpeName.split('.')[5][1:],mpename=mpeName,processedrows=fileCnt) )

        return True

    def __decodeEntry(self, tableid, mpeRec: bytes) -> dict | None:
        """ #### Decode ACSII decoded MPE entry 
          Using the MPEmapping settings,  Decode the text string into a JSON format 
          ready to be passed to SQL engine 
        """
        # Decode the MPE table based on MPEmapper JSON seq settings
        recJS = {}
        tabMap = self.MPEmapper[tableid]  #  Extract the JSON definition from MPEmapper
        # stub=mpeRec[:19]
        ofs = 19  # Skip over Stub for Date,status,table id
        try:
            for entry in tabMap:
                if "startOfset" in entry:
                    ofs += entry["startOfset"]
                elif "seq" in entry:  # extract seq from stub
                    recJS[entry["seq"]] = 1

                elif "field" in entry:
                    ln = int(entry["length"])
                    recJS[entry["field"]] = mpeRec[ofs : ofs + ln].strip()
                    ofs += ln

                elif "array" in entry:
                    # If its a field then accept the field for the loop times
                    # otherwise its a number .
                    if entry["array"]["times"] in recJS:  # Fixed Loop Counter
                        loopTot = int(recJS[entry["array"]["times"]])
                    else:
                        loopTot = entry["array"]["times"]  # Based on field setting

                    if "name" in entry["array"]:
                        loopName = entry["array"]["name"]
                    else:
                        loopName = "Array"

                    loopIdx = 0
                    loop = [{}] * loopTot
                    while loopIdx < loopTot and ofs < len(mpeRec) - 3:  # +3 is the CLFD
                        loop[loopIdx] = {}
                        for loopEntry in entry["array"]["loop"]:
                            ln = int(loopEntry["length"])
                            loop[loopIdx][loopEntry["field"]] = mpeRec[
                                ofs : ofs + ln
                            ].strip()
                            ofs += ln
                        loopIdx += 1
                    # if self.verbose :  print(loopIdx,'--',loop[:loopIdx],mpeRec)
                    recJS[loopName] = loop[:loopIdx]

        except Exception as ex:
            print("------------------------------ Error ----------------------")
            print("Error :", ex)
            print("Ofset :", ofs, ":  Idx", loopIdx, ":  Tot", loopTot)
            print("Loop  :", loop)
            print("Rec   :", mpeRec)
            return False

        return recJS


