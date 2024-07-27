---
date: 2024-07-20
title: Streamlit is lit
---

Briefly describing this Streamlit fronted python app that queries against menus pulled from a kaggle uber eats dataset found [here](https://www.kaggle.com/code/sadeghjalalian/uber-eats-restaurant-menus/input?select=restaurants.csv).



{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117060822_0.png" width="80%">}}

## First query something random

{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722119433724_0.png" width="50%">}}
It is off topic, so no results 

{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117019959_0.png" width="80%">}}

Basically, continuing from an earlier post, this is taking advantage of Facebook's BART model. Hits against six food and restaurant related topics are averaged and compared against a threshold of `0.60` to determine if the query is food related.

## Now an on-topic query, 


{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117613051_0.png" width="80%">}}
How about a query about chicken parmesan, which is a dish, so should be on topic. 


{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117136810_0.png" width="80%">}}

And so the next part of the app is therefore run, which is to do a lookup against the local postgreql pgvector vector store, in this case using cohere embeddings.


## We note at the bottom it says `no location tokens found`
{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117464863_0.png" width="80%">}}
This is because we have triggered the last step, where we we a second hugging face pipeline, to query the entire input against `"dbmdz/bert-large-cased-finetuned-conll03-english"`, which is a name entity recognition model.


If we try a query now that uses location information, that final result looks different.
{{< figure src="https://s3.amazonaws.com/my-blog-content/2024-07-20-streamlit-is-lit/image_1722117633829_0.png" width="80%">}}






{{< vimeoiframe "https://player.vimeo.com/video/988119356?h=dd2ba0d13c" >}}


