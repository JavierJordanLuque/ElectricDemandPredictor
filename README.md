# ElectricDemandPredictor

Electric Demand Predictor: A forecasting tool designed to predict kW and kVAr consumption for the School of Industrial Engineering of Malaga at specific dates and times. By providing accurate energy consumption predictions, this tool helps optimize electricity costs.

This project was developed as a complement to the final degree project (TFG) of the Industrial Organization Engineering degree at the University of Malaga (UMA), authored by Alejandro Pastor Schoenrogge.

Within the repository's structure, you'll find several directories that organize the project's components:

- `data/`: Contains the dataset "Registro_Potencias_EII_30_Septiembre_2021_a_30_Septiembre_2022.xlsx". This dataset includes kW and kVAr consumption records for specific dates and times, covering the period from September 2021 to September 2022 for the School of Industrial Engineering of Malaga.
- `electricDemandPredictorAnalysis.ipynb`: A Jupyter Notebook where an Exploratory Data Analysis (EDA) has been performed on the dataset. A Random Forest machine learning model has been trained based on this data.
- `requirements.txt`: Lists all the necessary dependencies to run the project locally. You can install them using: ``pip install -r requirements.txt``
- `model/`: Contains the trained Random Forest model saved as a `.pkl` file.