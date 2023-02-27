---
title: Mini scikit-learn backwards compatibility story
date: 2022-07-12
---

- hmm blah blah
	- test something
- #publish-this
	- ## What
	- So I had a particular need to load a #[[scikit learn sklearn]] model trained with   `0.20.4` on Databricks 10.4 and ran into some fun details
	- I was not initially able to use the Databricks 10.4 pinned version of scikit-learn , 0.24.x because of course there were #backwards-compatibility issues where trying to load the model gave me an error saying that `ModuleNotFoundError: No module named 'sklearn.preprocessing.imputation'` was not found basically because I learned that all the Imputers were moved over to `sklearn.impute`
	- I tried also just vetting the assumption that I can simply pip install this earlier version of scikit learn. And turned out that well yes I can. But,
	- ![IMG_8096](https://s3.amazonaws.com/my-blog-content/2022/2022-07-12-Mini-scikit-learn-backwards-compatibility-story/IMG_8096.jpg)
	- But then when I try to `import sklearn` , oops, that gives a strange error
	- ![IMG_8095](https://s3.amazonaws.com/my-blog-content/2022/2022-07-12-Mini-scikit-learn-backwards-compatibility-story/IMG_8095.jpg)
	- and trying to look for using #conda to the rescue , well I looked around on https://anaconda.org and I ended up seeing that there is `0.20.2` from `cctbx` and then I saw `0.20.3` from `cdat-forge` so then trying that I basically got 
	  
	  ```python
	  
	  (pandars310) $ conda install -c cdat-forge scikit-learn=0.20.3
	  Collecting package metadata (current_repodata.json): done
	  Solving environment: failed with initial frozen solve. Retrying with flexible solve.
	  Solving environment: failed with repodata from current_repodata.json, will retry with next repodata source.
	  Collecting package metadata (repodata.json): done
	  Solving environment: failed with initial frozen solve. Retrying with flexible solve.
	  Solving environment: | 
	  Found conflicts! Looking for incompatible packages.
	  This can take several minutes.  Press CTRL-C to abort.
	  failed                                                                                         
	  
	  UnsatisfiableError: The following specifications were found
	  to be incompatible with the existing python installation in your environment:
	  
	  Specifications:
	  
	    - scikit-learn=0.20.3 -> python[version='>=2.7,<2.8.0a0|>=3.7,<3.8.0a0|>=3.6,<3.7.0a0']
	  
	  Your python: python=3.10
	  
	  If python is on the left-most side of the chain, that's the version you've asked for.
	  When python appears to the right, that indicates that the thing on the left is somehow
	  not available for the python version you are constrained to. Note that conda will not
	  change your python version to a different minor version unless you explicitly specify
	  that.
	  
	  ```
	- So aha I learned that if I want to use this earlier version of scikit learn then I would need `<3.8` basically but Databricks 10.4 has pinned `python 3.8` so basically that is a no go and this model just needs to be retrained to be used.
	-