# -*- coding: UTF-8 -*-
 
from xml.dom.minidom import parse
import xml.dom.minidom
import MySQLdb
import argparse
import os

from tables import *

g_ecgID = 1
g_intervalMeasurementID = 1
g_waveformID = 1

class ECGReader:

    def __init__(self, xmlName):
        self.DOMTree = xml.dom.minidom.parse(xmlName)
        self.collection = self.DOMTree.documentElement

        global g_ecgID
        global g_intervalMeasurementID
        global g_waveformID

        intervalMeasurementNode = None
        measuredIntervalNodes = None
        measuredAmplitudeNodes = None

        # get xml node
        patientNode = self.collection.getElementsByTagName('PatientDemographics')[0]
        testDemographicsNode = self.collection.getElementsByTagName('TestDemographics')[0]
        restingECGMeasurementsNode = self.collection.getElementsByTagName('RestingECGMeasurements')[0]
        originRestingECGMeasurementsNode = self.collection.getElementsByTagName('OriginalRestingECGMeasurements')[0]
        diagnosisNode = self.collection.getElementsByTagName('Diagnosis')[0]
        diagnosisStatmentNodes = diagnosisNode.getElementsByTagName('DiagnosisStatement')
        originalDiagnosisNode = self.collection.getElementsByTagName('OriginalDiagnosis')[0]
        originalDiagnosisStatmentNodes = originalDiagnosisNode.getElementsByTagName('DiagnosisStatement')
        measurementMatrixNode = self.collection.getElementsByTagName('MeasurementMatrix')[0]

        if len(self.collection.getElementsByTagName('IntervalMeasurements')) != 0:
            intervalMeasurementNode = self.collection.getElementsByTagName('IntervalMeasurements')[0]
        if len(self.collection.getElementsByTagName('MeasuredInterval')) != 0:
            measuredIntervalNodes = self.collection.getElementsByTagName('MeasuredInterval')
        if len(self.collection.getElementsByTagName('MeasuredAmplitude')) != 0:
            measuredAmplitudeNodes = self.collection.getElementsByTagName('MeasuredAmplitude')

        qrsTimesTypeNode = self.collection.getElementsByTagName('QRSTimesTypes')[0]
        qrsNodes = qrsTimesTypeNode.getElementsByTagName('QRS')
        waveFormsNode = self.collection.getElementsByTagName('Waveform')[0]
        leadDataNodes = waveFormsNode.getElementsByTagName('LeadData')
        pharmaDataNode = self.collection.getElementsByTagName('PharmaData')[0]

        # generate class object
        ecg = Ecg(testDemographicsNode, diagnosisNode)
        patient = Patient(patientNode, g_ecgID)
        measurements = Measurement(restingECGMeasurementsNode, g_ecgID)
        originalMeasurements = Measurement(originRestingECGMeasurementsNode, g_ecgID)

        for diag in diagnosisStatmentNodes:
            ecg.diagnosis.append(Diagnosis(diag, g_ecgID))

        for diag in originalDiagnosisStatmentNodes:
            ecg.originalDiagnosis.append(Diagnosis(diag, g_ecgID))

        measurementMatrix = MeasurementMatrix(measurementMatrixNode, g_ecgID)

        intervalMeasurement = None
        if intervalMeasurementNode is not None:
            intervalMeasurement = IntervalMeasurement(intervalMeasurementNode, g_ecgID)

        measuredAmplitudes = []
        measuredIntervals = []

        if measuredAmplitudeNodes is not None:
            for ma in measuredAmplitudeNodes:
                measuredAmplitude = MeasuredAmplitude(ma, g_ecgID)
                measuredAmplitudes.append(measuredAmplitude)
            intervalMeasurement.measuredIntervals = measuredIntervals

        if measuredIntervalNodes is not None:
            for mi in measuredIntervalNodes:
                measuredInterval = MeasuredInterval(mi, g_intervalMeasurementID)
                measuredIntervals.append(measuredInterval)

        qrsTimesTypes = []
        for qrs in qrsNodes:
            qrsTimesType = QRSTimesType(qrs, g_ecgID)
            qrsTimesTypes.append(qrsTimesType)

        waveform = Waveform(waveFormsNode, g_ecgID)
        leadData = []
        for ld in leadDataNodes:
            lead = LeadData(ld, g_waveformID)
            leadData.append(lead)
        waveform.leads = leadData

        pharmaData = PharmaData(pharmaDataNode, g_ecgID)

        # set relationship of ecg
        ecg.patient = patient
        ecg.measurements = measurements
        ecg.originalMeasurements = originalMeasurements
        ecg.measurementMatrix = measurementMatrix
        ecg.intervalMeasurement = intervalMeasurement
        ecg.measuredAmplitude = measuredAmplitudes
        ecg.qrsTimesType = qrsTimesTypes
        ecg.waveform = waveform
        ecg.pharmaData = pharmaData

        self.ecg = ecg

        # increment index
        g_ecgID += 1
        g_intervalMeasurementID += 1
        g_waveformID += 1

    def __delattr__(self):
        self.DOMTree.unlink()

    def __repr__(self):
        return 'ecg form:\necgID: {0}, dataType: {1}, number of leads: {2}'.format(g_ecgID, self.ecg.dataType, len(self.ecg.waveform.leads))

class MySQLWriter:

    def __init__(self):
        self.db = create_engine('mysql+mysqldb://root:ym19950823@localhost:3306/ecgtest?charset=utf8')
        self.DBSession = sessionmaker(bind=self.db)

    # deconstructor
    def __delattr__(self):
        pass

    def insertECG(self, data):
        session = self.DBSession()
        session.add(data)
        try:
            session.commit()
        except Exception as e:
            print e
        session.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='load ECG xml and write into MySQL database')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--dict', help='parse all xml files from a dictionary')
    group.add_argument('-f', '--file', help='parse a xml file')

    path = parser.parse_args().dict
    filename = parser.parse_args().file
    writer = MySQLWriter()

    # parse all files from a dict
    if path is not None:
        ls = os.listdir(path)

        for file in ls:
            ext = file.split('.')[-1]
            if ext == 'xml':
                filepath = path + '/' + file
                print 'reading from: {}'.format(filepath)
                reader = ECGReader(filepath)
                writer.insertECG(reader.ecg)
                # print 'write {} into database successfully'.format(filepath)
                del reader
    elif filename is not None:
        reader = ECGReader(filename)
        writer.insertECG(reader.ecg)
        # print 'write {} into database successfully'.format(filename)
