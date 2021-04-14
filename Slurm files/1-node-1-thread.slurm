#!/bin/bash

#SBATCH --node=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=0-00:30:00

module purge
module load foss/2019b
module load python/3.7.4

srun -n 1 python3 main.py bigTwitter.json melbGrid.json AFINN.txt
