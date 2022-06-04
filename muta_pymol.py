import pymol
from pymol import cmd
import os


def Mutagenesis(filename,mutation_type,start_mutation,finish_mutation):
	cmd.load(filename)
	PDBs = cmd.get_names()
	ProtChainResiList = []
	for PDB in PDBs:
		CAindex = cmd.identify("%s and name CA"%PDB)
		print(CAindex)
		for CAid in CAindex:
			pdbstr = cmd.get_pdbstr("%s and id %s"%(PDB,CAid))
			pdbstr_lines = pdbstr.splitlines()
			chain = pdbstr_lines[0].split()[4]
			resi = pdbstr_lines[0].split()[5]
			ProtChainResiList.append([PDB,chain,resi])
		for output in ProtChainResiList:
			print (output)

