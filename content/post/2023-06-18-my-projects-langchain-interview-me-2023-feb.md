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
![image.png](../assets/image_1689873985593_0.png)
new language,
new characters ( with accents)
new domain (medical, technical, legal)
new style (haha like [[Old English]] or [[Old French]] )
#take-away ohhh and #moment/aha a really good example is explained that a tokenizer unfamiliar with a #corpus  will excessively split and that is not good because #[[input sequence]] is limited [[context-window]] [[maximum-context-size]] !
And so you will risk not capturing the full sentence you want to pass to a #LLM . Nice.
Excessive tokenizer splitting, can impact model performance, too, #question #card , why though?
Maybe the argument is similar to like "<UNK>" those unknowns, in that there is less information being captured. My intuitive reasoning is that tiny subwords embedding representations will be likely meaningless . The #attention will get thrown off by basically letter chunks that will end up being as common as the word "the" , so perhaps you will have just #stop-words at that point with low information.
Example of this particular model tokenizer missing a lot of #unicode characters from [[Bangla]] #language-type . 
![image.png](../assets/image_1689874273026_0.png)
And yea [[out-of-vocabulary-words-OOV]] "<UNK>" , has no useful information for the model to use there.
And [[excessive splitting by tokenizer]] , for say #[[biomedical Glossary]]
![image.png](../assets/image_1689875286166_0.png)
And for the other example given, of using `code-search-net` python dataset to train a tokenizer, I like the question that gets asked is [[performance-lift]] at least eye-balling. And in below example, she does show it is desirable to capture a concept as one token, but I think this will ultimately only happen if that example is more frequent , relative to other patterns when doing merges per  [[byte-pair encoding]]
![image.png](../assets/image_1689875776287_0.png)
![image.png](../assets/image_1689875808385_0.png)



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


ok
