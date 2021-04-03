

https://databricks.com/try-databricks



### 2021-03-21

#### Running A quick start notebook
* Based on the notes here, it is pretty easy to create an auto-scaling cluster.
* Not sure yet what events prompt the cluster to get more workers.
* But I would be curious to try a job that uses fewer workers and more workers, to see how the outcomes compare.
* I also like ethat this notebook supports `SQL` and also `python` , using what looks like first line as `%python` to indicate the language.

#### Is this spark sql or sql ?
* From the quick start notebook...

```sql
CREATE TABLE diamonds
USING csv
OPTIONS (path "/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header "true")
```

### 2021-04-03

#### Revisit my earlier problem
* [Last time](https://michal.piekarczyk.xyz/2021/01/23/spark-weekend.html#2021-01-31) , I found this [CDC dataset](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf) called "COVID-19_Case_Surveillance_Public_Use_Data.csv"  
* My basic initial question I would like to answer is "how do the symptomatic rates compare by age bin", since this dataset has an `onset_dt` column, which is eithr blank if no symptoms and has a date if symptoms.

#### More dataset metadata..
* 22.5 M rows
* each row is a de-identified patient
* created: `2020-05-15`
* updated `2021-03-31` (not sure what was being updated though)
* Temporal Applicability: 	`2020-01-01/2021-03-16`
* Update Frequency:	Monthly
* columns


Column Name|Description|Type
--|--|--
cdc_case_earliest_dt |	Calculated date--the earliest available date for the record, taken from either the available set of clinical dates (date related to the illness or specimen collection) or the calculated date representing initial date case was received by CDC. This variable is optimized for completeness and may change for a given record from time to time as new information is submitted about a case.|Date & Time
cdc_report_dt	|Calculated date representing initial date case was reported to CDC. Depreciated; CDC recommends researchers use cdc_case_earliest_dt in time series and other time-based analyses.|Date & Time
pos_spec_dt	|Date of first positive specimen collection|Date & Time
onset_dt|Symptom onset date, if symptomatic|Date & Time
current_status	|Case Status: Laboratory-confirmed case; Probable case|Plain Text
sex	|Sex: Male; Female; Unknown; Other|Plain Text
age_group	|Age Group: 0 - 9 Years; 10 - 19 Years; 20 - 39 Years; 40 - 49 Years; 50 - 59 Years; 60 - 69 Years; 70 - 79 Years; 80 + Years|Plain Text
race_ethnicity_combined	|Race and ethnicity (combined): Hispanic/Latino; American Indian / Alaska Native, Non-Hispanic; Asian, Non-Hispanic; Black, Non-Hispanic; Native Hawaiian / Other Pacific Islander, Non-Hispanic; White, Non-Hispanic; Multiple/Other, Non-Hispanic|Plain Text
hosp_yn	|Hospitalization status|Plain Text
icu_yn	|ICU admission status|Plain Text
death_yn	|Death status|Plain Text
medcond_yn	|Presence of underlying comorbidity or disease|Plain Text


#### Get data in there
* Per the Databricks web console I can specify an S3 bucket and create a table from my file like that
* And they refer to "DBFS" as "Databricks File System"
* from the example you can load from the File Store like

```python
sparkDF = spark.read.csv('/FileStore/tables/state_income-9f7c5.csv', header="true", inferSchema="true")

# then you can create a temp table from that df
sparkDF.createOrReplaceTempView("temp_table_name")
```
* THere was also an interesting note in the help notebook about permanent tables available across cluster restarts...

```python
# Since this table is registered as a temp view, it will only be available to this notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.
# Once saved, this table will persist across cluster restarts as well as allow various users across different notebooks to query this data.
# To do so, choose your table name and uncomment the bottom line.

permanent_table_name = "{{table_name}}"

# df.write.format("{{table_import_type}}").saveAsTable(permanent_table_name)
```

* I am looking for how to do this w/ s3...
* Ah according to [docs](https://docs.databricks.com/data/data-sources/aws/amazon-s3.html)  you mount s3 files as regular files then proceed as usual
* ok will try that ...

```python
aws_bucket_name = "my-databricks-assets-alpha"
s3fn = "s3://my-databricks-assets-alpha/cdc-dataset/COVID-19_Case_Surveillance_Public_Use_Data.csv"
s3fn = "s3://my-databricks-assets-alpha/cdc-dataset/COVID-19_Case_Surveillance_Public_Use_Data.head1000.csv"

mount_name = "blah"
dbutils.fs.mount("s3a://%s" % aws_bucket_name, "/mnt/%s" % mount_name)
display(dbutils.fs.ls("/mnt/%s" % mount_name))

```
* Funny thing I was trying to run this cell in the databricks notebook but it would not run and no error was given. But the reason I am pretty sure is that no cluster was attached to the notebook.
* Then when I started the cluster creation process and then tried executing a cell, I was seeing "Waiting for cluster to start: Starting Spark" in the output.
* Now `AccessDenied`. Will try to tweak the Role which I created for databricks . Ah I see it has no s3 access at all...
* Hmm I tweaked permissions and tried again but now got a new error that the directory is already mounted.
* So going to try just the second part..
* Now getting Access Denied for `getFileStatus on s3a://my-databricks-assets-alpha/:` ,
* I unmounted `dbutils.fs.unmount("/mnt/%s" % mount_name)` , gave all the read s3 permissions available, but still getting that Access Denied for `getFileStatus on s3a://my-databricks-assets-alpha/:` ,
* But oddly enough when I go to my AWS EC2 the workers which were created have no "IAM Role"s associated with them. so that's weird.
* Trying to use these [docs](http://hadoop.apache.org/docs/r2.8.0/hadoop-aws/tools/hadoop-aws/index.html#Troubleshooting_S3A) to troubleshoot s3a

* Ok going to just try the upload instead  because cannot figure out the permissions. But I feel it is possibly because of the missing IAM Role on the ec2 workers.

#### Wait oops!
* At the very top of this sample notebook I completely ignored the link , https://docs.databricks.com/administration-guide/cloud-configurations/aws/instance-profiles.html  , which has super detailed IAM role instructions #$%*#$$#!! haha
* Ok going to try the upload route anyway just so I can possibly get started ..

#### upload
* ok I stepped away from my upload of this 1.5 gig file, and when I came back there was no evidence of success or error hehe,
* I looked around the file system w/ the notebook and stumbled upon this interesting dir, which looks like it has my file

```python

import os
print(os.listdir("/dbfs/FileStore/tables"))
# ['COVID_19_Case_Surveillance_Public_Use_Data.csv']

```
* So going to try making a table from it...

```python
# File location and type
file_location = "/dbfs/FileStore/tables/COVID_19_Case_Surveillance_Public_Use_Data.csv"
file_type = "csv"

# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

display(df)
```
* Got ...

```
AnalysisException: Path does not exist: dbfs:/dbfs/FileStore/tables/COVID_19_Case_Surveillance_Public_Use_Data.csv;
```

* Maybe without the leading `/dbfs/` ?
* Ah bingo.. so it's not an absolute path but like a relative path..

```python
# File location and type
file_location = "/FileStore/tables/COVID_19_Case_Surveillance_Public_Use_Data.csv"
file_type = "csv"

# CSV options
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

display(df)
```
* Ok that was pretty fast..

* And create that table..

```python
# Since this table is registered as a temp view, it will only be available to this notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.
# Once saved, this table will persist across cluster restarts as well as allow various users across different notebooks to query this data.
# To do so, choose your table name and uncomment the bottom line.

permanent_table_name = "covid"
# table_import_type?
df.write.format("json").saveAsTable(permanent_table_name)
```
* Took 50 seconds
* try read ..

```sql
select * from covid limit 10
```
* wow ok actually worked ... I am now seeing first ten rows ..
