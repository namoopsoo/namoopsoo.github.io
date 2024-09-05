
# initial approach
I know more about Databricks for distributed computing. But there is also the Kubernetes world. Let’s read some more on that.

Was wondering hmm, I have used Tensorflow, pytorch on standalone VMs in the past and I know that Spark has its own distributed libraries, so do  Tensorflow, pytorch natively support spark, hmm? (Basically learned no)

## A few topics spawned 
(1) What are the dominant technologies for distributed computing? (spark, and containerization by K8S)
(2) specifically GPU vs cluster based, are these alternatives? (learning hybrid actually common too.)
(3) Are the typical deep learning options (Tensorflow, pytorch) abstracted by Horovod/ TFJobs or did Tensorflow , pytorch need to be modified to suport multiple clusters ? Wondering about the level of abtraction basically.
(4) Back prop has some parallelization opportunities , but there are lot of dependencies too. wondering, hmm, what are some parallelization methods w.r.t. what us available? 

(5) are Horovod (and TFJobs) only really for deep learning or how about xgboost? (ah xgboost has its own, not on top of Horovod though)
## the dominant architectures/frameworks? 
- Not just GPU distributted vs cluster distributed, but also hybrid of these.
- oh and both Databricks ane Kubernetes can be used for hybrid. 
- But interestingly Databricks / spark, stepped away from distributed. Originally had **Spark Deep Learning Libraries**, but today, only Horovod and TFJobs . 
	- Shifted focus, perhaps because lots already options, market saturated . 
- There are a few others, less widely used,  **Spark on Ray**,  and **BigDL**, 
- And **Dask**,  not particularly for deep learning.
- **Deep Speed**,  from **Microsoft**,  but hmm not well known I think. 

## but how to distribute Tensorflow , pytorch?
I was wondering , do Horovod, basically abstract away existance of the distributed environment ? Learned that mostly yes. But that TensorFlow , pytorch have some knowledge about the multiple cclusters too.

## MPI
interestingly learned MPI , used by Horovod. More low level.

## Also interesting comparison, distributed training and distributed inference
hmm

## back prop distributed training approaches
Apparently there is a kind of distributed training where back prop gradient updates on minibatches are not synchronized. And can cause convergence to take longer or be harder (think lower learning rate suggested for those cases). So this is  synchronous  vs asynchronous. And yea 






