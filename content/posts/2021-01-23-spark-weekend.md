---
title: Spark Weekend
date: 2021-01-23
tags: notebook
---
### Trying out Spark this weekend
_These are just my casual notes from doing that, updating them as I go along._

#### Following this post to get kubernetes running in Docker for mac
- Per [this post](https://medium.com/faun/apache-spark-on-kubernetes-docker-for-mac-2501cc72e659) , I just ticked the  "Enable Kubernetes" option in the docker settings.
- Kubernetes is taking quite a while to start up though . several minutes. kind of weird?

#### Download spark image
* From [here](https://spark.apache.org/downloads.html)

### 2021-01-24

#### ok backup my docker images
* Per [notes](https://corgibytes.com/blog/2019/05/13/docker-for-mac-safely-reset-from-factory-defaults/) , I backed up local docker images,
* Like this...

```
docker save citibike-learn:0.9
# image:citibike-learn, tag:latest, image-id:1ff5cd891f00
# image:citibike-learn, tag:0.9, imageid:c8d430e84654
```

* Then I did the factory reset.
* And Enabled Kubernetes and wow! Nice finally got the green light.
* And restoring with `docker load` like this

```
docker load -i  citibike-learn-0.9.tar
```

#### Ok now I can continue trying to get spark setup..
* Per the [post](https://medium.com/faun/apache-spark-on-kubernetes-docker-for-mac-2501cc72e659) , I grabbed spark albeit `3.0.1` , instead of `2.x` ( from [here](https://www.apache.org/dyn/closer.lua/spark/spark-3.0.1/spark-3.0.1-bin-hadoop3.2.tgz) )  , because according to the [release notes](https://databricks.com/blog/2020/06/18/introducing-apache-spark-3-0-now-available-in-databricks-runtime-7-0.html) , 3.0 and 2.x are sounding very compatible.

```
./bin/docker-image-tool.sh -t spark-docker build
```

* ... following along...

```
kubectl create serviceaccount spark
# serviceaccount/spark created

kubectl create clusterrolebinding spark-role --clusterrole=edit  --serviceaccount=default:spark --namespace=default
# clusterrolebinding.rbac.authorization.k8s.io/spark-role created
```

* And submitting an example job

```
bin/spark-submit  \
    --master k8s://https://localhost:6443  \
    --deploy-mode cluster  \
    --conf spark.executor.instances=1  \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  \
    --conf spark.kubernetes.container.image=spark:spark-docker  \
    --class org.apache.spark.examples.SparkPi  \
    --name spark-pi  \
    local:///opt/spark/examples/jars/spark-examples_2.12-3.0.1.jar
```
* Taking `4 minutes` so far. Not sure how long this is meant to take haha.

* I tried https://localhost:6443/ from my browser but got denied for now, as below...

```
{
kind: "Status",
apiVersion: "v1",
metadata: { },
status: "Failure",
message: "forbidden: User "system:anonymous" cannot get path "/"",
reason: "Forbidden",
details: { },
code: 403
}
```

* I tried the `kubectl get pods ` command and I can see the run time so far..

```
$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
spark-pi-4df4497735de91a1-driver   1/1     Running   0          6m1s
spark-pi-79033a7735deb0a4-exec-1   0/1     Pending   0          5m52s
```

* Likely something is blocking. (Actually I noticed my Dropbox was being pretty aggressive. so I paused that.)

##### enabling port forwarding to get access to the dashboard..

```
kubectl get pods -n kube-system
```
```
NAME                                     READY   STATUS    RESTARTS   AGE
coredns-f9fd979d6-pdx99                  1/1     Running   0          30m
coredns-f9fd979d6-vjpfp                  1/1     Running   0          30m
etcd-docker-desktop                      1/1     Running   0          29m
kube-apiserver-docker-desktop            1/1     Running   0          29m
kube-controller-manager-docker-desktop   1/1     Running   0          29m
kube-proxy-42wws                         1/1     Running   0          30m
kube-scheduler-docker-desktop            1/1     Running   0          29m
storage-provisioner                      1/1     Running   0          29m
vpnkit-controller                        1/1     Running   0          29m
```

* and hmm I cant run `kubectl port-forward kubernetes-dashboard-7b9c7bc8c9-ckfmr 8443:8443 -n kube-system` because I dont have that running looks like .

* Ah according to [here](https://medium.com/backbase/kubernetes-in-local-the-easy-way-f8ef2b98be68) the kubernetes dashboard does not come _out of the box_


* Per [here](https://stackoverflow.com/a/30094032/472876) tried killing

```
# ./bin/spark-class org.apache.spark.deploy.Client kill <master url> <driver ID>
./bin/spark-class org.apache.spark.deploy.Client kill k8s://https://localhost:6443 spark-pi-4df4497735de91a1-driver

WARNING: This client is deprecated and will be removed in a future version of Spark
Use ./bin/spark-submit with "--master spark://host:port"
log4j:WARN No appenders could be found for logger (org.apache.hadoop.util.NativeCodeLoader).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.

...
Exception in thread "main" org.apache.spark.SparkException: Invalid master URL: spark://k8s://https://localhost:6443

```
* Crashed... anyway just `Ctrl-C` for now
* But when looking around I see per [here](https://issues.apache.org/jira/browse/SPARK-11909) that the master url in that command should be `spark://localhost:6443` instead.
* And per [this note](https://sparkbyexamples.com/spark/spark-how-to-kill-running-application/) , yarn is mentioned too. I dont have that yet however.

* TRy to get that dashboard , following from [here](https://medium.com/backbase/kubernetes-in-local-the-easy-way-f8ef2b98be68)
* It is here, https://github.com/kubernetes/dashboard/releases/tag/v2.0.5

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.5/aio/deploy/recommended.yaml

namespace/kubernetes-dashboard created
serviceaccount/kubernetes-dashboard created
service/kubernetes-dashboard created
secret/kubernetes-dashboard-certs created
secret/kubernetes-dashboard-csrf created
secret/kubernetes-dashboard-key-holder created
configmap/kubernetes-dashboard-settings created
role.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrole.rbac.authorization.k8s.io/kubernetes-dashboard created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
clusterrolebinding.rbac.authorization.k8s.io/kubernetes-dashboard created
deployment.apps/kubernetes-dashboard created
service/dashboard-metrics-scraper created
deployment.apps/dashboard-metrics-scraper created
```

* Hmm I did not see the dashboard with `kubectl get pods -n kube-system`, but the mentioned to look using  `kubectl get pods --all-namespaces` , and I do see it indeed , in its own namespace indeed... not in the `kube-system` namespace

```
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
kubernetes-dashboard   kubernetes-dashboard-6f65cb5c64-kbq8d        1/1     Running   0          2m46s
```

* Not seeing anything listening on `8443` with `netstat -an |grep LIST` however, as mentioned [here](https://medium.com/faun/apache-spark-on-kubernetes-docker-for-mac-2501cc72e659)
* But the other  blog post is telling me to go here , http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy
* After first starting a local proxy that is..

```
kubectl proxy
# Starting to serve on 127.0.0.1:8001
```

* As mentioned, when I visited this url, I saw the screen asking for a token.
* And running the one liner ,

```
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | awk '/^deployment-controller-token-/{print $1}') | awk '$1=="token:"{print $2}'
```
* Yielded a token, which was accepted.

#### let me retry that earlier example job ..
* Since now I can look at the dashboard. Maybe I will see why that job was stalling..
* trying again

```
bin/spark-submit  \
--master k8s://https://localhost:6443  \
--deploy-mode cluster  \
--conf spark.executor.instances=1  \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  \
--conf spark.kubernetes.container.image=spark:spark-docker  \
--class org.apache.spark.examples.SparkPi  \
--name spark-pi  \
local:///opt/spark/examples/jars/spark-examples_2.12-3.0.1.jar
```
* One of the early outputs...

```
21/01/24 16:03:01 INFO KerberosConfDriverFeatureStep: You have not specified a krb5.conf file locally or via a ConfigMap. Make sure that you have the krb5.conf locally on the driver image.
```
* And basically now stuck in `Pending`.

##### Insufficient Memory!
* Ok so when I looked around in the Dashboard, I see oddly ... the first attempt could not succeed because of memory

<img src="https://s3.amazonaws.com/my-blog-content/2021-01-23-spark-weekend/Screen Shot 2021-01-24 at 4.15.17 PM-insufficient-memory.png" width="50%">

* Oh and it is hanging around still blocking resources.
```
$ kubectl get pods --all-namespaces
NAMESPACE              NAME                                         READY   STATUS    RESTARTS   AGE
default                spark-pi-4df4497735de91a1-driver             1/1     Running   0          116m
default                spark-pi-79033a7735deb0a4-exec-1             0/1     Pending   0          116m
default                spark-pi-df12a57736350578-driver             0/1     Pending   0          21m
default                spark-pi-e333f47736434a39-driver             0/1     Pending   0          6m16s
```
* So actually `Ctrl-C` was not enough to kill it.
* When I look at the logs for this driver pod, I'm seeing

```
21/01/24 21:23:30 WARN TaskSchedulerImpl: Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources
```
* Not sure how to know what resources are needed though.

##### Deleting this pod
* Kind of handy , when I try deleting that pod in the dashboard , I'm seeing a handy note that

```
This action is equivalent to:kubectl delete -n default pod spark-pi-4df4497735de91a1-driver
```
* And as soon as that was terminated, the Pending job is running. So yea none of my `Ctrl-C` were useful haha.
* Trying that CLI delete instead then

```
kubectl delete -n default pod spark-pi-df12a57736350578-driver
```
* Ok that seems to have worked.

#### How to try this again without the memory issue?
* not sure but...

#### Read about the pyspark shell being in the base spark so trying
* nice ..

```python
$ ./bin/pyspark
Python 3.7.2 (default, Dec 29 2018, 00:00:04)
[Clang 4.0.1 (tags/RELEASE_401/final)] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
21/01/24 17:21:27 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 3.0.1
      /_/

Using Python version 3.7.2 (default, Dec 29 2018 00:00:04)
SparkSession available as 'spark'.
```
```python
from pyspark.context import SparkContext
sc = SparkContext('local', 'test')
```
Oops

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/context.py", line 133, in __init__
    SparkContext._ensure_initialized(self, gateway=gateway, conf=conf)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/context.py", line 341, in _ensure_initialized
    callsite.function, callsite.file, callsite.linenum))
ValueError: Cannot run multiple SparkContexts at once; existing SparkContext(app=PySparkShell, master=local[*]) created by <module> at /Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/shell.py:41

```
* oh interesting it is already pre defined

```
>>> sc
<SparkContext master=local[*] appName=PySparkShell>
```
* Will try something basic..

```python
rdd = sc.parallelize([1, 2, 3, 4])
rdd
# ParallelCollectionRDD[0] at readRDDFromFile at PythonRDD.scala:262

rdd.map(lambda x: x*3)
# PythonRDD[1] at RDD at PythonRDD.scala:53

rdd.collect()
# [1, 2, 3, 4]
```
* ok haha not quite right.
* Ah duh of course have to compose/chain that..

```python
rdd.map(lambda x: x*3).collect()
# [3, 6, 9, 12]                                                                   
rdd.collect()
# [1, 2, 3, 4]
```
* Ok excellent!
* Going to look more through these docs [here](spark.apache.org/docs/latest/api/python/index.html)


#### Next
* I would like to try some more basic transformations and actions.

### 2021-01-31

#### try some things on this covid19 dataset
* from [here](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data/vbim-akqf)
* This is a `1.59GiB` file , so perfect, how do I use Spark to split this up and perform some basic statistics
* `COVID-19_Case_Surveillance_Public_Use_Data.csv`
* Specifically, I think a good idea to test if random sampling this data, the `onset_dt` or onset date of symptoms, what is the onset rate by age bin, which is already binned as `age_group`.
* Ah and looks like you need to be explicit with specifying a header is present.

```python
workdir = '/Users/michal/Downloads/'
loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head.csv'

df = spark.read.option("header",True).csv(loc)

df.printSchema()
```
```python
root
 |-- cdc_case_earliest_dt : string (nullable = true)
 |-- cdc_report_dt: string (nullable = true)
 |-- pos_spec_dt: string (nullable = true)
 |-- onset_dt: string (nullable = true)
 |-- current_status: string (nullable = true)
 |-- sex: string (nullable = true)
 |-- age_group: string (nullable = true)
 |-- race_ethnicity_combined: string (nullable = true)
 |-- hosp_yn: string (nullable = true)
 |-- icu_yn: string (nullable = true)
 |-- death_yn: string (nullable = true)
 |-- medcond_yn: string (nullable = true)

```

### 2021-02-07

#### Symptomatic by age group.
* Hmm interesting that [in docs](https://spark.apache.org/docs/latest/api/python/pyspark.sql.html#pyspark.sql.DataFrameReader.jdbc) is says that so does that mean that all the partitions are running in parallel? How do you only run based on the number of workers you can run simultaneously?

> Note: Don’t create too many partitions in parallel on a large cluster; otherwise Spark might crash your external database systems.

```python
df.groupBy('age_group').count().collect()

[Row(age_group='0 - 9 Years', count=9)]                                         

```
* Try w/ a column that has more variation.. and `1000` rows instead.

```python
loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head1000.csv'
df = spark.read.option("header",True).csv(loc)
df.groupBy('sex').count().collect()

# [Row(sex='Female', count=446), Row(sex='Unknown', count=30), Row(sex='Missing', count=3), Row(sex='Male', count=520)]

```
* And how do I apply a custom `apply` function with my group by

```python
def foo(dfx):
    return dfx.count()


df.groupBy('sex').apply(foo)
```

```python
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/sql/pandas/group_ops.py", line 70, in apply
    raise ValueError("Invalid udf: the udf argument must be a pandas_udf of type "
ValueError: Invalid udf: the udf argument must be a pandas_udf of type GROUPED_MAP.
```
* hmm oops

```python
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructType, StringType, LongType, DoubleType, StructField

schema = StructType([StructField('sex', StringType(), True),
                     StructField('onset_dt', StringType(), True)])

@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def foo(dfx):
    return dfx.count()
```

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/sql/pandas/functions.py", line 325, in pandas_udf
    require_minimum_pyarrow_version()
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/sql/pandas/utils.py", line 54, in require_minimum_pyarrow_version
    "it was not found." % minimum_pyarrow_version)
ImportError: PyArrow >= 0.15.1 must be installed; however, it was not found.
```

* hmm

```python
(pandars3) $ pip install  PyArrow
Collecting PyArrow
  Downloading https://files.pythonhosted.org/packages/68/5f/1fb0c604636d46257af3c3075955e860161e8c41386405467f073df73f91/pyarrow-3.0.0-cp37-cp37m-macosx_10_13_x86_64.whl (14.1MB)
    100% |████████████████████████████████| 14.1MB 1.6MB/s
Collecting numpy>=1.16.6 (from PyArrow)
  Downloading https://files.pythonhosted.org/packages/68/30/a8ce4cb0c084cc1442408807dde60f9796356ea056ca6ef81c865a3d4e62/numpy-1.20.1-cp37-cp37m-macosx_10_9_x86_64.whl (16.0MB)
    100% |████████████████████████████████| 16.0MB 1.3MB/s
tensorboard 1.14.0 has requirement setuptools>=41.0.0, but you'll have setuptools 40.6.3 which is incompatible.
Installing collected packages: numpy, PyArrow
  Found existing installation: numpy 1.16.0
    Uninstalling numpy-1.16.0:
      Successfully uninstalled numpy-1.16.0
Successfully installed PyArrow-3.0.0 numpy-1.20.1
```

* Ok cool now this worked ..

```python

from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructType, StringType, LongType, DoubleType, StructField

schema = StructType([StructField('sex', StringType(), True),
                     StructField('onset_dt', StringType(), True)])

@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def foo(dfx):
    return dfx.count()


workdir = '/Users/michal/Downloads/'

loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head1000.csv'
df = spark.read.option("header",True).csv(loc)
df.groupBy('sex').count().collect()

#
out = df.groupBy('sex').apply(foo)
```
* Really weird error though haha...

```python
>>> out.collect()
21/02/07 23:33:31 ERROR Executor: Exception in task 60.0 in stage 6.0 (TID 205)]
org.apache.spark.api.python.PythonException: Traceback (most recent call last):
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 605, in main
    process()
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 597, in process
    serializer.dump_stream(out_iter, outfile)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 255, in dump_stream
    return ArrowStreamSerializer.dump_stream(self, init_stream_yield_batches(), stream)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 88, in dump_stream
    for batch in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 248, in init_stream_yield_batches
    for series in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 210, in load_stream
    yield [self.arrow_to_pandas(c) for c in pa.Table.from_batches([batch]).itercolumns()]
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 210, in <listcomp>
    yield [self.arrow_to_pandas(c) for c in pa.Table.from_batches([batch]).itercolumns()]
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 236, in arrow_to_pandas
    s = super(ArrowStreamPandasUDFSerializer, self).arrow_to_pandas(arrow_column)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 128, in arrow_to_pandas
    s = arrow_column.to_pandas(date_as_object=True)
  File "pyarrow/array.pxi", line 751, in pyarrow.lib._PandasConvertible.to_pandas
  File "pyarrow/table.pxi", line 224, in pyarrow.lib.ChunkedArray._to_pandas
  File "pyarrow/array.pxi", line 1310, in pyarrow.lib._array_like_to_pandas
  File "pyarrow/error.pxi", line 116, in pyarrow.lib.check_status
pyarrow.lib.ArrowException: Unknown error: Wrapping 2020/03/�9 failed

	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.handlePythonException(PythonRunner.scala:503)
	at org.apache.spark.sql.execution.python.PythonArrowOutput$$anon$1.read(PythonArrowOutput.scala:99)
	at org.apache.spark.sql.execution.python.PythonArrowOutput$$anon$1.read(PythonArrowOutput.scala:49)
	at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:456)
	at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
	at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:489)
	at scala.collection.Iterator$$anon$10.hasNext(Iterator.scala:458)
	at org.apache.spark.sql.execution.SparkPlan.$anonfun$getByteArrayRdd$1(SparkPlan.scala:340)
	at org.apache.spark.sql.execution.SparkPlan$$Lambda$2055/64856516.apply(Unknown Source)
	at org.apache.spark.rdd.RDD.$anonfun$mapPartitionsInternal$2(RDD.scala:872)
	at org.apache.spark.rdd.RDD.$anonfun$mapPartitionsInternal$2$adapted(RDD.scala:872)
	at org.apache.spark.rdd.RDD$$Lambda$2051/1858155754.apply(Unknown Source)
	at org.apache.spark.rdd.MapPartitionsRDD.compute(MapPartitionsRDD.scala:52)
	at org.apache.spark.rdd.RDD.computeOrReadCheckpoint(RDD.scala:349)
	at org.apache.spark.rdd.RDD.iterator(RDD.scala:313)
	at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:90)
	at org.apache.spark.scheduler.Task.run(Task.scala:127)
	at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$3(Executor.scala:446)
	at org.apache.spark.executor.Executor$TaskRunner$$Lambda$2018/1084937392.apply(Unknown Source)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1377)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:449)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
	at java.lang.Thread.run(Thread.java:745)

```

### 2021-02-20

#### Going to attempt to use ipython w/ pyspark
* According to [stackoverflow](https://stackoverflow.com/questions/31862293/how-to-load-ipython-shell-with-pyspark#31863595)

```python
PYSPARK_DRIVER_PYTHON=ipython ./bin/pyspark
```
* Ok nice worked. Just had to make sure to `source activate pandars3` my conda environment which actually has `ipython` ..

#### Hmm maybe since i had errors w/ group by , I can try   `reduceByKey` intead?
* oh actually, when looking at the doc for the group by with `help(df.groupBy('sex'))` , I read in the `apply` description that it is depracated and  `applyInPandas` is recommended instead.
* And in the [apache spark doc here](https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html#pandas-function-apis)  , I'm reading that " Using PandasUDFType will be deprecated in the future."  so then the complicated decorator looking code I was trying above, maybe that is getting phased out anyway.
* The only thing new here is that I need to pass the schema of the dataframe to `applyInPandas`
* My particualr dataset is actually all categorical data and dates.

```python
def foo(dfx):
    return dfx.count()

#
workdir = '/Users/michal/Downloads/'
loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head.csv'


df = spark.read.option("header",True).csv(loc)     

from pyspark.sql.types import StructType, StringType, LongType, DoubleType, StructField

# Let me try to treat them all as nullable strings for now...
schema = StructType([StructField(x, StringType(), True)
                     for x in df.columns
                     ])


df.groupBy('sex').applyInPandas(foo, schema).collect()

```

* => ok now error I got is actually more clear...

```python
PythonException:
  An exception was thrown from the Python worker. Please see the stack trace below.
Traceback (most recent call last):
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 605, in main
    process()
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 597, in process
    serializer.dump_stream(out_iter, outfile)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 255, in dump_stream
    return ArrowStreamSerializer.dump_stream(self, init_stream_yield_batches(), stream)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 88, in dump_stream
    for batch in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 248, in init_stream_yield_batches
    for series in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 429, in mapper
    return f(keys, vals)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 175, in <lambda>
    return lambda k, v: [(wrapped(k, v), to_arrow_type(return_type))]
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 167, in wrapped
    "pandas.DataFrame, but is {}".format(type(result)))
TypeError: Return type of the user-defined function should be pandas.DataFrame, but is <class 'pandas.core.series.Series'>
```

* So  let me make sure to return a dataframe in my `foo` func

```python
import pandas as pd

def foo(dfx):
    # This group by key
    key = dfx.limit(1)[0].sex
    return pd.DataFrame({'sex': key, 'count': dfx.count()})
#


schema = StructType([StructField(x, StringType(), True)
                     for x in df.columns
                     ])
#
df.groupBy('sex').applyInPandas(foo, schema).collect()


```
* Now getting the error..

```
PythonException:
  An exception was thrown from the Python worker. Please see the stack trace below.
  ...
AttributeError: 'DataFrame' object has no attribute 'limit'

```
* Hmm so literally the input is a vanilla pandas dataframe I think oh that's why!


```python
def foo(dfx):
    # This group by key
    key = dfx.iloc[0].sex
    return pd.DataFrame({'sex': key, 'count': dfx.count()})

#
schema = StructType([StructField(x, StringType(), True)
                     for x in df.columns
                     ])

df.groupBy('sex').applyInPandas(foo, schema).collect()


```

* hmm..

```python


PythonException:
  An exception was thrown from the Python worker. Please see the stack trace below.
Traceback (most recent call last):
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 605, in main
    process()
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 597, in process
    serializer.dump_stream(out_iter, outfile)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 255, in dump_stream
    return ArrowStreamSerializer.dump_stream(self, init_stream_yield_batches(), stream)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 88, in dump_stream
    for batch in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/sql/pandas/serializers.py", line 248, in init_stream_yield_batches
    for series in iterator:
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 429, in mapper
    return f(keys, vals)
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 175, in <lambda>
    return lambda k, v: [(wrapped(k, v), to_arrow_type(return_type))]
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/worker.py", line 160, in wrapped
    result = f(pd.concat(value_series, axis=1))
  File "/Users/michal/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/pyspark.zip/pyspark/util.py", line 107, in wrapper
    return f(*args, **kwargs)
  File "<ipython-input-54-736ec161f4f7>", line 4, in foo
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/frame.py", line 392, in __init__
    mgr = init_dict(data, index, columns, dtype=dtype)
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/internals/construction.py", line 212, in init_dict
    return arrays_to_mgr(arrays, data_names, index, columns, dtype=dtype)
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/internals/construction.py", line 56, in arrays_to_mgr
    arrays = _homogenize(arrays, index, dtype)
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/internals/construction.py", line 277, in _homogenize
    raise_cast_failure=False)
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/internals/construction.py", line 642, in sanitize_array
    value, len(index), dtype)
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/pandas/core/dtypes/cast.py", line 1187, in construct_1d_arraylike_from_scalar
    subarr = np.empty(length, dtype=dtype)
