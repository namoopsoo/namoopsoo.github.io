---
title: Does the Wahoo TIKR measure intervals that can be used for Heart Rate Variability measurements?
date: 2020-06-06
---


Not sure yet. There are a fitness trackers out there, but I am curious if my chest band can help. I took a quick look at one of my recordings on the Wahoo app, but I don't see anything more granular than just beats per minute. The app indeed has  pushed to Apple Health, but I only see the bpm data and no HRV data.


{{< row >}}
{{< column >}}
 {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.42.png" width="30%" >}}
{{< /column >}}

{{< column >}}
 {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.49.png" width="30%" >}}
{{< /column >}}

{{< column >}}
 {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.44.39.png" width="30%" >}} 
{{< /column >}}
{{< /row >}}


<table>
<tr>
<td> {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.42.png" width="30%" >}} </td>
<td> {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.49.png" width="30%" >}} </td>
<td> {{< figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.44.39.png" width="30%" >}} </td>
</tr>
</table>

#### Didnt finish this but I tried parsing the raw fit file
* Making a note for later I suppose. I git cloned [fit_processing](https://github.com/mcandocia/fit_processing) , which requires installing [fitparse](https://github.com/dtcooper/python-fitparse)
* But when I ran

```
python3 process_all.py --subject-name=mysubjectname --fit-source-dir=/media/myname/GARMIN/Garmin/ACTIVITY/
```
* I got

```
doing FIT conversions
activity files:  ['2020-02-06-160620-FITNESS 3A6A-20-0.fit']
new names:  ['2020-02-06-160620-FITNESS 3A6A-20-0.fit']
current_files:  {'2020-02-06-160620-FITNESS 3A6A-20-0.fit'}
2020-02-06-160620-FITNESS 3A6A-20-0.fit already exists...
converting ....../fit_files/2020-02-06-160620-FITNESS 3A6A-20-0.fit
...
  File "/...../fit_processing/process_all.py", line 1, in <module>
    import os
...
  File "/usr/local/miniconda3/envs/pandars3/lib/python3.7/site-packages/fitparse/records.py", line 450, in add_dev_field_description
    field_def_num = message.get('field_definition_number').raw_value
AttributeError: 'NoneType' object has no attribute 'raw_value'

```
* And I got the same result when trying the raw [docs here](http://dtcooper.github.io/python-fitparse/#api-documentation) for `fitparse` itself. To be fair those docs appear to be python2.7 docs.
* Of course also possible that not all `.fit` files, Wahoo or Garmin, have the same kinds of data. Maybe `fitparse` was tested only on Garmin `.fit` files?
