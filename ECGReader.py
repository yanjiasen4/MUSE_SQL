# -*- coding: UTF-8 -*-
 
from xml.dom.minidom import parse
import xml.dom.minidom
import MySQLdb
import argparse
import os

class ECGReader:

    def __init__(self, xmlName):
        self.DOMTree = xml.dom.minidom.parse(xmlName)
        self.collection = self.DOMTree.documentElement

        patientDemoNode = self.collection.getElementsByTagName('PatientDemographics')
        waveFormsNode = self.collection.getElementsByTagName('Waveform')

        # patient attribute

        patientDemo = patientDemoNode[0]

        self.patientID = patientDemo.getElementsByTagName('PatientID')[0].firstChild.data
        self.patientAge = patientDemo.getElementsByTagName('PatientAge')[0].firstChild.data
        self.birth = patientDemo.getElementsByTagName('DateofBirth')[0].firstChild.data
        self.gender = patientDemo.getElementsByTagName('Gender')[0].firstChild.data

        print self.patientID
        print self.patientAge
        print self.birth
        print self.gender

        # waveform
        waveFormMedian = waveFormsNode[0]
        waveFormRythmn = waveFormsNode[1]

        self.medianLeadsCount = waveFormMedian.getElementsByTagName('NumberofLeads')[0].firstChild.data
        self.medianSimpleBase = waveFormMedian.getElementsByTagName('SampleBase')[0].firstChild.data
        self.medianHighPassFilter = waveFormMedian.getElementsByTagName('HighPassFilter')[0].firstChild.data
        self.medianLowPassFilter = waveFormMedian.getElementsByTagName('LowPassFilter')[0].firstChild.data

        medianLeadsData = waveFormMedian.getElementsByTagName('LeadData')
        self.mLeadI = medianLeadsData[0].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadII = medianLeadsData[1].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV1 = medianLeadsData[2].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV2 = medianLeadsData[3].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV3 = medianLeadsData[4].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV4 = medianLeadsData[5].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV5 = medianLeadsData[6].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.mLeadV6 = medianLeadsData[7].getElementsByTagName('WaveFormData')[0].firstChild.data

        rythmnLeadsData = waveFormRythmn.getElementsByTagName('LeadData')
        self.rLeadI = rythmnLeadsData[0].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadII = rythmnLeadsData[1].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV1 = rythmnLeadsData[2].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV2 = rythmnLeadsData[3].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV3 = rythmnLeadsData[4].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV4 = rythmnLeadsData[5].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV5 = rythmnLeadsData[6].getElementsByTagName('WaveFormData')[0].firstChild.data
        self.rLeadV6 = rythmnLeadsData[7].getElementsByTagName('WaveFormData')[0].firstChild.data

    def ECGData(self):
        medianLeadsSql = "'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}'".format(self.mLeadI, self.mLeadII, self.mLeadV1, self.mLeadV2, self.mLeadV3, self.mLeadV4, self.mLeadV5, self.mLeadV6)
        rythmnLeadsSql = "'{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}'".format(self.rLeadI, self.rLeadII, self.rLeadV1, self.rLeadV2, self.rLeadV3, self.rLeadV4, self.rLeadV5, self.rLeadV6)
        return "'{0}', '{1}', '{2}', '{3}', ".format(self.patientID, self.patientAge, self.birth, self.gender) + medianLeadsSql + ',' + rythmnLeadsSql

class MySQLWriter:

    def __init__(self):
        self.db = MySQLdb.connect('localhost', 'root', 'ym19950823', 'hearthorizon')

    # deconstructor
    def __delattr__(self):
        self.db.close()

    def insertECG(self, data):
        cursor = self.db.cursor()

        sql =  "INSERT INTO TEST(patientID, patientAge, birth, gender, mLeadI, mLeadII, mLeadV1, mLeadV2, mLeadV3, mLeadV4, mLeadV5, mLeadV6, rLeadI, rLeadII, rLeadV1, rLeadV2, rLeadV3, rLeadV4, rLeadV5, rLeadV6) VALUES ({0})".format(data)

        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print e
            self.db.rollback()

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
                print 'reading from: {}'.format(file)
                reader = ECGReader(file)
                writer.insertECG(reader.ECGData())
                print 'write {} into database successfully'.format(file)
                del reader
    elif filename is not None:
        reader = ECGReader(filename)
        writer.insertECG(reader.ECGData())
        print 'write {} into database successfully'.format(filename)
