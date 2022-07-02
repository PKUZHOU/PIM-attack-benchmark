import os 
import sys
import getpass
import argparse


applications = {"VA"       : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -i 2621440 -x 1"], 
                "GEMV"     : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/gemv_host -m 8192 -n 1024"],
                "SpMV"     : ["NR_DPUS=X NR_TASKLETS=Y make all", "./bin/host_code -v 0"],
                "SEL"      : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -i 3932160 -x 1"],
                "UNI"      : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -i 3932160 -x 1"],
                "BS"       : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/bs_host -i 262144"],
                "TS"       : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/ts_host -n 524288"],
                "BFS"      : ["NR_DPUS=X NR_TASKLETS=Y make all", "./bin/host_code -v 0 -f data/loc-gowalla_edges.txt"],
                "MLP"      : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/mlp_host -m 8192 -n 1024"],
                "NW"       : ["NR_DPUS=X NR_TASKLETS=Y BL=Z BL_IN=2 make all", "./bin/nw_host -w 0 -e 1 -n 2560"],
                "HST-S"    : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -b 256 -x 1"],
                "HST-L"    : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -b 256 -x 1"],
                "RED"      : ["NR_DPUS=X NR_TASKLETS=Y BL=Z VERSION=SINGLE make all", "./bin/host_code -w 0 -e 1 -i 6553600 -x 1"],
                "SCAN-SSA" : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -i 3932160 -x 1"],
                "SCAN-RSS" : ["NR_DPUS=X NR_TASKLETS=Y BL=Z make all", "./bin/host_code -w 0 -e 1 -i 3932160 -x 1"],
                "TRNS"     : ["NR_DPUS=X NR_TASKLETS=Y make all", "./bin/host_code -w 0 -e 1 -p 64 -o 12288 -x 1"],}

def run(cfg):
    rootdir = cfg.root_dir
    app_name = cfg.task_name
    n_tasklets = cfg.n_tasklets
    n_dpus = cfg.n_dpus
    bl = cfg.bl

    if app_name in applications:
        print ("------------------------ Running: "+app_name+"----------------------")
        print ("--------------------------------------------------------------------")
        if(len(applications[app_name]) > 1):
            make = applications[app_name][0]
            run_cmd = applications[app_name][1]
        
            os.chdir(rootdir + "/"+app_name)
            os.getcwd()
        
            os.system("make clean")

            try:
                os.mkdir(rootdir + "/"+ app_name +"/bin")
            except OSError:
                print ("Creation of the direction /bin failed")
                
            try:
                os.mkdir(rootdir + "/"+ app_name +"/log")
            except OSError:
                print ("Creation of the direction /log failed")
            
            try:
                os.mkdir(rootdir + "/"+ app_name +"/log/host")
            except OSError: 
                print ("Creation of the direction /log/host failed")

            try:
                os.mkdir(rootdir + "/"+ app_name +"/profile")
            except OSError:
                print ("Creation of the direction /profile failed")
        
            m = make.replace("X", str(n_dpus))
            m = m.replace("Y", str(n_tasklets))
            if (app_name == "NW"):
                if (n_dpus == 1):
                    m = m.replace("Z", str(2560))
                elif (n_dpus == 4):
                    m = m.replace("Z", str(640))
                elif (n_dpus == 16):
                    m = m.replace("Z", str(160))
                elif (n_dpus == 64):
                    m = m.replace("Z", str(40))
            else: 
                m = m.replace("Z", str(bl))
            print ("Running = " + m) 
            try:
                os.system(m)
            except: 
                pass 

            r_cmd = run_cmd.replace("#ranks", str(n_dpus))
            r_cmd = r_cmd +  " >> profile/outs_tl"+str(n_tasklets)+"_bl"+str(bl)+"_dpus"+str(n_dpus)+".log" 
            
            print ("Running = " + app_name + " -> "+ r_cmd)
            try:
                for round in range(cfg.rounds):
                    os.system(r_cmd) 
            except:  
                pass 
        else:
            make = applications[app_name] 

            os.chdir(rootdir + "/"+app_name)
            os.getcwd()
        
            try:
                os.mkdir(rootdir + "/"+ app_name +"/bin")
                os.mkdir(rootdir + "/"+ app_name +"/log")
                os.mkdir(rootdir + "/"+ app_name +"/log/host")
                os.mkdir(rootdir + "/"+ app_name +"/profile")
            except OSError:
                print ("Creation of the direction failed")

            print (make)    
            os.system(make + ">& profile/out")

    else:
        print ( "Application "+app_name+" not available" )

def main(cfg):
    app = cfg.task_name
    print ("Application to run is: " + app)
    run(cfg)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root_dir",
        type = str,
        default = "/home/zhou/projects/PIM-attack-benchmark"
    )

    parser.add_argument(
        "--task_name",
        type=str,
        default = "VA",
        choices  = ["VA","GEMV","SpMV","SEL","UNI","BS","TS","BFS","MLP","HST-S","HST-L","RED","SCAN-SSA","SCAN-RSS","TRNS"]
    )

    parser.add_argument(
        "--n_tasklets",
        type=int,
        default=1,
        choices = [1, 2, 4, 8, 16]
    )

    parser.add_argument(
        "--n_dpus",
        type=int,
        default=64,
    )

    parser.add_argument(
        "--bl",
        type=int,
        default=10,
        choices=[10]
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=1000
    )
    cfg = parser.parse_args()

    main(cfg)
