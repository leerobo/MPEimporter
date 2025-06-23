from sqlalchemy import Column, CHAR, Text, JSON, String, Integer,PrimaryKeyConstraint, ForeignKey
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


# class TMPE000V1(Base):
#     __tablename__ = 'tmpe000V1'
#     __table_args__ = (
#         PrimaryKeyConstraint('key', 'dte'),
#             {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
#         )

#     tabid = Column(String(8))
#     key = Column(Text, nullable=False, default='DEFAULT')
#     dte = Column(String(12), nullable=False, default='DEFAULT')
#     stat = Column(String(1))
#     src = Column(Text)
#     tsk = Column(String(1))
#     rec = Column(Text)
#     recjs = Column(JSON)

class TMPE000(Base):
    __tablename__ = 'tmpe000'
    __table_args__ = (
        PrimaryKeyConstraint('tableid'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )
    tableid =       Column(String(8))
    description =   Column(String(27))
    keylength =     Column(Integer, default=0)
    keyofs =        Column(Integer, default=0)
    minlength =     Column(Integer, default=0)
    maxlength =     Column(Integer, default=0)
    version =       Column(String(8))
    createdate =    Column(String(12),nullable=False, default='DEFAULT')
    modifieddate =  Column(String(12),nullable=False, default='DEFAULT')
    totalrows =     Column(Integer, default=0)
    processedrows = Column(Integer, default=0)
    mpename =       Column(String(70),default='')

class TMPE006(Base):
    __tablename__ = 'tmpe006'
    __table_args__ = (
        PrimaryKeyConstraint('cpi','iso','subindex'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    cpi = Column(String(3))
    iso = Column(String(3))
    name = Column(String(57))
    format = Column(String(3))
    min = Column(String(3))
    max = Column(String(3))
    mxi= Column(String(3))
    lensize = Column(String(1))
    subindex = Column(String(2))

class TMPE007(Base):
    __tablename__ = 'tmpe007'
    __table_args__ = (
        PrimaryKeyConstraint('iso','subindex'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )
    iso = Column(String(3))
    subindex = Column(String(2))
    name = Column(String(57))
    format = Column(String(3))
    startofset = Column(String(3))
    min = Column(String(3))
    max = Column(String(3))

class TMPE008(Base):
    __tablename__ = 'tmpe008'
    __table_args__ = (
        PrimaryKeyConstraint('pds','subindex'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )
    pds = Column(String(4))
    name = Column(String(57))
    format = Column(String(3))  
    min = Column(String(3))
    max = Column(String(3))
    subindex = Column(String(2))

class TMPE009(Base):
    __tablename__ = 'tmpe009'
    __table_args__ = (
        PrimaryKeyConstraint('pds','sub'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    pds = Column(String(4))
    sub = Column(String(2))
    name = Column(String(57))
    format = Column(String(3))
    min = Column(String(3))
    max = Column(String(3))
    startofset = Column(String(3))

class TMPE015(Base):
    __tablename__ = 'tmpe015'
    __table_args__ = (
        PrimaryKeyConstraint('errorcode'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )   
    errorcode = Column(String(4), primary_key=True)
    errormessage = Column(String(255))

class TMPE016(Base):
    __tablename__ = 'tmpe016'
    __table_args__ = (
        PrimaryKeyConstraint('licenseprodid','prodid','cpi'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )     
    licenseprodid = Column(String(3))
    prodid = Column(String(3))
    cpi = Column(String(3))
    prodclass = Column(String(3))
    prodtype = Column(String(1))
    prodcatcode = Column(String(1))
    euprodcatcat = Column(String(1))
    commericalprodind = Column(String(1))

class TMPE017(Base):
    __tablename__ = 'tmpe017'
    __table_args__ = (
        PrimaryKeyConstraint('isonum'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    isonum = Column(String(3), primary_key=True)
    isoalpha3 = Column(String(3))
    exponent = Column(String(1))

class TMPE018(Base):
    __tablename__ = 'tmpe018'
    __table_args__ = (
        PrimaryKeyConstraint('licprodid','acctcatcode'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )       
    acctcatcode = Column(String(1))
    licprodid = Column(String(3))
    ird = Column(String(2))
    gcmsprodid = Column(String(3))
    prodclass = Column(String(3))
    prodtype = Column(String(1))
    acctcatcodetype = Column(String(3))
    acctcatcodelifecycle = Column(String(8))
    prodcodelifecycle = Column(String(8))

class TMPE019(Base):
    __tablename__ = 'tmpe019'
    __table_args__ = (
        PrimaryKeyConstraint('bsa','brand','ird','licprodid','acctcatcode'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )
    brand = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ird = Column(String(2))
    licprodid = Column(String(3))
    acctcatcode = Column(String(1))
    acctcatcodetype = Column(String(3))
    acctcatcodelifecycle = Column(String(8))
    flag1 = Column(String(1))
    flag2 = Column(String(1))

class TMPE020(Base):
    __tablename__ = 'tmpe020'
    __table_args__ = (
        PrimaryKeyConstraint('poslicprodid','fundlicprodid','fundgcmsprodid'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    poslicprodid = Column(String(3))
    fundlicprodid = Column(String(3))
    fundgcmsprodid = Column(String(3))
    fundprodclass = Column(String(3))
    fundtype = Column(String(1))
    fundcardprogid = Column(String(3))
    icfuswitch = Column(String(1))
    fswitch = Column(String(1))
    eswitch = Column(String(1))

class TMPE040(Base):
    __tablename__ = 'tmpe040'
    __table_args__ = (
        PrimaryKeyConstraint('issuerbinlow','issuerbinhi','cpi','prodid'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    id = Column(Integer)  
    issuerbinlow = Column(String(19))
    prodid = Column(String(3))
    issuerbinhi = Column(String(19))
    cpi = Column(String(3))
    prorityindex = Column(String(2))
    memberid = Column(String(11))
    prodtype = Column(String(1))
    endpoint = Column(String(7))
    countryiso = Column(String(3))
    countrynum = Column(String(3))
    region = Column(String(1))
    prodclass = Column(String(3))
    routing = Column(String(1))
    fprs = Column(String(1))
    prs = Column(String(1))
    purchasewithcb = Column(String(1))
    licensedproductid = Column(String(3))
    mappingsevice = Column(String(1))
    alm = Column(String(1))
    almdate = Column(String(6))
    billingccydefault = Column(String(3))
    billingccyexp = Column(String(1))
    chip2magservice = Column(String(1))
    floorexpirydate = Column(String(6))
    cobranded = Column(String(1))
    spendcontrolswitch = Column(String(1))
    mcsp = Column(String(3))
    mcad = Column(String(6))
    contractlessenabled = Column(String(1))
    rrti = Column(String(1))
    psnrouting = Column(String(1))
    cashbackwithoutpurchase = Column(String(1))
    filler1 = Column(String(1))
    rpi = Column(String(1))
    moneysend = Column(String(1))
    durbin = Column(String(1))
    cashonly = Column(String(1))
    authenticationind = Column(String(1))
    filler2 = Column(String(1))
    itmpa = Column(String(1))
    pstdte = Column(String(1))
    mealvoucherind = Column(String(1))
    prepaidnonreloadable = Column(String(2))
    fastfund = Column(String(1))
    prepaidanonymous = Column(String(1))
    cardholderccyind = Column(String(1))
    paybyaccount = Column(String(1))
 
    billingccy = Column(JSON)

 
class TMPE041(Base):
    __tablename__ = 'tmpe041'
    __table_args__ = (
        PrimaryKeyConstraint('acquirerid','memberid','cpi'),
            {'prefixes': ['UNLOGGED']}     # This sets the table as UNLOGGED
        )    
    acquirerid = Column(String(6))
    cpi = Column(String(3))
    memberid = Column(String(11))
    filler = Column(String(1))
    endpoint = Column(String(7))
    posemvcomplianceind = Column(String(1))
    atmemvcomplianceind = Column(String(1))
    ucaf = Column(String(1))
    regions = Column(JSON)
    countrys = Column(JSON)

class TMPE048(Base):
    __tablename__ = 'tmpe048'
    __table_args__ = (
        PrimaryKeyConstraint('keyseq','memberid','sslpriority','sscode','ssid','acctrefcode','transferagent','settlementccy'),
            {'prefixes': ['UNLOGGED']}
        )  
    keyseq = Column(String(11))
    memberid = Column(String(11))
    sslpriority = Column(String(1))
    sscode = Column(String(1))
    ssid = Column(String(10))
    acctrefcode = Column(String(9))
    transferagent = Column(String(11))
    filler = Column(String(19))
    settlementccy = Column(String(3))
    settlementccyexp = Column(String(1))


class TMPE052(Base):
    __tablename__ = 'tmpe052'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','cpi','d03','d24','ird'),
            {'prefixes': ['UNLOGGED']}
        )  
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ird = Column(String(2))
    mti = Column(String(4))
    d24 = Column(String(3))
    d03 = Column(String(6))
    reversals = Column(String(1))
    complianceswitch = Column(String(1))
    t53 = Column(String(11))
    producttype = Column(String(1))
    t59 = Column(String(11))
    t57 = Column(String(11))
    mcassignedmanind = Column(String(1))
    mcvalidassignedid = Column(String(1))
    contactless = Column(String(1))

class TMPE053(Base):
    __tablename__ = 'tmpe053'
    __table_args__ = (
        PrimaryKeyConstraint('feepointer','paymentparty','ccy','ratetype','feetypecode'),
            {'prefixes': ['UNLOGGED']}
        )
    feepointer = Column(String(11))
    ratetype = Column(String(3))
    paymentparty = Column(String(3))
    ccy = Column(String(3))
    exp = Column(String(1))
    filler = Column(String(11))
    programtype = Column(String(4))
    feetypecode = Column(String(2))
    feeseg = Column(String(2))
    feessegment = Column(JSON)


class TMPE056(Base):
    __tablename__ = 'tmpe056'
    id = Column(Integer, primary_key=True)
    feepointer = Column(String(11))
    bsapriority = Column(String(2))
    bsatype = Column(String(1))
    bsacode = Column(String(6))
    bsacpipriority = Column(String(2))
    cpi = Column(String(3))
    bsaliftcycle = Column(String(1))

class TMPE057(Base):
    __tablename__ = 'tmpe057'
    id = Column(Integer, primary_key=True)
    feepointer = Column(String(11))
    feeoverride = Column(String(11))
    prodclass = Column(String(3))
    cab = Column(String(4))
    mcassignid = Column(String(6))
    overideproiritycode = Column(String(2))
    t53 = Column(String(11))

class TMPE058(Base):
    __tablename__ = 'tmpe058'
    id = Column(Integer, primary_key=True)  
    cpi = Column(String(3))
    cbtype = Column(String(1))
    mcc = Column(String(5))
    region = Column(String(1))
    countrynum = Column(String(3))
    countryiso3 = Column(String(3))
    ccynum = Column(String(3))
    ccyiso3 = Column(String(3))
    ccyexponent = Column(String(1))
    cbprotectionamt = Column(String(12))

class TMPE059(Base):
    __tablename__ = 'tmpe059'
    id = Column(Integer, primary_key=True)
    feepointer = Column(String(11))
    systemapplication = Column(String(1))
    holiday = Column(String(1))
    dateexclusion = Column(String(1))
    headerprocessingdateexclusion = Column(String(1))
    authorisationind = Column(String(1))
    timeframe = Column(JSON)

 
class TMPE069(Base):
    __tablename__ = 'tmpe069'
    __table_args__ = (
        PrimaryKeyConstraint('globalccy'),
            {'prefixes': ['UNLOGGED']}
        )    
    globalccy = Column(String(3))
    exp = Column(String(1))


class TMPE072(Base):
    __tablename__ = 'tmpe072'
    __table_args__ = (
        PrimaryKeyConstraint('reg','iei'),
            {'prefixes': ['UNLOGGED']}
        )    
    member = Column(String(11))
    f1 = Column(String(2))
    reg = Column(String(1))
    iei = Column(String(2))
    intmemind = Column(String(1))
    switch = Column(String(1))
    atm = Column(String(1))
    rcl = Column(String(1))
    endp = Column(String(7))
    cbswtch = Column(String(1))
    mccgrp1 = Column(String(1))
    mccgrp2 = Column(String(1))
    mccgrp3 = Column(String(1))
    mccgrp4 = Column(String(1))
    mccgrp5 = Column(String(1))
    f2 = Column(String(1))
    mername = Column(String(30))
    ccode = Column(String(3))
    cciso = Column(String(3))
    f3 = Column(String(21))
    ofmt = Column(String(1))
    meci = Column(String(1))
    eea = Column(String(1))
    f4 = Column(String(1))
    npgps = Column(String(1))
    ptapi = Column(String(1))


class TMPE075(Base):
    __tablename__ = 'tmpe075'
    __table_args__ = (
        PrimaryKeyConstraint('mcc','cab'),
            {'prefixes': ['UNLOGGED']}
        )  
    filler = Column(String(1))
    mcc = Column(String(4))
    cab = Column(String(4))
    life = Column(String(1))
    mcctype = Column(String(1))
    flag = Column(String(1))

class TMPE078(Base):
    __tablename__ = 'tmpe078'
    __table_args__ = (
        PrimaryKeyConstraint('mcc','cab','cpi'),
            {'prefixes': ['UNLOGGED']}
        )  
    mcc = Column(String(10))
    cab = Column(String(10))
    cpi = Column(String(3))
    bsat = Column(String(1))
    bsc = Column(String(6))
    mtype = Column(String(1))
    mcpi = Column(String(3))
    mbsat = Column(String(1))
    mbs = Column(String(6))

class TMPE087(Base):
    __tablename__ = 'tmpe087'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','cpi','ird'),
            {'prefixes': ['UNLOGGED']}
        )  
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ird = Column(String(2))
    maskedcpi = Column(String(3))
    maskedbsatype = Column(String(1))
    maskedbsa = Column(String(6))
    maskedird = Column(String(2))

class TMPE088(Base):
    __tablename__ = 'tmpe088'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','cpi'),
            {'prefixes': ['UNLOGGED']}
        )      
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    maskedtype = Column(String(1))
    maskedcpi = Column(String(3))
    maskedbsatype = Column(String(1))
    maskedbsa = Column(String(6))

class TMPE089(Base):
    __tablename__ = 'tmpe089'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa'),
            {'prefixes': ['UNLOGGED']}
        )    
    bsatype = Column(String(1))
    bsa = Column(String(6))
    filler = Column(String(4))
    centralacqswitch = Column(String(1))


class TMPE090(Base):
    __tablename__ = 'tmpe090'
    __table_args__ = (
        PrimaryKeyConstraint('binlow','binhi','cpi','bsaagreement'),
            {'prefixes': ['UNLOGGED']}
        )
    binlow = Column(String(19))
    bsapriority = Column(String(1))
    bsaagreement = Column(String(6))
    cpi = Column(String(3))
    binhi = Column(String(19))
    cpipriority = Column(String(2))
    unknown = Column(String(2))
    lifecycleind = Column(String(1))
    enforcementind = Column(String(1))

class TMPE091(Base):
    __tablename__ = 'tmpe091'
    __table_args__ = (
        PrimaryKeyConstraint('acquirerbin','bsatype','bsa','cpi'),
            {'prefixes': ['UNLOGGED']}
        )
    acquirerbin = Column(String(6))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    cpi = Column(String(3))
    priority = Column(String(2))
    lifecycleind = Column(String(1))
    xxx = Column(String(3))

class TMPE092(Base):
    __tablename__ = 'tmpe092'
    __table_args__ = (
        PrimaryKeyConstraint('mti','d24'),
            {'prefixes': ['UNLOGGED']}
        )
    mti = Column(String(4))
    d24 = Column(String(3))
    busserviveprocswitch = Column(String(1))

class TMPE093(Base):
    __tablename__ = 'tmpe093'
    __table_args__ = (
        PrimaryKeyConstraint('accountrange','bsatype','bsa'),
            {'prefixes': ['UNLOGGED']}
        )    
    accountrange = Column(String(6))
    bsatype = Column(String(1))
    bsa = Column(String(6))

class TMPE094(Base):
    __tablename__ = 'tmpe094'
    id = Column(Integer, primary_key=True)
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    cntyoveride = Column(JSON)
    regionoveride = Column(JSON)
 
class TMPE095(Base):
    __tablename__ = 'tmpe095'
    __table_args__ = (
        PrimaryKeyConstraint('cpi','bsatype','bsa','ird','cab'),
            {'prefixes': ['UNLOGGED']}
        )   
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ird = Column(String(2))
    cab = Column(String(4))
    life = Column(String(1))

class TMPE096(Base):
    __tablename__ = 'tmpe096'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','ird','cpi','prodid'),
            {'prefixes': ['UNLOGGED']}
        )  
    seq = Column(String)
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ird = Column(String(2))
    prodid = Column(String(3))
    life = Column(String(1))

class TMPE097(Base):
    __tablename__ = 'tmpe097'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','cpi','mti','func','d025'),
            {'prefixes': ['UNLOGGED']}
        )  
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    mti = Column(String(4))
    func = Column(String(3))
    d025 = Column(String(4))
    rev = Column(String(1))
    cbdoc = Column(String(1))
    fpis = Column(String(1))
    fcma = Column(String(12))
    fcmc = Column(String(3))
    fcmae = Column(String(1))

class TMPE098(Base):
    __tablename__ = 'tmpe098'
    __table_args__ = (
        PrimaryKeyConstraint('bsatype','bsa','cpi','mti','d24','d03'),
            {'prefixes': ['UNLOGGED']}
        )  
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    mti = Column(String(4))
    d24 = Column(String(3))
    d03 = Column(String(6))
    rev = Column(String(1))
    ird = Column(String(1))
    edii = Column(String(1))
    eros = Column(String(1))

class TMPE099(Base):
    __tablename__ = 'tmpe099'
    id = Column(Integer, primary_key=True)
    cpi = Column(String(3))
    bsatype = Column(String(1))
    bsa = Column(String(6))
    ccy = Column(String(3))

class TMPE137(Base):
    __tablename__ = 'tmpe137'
    id = Column(Integer, primary_key=True)
    low = Column(String(16))
    hi = Column(String(16))
    reg = Column(String(1))
    cpi = Column(String(3))
    bsa = Column(String(3))
    plus = Column(String(1))

# Mapping of table IDs to model classes
TABLE_MODEL_MAP = {
   'IP0000T1': TMPE000,
   'IP0006T1': TMPE006,
   'IP0007T1': TMPE007,
   'IP0008T1': TMPE008,
   'IP0009T1': TMPE009,
   'IP0015T1': TMPE015,
   'IP0016T1': TMPE016,   
   'IP0017T1': TMPE017,
   'IP0018T1': TMPE018,   
   'IP0019T1': TMPE019,
   'IP0020T1': TMPE020,
   'IP0040T1': TMPE040,
   'IP0041T1': TMPE041,
   'IP0048T1': TMPE048,
   'IP0052T1': TMPE052,
   'IP0053T1': TMPE053,   
   'IP0056T1': TMPE056,
   'IP0057T1': TMPE057,
   'IP0058T1': TMPE058,
   'IP0059T1': TMPE059,
   'IP0069T1': TMPE069,
   'IP0072T1': TMPE072,
   'IP0075T1': TMPE075,
   'IP0078T1': TMPE078,
   'IP0087T1': TMPE087,
   'IP0088T1': TMPE088,
   'IP0089T1': TMPE089,
   'IP0090T1': TMPE090,
   'IP0091T1': TMPE091,
   'IP0092T1': TMPE092,
   'IP0093T1': TMPE093,
   'IP0094T1': TMPE094,
   'IP0095T1': TMPE095,
   'IP0096T1': TMPE096,
   'IP0097T1': TMPE097,
   'IP0098T1': TMPE098,
   'IP0099T1': TMPE099,
   'IP0137T1': TMPE137,
}


def get_model_by_tableid(tableid: str):
  """Return the SQLAlchemy model class based on the table ID."""
 
  return TABLE_MODEL_MAP.get(tableid.upper())
