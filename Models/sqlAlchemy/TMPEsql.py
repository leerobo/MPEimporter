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
    __tablename__ = 'TMPE007'
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
    __tablename__ = 'TMPE008'
    id = Column(Integer, primary_key=True)
    PDS = Column(String(4))
    name = Column(String(57))
    foramt = Column(String(3))  # Note: 'foramt' might be a typo for 'format'
    MIN = Column(String(3))
    MAX = Column(String(3))
    subIndex = Column(String(2))

class TMPE009(Base):
    __tablename__ = 'TMPE009'
    id = Column(Integer, primary_key=True)
    PDS = Column(String(4))
    SUB = Column(String(2))
    name = Column(String(57))
    format = Column(String(3))
    MIN = Column(String(3))
    MAX = Column(String(3))
    startOfset = Column(String(3))

class TMPE015(Base):
    __tablename__ = 'TMPE015'
    ErrorCode = Column(String(4), primary_key=True)
    ErrorMessage = Column(String(255))


class TMPE016(Base):
    __tablename__ = 'TMPE016'
    licenseProdId = Column(String(3), primary_key=True)
    ProdId = Column(String(3))
    CPI = Column(String(3))
    prodClass = Column(String(3))
    prodType = Column(String(1))
    prodCatCode = Column(String(1))
    EUprodCatCat = Column(String(1))
    commericalProdInd = Column(String(1))

class TMPE017(Base):
    __tablename__ = 'TMPE017'
    ISOnum = Column(String(3), primary_key=True)
    ISOalpha3 = Column(String(3))
    exponent = Column(String(1))

class TMPE018(Base):
    __tablename__ = 'TMPE018'
    acctCatCode = Column(String(1), primary_key=True)
    licprodId = Column(String(3))
    ird = Column(String(2))
    GCMSprodId = Column(String(3))
    prodClass = Column(String(3))
    prodType = Column(String(1))
    acctCatCodeType = Column(String(3))
    acctCatCodeLifeCycle = Column(String(8))
    prodCodeLifeCycle = Column(String(8))

class TMPE019(Base):
    __tablename__ = 'TMPE019'
    Brand = Column(String(3), primary_key=True)
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    ird = Column(String(2))
    licprodId = Column(String(3))
    acctCatCode = Column(String(1))
    acctCatCodeType = Column(String(3))
    acctCatCodeLifeCycle = Column(String(8))
    flag1 = Column(String(1))
    flag2 = Column(String(1))

class TMPE020(Base):
    __tablename__ = 'TMPE020'
    posLicProdId = Column(String(3), primary_key=True)
    fundLicProdId = Column(String(3))
    fundGCMSProdId = Column(String(3))
    fundProdClass = Column(String(3))
    fundType = Column(String(1))
    fundCardProgId = Column(String(3))
    ICFUswitch = Column(String(1))
    Fswitch = Column(String(1))
    Eswitch = Column(String(1))

 
class TMPE040(Base):
    __tablename__ = 'TMPE040'
    id = Column(Integer, primary_key=True)
    IssuerBinLow = Column(String(19))
    ProdId = Column(String(3))
    IssuerBinHi = Column(String(19))
    CPI = Column(String(3))
    ProrityIndex = Column(String(2))
    MemberId = Column(String(11))
    ProdType = Column(String(1))
    Endpoint = Column(String(7))
    CountryISO = Column(String(3))
    CountryNUM = Column(String(3))
    Region = Column(String(1))
    ProdClass = Column(String(3))
    Routing = Column(String(1))
    FPRS = Column(String(1))
    PRS = Column(String(1))
    PurchaseWithCB = Column(String(1))
    LicensedProductId = Column(String(3))
    MappingSevice = Column(String(1))
    ALM = Column(String(1))
    ALMDate = Column(String(6))
    BillingCCYdefault = Column(String(3))
    BillingCCYexp = Column(String(1))
    Chip2MagService = Column(String(1))
    FloorExpiryDate = Column(String(6))
    CObranded = Column(String(1))
    SpendControlSwitch = Column(String(1))
    MCSP = Column(String(3))
    MCAD = Column(String(6))
    ContractlessEnabled = Column(String(1))
    RRTI = Column(String(1))
    PSNRouting = Column(String(1))
    CashBackWithoutPurchase = Column(String(1))
    filler1 = Column(String(1))
    RPI = Column(String(1))
    MoneySend = Column(String(1))
    Durbin = Column(String(1))
    CashOnly = Column(String(1))
    AuthenticationInd = Column(String(1))
    filler2 = Column(String(1))
    ITMPA = Column(String(1))
    PSTDTE = Column(String(1))
    MealVoucherInd = Column(String(1))
    PrePaidNonReloadable = Column(String(2))
    FastFund = Column(String(1))
    PrePaidAnonymous = Column(String(1))
    CardHolderCCYind = Column(String(1))
    PayByAccount = Column(String(1))
    billing_ccy = relationship("BillingCCY", back_populates="parent", cascade="all, delete-orphan")

