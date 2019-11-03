# COSC 587 Data Analytics Project 2 Data Analysis
# Dr. Lisa Singh
# Author: Yang Chen
```bash
./commercial_process/data/
./commercial_process/analysis/
```

## Analysis Folder
* run.sh: Running shell script to run py files by the order sequence.

### Exploratory Analysis

* outlier_process.py: The py file processes the statistical report(mean/median/std/mode), LOF algorithm, and Binning algorithms. It solved noisy and to construct cleaned_enery_commercial.csv for analysis, and records print-out info in commercial_record.txt.

* commercial_record.txt: Records of mean/median/std, LOF, and binning info.

* cleaned_energy_commercial.csv: Cleaned data for the analysis.

* outliers_100.csv: Contains the info of outliers when k=100 in LOF.
* outliers_200.csv: Contains the info of outliers when k=200 in LOF.
* outliers_500.csv: Contains the info of outliers when k=500 in LOF.

* outliers_100.png: Plot of LOF outliers detector when k=100.
* outliers_200.png: Plot of LOF outliers detector when k=200.
* outliers_500.png: Plot of LOF outliers detector when k=500.

* clusters.py: The py file processes the histogram of all features of data, association rules, correlation, and 3 clusters and 2D PCA plots.
* KMeans-pca2D.png: 2D PCA plot of K Means.
* Ward-pca2D.png: 2D PCA plot of Ward.
* DBScan-pca2D.png: 2D PCA plot of DBScan.
* correlation.png: The plot of correlation.

* hist.jpg: Histogram plot of all features of data.

### Predictive Analysis

* prediction.py: The py file processes the T-test, linear  regression, and classfiers. All info will be printed in the terminal.

## Data Folder
* commercial_process.py: The py file further processes noisy, missing values, and other errors.
* energy_commercial.csv: Final data after processing, wrangling and computing some important features.

* common_attrs_commercial.csv: Other members' features that will impact my data.
* cleaned_commercial_building_csv.zip: Data from project 1 that is used for further processiong.
* cleaned_attributes.csv: Select most important features from the data, it is userd to merge.
* business.csv: Compute scores for every business.
* business_score.csv: Compute scores as features of final data. Every city would have a usage score in elec and gas.