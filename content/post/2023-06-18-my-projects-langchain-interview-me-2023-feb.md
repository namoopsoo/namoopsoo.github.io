---
date: 2023-07-12
title: langchain interview me 2023 feb
---
type:: #project-type
status:: #in-progress-status


## Note
This is not a blog post but kind of a landing page I'm using to aggregate on-going project notes here

## Vision
Broadly would like to do here something like the following
### compare against arbitrary #job-listings , #job-description ,
And [[my projects/personal/langchain-interview-me-2023-feb]] , also now the repo usable by anyone who wants to compare their #brag-document to #job-listings [[job-description]] out there , get a delta , and more broadly , understand say , their industry posture , since that’s a moving target . And you can interview yourself too haha .

I can use the [[my projects/personal/langchain-interview-me-2023-feb]] stuff concepts to see , what roles online do I align with and am I progressing towards them at #Humana or stagnating?

### Making updating your #brag-document like a #fun-factor #[[having fun]] experience 😀
### And original intent was a UI to actually ask questions
### Also better #TellMeAboutYourself , #[[tell a story]] . Since the #brag-document has lots of cool stories, and also #chronological-story , this could be a cool way to weave together the personal story.
And for [[my projects/personal/langchain-interview-me-2023-feb]] thing, so I was in this [[May 28th, 2023]] too. Would be cool to make it easier for an individual to construct their [[TellMeAboutYourself]] since this is so important and at least to myself cannot rely on my memory haha


## my blog posts
### initial post with the #question-answer-task
20:55 So I have the #blog-post from [[Feb 18th, 2023]] [here](https://michal.piekarczyk.xyz/post/2023-02-18-first-stab-langchain-interview-me/), where I put together my technical background , create embeddings from them and run a #question-answer-task #langchain , with one of the chains called "load_qa_with_sources_chain" that gives intermediate source text results too.

## Also this one
[[blogpost/2023-06-25-everybody-loves-reynauds]] https://michal.piekarczyk.xyz/post/2023-06-25-everybody-loves-reynauds with a comparison across a few embedding models, to suss out which of them do or do not have medical vocabulary
## research
### went through that [[article/Getting Started With Embeddings]] , which was useful to start learning about #sentence-transformers library
And more recently, I went through the #[[hugging face]] example around #Medicare and with the #article-type ,  [[article/Getting Started With Embeddings]] , [link](https://huggingface.co/blog/getting-started-with-embeddings),

And used the  "langchainz" virtual env I have, and I used the https://api-inference.huggingface.co REST API specifying to use the "sentence-transformers/all-MiniLM-L6-v2" model to produce embeddings , and then the   #sentence-transformers library,  `semantic_search` , ( `from sentence_transformers.util import semantic_search` ) , to a question to a set of frequently asked questions
### I have this question, is the #sentence-transformers #average-pooling noisy?
### Can I use better #NER [[Named Entity Recognition NER]] ?
Maybe help from https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da ?

## attempts
### on [[May 28th, 2023]], I started defining the #job-description comparison concept, and I ran a comparison of my blurb "2023-02-19T011846-the-story-blurb.txt" against "2023-05-28-enigma-mle.txt" . The results were maybe somewhat not easy to read. Perhaps a lot of text. Maybe I need shorter sentences?
21:50 okay here's a quick example,

```python
import torch
import json
from pathlib import Path 
import os
import requests

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
#### noticed that the paraphrase mining output is not full
looks like more or less we get the better matches first
#### the model I'm testing with does have technical data sources
08:56 haha this is not simple, so many sentences, is there any way of getting around hand labeling?

Maybe I can look for technical terms which I suspect are not part of the #vocabulary , hmm
So https://huggingface.co/datasets/code_search_net and [[stack exchange]] duplicate questions and actually many other technical datasets are used per https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 ,
#### hmm oh the AutoTokenizer is a way to get tokens and vocabulary in the model
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

