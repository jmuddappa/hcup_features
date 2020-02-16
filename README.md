# HCUP Feature Engineering

Code to take a given HCUP database, filter it based on certain diseases and add a bunch of features for the diseases, complications and medical team. 

## Getting Started

Download the python file - diseaseCoding.py and place it in the folder with HCUP data present. 
To run the file simply run 'python diseaseCoding.py' in a terminal. 
The code will output a file 'filteredData.csv' in the folder which will contain the new filtered dataset with additional features.

## Results

This code was used to filter the dataset and generate features that were then utilized in regression models. The final analysis was published in my masters thesis as seen here: https://shorturl.at/atHVY

This work is going to be published in a medical journal, mid-2020 .

### Prerequisites

This code only requires numpy and pandas to be installed.
