---
title: Spark Weekend
date: 2021-01-23
tags: notebook
---

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
