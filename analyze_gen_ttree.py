from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
import math
argv.remove( '-b-' )
import numpy as n

ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

from DataFormats.FWLite import Handle, Events


def delta_r(a,b):
    deta = a.Eta()-b.Eta()
    dphi = math.acos( math.cos( a.Phi()-b.Phi() ) )
    return math.sqrt( deta*deta+dphi*dphi )

events = Events("root://cmseos.fnal.gov//store/user/kreis/"+argv[1])

genParticlesH, genParticlesN = Handle("std::vector<reco::GenParticle>"), "genParticles"

fout = ROOT.TFile("hist_"+argv[2]+".root", "recreate")
fout.cd()

#for now, fill histograms directly here
#dR
h_dR_ss     = ROOT.TH1D("h_dR_ss", "h_dR_ss", 40, 0, 6)
h_dR_bb1    = ROOT.TH1D("h_dR_bb1", "h_dR_bb1", 40, 0, 6)
h_dR_bb2    = ROOT.TH1D("h_dR_bb2", "h_dR_bb2", 40, 0, 6)
h_dR_bb_min = ROOT.TH1D("h_dR_bb_min", "h_dR_bb_min", 40, 0, 6)
h_dR_bb_max = ROOT.TH1D("h_dR_bb_max", "h_dR_bb_max", 40, 0, 6)
#pT
h_pT_s1     = ROOT.TH1D("h_pT_s1", "h_pT_s1", 40, 0, 100)
h_pT_s2     = ROOT.TH1D("h_pT_s2", "h_pT_s2", 40, 0, 100)
h_pT_s1b1   = ROOT.TH1D("h_pT_s1b1", "h_pT_s1b1", 40, 0, 100)
h_pT_s1b2   = ROOT.TH1D("h_pT_s1b2", "h_pT_s1b2", 40, 0, 100)
h_pT_s2b1   = ROOT.TH1D("h_pT_s2b1", "h_pT_s2b1", 40, 0, 100)
h_pT_s2b2   = ROOT.TH1D("h_pT_s2b2", "h_pT_s2b2", 40, 0, 100)
#vertex
h_vertex_s1b1 = ROOT.TH1D("h_vertex_s1b1", "h_vertex_s1b1", 40, 0, 100) #currently not filled
h_vertex_s1b2 = ROOT.TH1D("h_vertex_s1b2", "h_vertex_s1b2", 40, 0, 100) #currently not filled
h_vertex_s2b1 = ROOT.TH1D("h_vertex_s2b1", "h_vertex_s2b1", 40, 0, 100) #currently not filled
h_vertex_s2b2 = ROOT.TH1D("h_vertex_s2b2", "h_vertex_s2b2", 40, 0, 100) #currently not filled
h_vertex_all = ROOT.TH1D("h_vertex_all", "h_vertex_all", 40, 0, 1000)

tree = ROOT.TTree("tree", "tree")
t_dR_ss = n.zeros(1,dtype=float)
t_dR_bb1 = n.zeros(1,dtype=float)
t_dR_bb2 = n.zeros(1,dtype=float)
t_vertex_all = n.zeros(1,dtype=float)
t_vertexT_all = n.zeros(1,dtype=float)
t_gamma_distance_all = n.zeros(1,dtype=float)
t_h_pt = n.zeros(1,dtype=float)
t_s_mass = n.zeros(1,dtype=float)
t_s_pt = n.zeros(1,dtype=float)
t_b_pt_all = n.zeros(1,dtype=float)
tree.Branch('t_dR_ss', t_dR_ss, 't_dR_ss/D')
tree.Branch('t_dR_bb1', t_dR_bb1, 't_dR_bb1/D')
tree.Branch('t_dR_bb2', t_dR_bb2, 't_dR_bb2/D')
tree.Branch('t_vertex_all', t_vertex_all, 't_vertex_all/D')
tree.Branch('t_vertexT_all', t_vertexT_all, 't_vertexT_allT/D')
tree.Branch('t_gamma_distance_all', t_gamma_distance_all, 't_gamma_distance_allT/D')
tree.Branch('t_h_pt', t_h_pt, 't_h_pt/D')
tree.Branch('t_s_mass', t_s_mass, 't_s_mass/D')
tree.Branch('t_s_pt', t_s_pt, 't_s_pt/D')
tree.Branch('t_b_pt_all', t_b_pt_all, 't_b_pt_all/D')

higgs_x = 0
higgs_y = 0
higgs_z = 0