class BillingCCY(Base):
    __tablename__ = 'billing_ccy'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TMPE040.id'))
    BillingTransactionCCY = Column(String(3))
    BillingSettlementCCY = Column(String(3))
    BillingExp = Column(String(1))
    parent = relationship("TMPE040", back_populates="billing_ccy")

class TMPE041(Base):
    __tablename__ = 'TMPE041'

    id = Column(Integer, primary_key=True)
    acquirerId = Column(String(6))
    CPI = Column(String(3))
    memberId = Column(String(11))
    FILLER = Column(String(1))
    endPoint = Column(String(7))
    POSEMVcomplianceInd = Column(String(1))
    ATMEMVcomplianceInd = Column(String(1))
    UCAF = Column(String(1))

    regions = relationship("Region", back_populates="parent", cascade="all, delete-orphan")
    countrys = relationship("Country", back_populates="parent", cascade="all, delete-orphan")


class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TMPE041.id'))
    region = Column(String(1))

    parent = relationship("TMPE041", back_populates="regions")

class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TMPE041.id'))
    country = Column(String(3))
    parent = relationship("TMPE041", back_populates="countrys")

class TMPE048(Base):
    __tablename__ = 'TMPE048'

    id = Column(Integer, primary_key=True)
    keySeq = Column(String(11))
    memberId = Column(String(11))
    SSLpriority = Column(String(1))
    SScode = Column(String(1))
    SSid = Column(String(10))
    acctRefCode = Column(String(9))
    transferAgent = Column(String(11))
    filler = Column(String(19))
    settlementCCY = Column(String(3))
    settlementCCYexp = Column(String(1))


class TMPE052(Base):
    __tablename__ = 'TMPE052'

    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    IRD = Column(String(2))
    MTI = Column(String(4))
    D24 = Column(String(3))
    D03 = Column(String(6))
    reversals = Column(String(1))
    complianceSwitch = Column(String(1))
    T53 = Column(String(11))
    ProductType = Column(String(1))
    T59 = Column(String(11))
    T57 = Column(String(11))
    MCassignedManInd = Column(String(1))
    MCvalidAssignedId = Column(String(1))
    contactless = Column(String(1))

class TMPE053(Base):
    __tablename__ = 'TMPE053'

    id = Column(Integer, primary_key=True)
    FeePointer = Column(String(11))
    rateType = Column(String(3))
    paymentParty = Column(String(3))
    CCY = Column(String(3))
    exp = Column(String(1))
    filler = Column(String(11))
    programType = Column(String(4))
    feeTypeCode = Column(String(2))
    FEESEG = Column(String(2))  # Could be Integer if numeric

    fees_segments = relationship("FeesSegment", back_populates="parent", cascade="all, delete-orphan")

class FeesSegment(Base):
    __tablename__ = 'fees_segment'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TMPE053.id'))
    LOWAMT = Column(String(15))
    RATE = Column(String(14))
    RATEDIR = Column(String(2))
    UNITFEE = Column(String(12))
    MMDIR = Column(String(2))
    MINFEE = Column(String(8))
    MAXFEE = Column(String(8))
    parent = relationship("TMPE053", back_populates="fees_segments")

