
# motivation
I know more about Databricks for distributed computing. But there is also the Kubernetes world. Let’s read some more on that.

Was wondering hmm, I have used Tensorflow, pytorch on standalone VMs in the past and I know that Spark has its own distributed libraries, so do  Tensorflow, pytorch natively support spark, hmm? (Basically learned no)

## lingering questions
(1) What are the dominant technologies for distributed computing? (spark, and containerization by K8S)
(2) specifically GPU vs cluster based, are these alternatives? (learning hybrid actually common too.)
(3) Are the typical deep learning options (Tensorflow, pytorch) abstracted by Horovod/ TFJobs or did Tensorflow , pytorch need to be modified to suport multiple clusters ? Wondering about the level of abtraction basically.
(4) Back prop has some parallelization opportunities , but there are lot of dependencies too. wondering, hmm, what are some parallelization methods w.r.t. what us available? 
(5) are Horovod (and TFJobs) only really for deep learning or how about xgboost? (ah xgboost has its own, not on top of Horovod though)
## the dominant architectures/frameworks?
Somehow I got the impression that, since whenever I opened up a google colab notebook in the past and saw GPU set up for tensorflow, and then later when I started working with Databricks, I got the impression that GPU and clusters were an either or thing.

### I learned 
- Not just GPU distributted vs cluster distributed, but also hybrid of these.
- oh and both Databricks ane Kubernetes can be used for hybrid. 
- But interestingly Databricks / spark, stepped away from distributed. Originally had **Spark Deep Learning Libraries**, but today, only Horovod and TFJobs . 
	- Shifted focus, perhaps because lots already options, market saturated . 
- Also there are a few others, less widely used,  **Spark on Ray**,  and **BigDL**, 
- And **Dask**,  though not particularly for deep learning. (but **dask** can extend scikit-learn )
- **Deep Speed**,  from **Microsoft**,  but hmm not well known I think. 
- Few years ago Google introduced JAX ([jax](https://github.com/google/jax) ) as a competitor since pytorch ( facebook ) , grew more popular. 

## how do Tensorflow / pytorch actually work on Databricks, or can they even?
I was wondering , do Horovod, basically abstract away existance of the distributed environment ? Learned that mostly yes. But that TensorFlow , pytorch have some knowledge about the multiple clusters too.

## Can you theoretically infinitely scale out , therefore , as wide as you wish?

## parallelization strategies
data partitioning and `allreduce` . 


## MPI
interestingly learned MPI , used by Horovod. More low level.

## Also interesting comparison, distributed training and distributed inference
hmm

## back prop distributed training approaches
Apparently there is a kind of distributed training where back prop gradient updates on minibatches are not synchronized. And can cause convergence to take longer or be harder (think lower learning rate suggested for those cases). So this is  synchronous  vs asynchronous. And yea 






