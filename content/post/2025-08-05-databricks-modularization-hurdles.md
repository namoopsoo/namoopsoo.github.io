---
date: 2025-08-05
title: python path to Databricks modules
---

This year, and last, Ive been glad Databricks changed one simple thing that has nothing to do with fancy ML algorithms or distributed computing optimization, and thats the ability to interact with workspace files on the python level. 

Prior to Databricks 11.3 , the workspace could only contain notebooks and folders but no plain files. If you used python to do 

```python
import os
os.getcwd()
```

you would see `/databricks/driver` and you could just use this cluster file system to copy files from outside blob systems for python file processing like say to read some csv into pandas and convert that to a spark dataframe but there was no notion of interacting with the actual file system where your notebooks lived (aka the workspace). 

So with databricks 11.2 onward, that all changed, you could now run your `os.getcwd()` , and if you were editing a notebook, say, `/Workspace/foo/bar/my_feature_selection`, you would get `/Workspace/foo/bar`

and you could now all of a sudden create tiny modules in your workspace, say, 
`/Workspace/foo/bar/my_module/__init__.py`, 

and in your notebook, `from my_module.hello import friend`, and run `friend.hack()`. 

Now you could finally do in the databricks Notebook Driven Development world what you could always do in your jupyter notebook on your laptop.

Sure prior you  had the ability to `pip install /dbfs/path/to/some.whl`, which was great too, but with native files, you can write modular code faster without extra steps of externally writing and building and uploading your `some.whl`.

# Enter python path

So the above is all well and good but what if you want a super simple thing like, 

```
# notebook stuff
/Workspace/foo/bar/notebooks
/Workspace/foo/bar/notebooks/training/my_feature_selection

# module stuff
/Workspace/foo/bar/my_module/hello/friend.py

```
well now in your notebook you need  a special line

```python
import sys
sys.path.insert(0, "/Workspace/foo/bar/"
```

so that your python `my_feature_selection` notebook can see your module `my_module` and be able to import it.
 
Thats your python path.


In a recent project, I was running into this interesting conundrum, where I had a set of two notebooks, which both had a pandas udf `call_model` function defined inline, for calling a model , on a spark feature dataframe. and to add  append its output predictions to the dataframe. 

I was in the process of updating `call_model`, because I converted the scikit-learn model with skl2onnx to onnx, for better model portability. But at the same time, as a good boyscout 😆, I was interested in reducing the copy pasta so I put the `call_model` into a module, so it can be imported by the two notebooks using it.

My new code ran swimmingly interactively, except that within a databricks job, interestingly, I was getting a `ModuleNotFound` error for the module I was importing.

The reason was subtle. One of the notebooks was actually using multithreading and when the spark driver distributes work to its workers, it will often serialize the pandas udf in cases like this with cloudpickle, and I have found in my case, the worker is okay with the namespace , however, when multithreading, somehow my sys.path update from earlier was not propagated.  

To  address the above, I found, if I packaged my module into a .whl and `pip install` -ed it on my init script for my cluster, the problem went away of course. And also, I realized one night as I was falling asleep, if I made my code generic enough perhaps it would make sense to include it in a generic package that is installed everywhere on all clusters.

As I'm writing this Im also literally having an epiphany that 😅, since Databricks does also add a default root of the git repository for the code in question, to the python path here, and maybe if I just stuff my module there, perhaps that would be the path if least resistance?! 

Let me try that next 😀.

### Update per above: yes leverage default databricks sys.path
Oh wow haha, the above final idea is what worked and what I switched to. Silly that the simplest solution was hiding in plain sight all along.
