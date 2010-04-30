# gmagoon 7/22/09: writes the lowest energy conformation for mole file in
# arg#1 to mole file in arg#2, based on UFF energy of arg#3 embeddings
# (optimized); should be reproducible due to use of consistent randomSeed
#updated 8/12/09 for Q2 2009 version of RDKit (rdkit "import" lines of script)
#arg#4 should contain the absolute path of the RDBASE environment variable
import sys
sys.path.append(sys.argv[4]+"/")#add $RDBASE/ to the PYTHONPATH so that import statements below work properly
from rdkit import Chem
from rdkit.Chem import AllChem
attempts=int(sys.argv[3])
m = Chem.MolFromMolFile(sys.argv[1])
m2=Chem.AddHs(m)
AllChem.EmbedMultipleConfs(m2, attempts,randomSeed=1)
energy=0.0
minEid=0;
lowestE=9.999999e99;#start with a very high number, which would never be reached
for i in range(m2.GetNumConformers()):
    AllChem.UFFOptimizeMolecule(m2,confId=i)
    energy=AllChem.UFFGetMoleculeForceField(m2,confId=i).CalcEnergy()
    if (energy < lowestE):
        minEid = i
        lowestE = energy
    #energy.append(AllChem.UFFGetMoleculeForceField(m2,confId=i).CalcEnergy())
f=open(sys.argv[2], 'w')
print >>f,Chem.MolToMolBlock(m2,confId=minEid)
f.close()