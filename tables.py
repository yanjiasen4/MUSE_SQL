# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, BigInteger, Float, BLOB, Date, Time, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

import datetime
import time

engine = create_engine('mysql+mysqldb://root:ym19950823@localhost:3306/ecgtest?charset=utf8')

Base = declarative_base()

# ECG Table
class Ecg(Base):

    __tablename__ = 'ecg'

    ecgID = Column(Integer, primary_key=True, autoincrement='auto')
    dataType = Column(String(45))
    acquisitionDevice = Column(String(45))
    status = Column(String(45))
    editListStatus = Column(String(45))
    priority = Column(String(45))
    location = Column(String(45))
    acquisitionTime = Column(Time)
    acquisitionDate = Column(Date)
    cartNumber = Column(Integer)
    editTime = Column(Time)
    editDate = Column(Date)
    overreaderID = Column(Integer)
    editorID = Column(Integer)
    testReason = Column(String(45))
    modality = Column(String(45))

    patient = relationship('Patient', uselist=False)
    measurements = relationship('Measurement', uselist=False)
    originalMeasurements = relationship('Measurement', uselist=False)
    diagnosis = relationship('Diagnosis')
    originalDiagnosis = relationship('Diagnosis')
    measurementMatrix = relationship('MeasurementMatrix', uselist=False)
    intervalMeasurement = relationship('IntervalMeasurement', uselist=False)
    measuredAmplitude = relationship('MeasuredAmplitude')
    qrsTimesType = relationship('QRSTimesType')
    waveform = relationship('Waveform', uselist=False)
    pharmaData = relationship('PharmaData', uselist=False)

    def __init__(self, xmlData, diagnosis):
        # TestDemographics
        self.dataType = xmlData.getElementsByTagName('DataType')[0].firstChild.data
        self.acquisitionDevice = xmlData.getElementsByTagName('AcquisitionDevice')[0].firstChild.data
        self.status = xmlData.getElementsByTagName('Status')[0].firstChild.data
        self.editListStatus = xmlData.getElementsByTagName('EditListStatus')[0].firstChild.data
        self.priority = xmlData.getElementsByTagName('Priority')[0].firstChild.data
        self.location = xmlData.getElementsByTagName('Location')[0].firstChild.data
        self.acquisitionTime = datetime.datetime.strptime(xmlData.getElementsByTagName('AcquisitionTime')[0].firstChild.data, '%H:%M:%S').time()
        self.acquisitionDate = datetime.datetime.strptime(xmlData.getElementsByTagName('AcquisitionDate')[0].firstChild.data, '%m-%d-%Y').date()
        self.cartNumber = xmlData.getElementsByTagName('CartNumber')[0].firstChild.data
        self.editTime = datetime.datetime.strptime(xmlData.getElementsByTagName('EditTime')[0].firstChild.data, '%H:%M:%S').time()
        self.editDate = datetime.datetime.strptime(xmlData.getElementsByTagName('EditDate')[0].firstChild.data, '%m-%d-%Y').date()
        self.overreaderID = xmlData.getElementsByTagName('OverreaderID')[0].firstChild.data
        self.editorID = xmlData.getElementsByTagName('EditorID')[0].firstChild.data
        if len(xmlData.getElementsByTagName('TestReason')) != 0:
            self.testReason = xmlData.getElementsByTagName('TestReason')[0].firstChild.data
        
        #Diagnosis
        self.modality = diagnosis.getElementsByTagName('Modality')[0].firstChild.data

    def __repr__(self):
        return '%s(%r) % (self.__class__.__name__, self.ecgID)'


class Patient(Base):

    __tablename__ = 'patient'

    patientID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    patientAge = Column(Integer)
    dateofBirth = Column(String(45))
    gender = Column(String(45))
    race = Column(String(45))

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.patientID = xmlData.getElementsByTagName('PatientID')[0].firstChild.data
        self.patientAge = xmlData.getElementsByTagName('PatientAge')[0].firstChild.data
        self.dateofBirth = xmlData.getElementsByTagName('DateofBirth')[0].firstChild.data
        self.gender = xmlData.getElementsByTagName('Gender')[0].firstChild.data
        self.race = xmlData.getElementsByTagName('Race')[0].firstChild.data
        self._ecgID = id
      

