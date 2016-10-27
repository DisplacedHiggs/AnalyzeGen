from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
import math
argv.remove( '-b-' )


ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Handle, Events


def delta_r(a,b):
    deta = a.Eta()-b.Eta()
    dphi = math.acos( math.cos( a.Phi()-b.Phi() ) )
    return math.sqrt( deta*deta+dphi*dphi )

events = Events(argv[1])

genParticlesH, genParticlesN = Handle("std::vector<reco::GenParticle>"), "genParticles"

fout = ROOT.TFile("hist_"+argv[2]+".root", "recreate")
fout.cd()

#for now, fill histograms directly here
h_dR_ss     = ROOT.TH1D("h_dR_ss", "h_dR_ss", 40, 0, 6)
h_dR_bb1    = ROOT.TH1D("h_dR_bb1", "h_dR_bb1", 40, 0, 6)
h_dR_bb2    = ROOT.TH1D("h_dR_bb2", "h_dR_bb2", 40, 0, 6)
h_dR_bb_min = ROOT.TH1D("h_dR_bb_min", "h_dR_bb_min", 40, 0, 6)
h_dR_bb_max = ROOT.TH1D("h_dR_bb_max", "h_dR_bb_max", 40, 0, 6)
h_pT_s1     = ROOT.TH1D("h_pT_s1", "h_pT_s1", 40, 0, 100)
h_pT_s2     = ROOT.TH1D("h_pT_s2", "h_pT_s2", 40, 0, 100)
h_pT_s1b1   = ROOT.TH1D("h_pT_s1b1", "h_pT_s1b1", 40, 0, 100)
h_pT_s1b2   = ROOT.TH1D("h_pT_s1b2", "h_pT_s1b2", 40, 0, 100)
h_pT_s2b1   = ROOT.TH1D("h_pT_s2b1", "h_pT_s2b1", 40, 0, 100)
h_pT_s2b2   = ROOT.TH1D("h_pT_s2b2", "h_pT_s2b2", 40, 0, 100)


for i,event in enumerate(events):
    #print "\nEvent", i

    event.getByLabel(genParticlesN, genParticlesH)
    gen_particles = genParticlesH.product();
    #print len(gen_particles);

    #LOOP OVER ALL PARTICLES
    s_p4_list = []
    daughter_p4_list = []
    for g in gen_particles:
        
        #FIND SCALAR
        if g.pdgId() == 9000006:
            #print "s: ", g.pdgId(), g.status(), g.p4().pt(), g.pt()
            s_p4_list.append(g.p4())

            #FIND DAUGHTER
            num_daughters = g.numberOfDaughters();
            for d in range(0, num_daughters):
                daughter = g.daughter(d)
                #print "daughter: ", daughter.pdgId(), daughter.status()
                daughter_p4_list.append(daughter.p4())

    #assume 2s, each with 2 daughteres
    h_dR_ss.Fill( delta_r(s_p4_list[0], s_p4_list[1]) )
    if s_p4_list[0].pt() > s_p4_list[1].pt():
        h_dR_bb1.Fill( delta_r(daughter_p4_list[0],daughter_p4_list[1]) )
        h_dR_bb2.Fill( delta_r(daughter_p4_list[2],daughter_p4_list[3]) )
    else:
        h_dR_bb1.Fill( delta_r(daughter_p4_list[2],daughter_p4_list[3]) )
        h_dR_bb2.Fill( delta_r(daughter_p4_list[0],daughter_p4_list[1]) )

    min_dR = 999999
    max_dR = 0
    for i in range(0,4):
        for j in range (i+1,4):
           dR = delta_r(daughter_p4_list[i],daughter_p4_list[j]) 
           if dR < min_dR:
               min_dR = dR
           if dR > max_dR:
               max_dR = dR
    h_dR_bb_max.Fill( max_dR )
    h_dR_bb_min.Fill( min_dR )

fout.cd()
h_dR_ss.Write()
h_dR_bb1.Write()
h_dR_bb2.Write()
h_dR_bb_min.Write()
h_dR_bb_max.Write()
fout.Close()




        #b's (status 23 is guess from looking at file. better to check mother!)
        #if abs(g.pdgId()) == 5 and g.status() == 23: 
        #    print "b: ", g.pdgId(), g.status(), g.mother()


# could also check H vs V
