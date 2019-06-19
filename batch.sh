#!/usr/bin/env bash
#PBS -N install_packages
#PBS -l ncpus=1
#PBS -l mem=16GB
#PBS -l walltime=1:00:00
#PBS -l ngpus=1
#PBS -l gputype=P100
#PBS -o bt_20000_stdout.out
#PBS -e bt_20000_stderr.out
###############################################
#
#
#  Display PBS info
#
#
###############################################
print_pbs_info(){
    echo ------------------------------------------------------
    echo -n 'Job is running on node '; cat $PBS_NODEFILE
    echo ------------------------------------------------------
    echo PBS: qsub is running on $PBS_O_HOST
    echo PBS: originating queue is $PBS_O_QUEUE
    echo PBS: executing queue is $PBS_QUEUE
    echo PBS: working directory is $PBS_O_WORKDIR
    echo PBS: execution mode is $PBS_ENVIRONMENT
    echo PBS: job identifier is $PBS_JOBID
    echo PBS: job name is $PBS_JOBNAME
    echo PBS: node file is $PBS_NODEFILE
    echo PBS: current home directory is $PBS_O_HOME
    echo PBS: PATH = $PBS_O_PATH
    echo ------------------------------------------------------
}

###############################################
#
#
#  Helper/Setup Functions
#
#
###############################################

load_modules(){
    #activate module environment
    #NOTE: a recent HPC update means that you shouldn't need
    #to do this anymore, but I have included as a sanity check
    source /etc/profile.d/modules.sh 

    #load cuda modules
    module load cuda
    module load cudnn

}    


copy_in(){
    #copy some data to  your input directory
    #nothing to copy in on this script
    #For empty bash functions, must put a colon in them,
    #otherwise it will throw an error
    :
}


copy_out(){
    #nothing to copy out on this script
    #For empty bash functions, must put a colon in them,
    #otherwise it will throw an error
    :
}



run_program(){
    #make sure we change to the current directory
    #where this bash job script is
    cd $PBS_O_WORKDIR
    #now run the script
    :
    # ./darknet detector train 20190424_trashnet_5/data/trashnet5.data 20190424_trashnet_5/cfg/trashnet5_train_4_gpu.cfg trashnet4_train_1000.weights   
}


run_clean(){
    #nothing to clean for this script
    #For empty bash functions, must put a colon in them,
    #otherwise it will throw an error
    :
}

###############################################
#
#
#  Running everything
#
#
###############################################

print_pbs_info
load_modules
copy_in
copy_out
run_program
run_cleannad_modules
copy_in
copy_out
run_program
run_cleanncleanncleann