class Measurement(Base):

    __tablename__ = 'measurement'

    measurementID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    ventricularRate = Column(Integer)
    atrialRate = Column(Integer)
    PRInterval = Column(Integer)
    QRSDuration = Column(Integer)
    QTInterval = Column(Integer)
    QTCorrected = Column(Integer)
    RAxis = Column(Integer)
    TAxis = Column(Integer)
    QRSCount = Column(Integer)
    QOnset = Column(Integer)
    Qoffset = Column(Integer)
    POnset = Column(Integer)
    POffset = Column(Integer)
    TOffset = Column(Integer)
    ECGSampleBase = Column(Integer)
    ECGSampleExponent = Column(Integer)
    QTcFrederica = Column(Integer)

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        if len(xmlData.getElementsByTagName('VentricularRate')) != 0:
            self.ventricularRate = xmlData.getElementsByTagName('VentricularRate')[0].firstChild.data
        if len(xmlData.getElementsByTagName('AtrialRate')) != 0:
            self.atrialRate = xmlData.getElementsByTagName('AtrialRate')[0].firstChild.data
        if len(xmlData.getElementsByTagName('PRInterval')) != 0:
            self.PRInterval = xmlData.getElementsByTagName('PRInterval')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QRSDuration')) != 0:
            self.QRSDuration = xmlData.getElementsByTagName('QRSDuration')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QTInterval')) != 0:
            self.QTInterval = xmlData.getElementsByTagName('QTInterval')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QTCorrected')) != 0:
            self.QTCorrected = xmlData.getElementsByTagName('QTCorrected')[0].firstChild.data
        if len(xmlData.getElementsByTagName('PAxis')) != 0:
            self.PAxis = xmlData.getElementsByTagName('PAxis')[0].firstChild.data
        if len(xmlData.getElementsByTagName('RAxis')) != 0:
            self.RAxis = xmlData.getElementsByTagName('RAxis')[0].firstChild.data
        if len(xmlData.getElementsByTagName('TAxis')) != 0:
            self.TAxis = xmlData.getElementsByTagName('TAxis')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QRSCount')) != 0:
            self.QRSCount = xmlData.getElementsByTagName('QRSCount')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QOnset')) != 0:
            self.QOnset = xmlData.getElementsByTagName('QOnset')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QOffset')) != 0:
            self.QOffset = xmlData.getElementsByTagName('QOffset')[0].firstChild.data
        if len(xmlData.getElementsByTagName('POnset')) != 0:
            self.POnset = xmlData.getElementsByTagName('POnset')[0].firstChild.data
        if len(xmlData.getElementsByTagName('POffset')) != 0:
            self.POffset = xmlData.getElementsByTagName('POffset')[0].firstChild.data
        if len(xmlData.getElementsByTagName('TOffset')) != 0:
            self.TOffset = xmlData.getElementsByTagName('TOffset')[0].firstChild.data
        self.ECGSampleBase = xmlData.getElementsByTagName('ECGSampleBase')[0].firstChild.data
        self.ECGSampleExponent = xmlData.getElementsByTagName('ECGSampleExponent')[0].firstChild.data
        if len(xmlData.getElementsByTagName('QTcFrederica')) != 0:
            self.QTcFrederica = xmlData.getElementsByTagName('QTcFrederica')[0].firstChild.data

        self._ecgID = id


class Diagnosis(Base):

    __tablename__ = 'diagnosis'

    diagnosisID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    stmtFlag = Column(String(45))
    stmtText = Column(String(45))

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        # join all stmtFlag into a String
        stmtFlags = xmlData.getElementsByTagName('StmtFlag')
        stmtFlagStr = ''
        for flag in stmtFlags:
            stmtFlagStr += flag.firstChild.data + ','
        self.stmtFlag = stmtFlagStr[:-1]
        self.stmtText = xmlData.getElementsByTagName('StmtText')[0].firstChild.data
        self._ecgID = id


class MeasurementMatrix(Base):

    __tablename__ = 'measurementMatrix'

    mmID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    matrix = Column(BLOB)

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.matrix = xmlData.firstChild.data
        self._ecgID = id


class IntervalMeasurement(Base):

    __tablename__ = 'intervalMeasurement'

    imID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    imTimeResolution = Column(Integer)
    imAmplitudeResolution = Column(Integer)
    imFilter = Column(String(12))
    imMode = Column(String(12))
    imMethodType = Column(String(45))
    leadIntervalCalculationMethod = Column(String(45))
    beatIntervalCalculationMethod = Column(String(45))

    measuredIntervals = relationship('MeasuredInterval')

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.imTimeResolution = xmlData.getElementsByTagName('IntervalMeasurementTimeResolution')[0].firstChild.data
        self.imAmplitudeResolution = xmlData.getElementsByTagName('IntervalMeasurementAmplitudeResolution')[0].firstChild.data
        self.imFilter = xmlData.getElementsByTagName('IntervalMeasurementFilter')[0].firstChild.data
        self.imMode = xmlData.getElementsByTagName('IntervalMeasurementMode')[0].firstChild.data
        self.imMethodType = xmlData.getElementsByTagName('IntervalMeasurementMethodType')[0].firstChild.data
        self.leadIntervalCalculationMethod = xmlData.getElementsByTagName('LeadIntervalCalculationMethod')[0].firstChild.data
        self.beatIntervalCalculationMethod = xmlData.getElementsByTagName('BeatIntervalCalculationMethod')[0].firstChild.data
        self._ecgID = id


