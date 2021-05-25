# TwitterDataAnalysisOnHPC-COMP90024
Analysing Twitter data to obtain sentiment of different blocks in Melbourne

## Motivation
Project was created to compare the overall sentiment of people in different parts of Melboure city. As the data obtained from twitter was 15 GB, we utilized resources of a high performance computer (HPC) - `Spartan` (University of Melbourne's HPC) and parrellelize our program.

## Results

| Total number of nodes | Number of threads on each node | Execution time in seconds |
| ---  | ---  | ---  |
| 1 | 1 | 991.4 |
| 1 | 8 | 189.6 |
| 2 | 4 | 193.1 |

![alt text](https://github.com/arnavgarg123/TwitterDataAnalysisOnHPC-COMP90024/blob/main/Screenshots/ExecutionTime.png)

## Output
| Area | Sentiment | Tweets |
| ---  | ---  | ---  |
| `A1` | 763 | 2752 |
| `A2` | 4116 | 4904 |
| `A3` | 2679 | 5824 |
| `A4` | 54 | 381 |
| `B1` | 11614 | 21232 |
| `B2` | 32061 | 107386 |
| `B3` | 20211 | 34494 |
| `B4` | 5733 | 6643 |
| `C1` | 7551 | 10530 |
| `C2` | 191791 | 246828 |
| `C3` | 41434 | 69901 |
| `C4` | 19537 | 26097 |
| `C5` | 7551 | 5581 |
| `D3` | 7777 | 16220 |
| `D4` | 9698 | 16536 |
| `D5` | 3757 | 4705 |
| **Total** | 361428 | 580014 |

## Observation

A 5 times performance improvement was observed when running the code parallelly on 8 
threads as compared to running on a single thread.

## How to use?
### Clone
- Clone this repo to your local machine or a HPC using https://github.com/arnavgarg123/TwitterDataAnalysisOnHPC-COMP90024.git
### Setup
- Make sure you have python3 installed on your system.
- To run the script on Windows, install Microsoft MPI from this [link](https://www.microsoft.com/en-us/download/details.aspx?id=100593).
- To run the script on Linux,  run the following commands<br />
    `sudo apt update`<br />
    `sudo apt install python3-mpi4py`
- Using terminal/cmd navigate to the folder containing the files of this repo and run the command
    ```
    mpiexec -n <number_of_threads> python main.py <data_file_name> <area_file_name> <sentiment_analysis_keywords_with_score>
     ```
    Example
    ```
    mpiexec -n 4 python main.py ./Data/smallTwitter.json ./Data/melbGrid.json ./Data/AFINN.txt
    ```

## Contributors
- [Arnav Garg ](https://github.com/arnavgarg123)
- [Piyush Bhandula](https://github.com/piyushbhandula)

## Contributing
### Step 1
 - Clone this repo to your local machine using https://github.com/arnavgarg123/TwitterDataAnalysisOnHPC-COMP90024.git <br />
### Step 2
 - HACK AWAY! <br />
### Step 3
 - Create a new pull request <br />

## License

[![License](https://img.shields.io/github/license/arnavgarg123/TwitterDataAnalysisOnHPC-COMP90024.svg?color=ye)](http://badges.mit-license.org)<br />
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/arnavgarg123/TwitterDataAnalysisOnHPC-COMP90024/blob/main/LICENSE.md) file for details