class TMPE056(Base):
    __tablename__ = 'TMPE056'

    id = Column(Integer, primary_key=True)
    FeePointer = Column(String(11))
    BSApriority = Column(String(2))
    BSAtype = Column(String(1))
    BSAcode = Column(String(6))
    BSAcpiPriority = Column(String(2))
    CPI = Column(String(3))
    BSAliftCycle = Column(String(1))

class TMPE057(Base):
    __tablename__ = 'TMPE057'

    id = Column(Integer, primary_key=True)
    FeePointer = Column(String(11))
    FeeOverride = Column(String(11))
    prodClass = Column(String(3))
    cab = Column(String(4))
    MCassignId = Column(String(6))
    OverideProirityCode = Column(String(2))
    T53 = Column(String(11))

class TMPE058(Base):
    __tablename__ = 'TMPE058'

    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    CBtype = Column(String(1))
    MCC = Column(String(5))
    region = Column(String(1))
    countryNum = Column(String(3))
    countryISO3 = Column(String(3))
    CCYnum = Column(String(3))
    CCYiso3 = Column(String(3))
    CCYexponent = Column(String(1))
    CBprotectionAmt = Column(String(12))

class TMPE059(Base):
    __tablename__ = 'TMPE059'
    id = Column(Integer, primary_key=True)
    FeePointer = Column(String(11))
    SystemApplication = Column(String(1))
    Holiday = Column(String(1))
    DateExclusion = Column(String(1))
    HeaderProcessingDateExclusion = Column(String(1))
    AuthorisationInd = Column(String(1))
    timeframes = relationship("TimeFrame", back_populates="parent", cascade="all, delete-orphan")

class TimeFrame(Base):
    __tablename__ = 'timeframe'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('TMPE059.id'))
    Airline = Column(String(1))
    SubTimeFrame = Column(String(4))
    NonProcDays = Column(String(1))
    Holiday = Column(String(1))
    DateExclusion = Column(String(1))
    HeaderProcessingDateExclusion = Column(String(1))
    AuthorisationInd = Column(String(1))
    parent = relationship("TMPE059", back_populates="timeframes")

class TMPE069(Base):
    __tablename__ = 'TMPE069'

    id = Column(Integer, primary_key=True)
    GlobalCCY = Column(String(3))
    exp = Column(String(1))

class TMPE072(Base):
    __tablename__ = 'TMPE072'

    id = Column(Integer, primary_key=True)
    MEMBER = Column(String(11))
    F1 = Column(String(2))
    REG = Column(String(1))
    IEI = Column(String(2))
    INTMEMIND = Column(String(1))
    SWITCH = Column(String(1))
    ATM = Column(String(1))
    RCL = Column(String(1))
    ENDP = Column(String(7))
    CBSWTCH = Column(String(1))
    MCCGRP1 = Column(String(1))
    MCCGRP2 = Column(String(1))
    MCCGRP3 = Column(String(1))
    MCCGRP4 = Column(String(1))
    MCCGRP5 = Column(String(1))
    F2 = Column(String(1))
    MERNAME = Column(String(30))
    CCODE = Column(String(3))
    CCISO = Column(String(3))
    F3 = Column(String(21))
    OFMT = Column(String(1))
    MECI = Column(String(1))
    EEA = Column(String(1))
    F4 = Column(String(1))
    NPGPS = Column(String(1))
    PTAPI = Column(String(1))

class TMPE075(Base):
    __tablename__ = 'TMPE075'

    id = Column(Integer, primary_key=True)
    filler = Column(String(1))
    MCC = Column(String(4))
    CAB = Column(String(4))
    life = Column(String(1))
    MCCtype = Column(String(1))
    flag = Column(String(1))

class TMPE078(Base):
    __tablename__ = 'TMPE078'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAT = Column(String(1))
    BSC = Column(String(6))
    MTYPE = Column(String(1))
    MCPI = Column(String(3))
    MBSAT = Column(String(1))
    MBS = Column(String(6))

class TMPE087(Base):
    __tablename__ = 'TMPE087'

    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    IRD = Column(String(2))
    maskedCPI = Column(String(3))
    maskedBSAtype = Column(String(1))
    maskedBSA = Column(String(6))
    maskedIRD = Column(String(2))

