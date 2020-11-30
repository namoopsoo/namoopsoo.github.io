---
layout: default
title: Blahhh
---

### Michal Piekarczyk

### Professional Experience

#### Data Scientist at Katapult (Sep 2014 - Present)
_Data Scientist since 2017 and 2nd software engineering hire since 2014_
* Collaborating with a colleague, rebuilt, feature engineered, iterated, tuned and productionized our underwriting model with XGboost + ScikitLearn + SageMaker to help our main business function when on short notice our main data provider deprecated their data products.
* Created a *Data Drift Monitor* to more quickly catch the need to refit our model.
* Decoupled and parallelized our underwriting *data pipeline* into a separate *AWS Lambda API Gateway* stack to help our team deploy faster and with more confidence.
* *Dockerized* our production underwriting stack and split from the main company *git repo* to give us the flexibility to deploy both scikit learn and XGBoost models with *AWS SageMaker*. This update has now been validated over many months of iterations and model deployments.
*  Optimized and re-engineered a colleague's SQL based logistic regression model, to let us make better underwriting decisions on returning customers. Built a python + Docker + AWS Batch SQL pipeline, optimizing from a 6+ hour under an hour runtime so it can run daily. And added the ability to update and version to make iteration easier.
* Sped up our live underwriting model data pipeline by cutting less important features to save 1.5 sec, while maintaining model accuracy, to help keep our biggest retailer,
* Also re-wrote our *feature engineering* code almost from scratch to cut another 2 sec.
* Parallelized our costly data provider pulls in *Clojure*, *Docker*, *MongoDB* and *AWS ECS* to cut 2 more seconds.
* Overhauled our anti-fraud code, responding to new data requirements, to help onboard our biggest retailer.
* Introduced velocity checks to save thousands of dollars in redundant data costs.
* Removed our data blind spots by logging to *AWS Athena* in critical areas, helping us with countless data investigations and business questions.

#### VP and Software Lead at Cortix Systems Inc (Feb 2011 - Jul 2014)
_Lead system and software engineer responsible for taking initial search engine for data company concept into a Python code base (with a demo helping us secure a \$720,000 contract) and iterating it through several subsequent stages of customer validation._
* Architected the API for how our system consumes new data sources.
* Led the design, implementation, parallelization, and testing of *NLP* processing algorithms weighing aspects about data and user decisions, to make predictions about new data introduced into the system.
* Iterated through several versions of our query interpretation system, with partial text matching and allowing us to support both free-form and unambiguous query language.
* Formalized our system's resource model and web API with RESTful HTTP.

### Projects

#### A look into physiological time series data
_https://github.com/namoopsoo/aviation-pilot-physiology-hmm_
* Iterated *Tensor Flow* *LSTM* based models to predict physiological states.
* Built datasets in chunks with *numpy* and *h5py* for online learning, reliable memory consumption and parallel prediction
* Used *matplotlib* to plot validation learning curves for a better understanding of progress in model iteration.

#### Bike share destination prediction
_https://github.com/namoopsoo/learn-citibike_

* Iterated a *scikit learn* classification problem over many data normalization, feature engineering and model evaluation steps.
* Feature engineered additional geolocation data with *Google's Geocoding API*.
* Built a redis backend to track the performance of different models and hyper parameters for easier ranking.
* Dockerized and deployed the model with AWS SageMaker, Lambda and API Gateway, Docker, XGBoost and Python.

#### Clojure 168 hours time parser
_https://github.com/namoopsoo/time-parser_

* Built an AWS Lambda API Gateway and DynamoDB backed micro service to log and summarize time data.


### Education

#### NYU Polytechnic School of Engineering (Sep 2003 - May 2008)
_Honors College Brooklyn, NY_
* Bachelor of Science magna cum laude in Computer Engineering
* Master of Science in Electrical Engineering

#### University of Sheffield  (Spring 2005)
_Sheffield, UK_
Global Engineering Education Exchange (Study Abroad Program)
