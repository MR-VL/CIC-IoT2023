**CIC-IoT2023 Intrusion Detection** Analysis

This project explores machine learning-based approaches for intrusion detection using the CIC IoT 2023 dataset. It includes custom sampling techniques, feature engineering, and classification models implemented in Python 

**Download Dataset**

To download the dataset go to 
``` 
https://www.kaggle.com/datasets/akashdogra/cic-iot-2023
```

```
📁 Directory Structure

📁 CIC                     # Contains CSV files from CIC-IoT dataset (Download and extract them in this folder
📁 .ipynb_checkpoints     # Jupyter autosave checkpoints
📄 CIC analysis.ipynb     # Notebook files, you may have more depending on the date you fork this repo
```

***Key Features***

Feature Engineering

Custom feature: Packets_Duration_Ratio = Tot sum / (Duration + 1e-6)

Data clustering (reduce CPU and Memory Load) 



**Sampling & Balancing**

Stratified sampling for preserving class distribution

Custom Data Diffusion: Adds Gaussian noise to underrepresented classes after sampling 5% of chunked data

SMOTE based sampling

Simple Undersampling


**Model Evaluation**

Evaluation Metrics: Accuracy, Precision, Recall, F1-score

Classification of Original vs Synthetic (Sampled) data to assess realism of synthetic data


**Models**

RandomForestClassifier

XGBClassifier


**Sample Results**

Random Forest with Stratified Sampling:

Accuracy of Random Forest: 0.9298

Classification Report:
              precision    recall  f1-score   support

    Original       1.00      0.93      0.96    700297
     Sampled       0.01      0.58      0.01       632

    accuracy                           0.93    700929
   macro avg       0.50      0.75      0.49    700929
weighted avg       1.00      0.93      0.96    700929

Accuracy: 1.0 (Overfitting Detected)


**Requirements**

Jupyter Notebook 7.2.2 or Higher
pip install pandas scikit-learn xgboost (required for XGBoost IPYNB, not required for others)


**Running the Project**

Place your CIC-IoT .csv files inside the CIC/ folder

Open CIC analysis.ipynb in Jupyter Notebook

Run cells sequentially to:

Sample data

Perform feature engineering

Train and evaluate models


**Notes**

Designed for experimentation with real vs synthetic classification

All models tested on chunked CSVs using 5% samples (Depending on computer performance you can increase amount of sampled data to keep)

Intended for research into detection generalization & class balance challenges


**Hardware**

The code was built and ran off of 

```
Windows 10 Enterprise LSTC
Interl(R) Core(TM) i7-10700 CPU
Memory: 16GB DDR4
```
*This code does not utilize GPU*

For lower end systems it may not be possible to run or take extremely long time to run due to hardware limitations. 

**License**
This project is licensed under the MIT License

Copyright (c) 2025 MR-VL

