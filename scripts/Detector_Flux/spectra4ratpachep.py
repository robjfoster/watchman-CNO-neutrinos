import numpy as np
import matplotlib.pyplot as plt
import pdb
import os

dirname = os.path.dirname(os.path.realpath(__file__))

#integrated fluxes from N Vingoles

fi_hep = 5.28e3


# read data for the hep chain neutrinos. Flux in cm^-2 s^-1 MeV^-1 at Earth's surface, E in MeV
hep = np.genfromtxt(dirname + "/../../data/hep.dat", delimiter="  ") # sns.ias.edu

Ehep = hep[:, 0]
fhep = hep[:, 1]*fi_hep

Rfid = (10026.35-3080)/10 #Radius fiducial volume in cm
hfid = 2*Rfid #Height of fiducial volume in cm

theta = 1.3103 * np.pi/180 #Average Solar elevation at Boubly

Aeff = (np.cos(theta) * hfid * 2 * Rfid) + (np.sin(theta) * np.pi * Rfid**2) #Effective area of fiducial volume exposed to Sun

#fhep = np.pi * Rfid**2 * hep[:, 1]*fi_hep #Flux in s^-1 MeV^-1 in detector

fhep = Aeff * hep[:, 1]*fi_hep #Flux in s^-1 MeV^-1 in detector

FreeProtons = 0.668559 # 0.668559 * 10^32 Free protons per kton of water
nktons = 2 * np.pi * (hfid/100) * (Rfid/100)**2 /1000 # Number of ktons of water in detector. 1000 m^3 in 1 kton
TNU = FreeProtons * nktons #Using s^-1 not year^-1 as this is what watchmakers uses.

Fhep = fhep * TNU * Ehep #Flux in terms of TNU (using s^-1)

n_bins = len(Ehep)

with open(dirname + "/../../data/Detector_Flux/hep.ratdb",'w') as outfile:
    outfile.write("{\n")
    outfile.write('name: "SPECTRUM",\n')
    outfile.write('index: "hep",\n')
    outfile.write("valid_begin: [0,0],\n")
    outfile.write("valid_end:[0,0],\n")
    outfile.write("emin: %f\n" % Ehep[0])
    outfile.write("emax: %f\n" % Ehep[-1])
    outfile.write("spec_e: [")
    for i in range(n_bins-1):
        if i != (n_bins-2): outfile.write("%f," % Ehep[i])
        else: outfile.write("%f],\n" % Ehep[i])
    outfile.write("spec_mag: [")
    for i in range(n_bins-1):
        if i != (n_bins-2): outfile.write("%f," % Fhep[i])
        else: outfile.write("%f],\n" % Fhep[i])
    outfile.write("}")

