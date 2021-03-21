# TwitterDataAnalysisOnHPC-COMP90024
Analysing Twitter data to obtain sentiment of different blocks in Melbourne

To run the script on Windows, install Microsoft MPI from https://www.microsoft.com/en-us/download/details.aspx?id=100593

Execution command : 
mpiexec -n <number_of_cores> python main.py <data_file_name> <area_file_name> <sentiment_analysis_keywords_with_score>

e.g. mpiexec -n 4 python main.py smallTwitter.json melbGrid.json AFINN.txt

Contributors : Arnav Garg and Piyush Bhandula