TypeError: Cannot interpret '<attribute 'dtype' of 'numpy.generic' objects>' as a data type

```

```python
schema = StructType([StructField('sex', StringType(), True),
                     StructField('count', LongType(), True)
                     ])
df.groupBy('sex').applyInPandas(foo, schema).collect()
```

* group to try the string schema usage instead

```python
schema = ', '.join([f'{x} string' for x in df.columns]); schema                                                               
# 'cdc_case_earliest_dt string, cdc_report_dt string, pos_spec_dt string, onset_dt string, current_status string, sex string, age_group string, race_ethnicity_combined string, hosp_yn string, icu_yn string, death_yn string, medcond_yn string'


df.groupBy('sex').applyInPandas(foo, schema).collect()

```
* Dang same error. Maybe doesnt like string type group bys?

* Randomly reading this may be something to do w/ old pandas version?

```

In [68]: pd.__version__                                                                                                                
Out[68]: '0.24.2'

```
* I upgraded to `1.0.5`


```python
import pandas as pd

workdir = '/Users/michal/Downloads/'

loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head1000.csv'
df = spark.read.option("header",True).csv(loc)

def foo(dfx):
    # This group by key
    key = dfx.iloc[0].sex
    return pd.DataFrame({'sex': key, 'count': dfx.count()})

