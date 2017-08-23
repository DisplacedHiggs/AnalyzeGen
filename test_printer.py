import FWCore.ParameterSet.Config as cms
import sys, os

#closely based on
# http://cmslxr.fnal.gov/source/PhysicsTools/HepMCCandAlgos/test/testParticleTreeDrawer.py

process = cms.Process("USER")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi") 

process.maxEvents = cms.untracked.PSet(
     input = cms.untracked.int32(1)
)

process.source = cms.Source("PoolSource",
fileNames=cms.untracked.vstring(
'file:/uscms_data/d2/kreis/1A48C7D8-1B54-E611-B109-842B2B760921.root'
)
)

process.printGenParticles = cms.EDAnalyzer("ParticleListDrawer",
     src = cms.InputTag("genParticles"),
     maxEventsToPrint = cms.untracked.int32(1)
)

process.printTree2 = cms.EDAnalyzer("ParticleTreeDrawer",
     src = cms.InputTag("genParticles"),
     printP4 = cms.untracked.bool(False),
     printPtEtaPhi = cms.untracked.bool(False),
     printVertex = cms.untracked.bool(False),
     printStatus = cms.untracked.bool(False),
     printIndex  = cms.untracked.bool(False)
)
 
process.printEventNumber = cms.OutputModule("AsciiOutputModule")
 
process.p = cms.Path(process.printGenParticles*process.printTree2)
process.outpath = cms.EndPath(process.printEventNumber)
process.MessageLogger.destinations = cms.untracked.vstring('cout','cerr')