class MeasuredInterval(Base):

    __tablename__ = 'measuredInterval'

    miID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    imLeadID = Column(String(12))
    imBeatNumber = Column(Integer)
    imBeatOffset = Column(Integer)
    imPOnset = Column(Integer)
    imPOffset = Column(Integer)
    imQOnset = Column(Integer)
    imQOffset = Column(Integer)
    imTOffset = Column(Integer)
    imRRInterval = Column(Integer)

    _imID = Column(Integer, ForeignKey('intervalMeasurement.imID'))

    def __init__(self, xmlData, id):
        self.imLeadID = xmlData.getElementsByTagName('IntervalMeasurementLeadID')[0].firstChild.data
        self.imBeatNumber = xmlData.getElementsByTagName('IntervalMeasurementBeatNumber')[0].firstChild.data

        imPOnsetNode = xmlData.getElementsByTagName('IntervalMeasurementPOnset')
        imPoffsetNode = xmlData.getElementsByTagName('IntervalMeasurementPOffset')
        imQOnsetNode = xmlData.getElementsByTagName('IntervalMeasurementQOnset')
        imQOffsetNode = xmlData.getElementsByTagName('IntervalMeasurementQOffset')
        imTOffsetNode = xmlData.getElementsByTagName('IntervalMeasurementTOffset')
        imRRIntervalNode = xmlData.getElementsByTagName('IntervalMeasurementRRInterval')
        if len(imPOnsetNode) != 0 and imPOnsetNode[0].firstChild is not None:
            self.imPOnset = imPOnsetNode[0].firstChild.data
        if len(imPoffsetNode) != 0 and imPoffsetNode[0].firstChild is not None:
            self.imPOffset = imPoffsetNode[0].firstChild.data
        if len(imQOnsetNode) != 0 and imQOnsetNode[0].firstChild is not None:
            self.imQOnset = imQOnsetNode[0].firstChild.data
        if len(imQOffsetNode) != 0 and imQOffsetNode[0].firstChild is not None:
            self.imQOffset = imQOffsetNode[0].firstChild.data
        if len(imTOffsetNode) != 0 and imTOffsetNode[0].firstChild is not None:
            self.imTOffset = imTOffsetNode[0].firstChild.data
        if len(imRRIntervalNode) != 0 and imRRIntervalNode[0].firstChild is not None:
            self.imRRInterval = imRRIntervalNode[0].firstChild.data
        self._imID = id


class Waveform(Base):

    __tablename__ = 'waveform'

    waveformID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    waveformType = Column(String(45))
    waveformStartTime = Column(Integer)
    numberofLeads = Column(Integer)
    sampleType = Column(String(45))
    sampleBase = Column(Integer)
    sampleExponent = Column(Integer)
    highPassFilter = Column(Integer)
    lowPassFilter = Column(Integer)
    ACFilter = Column(String(45))

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    leads = relationship('LeadData')

    def __init__(self, xmlData, id):
        self.waveformType = xmlData.getElementsByTagName('WaveformType')[0].firstChild.data
        self.waveformStartTime = xmlData.getElementsByTagName('WaveformStartTime')[0].firstChild.data
        self.numberofLeads = xmlData.getElementsByTagName('NumberofLeads')[0].firstChild.data
        self.sampleType = xmlData.getElementsByTagName('SampleType')[0].firstChild.data
        self.sampleBase = xmlData.getElementsByTagName('SampleBase')[0].firstChild.data
        self.sampleExponent = xmlData.getElementsByTagName('SampleExponent')[0].firstChild.data
        self.highPassFilter = xmlData.getElementsByTagName('HighPassFilter')[0].firstChild.data
        self.lowPassFilter = xmlData.getElementsByTagName('LowPassFilter')[0].firstChild.data
        self.ACFilter = xmlData.getElementsByTagName('ACFilter')[0].firstChild.data
        self._ecgID = id

