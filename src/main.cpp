#include <iostream>
#include <cstdlib>
#include <bits/stdc++.h> 
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "fastjet/ClusterSequence.hh"
#define infinity 9999
#include <algorithm>
#include <pybind11/stl.h>
using namespace fastjet;

namespace py = pybind11;
using namespace std;

void interface(){
  vector<PseudoJet> particles;
  // an event with three particles:   px    py  pz      E
  particles.push_back( PseudoJet(   99.0,  0.1,  0, 100.0) ); 
  particles.push_back( PseudoJet(    4.0, -0.1,  0,   5.0) ); 
  particles.push_back( PseudoJet(  -99.0,    0,  0,  99.0) );

  // choose a jet definition
  double R = 0.8;
  JetDefinition jet_def(antikt_algorithm, R);

  // run the clustering, extract the jets
  ClusterSequence cs(particles, jet_def);
  vector<PseudoJet> jets = sorted_by_pt(cs.inclusive_jets());

  // print out some infos
  cout << "Clustering with " << jet_def.description() << endl;

  // print the jets
  cout <<   "        pt y phi" << endl;
  for (unsigned i = 0; i < jets.size(); i++) {
    cout << "jet " << i << ": "<< jets[i].pt() << " " 
                   << jets[i].rap() << " " << jets[i].phi() << endl;
    vector<PseudoJet> constituents = jets[i].constituents();
    for (unsigned j = 0; j < constituents.size(); j++) {
      cout << "    constituents " << j << "'s pt: " << constituents[j].pt()
           << endl;
    }
  }
}

PYBIND11_MODULE(_core, m) {

    m.def("interface", &interface);

}
