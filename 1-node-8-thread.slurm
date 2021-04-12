#!/bin/bash

#SBATCH --node=1
#SBATCH --ntasks-per-node=8

module purge
module load foss/2019b
module load python/3.7.4

srun -n 8 python3 main.py bigTwitter.json melbGrid.json AFINN.txt
