# COSC 587 Data Analytics Project 2 Data Analysis
# Dr. Lisa Singh
# Author: Yang Chen

## Analysis Folder
* run.sh: Running shell script to run py files by the order sequence. Run all py files in this order.<br/>

Windows Command:
```bash
$run.sh
```
Linux Commands:
```bash
$./run.sh
```

### Exploratory Analysis

* outlier_process.py: The py file processes the statistical report(mean/median/std/mode), LOF algorithm, and Binning algorithms. It solved noisy and to construct cleaned_enery_industrial.csv for analysis, and records print-out info in industrial_record.txt.

* industrial_record.txt: Records of mean/median/std, LOF, and binning info.

* cleaned_energy_industrial.csv: Cleaned data for the analysis.

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