#

schema = 'sex string, count int'
#
df.groupBy('sex').applyInPandas(foo, schema).collect()




```

* now a different error..

```
pyarrow.lib.ArrowException: Unknown error: Wrapping 2020/03/�6 failed

```
* Makes me think I have some garbage data
* Trying the 10 line datafile i have instead

```python

loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head1000.csv'
df = spark.read.option("header",True).csv(loc)

# everything else is the same ..
```
* WOw now a scala/java error..

```
21/02/20 22:19:32 ERROR Executor: Exception in task 60.0 in stage 8.0 (TID 406)]
org.apache.spark.SparkException: Python worker exited unexpectedly (crashed)
...
at org.apache.spark.api.python.BasePythonRunner$ReaderIterator$$anonfun$1.applyOrElse(PythonRunner.scala:536)
at org.apache.spark.api.python.BasePythonRunner$ReaderIterator$$anonfun$1.applyOrElse(PythonRunner.scala:525)
at scala.runtime.AbstractPartialFunction.apply(AbstractPartialFunction.scala:38)
at org.apache.spark.sql.execution.python.PythonArrowOutput$$anon$1.read(PythonArrowOutput.scala:105)
at org.apache.spark.sql.execution.python.PythonArrowOutput$$anon$1.read(PythonArrowOutput.scala:49)
at org.apache.spark.api.python.BasePythonRunner$ReaderIterator.hasNext(PythonRunner.scala:456)
at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:37)
at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:489)
at scala.collection.Iterator$$anon$10.hasNext(Iterator.scala:458)
at org.apache.spark.sql.execution.SparkPlan.$anonfun$getByteArrayRdd$1(SparkPlan.scala:340)
at org.apache.spark.sql.execution.SparkPlan$$Lambda$2055/1769623532.apply(Unknown Source)
at org.apache.spark.rdd.RDD.$anonfun$mapPartitionsInternal$2(RDD.scala:872)
at org.apache.spark.rdd.RDD.$anonfun$mapPartitionsInternal$2$adapted(RDD.scala:872)
at org.apache.spark.rdd.RDD$$Lambda$2051/917090051.apply(Unknown Source)
at org.apache.spark.rdd.MapPartitionsRDD.compute(MapPartitionsRDD.scala:52)
at org.apache.spark.rdd.RDD.computeOrReadCheckpoint(RDD.scala:349)
at org.apache.spark.rdd.RDD.iterator(RDD.scala:313)
at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:90)
at org.apache.spark.scheduler.Task.run(Task.scala:127)
at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$3(Executor.scala:446)
at org.apache.spark.executor.Executor$TaskRunner$$Lambda$2018/644307005.apply(Unknown Source)
at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:1377)
at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:449)
at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1142)
at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:617)
at java.lang.Thread.run(Thread.java:745)
Caused by: java.io.EOFException
at java.io.DataInputStream.readInt(DataInputStream.java:392)
at org.apache.spark.sql.execution.python.PythonArrowOutput$$anon$1.read(PythonArrowOutput.scala:86)
... 22 more