class TMPE088(Base):
    __tablename__ = 'TMPE088'

    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    maskedType = Column(String(1))
    maskedCPI = Column(String(3))
    maskedBSAtype = Column(String(1))
    maskedBSA = Column(String(6))

class TMPE089(Base):
    __tablename__ = 'TMPE089'

    id = Column(Integer, primary_key=True)
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    filler = Column(String(4))
    centralAcqSwitch = Column(String(1))

class TMPE090(Base):
    __tablename__ = 'TMPE090'

    id = Column(Integer, primary_key=True)
    BinLow = Column(String(19))
    BSApriority = Column(String(1))
    BSAagreement = Column(String(6))
    CPI = Column(String(3))
    BinHi = Column(String(19))
    CPIpriority = Column(String(2))
    unknown = Column(String(2))
    LifeCycleInd = Column(String(1))
    EnforcementInd = Column(String(1))

class TMPE091(Base):
    __tablename__ = 'TMPE091'

    id = Column(Integer, primary_key=True)
    AcquirerBin = Column(String(6))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    CPI = Column(String(3))
    priority = Column(String(2))
    LifeCycleInd = Column(String(1))
    xxx = Column(String(3))

class TMPE092(Base):
    __tablename__ = 'TMPE092'

    id = Column(Integer, primary_key=True)
    MTI = Column(String(4))
    D24 = Column(String(3))
    busServiveProcSwitch = Column(String(1))

class TMPE093(Base):
    __tablename__ = 'TMPE093'

    id = Column(Integer, primary_key=True)
    accountRange = Column(String(6))
    BSAtype = Column(String(1))
    BSA = Column(String(6))

class TMPE094(Base):
    __tablename__ = 'TMPE094'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    cnty_overrides = relationship("CntyOverride", back_populates="parent", cascade="all, delete-orphan")
    region_overrides = relationship("RegionOverride", back_populates="parent", cascade="all, delete-orphan")

class CntyOverride(Base):
    __tablename__ = 'cnty_override'
    id = Column(Integer, primary_key=True)
    ip0094t1_id = Column(Integer, ForeignKey('TMPE094.id'))
    Country = Column(String(3))
    life = Column(String(1))
    parent = relationship("TMPE094", back_populates="cnty_overrides")

class RegionOverride(Base):
    __tablename__ = 'region_override'
    id = Column(Integer, primary_key=True)
    ip0094t1_id = Column(Integer, ForeignKey('TMPE094.id'))
    region = Column(String(1))
    life = Column(String(1))
    parent = relationship("TMPE094", back_populates="region_overrides")

class TMPE095(Base):
    __tablename__ = 'TMPE095'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    IRD = Column(String(2))
    CAB = Column(String(4))
    life = Column(String(1))

class TMPE096(Base):
    __tablename__ = 'TMPE096'
    id = Column(Integer, primary_key=True)
    seq = Column(String)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    IRD = Column(String(2))
    prodId = Column(String(3))
    life = Column(String(1))

class TMPE097(Base):
    __tablename__ = 'TMPE097'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    MTI = Column(String(4))
    FUNC = Column(String(3))
    D025 = Column(String(4))
    REV = Column(String(1))
    CBDOC = Column(String(1))
    FPIS = Column(String(1))
    FCMA = Column(String(12))
    FCMC = Column(String(3))
    FCMAE = Column(String(1))

class TMPE098(Base):
    __tablename__ = 'TMPE098'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    MTI = Column(String(4))
    D24 = Column(String(3))
    D03 = Column(String(6))
    REV = Column(String(1))
    IRD = Column(String(1))
    EDII = Column(String(1))
    EROS = Column(String(1))

class TMPE099(Base):
    __tablename__ = 'TMPE099'
    id = Column(Integer, primary_key=True)
    CPI = Column(String(3))
    BSAtype = Column(String(1))
    BSA = Column(String(6))
    CCY = Column(String(3))

class TMPE137(Base):
    __tablename__ = 'TMPE137'
    id = Column(Integer, primary_key=True)
    LOW = Column(String(16))
    HI = Column(String(16))
    REG = Column(String(1))
    CPI = Column(String(3))
    BSA = Column(String(3))
    PLUS = Column(String(1))

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
