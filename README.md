# Data-Driven Modeling for ETA Prediction of Vessels in Inland Natural Waterways - M.Sc. Data Science Final Thesis of Firoj Ahmmed Patwary

## ETA Prediction
This is the repository of my Data Science master's degree thesis at Freie Universität Berlin

### Folder Description
- **Data Preprocessing / ETL:** Contains all the notebooks and codes to preprocess the data for models implementation. It also included Extract, Transform, and Load (ETL) for entire data engineering of the project.
- **Data:** This folder contains the final data that have used in this thesis. 
- **Exploratory Data Analysis:** This folder contains all notebooks for the EDA before and after outlier detection in all features of the final dataset.
- **Feature Matrices:** Contains all feature matrices for the final data and sub dataset.
- **Figures:** Contains all visualization plot, figures of the thesis.
- **Lock Data Integration:** Contains the notebook for the river lock data integration with the main data.
- **Models:** Contains MLP, BiLSTM, GRU, and 1D-CNN models notebooks and hyperparameter tuning.
- **Trip Generator:** Notebook for the successfull trip generator from one POI to the next consecutive POI.

### Prediction Performance of All Models to the Test Dataset

| **Model** | **MAE (All)** | **MSE (All)** | **MAE (AIS)** | **MSE (AIS)** | **MAE (AIS & Weather)** | **MSE (AIS & Weather)** | **MAE (AIS, Lock & Weather)** | **MSE (AIS, Lock & Weather)** |
|:----------|--------------:|--------------:|--------------:|--------------:|------------------------:|------------------------:|-----------------------------:|------------------------------:|
| **MLP**   |        159.21  |      70682.30 |      198.81   |      97982.30 |       174.77            |      78189.60           |      172.28                   |       76835.76                 |
| **BiLSTM**|         62.04  |      15544.70 |      156.26   |      72359.01 |        95.80            |      30941.30           |       81.12                   |       22487.25                 |
| **GRU**   |         82.90  |      24592.00 |      158.42   |      73186.94 |        93.03            |      29953.55           |       91.35                   |       28799.90                 |
| **1D-CNN**|        108.40  |      33597.39 |      171.85   |      79980.45 |       129.61            |      43108.33           |      123.93                   |       41250.50                 |

*Note: MAE in minutes and MSE in minutes².*

### Feature Importance with SHAP:
![Summary Plot](https://github.com/firojap/Master_Thesis__ETA_Prediction/raw/master/Figures/summary_plot.png)

__Figure:__ *SHAP summary plot for the BiLSTM model. Red dots represent the high values of each feature and blue dots represent the low values of each feature. The y-axis lists the features in order of their importance, with the most significant feature at the top. The x-axis represents the SHAP values, which indicate the magnitude and direction of each feature’s impact on the model’s output.*

### Final Manuscript:
The final manuscript of the thesis can be download and view from [here](https://www.researchgate.net/publication/394027095_Data-Driven_Modeling_for_ETA_Prediction_of_Vessels_in_Inland_Natural_Waterways)

### Citation:
If you use or refer to this work, please cite it as follows:

#### 🔹 APA Citation
Patwary, F. A. (2024, August). *Data-driven modeling for ETA prediction of vessels in inland natural waterways* [Master’s thesis, Freie Universität Berlin]. ResearchGate. [https://doi.org/10.13140/RG.2.2.13255.41122](https://doi.org/10.13140/RG.2.2.13255.41122)

#### 🔹 BibTeX Citation
```bibtex
@mastersthesis{patwary2024eta,
  author       = {Firoj Ahmmed Patwary},
  title        = {Data-Driven Modeling for ETA Prediction of Vessels in Inland Natural Waterways},
  school       = {Freie Universität Berlin},
  year         = {2024},
  month        = {August},
  doi          = {10.13140/RG.2.2.13255.41122},
  note         = {Master’s Thesis},
  howpublished = {ResearchGate},
  url          = {https://doi.org/10.13140/RG.2.2.13255.41122}
}