21/02/20 22:19:32 ERROR TaskSetManager: Task 159 in stage 8.0 failed 1 times; aborting job
---------------------------------------------------------------------------
Py4JJavaError                             Traceback (most recent call last)
<ipython-input-3-e6065af68166> in <module>
     15 schema = 'sex string, count int'
     16 #
---> 17 df.groupBy('sex').applyInPandas(foo, schema).collect()
     18

~/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/sql/dataframe.py in collect(self)
    594         """
    595         with SCCallSiteSync(self._sc) as css:
--> 596             sock_info = self._jdf.collectToPython()
    597         return list(_load_from_socket(sock_info, BatchedSerializer(PickleSerializer())))
    598

~/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/py4j-0.10.9-src.zip/py4j/java_gateway.py in __call__(self, *args)
   1303         answer = self.gateway_client.send_command(command)
   1304         return_value = get_return_value(
-> 1305             answer, self.gateway_client, self.target_id, self.name)
   1306
   1307         for temp_arg in temp_args:

~/Downloads/spark-3.0.1-bin-hadoop3.2/python/pyspark/sql/utils.py in deco(*a, **kw)
    126     def deco(*a, **kw):
    127         try:
--> 128             return f(*a, **kw)
    129         except py4j.protocol.Py4JJavaError as e:
    130             converted = convert_exception(e.java_exception)

~/Downloads/spark-3.0.1-bin-hadoop3.2/python/lib/py4j-0.10.9-src.zip/py4j/protocol.py in get_return_value(answer, gateway_client, target_id, name)
    326                 raise Py4JJavaError(
    327                     "An error occurred while calling {0}{1}{2}.\n".
--> 328                     format(target_id, ".", name), value)
    329             else:
    330                 raise Py4JError(

Py4JJavaError: An error occurred while calling o148.collectToPython.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 159 in stage 8.0 failed 1 times, most recent failure: Lost task 159.0 in stage 8.0 (TID 409, 192.168.16.173, executor driver): org.apache.spark.SparkException: Python worker exited unexpectedly (crashed)


```
* hahaha that is great.

#### The toy example does work though
* from the [docs](https://spark.apache.org/docs/latest/sql-pyspark-pandas-with-arrow.html#grouped-map)

```python

df = spark.createDataFrame(
    [(1, 1.0), (1, 2.0), (2, 3.0), (2, 5.0), (2, 10.0)],
    ("id", "v"))

def subtract_mean(pdf):
    # pdf is a pandas.DataFrame
    v = pdf.v
    return pdf.assign(v=v - v.mean())

df.groupby("id").applyInPandas(subtract_mean, schema="id long, v double").show()


+----+----+                                                                     
|  id|   v|
+----+----+
|   1| 0.0|
|null|null|
|   2| 0.0|
|null|null|
|null|null|
+----+----+

```
* Hmm so my guess is the string group by is not appreciated..?


##### uummm tried again w/ the small file and this time worked... well didnt crash at least..

```python
import pandas as pd

workdir = '/Users/michal/Downloads/'

loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head.csv'
df = spark.read.option("header",True).csv(loc)

def foo(dfx):
    # This group by key
    key = dfx.iloc[0].sex
    return pd.DataFrame({'sex': key, 'count': dfx.count()})

#

schema = 'sex string, count int'
#
df.groupBy('sex').applyInPandas(foo, schema).collect()
```

```
[Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=3),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Female', count=7),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=1),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2),
 Row(sex='Male', count=2)]
```

* But now this output looks like well not what I would expect.
* I expect two rows since you know, this is a group by. So hmm
* But in any case, at least it is not crashing! so major improvement.
* Hmm unless this is a partitioned group by... hmm that would be exciting. So the group by has to be combined?
* So could it be I have `12` partitions here?  But the file only has `9` rows. Weird.

#### oh the apply func can take the key as an arg ?

```python
import pandas as pd

workdir = '/Users/michal/Downloads/'

loc = f'{workdir}/COVID-19_Case_Surveillance_Public_Use_Data.head.csv'
df = spark.read.option("header",True).csv(loc)

def foo(key, dfx):
    """
    Args:
        key: tuple of the group by keys.
        dfx: pandas df for the given group by key.
    """
    return pd.DataFrame({'sex': key[0], 'count': dfx.count()})

#
schema = 'sex string, count int'
#
df.groupBy('sex').applyInPandas(foo, schema).show()
```

* result is same, but since using `show()` instead of `collect()` this time, the output looks slightly different
* Still don't know why more than two rows though ..

```python

+------+-----+
|   sex|count|
+------+-----+
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    3|
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    7|
|Female|    7|
|  Male|    2|
|  null| null|
|  Male|    2|
|  null| null|
|  Male| null|
|  null| null|
|  null| null|
|  null| null|
+------+-----+
only showing top 20 rows


```
