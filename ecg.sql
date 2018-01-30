-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: ecg
-- ------------------------------------------------------
-- Server version	5.7.20-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `amplitudemeasurement`
--

DROP TABLE IF EXISTS `amplitudemeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `amplitudemeasurement` (
  `amID` int(11) NOT NULL AUTO_INCREMENT,
  `AmplitudeMeasurementMode` varchar(45) DEFAULT NULL,
  `ecgID` int(11) NOT NULL,
  PRIMARY KEY (`amID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diagnosis`
--

DROP TABLE IF EXISTS `diagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diagnosis` (
  `DiagnosisID` int(11) NOT NULL AUTO_INCREMENT,
  `Modality` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`DiagnosisID`),
  UNIQUE KEY `DiagnosisID_UNIQUE` (`DiagnosisID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `diagnosisstatement`
--

DROP TABLE IF EXISTS `diagnosisstatement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `diagnosisstatement` (
  `DiagnosisStatementID` int(11) NOT NULL AUTO_INCREMENT,
  `StmtFlag` varchar(45) DEFAULT NULL,
  `StmtText` varchar(45) DEFAULT NULL,
  `diagnosisID` int(11) DEFAULT NULL,
  PRIMARY KEY (`DiagnosisStatementID`),
  UNIQUE KEY `DiagnosisStatementID_UNIQUE` (`DiagnosisStatementID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ecg`
--

DROP TABLE IF EXISTS `ecg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ecg` (
  `ecgID` int(11) NOT NULL AUTO_INCREMENT,
  `PatientID` varchar(45) DEFAULT NULL,
  `DataType` varchar(45) DEFAULT NULL,
  `AcquisitionDevice` varchar(45) DEFAULT NULL,
  `Status` varchar(45) DEFAULT NULL,
  `EditListStatus` varchar(45) DEFAULT NULL,
  `Priority` varchar(45) DEFAULT NULL,
  `Location` varchar(45) DEFAULT NULL,
  `AcquisitionTime` time DEFAULT NULL,
  `AcquisitionDate` date DEFAULT NULL,
  `CartNumber` int(11) DEFAULT NULL,
  `EditTime` time DEFAULT NULL,
  `EditDate` date DEFAULT NULL,
  `OverreaderID` int(11) DEFAULT NULL,
  `EditorID` int(11) DEFAULT NULL,
  `TestReason` varchar(45) DEFAULT NULL,
  `MeasurementsID` varchar(45) DEFAULT NULL,
  `OriginalMeasurementsID` varchar(45) DEFAULT NULL,
  `DiagnosisID` varchar(45) DEFAULT NULL,
  `OriginalDiagnosisID` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ecgID`),
  UNIQUE KEY `ecgID_UNIQUE` (`ecgID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `intervalmeasurement`
--

DROP TABLE IF EXISTS `intervalmeasurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `intervalmeasurement` (
  `imID` int(11) NOT NULL AUTO_INCREMENT,
  `TimeResolution` int(11) DEFAULT NULL,
  `AmplitudeResolution` int(11) DEFAULT NULL,
  `Filter` varchar(45) DEFAULT NULL,
  `Mode` varchar(45) DEFAULT NULL,
  `MethodType` varchar(45) DEFAULT NULL,
  `LeadIntervalCalculationMethod` varchar(45) DEFAULT NULL,
  `BeatIntervalCalculationMethod` varchar(45) DEFAULT NULL,
  `ecgID` int(11) NOT NULL,
  PRIMARY KEY (`imID`),
  UNIQUE KEY `imID_UNIQUE` (`imID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `leaddata`
--

DROP TABLE IF EXISTS `leaddata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `leaddata` (
  `LeadDataID` int(11) NOT NULL AUTO_INCREMENT,
  `WaveformID` int(11) NOT NULL,
  `ByteCountTotal` int(11) DEFAULT NULL,
  `TimeOffset` int(11) DEFAULT NULL,
  `SampleCountTotal` int(11) DEFAULT NULL,
  `AmplitudeUnitsPerBit` float DEFAULT NULL,
  `AmplitudeUnits` varchar(45) DEFAULT NULL,
  `HighLimit` varchar(45) DEFAULT NULL,
  `LowLimit` varchar(45) DEFAULT NULL,
  `leadDatacol` varchar(45) DEFAULT NULL,
  `LeadID` varchar(45) DEFAULT NULL,
  `OffsetFirstSample` int(11) DEFAULT NULL,
  `FirstSampleBaseline` int(11) DEFAULT NULL,
  `SampleSize` int(11) DEFAULT NULL,
  `DataCRC32` varchar(45) DEFAULT NULL,
  `WaveFormData` blob,
  PRIMARY KEY (`LeadDataID`),
  UNIQUE KEY `leadID_UNIQUE` (`LeadDataID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `measuredinterval`
--

DROP TABLE IF EXISTS `measuredinterval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measuredinterval` (
  `miID` int(11) NOT NULL AUTO_INCREMENT,
  `IntervalMeasurementID` int(11) DEFAULT NULL,
  `LeadID` varchar(45) DEFAULT NULL,
  `BeatNumber` int(11) DEFAULT NULL,
  `BeatOffset` int(11) DEFAULT NULL,
  `POnset` int(11) DEFAULT NULL,
  `POffset` int(11) DEFAULT NULL,
  `QOnset` int(11) DEFAULT NULL,
  `QOffset` int(11) DEFAULT NULL,
  `TOffset` int(11) DEFAULT NULL,
  `RRInterval` int(11) DEFAULT NULL,
  PRIMARY KEY (`miID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `measurement`
--

DROP TABLE IF EXISTS `measurement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurement` (
  `MeasurementID` int(11) NOT NULL AUTO_INCREMENT,
  `VentricularRate` int(11) DEFAULT NULL,
  `AtrialRate` int(11) DEFAULT NULL,
  `PRInterval` int(11) DEFAULT NULL,
  `QRSDuration` int(11) DEFAULT NULL,
  `QTInterval` int(11) DEFAULT NULL,
  `QTCorrected` int(11) DEFAULT NULL,
  `RAxis` int(11) DEFAULT NULL,
  `TAxis` int(11) DEFAULT NULL,
  `QRSCount` int(11) DEFAULT NULL,
  `QOnset` int(11) DEFAULT NULL,
  `QOffset` int(11) DEFAULT NULL,
  `POnset` int(11) DEFAULT NULL,
  `POffset` int(11) DEFAULT NULL,
  `TOffset` int(11) DEFAULT NULL,
  `ECGSampleBase` int(11) DEFAULT NULL,
  `ECGSampleExponent` int(11) DEFAULT NULL,
  `QTcFrederica` int(11) DEFAULT NULL,
  PRIMARY KEY (`MeasurementID`),
  UNIQUE KEY `MeasurementID_UNIQUE` (`MeasurementID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `measurementmatrix`
--

DROP TABLE IF EXISTS `measurementmatrix`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measurementmatrix` (
  `mmID` int(11) NOT NULL AUTO_INCREMENT,
  `ecgID` int(11) NOT NULL,
  `Matrix` blob,
  PRIMARY KEY (`mmID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `patient` (
  `patientID` varchar(45) NOT NULL,
  `ecgID` varchar(45) NOT NULL,
  `PatientAge` int(11) DEFAULT NULL,
  `DateofBirth` varchar(45) DEFAULT NULL,
  `Gender` varchar(45) DEFAULT NULL,
  `Race` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`patientID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pharmadata`
--

DROP TABLE IF EXISTS `pharmadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pharmadata` (
  `ECGID` varchar(45) NOT NULL,
  `RRInterval` int(11) DEFAULT NULL,
  `PPInterval` int(11) DEFAULT NULL,
  `CartID` int(11) DEFAULT NULL,
  PRIMARY KEY (`ECGID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `qrstimestypes`
--

DROP TABLE IF EXISTS `qrstimestypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qrstimestypes` (
  `QRSTTID` int(11) NOT NULL AUTO_INCREMENT,
  `ecgID` int(11) DEFAULT NULL,
  `Number` int(11) DEFAULT NULL,
  `Type` int(11) DEFAULT NULL,
  `Time` int(11) DEFAULT NULL,
  PRIMARY KEY (`QRSTTID`),
  UNIQUE KEY `QRSTTID_UNIQUE` (`QRSTTID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `waveform`
--

DROP TABLE IF EXISTS `waveform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `waveform` (
  `WaveformID` int(11) NOT NULL AUTO_INCREMENT,
  `ecgID` int(11) DEFAULT NULL,
  `WaveformType` varchar(45) DEFAULT NULL,
  `WaveformStartTime` int(11) DEFAULT NULL,
  `NumberofLeads` int(11) DEFAULT NULL,
  `SampleType` varchar(45) DEFAULT NULL,
  `SampleBase` int(11) DEFAULT NULL,
  `SampleExponent` int(11) DEFAULT NULL,
  `HighPassFilter` int(11) DEFAULT NULL,
  `LowPassFilter` int(11) DEFAULT NULL,
  `ACFilter` int(11) DEFAULT NULL,
  PRIMARY KEY (`WaveformID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-29 22:02:01
