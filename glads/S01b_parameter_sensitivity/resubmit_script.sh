#!/bin/bash
#SBATCH --job-name="Seas resubmit"
#SBATCH --time=00-72:0:00
#SBATCH --mem=4G
#SBATCH --account=def-gflowers
#SBATCH --mail-user=tha111@sfu.ca
#SBATCH --mail-type=FAIL,END



# Don't change this line:
autojob.run
