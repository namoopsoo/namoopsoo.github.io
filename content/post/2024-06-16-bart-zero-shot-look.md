---
title: Let's try BART zero shot on restaurant related queries 
date: 2024-06-16
---


[[_TOC_]]

## Let's look at what bart-large-mnli has to say on restaurant related labels for food and non food queries
The queries here are just arbitrary statements I came up with off the top of my head. 


You can [skip to the final scoring](#final-evaluation), but in summary, using a super simplistic evaluation here, I think that the super accessible `bart-large-mnli` model does pretty well here.

One observation I am seeing casually, which I believe Jake Tae https://jaketae.github.io/study/zero-shot-classification/ refers too also, is that `bart-large-mnli` is more or less by design, not as helpful w.r.t. single-word hypothesis entailment. And that's why, inspired by Jake and the underlying work being discussed [here](https://joeddav.github.io/blog/2020/05/29/ZSL.html), below, I'm also using mostly multi-word (multi-token) hypotheses as topics.


## mini func, check if a query is on topic or off topic , first


```python
from transformers import pipeline, BertTokenizer, BertModel
import torch

# Load Hugging Face pipeline for zero-shot classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def check_if_on_topic(query, topics):
    
    classification = classifier(query, topics, multi_label=True)
    return classification



queries = [
    "I'm looking for good wings near me",
    "What is a good chicken wings place near me?",
    "Are there any good pasta places around here?",
    "What is a good italian place nearby?",
    "What is a decent burger spot here?",
    "Are there some decent fast food spots nearby?",
    "What is a good noodle place in town?",
]
topics = [
    "this is about food",
    "food",
    "this is about a restaurant",
    "restaurants",
    "food places",
    "this is about food places",
]
for query in queries:
    classification = check_if_on_topic(query, topics)
    print("")
    print("query", query)
    print(classification)

```

    
    query I'm looking for good wings near me
    {'sequence': "I'm looking for good wings near me", 'labels': ['food places', 'this is about food places', 'this is about food', 'this is about a restaurant', 'food', 'restaurants'], 'scores': [0.9868150949478149, 0.984097421169281, 0.9606814384460449, 0.8281988501548767, 0.7463715672492981, 0.5991970300674438]}
    
    query What is a good chicken wings place near me?
    {'sequence': 'What is a good chicken wings place near me?', 'labels': ['food', 'food places', 'this is about food', 'this is about food places', 'this is about a restaurant', 'restaurants'], 'scores': [0.9929962158203125, 0.9925386309623718, 0.991735577583313, 0.9857849478721619, 0.9375878572463989, 0.9168540835380554]}
    
    query Are there any good pasta places around here?
    {'sequence': 'Are there any good pasta places around here?', 'labels': ['food places', 'this is about food', 'food', 'this is about food places', 'this is about a restaurant', 'restaurants'], 'scores': [0.9887880682945251, 0.9881364703178406, 0.9875245690345764, 0.9853124618530273, 0.81657475233078, 0.695604681968689]}
    
    query What is a good italian place nearby?
    {'sequence': 'What is a good italian place nearby?', 'labels': ['this is about food', 'food places', 'this is about food places', 'food', 'this is about a restaurant', 'restaurants'], 'scores': [0.9897514581680298, 0.9895842671394348, 0.9839956760406494, 0.9764175415039062, 0.9479529857635498, 0.9041155576705933]}
    
    query What is a decent burger spot here?
    {'sequence': 'What is a decent burger spot here?', 'labels': ['food places', 'food', 'this is about food', 'this is about food places', 'this is about a restaurant', 'restaurants'], 'scores': [0.9959198236465454, 0.9925549626350403, 0.9921599626541138, 0.9869840741157532, 0.8683270812034607, 0.7085756063461304]}
    
    query Are there some decent fast food spots nearby?
    {'sequence': 'Are there some decent fast food spots nearby?', 'labels': ['this is about food', 'food places', 'this is about food places', 'food', 'restaurants', 'this is about a restaurant'], 'scores': [0.97259920835495, 0.9641566276550293, 0.9544232487678528, 0.9524098634719849, 0.5524296164512634, 0.06884073466062546]}
    
    query What is a good noodle place in town?
    {'sequence': 'What is a good noodle place in town?', 'labels': ['this is about food', 'food places', 'this is about food places', 'food', 'this is about a restaurant', 'restaurants'], 'scores': [0.9946930408477783, 0.9917978048324585, 0.9895104169845581, 0.9882515668869019, 0.8941181302070618, 0.696493923664093]}


Ok wow, kind of like I recall reading about Zero Shot learning recently, using BART , seems the one-word MNLI use is not so great, also for this super limited example here.


Let's mix in also some counter cases too? 


```python
sum(classification["scores"])
```




    5.554864883422852




```python


queries = [
    ["I'm looking for good wings near me", 1],
    ["What is a good chicken wings place near me?", 1],
    ["Are there any good pasta places around here?", 1],
    ["What is a good italian place nearby?", 1],
    ["What is a decent burger spot here?", 1],
    ["Are there some decent fast food spots nearby?", 1],
    ["What is a good noodle place in town?", 1],
    ["I am looking for medical help", 0],
    ["I want to learn about painting", 0],
    ["Where is a good place to do my taxes?", 0],
    ["I want to go somewhere and play soccer.", 0],
    ["Where is a good public school for my kids?", 0],
    ["What are good movies to see these days?", 0],
    ["Any good bowling alleys nearby?", 0],
    ["What is a good activity as a tourist to do some sight seeing maybe?", 0],
    ["I am looking for a good museum for art history", 0],
    ["I am hungry where can I go? Hungry for japanese food.", 1],
    ["I want to eat some yummy tacoes with a small group of people. ", 1],
    ["Ok any chicken wings places in the area?", 1],
    ["What is a good meat place like for smoked meat?", 1],
    ["I am in the mood for some ramen, any nearby?", 1],
]
topics = [
    "this is about food",
    "food",
    "this is about a restaurant",
    "restaurants",
    "food places",
    "this is about food places",
]

scores = []

len_food_topics = len(topics)
for query, food_true in queries:
    classification = check_if_on_topic(query, topics)

    food_pred = sum(classification["scores"]) / len_food_topics
    scores.append([query, food_pred, food_true, abs(food_true - food_pred)])

sorted(scores, key=lambda x:x[-1])



```




    [['I am looking for medical help',
      8.088221087139875e-05,
      0,
      8.088221087139875e-05],
     ['I am looking for a good museum for art history',
      9.62637289679454e-05,
      0,
      9.62637289679454e-05],
     ['I want to learn about painting',
      0.00011275537811646548,
      0,
      0.00011275537811646548],
     ['I want to go somewhere and play soccer.',
      0.00011537025845124542,
      0,
      0.00011537025845124542],
     ['Where is a good place to do my taxes?',
      0.00014225074361699322,
      0,
      0.00014225074361699322],
     ['Any good bowling alleys nearby?',
      0.0001614166055029879,
      0,
      0.0001614166055029879],
     ['Where is a good public school for my kids?',
      0.00023048519263587272,
      0,
      0.00023048519263587272],
     ['What is a good activity as a tourist to do some sight seeing maybe?',
      0.0002453784157599633,
      0,
      0.0002453784157599633],
     ['What are good movies to see these days?',
      0.0025914414545695763,
      0,
      0.0025914414545695763],
     ['What is a good chicken wings place near me?',
      0.9695828855037689,
      1,
      0.03041711449623108],
     ['What is a good italian place nearby?',
      0.9653029143810272,
      1,
      0.03469708561897278],
     ['What is a good noodle place in town?',
      0.9258108139038086,
      1,
      0.0741891860961914],
     ['What is a decent burger spot here?',
      0.9240869184335073,
      1,
      0.07591308156649268],
     ['Are there any good pasta places around here?',
      0.9103235006332397,
      1,
      0.08967649936676025],
     ['Ok any chicken wings places in the area?',
      0.9090869526068369,
      1,
      0.09091304739316308],
     ['I am hungry where can I go? Hungry for japanese food.',
      0.9055028756459554,
      1,
      0.09449712435404456],
     ["I'm looking for good wings near me",
      0.8508935670057932,
      1,
      0.14910643299420678],
     ['I am in the mood for some ramen, any nearby?',
      0.848459447423617,
      1,
      0.151540552576383],
     ['Are there some decent fast food spots nearby?',
      0.7441432165602843,
      1,
      0.25585678343971574],
     ['I want to eat some yummy tacoes with a small group of people. ',
      0.7101784072195491,
      1,
      0.28982159278045094],
     ['What is a good meat place like for smoked meat?',
      0.6372983492910862,
      1,
      0.3627016507089138]]


## Final evaluation

```python
for row in sorted(scores, key=lambda x:x[-1]):
    print(f"{row[0]}: delta: {row[-1]:.2f} (actual: {row[1]:.2f}, true: {row[2]:.2f})")

```

    I am looking for medical help: delta: 0.00 (actual: 0.00, true: 0.00)
    I am looking for a good museum for art history: delta: 0.00 (actual: 0.00, true: 0.00)
    I want to learn about painting: delta: 0.00 (actual: 0.00, true: 0.00)
    I want to go somewhere and play soccer.: delta: 0.00 (actual: 0.00, true: 0.00)
    Where is a good place to do my taxes?: delta: 0.00 (actual: 0.00, true: 0.00)
    Any good bowling alleys nearby?: delta: 0.00 (actual: 0.00, true: 0.00)
    Where is a good public school for my kids?: delta: 0.00 (actual: 0.00, true: 0.00)
    What is a good activity as a tourist to do some sight seeing maybe?: delta: 0.00 (actual: 0.00, true: 0.00)
    What are good movies to see these days?: delta: 0.00 (actual: 0.00, true: 0.00)
    What is a good chicken wings place near me?: delta: 0.03 (actual: 0.97, true: 1.00)
    What is a good italian place nearby?: delta: 0.03 (actual: 0.97, true: 1.00)
    What is a good noodle place in town?: delta: 0.07 (actual: 0.93, true: 1.00)
    What is a decent burger spot here?: delta: 0.08 (actual: 0.92, true: 1.00)
    Are there any good pasta places around here?: delta: 0.09 (actual: 0.91, true: 1.00)
    Ok any chicken wings places in the area?: delta: 0.09 (actual: 0.91, true: 1.00)
    I am hungry where can I go? Hungry for japanese food.: delta: 0.09 (actual: 0.91, true: 1.00)
    I'm looking for good wings near me: delta: 0.15 (actual: 0.85, true: 1.00)
    I am in the mood for some ramen, any nearby?: delta: 0.15 (actual: 0.85, true: 1.00)
    Are there some decent fast food spots nearby?: delta: 0.26 (actual: 0.74, true: 1.00)
    I want to eat some yummy tacoes with a small group of people. : delta: 0.29 (actual: 0.71, true: 1.00)
    What is a good meat place like for smoked meat?: delta: 0.36 (actual: 0.64, true: 1.00)


## ok that is not that bad 
maybe should look at more data, but that's looking pretty decent for a first stab with how well BART is doing here 


```python

```

