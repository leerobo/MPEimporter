# MPE BreakDown

MPEprocess Handles the T068/T168 Full MPE replacement and the T067/T167 MPE Updates

There are 2 main configurates which are affected by Complance
  - MPEmapping  :  This Holds the fields for all Tables within the MPE that ARE required to be extracted
  - TMPEsql     :  This holds the SQLalchemy Base Modes of all the MPE Tables as defined in the MPEmapping,  This extracts to allow for a more split detail of the keys 

  Remember too keep these two models inline along with the define.sql 

There are 2 Config parms
  - Define.sql  : Holds the SQL create statements for all the tables (within MPEmapping) , usefull at setup an if tables change due to keys or extra fields
  - config.yml  : This is linked to the ENV parm, it holds the folders that MPEprocess with extract too and from.

## Working Files
Defined within config.yml 

``` yml
PRODUCTION :
  working :   /aci_cmm/ACI01/ICG/NETCT/files/LandingArea/Bin/wrk
  ixmp    :   /aci_cmm/ACI01/ICG/NETCT/files/LandingArea/Bin/wrk
  new     :   /aci_cmm/ACI01/ICG/NETCT/files/LandingArea/Bin
  database:   postgresql://user:postgres@localhost:5432/MPE'
  block   :   20000

TEST :
  working :   data/wrk
  new     :   data/new
  ixmp    :   data
  database:   postgresql://user:postgres@localhost:5432/MPE'
  block   :   10000

``` 
#### - Working directory
This is where the MPE daily files are stored which have been converted from a U1014 Stream to a ASCII CRLF format, the system will keep trace of the last loaded file.  Do not mix T067/T068 with T167/T168.
If a new T068 is the latest the system will go into a RELOAD mode.
#### - ixmp directory 
This is where the batch SEQ extract is placed
#### - new 
This is where the U1014 Blocked raw MPE files are received from Mastercard
Once here run MPEdecode.py to convert to a usable/readable format and place into working directory once complete (MPEdecode uses the same Config)
#### - database
SQL URL connection string 
(Do not put raw passwords here and up load to GH,create your own and place it within the ignore)
#### - block
This is the amount of MPE records that are in memory at any point in time,  the system will read the rows from MPE in blocks , process them and commit to DB.  in test this block is smaller due to memory limits,  in production is can be higher so making the MPEimporter slightly quicker .  

Some Blocks to time
  WSL - block at 1K    >> TMPE Table Build - Duration  0:14:08.591591
  WSL - block at 10K   >> TMPE Table Build - Duration  0:09:26.516518
  WSL - block at 20k   >> TMPE Table Build - Duration  0:10:01.818314
  WSL - block at 100K  >> TMPE Table Build - Duration  0:10:54.527488

0:10:01.818314
### CLI 

#### Python Venv setup

You might need to install pip first
sudo apt install pip 
Create a Venv area on the RPI and download required packages
``` bash
sudo python3 -m venv venv
sudo chown pi:pi venv -R
source  venv/bin/activate
python3 -m pip install -r requirements.txt
```

#### Execute

To get the latest options type
``` bash
python3 MPEimport.py -h

  -h, --help     show this help message and exit
  -v, --verbose  Show Processing Summary
  -d, --debug    Show Detailed Processing
  --RELOAD       Reload from latest Full MPE and all Updates
  --NO_MPEUPD    Do not Apply MPE files to TMPE9999
  --NO_TMPE      Do not Rebuild the TMPE Sub Tables
  --NO_IXMP      Do not Rebuild the IXMPI Extract File
  --ENV [ENV]    Config Level (PRODUCTION/TEST)
``` 

General batch setup would be 
``` bash
python3 MPEimport.py -- ENV PRODUCTION
``` 
This would check if there are any new MPE files and apply them 

Maybe you may need to rebuild the tables and IXMP if a mandate has affected a table or two
``` bash
python3 MPEimport.py -- ENV PRODUCTION --RELOAD
``` 

If you only apply BIN tables in batch once a week 
``` bash
python3 MPEimport.py -- ENV PRODUCTION --NO_IXMP --NO_TMPE  #  Daily batch to just apply MPE to TMPE9999

python3 MPEimport.py -- ENV PRODUCTION --NO_MPEUPD          #  Build IXMP and update the TMPE tables Weekly
``` 
You would them follow this up with a Batch BIN table reload from IXMP

Note :
If you lose/dont apply an MPE in sequence and another one is apply with a greater date,  it will never be applied.  if this is the case the just do a --RELOAD,  but be aware that if there are hundreds of updates, this process can run for an hour or so.



 
### Requirements
| Packages | Description | |
| ----------- | ----------- | -------------- |
| SQLalchemy | DB Framework | |
| Postgres | DataBase | |


### Reference
- GitHub : leerobo/MPEimport
- Docker Hub :  N/A