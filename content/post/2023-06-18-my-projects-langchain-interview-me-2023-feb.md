---
date: 2023-02-18
title: langchain interview me 2023 feb
---
type:: #project-type
status:: #in-progress-status
blogDate:: 2023-02-18


## Note
This is not a blog post but kind of a landing page I'm using to aggregate on-going project notes here

## Vision
Broadly would like to do here something like the following
### compare against arbitrary #job-listings , #job-description ,
collapsed:: true
And [[my projects/personal/langchain-interview-me-2023-feb]] , also now the repo usable by anyone who wants to compare their #brag-document to #job-listings [[job-description]] out there , get a delta , and more broadly , understand say , their industry posture , since that’s a moving target . And you can interview yourself too haha .

I can use the [[my projects/personal/langchain-interview-me-2023-feb]] stuff concepts to see , what roles online do I align with and am I progressing towards them at #Humana or stagnating?

### Making updating your #brag-document like a #fun-factor #[[having fun]] experience 😀
### And original intent was a UI to actually ask questions
### Also better #TellMeAboutYourself , #[[tell a story]] . Since the #brag-document has lots of cool stories, and also #chronological-story , this could be a cool way to weave together the personal story.
collapsed:: true
And for [[my projects/personal/langchain-interview-me-2023-feb]] thing, so I was in this [[May 28th, 2023]] too. Would be cool to make it easier for an individual to construct their [[TellMeAboutYourself]] since this is so important and at least to myself cannot rely on my memory haha

### Getting feedback about your text corpus of your experience
Maybe the documents out there can help inform you, of other relevant terms that you forgot to discuss.
Also maybe there is low-information density in your corpus. Take out the stop words haha.


## my blog posts
### initial post with the #question-answer-task
20:55 So I have the #blog-post from [[Feb 18th, 2023]] [here](https://michal.piekarczyk.xyz/post/2023-02-18-first-stab-langchain-interview-me/), where I put together my technical background , create embeddings from them and run a #question-answer-task #langchain , with one of the chains called "load_qa_with_sources_chain" that gives intermediate source text results too.