for i,event in enumerate(events):
    #print "\nEvent", i

    event.getByLabel(genParticlesN, genParticlesH)
    gen_particles = genParticlesH.product();
    #print len(gen_particles);

    #LOOP OVER ALL PARTICLES
    s_p4_list = []

    daughter_p4_list = []
    for g in gen_particles:
        
        #FIND HIGGS
        if g.pdgId() == 25 and g.status() == 22:
            print "higgs, ", g.pt()
            #t_h_pt[0] = g.pt()
            higgs_x = g.vertex().x()
            higgs_y = g.vertex().y()
            higgs_z = g.vertex().z()
            print "higgx v: ", higgs_x, higgs_y, higgs_z

        #FIND SCALAR
        if abs(g.pdgId()) == 9000006:
            print "s: ", g.pdgId(), g.status(), g.p4().pt(), g.pt()
            s_p4_list.append(g.p4())
            t_s_mass[0] = g.p4().mass()
            t_s_pt[0] = g.pt()

            #FIND SCALAR DAUGHTER
            num_daughters = g.numberOfDaughters();
            for d in range(0, num_daughters):
                daughter = g.daughter(d)
                t_b_pt_all[0] = daughter.pt()
                #tree.Fill()
                print "daughter: ", daughter.pdgId(), daughter.status()
                if d==0: #trick to get decay location of s
                    diff_x = daughter.vertex().x() - higgs_x
                    diff_y = daughter.vertex().y() - higgs_y
                    diff_z = daughter.vertex().z() - higgs_z
                    distance = math.sqrt(diff_x*diff_x + diff_y*diff_y + diff_z*diff_z)
                    print "x: ", daughter.vertex().x(), higgs_x
                    print "y: ", daughter.vertex().y(), higgs_y
                    print "z: ", daughter.vertex().z(), higgs_z
                    #print "p eq, p: ", math.sqrt(daughter.px()*daughter.px()+daughter.py()*daughter.py()+daughter.pz()*daughter.pz()), daughter.p()
                    beta = daughter.p()/daughter.energy()
                    gamma = 1.0/math.sqrt(1-beta*beta) #1 over sqrt(1-b*b) where b = p3.mag over e
                    #my_vertex = math.sqrt(daughter.vertex().x()*daughter.vertex().x()+daughter.vertex().y()*daughter.vertex().y()+daughter.vertex().z()*daughter.vertex().z())
                    #my_vertexT = math.sqrt(daughter.vertex().x()*daughter.vertex().x()+daughter.vertex().y()*daughter.vertex().y())
                    #h_vertex_all.Fill( my_vertex )
                    t_gamma_distance_all[0] = gamma*distance
                    #tree.Fill()
                daughter_p4_list.append(daughter.p4())

    #assume 2s, each with 2 daughteres
    h_dR_ss.Fill( delta_r(s_p4_list[0], s_p4_list[1]) )
    t_dR_ss[0] = delta_r(s_p4_list[0], s_p4_list[1]) 
    if s_p4_list[0].pt() > s_p4_list[1].pt():
        h_dR_bb1.Fill( delta_r(daughter_p4_list[0],daughter_p4_list[1]) )
        h_dR_bb2.Fill( delta_r(daughter_p4_list[2],daughter_p4_list[3]) )
        t_dR_bb1[0] = delta_r(daughter_p4_list[0],daughter_p4_list[1]) 
        t_dR_bb2[0] = delta_r(daughter_p4_list[2],daughter_p4_list[3]) 
    else:
        h_dR_bb1.Fill( delta_r(daughter_p4_list[2],daughter_p4_list[3]) )
        h_dR_bb2.Fill( delta_r(daughter_p4_list[0],daughter_p4_list[1]) )
        t_dR_bb1[0] = delta_r(daughter_p4_list[2],daughter_p4_list[3]) 
        t_dR_bb2[0] = delta_r(daughter_p4_list[0],daughter_p4_list[1]) 

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
    tree.Fill()


fout.cd()
tree.Write()
h_dR_ss.Write()
h_dR_bb1.Write()
h_dR_bb2.Write()
h_dR_bb_min.Write()
h_dR_bb_max.Write()
h_vertex_all.Write()
fout.Close()




        #b's (status 23 is guess from looking at file. better to check mother!)
        #if abs(g.pdgId()) == 5 and g.status() == 23: 
        #    print "b: ", g.pdgId(), g.status(), g.mother()


# could also check H vs V
