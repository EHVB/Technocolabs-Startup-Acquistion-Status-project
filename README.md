# Startup Acquistion Status Modelling on Crunchbase Data
In this project we aim to predict whether a startup is operating or not based on given features.

--- 
## Understanding the Dataset
The dataset we are working on is a combination of numerical and categorical data that describe the startup 

- The dataset contains features of the startup, such as: *name, founded at, funding rounds, and total funding in usd*

- The label of the dataset is whether the startup is `operating` , `closed` , `acquired`, or `ipo`

---
## Preprocessing  

### Data cleaning  
**1. deleting irrelevant features and duplicate values:**

after proper inspection of the dataset, we selected the irrelevant features and deleted them, such as:
* `id`, `Unnamed: 0.1`, `entity_type`, `entity_id`, `parent_id`  
* `region`,`city`,`state_code`, `created_by`, `created_at`, `updated_at`  
* `domain`, `homepage_url`, `twitter_username`, `logo_url`, `logo_width`, `logo_height`  
* `short_description`, `description`, `overview`,`tag_list`, `name`, `normalized_name`  
* `invested_companies`, `permalink`  
* `first_milestone_at`, `last_milestone_at`, `first_funding_at`,`last_funding_at`
  
Duplicate values provide high bias, therefore were deleted.  
  
**2. removing noise and unreliable data:**  
* Columns with percentage of null values more than 97.7% were dropped.  
* Delete instances with missing values for 'status', 'country_code', 'category_code' and 'founded_at'.
* Outliers for `funding_total_usd` and `funding_rounds` were deleted using the IQR method *(Inter-Quantile Range)*.  
  
### Data transformation  
**1. changes in original data:**

we converted dates in the dataset to years
* `founded_at`, `closed_at`
  
We used One-Hot Encoding to generalize categorical data present in
* `category_code` and `country_code`
  
**2. creating new variables:**

Two new features were created based on other features: 'isClosed' and 'active_days':  
* 'isClosed' = 1 if 'status' = 'operating' or 'ipo'  
* 'isClosed' = 0 if 'status' = 'acquired' or 'closed'  
* 'active_days' calculated using 'closed_at', 'founded_at', and 'status' to calculate the age of the company  
  
**3. other transformations:**

* deleteing `closed_at` column  
* filling null values of the numerical with the mean values of each column  

encoding `status` column:
- replace `operating` with `1`
- replace `acquired` with `2`
- replace `closed` with `3`
- replace `ipo` with `4`

---  
## EDA and Feature Engineering  

### creating new feature  
we calculated the `funding_per_round` for the startup to show the average us dollars funded per round by dividing `funding_total_usd` by `funding_rounds`

### mutual information  
Using MI to detect the most important features in the data.  
It is more efficient than the correlation as it doesn't assume a linear relationship, instead it measures the level of uncertainty between two features.  
* `founded_at` and `funding_per_round` have the highest scores.
* we selected features that have MI score higher than 0.01 to proceed with  

### clustering with KMeans
we used `KMeans(n_clusters=7)` to create clusters

### standardization  
we used `StandardScaler()` to standarize the data

### pca  
Using standardized data to perform pca in order to find the principal components contributing to the label data.  
`pca = PCA(n_components=7)`  

---  
## Classification Models  

In order to choose the models wisely, a few metrics were considered for the model evaluation:  
**Accuracy , Precision , Recall, F1 Score, and Support**  

The classifiers we used are: **SVM, and Naive Bayes**  
### *SVM - Support Vector Machine*
we tested the model with different kernels to choose the best one for our dataset
* we found that the best kernel is `poly` with `degree = 3`

the classification reports for different kernels showed us that the data is biased as about 90% of the examples were labeled `operating` and the rest was divided between `closed`, `acquired`, and `ipo`
* we used the value count of acquired to undersample operating and oversample closed and ipo

after balancing the data we tried the different kernels again to choose the best for the data, and this one was `rbf`
* the accuracy decreased as we balanced the data but the recall for ipo increased significantly. and the f1-score for all classes is above 0.85

### *Niave Bayes*
* we tested the model with `.ComplementNB()`, `.GaussianNB()`, and `.MultinomialNB()`

the classification reports for different kernels showed us that the data is biased as about 90% of the examples were labeled `operating` and the rest was divided between `closed`, `acquired`, and `ipo`
* we used SMOTE to oversample the dataset 

after balancing the data we tested the model with `.ComplementNB()`, `.GaussianNB()`, and `.MultinomialNB()` again and found that `.MultinomialNB()` has the best values for **accuracy** and **f1-score**

---  
## Building Pipelines  
Pipelines provide clear and understandable code. The process of creating a pipeline that was used goes as follows:  

* ***SVM*** &rarr; `Operating`, `IPO`, `Acquired`, and `Closed`. 
* ***Naive Bayes*** &rarr; `Operating`, `IPO`, `Acquired`, and `Closed`.  

#### *SVM Pipeline*    
```python
from sklearn.pipeline import Pipeline

SVM_pipeline = Pipeline(steps=[
    ('scaler',StandardScaler()),
    ('pca',PCA(n_components=5)),
    ('model',SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo'))
])
```  
#### *Naive Bayes Pipeline*  
```python
from sklearn.pipeline import Pipeline

naive_bayes_pipeline = Pipeline(steps=[
    ('scaler',StandardScaler()),
    ('pca',PCA(n_components=5)),
    ('min_max_scaler',MinMaxScaler()),
    ('model',naive_bayes.MultinomialNB())
])
```  

---  
## Deployment  
Our web-app can be accessed through this link [startup-acquistion-status-app](https://project-dep.herokuapp.com/).  
  
#### Flask  
A framework that helps create web applications for your models while using simple python code.  
Our app allows the user to enter a few pieces of information about the startup of interest:  
`Founded at`, `Funding Rounds`, `Total Funding in USD`, `Milestones`, `Relationships`.  
The app takes the data and predicts based on SVM classifier as it had better **accuracy** and **f1-score** values.

#### Django
A high-level Python web framework that encourages rapid development and clean, pragmatic design.
Our app allows the user to enter a few pieces of information about the startup of interest:  
`Founded at`, `Funding Rounds`, `Total Funding in USD`, `Milestones`, `Relationships`.  
The app takes the data and predicts based on SVM classifier as it had better **accuracy** and **f1-score** values.

#### Heroku  
In order to deploy our model, [Heroku](https://www.heroku.com/) was used. Finally our model is hosted online and can be accessed through this link [startup-acquistion-status-app](https://project-dep.herokuapp.com/).  

---  
