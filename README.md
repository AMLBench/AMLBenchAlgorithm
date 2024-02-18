# AMLBenchAlgorithm

This repository can be used to generate an AMLBench dataset using Rabobank transaction data and money laundering case data.

## Requirements

- A Python environment with [Pandas installed](https://pandas.pydata.org/docs/getting_started/index.html).
- The money laundering data provided in the repository in the *data* directory.
- The Rabobank bank transaction dataset provided upon request at https://github.com/akratiiet/RaboBank_Dataset.

## Running AMLBench 

- In the loader.py script, change the paths to point to the correct .csv files pertaining to the Rabobank data, and money laundering case data. Using full paths is advised.
- Run the script.
- A new AMLBench dataset named *amlbench_dataset.csv* will be generated in the current working directory.
