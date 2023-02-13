---
title: Dockerizing Daniel Bourke's Food Not Food
date: 2022-11-12
tags: docker, tensorflow
---
I have this on-going effort to be able to more easily show off my photos in the context of conversations. (I have a repo here, https://github.com/namoopsoo/manage-my-photos related to my glue code.)

But I want a nice photo stream and my food diary is not part of that at all haha. So after manually moving food photos out, ultimately I stumbled upon  Daniel Bourke's Food Not Food repo, https://github.com/mrdbourke/food-not-food . 

This was great I thought but I had some challenges getting this code off the ground, so here are my notes where ultimately I forked this, 
https://github.com/namoopsoo/food-not-food and added a `Dockerfile` to make this easier. Also putting this into docker eventually helped me to batch process photos as well. I can link to a separate post on that as well.


## My stream of consciousness notes!

- 14:02 continue with [[my photo system]] [[import my photos to icloud photos 2022-Oct]]
	- 14:12 I am also using a pytorch repo for photo deduping.
	- 14:22 Ok I took a snapshot `dedupe-requirements-snapshot-2022-11-12.txt` of what I have in my `dedupe` pip environment and looks like actually the #deduping-images library I use , uses #PyTorch and the [[Daniel Bourke Food not Food]] uses #TensorFlow , so likely will not clash .
	- 14:28 ok I cloned the repo and running the `pip install -r requirements.txt`
		- Stumbling on dependency resolution bottlenecks with several packages, `tensorflow-metadata` , `tabulate` , 
		  ```
		  INFO: pip is looking at multiple versions of tabulate to determine which version is compatible with other requirements. This could take a while.
		  
		  ...
		  INFO: This is taking longer than usual. You might need to provide the dependency resolver with stricter constraints to reduce runtime. If you want to abort this run, you can press Ctrl + C to do so. To improve how pip performs, tell us what happened here: https://pip.pypa.io/surveys/backtracking
		  
		  ...
		  INFO: pip is looking at multiple versions of sortedcontainers to determine which version is compatible with other requirements. This could take a while.
		  
		  INFO: pip is looking at multiple versions of tifffile to determine which version is compatible with other requirements. This could take a while.
		  Collecting tifffile>=2019.7.26
		    Downloading tifffile-2022.8.12-py3-none-any.whl (208 kB)
		       |████████████████████████████████| 208 kB 15.6 MB/s 
		  
		    Downloading tifffile-2022.8.8-py3-none-any.whl (208 kB)
		  
		  ```
	- 14:56 yea had to cancel, that wasn't going anywhere .
		- Let me try conda instead, 

		  ```python
		  conda create -n foodnot 
		  conda activate foodnot
		  
		  (foodnot) $ conda install  matplotlib numpy pandas requests scikit-learn tensorflow tflite-model-maker tqdm # fiftyone
		  
		  # Hmm cannot find tflite-model-maker
		  conda install  matplotlib numpy pandas requests scikit-learn tensorflow  tqdm # fiftyone
		  
		  ```
		  Ok well that worked but now since cannot find `tflite-model-maker` with conda, trying with `pip` , 
		  
		  ```
		  pip install tflite-model-maker
		  ```
		  and it is a mess again! Just some kind of hell this installation just looks like a whole lot of this , 
		  
		  ```python
		    Downloading tf_nightly-2.12.0.dev20221104-cp310-cp310-macosx_10_14_x86_64.whl (221.5 MB)
		       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 221.5/221.5 MB 3.3 MB/s eta 0:00:00
		    Downloading tf_nightly-2.12.0.dev20221103-cp310-cp310-macosx_10_14_x86_64.whl (221.5 MB)
		       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 221.5/221.5 MB 7.3 MB/s eta 0:00:00
		    Downloading tf_nightly-2.12.0.dev20221102-cp310-cp310-macosx_10_14_x86_64.whl (221.7 MB)
		       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 221.7/221.7 MB 4.1 MB/s eta 0:00:00
		    Downloading tf_nightly-2.12.0.dev20221101-cp310-cp310-macosx_10_14_x86_64.whl (221.7 MB)
		       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 221.7/221.7 MB 3.4 MB/s eta 0:00:00
		    Downloading tf_nightly-2.12.0.dev20221031-cp310-cp310-macosx_10_14_x86_64.whl (222.4 MB)
		       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 222.4/222.4 MB 3.4 MB/s eta 0:00:00
		    Downloading tf_nightly-2.12.0.dev20221030-cp310-cp310-macosx_10_14_x86_64.whl (222.4 MB)
		  
		  ```
	- 15:21 ok let me try #Docker  .
		- 15:35 ok from , https://www.tensorflow.org/install/docker , 
		  
		  ```
		  (foodnot) $ docker -v 
		  Docker version 20.10.21, build baeda1f
		  (foodnot) $ docker pull tensorflow/tensorflow
		  ...
		  
		  (foodnot) $ docker run -it --rm tensorflow/tensorflow python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
		  2022-11-12 20:37:15.606702: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
		  To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
		  2022-11-12 20:37:17.349502: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
		  To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
		  tf.Tensor(-1153.0294, shape=(), dtype=float32)
		  ```
		- ok cool so now let me try to apply the [[Daniel Bourke Food not Food]] requirements?
		- 15:39 ok let me see from the typical build can I install tflite-model-maker ? 
		  
		  ```sh
		  
		  docker run -it tensorflow/tensorflow bash
		  
		  ________                               _______________                
		  ___  __/__________________________________  ____/__  /________      __
		  __  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
		  _  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ / 
		  /_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/
		  
		  
		  WARNING: You are running this container as root, which can cause new files in
		  mounted volumes to be created as the root user on your host machine.
		  
		  To avoid this, run the container by specifying your user's userid:
		  
		  $ docker run -u $(id -u):$(id -g) args...
		  
		  
		  root@566168cfbe3e:/# which pip
		  /usr/local/bin/pip
		  root@566168cfbe3e:/# pip freeze
		  absl-py==1.2.0
		  astunparse==1.6.3
		  cachetools==5.2.0
		  certifi==2022.6.15
		  charset-normalizer==2.1.1
		  flatbuffers==2.0.7
		  gast==0.4.0
		  google-auth==2.11.0
		  google-auth-oauthlib==0.4.6
		  google-pasta==0.2.0
		  grpcio==1.48.1
		  h5py==3.7.0
		  idna==3.3
		  importlib-metadata==4.12.0
		  keras==2.10.0
		  Keras-Preprocessing==1.1.2
		  libclang==14.0.6
		  Markdown==3.4.1
		  MarkupSafe==2.1.1
		  numpy==1.23.2
		  oauthlib==3.2.0
		  opt-einsum==3.3.0
		  packaging==21.3
		  protobuf==3.19.4
		  pyasn1==0.4.8
		  pyasn1-modules==0.2.8
		  pyparsing==3.0.9
		  requests==2.28.1
		  requests-oauthlib==1.3.1
		  rsa==4.9
		  six==1.16.0
		  tensorboard==2.10.0
		  tensorboard-data-server==0.6.1
		  tensorboard-plugin-wit==1.8.1
		  tensorflow-cpu==2.10.0
		  tensorflow-estimator==2.10.0
		  tensorflow-io-gcs-filesystem==0.26.0
		  termcolor==1.1.0
		  typing-extensions==4.3.0
		  urllib3==1.26.12
		  Werkzeug==2.2.2
		  wrapt==1.14.1
		  zipp==3.8.1
		  root@566168cfbe3e:/# pip install tflite-model-maker
		  Collecting tflite-model-maker
		    Downloading tflite_model_maker-0.4.2-py3-none-any.whl (577 kB)
		       |████████████████████████████████| 577 kB 1.2 MB/s 
		        ... 
		        ... 
		        ... 
		  
		  Successfully built fire promise kaggle audioread
		  Installing collected packages: pillow, PyYAML, packaging, tensorflow-hub, tensorflow, tensorflowjs, typeguard, tensorflow-addons, scann, dm-tree, tensorflow-model-optimization, lxml, kiwisolver, python-dateutil, cycler, matplotlib, llvmlite, numba, importlib-resources, toml, dill, etils, tqdm, googleapis-common-protos, tensorflow-metadata, promise, tensorflow-datasets, opencv-python-headless, Cython, tf-slim, proto-plus, pyarrow, grpcio-status, google-api-core, google-cloud-bigquery-storage, google-cloud-core, google-crc32c, google-resumable-media, google-cloud-bigquery, psutil, py-cpuinfo, httplib2, uritemplate, google-auth-httplib2, google-api-python-client, dataclasses, gin-config, sentencepiece, scipy, text-unidecode, python-slugify, urllib3, kaggle, pytz, pandas, tf-models-official, fire, pycparser, CFFI, sounddevice, pybind11, tflite-support, attrs, neural-structured-learning, appdirs, pooch, joblib, threadpoolctl, scikit-learn, soundfile, resampy, audioread, decorator, librosa, tflite-model-maker
		    Attempting uninstall: packaging
		      Found existing installation: packaging 21.3
		      Uninstalling packaging-21.3:
		        Successfully uninstalled packaging-21.3
		  
		  		 ...
		       ERROR: After October 2020 you may experience errors when installing or updating packages. This is because pip will change the way that it resolves dependency conflicts.
		  
		       We recommend you use --use-feature=2020-resolver to test your packages with the new resolver before it becomes the default.
		  
		       scann 1.2.6 requires tensorflow~=2.8.0, but you'll have tensorflow 2.10.0 which is incompatible.
		       grpcio-status 1.50.0 requires grpcio>=1.50.0, but you'll have grpcio 1.48.1 which is incompatible.
		       grpcio-status 1.50.0 requires protobuf>=4.21.6, but you'll have protobuf 3.19.4 which is incompatible.
		       google-api-core 2.10.2 requires protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.19.5, but you'll have protobuf 3.19.4 which is incompatible.
		       google-cloud-bigquery-storage 2.16.2 requires protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.19.5, but you'll have protobuf 3.19.4 which is incompatible.
		       google-cloud-bigquery 3.3.6 requires protobuf!=3.20.0,!=3.20.1,!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<5.0.0dev,>=3.19.5, but you'll have protobuf 3.19.4 which is incompatible.
		       Successfully installed CFFI-1.15.1 Cython-0.29.32 PyYAML-6.0 appdirs-1.4.4 attrs-22.1.0 audioread-3.0.0 cycler-0.11.0 dataclasses-0.6 decorator-5.1.1 dill-0.3.6 dm-tree-0.1.7 etils-0.9.0 fire-0.4.0 gin-config-0.5.0 google-api-core-2.10.2 google-api-python-client-2.65.0 google-auth-httplib2-0.1.0 google-cloud-bigquery-3.3.6 google-cloud-bigquery-storage-2.16.2 google-cloud-core-2.3.2 google-crc32c-1.5.0 google-resumable-media-2.4.0 googleapis-common-protos-1.56.4 grpcio-status-1.50.0 httplib2-0.21.0 importlib-resources-5.10.0 joblib-1.2.0 kaggle-1.5.12 kiwisolver-1.4.4 librosa-0.8.1 llvmlite-0.36.0 lxml-4.9.1 matplotlib-3.4.3 neural-structured-learning-1.4.0 numba-0.53.0 opencv-python-headless-4.6.0.66 packaging-20.9 pandas-1.5.1 pillow-9.3.0 pooch-1.6.0 promise-2.3 proto-plus-1.22.1 psutil-5.9.4 py-cpuinfo-9.0.0 pyarrow-10.0.0 pybind11-2.10.1 pycparser-2.21 python-dateutil-2.8.2 python-slugify-6.1.2 pytz-2022.6 resampy-0.4.2 scann-1.2.6 scikit-learn-1.1.3 scipy-1.9.3 sentencepiece-0.1.97 sounddevice-0.4.5 soundfile-0.11.0 tensorflow-2.10.0 tensorflow-addons-0.18.0 tensorflow-datasets-4.7.0 tensorflow-hub-0.12.0 tensorflow-metadata-1.11.0 tensorflow-model-optimization-0.7.3 tensorflowjs-3.18.0 text-unidecode-1.3 tf-models-official-2.3.0 tf-slim-1.1.0 tflite-model-maker-0.4.2 tflite-support-0.4.3 threadpoolctl-3.1.0 toml-0.10.2 tqdm-4.64.1 typeguard-2.13.3 uritemplate-4.1.1 urllib3-1.25.11
		       WARNING: You are using pip version 20.2.4; however, version 22.3.1 is available.
		       You should consider upgrading via the '/usr/bin/python3 -m pip install --upgrade pip' command.
		       root@566168cfbe3e:/#  
		  
		  
		  
		  ```
		- 15:47 ok that wasn't terrible.
		- 17:56 So per the initial `pip freeze`, I had `tensorflow-cpu==2.10.0` and when I tried pip installing `tflite-model-maker` and among packages ended up getting installed, includes 
		  ```
		  scikit-learn-1.1.3
		  scipy-1.9.3
		  tensorflow-2.10.0
		  tensorflow-datasets-4.7.0
		  tensorflow-hub-0.12.0
		  tensorflow-metadata-1.11.0
		  tflite-model-maker-0.4.2
		  tflite-support-0.4.3
		  
		  ```
			- but I hope this Docker , if it flipped from `tensorflow-cpu` to `tensorflow` vanilla, will still work.  So when I import `tensorflow` I get more or less a warning but not an error, 
			  ```python
			  In [1]: import tensorflow as tf
			  2022-11-12 23:09:24.366553: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
			  To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
			  2022-11-12 23:09:25.000557: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
			  2022-11-12 23:09:25.000647: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
			  2022-11-12 23:09:25.124265: E tensorflow/stream_executor/cuda/cuda_blas.cc:2981] Unable to register cuBLAS factory: Attempting to register factory for plugin cuBLAS when one has already been registered
			  2022-11-12 23:09:27.457123: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libnvinfer.so.7'; dlerror: libnvinfer.so.7: cannot open shared object file: No such file or directory
			  2022-11-12 23:09:27.457399: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libnvinfer_plugin.so.7'; dlerror: libnvinfer_plugin.so.7: cannot open shared object file: No such file or directory
			  2022-11-12 23:09:27.457462: W tensorflow/compiler/tf2tensorrt/utils/py_utils.cc:38] TF-TRT Warning: Cannot dlopen some TensorRT libraries. If you would like to use Nvidia GPU with TensorRT, please make sure the missing libraries mentioned above are installed properly.
			  
			  
			  ```
			- Ah but too good to be true, so , 
			  ```python
			  from tflite_model_maker import image_classifier
			  
			  ImportError: libusb-1.0.so.0: cannot open shared object file: No such file or directory
			  
			  ```
			- Reading the https://www.tensorflow.org/lite/models/modify/model_maker#installation information here I am not yet sure is #GPU support required or not .
			- Also read on [stackoverflow](https://askubuntu.com/questions/629619/how-to-install-libusb)  
			  ```
			  apt-get install libusb-1.0-0-dev
			  
			  ```
			  seems to have worked.
			- 18:38 ok well, so next time around, that `from tflite_model_maker import image_classifier` did not crash. so full input of mine was , 
			  
			  ```sh
			  docker run -it tensorflow/tensorflow bash
			  ...
			  ```
			  then , 
			  ```sh
			  apt-get install libusb-1.0-0-dev
			  ```
			  Next I tried to install the raw dependencies that got installed last time but that threw a weird error about , 
			  ```sh
			  ERROR: Double requirement given: google==api-python-client-2.65.0 (already in google==api-core-2.10.2, name='google')
			  ```
			  so I ended up upgrading pip, from `20.2.4` because maybe  , `version 22.3.1` was smarter w/ dependencies?
			  ```
			  python3 -m pip install --upgrade pip
			  ```
			  Then I tried to again install the full chain of dependencies but I got an error about python 3.7 , 
			  
			  ```
			  ERROR: Ignored the following versions that require a different python version: 0.7 Requires-Python >=3.6, <3.7; 0.8 Requires-Python >=3.6, <3.7
			  ```
			  so I just went ahead to try `tflite-model-maker` by itself why not 
			  
			  ```
			  pip install tflite-model-maker==0.4.2
			  ```
			  so the `tflite-model-maker` installation took maybe 3 minutes.
			  
			  ```
			  ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
			  tensorflow-cpu 2.10.0 requires keras<2.11,>=2.10.0, but you have keras 2.8.0 which is incompatible.
			  tensorflow-cpu 2.10.0 requires tensorboard<2.11,>=2.10, but you have tensorboard 2.8.0 which is incompatible.
			  tensorflow-cpu 2.10.0 requires tensorflow-estimator<2.11,>=2.10.0, but you have tensorflow-estimator 2.8.0 which is incompatible.
			  Successfully installed CFFI-1.15.1 Cython-0.29.32 PyYAML-6.0 appdirs-1.4.4 attrs-22.1.0 audioread-3.0.0 cycler-0.11.0 dataclasses-0.6 decorator-5.1.1 dill-0.3.6 dm-tree-0.1.7 etils-0.9.0 fire-0.4.0 gin-config-0.5.0 google-api-core-2.10.2 google-api-python-client-2.65.0 google-auth-httplib2-0.1.0 google-cloud-bigquery-3.3.6 google-cloud-bigquery-storage-2.16.2 google-cloud-core-2.3.2 google-crc32c-1.5.0 google-resumable-media-2.4.0 googleapis-common-protos-1.56.4 grpcio-1.50.0 grpcio-status-1.48.2 httplib2-0.21.0 importlib-resources-5.10.0 joblib-1.2.0 kaggle-1.5.12 keras-2.8.0 kiwisolver-1.4.4 librosa-0.8.1 llvmlite-0.36.0 lxml-4.9.1 matplotlib-3.4.3 neural-structured-learning-1.4.0 numba-0.53.0 opencv-python-headless-4.6.0.66 packaging-20.9 pandas-1.5.1 pillow-9.3.0 pooch-1.6.0 promise-2.3 proto-plus-1.22.1 protobuf-3.19.6 psutil-5.9.4 py-cpuinfo-9.0.0 pyarrow-10.0.0 pybind11-2.10.1 pycparser-2.21 python-dateutil-2.8.2 python-slugify-6.1.2 pytz-2022.6 resampy-0.4.2 scann-1.2.6 scikit-learn-1.1.3 scipy-1.9.3 sentencepiece-0.1.97 sounddevice-0.4.5 soundfile-0.11.0 tensorboard-2.8.0 tensorflow-2.8.3 tensorflow-addons-0.18.0 tensorflow-datasets-4.7.0 tensorflow-estimator-2.8.0 tensorflow-hub-0.12.0 tensorflow-metadata-1.11.0 tensorflow-model-optimization-0.7.3 tensorflowjs-3.18.0 text-unidecode-1.3 tf-models-official-2.3.0 tf-slim-1.1.0 tflite-model-maker-0.4.2 tflite-support-0.4.3 threadpoolctl-3.1.0 toml-0.10.2 tqdm-4.64.1 typeguard-2.13.3 uritemplate-4.1.1 urllib3-1.25.11
			  ```
			- 18:59 ok let me try to run docker now w/ a shared directory , with a `Dockerfile` , summarizing the above, and I am using  from what I can tell, this version but somehow I do not see it on https://hub.docker.com/r/tensorflow/tensorflow/ ,  #Docker-hub 
			  
			  ```
			  tensorflow/tensorflow   latest    976c17ec6daa   2 months ago    1.46GB
			  ```
			  
			  ```
			  FROM tensorflow/tensorflow:latest 
			  
			  RUN apt-get install -y libusb-1.0-0-dev
			  
			  RUN python3 -m pip install --upgrade pip
			  
			  RUN pip install tflite-model-maker==0.4.2
			  
			  RUN pip install ipython
			  
			  ```
			  create an image, 
			  ```sh
			  docker build -t food-not-food -f hmm-docker/Dockerfile hmm-docker 
			  
			  [+] Building 259.2s (9/9) FINISHED                                                                                           
			   => [internal] load build definition from Dockerfile                                                                    0.2s
			   => => transferring dockerfile: 228B                                                                                    0.1s
			   => [internal] load .dockerignore                                                                                       0.1s
			   => => transferring context: 2B                                                                                         0.1s
			   => [internal] load metadata for docker.io/tensorflow/tensorflow:latest                                                 0.0s
			   => [1/5] FROM docker.io/tensorflow/tensorflow                                                                          0.1s
			   => [2/5] RUN apt-get install -y libusb-1.0-0-dev                                                                       3.9s
			   => [3/5] RUN python3 -m pip install --upgrade pip                                                                      3.7s
			   => [4/5] RUN pip install tflite-model-maker==0.4.2                                                                   219.6s 
			   => [5/5] RUN pip install ipython                                                                                       8.4s 
			   => exporting to image                                                                                                 23.5s 
			   => => exporting layers                                                                                                23.4s 
			   => => writing image sha256:dc8e469de66a5e8e9d91b4fc971a7cc9ff8ba9f2ed04e395e182e472a237c526                            0.1s 
			   => => naming to docker.io/library/food-not-food                                                                        0.0s 
			                                                                                                                 
			  ```
			  And run it , per my handy notes , https://github.com/namoopsoo/handy/blob/master/Docker/hmm.md 
			  
			  ```sh
			  cd ~/Dropbox/Code/repo/food-not-food
			  docker run -i -t -v $(pwd):/home \
			      -v ~/Dropbox/Code/repo/data/101_food_classes_all_data:/mnt/101_food_classes_all_data \
			      food-not-food
			   
			  # docker run -it tensorflow/tensorflow bash
			  
			  ```
			-
		- 18:19 Since the installation basically worked in Docker at least,
		- 17:50 so let me see, can I run the model training script ?
	- Next downloading the data ok , 
	  
	  ```python
	  /Users/michal/Dropbox/Code/repo/food-not-food
	  (dedupe) (base) $ python data_download/download_food101.py
	  101_food_classes_all_data.zip: 100%|█████████████████████| 4.67G/4.67G [06:07<00:00, 13.6MiB/s]
	  [INFO] Food101 downloaded, unzipping...
	  
	  ```
	- 20:04 So I kind of lazily ended up doing this 
	  ```python
	  
	  In [2]: from pathlib import Path
	     ...: from datetime import date
	     ...: from tflite_model_maker import image_classifier
	     ...: from tflite_model_maker.image_classifier import DataLoader
	     ...: 
	  
	  In [3]: train_data_path = "/mnt/101_food_classes_all_data/train/apple_pie"
	  
	  In [4]: test_data_path = "/mnt/101_food_classes_all_data/test/apple_pie"
	  
	  In [5]: train_data = DataLoader.from_folder(train_data_path)
	     ...: test_data = DataLoader.from_folder(test_data_path)
	     ...: 
	  ---------------------------------------------------------------------------
	  ValueError                                Traceback (most recent call last)
	  Cell In [5], line 1
	  ----> 1 train_data = DataLoader.from_folder(train_data_path)
	        2 test_data = DataLoader.from_folder(test_data_path)
	  
	  File /usr/local/lib/python3.8/dist-packages/tensorflow_examples/lite/model_maker/core/data_util/image_dataloader.py:73, in ImageClassifierDataLoader.from_folder(cls, filename, shuffle)
	       71 all_image_size = len(all_image_paths)
	       72 if all_image_size == 0:
	  ---> 73   raise ValueError('Image size is zero')
	       75 if shuffle:
	       76   # Random shuffle data.
	       77   random.shuffle(all_image_paths)
	  
	  ValueError: Image size is zero
	  ```
	  and I think the error was because a certain directory structure is expected. 
	  
	  So I did this. 
	  
	  ```sh
	  (base) $ cp  ../data/101_food_classes_all_data/train/apple_pie/* ../data/101_food_classes_all_data/small/train/apple_pie
	  (base) $ du -d 0 -h ../data/101_food_classes_all_data/small/train/apple_pie
	   36M	../data/101_food_classes_all_data/small/train/apple_pie
	  (base) $ cp  ../data/101_food_classes_all_data/test/apple_pie/* ../data/101_food_classes_all_data/small/test/apple_pie/
	  (base) $ 
	  (base) $ cp  ../data/101_food_classes_all_data/test/churros/* ../data/101_food_classes_all_data/small/test/not_apple_pie/
	  (base) $ cp  ../data/101_food_classes_all_data/train/churros/* ../data/101_food_classes_all_data/small/train/not_apple_pie/
	  (base) $ 
	  ```
	- 20:06 ok does that help?
	  
	  ```python
	  train_data_path = "/mnt/101_food_classes_all_data/small/train"
	  test_data_path = "/mnt/101_food_classes_all_data/small/test"
	  train_data = DataLoader.from_folder(train_data_path)
	  test_data = DataLoader.from_folder(test_data_path)
	  
	  2022-11-13 01:08:49.543996: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcuda.so.1'; dlerror: libcuda.so.1: cannot open shared object file: No such file or directory
	  2022-11-13 01:08:49.545031: W tensorflow/stream_executor/cuda/cuda_driver.cc:269] failed call to cuInit: UNKNOWN ERROR (303)
	  2022-11-13 01:08:49.546377: I tensorflow/stream_executor/cuda/cuda_diagnostics.cc:156] kernel driver does not appear to be running on this host (a4d9f933dc4f): /proc/driver/nvidia/version does not exist
	  2022-11-13 01:08:49.561325: I tensorflow/core/platform/cpu_feature_guard.cc:151] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 FMA
	  To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
	  INFO:tensorflow:Load image with size: 1500, num_label: 2, labels: apple_pie, not_apple_pie.
	  INFO:tensorflow:Load image with size: 500, num_label: 2, labels: apple_pie, not_apple_pie.
	  
	  
	  ```
	- ok so that was the correct folder structure cool, but hopefully the other #GPU cuda errors don't hold me back. Let's find out
	- 20:10 ok, 
	  
	  ```python
	  NUM_EPOCHS = 1
	  MODEL_SPEC = "efficientnet_lite0"
	  # Create model
	  print(f"[INFO] Creating and training model...")
	  print(f"[INFO] Training {MODEL_SPEC} for {NUM_EPOCHS} epochs...")
	  model = image_classifier.create(
	      train_data=train_data,
	      model_spec=MODEL_SPEC,
	      epochs=NUM_EPOCHS,
	      use_augmentation=True,
	  )
	  
	  [INFO] Creating and training model...
	  [INFO] Training efficientnet_lite0 for 1 epochs...
	  INFO:tensorflow:Retraining the models...
	  Model: "sequential"
	  _________________________________________________________________
	   Layer (type)                Output Shape              Param #   
	  =================================================================
	   hub_keras_layer_v1v2 (HubKe  (None, 1280)             3413024   
	   rasLayerV1V2)                                                   
	                                                                   
	   dropout (Dropout)           (None, 1280)              0         
	                                                                   
	   dense (Dense)               (None, 2)                 2562      
	                                                                   
	  =================================================================
	  Total params: 3,415,586
	  Trainable params: 2,562
	  Non-trainable params: 3,413,024
	  _________________________________________________________________
	  None
	  INFO:tensorflow:Use default resize_bicubic.
	  INFO:tensorflow:Use default resize_bicubic.
	  INFO:tensorflow:Use customized resize method bilinear
	  INFO:tensorflow:Use customized resize method bilinear
	  2022-11-13 01:12:34.077741: W tensorflow/core/framework/cpu_allocator_impl.cc:82] Allocation of 19267584 exceeds 10% of free system memory.
	  2022-11-13 01:12:34.350836: W tensorflow/core/framework/cpu_allocator_impl.cc:82] Allocation of 19267584 exceeds 10% of free system memory.
	  2022-11-13 01:12:34.357610: W tensorflow/core/framework/cpu_allocator_impl.cc:82] Allocation of 51380224 exceeds 10% of free system memory.
	  2022-11-13 01:12:34.718472: W tensorflow/core/framework/cpu_allocator_impl.cc:82] Allocation of 19267584 exceeds 10% of free system memory.
	  2022-11-13 01:12:34.887098: W tensorflow/core/framework/cpu_allocator_impl.cc:82] Allocation of 51380224 exceeds 10% of free system memory.
	  46/46 [==============================] - 48s 963ms/step - loss: 0.4440 - accuracy: 0.8274
	  
	  
	  ```
	- ok wow that did something without crashing. nice. Will the testing work?
	  ```python
	  test_loss, test_accuracy = model.evaluate(test_data)
	  
	  INFO:tensorflow:Use customized resize method bilinear
	  INFO:tensorflow:Use customized resize method bilinear
	  16/16 [==============================] - 22s 1s/step - loss: 0.3070 - accuracy: 0.9540
	  ```
	- 22:22 ok and let's see how do I run this on unlabeled data then ? 
	  
	  ```python
	  from datetime import date
	  
	  current_date = str(date.today())
	  model_number = 1
	  export_dir = "/home/models"
	  model_save_path = (
	      Path(export_dir) 
	      / f"{current_date}_apple_pie_or_churro_model_{MODEL_SPEC}_v{model_number}.tflite")
	  
	  print(f"[INFO] Saving the model to '{export_dir}' directory as '{model_save_path}'...")
	  model.export(export_dir=export_dir, tflite_filename=model_save_path)
	  print(f"[INFO] Model saved to: '{model_save_path}'.")
	  
	  ```
	  Ok that took a minute or two
	  ```
	  [INFO] Saving the model to '/home/models' directory as '/home/models/2022-11-13_apple_pie_or_churro_model_efficientnet_lite0_v1.tflite'...
	  INFO:tensorflow:Use customized resize method bilinear
	  INFO:tensorflow:Use customized resize method bilinear
	  2022-11-13 03:37:29.984575: W tensorflow/python/util/util.cc:368] Sets are not currently considered sequences, but this may change in the future, so consider avoiding using them.
	  INFO:tensorflow:Assets written to: /tmp/tmpodz47y2g/assets
	  INFO:tensorflow:Assets written to: /tmp/tmpodz47y2g/assets
	  2022-11-13 03:37:35.785772: I tensorflow/core/grappler/devices.cc:66] Number of eligible GPUs (core count >= 8, compute capability >= 0.0): 0
	  2022-11-13 03:37:35.787503: I tensorflow/core/grappler/clusters/single_machine.cc:358] Starting new session
	  2022-11-13 03:37:35.864717: I tensorflow/core/grappler/optimizers/meta_optimizer.cc:1164] Optimization results for grappler item: graph_to_optimize
	    function_optimizer: Graph size after: 913 nodes (656), 923 edges (664), time = 35.413ms.
	    function_optimizer: function_optimizer did nothing. time = 0.888ms.
	  
	  /usr/local/lib/python3.8/dist-packages/tensorflow/lite/python/convert.py:746: UserWarning: Statistics for quantized inputs were expected, but not specified; continuing anyway.
	    warnings.warn("Statistics for quantized inputs were expected, but not "
	  2022-11-13 03:37:37.252870: W tensorflow/compiler/mlir/lite/python/tf_tfl_flatbuffer_helpers.cc:357] Ignored output_format.
	  2022-11-13 03:37:37.253120: W tensorflow/compiler/mlir/lite/python/tf_tfl_flatbuffer_helpers.cc:360] Ignored drop_control_dependency.
	  
	  fully_quantize: 0, inference_type: 6, input_inference_type: 3, output_inference_type: 3
	  INFO:tensorflow:Label file is inside the TFLite model with metadata.
	  INFO:tensorflow:Label file is inside the TFLite model with metadata.
	  INFO:tensorflow:Saving labels in /tmp/tmpmy_t1d99/labels.txt
	  INFO:tensorflow:Saving labels in /tmp/tmpmy_t1d99/labels.txt
	  INFO:tensorflow:TensorFlow Lite model exported successfully: /home/models/2022-11-13_apple_pie_or_churro_model_efficientnet_lite0_v1.tflite
	  INFO:tensorflow:TensorFlow Lite model exported successfully: /home/models/2022-11-13_apple_pie_or_churro_model_efficientnet_lite0_v1.tflite
	  [INFO] Model saved to: '/home/models/2022-11-13_apple_pie_or_churro_model_efficientnet_lite0_v1.tflite'.
	  
	  ```
	  And reading on here, https://www.tensorflow.org/lite/models/modify/model_maker/image_classification that you can also evaluate data like , 
	  ```python
	  model.evaluate_tflite('model.tflite', test_data)
	  ```
	  but yea still looking for how do I create unlabeled dataset?
	- Also reading on https://www.tensorflow.org/lite/api_docs/python/tflite_model_maker/image_classifier/DataLoader that the data passed in to `DataLoader` can also be a `tf.data.Dataset` , 
	  
	  ```python
	  tflite_model_maker.image_classifier.DataLoader(
	      dataset, size, index_to_label
	  )
	  
	  ```
	- 23:03 also reading on https://www.tensorflow.org/lite/api_docs/python/tf/lite/Interpreter here that not only can you convert a regular tensorflow model to the tensorflow lite format you also need to  allocate tensors before using it, 
	  
	  ```python
	  interpreter = tf.lite.Interpreter(model_content=tflite_model)
	  interpreter.allocate_tensors()  # Needed before execution!
	  
	  ```
	- lets try whatever, 
	  ```python
	  unlabeled_data_path = "/mnt/101_food_classes_all_data/small/unlabeled/"
	  unlabeled_data = DataLoader.from_folder(unlabeled_data_path)
	  
	  ```

