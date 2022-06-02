from core.clusters.accre import Accre
import datetime
from Class_PDB import PDB
from Class_Conf import Config
from Class_ONIOM_Frame import *
from helper import write_data


def main():
    starttime = datetime.datetime.now()
    # --- Preparation ---
    pdb_obj = PDB('/scratch/ranx/1L6X/1L6X_DD_KK/1L6X_dimer_mutated.pdb')
    Mutat_list = ['KA409D', 'KA392D', 'DB399K' , 'DB356K']

    # --- Operation ---
    # Mutation
    pdb_obj.Add_MutaFlag(Mutat_list)
    pdb_obj.PDB2PDBwLeap()
    pdb_obj.rm_allH()
    pdb_obj.get_protonation(if_prt_ligand=0)
    # use minimization to relax each mutated PDB
    pdb_obj.PDB2FF(local_lig=0)
    pdb_obj.PDBMin( engine='Amber_GPU', 
                    if_cluster_job=1,
                    cluster=Accre(),
                    period=10,
                    res_setting={'partition': 'maxwell',
                                 'mem_per_core' : '10G',
                                 'account':'csb_gpu_acc'} ) # see full setting in Conf
    pdb_obj.rm_wat()

    endtime_1 = datetime.datetime.now()
    print(f'mutation: {endtime_1 - starttime}')

if __name__ == "__main__":
    main()
