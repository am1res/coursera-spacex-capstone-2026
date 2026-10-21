"""Actual capstone experiments on the official IBM frozen course CSV.
Live SpaceX collection is not claimed; it timed out in both Mac and official lab.
"""
import json
from pathlib import Path
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split,GridSearchCV,StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
ROOT=Path(__file__).resolve().parent
frame=pd.read_csv(ROOT/'dataset_part_1.csv')
frame['Class']=frame.Outcome.str.startswith('True').astype(int)
# Follow course predictor set; excluded Outcome, target Class, LandingPad and coordinates.
features=['FlightNumber','PayloadMass','Orbit','LaunchSite','Flights','GridFins','Reused','Legs','Block','ReusedCount','Serial']
X=frame[features].copy();y=frame.Class
categorical=['Orbit','LaunchSite','Serial'];numeric=[x for x in features if x not in categorical]
preprocess=ColumnTransformer([('numeric',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),numeric),('categorical',OneHotEncoder(handle_unknown='ignore',sparse_output=False),categorical)])
Xtrain,Xtest,ytrain,ytest=train_test_split(X,y,test_size=.2,random_state=2)
cv=StratifiedKFold(5,shuffle=True,random_state=42)
candidates={'Logistic regression':(LogisticRegression(max_iter=2000),{'model__C':[.01,.1,1,10]}),'SVM':(SVC(),{'model__C':[.1,1,10],'model__kernel':['linear','rbf'],'model__gamma':['scale',.1,1]}),'Decision tree':(DecisionTreeClassifier(random_state=42),{'model__max_depth':[2,3,5,10],'model__min_samples_leaf':[1,2,4]}),'K nearest neighbors':(KNeighborsClassifier(),{'model__n_neighbors':[1,3,5,7,9],'model__weights':['uniform','distance']})}
results={}
for name,(model,grid) in candidates.items():
 search=GridSearchCV(Pipeline([('features',preprocess),('model',model)]),grid,cv=cv,scoring='accuracy',n_jobs=1).fit(Xtrain,ytrain)
 pred=search.predict(Xtest)
 results[name]={'best_parameters':search.best_params_,'training_cv_accuracy':float(search.best_score_),'test_accuracy':float(accuracy_score(ytest,pred)),'test_confusion_matrix':confusion_matrix(ytest,pred).tolist(),'test_predictions':pred.tolist()}
 print(name,results[name],flush=True)
# Select solely by training CV; test-set comparisons are descriptive after selection.
best=max(results,key=lambda name:results[name]['training_cv_accuracy'])
summary={'source_url':'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_1.csv','source_kind':'official frozen enriched snapshot; not a fresh live API collection','rows':len(frame),'date_min':frame.Date.min(),'date_max':frame.Date.max(),'outcome_counts':frame.Outcome.value_counts().to_dict(),'class_counts':frame.Class.value_counts().to_dict(),'label_rule':'Outcome begins with True -> 1; otherwise 0, including True Ocean as successful course label.','heldout_split':'train_test_split(test_size=.2,random_state=2), 72 train and18 test','training_cv':'five stratified shuffled folds seed42; preprocessing fit inside folds','selected_model_by_training_cv':best,'models':results,'limitations':['Frozen 2010-2020 data are not current launch data.','The 18-flight holdout is small and random, not chronological or booster-disjoint.','Flight number, reuse counts, serial and hardware are time-related; some recorded attributes may not be available at forecast time.','Successful ocean outcomes follow the course class definition; this is not identical to recovered reusable hardware.','This predicts a label, not actual launch prices or causal effects.']}
(ROOT/'frozen-model-results.json').write_text(json.dumps(summary,indent=2))
frame.to_csv(ROOT/'derived_dataset_part_2.csv',index=False)
fig,axes=plt.subplots(1,2,figsize=(10,4.5));frame.groupby('LaunchSite').Class.mean().plot.bar(ax=axes[0],color='#256d85');axes[0].set_ylabel('Mean successful course label');axes[0].set_ylim(0,1);axes[0].tick_params(axis='x',rotation=15);frame.assign(Year=pd.to_datetime(frame.Date).dt.year).groupby('Year').Class.mean().plot(marker='o',ax=axes[1]);axes[1].set_ylim(0,1);axes[1].set_ylabel('Mean successful course label');fig.tight_layout();fig.savefig(ROOT/'frozen-eda.png',dpi=170)