class LeadData(Base):

    __tablename__ = 'leaddata'

    leadID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    byteCountTotal = Column(Integer)
    timeOffset = Column(Integer)
    sampleCountTotal = Column(Integer)
    amplitudeUnitsPerBit = Column(Float)
    amplitudeUnits = Column(String(45))
    highLimit = Column(BigInteger)
    lowLimit = Column(BigInteger)
    ID = Column(String(12))
    offsetFirstSample = Column(Integer)
    sampleSize = Column(Integer)
    dataCRC32 = Column(String(45))
    waveformData = Column(BLOB)

    _waveformID = Column(Integer, ForeignKey('waveform.waveformID'))

    def __init__(self, xmlData, id):
        self.byteCountTotal = xmlData.getElementsByTagName('LeadByteCountTotal')[0].firstChild.data
        self.timeOffset = xmlData.getElementsByTagName('LeadTimeOffset')[0].firstChild.data
        self.sampleCountTotal = xmlData.getElementsByTagName('LeadSampleCountTotal')[0].firstChild.data
        self.amplitudeUnitsPerBit = xmlData.getElementsByTagName('LeadAmplitudeUnitsPerBit')[0].firstChild.data
        self.amplitudeUnits = xmlData.getElementsByTagName('LeadAmplitudeUnits')[0].firstChild.data
        self.highLimit = xmlData.getElementsByTagName('LeadHighLimit')[0].firstChild.data
        self.lowLimit = xmlData.getElementsByTagName('LeadLowLimit')[0].firstChild.data
        self.ID = xmlData.getElementsByTagName('LeadID')[0].firstChild.data
        self.offsetFirstSample = xmlData.getElementsByTagName('LeadOffsetFirstSample')[0].firstChild.data
        self.sampleSize = xmlData.getElementsByTagName('LeadSampleSize')[0].firstChild.data
        self.dataCRC32 = xmlData.getElementsByTagName('LeadDataCRC32')[0].firstChild.data
        self.waveformData = xmlData.getElementsByTagName('WaveFormData')[0].firstChild.data
        self._waveformID = id
    

class MeasuredAmplitude(Base):

    __tablename__ = 'MeasuredAmplitude'

    amID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    amLeadID = Column(String(10))
    amWaveID = Column(String(10))
    amBeatID = Column(Integer)
    amPeak = Column(Integer)
    amStart = Column(Integer)
    amDuration = Column(Integer)
    amArea = Column(Integer)

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.amLeadID = xmlData.getElementsByTagName('AmplitudeMeasurementLeadID')[0].firstChild.data
        self.amWaveID = xmlData.getElementsByTagName('AmplitudeMeasurementWaveID')[0].firstChild.data
        self.amBeatID = xmlData.getElementsByTagName('AmplitudeMeasurementBeatID')[0].firstChild.data
        self.amPeak = xmlData.getElementsByTagName('AmplitudeMeasurementPeak')[0].firstChild.data
        self.amStart = xmlData.getElementsByTagName('AmplitudeMeasurementStart')[0].firstChild.data
        self.amDuration = xmlData.getElementsByTagName('AmplitudeMeasurementDuration')[0].firstChild.data
        self.amArea = xmlData.getElementsByTagName('AmplitudeMeasurementArea')[0].firstChild.data
        self._ecgID = id

class QRSTimesType(Base):

    __tablename__ = 'qrsTimesType'

    qrsID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    number = Column(Integer)
    type = Column(Integer)
    time = Column(Integer)

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.number = xmlData.getElementsByTagName('Number')[0].firstChild.data
        self.type = xmlData.getElementsByTagName('Type')[0].firstChild.data
        self.time = xmlData.getElementsByTagName('Time')[0].firstChild.data
        self._ecgID = id

class PharmaData(Base):

    __tablename__ = 'pharmaData'

    pharamDataID = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    RRInterval = Column(Integer)
    PPInterval = Column(Integer)
    uniqueECGID = Column(String(45))
    cartID = Column(String(45))

    _ecgID = Column(Integer, ForeignKey('ecg.ecgID'))

    def __init__(self, xmlData, id):
        self.RRInterval = xmlData.getElementsByTagName('PharmaRRinterval')[0].firstChild.data
        self.PPInterval = xmlData.getElementsByTagName('PharmaPPinterval')[0].firstChild.data
        if len(xmlData.getElementsByTagName('PharmaUniqueECGID')) != 0:
            self.uniqueECGID = xmlData.getElementsByTagName('PharmaUniqueECGID')[0].firstChild.data
        if len(xmlData.getElementsByTagName('PharmaCartID')) != 0:
            self.cartID = xmlData.getElementsByTagName('PharmaCartID')[0].firstChild.data
        self._ecgID = id

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # pass



