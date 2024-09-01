
# initial approach
I know more about Databricks for distributed computing. But there is also the Kubernetes world. Let’s read some more on that.

Was wondering hmm, I have used Tensorflow, pytorch on standalone VMs in the past and I know that Spark has its own distributed libraries, so do  Tensorflow, pytorch natively support spark, hmm? (Basically learned no)

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





