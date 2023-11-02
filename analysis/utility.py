
import sys
sys.path.append('./data')



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
import os
import pickle

## preprocessing
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler, OrdinalEncoder, MinMaxScaler, PowerTransformer

## pipeline
from sklearn.pipeline import Pipeline, FeatureUnion



from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
import re
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import mutual_info_regression
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import SelectKBest

df = pd.read_csv(r'./data.csv', na_values=[0,' ','','--', 'nan','Unknown'])




df.loc[df['max_salary'].isna() & df['min_salary'], 'max_salary'] =df['min_salary']

df.loc[df['min_salary'] < 100, 'min_salary'] = df['min_salary'] * 1000 
df.loc[df['max_salary'] < 100, 'max_salary'] = df['max_salary'] * 1000 


df.dropna(subset=['min_salary','max_salary'],inplace=True)



df.loc[df['company_type'].isin(['4.4','3.5','4.3','nan']), 'company_type'] = np.nan



def get_outliers(col):
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    max_val = col[(col >= lower_bound) & (col <= upper_bound)].max()
    col[(col < lower_bound) | (col > upper_bound)] = max_val
    return col

columns_to_process = ['min_salary','max_salary']
df[columns_to_process] = df[columns_to_process].apply(get_outliers, axis=0)


df.drop(['Unnamed: 0', 'company_founde', 'company_revenue', 'stars', 'id','job_location', 'company_name'],axis=1,inplace= True)





def title_transformer(title):
    try:
        if 'analyst' in title.lower():
            return 'data analyst'
        elif 'scientist' in title.lower():
            return 'data scientist'
        elif 'analysis' in title.lower():
            return 'data analyst'
    except:
        return None

df['job_title'] = df['job_title'].apply(title_transformer)




## company size bining for converting it to encoded nominal column
bin_edges = [0, 500, 1000, float('inf')]
bin_labels = [0, 1, 2]
df['company_size'] = pd.cut(df['company_size'], bins=bin_edges, labels=bin_labels)


categ_cols = ['job_title', 'company_type', 'company_industry', 'company_sector']


## split
X = df.drop(columns=['min_salary','max_salary'], axis=1)
y = df[['min_salary','max_salary']]

## split to train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=45)

print(X_test.iloc[0].values)
print(y_test.iloc[0].values)
print('------------------------------------------------------------------')
print('------------------------------------------------------------------')
print('------------------------------------------------------------------')
print(X_test.iloc[1].values)
print(y_test.iloc[1].values)
print('&'*100)
print(X_train.columns)


with open('/home/me/work/epsilon_project/assets/skills.pkl', 'rb') as file:
    skills = pickle.load(file)
skills = list(skills)



class SkillExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, skills):
        self.skills = skills

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        extracted_skills = []

        for job_description in X:
            if not isinstance(job_description, str):
                job_description = str(job_description)

            skills_in_description = {skill: 0 for skill in self.skills}
            for skill in self.skills:
                pattern = re.compile(fr'\b{re.escape(skill)}\b', flags=re.IGNORECASE)
                matches = re.findall(pattern, job_description)
                skills_in_description[skill] = 1 if matches else 0
            extracted_skills.append(skills_in_description)

        skills_df = pd.DataFrame(extracted_skills)
        return skills_df



# Create separate transformers for numeric and categorical columns
num_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent', add_indicator=False)),
])

categ_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
])

# Include all columns for PCA and feature selection
all_columns = ['company_size'] + categ_cols

# Create the ColumnTransformer to preprocess all columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, ['company_size']),
        ('cat', categ_transformer, categ_cols),
        ('skills', SkillExtractor(skills), 'job_description'),
    ])


print(f'Columns ======>  {X_train.columns}')
X_train_final = preprocessor.fit_transform(X_train)

X_train_final_df = pd.DataFrame(X_train_final)

categ_encoder = preprocessor.named_transformers_['cat']['encoder']

cat_column_names = categ_encoder.get_feature_names_out(input_features=categ_cols)

all_column_names = ['company_size']+list(cat_column_names) + skills

X_train_final_df.columns = all_column_names




## pca
pca_all = PCA(n_components=0.95)
X_train_pca_95 = pca_all.fit_transform(X_train_final_df)





def process_new(X_new):
    
    
    
    
    X_new_final = preprocessor.transform(X_new)

    X_new_final_df = pd.DataFrame(X_new_final)

    categ_encoder = preprocessor.named_transformers_['cat']['encoder']

    cat_column_names = categ_encoder.get_feature_names_out(input_features=categ_cols)

    all_column_names = ['company_size']+list(cat_column_names) + skills

    X_new_final_df.columns = all_column_names
    
    X_new_processed = pca_all.transform(X_new_final_df)

    # Return the preprocessed data
    return X_new_processed