### Also this one
collapsed:: true
[[blogpost/2023-06-25-everybody-loves-reynauds]] https://michal.piekarczyk.xyz/post/2023-06-25-everybody-loves-reynauds with a comparison across a few embedding models, to suss out which of them do or do not have medical vocabulary
### Also  applying sentence transformers to code search
[part one](https://michal.piekarczyk.xyz/post/2023-06-11-semantic-code-search-first-stab/) and [part two](https://michal.piekarczyk.xyz/post/2023-06-13-semantic-code-search-part-2/)
## research
### went through that [[article/Getting Started With Embeddings]] , which was useful to start learning about #sentence-transformers library
collapsed:: true
And more recently, I went through the #[[hugging face]] example around #Medicare and with the #article-type ,  [[article/Getting Started With Embeddings]] , [link](https://huggingface.co/blog/getting-started-with-embeddings),

And used the  "langchainz" virtual env I have, and I used the https://api-inference.huggingface.co REST API specifying to use the "sentence-transformers/all-MiniLM-L6-v2" model to produce embeddings , and then the   #sentence-transformers library,  `semantic_search` , ( `from sentence_transformers.util import semantic_search` ) , to a question to a set of frequently asked questions
### I have this question, is the #sentence-transformers #average-pooling noisy?
### Can I use better #NER [[Named Entity Recognition NER]] ?
Maybe help from https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da ?

## attempts
### on [[May 28th, 2023]], I started defining the #job-description comparison concept, and I ran a comparison of my blurb "2023-02-19T011846-the-story-blurb.txt" against "2023-05-28-enigma-mle.txt" . The results were maybe somewhat not easy to read. Perhaps a lot of text. Maybe I need shorter sentences?
collapsed:: true
#### Motivation / plan
So, now , let me create a quick tool, to cross the sentences of a brag document, against like 10 job description embeddings, and help match them,  to understand say, two kinds of problems,

(1) Which job descriptions match the best,
(2) but then also, for a specific job description, which sentences are  matched and which are not matched.
(3) So help you know, say even if you are not necessarily looking for something right now, can you know do you align with recent postings in your field?
#### Outcome
21:50 okay here's a quick example,

```python
import torch
import json
from pathlib import Path 
import os
import requests
from sentence_transformers.util import semantic_search

model_id =  "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()
repos_dir = os.getenv("REPOS_DIR")
workdir = str(Path(repos_dir) / "2023-interview-me"  )
loc = str(Path(repos_dir) 
          / "2023-interview-me/2023-02-19T011846-the-story-blurb.txt")

my_story_vec = Path(loc).read_text().split("\n")

  
folder = "job_descriptions"
jd1 = Path(folder) / "2023-05-28-enigma-mle.txt"

texts = jd1.read_text().split("\n")

output = query(my_story_vec)
my_story_embeddings = torch.FloatTensor(output)

output = query(texts)
jd_embeddings = torch.FloatTensor(output)


hits = semantic_search(my_story_embeddings, jd_embeddings, top_k=10)

```
22:24 Ah interesting, so since unlike the #Medicare #faq tutorial, where one question was given, I am passing an array now so my output is now also multi-dimensional

```python
# [[texts[x["corpus_id"]], x["corpus_id"]] for x in hits[0] ]
for i, row in enumerate(hits):
    print(f"({i})", "matching,", my_story_vec[i], ":")
    hmm = [[texts[x["corpus_id"]], x["corpus_id"], x["score"]] for x in row[:3] ]
    print(hmm, "\n\n")

(1) matching,  :
[['', 34, 1.0], ['', 1, 0.9999997615814209], ['', 9, 0.9999997615814209]] 


(2) matching, When I worked at zibby1, there was a project in 2015, various earlier projects.Created a Vagrant virtual machine based staging environment that developers can quickly use to stage code, to help us transition from personalized AWS staging environments which can potentially help us save several hundreds of dollars a month..  :
[['• Has experience working with distributed computing and building CI/CD tools.', 26, 0.34121203422546387], ['• Engineers best-in-class solutions that enables data scientists to develop, test, explain, deploy and monitor statistical models to production environments (we use PySpark)', 14, 0.3387572765350342], ['As a member of Machine Learning team, you will build the ML systems and infrastructure at the core of our small business data product. Your impact will be measured by the performance, testability and reliability of our ML systems.', 10, 0.28739088773727417]] 


(3) matching, Implemented the retailer lead list reporting, so that big data heavy retailers like Sears could finally be more involved in following up with customers who were not originating their preapprovals..  :
[['• Is driven to work with customers to have an impact on the real world', 29, 0.3841177821159363], ['• Impact: your work product will have a direct impact on hundreds of millions of significant decisions within the massive small business economy', 21, 0.28213953971862793], ['This is a critical and exciting time at Enigma. We are hearing from repeated customers that our product is creating tremendous value for them and is aligned perfectly with their needs. This creates an urgent need to accelerate the build out of our machine learning capabilities', 4, 0.2662915289402008]] 

```
Okay there is some beginnings of something here. Got to do some more preprocessing on this data though, do get way more cleaner comparisons .



### and on [[Jun 18th, 2023]] , how about #spacy and #[[Named Entity Recognition NER]] ,
collapsed:: true
Think because yea I saw that #sentence-transformers #[[cosine similarity]] between my #brag-document sentences and #job-description was super low, so thinking hey how about extract entities and then attempt matches using that instead,
Initially I saw that the first extraction was pulling only very few entities for this job description for instance,
19:33 hmm ok but , this is not capturing all the entities, hmm weird, 

```python
import spacy

nlp = spacy.load("en_core_web_sm")

In [3]: jd = """
   ...: Google's software engineers develop the next-generation technologies that change how billions of users connect, explore, and interact with information and one another. Our pro
   ...: ducts need to handle information at massive scale, and extend well beyond web search. We're looking for engineers who bring fresh ideas from all areas, including information r
   ...: etrieval, distributed computing, large-scale system design, networking and data storage, security, artificial intelligence, natural language processing, UI design and mobile; 
   ...: the list goes on and is growing every day. As a software engineer, you will work on a specific project critical to Google’s needs with opportunities to switch teams and projec
   ...: ts as you and our fast-paced business grow and evolve. We need our engineers to be versatile, display leadership qualities and be enthusiastic to take on new problems across t
   ...: he full-stack as we continue to push technology forward.
   ...: 
   ...: With your technical expertise you will manage project priorities, deadlines, and deliverables. You will design, develop, test, deploy, maintain, and enhance software solutions
   ...: .
   ...: 
   ...: The web is what you make of it and our team is helping the world make more of the web. From open-source pros to user-experience extraordinaires, we develop products that help 
   ...: users connect, communicate and collaborate with others. Our consumer products and cloud platforms are giving millions of users at homes, businesses, universities and nonprofit
   ...: s around the world the tools that shape their web experience -- and changing the way they think about computing.
   ...: """

In [4]: doc = nlp(jd)

In [5]: for ent in doc.ents:
   ...:     print(ent.text, ent.start_char, ent.end_char, ent.label_)
   ...: 
Google 1 7 ORG
billions 86 94 CARDINAL
UI 504 506 GPE
Google’s 641 649 ORG
millions 1396 1404 CARDINAL
```


### and on [[Jun 25th, 2023]] the [[blogpost/2023-06-25-everybody-loves-reynauds]]
So in that mini blogpost, I tried out multiple #[[embedding space]] using different embedding models. And it looked like only `“all-MiniLM-L12-v2”` appeared to have some kind of [[medical-condition]] knowledge .
### [[Jul 6th, 2023]] , can I do a #[[supervised fine-tuning]] #[[my first]] ,
collapsed:: true
yea so just starting , going through , between https://www.sbert.net/docs/training/overview.html and [[article/Train and Fine-Tune Sentence Transformers Models]]

08:35 so yea if a particular out of the box model uses [[average-pooling]] then for sure that yells at me that [[stop-words]] should be removed hmm
08:39 ACtually looking at https://www.kaggle.com/datasets?search=job and hmm I do see job related datasets. Maybe there are some relevant ones !?
How about, say, https://www.kaggle.com/datasets/niyamatalmass/google-job-skills , obtained by way of #selenium . Ok cool so this gives me hope that maybe in the future I can pull some more posts in the future, hopefully [[web-scrape]] is still possible later.
08:55 ok that is actually pretty decent, looking at the "job_skills.csv" . Some nice jargon in there !
09:04 ok so of the 4 dataset cases in https://huggingface.co/blog/how-to-train-sentence-transformers , I think makes most sense to use Case 2, where instead of assigning a number from 0 to 1 for similarity, I can just choose sentences that. I feel are similar to beuild a dataset. These are "positive pairs" [[positive pair]]
So https://huggingface.co/datasets/embedding-data/sentence-compression here is a reference example that uses this. #[[Lossy compression]] perhaps . Kind of cool since yea #summarization-task is kind of this. Some details are missed yes but get the main idea #TLDR .
I see pretty simple, each row is a json looking pair. Ah ok [[json lines]] right. Learned about this from [[Michael Light]]. https://jsonlines.org/examples/ nice.
09:13 ok so I can write some dataset building code like this, 

```python
from sentence_transformers import InputExample
from torch.utils.data import DataLoader

train_examples = []
dataset = read_json_lines(...)
for i, x in enumerate(dataset):
    s1, s2 = x
    train_examples.append(
        InputExample(texts=[s1, s2]))

train_dataloader = DataLoader(
    train_examples, shuffle=True, batch_size=16)
```
feels like I should use my [[my projects/personal/manage-my-photos]] labeler to help me kind of somewhat quickly build some labels.
Ok and for case 2 of [[positive pair]] looks like https://www.sbert.net/docs/package_reference/losses.html#multiplenegativesrankingloss [[Multiple negatives ranking loss]] #[[loss function]] should be used
```python
from sentence_transformers import losses

from sentence_transformers import SentenceTransformer

model_id = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(model_id)

train_loss = losses.MultipleNegativesRankingLoss(model=model)

# fine tune 
model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10) 
```
just try for a handful then?
```python
import pandas as pd
import os
from pathlib import Path
loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
df = pd.read_csv(loc)
```
09:30 ok stopping here. next can continue to try out the first example of this fine tuning.
### [[Jul 7th, 2023]] some [[paraphrase-mining]] hmm how can I build my dataset
08:40 [[my projects/personal/langchain-interview-me-2023-feb]]

collapsed:: true
so yea next was going to write that csv data, see can I do a fine tune , first try haha,
Wonder if I can dump out all the sentences , use out of the box similarity to see what looks like might be related, and maybe I can use the labeling annotation system I have to refine?
Ok, what are the closest right now?
```python
import pandas as pd
import os
from pathlib import Path
from functools import reduce
from collections import Counter
loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
df = pd.read_csv(loc)

raw_sentences = reduce(lambda x, y: x + y,
	[re.split(r"[\n\.]", df.iloc[i][col])
            for i in range(df.shape[0])
            for col in ["Responsibilities", 
                        'Minimum Qualifications', 
                        'Preferred Qualifications']
             if not pd.isnull(df.iloc[i][col])
            ]
)

sentences = list(set(raw_sentences))
```
hmm ok 
```python
In [101]: dict(Counter(raw_sentences).most_common(5))
Out[101]: 
{'': 14038,
 'BA/BS degree or equivalent practical experience': 521,
 'g': 261,
 "Bachelor's degree or equivalent practical experience": 71,
 ' Specific responsibilities are assigned to interns at the start of the program': 69}

In [102]: len(raw_sentences), len(sentences)
Out[102]: (31424, 9421)
```
09:13 ok and similarities , [[paraphrase-mining]] 
```python
%%time
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
paraphrases = util.paraphrase_mining(model, sentences)

for paraphrase in paraphrases[0:10]:
    score, i, j = paraphrase
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[i], sentences[j], score))
```
09:21  wow that was pretty fast . 
```python

 Work with Google Cloud Platform Partners to develop campaigns 		  Work with Google Cloud Platform partners to develop campaigns 	 Score: 1.0000
Collect customer support data from partners and derive insights for cross-functional teams 		  Collect customer support data from partners and derive insights for cross-functional teams 		 Score: 1.0000
10 years of partner programs experience at an enterprise software (or Cloud) company and experience with competitive partner programs 		 10 years of partner programs experience at an Enterprise Software (or Cloud) company and experience with competitive partner programs 		 Score: 1.0000
9 years of experience serving in the capacity of a technical sales engineer in a cloud computing environment or equivalent experience in a customer facing role (including working as a member of a professional services or systems engineering team) 		 9 years of experience serving in the capacity of a Technical Sales Engineer in a cloud computing environment or equivalent experience in a customer facing role (including working as a member of a professional services or systems engineering team) 		 Score: 1.0000
 Identify, engage, and advise Google-caliber talent with a focus on creating a great experience for each candidate 		 Identify, engage, and advise Google-caliber talent with a focus on creating a great experience for each candidate 		 Score: 1.0000
Manage a team of software engineers, including task planning and code reviews 		 Manage a team of Software Engineers, including task planning and code reviews 		 Score: 1.0000
Perform an array of administrative tasks (Manage calendars, book travel, and schedule facilities and equipment) 		 Perform an array of administrative tasks (manage calendars, book travel, and schedule facilities and equipment) 		 Score: 1.0000
Understanding of solution architecture within web and mobile environments and technical experience of web/internet related technologies, architecture across SAAS, PAAS and IAAS and competitive cloud productivity suites 		 Understanding of solution architecture within web and mobile environments and technical experience of web/internet related technologies, architecture across SaaS, PaaS and IaaS and competitive cloud productivity suites 		 Score: 1.0000
Extensive knowledge of UNIX/Linux environments 		 Extensive knowledge of Unix/Linux environments 		 Score: 1.0000
 Experience working towards strategic business goals 		 Experience working towards strategic business goals 		 Score: 1.0000
CPU times: user 1min 41s, sys: 3.35 s, total: 1min 44s
Wall time: 57.3 s
```
Ok seeing even though I used "set" I still have dupes . Ok seeing , should also use strip and lower case too
09:25 ok
```python
stripped_raw_sentences = [x.strip().lower() for x in raw_sentences]
sentences = list(set(stripped_raw_sentences))
print(len(raw_sentences), len(set(raw_sentences)), len(sentences))

# 31424 9421 9325
```
```python
%%time
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
paraphrases = util.paraphrase_mining(model, sentences)

for paraphrase in paraphrases[0:10]:
    score, i, j = paraphrase
    print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[i], sentences[j], score))
```
```python
cpa / ca or other professional accounting accreditation 		 cpa/ca or other professional accounting accreditation 		 Score: 1.0000
10 years of partner programs experience at a enterprise software (or cloud) company and experience with competitive partner programs 		 10 years of partner programs experience at an enterprise software (or cloud) company and experience with competitive partner programs 		 Score: 1.0000
5 years of partner programs experience at a enterprise software (or cloud) company 		 5 years of partner programs experience at an enterprise software (or cloud) company 		 Score: 1.0000
technically minded, with an understanding of the technology and cloud computing market, and a passion for google cloud products (g-suite, google cloud platform) 		 technically minded, with a understanding of the technology and cloud computing market, and a passion for google cloud products (g-suite, google cloud platform) 		 Score: 0.9999
shape google’s approach to partnership strategy with stakeholders in partner programs, product management, engineering, sales, and marketing; support regional engagement with strategic global and regional partners 		 shape google’s approach to partnership strategy with stakeholders in partner programs, product management, engineering, sales and marketing; support regional engagement with strategic global and regional partners 		 Score: 0.9998
a combination of hr experience in the following areas: organizational design, succession planning, performance management, diversity and inclusion, business consulting, coaching and development, talent management, data analysis and employee relations 		 a combination of hr experience in the following areas: organizational design, succession planning, performance management, diversity and inclusion, business consulting, coaching and development, talent management, data analysis, and employee relations 		 Score: 0.9998
assist clients in the adoption of new products via upgrades and migrations to develop their long term success and improve product offerings by providing client feedback on features to product management and engineering 		 assist clients in the adoption of new products via upgrades and migrations to develop their long-term success and improve product offerings by providing client feedback on features to product management and engineering 		 Score: 0.9995
build strong relationships and operating rhythms with leaders inside and outside their core product team to efficiently implement user experiences that are cohesive, inclusive and well-informed 		 build strong relationships and operating rhythms with leaders inside and outside their core product team to efficiently implement user experiences that are cohesive, inclusive, and well-informed 		 Score: 0.9995
take responsibility for technical aspects of solutions to include such activities as supporting bid responses, product and solution briefings, proof-of-concept work and the coordination of supporting technical resources 		 take responsibility for technical aspects of solutions to include such activities as supporting bid responses, product and solution briefings, proof-of-concept work, and the coordination of supporting technical resources 		 Score: 0.9994
experience serving in the capacity of a technical sales engineer in a cloud computing environment or equivalent experience in a customer facing role (including working as a member of a professional services or systems engineering team) 		 experience serving in the capacity of a technical sales engineer in a cloud computing environment or equivalent experience in a customer-facing role (including working as a member of a professional services or systems engineering team) 		 Score: 0.9994
CPU times: user 1min 45s, sys: 2.84 s, total: 1min 48s
Wall time: 1min

```
09:41 ok haha I can see there are some arbitrary internal space differences as well haha
08:49 ok lets find 10 [[positive pair]] , and use that , 
```python
pairs = [
  []
]
```

### [[Jul 10th, 2023]] looked at the vocabulary misses and job titles
collapsed:: true
#### noticed that the paraphrase mining output is not full
looks like more or less we get the better matches first
#### the model I'm testing with does have technical data sources
08:56 haha this is not simple, so many sentences, is there any way of getting around hand labeling?

Maybe I can look for technical terms which I suspect are not part of the #vocabulary , hmm
So https://huggingface.co/datasets/code_search_net and [[stack exchange]] duplicate questions and actually many other technical datasets are used per https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 ,
#### hmm oh the AutoTokenizer is a way to get tokens and vocabulary in the model
collapsed:: true
09:14 tokenizer?

```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

Downloading (…)okenizer_config.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████| 350/350 [00:00<00:00, 36.5kB/s]
Downloading (…)solve/main/vocab.txt: 100%|█████████████████████████████████████████████████████████████████████████████████████████████| 232k/232k [00:00<00:00, 7.02MB/s]
Downloading (…)/main/tokenizer.json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████| 466k/466k [00:00<00:00, 8.44MB/s]
Downloading (…)cial_tokens_map.json: 100%|███████████████████████████████████████████████████████████████████████████████████████████████| 112/112 [00:00<00:00, 28.4kB/s]

In [129]: tokenizer.vocab_files_names
Out[129]: {'vocab_file': 'vocab.txt', 'tokenizer_file': 'tokenizer.json'}

```
well that looks good ! Like a nice way perhaps to see the vocabulary,
```python
In [131]: vocabulary = tokenizer.get_vocab()

In [133]: len(vocabulary)
Out[133]: 30522

In [135]: print(list(vocabulary.keys())[:30])
['##iq', "##'", '1723', 'italians', 'caretaker', 'debbie', 'bloomberg', 'enforcing', 'sex', 'flicking', 'likes', 'glimpse', 'relax', 'coward', 'eyelids', 'worth', 'dynamics', '##¹', 'recognizes', 'arcadia', 'deportivo', 'pointedly', 'iowa', '##rio', 'moved', 'я', 'news', 'whoever', 'blossom', 'preserved']
```
09:21 Okay let me look for like if a few vocabulary terms in job descriptions are there, 
```python
job_terms = [
  "html", "databricks", "python", "css", "api", "postgresql", "database", 
  "mysql", "clojure", "java", "javascript", "angular", "idempotent", "azure",
  "github", "git", "concurrency", "asyncio", "dbutils", "ipython", "docker",
"pipeline", "sklearn", "tensorflow", "pytorch", "numpy", "pandas", "ec2", "ecs",
"aws", "sagemaker", "nginx", "redis", "cli", "auc", "xgboost", "repository"]
from tqdm import tqdm
hits = []
no_hits = []
for term in job_terms:
    for token in tqdm(vocabulary.keys()):
        if term in token:
            hits.append([term, token])
            
no_hits = list(set(job_terms) - set([x[0] for x in hits]))
```
```
In [137]: len(hits)
Out[137]: 117

In [138]: hits
Out[138]: 
[['api', 'rapidly'],
 ['api', 'shapiro'],
 ['api', 'shaping'],
 ['database', 'database'],
 ['ecs', 'ecstasy'],
 ['git', 'illegitimate'],
 ['angular', 'triangular'],
 ['git', 'digits'],
 ['cli', 'clicks'],
 ['cli', 'inclination'],
 ['api', 'apical'],
 ['java', 'java'],
 ['cli', 'cycling'],
 ['cli', 'clip'],
 ['cli', 'clit'],
 ['api', 'capitals'],
 ['cli', 'clicked'],
 ['cli', 'cliff'],
 ['concurrency', 'concurrency'],
 ['auc', 'caucus'],
 ['java', 'javanese'],
 ['cli', 'clifton'],
 ['cli', 'client'],
 ['git', 'legitimacy'],
 ['api', 'capita'],
 ['cli', 'clicking'],
 ['git', 'digit'],
 ['api', 'capitalist'],
 ['aws', 'flaws'],
 ['cli', 'incline'],
 ['cli', 'climbs'],
 ['cli', 'inclined'],
 ['git', 'digitally'],
 ['git', 'legitimate'],
 ['cli', 'decline'],
 ['cli', 'clinical'],
 ['git', 'longitude'],
 ['cli', 'declining'],
 ['pipeline', 'pipeline'],
 ['cli', 'climax'],
 ['cli', 'clinics'],
 ['api', 'capitol'],
 ['aws', 'laws'],
 ['aws', 'claws'],
 ['api', 'rapid'],
 ['azure', 'azure'],
 ['api', 'dilapidated'],
 ['angular', 'rectangular'],
 ['api', 'api'],
 ['api', 'gaping'],
 ['auc', 'caucasus'],
 ['redis', 'rediscovered'],
 ['cli', 'declines'],
 ['cli', 'eclipse'],
 ['git', 'agitated'],
 ['auc', 'bureaucracy'],
 ['api', 'scraping'],
 ['cli', 'clive'],
 ['database', 'databases'],
 ['api', 'therapist'],
 ['git', 'longitudinal'],
 ['cli', 'cyclist'],
 ['cli', 'climates'],
 ['cli', 'clinging'],
 ['auc', 'caucasian'],
 ['angular', 'angular'],
 ['cli', 'radcliffe'],
 ['cli', 'clinched'],
 ['git', 'agitation'],
 ['api', 'capitalism'],
 ['cli', 'recycling'],
 ['aws', 'lawson'],
 ['git', 'fugitive'],
 ['cli', 'cyclists'],
 ['api', 'capital'],
 ['python', 'python'],
 ['aws', 'paws'],
 ['cli', 'clint'],
 ['cli', 'clifford'],
 ['cli', '##cliff'],
 ['auc', 'auction'],
 ['cli', 'circling'],
 ['repository', 'repository'],
 ['auc', 'sauce'],
 ['html', 'html'],
 ['cli', 'clips'],
 ['aws', 'outlaws'],
 ['cli', '##cliffe'],
 ['api', 'escaping'],
 ['aws', 'lawsuit'],
 ['cli', 'clinch'],
 ['api', 'leaping'],
 ['api', 'rapids'],
 ['cli', 'clients'],
 ['auc', 'auckland'],
 ['cli', 'climb'],
 ['cli', 'climate'],
 ['cli', 'cyclic'],
 ['aws', 'dawson'],
 ['cli', 'declined'],
 ['cli', 'click'],
 ['cli', 'climatic'],
 ['cli', 'clinic'],
 ['aws', 'lawsuits'],
 ['cli', 'climbing'],
 ['api', 'napier'],
 ['aws', 'draws'],
 ['api', 'landscaping'],
 ['aws', 'jaws'],
 ['git', 'digital'],
 ['cli', 'clinton'],
 ['redis', 'redistribution'],
 ['git', '##git'],
 ['cli', 'climbed'],
 ['cli', 'clipped'],
 ['cli', 'cliffs'],
 ['cli', 'euclidean']]
```
ok this is interesting then 
```
In [140]: no_hits
Out[140]: 
['github',
 'databricks',
 'mysql',
 'pytorch',
 'sklearn',
 'postgresql',
 'docker',
 'nginx',
 'idempotent',
 'sagemaker',
 'xgboost',
 'css',
 'clojure',
 'dbutils',
 'tensorflow',
 'asyncio',
 'pandas',
 'numpy',
 'ec2',
 'ipython',
 'javascript']
```
#### and job titles, maybe I could group along that first
collapsed:: true
09:36 also another thing for trying next is I should also cut up and do paraphrase mining perhaps within the particular job title, (printing just a sample below )

```python
In [144]: print(df["Title"].unique().tolist()[:20])
['Google Cloud Program Manager', 'Supplier Development Engineer (SDE), Cable/Connector', 'Data Analyst, Product and Tools Operations, Google Technical Services', 'Developer Advocate, Partner Engineering', 'Program Manager, Audio Visual (AV) Deployments', 'Associate Account Strategist (Czech/Slovak), Global Customer Experience', 'Supplier Development Engineer, Camera, Consumer Hardware', 'Strategic Technology Partner Manager, Healthcare and Life Sciences', 'Manufacturing Business Manager, Google Hardware', 'Solutions Architect, Healthcare and Life Sciences, Google Cloud', 'Data Analyst, Consumer Hardware', 'Partner Onboarding Manager (Americas)', 'Associate Account Strategist (Ukrainian), GMS Sales', 'Survey Lead, Google Cloud Support', 'Solution Architect, Google Cloud Platform (Apigee)', 'Manufacturing Test Engineer', 'Machine Learning Product Specialist, Google Cloud (EMEA)', 'Software Engineering Manager, Cloud Storage, Site Reliability Engineering', 'Global Supply Chain Manager, Display/Touch, Consumer Hardware', 'Technical Program Manager, ASIC Development']



In [145]: len(df["Title"].unique().tolist())
Out[145]: 794

```
this list of titles is pretty extensive and might have duplicates also
#### thoughts for later
use vocabulary misses maybe to figure out what to fine tune with
### [[Jul 11th, 2023]] refined the nohits per the vocabulary of the model and used it to tokenize to verify they are unknown
collapsed:: true
#### yea no hits
first let me use more precise way of looking for hits,

```python
job_terms = [
  "html", "databricks", "python", "css", "api", "postgresql", "database", 
  "mysql", "clojure", "java", "javascript", "angular", "idempotent", "azure",
  "github", "git", "concurrency", "asyncio", "dbutils", "ipython", "docker",
"pipeline", "sklearn", "tensorflow", "pytorch", "numpy", "pandas", "ec2", "ecs",
"aws", "sagemaker", "nginx", "redis", "cli", "auc", "xgboost", "repository"]
from tqdm import tqdm
hits = []
no_hits = []
for term in job_terms:
    for token in tqdm(vocabulary.keys()):
        if term == token.strip("#"):
            hits.append([term, token])
            
no_hits = list(set(job_terms) - set([x[0] for x in hits]))
```
08:58 yea thats a lot of nohits,
```python
In [151]: hits
Out[151]: 
[['html', 'html'],
 ['python', 'python'],
 ['api', 'api'],
 ['database', 'database'],
 ['java', 'java'],
 ['angular', 'angular'],
 ['azure', 'azure'],
 ['git', '##git'],
 ['concurrency', 'concurrency'],
 ['pipeline', 'pipeline'],
 ['repository', 'repository']]

In [152]: no_hits
Out[152]: 
['github',
 'databricks',
 'ecs',
 'mysql',
 'pytorch',
 'sklearn',
 'auc',
 'aws',
 'postgresql',
 'docker',
 'nginx',
 'idempotent',
 'sagemaker',
 'cli',
 'xgboost',
 'css',
 'clojure',
 'dbutils',
 'tensorflow',
 'asyncio',
 'pandas',
 'redis',
 'numpy',
 'ec2',
 'ipython',
 'javascript']

```


#### and drafting looking for the nohits in the dataset,
So do I see job descriptions that have those job terms I did not find vocabulary hits for?

```python
import pandas as pd
import os
from pathlib import Path
loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
jobsdf = pd.read_csv(loc)

import utils as ut
columns = ["Responsibilities", 
                            'Minimum Qualifications', 
                            'Preferred Qualifications']
raw_sentences = ut.extract_raw_sentences(jobsdf, columns)

sentences_with_oov_tokens = []
for sentence in raw_sentences:
    words = re.split(r"[^a-zA-Z0-9]", sentence)
    words = [x for x in words if x]

    # for token in no_hits:
  
```
#### realized how to tokenize an arbitrary sentence
and therefore I can see this model indeed does not know about that vocabulary !
09:23 let me just try to tokenize a fabricated sentence that has the no hit tokens,

```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

sentence = "familiar with xgboost pandas and tensorflow including docker and other technologies"
sentences = [sentence]
encoded_input = tokenizer(
  sentences, padding=True, truncation=True, return_tensors='pt')

{'input_ids': tensor([[  101,  5220,  2007,  1060, 18259,  9541,  3367, 25462,  2015,  1998,
         23435, 12314,  2164,  8946,  2121,  1998,  2060,  6786,   102]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])}

```
hmm not really clear since these are numeric encodings, how to get the vocabulary debugging part here.
09:38 ah ok never mind found it in the docs here https://huggingface.co/learn/nlp-course/chapter2/4?fw=pt#tokenization
09:38 ok so here is how to #debugging #tokenizer #tokenization
```python
sentence = "familiar with xgboost pandas and tensorflow including docker and other technologies"
tokenizer.tokenize(sentence)

In [178]: print(tokenizer.tokenize(sentence))
['familiar', 'with', 'x', '##gb', '##oo', '##st', 'panda', '##s', 'and', 'tensor', '##flow', 'including', 'dock', '##er', 'and', 'other', 'technologies']

```
so yea super interesting ! if a particular word is not recognized in the vocabulary, it just gets split up into stuff that is known or the `##` is used perhaps to create some kinds of smaller #subword-tokenization .
I was reading the documentation of that tokenizer and found this section,
#+BEGIN_QUOTE

    is_split_into_words (`bool`, *optional*, defaults to `False`):
        Whether or not the input is already pre-tokenized (e.g., split into words). If set to `True`, the
        tokenizer assumes the input is already split into words (for instance, by splitting it on whitespace)
        which it will tokenize. This is useful for NER or token classification.

#+END_QUOTE
which I think is pretty cool, referring to #[[Named Entity Recognition NER]] , used with this,
09:41 next ok yea thinking would love to inform this model of the entities, vocabulary t hat is missing.


### [[Jul 12th, 2023]] ok started building up code to capture a mini corpus, of the sentences, which have words that are not part of the vocabulary,
collapsed:: true
08:17 [[my projects/personal/langchain-interview-me-2023-feb]]

09:05 ok wow organized earlier notes a bit !
So should I therefore, collect the sentences that have the no hits and at least see what happens if I fine tune with those, if the new #sentence-transformers model has the new vocabulary ?
ok, so to build a corpus, thinking for each sentence in this dataset I am working with right now, if I tokenize it using the AutoTokenizer from `'sentence-transformers/all-MiniLM-L6-v2'` , and the output does not include my desired tokens or tokens prefixed with `##` but the sentence does have the words in question visible in plain text, then that sentence is a candidate for the fine tuning set I think !
09:16 Also I just glanced through what this out put, looks like,
```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
vocabulary = tokenizer.get_vocab()
print(vocabulary.keys())
```
And I don't see anything upper case so pretty sure I can stick to lower case !
So first the slower way, and maybe I can find a faster #PyTorch way later,
09:34 ok drafting this on the side still. but high level concept yea,
find sentences that have the one or more of the desired terms in plain text,
that actually might be good enough, as long as I have checked indeed the words are no hits against the model vocabulary
but can also tokenize such sentences and verify that the expected tokens do not exist
09:36 have a high level #question though, per #subword-tokenization how do you contain #[[Named Entity Recognition NER]] concepts if they can end up being broken up? #card
Like even in the example in https://huggingface.co/learn/nlp-course/chapter2/4?fw=pt#tokenization , somehow "transformer" is not in

```
"bert-base-cased"
```
isn't that kind of silly?

and [[Jul 13th, 2023]] , got a bunch of the no hit sentences, at least for some definition,
08:41 [[my projects/personal/langchain-interview-me-2023-feb]]

collapsed:: true
hm ok, 
```python
import utils as ut
nohit_list = ut.current_nohit_list("sentence-transformers/all-MiniLM-L6-v2")

raw_sentences = ut.extract_raw_sentences(jobsdf, columns)

```
09:02 ok will filter oov words like this
```python
In [191]: for x in raw_sentences[:4]:
     ...:     print("=============")
     ...:     print(x, "\n", ut.sequence_from_sentence(x), "\n")
     ...: 
=============
lead projects from start to finish and manage all issues that impact design 
 ['lead', 'projects', 'from', 'start', 'to', 'finish', 'and', 'manage', 'all', 'issues', 'that', 'impact', 'design'] 

=============
break the mold, and bring creativity and innovation in strategy and tactics 
 ['break', 'the', 'mold', 'and', 'bring', 'creativity', 'and', 'innovation', 'in', 'strategy', 'and', 'tactics'] 

=============
become a brand advocate; engage and influence internal and external relationships; build, customize and deliver solutions through forums to achieve outcomes in support of the brand advertising annual plan 
 ['become', 'a', 'brand', 'advocate', 'engage', 'and', 'influence', 'internal', 'and', 'external', 'relationships', 'build', 'customize', 'and', 'deliver', 'solutions', 'through', 'forums', 'to', 'achieve', 'outcomes', 'in', 'support', 'of', 'the', 'brand', 'advertising', 'annual', 'plan'] 

=============
experience in java and/or python development 
 ['experience', 'in', 'java', 'and', 'or', 'python', 'development'] 


```
09:08 only search some of the technical roles maybe, to try to get faster results, 
```python
raw_titles = ut.extract_raw_sentences(jobsdf, ["Title"])
title_vocab = reduce(lambda x, y: x + y, 
                     [ut.sequence_from_sentence(x) for x in raw_titles]
)
print(Counter(title_vocab).most_common(25))

[('manager', 300), ('google', 237), ('cloud', 167), ('and', 127), ('sales', 89), ('marketing', 87), ('engineer', 79), ('technical', 71), ('account', 64), ('lead', 64), ('business', 63), ('partner', 62), ('solutions', 61), ('operations', 59), ('product', 57), ('specialist', 57), ('services', 53), ('english', 52), ('analyst', 52), ('hardware', 51), ('associate', 48), ('global', 46), ('program', 44), ('customer', 43), ('development', 42)]


```
ok based off of that, "engineer" feels like a safe assumption here,
09:17 ok so just the engineer sentences then, 
```python
In [203]: jobsdf[jobsdf["Title"].str.contains("engineer")].shape
Out[203]: (0, 7)

In [204]: jobsdf[jobsdf["Title"].str.contains("Engineer")].shape
Out[204]: (140, 7)

In [205]: jobsdf.shape
Out[205]: (1250, 7)

columns = ["Responsibilities", 
                            'Minimum Qualifications', 
                            'Preferred Qualifications']
engineer_df = jobsdf[jobsdf["Title"].str.contains("Engineer")].copy()
raw_sentences = ut.extract_raw_sentences(engineer_df, columns)

nohit_sentences = ut.find_nohit_sentences(raw_sentences, nohit_list)
```
```python
In [211]: len(raw_sentences), len(nohit_sentences)
Out[211]: (1217, 38)

  
In [212]: nohit_sentences
Out[212]: 
[['programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
  ['javascript']],
 ['experience with java, javascript, html5, and sap technologies like sap hana, sap fiori, netweaver',
  ['javascript']],
 ['experience with java for android, objective-c for ios, html, javascript',
  ['javascript']],
 ['experience building multi-tier high availability applications with modern web technologies (such as nosql, mongodb, sparkml, tensorflow)',
  ['tensorflow']],
 ['software development platforms and solutions experience (java servlets, javascript, php, asp, cgi, ajax, flash, cookies and xml)',
  ['javascript']],
 ['familiarity in one or more common web or mobile development language such as java, python, go, php, javascript, etc',
  ['javascript']],
 ['experience with front-end web technologies (html5, css3, and javascript)',
  ['javascript']],
 ['technical experience in web technologies such as html, xml, json, oauth 2 along with experience in analysis of relational data in mysql, google bigquery or similar',
  ['mysql']],
 ['familiarity with architecture and operational aspects of large scale distributed systems; familiarity with the popular technologies in the machine learning/big data ecosystem (tensorflow, spark, etc)',
  ['tensorflow']],
 ['html5, css3, and javascript development experience', ['javascript']],
 ['java, c/c++, c#, python, javascript, or go)', ['javascript']],
 ['experience with web technologies (object-oriented javascript, html, css), and experience with the latest web standards including html5 and css3',
  ['javascript', 'css']],
 ['experience programming in one of the following: java, javascript and/or c++',
  ['javascript']],
 ['4 years of relevant work experience, including web application experience or skills using ajax, html, css or javascript',
  ['javascript', 'css']],
 [', sql, mysql, mapreduce, hadoop)', ['mysql']],
 ['experience working with deployment and orchestration technologies (such as pxe, docker, kubernetes, puppet, chef, salt, ansible, jenkins)',
  ['docker']],
 ['development experience in c, c++ or java and experience designing modular, object-oriented javascript',
  ['javascript']],
 ['expert html and css skills', ['css']],
 [', unit, functional, integration, stress testing) for your code, using one or more of the following: c, c++, c#, java, javascript, go, or python',
  ['javascript']],
 ['experience in writing software in one or more languages such as java, c++, python, go, javascript',
  ['javascript']],
 ['experience with one or more general purpose programming languages including but not limited to: c/c++, c#, python, javascript, go, objective-c, swift',
  ['javascript']],
 ['fluency in one or more of the following: python, javascript, java, php, perl, or c++',
  ['javascript']],
 ['previous tech internships or relevant work experience programming in c, c++, c#, java, javascript, go or python',
  ['javascript']],
 [', object-oriented javascript, html, css)', ['javascript', 'css']],
 ['restful, soap, etc), and javascript', ['javascript']],
 ['experience in backend development and using one or more cloud platform services (aws, azure, gcp)',
  ['aws']],
 ['1 year of experience in software engineering and coding, working with two or more of the following languages: java, c/c++, c#, objective-c, python, javascript, php, ruby and/or go',
  ['javascript']],
 ['4 years of experience working with front end languages such as html5, css, javascript (angularjs)',
  ['javascript', 'css']],
 ['experience with web technologies such as html, css, javascript, and http',
  ['javascript', 'css']],
 ['software development platforms and solutions to include j2ee, java servlets, javascript, python, go, php, asp, cgi, ajax',
  ['javascript']],
 [', r, python, matlab, pandas) and database languages (e', ['pandas']],
 ['experience with modern javascript frameworks (such as backbone, angular, or ember) and css pre-processing frameworks (such as sass or less)',
  ['javascript', 'css']],
 ['experience in writing code fixes and tools to solve problems in c, c++, c#, java, javascript, go or python (e',
  ['javascript']],
 ['net, python, shell, perl, javascript)', ['javascript']],
 ['programming experience in one or more of the following languages/platforms: android, java, kotlin, ios, javascript',
  ['javascript']],
 ['experience with one or more general purpose programming languages including but not limited to: java, c/c++, c#, objective c, python, javascript, or go',
  ['javascript']],
 ['experience in writing software in one or more languages such as java, python, go, javascript, c++, or similar',
  ['javascript']],
 ['experience with java for android, and objective-c for ios, html and javascript',
  ['javascript']]]
```
09:25 hmm also actually seeing sometimes splitting on a `"."` is not quite accurate.
okay so next, since this is not looking terribly like a whole lot of sentences, can manually assign the ones that are similar, say, and try a fit.

### [[Jul 15th, 2023]] finally tried the [[supervised fine-tuning]] but didn't seem to add to the vocabulary
collapsed:: true
#### created clusters manually, by looking at my no hit list from earlier, of sentences containing words that were not in the vocabulary,
collapsed:: true
20:07 going to just manually create some groups, 

```python
# web stuff, front end leaning
group1 = [
  'programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
  'experience with java, javascript, html5, and sap technologies like sap hana, sap fiori, netweaver',
  'software development platforms and solutions experience (java servlets, javascript, php, asp, cgi, ajax, flash, cookies and xml)',
  'experience with front-end web technologies (html5, css3, and javascript)',
  'html5, css3, and javascript development experience',
  'experience with web technologies (object-oriented javascript, html, css), and experience with the latest web standards including html5 and css3',
  '4 years of relevant work experience, including web application experience or skills using ajax, html, css or javascript',
  'expert html and css skills',
  'restful, soap, etc), and javascript',
  '4 years of experience working with front end languages such as html5, css, javascript (angularjs)',
  'experience with web technologies such as html, css, javascript, and http',
  'software development platforms and solutions to include j2ee, java servlets, javascript, python, go, php, asp, cgi, ajax',
  'experience with modern javascript frameworks (such as backbone, angular, or ember) and css pre-processing frameworks (such as sass or less)',
  
]

# feeling more back end mle ish, 
group3 = [
  'experience building multi-tier high availability applications with modern web technologies (such as nosql, mongodb, sparkml, tensorflow)',
  'technical experience in web technologies such as html, xml, json, oauth 2 along with experience in analysis of relational data in mysql, google bigquery or similar',
  'familiarity with architecture and operational aspects of large scale distributed systems; familiarity with the popular technologies in the machine learning/big data ecosystem (tensorflow, spark, etc)',
  ', sql, mysql, mapreduce, hadoop)',
  'experience working with deployment and orchestration technologies (such as pxe, docker, kubernetes, puppet, chef, salt, ansible, jenkins)',
  'experience in backend development and using one or more cloud platform services (aws, azure, gcp)',
  ', r, python, matlab, pandas) and database languages ',
  
]

# mobile dev 
group2 = [
  'experience with java for android, objective-c for ios, html, javascript',
  'familiarity in one or more common web or mobile development language such as java, python, go, php, javascript, etc',
  'java, c/c++, c#, python, javascript, or go)',
  'experience programming in one of the following: java, javascript and/or c++',
  'development experience in c, c++ or java and experience designing modular, object-oriented javascript',
  ', unit, functional, integration, stress testing) for your code, using one or more of the following: c, c++, c#, java, javascript, go, or python',
  'experience in writing software in one or more languages such as java, c++, python, go, javascript',
  'experience with one or more general purpose programming languages including but not limited to: c/c++, c#, python, javascript, go, objective-c, swift',
  'fluency in one or more of the following: python, javascript, java, php, perl, or c++',
  '1 year of experience in software engineering and coding, working with two or more of the following languages: java, c/c++, c#, objective-c, python, javascript, php, ruby and/or go',
  'experience in writing code fixes and tools to solve problems in c, c++, c#, java, javascript, go or python ',
  'programming experience in one or more of the following languages/platforms: android, java, kotlin, ios, javascript',
  'experience with one or more general purpose programming languages including but not limited to: java, c/c++, c#, objective c, python, javascript, or go',
  'experience in writing software in one or more languages such as java, python, go, javascript, c++, or similar',
  'experience with java for android, and objective-c for ios, html and javascript',
]
```
### Then created a dataset from that, and ran fit with the out of the box 'all-MiniLM-L6-v2' sentence transformer model
collapsed:: true
20:36 since https://huggingface.co/datasets/embedding-data/sentence-compression/tree/main is given as the example and since I see those [[json lines]] , but it is with [[git-lfs]] , let me try pull it as appropriate,

ok file was "sentence-compression_compressed.jsonl.gz", internally looks like this
```
$ head data/kaggle-google-job-skills/sentence-compression_compressed.jsonl 
{"set": ["The USHL completed an expansion draft on Monday as 10 players who were on the rosters of USHL teams during the 2009-10 season were selected by the League's two newest entries, the Muskegon Lumberjacks and Dubuque Fighting Saints.", "USHL completes expansion draft"]}
{"set": ["Major League Baseball Commissioner Bud Selig will be speaking at St. Norbert College next month.", "Bud Selig to speak at St. Norbert College"]}
{"set": ["It's fresh cherry time in Michigan and the best time to enjoy this delicious and nutritious fruit.", "It's cherry time"]}
{"set": ["An Evesham man is facing charges in Pennsylvania after he allegedly dragged his girlfriend from the side of his pickup truck on the campus of Kutztown University in the early morning hours of Dec. 5, police said.", "Evesham man faces charges for Pa."]}
{"set": ["NRT LLC, one of the nation's largest residential real estate brokerage companies, announced several executive appointments within its Coldwell Banker Residential Brokerage operations in Southern California.", "NRT announces executive appointments at its Coldwell Banker operations in Southern California"]}
{"set": ["THE JSE kept toying with an all time high by midday today as resources continued to fuel the bourse.", "JSE keeps toying with all time high"]}
{"set": ["The government is defending the latest police crime statistics despite a worrying rise in the recorded amount of violent offending.", "Government defends crime statistics"]}
{"set": ["The renovated Marappalam bridge, which had been opened for two-wheelers last week, was opened for other vehicles also on Friday.", "Marappalam bridge opened"]}
{"set": ["A new survey shows 30 percent of Californians use Twitter, and more and more of us are using our smart phones to go online.", "Survey: 30 percent of Californians use Twitter"]}
{"set": ["Brightpoint ,a provider of logistic services to the mobile industry, has started operations in the Turkish market.", "Brightpoint starts operations on Turkish market"]}

```
20:50 ah ok the literal word "set" really is in there okay ! 
```python
import os
import utils as u
from pathlib import Path

path = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/2023-07-15-positive-pairs.jsonl")

dataset = u.make_positive_pairs_from_groups(group1, group2, group3)
path.write_text("\n".join([json.dumps(x) for x in dataset]))


from sentence_transformers import InputExample
from torch.utils.data import DataLoader

train_examples = []
for i, x in enumerate(dataset):
    train_examples.append(
        InputExample(texts=[x["set"][0], x["set"][1]])
    )
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# MultipleNegativesRankingLoss 
from sentence_transformers import losses

model = SentenceTransformer('all-MiniLM-L6-v2')
train_loss = losses.MultipleNegativesRankingLoss(model=model)


model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10) 
```
21:31 ok started that . Actually going pretty fast as I expected since yea my dataset is small for a proof of concept , 
```
Iteration: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:16<00:00,  1.26s/it]
Epoch:  10%|████████████                                                                                                             | 1/10 [00:16<02:27, 16.36s/it]
Iteration:  92%|███████████████████████████████████████████████████████████████████████████████████████████████████████████         | 12/13 [00:19<00:01,  1.64s/it]
...
...
CPU times: user 4min 8s, sys: 38.8 s, total: 4min 47s
Wall time: 2min 43s
```
### hmm but new vocabulary does not seem to reflect new terms somehow
And yea curious if I can see the vocabulary now as different, 

```python

path = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/2023-07-15-fine-tuned-on-pairs.foo")
model.save(path)
```
21:42 oh nice, I see the vocab.txt got saved, in that folder, 
```python
# 2023-07-15-fine-tuned-on-pairs.foo/vocab.txt"
path = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/2023-07-15-fine-tuned-on-pairs.foo"
            / "vocab.txt")
vocab = path.read_text()


In [250]: set(nohit_list) & set(vocab)
Out[250]: set()

In [251]: set([f"##{x}" for x in nohit_list]) & set(vocab)
Out[251]: set()

```
21:48 hmm not seeing any words from the nohit list in the dumped out vocab though. hmm ok back to the drawing board then? haha


### [[Jul 16th, 2023]] yea tried a different take on adding tokens to a tokenizer and that seemed to do it.
collapsed:: true
#### yea it was not "tokenizer.json"
11:17 ok so next though,

11:23 hmm interesting, I also looked at the "tokenizer.json" file that got created when doing `model.save()`, next to the "vocab.txt". They have the same tokens looks like except "tokenizer.json" also refers to the input ids [[tokenized-input-ids]] ,
11:30 hmm but maybe fine tuning simply does not update the vocabulary?
#### but "add_tokens"
collapsed:: true
12:01 ok super interesting, reading [here on medium](https://angelina-yang.medium.com/how-to-add-new-tokens-to-a-transformer-model-vocabulary-da778f99f910) someone kind of confirming that to expand the vocabulary [[add to transformer vocabulary]], and prevent [[out-of-vocabulary-words-OOV]], you need another approach,

12:32 lets try their recommendation,  just took out the for-loop since yea looking at current documentation for `add_tokens` function, you can add a list instead. Incorporating w/ a check of what is my hit list and no hit list ,
```python
from transformers import AutoTokenizer, AutoModel

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

nohit_list = ut.current_nohit_list("sentence-transformers/all-MiniLM-L6-v2")

# Before
vocabulary_before = list(tokenizer.get_vocab().keys())

tokenizer.add_tokens(nohit_list)

# add new embeddings to the embedding matrix of the transformer model
model.resize_token_embeddings(len(tokenizer))

# After 
vocabulary_after = list(tokenizer.get_vocab().keys())

# Did it work?
```
14:09 hmm got an error, 
```python
AttributeError: 'SentenceTransformer' object has no attribute 'resize_token_embeddings'
```
when trying to resize .
Maybe need to go one level down, to the lower layer.
```python
for child in model.children():
    print(child, hasattr(child, "resize_token_embeddings"), "\n")

Transformer({'max_seq_length': 256, 'do_lower_case': False}) with Transformer model: BertModel  False 

Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False}) False 

Normalize() False 
```
14:13 hmm nope, weird.
But ok looks like this part worked, 
```python
In [263]: print(set(vocabulary_after) - set(vocabulary_before))
{'github', 'databricks', 'nlp', 'ecs', 'pytorch', 'pyspark', 'sklearn', 'auc', 'aws', 'postgresql', 'docker', 'nginx', 'idempotent', 'sagemaker', 'xgboost', 'cli', 'css', 'clojure', 'spacy', 'ipython', 'dbutils', 'tensorflow', 'asyncio', 'redis', 'pandas', 'numpy', 'ec2', 'mysql', 'javascript'}


```
How about the tokenize command?
```python
sentence = "familiar with xgboost pandas and tensorflow including docker and other technologies"
print(tokenizer.tokenize(sentence))

['familiar', 'with', 'xgboost', 'pandas', 'and', 'tensorflow', 'including', 'docker', 'and', 'other', 'technologies']

```
14:18 ok nice #moment/satisfaction well that does seem to work.
so next, question is then, I should attempt to do some #[[cosine similarity]] , before and after, to understand did this really help 😀



### [[Jul 17th, 2023]] Reading more, I learn you do likely need to train a new tokenizer and you can't just simply update its vocabulary
collapsed:: true
#### Quick side question I had about this last tokenizer and its case awareness,
out of curiosity, does tokenize now show this for upper case too now? Should be yes right since this is a uncased model

```python
sentence = "familiar with XGBoost pandas and TensorFlow including Docker and other technologies"
print(tokenizer.tokenize(sentence))

['familiar', 'with', 'xgboost', 'pandas', 'and', 'tensorflow', 'including', 'docker', 'and', 'other', 'technologies']

```
08:47 nice . answer is yes.
#### yea hugging face docs,
collapsed:: true
So I suppose that now okay this is how you add tokens to this tokenizer, but two problems still.

Well one obvious problem is the tokenizer now needs to be thrown back into the model,
But also, so what if the tokenizer now has this vocabulary, I think now the [[supervised fine-tuning]] step next can help tell this model what is the association of these new tokens in the [[embedding space]] right?
Otherwise, without that, I'm curious what would the output vector , embedding, even look like for sentences with those new words? Like a undefined error? or like a equivalent of a zero vector ?
09:03 ok wow so the answer is in their nice course here, [chapter 6 ](https://huggingface.co/learn/nlp-course/chapter6/2?fw=pt), on training [[tokenizer]] [[train new tokenizer from an old one]]
So funny enough, the example being used here is [[code understanding]] , [[source code embedding]]
and so this dataset is used, to update the tokenizer of `gpt-2`, 
```python
raw_datasets = load_dataset("code_search_net", "python")
```
```python
from transformers import AutoTokenizer

old_tokenizer = AutoTokenizer.from_pretrained("gpt2")
```
```python
tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, 52000)
```
fastinating side note mentioned here is that there are tokenizers that can be written in python, which are slow and also can be written in #Rust-lang and also #cuda .
hmm so ok then you can save that tokenizer, 
```python
tokenizer.save_pretrained("code-search-net-tokenizer")
```
but how about updating the original model then ?
09:21 ok well conceptually, skipping ahead in the [[hugging face]] course there, I see [here in chapter 7](https://huggingface.co/learn/nlp-course/chapter7/2?fw=pt#fine-tuning-the-model), that you can use a `Trainer` from 
````
from transformers import Trainer
````
in order to fine tune a model and pass a tokenizer as an input,
So per above I suspect that is the answer to my question!
#### So thinking about next steps
Ok so a conceptual update here, I think maybe I need to hunt down some datasets or build a dataset which has additional technical language, and then use that to fine tune a tokenizer, and not just add vocabulary to it with `tokenizer.add_tokens` haha that was not a full answer. Yea and then I would need to use some of the tips in chapter 6 and 7 of the [[hugging face]] course to fine tune a model but a sentence transformer model say, with the tokenizer that I updated.


### [[Jul 18th, 2023]] reading more about subword tokenization and purpose of tokenizer tuning 
collapsed:: true
not sure if my use case where technical terms are lacking from a tokenizer warrants this but maybe
09:07 So then I'm not sure why the https://huggingface.co/blog/how-to-train-sentence-transformers method I used earlier for fine tuning, earlier [here the other day](https://michal.piekarczyk.xyz/post/2023-06-18-my-projects-langchain-interview-me-2023-feb/#then-created-a-dataset-from-that-and-ran-fit-with-the-out-of-the-box-all-minilm-l6-v2-sentence-transformer-model) , did not update the vocabulary. ,

09:13 Hmm ok maybe the explanation they give up front [here](https://huggingface.co/learn/nlp-course/chapter6/1?fw=pt) helps to confirm that fine tuning a transformer model will not update the tokenizer. My impression is that  fine tuning a transformer model is really just going to update the weights and since we know that many transformer models use [[subword-tokenization]], although you have new words, the fine tuning weight adjustments are made off of the subword tokens that are less meaningful than if they had concepts mapped out for those new words
Although I am also slightly getting the impression that training a tokenizer is less about vocabulary and more about like #grammar because in their phrasing they refer not to the differences in the vocabulary between #English and #Japanese but to the differences in punctuation .
And they are fine tuning a tokenizer on [[source code]] which definitely has different #grammar .
09:26 yea and additionally [here](https://huggingface.co/learn/nlp-course/chapter6/2?fw=pt) they spell out that [[train new tokenizer from an old one]] is really about deciding what are good [[subword-tokenization]] to use, actually what sub-words. hmm
But a tokenizer does indeed have a vocabulary so hmm, is my problem a tokenizer vocabulary problem or is it really I should be looking at this as a [[Named Entity Recognition NER]] problem ?
#### but yea next should try,
09:32 anyway I should still just try this,

so next let me apply the mini corpus I had from last time, to this,  and lets see what the new tokenizer does 
```python
tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, 52000)
```


### [[Jul 19th, 2023]] Ran the tokenizer fine tuning with a small dataset
The vocabulary of the output of `train_new_from_iterator` had only the new data. So "mission accomplished" haha I got the new vocabulary in there but at the cost of missing the original vocabulary 😅
#### Trying this out
collapsed:: true
so let's follow along per [hugging face nlp chapter 6 ](https://huggingface.co/learn/nlp-course/chapter6/2?fw=pt),

09:23 what does the data they are passing in for their use case look like?
```python
from datasets import load_dataset

# This can take a few minutes to load, so grab a coffee or tea while you wait!
raw_datasets = load_dataset("code_search_net", "python")

training_corpus = (
    raw_datasets["train"][i : i + 1000]["whole_func_string"]
    for i in range(0, len(raw_datasets["train"]), 1000)
)
```
ok haha I don't want to download the whole thing because I am using a laptop tethered to my phone [[phone-tether]] #moment/haha . But I can just look at it online, https://huggingface.co/datasets/code_search_net  , 
per the above, each row is a record and "whole_func_string" is a string of the function definition.
So their training_corpus data would look like a list of strings basically. Ok let me repurpose my mini [[positive pair]] dataset from earlier for this then,
```python
import os
import json
import utils as u
from functools import reduce
from pathlib import Path

path = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/2023-07-15-positive-pairs.jsonl")


"2023-07-15-positive-pairs.jsonl"

training_corpus = list(set(
    reduce(
        lambda x, y: x + y,
        [json.loads(x)["set"] for x in Path(path).read_text().splitlines()]
    )
))


```
09:40 ok so the second argument to 
```python
train_new_from_iterator
```
is the vocab_size . And currently it is, 
```python
from transformers import AutoTokenizer
old_tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

old_tokenizer.vocab_size
# Out[275]: 30522
```
ok the 52,000 in that doc is a lot more. Curious what happens , 
```python
tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, 52000)
[00:00:00] Pre-processing sequences                 ███████████████████████████████████████████████████████████████████████ 0        /        0
[00:00:00] Tokenize words                           ███████████████████████████████████████████████████████████████████████ 182      /      182
[00:00:00] Count pairs                              ███████████████████████████████████████████████████████████████████████ 182      /      182
[00:00:00] Compute merges                           ███████████████████████████████████████████████████████████████████████ 527      /      527


In [278]: tokenizer.vocab_size
Out[278]: 601
```
09:44 hmm interesting, so perhaps for this to work properly, I would have needed all the original data also, concatenated with the new data? Let me just last thing, look at the vocab and hit or no hit with my terms at least, 
```python
old_vocabulary = old_tokenizer.get_vocab()
vocabulary = tokenizer.get_vocab()

len(old_vocabulary), len(vocabulary)
# Out[281]: (30522, 601)

import utils as ut
job_terms = ut.get_nohit_job_terms()

print(job_terms)
# ['html', 'databricks', 'python', 'css', 'api', 'postgresql', 'database', 'mysql', 'clojure', 'java', 'javascript', 'angular', 'idempotent', 'azure', 'github', 'git', 'concurrency', 'asyncio', 'dbutils', 'ipython', 'docker', 'pipeline', 'sklearn', 'tensorflow', 'pytorch', 'numpy', 'pandas', 'ec2', 'ecs', 'aws', 'sagemaker', 'nginx', 'redis', 'cli', 'auc', 'xgboost', 'repository', 'pyspark', 'nlp', 'spacy']

In [285]: set(job_terms) & set(vocabulary)
Out[285]: 
{'angular',
 'aws',
 'azure',
 'css',
 'database',
 'docker',
 'html',
 'java',
 'javascript',
 'mysql',
 'pandas',
 'python',
 'tensorflow'}
```
ok haha well good to know at least this does indeed update the vocabulary for at least the new stuff. But since vocab is super small, makes me think yea this needs to be built using original and new data , from scratch perhaps.
#### Thoughts
summary thinkings here

I think I should go back to the original task of   evaluating how good is a model at matching a brag document to job description texts, perhaps also building my own dataset that can be used for this evaluation on a out of the box model, comparing then to something new



### [[Jul 20th, 2023]] did bit of reading learning , research mode 
Think I am now convinced that yes, having new terminology is a good reason for a new tokenizer, because otherwise a tokenizer that does not have the new words, will do excessive splitting and am embedding model will be less likely to get useful signal from them,
#### main benefit of train_new_from_iterator , is lets you quickly use the same class as an earlier tokenizer, but yea this is not a fine tuning step like I thought before
Looking at notes from yesterday, and that new tokenizer, yea it has some of the new vocabulary,

Some of it is not sub-worded, remaining intact 
```python
print(set(job_terms) & set(vocabulary))
{'aws', 'tensorflow', 'angular', 'docker', 'pandas', 'database', 'java', 'mysql', 'azure', 'css', 'python', 'html', 'javascript'}

```
And yea some of it underwent [[subword-tokenization]] 
```python
print(set(job_terms) - set(vocabulary))
{'databricks', 'api', 'nlp', 'ecs', 'concurrency', 'pyspark', 'pytorch', 'sklearn', 'auc', 'pipeline', 'postgresql', 'nginx', 'idempotent', 'sagemaker', 'cli', 'xgboost', 'git', 'repository', 'clojure', 'spacy', 'dbutils', 'asyncio', 'redis', 'numpy', 'ec2', 'ipython', 'github'}
```
09:11 So this sentence become, 
```python
print(tokenizer.tokenize(
  "Within databricks, you can use pyspark or scala, but to use tensorflow or pytorch in databricks, you need to stick to pyspark."))

['with', '##i', '##n', 'data', '##b', '##ri', '##ck', '##s', ',', 'yo', '##u', 'c', '##a', '##n', 'us', '##e', 'py', '##s', '##p', '##ark', 'or', 'sca', '##la', ',', 'but', 'to', 'us', '##e', 'tensorflow', 'or', 'py', '##t', '##or', '##ch', 'in', 'data', '##b', '##ri', '##ck', '##s', ',', 'yo', '##u', 'ne', '##e', '##d', 'to', 'st', '##ic', '##k', 'to', 'py', '##s', '##p', '##ark', '[UNK]']

```
Ok so I suppose the advantage of the form, 
```python
tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, 52000)
```
is you are using the specific class of that earlier tokenizer, 
```python
print(old_tokenizer.__class__.__name__, tokenizer.__class__.__name__)
BertTokenizerFast BertTokenizerFast
```
and training a tokenizer from scratch, I can find, 
```python
from tokenizers import BertWordPieceTokenizer
```
but I don't see `BertTokenizerFast` in that same namespace
#### and learned more precisely why , [[why a custom tokenizer]] , and also actually how a typical [[byte-pair encoding]] [[tokenizer]] algorithm relies on sub word frequencies when building a vocabulary
09:56 ok so then I am missing the primary reason maybe also of the custom tokenizer? [[why a custom tokenizer]]

Person [with this medium post](https://medium.com/analytics-vidhya/create-a-tokenizer-and-train-a-huggingface-roberta-model-from-scratch-f3ed1138180c), is also under the impression that a custom tokenizer [[tokenizer]] is useful as a way of focusing on your unique vocabulary,
> our domain is very specific, words and concepts about clothes, shapes, 
colors, … Therefore, we are interested in defining our own tokenizer 
created from our specific vocabulary, avoiding including more common 
words from other domains or use cases that are irrelevant for our final 
purpose.
10:13 ok reading, [here](https://huggingface.co/docs/transformers/tokenizer_summary) for some more detail,
So the focus around tokenizing 
```python
"Don't you love 🤗 Transformers? We sure do."
```
w.r.t. `["Don't", "you",]` versus `["Don", "'", "t"]` versus `["Do", "n't"]`
does hint that yes you do want to help extract units of meaning,
And they say that yes you ideally want a smaller vocabulary size to help constrain computation,  but using say [[character tokenization]] although ends up w/ a small vocabulary, will be less expressive and capturing the  meaning of words will be more difficult.
Feels like in the case of jargon words, like #acronym or just brand new words like "Tensorflow" or "pytorch" , I can see sometimes subword tokenization will be helpful, since say it would be great if the  word "tensor" was tokenized as meaningfully related to "tensorflow", similarly between "pytorch" and "python". And I get that if you are using a subword tokenizer with a good bit of language as a input, then you should have enough to prevent the [[out-of-vocabulary-words-OOV]] misses ,
10:51 Also they describe the example of `BertTokenizer` tokenizing an acronym it has not seen,
```python
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
tokenizer.tokenize("I have a new GPU!")
["i", "have", "a", "new", "gp", "##u", "!"]
```
And they only mention the benefit, of not having the vocabulary miss, but no mention of the meaning of the concept of #GPU getting missed .
Oh and they explain that the #double-hashtag  allows tokenization to be reversible since now you know to re-attach the subwords. But not every tokenizer is reversible I think. Or at least not every tokenizer has the same syntax, since they point out , the use of the underscore `_` instead, in `XLNetTokenizer`

```python
from transformers import XLNetTokenizer

tokenizer = XLNetTokenizer.from_pretrained("xlnet-base-cased")

tokenizer.tokenize("Don't you love 🤗 Transformers? We sure do.")
["▁Don", "'", "t", "▁you", "▁love", "▁", "🤗", "▁", "Transform", "ers", "?", "▁We", "▁sure", "▁do", "."]
```
11:10 going back to [chapter 6 here](https://huggingface.co/learn/nlp-course/chapter6/2), their statement helps with [[why a custom tokenizer]] ,
They highlight extreme reasons like your language is different than the original languages used in a model, or that your corpus is "very different" 😀.
So I am leaning more that this is about the statistics of your text data as it relates to allowing language models to extract meaning , but without being a performance burden.
12:36 continue reading there, see if I missed something,
collapsed:: true
Ah interesting so per [here](https://huggingface.co/docs/transformers/tokenizer_summary#bytepair-encoding-bpe), the [[vocabulary size]] is a hyper parameter, that is like a ceiling for splitting words, so if when just say space-splitting, we have too many words, then we split until the vocabulary size is under the input there.
collapsed:: true
But I know per my earlier attempt, yesterday, where I provided ,
```python
tokenizer = old_tokenizer.train_new_from_iterator(training_corpus, 52000)
```
I ended up with 
``python
In [278]: tokenizer.vocab_size
Out[278]: 601
``
and still I had quite a lot of [[subword-tokenization]] going on, so there are other details looks like.
So at least the [[byte-pair encoding]] #algorithm-type , will start with a base vocabulary which consists of just the characters.
collapsed:: true
12:51 ok actually glad I kept reading this is interesting, so this algo, will iteratively, find the most frequent symbol pair, adding the merger to its vocabulary, then finding the next most frequent symbol pair after that.
So symbols start out as just letters, but after one iteration, a symbol would consist of two characters together. And larger clumps can form after that.
So their example, started out with space split words with frequencies, 
```python
("hug", 10), ("pug", 5), ("pun", 12), ("bun", 4), ("hugs", 5)
```
and starting with a base vocabulary of 
```python
["b", "g", "h", "n", "p", "s", "u"]
```
and after performing three merges, having a vocabulary of 
```python
["b", "g", "h", "n", "p", "s", "u", "ug", "un", "hug"]
```
and at that point they showed that the original set of words and their frequencies would be represented as 
```python
("hug", 10), ("p", "ug", 5), ("p", "un", 12), ("b", "un", 4), 
("hug", "s", 5)  
```
and that a new test word like `"mug"` say would end up getting represented as `["<unk>", "ug"]`, since for this case `"m"` just was not part of the initial vocabulary.
13:10 and ultimately the size of the vocabulary for a tokenizer, [[vocabulary size]] will be the size of the base vocabulary plus the number of merges before it was decided to stop .
And clearly, haha we can have some absurd algorithm implementation that never stops and we end up with a vocabulary that includes  all the full words that were encountered, and then therefore we would get fewer computational benefits .
13:21 ok so [[why a custom tokenizer]], in the [video link](https://youtu.be/DJimQynXZsQ) #video-type, embedded in [chapter 6 link](https://huggingface.co/learn/nlp-course/chapter6/2?fw=pt), the lean is now to yes train a tokenizer from scratch if there is new jargon yes as in a new "domain" , #card
So high level four good reasons, for [[why a custom tokenizer]] [[derive-from-scratch]] #card
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1689873985593_0.png" width="50%">}}
new language,
new characters ( with accents)
new domain (medical, technical, legal)
new style (haha like [[Old English]] or [[Old French]] )
#take-away ohhh and #moment/aha a really good example is explained that a tokenizer unfamiliar with a #corpus  will excessively split and that is not good because #[[input sequence]] is limited [[context-window]] [[maximum-context-size]] !
And so you will risk not capturing the full sentence you want to pass to a #LLM . Nice.
Excessive tokenizer splitting, can impact model performance, too, #question #card , why though?
Maybe the argument is similar to like "<UNK>" those unknowns, in that there is less information being captured. My intuitive reasoning is that tiny subwords embedding representations will be likely meaningless . The #attention will get thrown off by basically letter chunks that will end up being as common as the word "the" , so perhaps you will have just #stop-words at that point with low information.
Example of this particular model tokenizer missing a lot of #unicode characters from [[Bangla]] #language-type . 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1689874273026_0.png" width="50%">}}
And yea [[out-of-vocabulary-words-OOV]] "<UNK>" , has no useful information for the model to use there.
And [[excessive splitting by tokenizer]] , for say #[[biomedical Glossary]]
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1689875286166_0.png" width="50%">}}
And for the other example given, of using `code-search-net` python dataset to train a tokenizer, I like the question that gets asked is [[performance-lift]] at least eye-balling. And in below example, she does show it is desirable to capture a concept as one token, but I think this will ultimately only happen if that example is more frequent , relative to other patterns when doing merges per  [[byte-pair encoding]]
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1689875776287_0.png" width="50%">}}
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1689875808385_0.png" width="50%">}}



### [[Jul 21st, 2023]] mainly just brief thoughts about building a new dataset
Thinking next I should look through various datasets out there , and choose which would have good english language breadth but also depth into the technical jargon world.

So for sure a dataset from job descriptions from that nice #Kaggle data. , https://www.kaggle.com/datasets/niyamatalmass/google-job-skills?resource=download
maybe there are others like that , but for sure I think this is something that would need to be updated at least once or twice a year because technical terms change frequently
09:29 side note this very much feels like a [[data-drift]] problem but feels like [[nlp-drift]]

### [[Jul 22nd, 2023]] one   brief look model card for, `'sentence-transformers/all-MiniLM-L6-v2'`
Think I am seeing that this model did not update the tokenizer of the pretrained model that it fine tuned.
So what are the dataset sources in `'sentence-transformers/all-MiniLM-L6-v2'` which has been my goto model recently.

So per https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 here,  haha there are a billion sentence tuples in there haha. Not sure how easy it will be to perform the same fine tuning steps, but maybe the tokenizer step requires way less data.
13:31 So next want to answer yea what data was used for the tokenizer there.
Ok so looking at https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/blob/main/train_script.py the `train_script.py` in there, it doesn't look like they modified the tokenizer that was from the pre-trained model, given as an input at the bottom, 
```
#python train_many_data_files_v2.py --steps 1000000 --batch_size 128 \
    --model nreimers/MiniLM-L6-H384-uncased train_data_configs/all_datasets_v4.json output/all_datasets_v4_MiniLM-L6-H384-uncased-batch128
```
ok so then perhaps I should look up the card for that then.
### [[Jul 23rd, 2023]] More practical dive today
Refreshed my story blurb texts after several months. Pulled another kaggle job description dataset for analysis. And another run of cosine similarity for the corpori corpi (what is plural of corpus haha )
#### wrapping up thoughts on tokenizers from other day
09:53 ok two thoughts, so

collapsed:: true
I can look at `nreimers/MiniLM-L6-H384-uncased` and if a tokenizer is described there,
And I can also look at that [chapter 7 fine tuning link](https://huggingface.co/learn/nlp-course/chapter7/2?fw=pt#fine-tuning-the-model) that takes a tokenizer passed in .
10:07 I also do want to think more high level, about the overall goal , task and reevaluate approaches.
But ok, quick look, of possible, at https://huggingface.co/nreimers/MiniLM-L6-H384-uncased ,
10:13 only points to https://huggingface.co/microsoft/MiniLM-L12-H384-uncased but not much else to go on
10:18 and that points to this paper, https://arxiv.org/abs/2002.10957 , hmm [[LLM distillation]] with a [[LLM distillation/teacher model and teacher assistant]]
10:28 well looking at their [train code in github](https://github.com/microsoft/unilm/blob/master/minilm/examples/run_xnli.py) , it looks like for each teacher assistant model (where the MiniLM on hugging face is one of them) , they appear to use these tokenizers directly, 
```python
from transformers import (
    BertTokenizer,
    DistilBertTokenizer,
    XLMTokenizer,
    XLMRobertaTokenizer,
)
```
without modification.
#### Datasets
10:31 ok hmm think I should define dataset and problem bit more now

collapsed:: true
ok going back to a core early example,  from [here](https://michal.piekarczyk.xyz/post/2023-06-18-my-projects-langchain-interview-me-2023-feb/#on-may-28th-2023-i-started-defining-the-job-description-comparison-concept-and-i-ran-a-comparison-of-my-blurb-2023-02-19t011846-the-story-blurbtxt-against-2023-05-28-enigma-mletxt--the-results-were-maybe-somewhat-not-easy-to-read-perhaps-a-lot-of-text-maybe-i-need-shorter-sentences) , I ran [[cosine similarity]] per [[sentence-transformers]] , let me try it again , ( [[May 28th, 2023]] )
This time with  the new dataset I have and maybe I will add another one too.
So look at that dataset job titles again,
```python
from sentence_transformers.util import semantic_search

import pandas as pd
import os
from functools import reduce
from collections import Counter
from pathlib import Path
import utils as ut

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
jobsdf = pd.read_csv(loc)

import utils as ut
columns = ["Responsibilities", 
                            'Minimum Qualifications', 
                            'Preferred Qualifications']

raw_titles = ut.extract_raw_sentences(jobsdf, ["Title"])
title_vocab = reduce(lambda x, y: x + y, 
                     [ut.sequence_from_sentence(x) for x in raw_titles]
)

print(Counter(title_vocab).most_common(25))
print("total", len(set(title_vocab)))
```
```python
[('manager', 300), ('google', 237), ('cloud', 167), ('and', 127), ('sales', 89), ('marketing', 87), ('engineer', 79), ('technical', 71), ('account', 64), ('lead', 64), ('business', 63), ('partner', 62), ('solutions', 61), ('operations', 59), ('product', 57), ('specialist', 57), ('services', 53), ('english', 52), ('analyst', 52), ('hardware', 51), ('associate', 48), ('global', 46), ('program', 44), ('customer', 43), ('development', 42)]
total 624
```
Picking a few more that stand out, 
```python
technical_job_title_terms = [
  "engineer", "developer", "research", "technical", "analyst", "engineering",
  "data", "sciences", "ux", "analytics", "systems", "architect", "researcher", "web",
  "infrastructure", "intelligence", "quantitative", "learning", "software",
  "scientist",
        ]
```

11:48 Maybe can see if more #MLE jobs in [this kaggle dataset](https://www.kaggle.com/datasets/atahmasb/amazon-job-skills) of #Amazon job descriptions.
12:47 ok so lets run cosine similarity, ranked, between my corpus and these, descriptions,
14:36 my last blurb was a few months ago, [here](https://michal.piekarczyk.xyz/post/2023-02-18-first-stab-langchain-interview-me/) ,  so refreshing slightly, 
```python
import yaml
import tempfile
from pathlib import Path
from datetime import datetime
import pytz
import os
import utils as ut

def utc_now():
    return datetime.utcnow().replace(tzinfo=pytz.UTC)

def utc_ts(dt):
    return dt.strftime("%Y-%m-%dT%H%M%S")

def read_yaml(loc):
    with open(loc) as fd:
        return yaml.safe_load(fd)

repos_dir = Path(os.getenv("REPOS_DIR"))
assert repos_dir.is_dir()      
experience_loc = repos_dir / "my-challenges-and-accomplishments/experience.yaml"

experiences_dict = read_yaml(experience_loc)["Descriptions"]
my_sentences = ut.build_my_blurb(experiences_dict)


```
15:44 ok and compare with those datasets,
Mini filter example, 
```python
import pandas as pd

vec = [
{"title": "Software Engineer yea"},
{"title": "Some Scientist"},
{"title": "Product Manager"},
{"title": "Industrial Designer"}
]
df = pd.DataFrame.from_records(vec)

In [31]: df
Out[31]: 
                   title
0  Software Engineer yea
1         Some Scientist
2        Product Manager
3    Industrial Designer

In [32]: df.query("title.str.contains('software', case=False) or title.str.contains('scientist', case=False)")
Out[32]: 
                   title
0  Software Engineer yea
1         Some Scientist

```
16:16 ok put that into a func,  ( putting it [here](https://github.com/namoopsoo/interview-me/blob/main/utils.py) )
```python
def filter_pandas_multiple_contains(df, column, vec, case=False):
    """filter dataframe for column containing any string from list vec given.

    Example
    >>> vec = [
    ... {"title": "Software Engineer yea"},
    ... {"title": "Some Scientist"},
    ... {"title": "Product Manager"},
    ... {"title": "Industrial Designer"}
    ]
    >>> df = pd.DataFrame.from_records(vec)
    >>> df
                       title
    0  Software Engineer yea
    1         Some Scientist
    2        Product Manager
    3    Industrial Designer
    >>> import utils as ut
    >>> ut.filter_pandas_multiple_contains(df, "title", ["engineer", "scientist"])
                       title
    0  Software Engineer yea
    1         Some Scientist
    """
    query = " or ".join(
            [f"{column}.str.contains('{x}', case={case})"
             for x in vec])
    return df.query(query)

```

```python
In [39]: ut.filter_pandas_multiple_contains(df, "title", ["engineer", "scientist"])
Out[39]: 
                   title
0  Software Engineer yea
1         Some Scientist

```

```python

import pandas as pd
import os
from pathlib import Path
import utils as ut

raw_sentences = []

technical_job_title_terms = [
  "engineer", "developer", "research", "technical", "analyst", "engineering",
  "data", "sciences", "ux", "analytics", "systems", "architect", "researcher", "web",
  "infrastructure", "intelligence", "quantitative", "learning", "software",
  "scientist",
        ]

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
jobsdf = ut.filter_pandas_multiple_contains(
    pd.read_csv(loc), "Title", technical_job_title_terms)
columns = ["Responsibilities", 
                            'Minimum Qualifications', 
                            'Preferred Qualifications']
raw_sentences.extend(ut.extract_raw_sentences(
  jobsdf, columns))
print("len raw_sentences after ingestion", len(raw_sentences))

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
			/ "kaggle-amazon-job-skills/amazon_jobs_dataset.csv")
jobsdf = ut.filter_pandas_multiple_contains(
    pd.read_csv(loc), "Title", technical_job_title_terms)
columns = [
    'DESCRIPTION',
    'BASIC QUALIFICATIONS',
    'PREFERRED QUALIFICATIONS']
raw_sentences.extend(ut.extract_raw_sentences(
  jobsdf, columns))
print("len raw_sentences after ingestion", len(raw_sentences))
```
```python
len raw_sentences after ingestion 3259
len raw_sentences after ingestion 33081
```
17:44 ok yea and doing that top k cosine similarity then 
```python

import json
from pathlib import Path 
import os
import requests
from sentence_transformers.util import semantic_search

model_id =  "sentence-transformers/all-MiniLM-L6-v2"
hf_token = os.getenv("HF_TOKEN")

my_story_embeddings = ut.vec_to_embeddings(model_id, hf_token, my_sentences)

jd_embeddings = ut.vec_to_embeddings(model_id, hf_token, raw_sentences[:1000])
# this line took 
# Wall time: 7.05 s

hits = semantic_search(my_story_embeddings, jd_embeddings, top_k=100)

for i, row in enumerate(hits[:5]):
    print(f"({i})", "matching,", my_sentences[i], ":")
    hmm = [[raw_sentences[x["corpus_id"]], x["corpus_id"], x["score"]] for x in row[:3] ]
    print(hmm, "\n\n")

```
18:07
```python
In [20]: for i, row in enumerate(hits[:5]):
    ...:     print(f"({i})", "matching,", my_sentences[i], ":")
    ...:     hmm = [[raw_sentences[x["corpus_id"]], x["corpus_id"], x["score"]] for x in row[:3] ]
    ...:     print(hmm, "\n\n")
    ...: 
(0) matching, Built our initial method for model hosting, transitioning from a purely business rule based flow :
[['experience in practical business modeling or financial modeling\ndistinctive problem solving and analytical skills, combined with impeccable business judgment', 740, 0.45160090923309326], ['review and fulfill managed software requests to ensure products meet business needs, while overseeing programmatic compliance with associated software licenses/other agreements, contractual terms, and policies', 394, 0.433631956577301], ['experience in business planning and/or financial modeling', 425, 0.4310281574726105]] 


(1) matching, Created a Vagrant virtual machine based staging environment that developers can quickly use to stage code, to help us transition from personalized AWS staging environments which can potentially help us save several hundreds of dollars a month. :
[['experience architecting, developing software, or internet scale production-grade big data solutions in virtualized environments such as google cloud platform', 753, 0.4532877206802368], ['establish and drive planning and execution steps towards production deployments', 959, 0.4100092053413391], ['experience in designing and implementing build automation, and configuration management for operating system platforms.', 859, 0.3592562973499298]] 


(2) matching, 
Implemented the retailer lead list reporting, so that big data heavy retailers like Sears could finally be more involved in following up with customers who were not originating their preapprovals. :
[['create effective, scalable, and easy to understand reporting solutions (e.g', 262, 0.45110809803009033], ['lead global analysis of in-store demo device analytics', 833, 0.4380985200405121], ['demonstrated understanding of customer support verticals', 961, 0.42506536841392517]] 


(3) matching, 
Troubleshooted and fixed rare and difficult to detect buyout bugs. When customers had multiple payments being taken on a day when they also did a buyout, for example, there was a bug where we were incorrectly discounting the additional payments that they made that day. :
[['serve as a central coordination point for customer bugs and issues escalated by internal sales teams', 941, 0.4794199466705322], ['author test plans with the goal of catching issues and fixing them at early design stage to improve the overall product quality and meet aggressive schedule', 313, 0.39714837074279785], ['support product implementation and help partners in their day to day challenges by delivering innovative and scalable solutions to their problems and troubleshooting their issues', 796, 0.3908129930496216]] 


(4) matching, 
Refactored payment processing to reflect a better interpretation of the law around customer suspense dollars. Previously, customers would pay down their next months payment. In the change, any payments that are made outside of the due date count towards the suspense account. This change required splitting out the plan shifting, away from the payment processing, into its own separate task, to simplify the new implementation of the payment law. :
[['work with partner teams to re-engineer process workflows around demand planning, supply planning, ordering, and fulfillment', 219, 0.32384926080703735], ['experience in devising and implementing strategies and business improvements.', 863, 0.31515663862228394], ['consult with internal account management teams and customers to track the progress and impact', 621, 0.30947157740592957]] 

```
Ok so definitely still not impressed with the hits I'm getting here.
#### Thoughts
A few follow up items coming to mind,

collapsed:: true
I think per above experiment I ran, I want to find a few false negative matches , look at the scores they are producing, and then probably take a closer dive into the [[average-pooling]] . I want to really answer the question, do I need to do pre-processing, removing [[stop-words]] so the [[sentence-transformers]] [[cosine similarity]] after average pooling does not suffer?
And then after doing the preprocessing if necessary , excluding it as an issue or acting to remove stop words or fluff words, then lets run cosine similarity like that.
And then maybe a refined , more granular approach would be to think about using [[Named Entity Recognition NER]] maybe to better remove stop words , especially if I do not perhaps have the luxury of  fine tuning.
but yea side note I think fine tuning would be really helpful to help with embedding these interesting jargon words close to each other if they are indeed related
And as a visual debugging I really should plot out or at least someone must have some nice tool to visualize embeddings


### [[Jul 24th, 2023]] started a nice debug session today , false negative analysis here,
Ok per my notes from [[Jul 23rd, 2023]], let me hunt down one good [[false negative]],

For sure I am realizing yes a lot of my sentences in my personal corpus are lacking a succinctness and there is a lot of filler in there ideally I should cut out.
Actually it would be cool to have that kind of feedback actually as a tool, ranking sentences by fluff haha that should be improved. And even, how many sentences are used in describing each individual project/story, can be helpful to see analyzed too.
```python
import random

# Using "my_sentences" defined last time

for i, x in enumerate(random.choices(my_sentences, k=4)):
    print(i, x)
    
0 So the behavior was changed and I had this now, erroneously haha, so I needed to now remove it
1 Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions
2 Improved our sklearn  model training that was crashing on a laptop, by cutting up the data into chunks and using python multiprocessing
3 (7) "humana hackathon exploration of langchain against health plan documents" ( I have described this in more detail earlier above )

```
Ok in any case, so let me search the corpus I have, for terms, say, spark, cluster pyspark, databricks . Of course I am realizing Google and Amazon have their own options for clustering and these job descriptions might not mention pyspark, but let's see, 
```python
import pandas as pd
import utils as ut

# Using "raw_sentences" defined last time
df = pd.DataFrame({"description": raw_sentences})

In [29]: df.iloc[:5]
Out[29]: 
                                         description
0            app scripts, spreadsheet software, etc)
1  leadership, problem solving and analysis exper...
2  hands-on experience using and/or managing data...
3  background in solving complex challenges and d...
4  travel frequently around emea for meetings, te...

terms = ["pyspark", "spark", "databricks", "multiprocessing", "cluster"]
resultsdf = ut.filter_pandas_multiple_contains(df, "description", terms)

In [34]: resultsdf.shape
Out[34]: (154, 1)

In [36]: resultsdf.iloc[:10]["description"].tolist()
Out[36]: 
['hands-on experience using and/or managing databases, or cloud technologies such as sql, nosql, hadoop or spark',
 'familiarity with architecture and operational aspects of large scale distributed systems; familiarity with the popular technologies in the machine learning/big data ecosystem (tensorflow, spark, etc)\ntechnical experience in web technologies such as html, xml, json, oauth 2 along with experience in analysis of relational data in mysql, google bigquery or similar',
 'regression, classification, clustering, etc)',
 'know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery',
 'experience using and/or managing databases, and with one or all of the following: mapreduce, hadoop, spark, flume, hive, impala, spark sql and/or bigquery',
 'experience building multi-tier high availability applications with modern web technologies (such as nosql, mongodb, sparkml, tensorflow)',
 'experience with data processing software (such as hadoop, spark, pig, hive) and data processing algorithms (mapreduce, flume)',
 'technologies you will employ to solve these complex real-world business problems include natural language processing, machine learning, image recognition, elastic computing, spark, and a host of other state of the art aws technologies',
 'in order to drive expansion of the amazon catalog, we use cluster-computing technologies like mapreduce, spark and hive to process billions of products and algorithmically find products not already sold on amazon',
 'experience working with scala/python/java on spark to build and deploy ml models in production']


```
09:19 Ok cool, so there are a few meaty sentences here that would be good to compare more directly with debugging eyes .
for example,
```python 
from sentence_transformers.util import semantic_search, cos_sim
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

model_id =  "sentence-transformers/all-MiniLM-L6-v2"
hf_token = os.getenv("HF_TOKEN")

s1 = "Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions"
s2 = 'know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery'
s3 = 'experience working with scala/python/java on spark to build and deploy ml models in production'


for s in [s1, s2, s3]:
    print(s, tokenizer.tokenize(s), "\n\n")


embeddings = ut.vec_to_embeddings(model_id, hf_token, [s1, s2, s3])

In [45]: cos_sim(embeddings[0,:], embeddings[1, :])
Out[45]: tensor([[0.2323]])

In [46]: cos_sim(embeddings[0,:], embeddings[2, :])
Out[46]: tensor([[0.2320]])

```
also try the other way too , 
```python
In [43]: sentences = [s1, s2, s3]
    ...: hits = semantic_search(embeddings, embeddings, top_k=3)
    ...: for i, row in enumerate(hits[:5]):
    ...:     print(f"({i})", "matching,", sentences[i], ":")
    ...:     hmm = [[sentences[x["corpus_id"]], x["corpus_id"], x["score"]] for x in row[:3] ]
    ...:     print(hmm, "\n\n")
    ...: 
(0) matching, Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions :
[['Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions', 0, 1.0], ['know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 0.23231448233127594], ['experience working with scala/python/java on spark to build and deploy ml models in production', 2, 0.2320040762424469]] 


(1) matching, know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery :
[['know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 0.9999999403953552], ['experience working with scala/python/java on spark to build and deploy ml models in production', 2, 0.4644332528114319], ['Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions', 0, 0.23231443762779236]] 


(2) matching, experience working with scala/python/java on spark to build and deploy ml models in production :
[['experience working with scala/python/java on spark to build and deploy ml models in production', 2, 1.000000238418579], ['know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 0.4644332826137543], ['Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions', 0, 0.2320040762424469]] 


```
Ok so that gave around same result. Ok cool, no matter which func was used,
Ok cool, so next want to keep diving deeper, probably ultimately looking at [[average-pooling]] here.


### [[Jul 25th, 2023]] Stop word removal experiment
So for the question yesterday, why was it that two cosine similarity comparisons had basically same score, `0.2323` and `0.2320`, maybe that is a clue.

I think I have seen that completely unrelated sentences can have a zero score comparison right? 
```python

s1 = "If a tree falls in the forest and there is no one there to hear it, then does it make a sound?"
s2 = "A bagel with cream cheese with some lox and some capers would go great with coffee."

for s in [s1, s2]:
    print(s, tokenizer.tokenize(s), "\n\n")
    
set(tokenizer.tokenize(s1)) & set(tokenizer.tokenize(s2))
# {'a', 'and'}

embeddings = ut.vec_to_embeddings(model_id, hf_token, [s1, s2])

cos_sim(embeddings[0,:], embeddings[1, :])
# tensor([[0.0240]])
```
09:03 ok cool
So for example from yesterday, lets see what happens if we remove [[stop-words]] . ( Side note [stacko link](https://datascience.stackexchange.com/questions/86252/effect-of-stop-word-removal-on-transformers-for-text-classification) someone suggests also trying to mask stop words ) .

```python
import nltk
from sentence_transformers.util import semantic_search, cos_sim
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

model_id =  "sentence-transformers/all-MiniLM-L6-v2"
hf_token = os.getenv("HF_TOKEN")

from nltk.corpus import stopwords


s1 = "Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions"
s2 = 'know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery'
s3 = 'experience working with scala/python/java on spark to build and deploy ml models in production'

def dont_stop(s):
    stop_words = stopwords.words('english')
    return " ".join([x for x in s.split() if x.lower() not in stop_words])
    

for s in [s1, s2, s3]:
    print(s, "\n", dont_stop(s), "\n\n")
```
```python
Took Databricks Spark cluster and pyspark to answer a question about a CDC Covid dataset, what is the asymptomatic rate by age bin as well as hospitalization rate by presence of prior medical conditions 
 Took Databricks Spark cluster pyspark answer question CDC Covid dataset, asymptomatic rate age bin well hospitalization rate presence prior medical conditions 


know your way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery 
 know way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery 


experience working with scala/python/java on spark to build and deploy ml models in production 
 experience working scala/python/java spark build deploy ml models production 
```
09:23 hmm not a whole lot of stop words there but lets try anyway, 
```python
sentences = [s1, s2, s3]
stopped = [dont_stop(x) for x in sentences]
embeddings = ut.vec_to_embeddings(model_id, hf_token, stopped)

hits = semantic_search(embeddings, embeddings, top_k=3)
for i, row in enumerate(hits[:5]):
    print(f"({i})", "matching,", stopped[i], ":")
    hmm = [[stopped[x["corpus_id"]], x["corpus_id"], x["score"]] for x in row[:3] ]
    print(hmm, "\n\n")
```
```python
(0) matching, Took Databricks Spark cluster pyspark answer question CDC Covid dataset, asymptomatic rate age bin well hospitalization rate presence prior medical conditions :
[['Took Databricks Spark cluster pyspark answer question CDC Covid dataset, asymptomatic rate age bin well hospitalization rate presence prior medical conditions', 0, 1.0], ['know way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 0.3553411066532135], ['experience working scala/python/java spark build deploy ml models production', 2, 0.25089341402053833]] 


(1) matching, know way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery :
[['know way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 1.0000001192092896], ['experience working scala/python/java spark build deploy ml models production', 2, 0.37388813495635986], ['Took Databricks Spark cluster pyspark answer question CDC Covid dataset, asymptomatic rate age bin well hospitalization rate presence prior medical conditions', 0, 0.3553411364555359]] 


(2) matching, experience working scala/python/java spark build deploy ml models production :
[['experience working scala/python/java spark build deploy ml models production', 2, 1.0000001192092896], ['know way around map reduce, hadoop, spark, flume, hive, impala, sparksql, bigquery', 1, 0.3738881051540375], ['Took Databricks Spark cluster pyspark answer question CDC Covid dataset, asymptomatic rate age bin well hospitalization rate presence prior medical conditions', 0, 0.25089341402053833]] 

```
09:33 ok well I am seeing improvements undeniably here, 
```
0.3553 vs 0.2323
0.25089 vs 0.23200
```
so therefore [[sentence-transformers]] #take-away is not internally penalizing stop words as I had thought a bit that it might before.
Ok I think next I still want to just dissect the way [[sentence-transformers]] [[cosine similarity]] gets the result and reproduce it manually see if I get the same thing

### [[Jul 26th, 2023]] some more experimentation, cosine similarity and stop words

ok next, yea let's try reproducing that [[cosine similarity]] ,

from last time, yea this model produces embeddings with this size, 
```python
In [63]: embeddings[0,:].shape
Out[63]: torch.Size([384])
```
08:36 just double checking, 
```python
n [68]: np.dot(embeddings[0, :], embeddings[1, :]), cos_sim(embeddings[0, :], embeddings[1, :])
Out[68]: (0.35534108, tensor([[0.3553]]))
```
Ok next,  just out of curiosity, since [blog post](https://towardsdatascience.com/text-pre-processing-stop-words-removal-using-different-libraries-f20bac19929a) also mentions that #spacy has a longer #stop-words list,

```python
from nltk.corpus import stopwords as sw_nltk
import spacy
en = spacy.load('en_core_web_sm')
sw_spacy = en.Defaults.stop_words


def dont_stop_both(s):
    en = spacy.load('en_core_web_sm')
    sw_spacy = en.Defaults.stop_words
    stop_words = set(sw_nltk.words('english') ) | set(sw_spacy)
    
    return " ".join([x for x in s.split() if x.lower() not in stop_words])


sentences = [s1, s2, s3]
stopped = [dont_stop(x) for x in sentences]
stopped_both = [dont_stop_both(x) for x in sentences]

[len(x) for x in stopped], [len(x) for x in stopped_both]
# ([158, 82, 76], [153, 75, 76])

```
08:57 ok so compare all three ways, for completeness
```python
results = []
for name, a_list in [("original", sentences), ("nltk", stopped), ("nltk+spacy", stopped_both)]:
    embeddings = ut.vec_to_embeddings(model_id, hf_token, a_list)
    results.append({"what": name, 
                    "one": cos_sim(embeddings[0, :], embeddings[1, :]),
                    "two": cos_sim(embeddings[0, :], embeddings[2, :]),
                   })
pd.DataFrame.from_records(results)

         what                 one                 two
0    original  [[tensor(0.2323)]]  [[tensor(0.2320)]]
1        nltk  [[tensor(0.3553)]]  [[tensor(0.2509)]]
2  nltk+spacy  [[tensor(0.3329)]]  [[tensor(0.2501)]]
```
09:08 Ok haha can be slightly hit or miss then .
But if I did this other extreme stop removal, say specifically with information I know about these sentences,

```python
jargon = ["python", "databricks", "cluster", "pyspark", "scala", 
          "answer", "question", "dataset", "map", "reduce", 
         "hadoop", "spark", "flume", "hive", "impala", "sparksql", "bigquery",
         "java", "build", "deploy", "ml", "models", "production"]

def talk_jargon_to_me(jargon, s):
    return " ".join([
      (x if x.lower() in jargon else "blah") 
      for x in s.split()])

only_jargon_sentences = [talk_jargon_to_me(jargon, x) for x in sentences]

results = []
for name, a_list in [
  ("original", sentences), ("nltk", stopped), ("nltk+spacy", stopped_both),
  ("only_jargon", only_jargon_sentences)
]:
    embeddings = ut.vec_to_embeddings(model_id, hf_token, a_list)
    results.append({"what": name, 
                    "one": cos_sim(embeddings[0, :], embeddings[1, :]),
                    "two": cos_sim(embeddings[0, :], embeddings[2, :]),
                   })
pd.DataFrame.from_records(results)

          what                 one                 two
0     original  [[tensor(0.2323)]]  [[tensor(0.2320)]]
1         nltk  [[tensor(0.3553)]]  [[tensor(0.2509)]]
2   nltk+spacy  [[tensor(0.3329)]]  [[tensor(0.2501)]]
3  only_jargon  [[tensor(0.3406)]]  [[tensor(0.5675)]]


```
09:36 Ok so sentence transformers can be a bit of a blunt tool for sure but I think I am verifying that with some pre-processing , I can get better use from them . And improving the jargon game can be helpful too.

One more thing out of curiosity,

```python
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
vocabulary = ut.vocabulary_of_model(model_id)
[(x, x in vocabulary) for x in ["spark", "pyspark", "python"]]
# [('spark', True), ('pyspark', False), ('python', True)]

[(x, tokenizer.tokenize(x)) for x in ["spark", "pyspark", "python"]]
```
```python
[('spark', ['spark']),
 ('pyspark', ['p', '##ys', '##park']),
 ('python', ['python'])]
```
```python
terms = ["spark", "pyspark", "python"]
embeddings = ut.vec_to_embeddings(model_id, hf_token, terms)
[
  ["spark, pyspark", cos_sim(embeddings[0, :], embeddings[1, :])], 
  ["spark, python", cos_sim(embeddings[0, :], embeddings[2, :])],
  ["pyspark, python", cos_sim(embeddings[1, :], embeddings[2, :])],
]
```
```python
[['spark, pyspark', tensor([[0.5201]])],
 ['spark, python', tensor([[0.2316]])],
 ['pyspark, python', tensor([[0.4150]])]]
```
09:47 might be worth poking at this a bit more, so if "pyspark" is not in the vocabulary here, but hmm maybe through all the fine tuning, on a billion sentences, maybe the embeddings still ended up being meaningfully close? Want to better understand this


### [[Jul 27th, 2023]] hmm what is the subword tokenization  multiple , when thinking about truncation

So it was cool to see you can get a better #[[cosine similarity]] score when taking out stop words and also when replacing the non-jargon words with blah words. Although that second part hmm might have actually artificially increased the score thre now that I think about it, 🤔

Maybe thinking about sentences is hmm not going to be as useful as thinking about the entire job description itself maybe.

So we have space only for 384 tokens but that can still be a good number of sentences, 10 mmaybe .
Ah yea and that is another good reason to get rid of the stop words
Like from my example from yesterday and day before, how many word-pieces in those?
```python
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

[{"num_words": len(x.split(" ")), "num_tokens": len(tokenizer.tokenize(x)), 
 "token_inflation_factor": len(tokenizer.tokenize(x))/len(x.split(" "))} 
 for x in [s1, s2, s3]]

[{'num_words': 34,
  'num_tokens': 46,
  'token_inflation_factor': 1.3529411764705883},
 {'num_words': 13,
  'num_tokens': 27,
  'token_inflation_factor': 2.076923076923077},
 {'num_words': 14,
  'num_tokens': 18,
  'token_inflation_factor': 1.2857142857142858}]

```
So yea if we have a 384 length input window then yea maybe 10 sentences or so on a good day. Not bad.
09:09 yea side note about that [[average-pooling]],

Reading the https://www.sbert.net/examples/applications/computing-embeddings/README.html section here again for insight.
This is a good page
Interesting looking at that `mean_pooling` function, it takes the attention mask into accoount. kinda cool,
### [[Jul 28th, 2023]] looking more closely on how sentence transformer model pools
ok thing I got it this time, per https://www.sbert.net/examples/applications/computing-embeddings/README.html

```python
In [109]: #Sentences we want sentence embeddings for
     ...: sentences = ['This framework generates embeddings for each input sentence',
     ...:              'Sentences are passed as a list of string.',
     ...:              'The quick brown fox jumps over the lazy dog.']
     ...: 
     ...: #Load AutoModel from huggingface model repository
     ...: tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
     ...: model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
     ...: 
     ...: #Tokenize sentences
     ...: encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt')
     ...: 
     ...: #Compute token embeddings
     ...: with torch.no_grad():
     ...:     model_output = model(**encoded_input)
     ...: 

Downloading (…)"pytorch_model.bin";: 100%|████████████████████████████████████████████████████████████████| 90.9M/90.9M [00:56<00:00, 1.61MB/s]
Downloading (…)"pytorch_model.bin";: 100%|████████████████████████████████████████████████████████████████| 90.9M/90.9M [00:56<00:00, 1.93MB/s]
In [110]: 
```
08:53 ok let's try to understand the function they show there,
So model_output, 
```python
In [123]: type(encoded_input)
Out[123]: transformers.tokenization_utils_base.BatchEncoding

In [124]: vars(encoded_input)
Out[124]: 
{'data': {'input_ids': tensor([[  101,  2023,  7705, 19421,  7861,  8270,  4667,  2015,  2005,  2169,
            7953,  6251,   102],
          [  101, 11746,  2024,  2979,  2004,  1037,  2862,  1997,  5164,  1012,
             102,     0,     0],
          [  101,  1996,  4248,  2829,  4419, 14523,  2058,  1996, 13971,  3899,
            1012,   102,     0]]),
  'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
  'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])},
 '_encodings': [Encoding(num_tokens=13, attributes=[ids, type_ids, tokens, offsets, attention_mask, special_tokens_mask, overflowing]),
  Encoding(num_tokens=13, attributes=[ids, type_ids, tokens, offsets, attention_mask, special_tokens_mask, overflowing]),
  Encoding(num_tokens=13, attributes=[ids, type_ids, tokens, offsets, attention_mask, special_tokens_mask, overflowing])],
 '_n_sequences': 1}
 
 ```
09:16 ok so looks somewhat close, to doing it manually, below,
```python
print("what was encoded,", encoded_input.data["input_ids"][0], )
print("back to tokens though,", tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0]))
print("original sentence,", sentences[0])
tokens = tokenizer.tokenize(sentences[0])
print("sentence to tokens", tokens)
print("tokens to ids", tokenizer.convert_tokens_to_ids(tokens))

```
```python
what was encoded, tensor([  101,  2023,  7705, 19421,  7861,  8270,  4667,  2015,  2005,  2169,
         7953,  6251,   102])
back to tokens though, ['[CLS]', 'this', 'framework', 'generates', 'em', '##bed', '##ding', '##s', 'for', 'each', 'input', 'sentence', '[SEP]']
original sentence, This framework generates embeddings for each input sentence
sentence to tokens ['this', 'framework', 'generates', 'em', '##bed', '##ding', '##s', 'for', 'each', 'input', 'sentence']
tokens to ids [2023, 7705, 19421, 7861, 8270, 4667, 2015, 2005, 2169, 7953, 6251]
```
Only difference is I see when going back from input ids to tokens , there is an additional `[CLS]` at the start and a `[SEP]` at the end.
no pad ?
```python
encoded_input_no_pad = tokenizer(sentences, padding=False, truncation=True, max_length=128, return_tensors='pt')
print("without pad, tokens, ", tokenizer.convert_ids_to_tokens(
    encoded_input_no_pad.data["input_ids"][0]))

ValueError: Unable to create tensor, you should probably activate truncation and/or padding with 'padding=True' 'truncation=True' to have batched tensors with the same length. Perhaps your features (`input_ids` in this case) have excessive nesting (inputs type `list` where type `int` is expected).

```
Ah ok so that doesn't even work then so padding required.
```python
([[{"num_words": len(x.split(" ")), 
    "len_tokens": len(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][i])),
    "len_input_ids": encoded_input.data["input_ids"][i,:].shape,
    "len_mask": encoded_input.data["attention_mask"][i,:].shape,
   }, x, 
   tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][i]),
   encoded_input.data["input_ids"][i,:], 
   encoded_input.data["attention_mask"][i,:]
  ] 
  for i, x in enumerate(sentences)])
```
```python
[[{'num_words': 8,
   'len_tokens': 13,
   'len_input_ids': torch.Size([13]),
   'len_mask': torch.Size([13])},
  'This framework generates embeddings for each input sentence',
  ['[CLS]',
   'this',
   'framework',
   'generates',
   'em',
   '##bed',
   '##ding',
   '##s',
   'for',
   'each',
   'input',
   'sentence',
   '[SEP]'],
  tensor([  101,  2023,  7705, 19421,  7861,  8270,  4667,  2015,  2005,  2169,
           7953,  6251,   102]),
  tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])],
 [{'num_words': 8,
   'len_tokens': 13,
   'len_input_ids': torch.Size([13]),
   'len_mask': torch.Size([13])},
  'Sentences are passed as a list of string.',
  ['[CLS]',
   'sentences',
   'are',
   'passed',
   'as',
   'a',
   'list',
   'of',
   'string',
   '.',
   '[SEP]',
   '[PAD]',
   '[PAD]'],
  tensor([  101, 11746,  2024,  2979,  2004,  1037,  2862,  1997,  5164,  1012,
            102,     0,     0]),
  tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])],
 [{'num_words': 9,
   'len_tokens': 13,
   'len_input_ids': torch.Size([13]),
   'len_mask': torch.Size([13])},
  'The quick brown fox jumps over the lazy dog.',
  ['[CLS]',
   'len_tokens': 13,
   'len_input_ids': torch.Size([13]),
   'len_mask': torch.Size([13])},
  'The quick brown fox jumps over the lazy dog.',
  ['[CLS]',
   'the',
   'quick',
   'brown',
   'fox',
   'jumps',
   'over',
  tensor([  101, 11746,  2024,  2979,  2004,  1037,  2862,  1997,  5164,  1012,
            102,     0,     0]),
  tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])],
 [{'num_words': 9,
   'len_tokens': 13,
   'len_input_ids': torch.Size([13]),
   'len_mask': torch.Size([13])},
  'The quick brown fox jumps over the lazy dog.',
  ['[CLS]',
   'the',
   'quick',
   'brown',
   'fox',
   'jumps',
   'over',
   'the',
   'lazy',
   'dog',
   '.',
   '[SEP]',
   '[PAD]'],
  tensor([  101,  1996,  4248,  2829,  4419, 14523,  2058,  1996, 13971,  3899,
           1012,   102,     0]),
  tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0])]]


```
09:36 ah interesting so the `[PAD]` is separate actually, and that corresponds to the additional `0` in the [[attention-mask]]          


### [[Jul 29th, 2023]] hmm
so back to that cool document, https://www.sbert.net/examples/applications/computing-embeddings/README.html

it was cool I saw you can easily do `tokenizer.convert_ids_to_tokens` and `tokenizer.convert_tokens_to_ids`, because I was able to veriffy that running
```python
encoded_input = tokenizer(
  sentences, padding=True, truncation=True, return_tensors='pt')
```
will add some additional `'[CLS]'` and `'[SEP]'` tokens at the beginning and end. I noticed since the length of the output was weird especially looking at the [[attention-mask]] . So that attention mask basically was showing that the three sentences being encoded had a final length that was the same number of ids and tokens , both 13, but there were some 0s at the end of some of the sentences. So that ended up being just yet another `[PAD]` token.
Ok so `'[CLS]` means special #BERT token for start of sequence and `[SEP]` is the separator  between sequences . Yea and `[PAD]` just says, nothing to do here.
And the `padding=True` option is not about padding up to like [[context-window]] limit, it just says if you are passing multiple sentences to be encoded, to make them all equal length.
Anyway `384` is the size of the embedding, in this case, and it is not yet clear to me what is the [[what is relationship between size of input token sequence and dimension of embedding]] , there might be some [[dimensionality reduction]] right.
12:58 so continuing along then, next step was
```python
#Compute token embeddings
with torch.no_grad():
    model_output = model(**encoded_input)
    
In [143]: vars(model_output)
Out[143]: 
{'last_hidden_state': tensor([[[ 0.2913, -0.2685, -0.2250,  ...,  0.4261,  0.0493, -0.2095],
          [-0.6272, -0.0421, -0.2452,  ...,  0.5336,  1.3115,  0.5999],
          [ 0.0023, -0.2805, -0.4198,  ..., -0.2900,  1.5808, -0.4912],
          ...,
          [ 0.1802, -0.5567,  0.0146,  ...,  0.9311,  0.5940, -0.3536],
          [ 0.0603, -0.2502,  0.5959,  ...,  0.9435,  0.9465, -1.0680],
          [-0.3356,  0.0650,  0.1109,  ...,  1.0801,  0.2653, -0.2762]],
 
         [[ 0.0856,  0.1876,  0.0488,  ...,  0.1204, -0.0907, -0.1662],
          [ 0.1291, -0.0266,  0.6318,  ...,  0.7958,  0.1555, -1.2737],
          [ 0.0062,  0.2263,  0.1851,  ...,  0.3981,  0.6461, -0.2192],
          ...,
          [ 0.3036,  0.3740,  0.2523,  ...,  0.6319,  0.5731, -0.2901],
          [-0.2124,  0.2626,  0.6867,  ...,  0.5504,  0.7065, -0.4728],
          [-0.2220,  0.2086,  0.6693,  ...,  0.5410,  0.5683, -0.3963]],
 
         [[ 0.0464,  0.3381,  0.2082,  ...,  0.2766, -0.0861, -0.0358],
          [ 0.1162,  0.2264,  0.1021,  ...,  0.1858,  0.4895,  1.2175],
          [ 0.1537,  0.1730,  0.5151,  ...,  1.3720,  0.3621,  0.5758],
          ...,
          [ 0.3883,  0.2813,  0.0309,  ...,  0.3264, -0.1039,  0.5856],
          [ 0.3477,  0.0940,  0.2564,  ...,  0.1463,  0.1743,  0.5586],
          [ 0.1911, -0.0142,  0.3021,  ...,  0.1814,  0.2111,  0.2329]]]),
 'pooler_output': tensor([[-0.0417, -0.0041,  0.0332,  ...,  0.0117, -0.0634, -0.0058],
         [-0.0227, -0.0248, -0.0112,  ...,  0.0482, -0.1108,  0.0122],
         [-0.0663,  0.0281,  0.0706,  ...,  0.0258, -0.0222, -0.0608]]),
 'hidden_states': None,
 'past_key_values': None,
 'attentions': None,
 'cross_attentions': None}
```
Ok cool, so seeing each input is embedded separately, we have size of 3 rows here, like 3 input encodings , 
```python
In [146]: [model_output.last_hidden_state.shape, model_output.pooler_output.shape]
Out[146]: [torch.Size([3, 13, 384]), torch.Size([3, 384])]

```
Hmm and last hidden state, with the 13 wonder if those are 13 [[attention-head]] ? And then the `pooler_output` what combines these then ?
13:29 oh never mind #moment/doh #moment/duh that is 13 because thre are 13 tokens in each sentence ! [[moment/haha]] . 😀

13:14 ok so final [[average-pooling]] mean pooling step
```python
#Perform pooling. In this case, mean pooling
sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
```
Ok so you can use key or index to access these, 
```python
In [155]: np.allclose(model_output.last_hidden_state, model_output[0]), np.allclose(model_output.pooler_output, model_output[1])
Out[155]: (True, True)
```

13:24 Not yet clear why this additional unsqueeze [[numpy unsqueeze ]] step is done 
```python
In [163]: attention_mask = encoded_input['attention_mask']
     ...: attention_mask.shape, attention_mask.unsqueeze(-1).shape
Out[163]: (torch.Size([3, 13]), torch.Size([3, 13, 1]))


```
Ah ok interesting,
```python
In [166]: token_embeddings = model_output[0]

In [167]:     input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

In [168]: input_mask_expanded
Out[168]: 
tensor([[[1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         ...,
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.]],

        [[1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         ...,
         [1., 1., 1.,  ..., 1., 1., 1.],
         [0., 0., 0.,  ..., 0., 0., 0.],
         [0., 0., 0.,  ..., 0., 0., 0.]],


        [[1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         ...,
         [1., 1., 1.,  ..., 1., 1., 1.],
         [1., 1., 1.,  ..., 1., 1., 1.],
         [0., 0., 0.,  ..., 0., 0., 0.]]])

In [169]: input_mask_expanded.shape
Out[169]: torch.Size([3, 13, 384])

In [170]: (token_embeddings.size())
Out[170]: torch.Size([3, 13, 384])

In [171]: input_mask_expanded[0,0,:]
Out[171]: 
tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1., 1.,
        1., 1., 1., 1., 1., 1.])

```
So this interesting unsqueeze then expand pattern , to the 384 size of the embedding dimension,
13:30 so yea literally the output is
```python
In [172]: token_embeddings.shape
Out[172]: torch.Size([3, 13, 384])

In [173]: token_embeddings
Out[173]: 
tensor([[[ 0.2913, -0.2685, -0.2250,  ...,  0.4261,  0.0493, -0.2095],
         [-0.6272, -0.0421, -0.2452,  ...,  0.5336,  1.3115,  0.5999],
         [ 0.0023, -0.2805, -0.4198,  ..., -0.2900,  1.5808, -0.4912],
         ...,
         [ 0.1802, -0.5567,  0.0146,  ...,  0.9311,  0.5940, -0.3536],
         [ 0.0603, -0.2502,  0.5959,  ...,  0.9435,  0.9465, -1.0680],
         [-0.3356,  0.0650,  0.1109,  ...,  1.0801,  0.2653, -0.2762]],

        [[ 0.0856,  0.1876,  0.0488,  ...,  0.1204, -0.0907, -0.1662],
         [ 0.1291, -0.0266,  0.6318,  ...,  0.7958,  0.1555, -1.2737],
         [ 0.0062,  0.2263,  0.1851,  ...,  0.3981,  0.6461, -0.2192],
         ...,
         [ 0.3036,  0.3740,  0.2523,  ...,  0.6319,  0.5731, -0.2901],
         [-0.2124,  0.2626,  0.6867,  ...,  0.5504,  0.7065, -0.4728],
         [-0.2220,  0.2086,  0.6693,  ...,  0.5410,  0.5683, -0.3963]],

        [[ 0.0464,  0.3381,  0.2082,  ...,  0.2766, -0.0861, -0.0358],
         [ 0.1162,  0.2264,  0.1021,  ...,  0.1858,  0.4895,  1.2175],
         [ 0.1537,  0.1730,  0.5151,  ...,  1.3720,  0.3621,  0.5758],
         ...,
         [ 0.3883,  0.2813,  0.0309,  ...,  0.3264, -0.1039,  0.5856],
         [ 0.3477,  0.0940,  0.2564,  ...,  0.1463,  0.1743,  0.5586],
         [ 0.1911, -0.0142,  0.3021,  ...,  0.1814,  0.2111,  0.2329]]])
```
at does the model_output.pooler_output mean then? Is that also doing a average of the 13 tokens?
13:33 The final step makes a bit more sense now 
```python
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
```
because it is just saying, dont take into account the stuff that the mask masked away. 
And we add them, and divide by length for each sentence, 
```python
In [178]:     sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
     ...:     sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)

In [179]: pooled = sum_embeddings / sum_mask

In [180]: pooled.shape
Out[180]: torch.Size([3, 384])
```
too of course.
16:34 Ok so since I now basically know, the [[average-pooling]] of [[sentence-transformers]] indeed is just literally averaging each word, yes in the 384 dimensions but yea any unimportant word should most certainly be removed before average pooling

And I still have that pretty critical two-part question, so if we are using [[subword-tokenization]] , and  therefore a concept is going to be spread apart to multiple tokens, does that mean we are relying on this multi-dimensional averaging to somehow maintain the meaning of a word that was broken up into pieces?
So the [[subword-tokenization]]  clearly I now understand is a statistical procedure unrelated to the #[[supervised fine-tuning]] step and yea likely that the more common sub-words will end up being longer subwords after [[why a custom tokenizer]] , but most likely a concept still gets broken apart, into multiple sub-words, so then ultimately does that not really matter, because upon computing [[cosine similarity]], another sentence which has the same exact [[jargon]] word will be split up in the same way.
And maybe even if a model is not #[[supervised fine-tuning]] with a new corpus, we may still benefit from at least words with a common word parts being close dimensionally, right,
18:20 hmm so a dead super simple test, of above sub-word theory,

```python
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
sentences = [
    "python",
    "pyspark",
]
embeddings = ut.vec_to_embeddings(model_id, sentences)

In [189]: cos_sim(embeddings[0, :], embeddings[1,:])
Out[189]: tensor([[0.4150]])
```
Ok kind of thought so.
18:47 added one more option for myself there,

```python
reload(ut)
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
sentences = [
    "python",
    "pyspark",
]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
```
```python
['[CLS]', 'python', '[SEP]', '[PAD]', '[PAD]']
['[CLS]', 'p', '##ys', '##park', '[SEP]']
```
That's terrible haha ok no wonder the cosine similarity is so low, `0.415` haha.
18:51 one more example to try, hmm, this one should be obvious ,

```python
sentences = ["postgresql", "database"]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

['[CLS]', 'post', '##gre', '##s', '##q', '##l', '[SEP]']
['[CLS]', 'database', '[SEP]', '[PAD]', '[PAD]', '[PAD]', '[PAD]']
cosine similarity tensor([[0.5301]])
```
hmm haha thats really bad I think
One more
```python
sentences = ["postgresql", "sql"]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

['[CLS]', 'post', '##gre', '##s', '##q', '##l', '[SEP]']
['[CLS]', 'sql', '[SEP]', '[PAD]', '[PAD]', '[PAD]', '[PAD]']
cosine similarity tensor([[0.5085]])
```
hmm yea this is no good. Whatever this is, it is terrible I think
It should be as good as this, 
```python
In [200]: sentences = ["banana", "apple"]
     ...: encoded_input, embeddings = ut.vec_to_embeddings(
     ...:     model_id, sentences, return_tokenizer_output=True)
     ...: tokenizer = AutoTokenizer.from_pretrained(model_id)
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
     ...: print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))
     ...: 
['[CLS]', 'banana', '[SEP]']
['[CLS]', 'apple', '[SEP]']
cosine similarity tensor([[0.4240]])

In [201]: sentences = ["fruit", "apple"]
     ...: encoded_input, embeddings = ut.vec_to_embeddings(
     ...:     model_id, sentences, return_tokenizer_output=True)
     ...: tokenizer = AutoTokenizer.from_pretrained(model_id)
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
     ...: print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))
['[CLS]', 'fruit', '[SEP]']
['[CLS]', 'apple', '[SEP]']
cosine similarity tensor([[0.5372]])

In [202]: 

In [202]: sentences = ["macintosh", "apple"]
     ...: encoded_input, embeddings = ut.vec_to_embeddings(
     ...:     model_id, sentences, return_tokenizer_output=True)
     ...: tokenizer = AutoTokenizer.from_pretrained(model_id)
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
     ...: print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))
['[CLS]', 'macintosh', '[SEP]']
['[CLS]', 'apple', '[SEP]']
cosine similarity tensor([[0.7044]])


```
18:57 ok haha I'm confused. these are also kind of bad.


### [[Jul 31st, 2023]] ok interesting, removing the special tokens has no effect on the cosine similarity
so following from [[Jul 29th, 2023]] I was going to remove the special tokens try again,

```python
texts = ["macintosh", "apple"]
encoded_input = tokenizer(
    texts, padding=True, truncation=True, max_length=128, 
    cls_token=None,
    sep_token=None,
    return_tensors='pt')

```
hmm that didn't work, 
```python
TypeError: _batch_encode_plus() got an unexpected keyword argument 'cls_token'

```
how about,
```python

texts = ["macintosh", "apple"]
encoded_input = tokenizer(
    texts, padding=True, truncation=True, max_length=128, 
    add_special_tokens=False,
    return_tensors='pt')
```
09:14 ok nice yes that did it !
```python
In [206]: encoded_input
Out[206]: 
{'input_ids': tensor([[22228],
        [ 6207]]), 'token_type_ids': tensor([[0],
        [0]]), 'attention_mask': tensor([[1],
        [1]])}
```
Let's then compare cosine similarity between these, with and without the special tokens present.
```python
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

cosine similarity tensor([[0.7044]])
```
09:27 ok looks like didn't make a difference. Try one more, 
```python
sentences = ["fruit", "apple"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

for add_special_tokens in [True, False]:
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, 
        add_special_tokens=add_special_tokens,
        return_tensors='pt')

    embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
    print("add_special_tokens:", add_special_tokens, "cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

    
add_special_tokens: True cosine similarity tensor([[0.2258]])
add_special_tokens: False cosine similarity tensor([[1.0000]])
```
09:34 oops, have some kind of bug in the mean pooling code I think.
### [[Aug 1st, 2023]] trying a few more things wondering why weird cosine similarity 1 w/ single words encoded but different words
ok what is bug from yesterday then ?

```python
sentences = ["fruit", "apple"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

for add_special_tokens in [True, False]:
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, 
        add_special_tokens=add_special_tokens,
        return_tensors='pt')

    embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
    print("add_special_tokens:", add_special_tokens, "cosine similarity", 
          cos_sim(embeddings[0, :], embeddings[1,:]))
    print("all close", np.allclose(embeddings[0, :], embeddings[1,:]))
    
```
```python
add_special_tokens: True cosine similarity tensor([[0.5372]])
all close False
add_special_tokens: False cosine similarity tensor([[1.0000]])
all close False

In [217]: embeddings.shape
Out[217]: torch.Size([2, 384])
```
hmm weird, yea spot checked, they don't look identical actually, but similar, 
```python
In [218]: np.transpose(embeddings).shape
Out[218]: torch.Size([384, 2])

In [219]: np.transpose(embeddings)[:5]
Out[219]: 
tensor([[ 0.0025,  0.0021],
        [ 0.0335,  0.0337],
        [ 0.0014,  0.0013],
        [-0.0084, -0.0081],
        [-0.0206, -0.0208]])

n [220]: np.transpose(embeddings)[-5:]
Out[220]: 
tensor([[ 0.0678,  0.0675],
        [ 0.1426,  0.1423],
        [-0.0018, -0.0016],
        [-0.1755, -0.1752],
        [-0.0967, -0.0969]])
```
but it is for sure a bug since, this happens for absurd cases,
```python
sentences = ["fruit", "couch"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

for add_special_tokens in [True, False]:
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, 
        add_special_tokens=add_special_tokens,
        return_tensors='pt')

    embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
    print("add_special_tokens:", add_special_tokens, "cosine similarity", 
          cos_sim(embeddings[0, :], embeddings[1,:]))
    print("all close", np.allclose(embeddings[0, :], embeddings[1,:]))
    
```
```python
add_special_tokens: True cosine similarity tensor([[0.2795]])
all close False
add_special_tokens: False cosine similarity tensor([[1.0000]])
all close False
```
pdb trace, 
```python
In [224]: ipdb.runcall(ut.encoded_to_embeddings, encoded_input, model_id)

ipdb> p encoded_input
{'input_ids': tensor([[5909],
        [6411]]), 'token_type_ids': tensor([[0],
        [0]]), 'attention_mask': tensor([[1],
        [1]])}
  
ipdb> p model_output.last_hidden_state.shape, model_output.pooler_output.shape
(torch.Size([2, 1, 384]), torch.Size([2, 384]))

cos_sim(model_output.last_hidden_state[0,:,:], model_output.last_hidden_state[1,:,:])
tensor([[1.0000]])

cos_sim(model_output.pooler_output[0, :], model_output.pooler_output[1, :])
tensor([[1.0000]])

np.allclose(model_output.pooler_output[0, :], model_output.pooler_output[1, :])
False
```
weird ok so this happens before the `mean_pooling` func gets called. weird.
```python
sentences = ["the fruit is edible", "this couch is on sale"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

for add_special_tokens in [True, False]:
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, 
        add_special_tokens=add_special_tokens,
        return_tensors='pt')

    embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
    print("add_special_tokens:", add_special_tokens, "cosine similarity", 
          cos_sim(embeddings[0, :], embeddings[1,:]))
    print("all close", np.allclose(embeddings[0, :], embeddings[1,:]))
    
add_special_tokens: True cosine similarity tensor([[0.0687]])
all close False
add_special_tokens: False cosine similarity tensor([[0.0756]])
all close False
```
ok so then something weird going on w/ a single token hmm?
```python
sentences = ["there is fruit on the table", "look at the table there is fruit"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

for add_special_tokens in [True, False]:
    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, max_length=128, 
        add_special_tokens=add_special_tokens,
        return_tensors='pt')

    embeddings = ut.encoded_to_embeddings(encoded_input, model_id)
    print("add_special_tokens:", add_special_tokens, "cosine similarity", 
          cos_sim(embeddings[0, :], embeddings[1,:]))
    print("all close", np.allclose(embeddings[0, :], embeddings[1,:]))
    
add_special_tokens: True cosine similarity tensor([[0.9155]])
all close False
add_special_tokens: False cosine similarity tensor([[0.9066]])
all close False


```
09:34 dont know why the output from the model produces nearly same embedding, for a single word encoded, but multiple words, it seems to be working fine.
guess more multi-word experiments then next .

### [[Aug 2nd, 2023]] interesting attempts around single and multiword embeddings
Since like I saw yesterday, I can get high `0.90s` score if I have a longer sentence, and for a single word, there is some kind of weird bug

So for just `["fruit", "apple"]` I had 
```python
sentences = ["fruit", "apple"]
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
embeddings = ut.vec_to_embeddings(model_id, sentences)
cos_sim(embeddings[0, :], embeddings[1,:])
```
```python
In [229]: sentences = ["fruit", "apple"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
     ...: 
Out[229]: tensor([[0.5372]])

In [230]: sentences = ["a fruit", "my apple"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[230]: tensor([[0.4532]])

In [231]: sentences = ["its some fruit", "here my apple"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[231]: tensor([[0.3700]])

In [232]: sentences = ["its some fruit juice", "here my apple sauce"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[232]: tensor([[0.4277]])

In [233]: sentences = ["its some fruit juice home made", "here my apple sauce custom recipe"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[233]: tensor([[0.3862]])
```
Ok I don't know haha, might not solve this mystery right now.
It might also be that hmm not all words are as close together as I thought?
09:05 ok yea haha, indeed I found some better single-word examples. 
```python
In [234]: sentences = ["couch", "sofa"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[234]: tensor([[0.8564]])

In [235]: sentences = ["hammock", "bed"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[235]: tensor([[0.2903]])

In [236]: sentences = ["mattress", "bed"]
     ...: model_id =  "sentence-transformers/all-MiniLM-L6-v2"
     ...: embeddings = ut.vec_to_embeddings(model_id, sentences)
     ...: cos_sim(embeddings[0, :], embeddings[1,:])
Out[236]: tensor([[0.6860]])
```
So yea putting the single-word-bug theory to rest, at least when using CLS, SEP `add_special_tokens=True` there is no problem. And without CLS, SEP, using `add_special_tokens=False` then yea, the embeddings for both inputs are nearly the same producing cosine similarity of 1. That's really weird. So I should stick to using `add_special_tokens=True` for now at least for this model.
Ok back to big picture then,

So I have observed this model has bad performance when I try throwing technical [[jargon]] at it,
collapsed:: true
```python
reload(ut)
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
sentences = [
    "python",
    "pyspark",
]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
```
```python
['[CLS]', 'python', '[SEP]', '[PAD]', '[PAD]']
['[CLS]', 'p', '##ys', '##park', '[SEP]']
```
```python
sentences = ["postgresql", "database"]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

['[CLS]', 'post', '##gre', '##s', '##q', '##l', '[SEP]']
['[CLS]', 'database', '[SEP]', '[PAD]', '[PAD]', '[PAD]', '[PAD]']
cosine similarity tensor([[0.5301]])
```
```python
sentences = ["postgresql", "sql"]
encoded_input, embeddings = ut.vec_to_embeddings(
    model_id, sentences, return_tokenizer_output=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
print("cosine similarity", cos_sim(embeddings[0, :], embeddings[1,:]))

['[CLS]', 'post', '##gre', '##s', '##q', '##l', '[SEP]']
['[CLS]', 'sql', '[SEP]', '[PAD]', '[PAD]', '[PAD]', '[PAD]']
cosine similarity tensor([[0.5085]])
```
I have tried building a tokenizer from this model's tokenizer, but that was problematic because it is not tokenizer fine tuning like model fine tuning, it just uses the same class.
collapsed:: true
So initially I was thinking building a new tokenizer means I need all billion examples earlier, hmm but that's just what went in to fine tuning the model. Maybe for a tokenizer, perhaps I just need to build a dataset that has a good sampling mix of English language and a healthy proportion of technical language.
But I think before doing that, I would like to take another stab at understanding, how to answer the more general question, about [[subword-tokenization]] , so for non jargon language, any tokenizer will still end up having plenty of subwords, but they will still end up with good embeddings right? So since subwords are split up into multiple embeddings, then maybe is it that the model just associates those subword embeddings appropriately then? So is it like you identify that multi-syllable words have the same #etymology roots perhaps, like
like, "charismatic" , "charisma" and "character" and "characterization" ,
```python
In [242]: sentences = [
     ...:     "charismatic" , "charisma", "character", "characterization"
     ...: ]

In [243]: encoded_input, embeddings = ut.vec_to_embeddings(
     ...:     model_id, sentences, return_tokenizer_output=True)
     ...: tokenizer = AutoTokenizer.from_pretrained(model_id)
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][0, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][1, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][2, :]))
     ...: print(tokenizer.convert_ids_to_tokens(encoded_input.data["input_ids"][3, :]))
     ...: 
['[CLS]', 'charismatic', '[SEP]', '[PAD]', '[PAD]']
['[CLS]', 'char', '##ism', '##a', '[SEP]']
['[CLS]', 'character', '[SEP]', '[PAD]', '[PAD]']
['[CLS]', 'characterization', '[SEP]', '[PAD]', '[PAD]']

In [244]: cos_sim(embeddings[0, :], embeddings[1,:])
Out[244]: tensor([[0.5882]])

In [245]: cos_sim(embeddings[0, :], embeddings[2,:])
Out[245]: tensor([[0.4623]])

In [246]: cos_sim(embeddings[1, :], embeddings[2,:])
Out[246]: tensor([[0.6060]])


```
yea maybe something like that happens with an embedding model then, it can still embed subwords well. Should try to do some reading on this .


### [[Aug 3rd, 2023]] trying to do some more research on subword tokenization embedding
#### are sub word token embeddings meaningful? 
Don't have a definitive answer yet , but played around with the idea
So what I wrote down yesterday, let's try to phrase this question , how do subword embedding models capture meaning of concepts that are broken up into parts? [[are sub word token embeddings meaningful?]]

collapsed:: true
so any tokenizer that uses [[subword-tokenization]], has the benefit of representing a large vocabulary with a subword vocabulary taht is smaller. Not remembering precisely but there are computational benefits to a smaller  [[vocabulary size]] . But also with [[byte-pair encoding]] and similar algos, you have fewer [[out-of-vocabulary-words-OOV]] , and that is important since that can have performance degradations, an embedding model literally doesn't know what those inputs mean. 
collapsed:: true
Other benefits of course are it is more resilient to #misspelling , #typographical-error
Related question is probably, [[Named Entity Recognition NER]] , [[Named Entity Recognition NER/how does it work across sub word tokenization]]
Well realized it is build for this since entities are already often defined across multiple words, so multiple sub-words doesn't sound like a huge stretch .
12:49 I'm reading the [[book/Natural Language Processing with Transformers]] chapter 4 , skimming,
collapsed:: true
one note I had from earlier, building a dataset in this chapter they chose representative sampling by percent data about languages spoken in #switzerland . Kind of cool
Cool how on page 89, there is a custom dataset created based on the proportion of languages that are in #switzerland , in this case ,

```python
langs = ["de", "fr", "it", "en"]
fracs = [0.629, 0.229, 0.084, 0.059]

```
So I can borrow above technique if I would need a dataset that is more jargon heavy.
13:28 hmm but a note on [[why a custom tokenizer]] ,
collapsed:: true
reading on page 35 in [[book/Natural Language Processing with Transformers]] , they are stressing, to use same tokenizer a model was trained with, so yea when creating a new tokenizer, therefore a new model is necessary too, otherwise the token id mappings will be completely off .

13:38 ultimately, maybe [[are sub word token embeddings meaningful?]]

collapsed:: true
maybe answer is yes if the [[average-pooling]] of the embeddings of those sub words is meaningful, which is precisely what that `mean_pooling` function of the [[sentence-transformers]] is doing. uniformly averages all the embeddings. So yea I wouldn't be surprised if meaning did have a chance of getting a bit lost.
#### Some more reading
14:24 I do want to continue reading some of the tokenizer sections in that book, but let me try to some quick research first.

collapsed:: true
[[hugging face Datasets]] , a custom dataset, hmm so warming up to this ,
reading [here](https://huggingface.co/learn/nlp-course/chapter5/4?fw=pt), for use on a laptop, they support streaming operations, yay so don't have to be a huge memory burden . Nice, they use [[memory mapped file]], wow, so can have like unlimited size then hmm , like magic
15:22 ok stumbled on [link](https://huggingface.co/learn/nlp-course/chapter5/6?fw=pt) this section of the [[hugging face]] nlp course , on  [[semantic search]],
covering [[average-pooling]] yea. But also [[faiss.ai]] which is the [[Facebook AI Similarity Search FAISS]] which maybe is an alternative library to [[sentence-transformers]]?
collapsed:: true
15:30 hmm [article link](https://towardsdatascience.com/master-semantic-search-at-scale-index-millions-of-documents-with-lightning-fast-inference-times-fa395e4efd88) someone hinting that [[Facebook AI Similarity Search FAISS]] is more about indexing and [[sentence-transformers]] more about the embeddings themselves perhaps.
So faster lookup, faster search,
15:48 ok what can I learn here then
Really not sure though why they are not concerned about removing the [[stop-words]] since they pollute that average .
Think I will steal their nice technique for more quickly visualizing similarity though, 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1691092410135_0.png" width="50%">}}
In video at head of the page , presenter here, characterizes `0.83` as a strong relationship between these sentences.
17:15 I had a sentence here wrote on #ipad but #[[logseq sync]] deleted it [[moment/grr]] [[data loss]]. I wrote that [[hugging face Datasets]] seems to be a #pandas alternative since it has filtering , has maps, and especially w/ the [[memory mapped file]] would be way better than a memory bound pandas dataframe
17:17 seeing a note that the [[symmetric vs asymmetric semantic search]] idea is being discussed here,  
```python
model_ckpt = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
```
but honestly I thought since now I know it is all just [[average-pooling]] then what's the point?
17:35 in any case this article uses a new kind of pooling , cls pooling, maybe worth seeing if that is better than average pooling?
```python
def cls_pooling(model_output):
    return model_output.last_hidden_state[:, 0]
```

When I look at this function though, does not make sense because it is just returning the embedding of the `[CLS]` token, isn't that weird? Wouldn't that be the same vector each time, for the `[CLS]` token?
Ok, try this, so for a bunch of sentences, let's just compare the cosine similarity between the two pooling methods, out of curiosity,
```python
sentences = [
    "postgresql",
    "pyspark",
    "this couch is for sale",
    "docker",
    "kubernetes",
    "tensorflow",
    "pytorch",
]
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# for sentence in sentences:
encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors='pt')

with torch.no_grad():
    model_output = model(**encoded_input)
    
[model_output.last_hidden_state.shape, model_output.pooler_output.shape]
```
```python
[torch.Size([7, 7, 384]), torch.Size([7, 384])]
```
```python
sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

sentence_embeddings.shape
# torch.Size([7, 384])

cls_pooled = ut.cls_pooling(model_output)

cls_pooled.shape
# torch.Size([7, 384])
```
```python
extract_scalar = lambda x: round(float(x[0][0]), 3)
for i, _ in enumerate(sentence_embeddings):
    print(sentences[i], 
          "cos_sim,",
          extract_scalar(cos_sim(sentence_embeddings[i, :], cls_pooled[i, :])),
          extract_scalar(cos_sim(sentence_embeddings[i, :], model_output.pooler_output[i, :])),
          extract_scalar(cos_sim(cls_pooled[i, :], model_output.pooler_output[i, :])),
    )  
```
```python
postgresql cos_sim, 0.581 0.008 -0.02
pyspark cos_sim, 0.63 0.04 -0.008
this couch is for sale cos_sim, 0.572 -0.041 -0.044
docker cos_sim, 0.686 0.018 -0.066
kubernetes cos_sim, 0.594 -0.068 -0.042
tensorflow cos_sim, 0.563 0.068 -0.016
pytorch cos_sim, 0.567 0.022 0.017
```
Ok yea so this cls pooling approach, there is some similarity to the average pooling. interesting. But haha the final `model_output.pooler_output`, yea that is unrelated to anything even though the dimension is the same. Wonder what that is, haha.





#### thoughts on a custom dataset
16:09 building my own custom dataset, for the [[supervised fine-tuning]] and for the measuring , can really be the same dataset,

Just train a test split, so build the [[positive pair]] with lots and lots of organic sentences , that use jargon, yea maybe using the cluster approach I was thinking about earlier, clustering by similar job titles, and maybe at some point  I can mix in [[positive pair]] constructed along with my own personal examples.
### [[Aug 4th, 2023]] reading and musing some more on meaning or no meaning with fertile sub-wording tokenization
[[are sub word token embeddings meaningful?]]

So thinking in context of [[Named Entity Recognition NER/how does it work across sub word tokenization]], I think it is the core #BERT #[[NLP Transformers]] model that is build for understanding #[[input sequence]] and so probably it picks up some cues about multi-token sequences that are entities. But [[sentence-transformers]] is a [[bag-of-words]] so yea it is not tuning anything here right?
Because reading , [[book/Natural Language Processing with Transformers]] page 97 , my notes I underlined that yea the [[Named Entity Recognition NER]] task is a [[token classification task]]
Wait but then what is happening in the [[article/Train and Fine-Tune Sentence Transformers Models]] ?
Yea also reading , page 313, that yes there are metrics specific to tokenizers like [[subword fertility]] which measures average number of subwords coming out of  [[subword-tokenization]], but that these are like [[end-to-end-vs-proxy-ML-training]] proxy metrics and instead [[end to end test]] of performance is best. Most direct .
Hmm so perhaps yea my focus on things like [[cosine similarity]] is good since it is an end to end measure, but it gives me more reason to build that nice dataset of my own 😀 , [[moment/anticipation]] , [[moment/curiosity]] ,
09:29 so yea think would be a useful next mini thing to look at, per [link](https://huggingface.co/blog/how-to-train-sentence-transformers), [[article/Train and Fine-Tune Sentence Transformers Models]], is this fine tuning changing weights actually, somehow helping to build associations around the tokens regardless of whether they are haha highly fertile and possibly meaningless looking [[subword-tokenization]] ? haha
Yea and should continue to build out my dataset [[positive pair]] , aspiration, to train test, build and measure !
### [[Aug 6th, 2023]] debugging does fine tuning update model weights?
Looks like yes. But a small dataset appears to minimally update weights, which makes sense.
10:06 yea so question from last time, [[article/Train and Fine-Tune Sentence Transformers Models]], what is this actually changing?

So earlier I tried this, on [[Jul 15th, 2023]] , [here](https://michal.piekarczyk.xyz/post/2023-06-18-my-projects-langchain-interview-me-2023-feb/#jul-15th-2023-finally-tried-the-supervised-fine-tuning-but-didnt-seem-to-add-to-the-vocabulary), with this `data/kaggle-google-job-skills/2023-07-15-positive-pairs.jsonl` mini first stab at a dataset w/ [[positive pair]],
collapsed:: true
But the only thing I did as a test was that I inspected whether the internal "vocab.txt" [[vocabulary]] had changed before and after and it did not. However I know better now that this #[[supervised fine-tuning]] does not change the vocabulary since that is fixed in the #tokenizer .
So instead, I should have checked, did the weights of the model change and I could have run some #[[cosine similarity]] tests to spot check or also to actually have a #holdout-set , built from my data, to see did the sentences I would have expected get ranked better than before the fine tuning ?
11:12 ok so let me do that one more time and lets check , of all the layers I see in this model, at least the before and after weights of the pooling layer,
```python
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

print("how many layers: ", len([x for x in model.modules()]))
how many layers:  120

```
120 layers, oh my, ok lets look at pooler at end, 
```python
[x for x in model.modules()][-5:]
# Out[299]: 
[LayerNorm((384,), eps=1e-12, elementwise_affine=True),
 Dropout(p=0.1, inplace=False),
 BertPooler(
   (dense): Linear(in_features=384, out_features=384, bias=True)
   (activation): Tanh()
 ),
 Linear(in_features=384, out_features=384, bias=True),
 Tanh()]


pooler = [x for x in model.modules()][-3]
pooler.dense.weight.shape, pooler.dense.bias.shape
# Out[309]: (torch.Size([384, 384]), torch.Size([384]))
```
Ok let me make a deep copy of that, and lets see if that changes w/ my mini mini dataset fine tuning,
```python
weights_before, bias_before = deepcopy(pooler.dense.weight), deepcopy(pooler.dense.bias)
In [312]: weights_before[:, :5]
Out[312]: 
tensor([[-0.0151, -0.0224, -0.0046, -0.0199,  0.0064],
        [ 0.0083, -0.0186, -0.0132, -0.0009, -0.0157],
        [-0.0030,  0.0108, -0.0102,  0.0023, -0.0006],
        ...,
        [-0.0049, -0.0010, -0.0043, -0.0035,  0.0108],
        [-0.0089,  0.0108,  0.0011,  0.0227, -0.0051],
        [ 0.0049,  0.0070, -0.0065, -0.0034,  0.0024]],
       grad_fn=<SliceBackward0>)

In [314]: bias_before[:5]
Out[314]: tensor([0., 0., 0., 0., 0.], grad_fn=<SliceBackward0>)
```
ok
```python
import os
import utils as u
from pathlib import Path

path = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/2023-07-15-positive-pairs.jsonl")

# path.write_text("\n".join([json.dumps(x) for x in dataset]))

dataset = [json.loads(x) for x in path.read_text().splitlines()]

dataset[:4]
# Out[319]: 
# [{'set': ['programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
#    'experience with java, javascript, html5, and sap technologies like sap hana, sap fiori, netweaver']},
#  {'set': ['programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
#    'software development platforms and solutions experience (java servlets, javascript, php, asp, cgi, ajax, flash, cookies and xml)']},
#  {'set': ['programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
#    'experience with front-end web technologies (html5, css3, and javascript)']},
#  {'set': ['programming experience in one or more of the following: java, python, javascript, nodejs, c#, net, ruby',
#    'html5, css3, and javascript development experience']}]


from sentence_transformers import InputExample
from torch.utils.data import DataLoader

train_examples = []
for i, x in enumerate(dataset):
    train_examples.append(
        InputExample(texts=[x["set"][0], x["set"][1]])
    )
train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)

# MultipleNegativesRankingLoss 
from sentence_transformers import losses

model = SentenceTransformer('all-MiniLM-L6-v2')
train_loss = losses.MultipleNegativesRankingLoss(model=model)


model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=10) 
```
```python
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:14<00:00,  1.09s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:16<00:00,  1.23s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:15<00:00,  1.18s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:15<00:00,  1.20s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:15<00:00,  1.20s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:15<00:00,  1.16s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:15<00:00,  1.20s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:14<00:00,  1.14s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:14<00:00,  1.11s/it]
Iteration: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████| 13/13 [00:14<00:00,  1.14s/it]
Epoch: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [02:31<00:00, 15.13s/it]
```

same? Well one interesting thing, now there are 124 layers instead of 125, 
```python 
In [322]: len([x for x in model.modules()])
Out[322]: 124
  

In [323]: [x for x in model.modules()][-5:]
Out[323]: 
[BertPooler(
   (dense): Linear(in_features=384, out_features=384, bias=True)
   (activation): Tanh()
 ),
 Linear(in_features=384, out_features=384, bias=True),
 Tanh(),
 Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False}),
 Normalize()]

```
```python
pooler = [x for x in model.modules()][-5]
print("pooler weights all close?", 
      np.allclose(
        weights_before.detach().numpy(), pooler.dense.weight.detach().numpy()))

# True
```
Ok so that is True within the default tolerance and per below, I see indeed the changes are quite minimal. 
```python
In [336]: weights_before[:, :5]
Out[336]: 
tensor([[-0.0151, -0.0224, -0.0046, -0.0199,  0.0064],
        [ 0.0083, -0.0186, -0.0132, -0.0009, -0.0157],
        [-0.0030,  0.0108, -0.0102,  0.0023, -0.0006],
        ...,
        [-0.0049, -0.0010, -0.0043, -0.0035,  0.0108],
        [-0.0089,  0.0108,  0.0011,  0.0227, -0.0051],
        [ 0.0049,  0.0070, -0.0065, -0.0034,  0.0024]],
       grad_fn=<SliceBackward0>)


In [330]: pooler.dense.weight.detach().numpy()[:, :5]
Out[330]: 
array([[-0.01512909, -0.02244568, -0.00457382, -0.01985168,  0.00641632],
       [ 0.0083313 , -0.01863098, -0.01322937, -0.00087643, -0.01565552],
       [-0.00302696,  0.01076508, -0.0102005 ,  0.00234985, -0.00063133],
       ...,
       [-0.00487518, -0.00100899, -0.00428391, -0.00347328,  0.01079559],
       [-0.00886536,  0.01075745,  0.00112629,  0.02267456, -0.00512314],
       [ 0.00490952,  0.00695419, -0.00653076, -0.00342751,  0.00236511]],
      dtype=float32)
```
Well definitely different weights on the `BertPooler` there for sure. And now there is some kind of new `Pooling` layer I did not see before too.
Ok so since the changes are super minimal, I don't think it is worth additional testing.
So instead, I need a bigger dataset to try this out. But at least I can see that yes, fine tuning does do something haha.

Custom dataset thought,
might be that instead of sticking to one engineering slice of that jobs dataset, I might try pulling out multiple slices, at least to attempt to see, with a train test split, does the fine tuning help .
12:41 going to look at my personal dataset one more time ,
One question I have, what percent of the text in my "my-challenges-and-accomplishments/experience.yaml" am I capturing into my blurb? Simple question ,
```python
import utils as ut

repos_dir = Path(os.getenv("REPOS_DIR"))
assert repos_dir.is_dir()      
experience_loc = repos_dir / "my-challenges-and-accomplishments/experience.yaml"
total_length = len(experience_loc.read_text())

experiences_dict = ut.read_yaml(experience_loc)["Descriptions"]
my_sentences = ut.build_my_blurb(experiences_dict)
print("proportion used:", len(" ".join(my_sentences)) / total_length)
```
```python
proportion used: 0.3994211783644008
```
Ok wow haha I did not expect that to be that low haha.
13:14 The reason it is not 100% is that I write initial drafts of work I did first which is not pulled by the `"build_my_blurb"` function and then when I have spare time I will to to better phrase those drafts, I put them into `one-liners` and `stories`, hopefully more succinctly, which is pulled by `"build_my_blurb"`.
#### Ok then perhaps a slight twist of what I would like to do next,
(1) Use the two raw job description dumps from earlier, to build a corpus not of individual sentences, as I had prior, but of job descriptions, attempting to also create a label column that tries to generalize the job titles they have, to hopefully around 5. I can keep "amazon" or "google" as an additional column for alter too .
(2) Create a [[positive pair]] dataset from that , clustering by job title so  this time not doing it by hand as much.
(3) Split that into a train test .
(4) Fine tune train , and then use test , also w/ the [[Multiple negatives ranking loss]] . Maybe I can test before and after the fine tuning.
(5) apply to my blurb dataset, and hand inspect what comes up for me.



### [[Aug 7th, 2023]] and [[Aug 8th, 2023]] approaching build a dataset of larger chunks perhaps 
Started looking at how big that would be
So , how long are these job descriptions then if I take them raw instead of splitting into sentences like I had done before?

```python

technical_job_title_terms = [
  "engineer", "developer", "research", "technical", "analyst", "engineering",
  "data", "sciences", "ux", "analytics", "systems", "architect", "researcher", "web",
  "infrastructure", "intelligence", "quantitative", "learning", "software",
  "scientist",
        ]

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
columns_map = {"Responsibilities": "description", 
                            'Minimum Qualifications': "minimum qualifications", 
                            'Preferred Qualifications': "preferred qualifications"
          }
columns = list(columns_map.keys())
google_jobsdf = ut.filter_pandas_multiple_contains(
    pd.read_csv(loc), "Title", technical_job_title_terms
)[["Title"] + columns]
print("google_jobsdf", google_jobsdf.shape)

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
			/ "kaggle-amazon-job-skills/amazon_jobs_dataset.csv")
columns_map = {
    'DESCRIPTION': "description",
    'BASIC QUALIFICATIONS': "minimum qualifications",
    'PREFERRED QUALIFICATIONS': "preferred qualifications"}
columns = list(columns_map.keys())
amazon_jobsdf = ut.filter_pandas_multiple_contains(
    pd.read_csv(loc), "Title", technical_job_title_terms
)[["Title"] + columns]
print("amazon_jobsdf", amazon_jobsdf.shape)

google_jobsdf["Responsibilities"].map(lambda x: len(x)).describe()


```
```python

In [346]: google_jobsdf[google_jobsdf["Responsibilities"].notnull()]["Responsibilities"].map(lambda x: len(x)).describe()
Out[346]: 
count     375.000000
mean      677.290667
std       272.640256
min        47.000000
25%       518.500000
50%       664.000000
75%       858.000000
max      1654.000000
Name: Responsibilities, dtype: float64
```
09:41 ok well getting a basic sense here, yea 1654  character length, don't know how many tokens that might map to, but feels like should be fine with the  "384" [[context-window]] I think, 
```python
1654/384 ~ 4.3 
```
and without spaces then this is better. so yea might be worth a shot to try this out.
### [[Aug 9th, 2023]] quick stab count max tokens then
ok so lets combine the three relevant columns, and see how many tokens that seems to produce

collapsed:: true
```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')


technical_job_title_terms = [
  "engineer", "developer", "research", "technical", "analyst", "engineering",
  "data", "sciences", "ux", "analytics", "systems", "architect", "researcher", "web",
  "infrastructure", "intelligence", "quantitative", "learning", "software",
  "scientist",
        ]

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
            / "kaggle-google-job-skills/job_skills.csv")
columns_map = {"Responsibilities": "description", 
                            'Minimum Qualifications': "minimum qualifications", 
                            'Preferred Qualifications': "preferred qualifications"
          }
columns = list(columns_map.keys())
google_jobsdf = pd.read_csv(loc).rename(columns=columns_map).dropna()
print("google_jobsdf", google_jobsdf.shape)
google_jobsdf["all"] = google_jobsdf.apply(
    lambda x: ". ".join([x["Title"],
                         x["description"], 
                         x["minimum qualifications"],
                         x["preferred qualifications"]
                        ]),
    axis=1
)
google_jobsdf["tokens"] = google_jobsdf["all"].map(
    lambda x: tokenizer.tokenize(x)
)
google_jobsdf["num_tokens"] = google_jobsdf["tokens"].map(
    lambda x: len(x)
)
google_jobsdf["num_tokens"].describe()
```
```python
google_jobsdf (1235, 7)
Token indices sequence length is longer than the specified maximum sequence length for this model (575 > 512). Running this sequence through the model will result in indexing errors
Out[362]: 
count    1235.000000
mean      253.638057
std        83.005630
min        65.000000
25%       198.000000
50%       245.000000
75%       298.000000
max       692.000000
Name: num_tokens, dtype: float64
```
ok indeed we hit some of the longer sequences and that error, 
```python
Token indices sequence length is longer than the specified maximum sequence length for this model (575 > 512). Running this sequence through the model will result in indexing errors
```
interesting says 512. Ok anyway, max is 692 I am seeing here.
Might as well also try with removing stop words at some point but maybe initial stab just truncate and go end to end, train test, positive pair dataset using the job titles for clustering and run full fine tuning and see does that change the weights, and does it improve sentence similarity for this jobs dataset itself. just as a POC .
### [[Aug 13th, 2023]] reading more about [[Multiple negatives ranking loss]] , researching how to bake that cake . Looking into clustering to maybe help create a dataset.
hmm I had encountered [this video](https://www.youtube.com/watch?v=b_2v9Hpfnbw) from [[Nicholas Broad]] on [[Multiple negatives ranking loss]] , let me continue that ,

collapsed:: true
interesting I did not get a negative cosine similarity yet
softmax is used too. so it is single label multi class classification hm m
hmm ok , so for two vectors of embeddings, of [[positive pair]] , we want high similarity pairwise `i == j` and low similarity otherwise `i != j` ,  
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1691932507190_0.png" width="50%">}}
ok yea he's driving the point home here that this loss, tries to minimize distance between the pairs and maximize distance between the non-pairs , 
> The model is rewarded for
reducing the angle between the
embeddings of positive pairs
maximizing the angle between
non-pair embeddings.

09:33 yea this [[Multiple negatives ranking loss]] is kind of elusive. It is basically saying each row in your dataset can have two  sentence embeddings  that are really close but when compared with any other row they should not be and therefore it is like you need to have as many unique concepts as rows and that sounds kind of hard to do, at least automatically.

collapsed:: true
Very much getting the [[Russel Peters]] #joke [[joke/How do you make a cake ]] , I think I have not seen a good explanation of how to do this ,
Case in point, [this article](https://www.pinecone.io/learn/series/nlp/fine-tune-sentence-transformers-mnr/) is another nice explanation but the actual dataset used again is a freebie, already given , the Stanford Natural Language Inference (SNLI) and Multi-Genre NLI (MNLI) corpora , they already have labels which nicely define tons of sentence pairs explicitly stating whether they are related.
Think you must just focus on the positive pairs and hopefully try not to put positives in the  non pairs somehow
Hmm perhaps perhaps that's why generating [[average-pooling]] embeddings from larger sentences then is important because thinking if you were to use say embeddings from just single words, say you are trying to fine tune a model around sentiment, you first of all have fewer examples you can come up with of single-word embeddings, since just combinatorially [[combinatorics]] , but in general, maybe you can convey more complicated emotions with multiple words also because they have some interesting context.
collapsed:: true
We are still dealing with a kind of [[bag-of-words]] here but, it feels kind of like how that [[course/Rethinking Stress]] put it, that yes you can let your response to stress stay in your #amygdala , where perhaps emotions have undergone  [[dimensionality reduction]] haha the model is very [[bias]] very #primal very basic , but alternatively you can process your stress in your [[prefrontal cortex]] and get more nuance that way.
For example, I am on a #roof-top right now and I brought my #sunscreen with me because last time I got pretty burnt with the diffuse sunlight, so the emotion might be a few different levels,
lowest level: "Oh no"
medium level: "darn I got sun-burnt "
higher level: "I know I get burnt easily but I was excited to work on my project in an outdoor area for a change and I forgot that light can diffract and be diffuse sometimes and I ended up not using sunsccreen because I thought I was in the shade but it was a lot of diffuse sunlight so I got pretty burnt. And on top of that, I   already had plans to spend several hours in the sun a week from then, on the water, so I realized I had about a week to try to hopefully get cured from the sun exposure."
Haha so in my examples there, I think the hypothesis I have now is that when building a [[positive pair]] dataset, one should attempt to use [[high dimensionality]] sentences to come up with their embeddings, to try to have a good dataset that doesn't have too many non-pairs which are also close.
10:38  One more thought enters my mind hmm that since the example earlier in that [[article/Train and Fine-Tune Sentence Transformers Models]] made reference to a positive pair dataset of sentence compression, it makes sense that a "transformation" would be a good way to build a dataset of this kind , so, 
```
X = some sentences, 
Z = f(X)  # where f() is some kind of transformation 
```

10:50 seeking some additional advice on this , lets see [this article](https://www.pinecone.io/learn/series/nlp/fine-tune-sentence-transformers-mnr/) ,

collapsed:: true
10:55 oh wow, this is a cool idea, they mention there is a `NoDuplicatesDataLoader` class in the [[sentence-transformers]] library. hmm this is handy although I think this is purely handling the duplicates case which is kind of easy to do anyway though haha. But probably a good idea to create a similar data loader like "NoAlmostDuplicateDataLoader" that helps you from shooting yourself in the foot with near-duplicates in there.
11:05 also interesting they are saying the evaluator there, uses [[Spearmans rank correlation]] [[correlation]] as a metric to evaluate.
```python
from sentence_transformers import InputExample

samples = []
for sample in sts:
    samples.append(InputExample(
        texts=[sample['sentence1'], sample['sentence2']],
        label=sample['label']
    ))

from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
evaluator = EmbeddingSimilarityEvaluator.from_input_examples(
    samples, write_csv=False
)
```
Kind of interesting, not to use like #RMSE say. Maybe more direct?
11:44 ok lets try something

referring to my [note from earlier](https://michal.piekarczyk.xyz/post/2023-06-18-my-projects-langchain-interview-me-2023-feb/#ok-then-perhaps-a-slight-twist-of-what-i-would-like-to-do-next), I see, yea if I had a base model, and say that train test split of a positive pair embeddings dataset, I can yea say, measure for that test set, say, the similarity for each pair, and likely, they would be lower than doing this with a tuned model.
```python

loc = (Path(os.getenv("REPOS_DIR")) 
            / "data" 
			/ "kaggle-amazon-job-skills/amazon_jobs_dataset.csv")
columns_map = {
    'DESCRIPTION': "description",
    'BASIC QUALIFICATIONS': "minimum qualifications",
    'PREFERRED QUALIFICATIONS': "preferred qualifications"}
columns = list(columns_map.keys())
amazon_jobsdf = pd.read_csv(loc).rename(columns=columns_map).dropna()
# [["Title"] + columns]
print("amazon_jobsdf", amazon_jobsdf.shape)
```
12:49 So the amazon dataset doesn't have a "Category" column like the google jobs dataset does, but I think if anything, this might be a good opportunity to try to cluster them in a sense, w/ similarity, to see if the clusters appear to align somewhat, along the job titles.
```python
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

print("amazon_jobsdf", amazon_jobsdf.shape) # amazon_jobsdf (3484, 7)
amazon_jobsdf["all"] = amazon_jobsdf.apply(
    lambda x: ". ".join([x["Title"],
                         x["description"], 
                         x["minimum qualifications"],
                         x["preferred qualifications"]
                        ]),
    axis=1
)
amazon_jobsdf["tokens"] = amazon_jobsdf["all"].map(
    lambda x: tokenizer.tokenize(x)
)
amazon_jobsdf["num_tokens"] = amazon_jobsdf["tokens"].map(
    lambda x: len(x)
)
amazon_jobsdf["num_tokens"].describe()

```
```python
Token indices sequence length is longer than the specified maximum sequence length for this model (785 > 512). Running this sequence through the model will result in indexing errors
Out[377]: 
count    3484.000000
mean      549.493972
std       182.492633
min        88.000000
25%       429.000000
50%       518.000000
75%       628.250000
max      1764.000000
Name: num_tokens, dtype: float64

```
hmm side note looks like the mean and median token counts are `549` and `518` here whereas it was `253` and `245` for that google dataset hmm. interesting. Haha more fluff or boilerplate in the amazon one? Maybe an interesting corollary to [[stop-words]] is like fluff words, oh haha kind of like I should use the vocabulary from that tool [[Bullshit.js]] [[bullshit]] tool haha, that would be funny
https://github.com/mourner/bullshit.js?ref=alian.info
The terms are in https://github.com/mourner/bullshit.js/blob/master/src/terms.js , using regex syntax
#### ok lets try to make some clusters
```python
raw_sentences = make_into_raw_sentences(amazon_jobsdf)

# take out the stop words , because of the long lengths
without_stop_words = take_out_stop_words(raw_sentences)

# Then run something like  this, 
hits = semantic_search(my_story_embeddings, jd_embeddings, top_k=10)

use that above to identify clusters that are of close similarity, maybe for some threshold
clusters = union_find(hits)
```
```python
amazon_jobsdf["raw"] = amazon_jobsdf["all"].map(ut.dont_stop)

amazon_jobsdf["tokens"] = amazon_jobsdf["raw"].map(
    lambda x: tokenizer.tokenize(x)
)
amazon_jobsdf["num_tokens"] = amazon_jobsdf["tokens"].map(
    lambda x: len(x)
)
amazon_jobsdf["num_tokens"].describe()
```
```python
count    3484.000000
mean      402.791619
std       131.850287
min        55.000000
25%       317.000000
50%       380.000000
75%       460.000000
max      1623.000000
Name: num_tokens, dtype: float64
```
14:31 ok that's a taken the median down by about 200 tokens, nice.
let me just get rid of the punctuation too since saw that is 18% of the tokens in the first sentence ,
```python
In [389]: punctuation_tokens = [",", '.', '·', "'", ":" ]
     ...: print(len([x for x in (amazon_jobsdf.iloc[0]["tokens"]) if x in punctuation_tokens])/len(amazon_jobsdf.iloc[0]["tokens"]))
0.18149466192170818
```
```python
amazon_jobsdf["raw1"] = amazon_jobsdf["all"].map(ut.dont_stop)
amazon_jobsdf["raw"] = amazon_jobsdf["raw1"].map(ut.remove_punctuation)
amazon_jobsdf["tokens"] = amazon_jobsdf["raw"].map(
    lambda x: tokenizer.tokenize(x)
)
amazon_jobsdf["num_tokens"] = amazon_jobsdf["tokens"].map(
    lambda x: len(x)
)
amazon_jobsdf["num_tokens"].describe()
```
```python
count    3484.000000
mean      329.933410
std       108.949385
min        46.000000
25%       259.000000
50%       311.000000
75%       377.000000
max      1511.000000
Name: num_tokens, dtype: float64


```
14:51 ok nice got lower by another 80 tokens wow.
So proceed with the comparisons then,
15:22 ok,
```python
raw_sentences = amazon_jobsdf["raw"].tolist()
model_id =  "sentence-transformers/all-MiniLM-L6-v2"
# some = random.choices(raw_sentences, k=1000)
embeddings = ut.vec_to_embeddings(model_id, raw_sentences)

hits = semantic_search(embeddings, embeddings, top_k=10)

```
15:29 hmm [[Union Find graph algo]] vs [[k means]]
oh https://www.sbert.net/examples/applications/clustering/README.html they have a page and they dont mention union find somehow . interesting.
16:12 quick look at the hits results,
```python

In [396]: hits[0]
Out[396]: 
[{'corpus_id': 0, 'score': 1.000000238418579},
 {'corpus_id': 529, 'score': 0.9883664846420288},
 {'corpus_id': 2052, 'score': 0.8829057216644287},
 {'corpus_id': 3377, 'score': 0.88020920753479},
 {'corpus_id': 376, 'score': 0.8609091639518738},
 {'corpus_id': 320, 'score': 0.859550416469574},
 {'corpus_id': 679, 'score': 0.8540301322937012},
 {'corpus_id': 958, 'score': 0.8538450598716736},
 {'corpus_id': 1692, 'score': 0.8538450598716736},
 {'corpus_id': 1352, 'score': 0.8520417213439941}]

In [397]: len(raw_sentences), len(some), len(hits), amazon_jobsdf.shape[0]
Out[397]: (3484, 1000, 3484, 3484)

In [398]: from collections import Counter

In [400]: amazon_jobsdf.iloc[0]["Title"]
Out[400]: 'Software Development Manager'

In [401]: Counter([amazon_jobsdf.iloc[i]["Title"] for i in [x["corpus_id"] for x in hits[0]]])
Out[401]: 
Counter({'Software Development Manager': 7,
         'Software Developer Manager': 1,
         'Software Development Engineer': 2})

```
interesting
next , ok I can continue this cluster analysis, and then perhaps I can use the clusters, to try to create at least some positive pairs that don't overlap too much , so the [[Multiple negatives ranking loss]] is not too diluted

### [[Aug 14th, 2023]] tried the clustering 
However there is a lot of information here so haha , not simple to verify it
continue from last time , I have `embeddings` , lets try with `10` clusters, see wht happens, following example from [here](https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/clustering/kmeans.py),

```python
from sklearn.cluster import KMeans

embeddings.shape  # torch.Size([3484, 384])


# Perform kmean clustering
num_clusters = 10
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(embeddings)
cluster_assignment = clustering_model.labels_

cluster_assignment.shape  # Out[406]: (3484,)

print(Counter(cluster_assignment))
Counter({6: 798, 9: 597, 8: 406, 7: 349, 5: 327, 3: 309, 1: 206, 2: 194, 4: 162, 0: 136})
```
look at what job titles have been clustered togethe,
```python
amazon_jobsdf["cluster"] = cluster_assignment.tolist()
for cluster_id in set(cluster_assignment):
    print("cluster", cluster_id)
    print(set(amazon_jobsdf[amazon_jobsdf["cluster"] == cluster_id]["Title"].tolist()))
    print("\n", "=" * 80)
```
09:22 ok wow , there are so many titles, the output is not easy to read.
```python

for cluster_id in set(cluster_assignment):
    print("cluster", cluster_id)
    print(list(
        set(amazon_jobsdf[amazon_jobsdf["cluster"] == cluster_id]["Title"].tolist())
    )[:5])
    print("\n", "=" * 80)
```
```python

cluster 0
['Development Manager – AWS AI: Backend Engine', 'Frontend/UI Engineer, AWS AmazonAI Machine Learning Platform', 'Software Development Engineer - AWS AI Deep Learning', 'Senior Software Development Engineer - AWS AI Deep Learning', 'Software Development Engineer, Browse Classification']

 ================================================================================
cluster 1
['Technical Program Manager - Speech technologies on devices', 'AMAZON ALEXA IoT in Boston - Software Developer on Alexa Machine Learning Team', 'Senior Software Development Engineer', 'ML Research/Software Engineer, Alexa ', 'Software Development Engineer - Alexa Machine Learning  - Boston or Seattle']

 ================================================================================
cluster 2
['Software Dev Engineer', 'Mobile Applications Engineer - Android', 'Senior Software Development Engineer', 'Principle SW Dev Engineer', 'Wireless Software Engineer Intern']

 ================================================================================
cluster 3
['Software Dev Engineer', 'S3 Software Development Manager', 'Senior Software Development Engineer - AWS Commerce Platform- Berlin (m/f)', 'Software Development Engineer - S3 Webserver', 'Senior Software Development Engineer']

 ================================================================================
cluster 4
['Game Server Engineer', 'Live Services Engineer', 'Senior Software Development Engineer', 'Senior Mobile Engineer', 'Software Development Engineer (Level 5)']

 ================================================================================
cluster 5
['Verification Engineer', 'Front-end Engineer, AWS', 'Software Development Engineer - Belgrade Hiring Event, February 2018', 'SW Development Engineer in Test', 'Senior Software Development Engineer']

 ================================================================================
cluster 6
['Senior Software Development Engineer, EC2 Virtual Private Cloud', 'Software Development Engineer - TEST', 'Senior Software Development Engineer', ' Software Development Engineer - Analytics', 'Senior Software Development Engineer, EC2 Cloud Manager Team']

 ================================================================================
cluster 7
['WDE', 'Software Development Engineer - Amazon FreeTime', 'Senior Software Development Engineer', 'Software Development Engineer (Level 5)', 'Sr.Android Software Development Engineer ']

 ================================================================================
cluster 8
['Alexa Software Development Engineer', 'Software Development Engineer in Test - Alexa New initiative!', 'Senior Software Development Engineer, Alexa Voice Services, Automotive', 'Quality Assurance Engineer, Alexa Voice Services, Automotive', 'Senior Software Development Engineer']

 ================================================================================
cluster 9
['Blitz pooling req -Software Development Engineer', 'Senior Software Development Engineer – Amazon Global Catalog Systems', 'Software Development Engineer - AWS Marketplace', 'Software Dev Engineer', 'Senior Software Development Engineer: Internationalization Core']

 ================================================================================


```
This is still difficult to interpret. I feel like there is still a lot of background noise in these job postings. Probably would help to get rid of that . This is like boiler plate speak looks like this, 
```
 “the world’s customer centric company "

Amazon Equal Opportunity-Affirmative Action Employer - Minority   Female   Disability   Veteran   Gender Identity   Sexual Orientation
```
So thinking either should go back to that idea of just entity extraction which would be the inverse of fluff extraction

### [[Aug 15th, 2023]] tried one fluff analytics approach
Not so simple hmm
The issue here is I think partly, there is a lot of information in these postings I suspect is noise that is confusing the [[average-pooling]] , so I am tempted to do some preprocessing to remove that

[[common sub sequence]] ? I feel like I have seen before, like features, that are embeddings specific to some kind of attribute of the full raw text.
```python
fluff_phrases = [
  ut.remove_punctuation(x) for x in
  [  "Amazon is an Equal Opportunity-Affirmative Action Employer - Minority / Female / Disability / Veteran / Gender Identity / Sexual Orientation"
    'Amazon is driven by being “the world’s most customer centric company."',
    'In the Health, Safety, Sustainability, Security, and Compliance (HS3C) organization, we own ensuring that all products at Amazon are 100% complaint with all legal, trade, product safety, and food safety requirements.',
    'We’re obsessed with the safety of all our customers and workers, creating a world-class experience for our millions of vendors and sellers world-wide, and inventing the best business and regulatory models for safe and sustainable supply chains in our industries.',
  ]
]

amazon_jobsdf["all"] = amazon_jobsdf.apply(
    lambda x: ". ".join([x["Title"],
                         x["description"], 
                         x["minimum qualifications"],
                         x["preferred qualifications"]
                        ]),
    axis=1
)

amazon_jobsdf["all_no_punctuation"] = amazon_jobsdf["all"].map(
    ut.remove_punctuation
)

amazon_jobsdf["fluff_count"] = amazon_jobsdf["all_no_punctuation"].map(
    lambda s: sum([
      1 if x in s else 0
      for x in fluff_phrases
    ])
)
```
```python
In [433]: amazon_jobsdf["fluff_count"].value_counts()
Out[433]: 
0    3477
2       7
Name: fluff_count, dtype: int64
```
Hmm maybe need to try this differently.
### [[Aug 17th, 2023]] detect fluff with cosine similarity
continuing w/ fluff analytics, out of curiosity, let me search for the fluff phrases by cosine similarity, maybe stuff is re-worded

```python
model_id =  "sentence-transformers/all-MiniLM-L6-v2"

fluff_phrases = [
  ut.remove_punctuation(x) for x in
  [  "Amazon is an Equal Opportunity-Affirmative Action Employer - Minority / Female / Disability / Veteran / Gender Identity / Sexual Orientation"
    'Amazon is driven by being “the world’s most customer centric company."',
    'In the Health, Safety, Sustainability, Security, and Compliance (HS3C) organization, we own ensuring that all products at Amazon are 100% complaint with all legal, trade, product safety, and food safety requirements.',
    'We’re obsessed with the safety of all our customers and workers, creating a world-class experience for our millions of vendors and sellers world-wide, and inventing the best business and regulatory models for safe and sustainable supply chains in our industries.',
  ]
]

raw_sentences = amazon_jobsdf["all_no_punctuation"].tolist()

hits = ut.search(model_id, fluff_phrases, raw_sentences)


```
```python
for i, row in enumerate(hits):
    print(f"({i})", "matching,", fluff_phrases[i][:20], ":")
    hmm = [
      [raw_sentences[x["corpus_id"]][:20], x["corpus_id"], x["score"]] for x in row ]
    print(hmm, "\n\n")
```
```python
(0) matching, Amazon is an Equal O :
[['Manager of Applicati', 11, 0.5805604457855225], ['Software Development', 774, 0.5495573282241821], ['Senior Manager Softw', 3221, 0.5386903882026672], ['Software Development', 1111, 0.5257833003997803], ['Software Development', 1110, 0.5257833003997803], ['Software Development', 2346, 0.5253446698188782], ['Software Development', 1957, 0.5253446698188782], ['Software Development', 2942, 0.5167820453643799], ['Software Development', 2896, 0.5167820453643799], ['Software Development', 2550, 0.5115794539451599]] 


(1) matching, In the Health Safety :
[['Software Development', 2167, 0.6412075161933899], ['Sr Software Developm', 2093, 0.6237956285476685], ['Software Development', 2, 0.6191249489784241], ['Software Development', 30, 0.6191249489784241], ['Software Development', 1, 0.6191249489784241], ['Software Development', 31, 0.6191249489784241], ['Senior Software Deve', 332, 0.6013069152832031], ['Software Development', 3161, 0.5426405668258667], ['Software Development', 83, 0.5362498760223389], ['Senior Software Deve', 191, 0.4951627850532532]] 


(2) matching, We re obsessed with  :
[['Software Development', 2167, 0.5930458903312683], ['Sr Software Developm', 2093, 0.5782648324966431], ['Software Development', 2, 0.5531834363937378], ['Software Development', 31, 0.5531834363937378], ['Software Development', 30, 0.5531834363937378], ['Software Development', 1, 0.5531834363937378], ['Software Development', 3161, 0.5344783663749695], ['Senior Software Deve', 332, 0.5275624990463257], ['Software Development', 1098, 0.5085136890411377], ['Software Development', 2302, 0.5051045417785645]] 



```
ok will look at the hits more next time. Interesting to see the scores greater than 0.5 though, even though those raw texts are really much longer than the phrases I'm searching for . This is an interesting mini #take-away . [[symmetric vs asymmetric semantic search]]

### [[Aug 18th, 2023]] briefly, fluff hits one ore time, but more so
try query again but dont cut just top 10 hmm

```python
vec = []
for i, row in enumerate(hits):
    print(f"({i})", "matching,", fluff_phrases[i][:20], ":")
    hmm = [
      [raw_sentences[x["corpus_id"]][:20], x["corpus_id"], x["score"]] for x in row ]
    print(hmm, "\n\n")
    vec.extend([{
      "query": fluff_phrases[i],
      "result": raw_sentences[x["corpus_id"]],
      "score": x["score"],
    } for x in row])

    
loc = (Path(workdir) / f"{utc_ts(utc_now())}-search-result.csv")
print(loc.name)  # 2023-08-18T130750-search-result.csv
pd.DataFrame.from_records(vec).to_csv(loc)

```
let me look at results. forgot to save score though.
```python
%%time
hits = ut.search(model_id, fluff_phrases, raw_sentences, top_k=4000)
Wall time: 5min 42s

loc = (Path(workdir) / f"{utc_ts(utc_now())}-search-result.csv")
print(loc.name)  # 2023-08-18T132229-search-result.csv
df = ut.search_results_to_pdf(hits, fluff_phrases, raw_sentences, preview=False)
df.to_csv(loc)


In [466]: df.iloc[0]
Out[466]: 
query     Amazon is an Equal Opportunity-Affirmative Act...
result    Manager of Application Development and Enginee...
score                                               0.58056
Name: 0, dtype: object

In [467]: df.score.describe()
Out[467]: 
count    10452.000000
mean         0.275819
std          0.082075
min         -0.011822
25%          0.218657
50%          0.274074
75%          0.329111
max          0.641208
Name: score, dtype: float64
```
ok next, can look at the more fuller results, scores,


### [[Aug 19th, 2023]] Looked at histogram of cosine similarity scores from the fluff phrase hits
what are scores like, quick histogram, they are in `df.score` from yesterday

```python
import matplotlib.pyplot as plt
import pylab

scores = df.score.tolist()

fig = plt.figure(figsize=(10, 10/1.6))
ax = fig.add_subplot(111)

with plt.style.context('fivethirtyeight'):
    ax.hist(scores, bins=10)
    loc = (Path(workdir) / f"{utc_ts(utc_now())}-scores-hist.png")
    print(loc, loc.name)
    pylab.savefig(loc)
    pylab.close()


```
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/2023-08-19T151019-scores-hist_1692457964293_0.png" width="50%">}}
11:16 That's interesting, so , interesting how it looks pretty normal. and very few over `0.5` .
So are the ones over `0.5` good ones ?
```python
In [473]: df[df.score >= 0.5].shape, df.shape[0]
Out[473]: ((47, 3), 10452)
```





ok

### [[Aug 20th, 2023]] using one hot encoding to try to confirm those results
12:06 so what are those `47` job descriptions I saw there

collapsed:: true
```python
loc = (Path(workdir) / f"{utc_ts(utc_now())}-search-result.csv") 
print(loc.name)  # '2023-08-20T161939-search-result.csv'
df_highest = df[df.score >= 0.5]
df_highest.to_csv(loc)

for phrase in fluff_phrases:
    print(phrase, df_highest[df_highest["query"] == phrase].shape)
```
```python
Amazon is an Equal Opportunity-Affirmative Action Employer - Minority Female Disability Veteran Gender Identity Sexual OrientationAmazon is driven by being “the world s most customer centric company " (27, 3)
In the Health Safety Sustainability Security and Compliance HS3C organization we own ensuring that all products at Amazon are 100% complaint with all legal trade product safety and food safety requirements (9, 3)
We re obsessed with the safety of all our customers and workers creating a world-class experience for our millions of vendors and sellers world-wide and inventing the best business and regulatory models for safe and sustainable supply chains in our industries (11, 3)
```
The only way to know false positive, false negatives perhaps, is to create some one hot features for the substrings I think
```python
one_hot_sub_phrases = [
  " ".join(x[i:i + 3]).lower() for i in range(len(x.split(" ")) - 3)
  for x in fluff_phrases
]
```
```python

df_highest = df[df.score >= 0.5].copy()
for sub_phrase in one_hot_sub_phrases:
    df_highest["OHE_" + sub_phrase] = df_highest["result"].map(lambda x: int(sub_phrase in x))

      
cols = df_highest.columns.tolist()
ohe_cols = [x for x in cols if x.startswith("OHE_")]

df_highest["sub_phrase_sum"] = df_highest.apply(lambda x: sum([x[col] for col in ohe_cols]), axis=1)

loc = (Path(workdir) / f"{utc_ts(utc_now())}-search-result-ohe.csv")
print(loc.name)  # 2023-08-20T172224-search-result-ohe.csv
df_highest[["query", "sub_phrase_sum"] + ohe_cols].to_csv(loc)

```

hmm not looking great, think I'm seeing lots of rows where the query has `sub_phrase_sum=0`  which feels like false positives?
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1692552249125_0.png" width="50%">}}
can continue this #[[one hot encoding]]
### [[Aug 21st, 2023]] debugging some one hot encoding results
ok so last time, yea saw yea oddly, lots of cases where the one hot columns not yet showing why the sentence matched more than `0.5` to that query. [[false-positive]] ?

Let's look at one, hmm nevermind, looking at the first one
```python
In [498]: df_highest.iloc[0]
Out[498]: 
query                                          Amazon is an Equal Opportunity-Affirmative Act...
result                                         Manager of Application Development and Enginee...
score                                                                                    0.58056
OHE_amazon is an                                                                               0
OHE_is an equal                                                                                0
OHE_an equal opportunity-affirmative                                                           0
OHE_equal opportunity-affirmative action                                                       0
OHE_opportunity-affirmative action employer                                                    0
OHE_action employer -                                                                          0
OHE_employer - minority                                                                        0
OHE_- minority female                                                                          0
OHE_minority female disability                                                                 0
OHE_female disability veteran                                                                  0
OHE_disability veteran gender                                                                  0
OHE_veteran gender identity                                                                    0
OHE_gender identity sexual                                                                     0
OHE_identity sexual orientationamazon                                                          0
OHE_sexual orientationamazon is                                                                0
OHE_orientationamazon is driven                                                                0
OHE_is driven by                                                                               0
OHE_driven by being                                                                            0
OHE_by being “the                                                                              0
OHE_being “the world                                                                           0
OHE_“the world s                                                                               0
OHE_world s most                                                                               0
OHE_s most customer                                                                            0
OHE_most customer centric                                                                      0
OHE_customer centric company                                                                   0
sub_phrase_sum                                                                                 0
Name: 0, dtype: object
```
I looked at the raw `result` and it should have matched the one hot columns here. Let me debug my one hot code.
Ah damn ok, forgot to lower case, lets try again,
```python
df_highest = df[df.score >= 0.5].copy()

for sub_phrase in one_hot_sub_phrases:
    df_highest["OHE_" + sub_phrase] = df_highest["result"].map(
      lambda x: int(sub_phrase in x.lower()))

cols = df_highest.columns.tolist()
ohe_cols = [x for x in cols if x.startswith("OHE_")]      

df_highest["sub_phrase_sum"] = df_highest.apply(lambda x: sum([x[col] for col in ohe_cols]), axis=1)

loc = (Path(workdir) / f"{utc_ts(utc_now())}-search-result-ohe.csv")
print(loc.name)  # 2023-08-21T131154-search-result-ohe.csv

df_highest[["query", "sub_phrase_sum"] + ohe_cols].to_csv(loc)
```
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-02-18-langchain-interview-me-2023-feb/image_1692623559125_0.png" width="50%">}}
ok nice, much better. Way fewer zeros in `sub_phrase_sum` this time. Still have them though.
Lets look at another,
```python
In [502]: df_highest.iloc[1]["query"]
Out[502]: 'Amazon is an Equal Opportunity-Affirmative Action Employer - Minority Female Disability Veteran Gender Identity Sexual OrientationAmazon is driven by being “the world s most customer centric company "'
  
In [507]: Counter(df_highest.iloc[1]["result"].split(" ")).most_common(6)
Out[507]: 
[('and', 25),
 ('the', 12),
 ('to', 11),
 ('of', 11),
 ('Amazon', 9),
 ('customers', 8)]
```
hmm for this one above my guess is that the "Amazon customers" part is what pops out then. So might not be a false positive because of that. Goes to show that [[explainability]] would be nice here.
Anyway, main motive for going down this path of potentially removing [[noise]] or fluff from the data , improve the [[Signal To Noise Ratio]] hopefully improve the clustering I was attempting earlier, because I was seeing lots of jobs getting clustered that had job titles that looked unrelated.

General hypothesis is that, perhaps there is a lot of boilerplate noisy fluff text in common in many of the job descriptions that is confusing the cosine similarity . Removing it would hopefully improve this , so ultimately I can build a better dataset for fine tuning. Haha. Complicated.
Maybe go back to the entity extraction if that is more straight forward perhaps .
### [[Aug 22nd, 2023]] another look at those fluff outputs hmm
hmm

Maybe cut up those fluff/noise queries more, to be more specific, more surgical?
Maybe need a more methodical understanding of what is a fluff/noise phrase?
Wonder if some of my documents are a bit long did they get truncated actually when I was running the search especially if some fluff phrases are at the tail ends?
Maybe good next thing , look at the one hot encoding results I had for all the data, can I spot the false negatives therefore?
```python
for sub_phrase in one_hot_sub_phrases:
    df["OHE_" + sub_phrase] = df["result"].map(
            lambda x: int(sub_phrase in x.lower()))

cols = df.columns.tolist()
ohe_cols = [x for x in cols if x.startswith("OHE_")]

df["sub_phrase_sum"] = df.apply(lambda x: sum([x[col] for col in ohe_cols]), axis=1)
```
```python
In [518]: df.sort_values(by="sub_phrase_sum", ascending=False)[["score", "sub_phrase_sum"]].iloc[:20]
Out[518]: 
         score  sub_phrase_sum
6975  0.527562              22
14    0.506731              22
34    0.497934              22
33    0.497934              22
32    0.497934              22
31    0.497934              22
6970  0.553183              22
3490  0.601307              22
3489  0.619125              22
3488  0.619125              22
3487  0.619125              22
3486  0.619125              22
3484  0.641208              22
6971  0.553183              22
6972  0.553183              22
10    0.509944              22
6973  0.553183              22
6968  0.593046              22
6969  0.578265              18
36    0.495994              18
```
can maybe have a correlation metric here say ,

### [[Aug 24th, 2023]] embeddings are not unit vectors?
Are #[[embedding space]] vectors all unit vectors ?? Therefore [[cosine similarity]] is being taken between unit vectors so equivalent to [[dot-product]] ?

Using embeddings from an earlier draw,
```python
In [522]: np.linalg.norm(embeddings[0,:])
Out[522]: 1.690175
```
weird I guess they are not unit vectors.
```python
In [537]: sorted([np.linalg.norm(embeddings[i,:]) for i in range(embeddings.shape[0])])[-10:]
Out[537]: 
[2.4754915,
 2.4754915,
 2.4754915,
 2.4868407,
 2.548294,
 2.5493302,
 2.5712116,
 2.5787024,
 2.5803518,
 2.5848124]

In [538]: sorted([np.linalg.norm(embeddings[i,:]) for i in range(embeddings.shape[0])])[:10]
Out[538]: 
[1.3734428,
 1.3868212,
 1.4120256,
 1.4284494,
 1.4339207,
 1.4454004,
 1.4503047,
 1.4520775,
 1.4637629,
 1.4657506]


```
the magnitudes to seem to be small though.

ok