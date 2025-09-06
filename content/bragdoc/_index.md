---
title: Careerlog
robots: noindex, nofollow
--- 

## Built infrastructure to serve my company’s first ML underwriting model in 2015, using Redis + Django to deliver real-time predictions., (2015)
When I joined my first ML startup in 2015, we barely had any customer data—so our early system relied entirely on heuristics. By the time we landed our first paying customers, I volunteered to take a stab at training our first real model from the new data we’d started collecting.

Coming out of school, I knew ML theory but not practice. I reached for Weka (which I’d used academically), unaware that scikit-learn was already the industry standard. My results were underwhelming compared to those of a newly hired Data Scientist, who had prior experience and quickly outperformed me. Looking back, it was a humbling and pivotal moment: my academic background didn’t directly translate into production-ready applied ML.

I learned scikit-learn from him, and with the data we had—default customer data plus our first provider—I trained my first Random Forest model. While my colleague’s model ultimately won on AUC and was chosen for deployment, I contributed by building the infrastructure to host it.

I used Redis to cache the model, integrated it into our Django web server, and wrote the glue code to call `predict_proba` on new prospective customer data. This supported underwriting decisions in real time. To manage multiple models, I keyed them by retailer, allowing us to segment and transition more deliberately as we added new versions.

Though humbling, it was a defining career moment: a hands-on education in the difference between academic ML and applied ML, and my first experience building real infrastructure to bring a model into production.


## Transformed Twilio from a messaging provider into a data source, analyzing prepaid vs. VOIP numbers and deploying a non-fixed-VOIP feature as a business rule to reduce default risk., (2017)
While working with Twilio for SMS processing, I noticed that Twilio also sold data on phone numbers, and I saw an opportunity to use it as a new data provider. I built features designating numbers as prepaid or VOIP (fixed vs. non-fixed) and tested their predictive power against default behavior.

My initial hypothesis was that prepaid numbers would be most predictive of risk, but the analysis showed otherwise: non-fixed VOIP numbers—those not tied to a physical address—were far more indicative of default likelihood. To measure the impact more meaningfully, I also introduced dollar delinquency metrics, going beyond simple binary default labels to weigh financial outcomes directly.

Based on these findings, we productionized the non-fixed VOIP signal as a business rule. The decision was supported by retroactive analysis, which showed that the dollar loss from the false positives was roughly 2:1.

This project reframed a familiar tool—Twilio, previously just a messaging API—as a valuable source of risk data. By turning it into a feature provider, I was able to collect, analyze, and validate new insights, then persuade others with ground-truth evidence to incorporate it into our modeling and decision processes.
...


## Explored separating potential fraud cases from default data by excluding single-payment histories, learning that more precise chargeback signals would be needed to improve model performance., (2017)
In our early credit default modeling, we treated all defaults as a single class without distinguishing the reasons behind them. I suspected this approach introduced noise, since some cases—like customers who only ever made a single payment—might actually represent fraud or identity theft rather than true payment default. Including these cases in training data could pollute the model, because fraud risk is distinct from default risk.

To test this idea, I engineered a new target variable, "only the first payment was made", and built a version of the default training set that excluded these cases. The goal was to see if this cleaner dataset would improve predictive performance. After training models on both datasets, I found that removing single-payment cases produced no measurable improvement in AUC.

Reflecting on this, I realized the limitation was potentially my lack of access to actual chargeback signals—concrete evidence that a payment default was tied to identity theft. Without that level of precision, excluding single-payment cases may have been too blunt an instrument to improve the model.

Although I chose to stop the effort rather than invest further without better data, the experiment reinforced an important lesson: fraud and default are not interchangeable signals, and future work in this area should focus on higher-quality chargeback data to more accurately separate the two.


## Decoupled underwriting ML pipeline from monolith into a SageMaker + Lambda microservice, enabling faster, safer model deployments with Dockerized scikit-learn and XGBoost., (2018)
At one point, our underwriting models were too tightly coupled to the company’s monolithic application. Feature engineering was abstracted behind layers of object-oriented code, making bugs hard to isolate. Even small changes required redeploying the entire monolith—an error-prone process that risked outages (and had already caused them).

To break this bottleneck, I designed and implemented a microservice-based approach using AWS SageMaker and Lambda. I began by containerizing one of our existing model artifacts, building a Docker-based pipeline that handled both feature preprocessing and model serving. From there, I rewrote the feature engineering code in a functional style, added unit tests, and integrated the service with an AWS Lambda + API Gateway stack. This allowed us to call SageMaker endpoints from Lambda for real-time predictions.

The decoupling effort gave us critical flexibility: the Dockerized approach supported both scikit-learn and XGBoost models, and by splitting our underwriting stack into its own Git repo we reduced shared dependency conflicts with the monolith. Over many months of iterations and deployments, this system proved stable and significantly improved our ability to test, deploy, and evolve models independently.

Along the way, I encountered and fixed issues typical of building new infrastructure. One memorable debugging moment—the “Sweetgreen story”—involved accidentally caching QA database connections globally, which risked being reused in production Lambda calls. I caught the bug while debugging at a Sweetgreen restaurant, removed the global variable, and ensured environment isolation going forward.

This project was one of the first major steps in transforming our underwriting ML stack from brittle, tightly coupled code into a modular, testable, and resilient production system.


## Resolved an out-of-memory issue during Databricks runtime upgrade by replacing a costly nested one-hot encoding loop with a streamlined manual transformation., (2022)
As part of upgrading our hosted model repositories to the Databricks 10.4 general release runtime—both to access new optimizations and because earlier runtimes were approaching end-of-support—I encountered an out-of-memory error in the feature engineering step of one repository.

The root cause was a combination of Databricks’ native OneHotEncoder and a custom double-nested for loop that iterated over hundreds of columns and their values to produce additional one-hot encodings. In this model’s case, the final feature set had already been selected, leaving only about 15 relevant columns. I opted to bypass the nested loop entirely and manually code the one-hot transformations for this small set.

While I initially considered switching to Spark’s built-in one-hot encoder, the existing code relied on a custom naming convention for new columns, which made a direct swap impractical. By unrolling the loop and explicitly writing the transformations, I eliminated the driver-side processing bottleneck, removed the memory issue, and enabled the model pipeline to run successfully on the newer Databricks runtime.


## Resolved a production pipeline failure in a 6-model chain caused by a dependency CVE and undeployed code changes, restoring all jobs through targeted fixes and coordinated rollbacks., (2023)
While on on-call support, I handled a production failure in a six-model repository chain. The issue began when the first model in the chain failed during its scoring step due to a high-severity CVE in the shared protobuf dependency between TensorFlow and MLflow. Installing the package crashed, and the immediate fix was to unpin the problematic version, allowing a secure, compatible version to be chosen. This worked in staging, and I deployed the fix to production.

However, once deployed, the downstream model (“model-2”) failed because it could not find an expected output path (old-path). Investigation revealed that on 2022-11-01, pull requests had been merged for all six models to standardize artifact output locations from old-path to new-path—but these changes had never been deployed to Databricks. The dependency fix PR effectively made “model-1” the first in the chain to write to the new path, while the remaining models still ran pre-November 2022 code expecting the old path.

To address this, I deployed the long-stalled November 2022 changes for the other five models. This led to a new failure in “model-2”: a Unable to infer schema for parquet error, indicating the expected artifact directory existed but was empty. It became clear the undeployed November 2022 code had never been properly tested, and the lack of an end-to-end integration test for the full chain had hidden this bug.

Given the proximity to the next scheduled run, I rolled back all six models to their pre-November 2022 state, keeping only the protobuf dependency fix in “model-1.” This restored successful execution for all pipelines in production on 2023-01-10, with all score outputs materializing correctly.

The incident highlighted several systemic gaps:

No reliable end-to-end integration testing for the full 6-model chain.

No automated mechanism to detect merged code that was never deployed to Databricks.

Long-running model repos that aren’t exercised often enough to catch latent issues.

Dependence on volatile datasets in feature engineering, which could benefit from frozen dataset snapshots to isolate code change impacts during integration tests.


## Introduced an explicit-parameter execution approach with dbutils.notebook.run in Databricks notebooks, replacing the long-standing %run global pattern and significantly reducing variable errors and wasted debugging time instead producing clear, isolated job outputs., (2022)
In our Machine Learning Platform at Humana, we host a Databricks Spark feature store, and I led an initiative to modernize how our notebooks are executed. Historically, notebooks were chained together using %run, which assumed the existence of global variables. This approach caused problems with code linters (due to undefined variables) and made debugging difficult, since only print statements and incomplete stack traces would appear in parent notebooks.

I began converting our notebooks to use dbutils.notebook.run, which allows explicit parameter passing and provides full contextual input/output when running child notebooks. One major challenge was ensuring that large Spark DataFrames could be safely passed between notebooks. Unlike %run, where globals are directly shared, dbutils.notebook.run requires a different mechanism. I discovered that Spark’s global temp views could be used to pass DataFrame references across caller and callee notebooks within the same JVM. While the documentation only demonstrated this with toy examples of a few rows, I successfully validated the approach at production scale, handling millions of rows across multiple DataFrames with reusable code. Interestingly, when I discussed this method during a Databricks office hour, even the Databricks team admitted they hadn’t seen this “hidden gem” of functionality in practice before.

To roll out the change safely, I built a standalone Azure Data Factory job that acted as a 3-way QA comparison. For each notebook under test, it would:
1. Run the current master branch with %run (baseline).
2. Run my new branch still using %run (backward compatibility check).
3. Run my new branch with dbutils.notebook.run (new approach).

It then compared all DataFrame outputs across the three runs to confirm that behavior remained consistent. This systematic approach gave the team confidence that the migration was safe.

A bonus outcome of using dbutils.notebook.run was the ability to introduce end-to-end integration tests for our production feature notebooks. Previously, our CI/CD pipeline only tested isolated functions. Now we could validate the entire notebook flow, improving trust and reliability in continuous integration.

In summary, this effort proved that production-grade Databricks notebooks don’t need to rely on hidden globals via %run. By switching to dbutils.notebook.run, we introduced rigorous isolation, parameterized execution, backward-compatible safety checks, and stronger end-to-end test coverage, while retaining the benefits of distributed Databricks workflows.


## Enhanced model repo integration tests with histogram visualizations and population drift checks, reducing troubleshooting time and improving clarity on score deviations., (2022)
Previously, our model repository integration tests summarized differences between code changes and reference outputs with only a single mismatch count. While this number flagged deviations, it gave little insight into how far off the scores were, or why.

I introduced a visual layer to these tests by generating histograms of score distribution differences. Seeing the full distribution provides richer context: you can quickly judge whether differences are minor shifts or major drifts, which accelerates troubleshooting. In addition, I added an outer join by the primary key so that we can now detect when the population itself has changed. This is critical, because if the scored population has drifted, the differences are due to new or missing source data—not code changes.

Together, these improvements reduced the time spent diagnosing integration test failures and provided more direct evidence about the scale and nature of deviations. They also made it easier for data scientists to distinguish between genuine code impacts and external data changes, which helps preserve trust in the test suite.


## Added stable-baseline score comparison in integration tests to isolate code changes from shifting source data, improving reliability and trust in results., (2022)
Our ML platform standardizes how Databricks model repositories are structured, with feature engineering notebooks gathering data and scoring notebooks producing outputs with potential business value. Integration tests play a key role in ensuring that code changes don’t alter model outputs in unintended ways. This is especially important because data science is iterative—teams often ship working ML code early to deliver business value and then refine for speed and efficiency over time. Reliable tests let us move quickly without introducing defects.

However, our staging environment didn't fully protect input data from upstream changes. This meant that even small code changes could produce large, unexplained deviations in integration test scores. In practice, it was impossible to tell whether differences came from code or from changing source data. Resolving these cases often required lengthy back-and-forth with repository owners, or ad-hoc updates to stored “original” output scores—an exception-prone process that undermined trust in the results.

To address this, I introduced the ability to save and reuse output scores from the most recent stable code commit. Now, integration tests for a pull request compare the new code's outputs to those from this stable reference, rather than to potentially stale “original” training outputs. This change removed the noise from upstream data shifts, allowed clearer attribution of differences to code changes, and eliminated the need to escalate unexplained results back to the original modelers.

The update not only improved confidence in test outcomes but was also highlighted by colleagues and our product owner as a simpler, more transparent process for the wider community of data scientists on our platform.


## Introduced Databricks Repos for shared integration test code, enabling pythonic imports, pytest in notebooks, and eliminating copy-pasted test logic across 100+ model repos., (2022)
To reduce repeated code across our ~100 model repositories, I introduced the use of Databricks Repos for automated job code—starting with our integration tests. Previously, identical test logic was manually copy-pasted into each repository, and our deployment approach with databricks workspace import_dir was verbose, unintuitive, and made it unclear where a given notebook originated.

With Databricks Repos, we can now mirror a Git repo directly into Databricks, allowing pythonic imports, more readable and testable code, and better linting. I focused first on integration testing as a proof of concept for broader production use. I used an existing central repo to add the centralized integration tests, and made this central repo now deployable to arbitrary workspaces, and demonstrated the first example of running pytest inside a Databricks notebook on imported modules. I also generalized the deployment yaml and it was adopted for deploying other repositories on our platform as well.

This shift not only removed duplicated test code but also made the deployment process simpler, more intuitive, and more maintainable. While there’s still room to expand the “Databricks Repos” approach to other parts of the platform, all model repository integration tests now use this new pattern.


## Contributed preprocessing, prompt engineering, and system integration to a team hackathon project on health plan documents, while also delivering an early fallback RAG-style demo., (2023)
During a 2.5-day internal hackathon, I joined a small team focused on applying LangChain and GPT to health insurance plan documents. These documents are highly tabular and difficult to parse, so on the first day I experimented with manually restructuring raw PDF text into contextual sentences. While time constraints kept me from automating this fully, it helped hedge against LangChain’s default handling of dense table dumps and may have improved the clarity of responses.

At the same time, I explored prompt engineering around empathy, since health plan Q&A could benefit from a friendlier tone. With minimal changes, I was able to shift answers toward warmer, more approachable responses, even experimenting with light backstories for context.

To ensure we’d have something working by the deadline, I also built a fallback demo loop: directly injecting parsed plan text into LangChain prompts for basic question answering. Meanwhile, teammates created separate Gradio apps—one for Q&A over embeddings stored on Hugging Face, and another for speech-to-speech interaction. I played a key role in integrating these efforts, gluing the two systems together into a unified demo that allowed both chat and audio-based Q&A over plan documents.

Although we didn’t measure accuracy improvements from my early sentence wrangling, from what I saw it was anecdotally clear to me that existing PDF-to-text tools lost the original context with table-heavy documents, so  I am curious to better measure this impact in the future.


## Advanced our Databricks modularization effort by maturing a shared Python package, adding testing, and pitching adoption as an internal OKR to reduce duplication and troubleshooting overhead., (2024-???)
As our Databricks-based ML platform grew, each model repository bundled not only feature engineering and scoring notebooks but also duplicated support code—installing packages, creating MLflow experiments, authenticating, configuring pipeline parameters, defining ingress data sources, and managing deployment YAML. This copy-paste approach meant every update required manually propagating changes from a template repo into many others, which was unsustainable.

Following a successful mini hackathon where colleagues began packaging common utilities into a shared Python library, I joined the effort to bring it to a higher level of maturity. My contributions included expanding test coverage, transitioning existing tests to pytest, and improving resilience as the shared code evolved. I also wrote a clear, compelling README to document usage and encourage adoption.

To build momentum, I collaborated with a colleague to pitch the initiative as a bottom-up internal OKR. We emphasized how modularizing platform utilities would simplify user-facing code, reduce repeated effort, and lower troubleshooting time. By formalizing the vision and contributing maturity work, I helped establish the foundation for shared abstractions to replace repeated notebook boilerplate.


## Standardized integration test code by introducing our shared internal Python library, replacing scattered custom logic with a uniform platform package.
, (2024-08-23)
Our ML platform’s integration tests had accumulated scattered custom Python code across different repositories, which made them inconsistent and harder to maintain. After we introduced a centralized internal platform library, I refactored the test code to use this package. This reduced duplication, brought consistency to how tests were written, and ensured they followed shared best practices—making the framework easier to maintain and extend.


## Integrated Sphinx-generated docs into our Hugo wiki, creating an accessible workflow for publishing ML platform library documentation., (2024-?)
..
Inspired by a colleague experimenting with Sphinx to generate documentation for one of our core ML platform libraries, I explored how we could make that documentation more easily accessible to our internal users. Since our internal wiki is built with Hugo, I tested whether the HTML output from a Sphinx build could be served directly in the wiki’s static section. The experiment worked seamlessly.

Building on this, I documented a clear process for running Sphinx builds and publishing their output into the Hugo wiki, making it quick and repeatable for others. This allowed our team to maintain high-quality, automatically generated reference material within the same platform our users already relied on for guidance.

After publishing the first iteration of the Sphinx-based docs, I began sharing them with users, who responded positively. The impact was that for the first time, we had a more structured and accessible way to point our internal community toward up-to-date documentation for our Databricks ML platform package—improving discoverability, reducing friction, and helping data scientists ramp up more quickly.


## Improved CI/CD for our new shared Databricks utility package by unifying test/deploy steps and parameterizing test clusters for concurrent development by multiple people., (2024-?)
A colleague had a great idea to consolidate our commonly used, user-facing utility code—previously copy-pasted across projects—into a new shared Python package, with a Twine pipeline to build and deploy it to our internal package repository. I saw an opportunity to build on his work by strengthening and generalizing the CI/CD pipeline he created.

Originally, the CI and CD steps were not fully aligned. Certain parts of deployment could fail because they weren’t being accurately tested in CI. I refactored the pipeline to make CI and CD more consistent, ensuring the same validations applied across both. This reduced the risk of runtime deployment failures and gave the team more confidence in the release process.

Another issue I addressed was scalability for multiple contributors. Early on, only a few people worked on the package, but I noticed a clash when a colleague and I ran feature branches against the same shared test cluster. To solve this, I parameterized the CI test code so that each feature branch would spin up its own isolated test cluster. 

Also, crucially, I parameterized the .whl file being created and the init script installing the .whl file as well.

This eliminated collisions and made it possible for several developers to contribute in parallel without stepping on each other’s work.


The result was a more resilient, reliable, and developer-friendly CI/CD process, which enabled the team to iterate faster on our new shared Databricks utility package. By stabilizing the pipeline and supporting concurrent development, I helped establish a foundation for this package to become a central, reusable resource across our ML platform.


## Introduced modular Python coding in Databricks 11.3 by enabling multi-file module imports and updating deployment pipelines to support plain files, moving beyond %run globals., (2024-01-23)
With the release of Databricks 11.3, our ML Platform gained a new capability: workspaces could now host not just notebooks, but also plain Python files. This opened the door to more modular, Pythonic development practices. Previously, our notebook code often relied on %run statements to pull in helper functions, which polluted the global namespace and discouraged clean module design.

I took the initiative to explore how far the new functionality could go. While Databricks’ documentation only described the simplest case—a single .py file—I tested whether it would support more complex structures. I confirmed that nested directories of Python files with __init__.py could indeed be imported as full Python modules, enabling us to organize code more professionally.

To prove the approach, I introduced this modular style into one of our model repositories, replacing %run calls in a feature engineering notebook with imports from a local module. To make the pattern sustainable, I extended our Azure DevOps deployment pipeline to automatically detect such modules in Git repositories and recursively push them into Databricks workspaces using the newly available Databricks SDK. This was a significant improvement over the old Databricks CLI, which had no support for plain files.

After successfully applying this pattern to a few additional repositories, I shared the results with colleagues. Interest grew quickly, and others began to adopt the approach. The impact was a meaningful cultural and technical shift: our team could now move away from hidden global-variable hacks and toward cleaner, modular, and maintainable code.


## Introduced workspace file access in Databricks 11.x to unify redundant JSON and notebook configs, reducing duplication and black-box %run dependencies., (2024-?)
On our Databricks-centered ML platform, we version control ML pipeline notebooks and JSON settings in Azure Git. For years, a redundancy existed: each repository included a JSON settings file (with cluster runtime versions, integration test parameters, etc.) and a Databricks configuration notebook (defining blob ADLS storage paths and other setup details). The overlap was awkward, as both JSON and notebooks contained key metadata, forcing duplication and reliance on %run calls to bring in opaque configuration code.

With the release of Databricks 11.x, which added Pythonic access to workspace-resident arbitrary files (not just notebooks), I created our first wrapper to directly load repository JSON into notebooks. This marked the first step toward reconciling the two configuration styles. By doing so, we began reducing both duplication across ML pipeline repos and the dependency on %run-based configuration notebooks, which couldn’t be linted and were difficult to maintain.

Although the full migration required incremental effort across many repositories, this initial wrapper established the conceptual shift: moving from redundant, black-box configs toward a single, maintainable, lintable source of truth for pipeline metadata.


## Eliminated template sprawl in our ML deployment system by centralizing and parameterizing ADF logic across staging, prod, and feature variants, from 16 templates to 1., (2023-03-20)
within our ML platform, we were supporting the onboarding deployment and running of 100 plus git repo based models and in our deploy design, we had a large amount of duplication. we had the same Azure DataFActory ADF arm template duplicated with respect to the existance or non existance of a databricks notebook used for measuring feature importance , and also w.r.t. a notebook used to save output data in a certain way . And this was bifurcated yet again w.r.t. staging and production, so there were therefore a total of 2x2x2 = 8 copies of essentially the same arm template with small tweaks. And on top of that, I was about to introduce another bifurcation w.r.t. a databricks notebook used to build ground truth data. So instead I took this opportunity, to actually pay down the tech debt and I parameterized all the arm templates so instead of 2x2x2x2 = 16 copies there was now only 1. On top of that, another area of duplication was that the json templates  for the different variations of arm templates parameters existed in all of the 100+ model repositories. And I removed this so the logic was now getting handled in our centralization repository instead. So therefore now both the deployment centralization code and the model repository code was simpler and leaner.

## Productionized feature drift monitoring across ~18k features with scheduled Databricks/ADF jobs, CI smoke tests, and multiple drift algorithms, providing monthly situational awareness of drifting features., (2023?)
Building on a colleague’s earlier proof-of-concept with the Deepchecks library, I implemented a production-ready feature drift monitoring system for our ML platform. The goal was to provide recurring visibility into how clinical and other features in our feature store change over time, since drift can indicate data quality issues or modeling risks.

I formalized the code to run in Databricks and scheduled it with Azure Data Factory as a monthly job. The job can process multiple lines of business in parallel, parameterized by feature groups and historical comparison windows. To make testing practical, I added options to run on only a subset of features, which enabled a fast smoke test used in CI. I also added frozen drift data for CI validation, which helped me catch and fix a production bug early in the rollout.

The system supports configurable sample sizes (e.g. 10k vs. 100k rows) to compare sensitivity, and it parameterizes the drift algorithms used. For numerical features, we run PSI and the Kolmogorov–Smirnov test; for categorical features, we use Cramer’s V and Earth Mover’s Distance. Across ~18k features, the output is a ranked list of those most likely to be drifting.

While the internal marketing needed to promote user adoption has not yet happened, the job has been running in production for about a year, generating monthly drift reports. So at least the first step has been achieved: creating a systematic, repeatable way to detect and rank feature drift, giving us better situational awareness of the stability of our feature store.


## Explored adjacent ML platform technologies (Kubernetes, Dask, Polars, distributed vs. GPU learning) to broaden perspective beyond Databricks, and shared findings in an internal tech talk and blog post., (2024-09-05)
Since much of my work centers on Databricks, I set out to broaden my perspective by surveying adjacent ML platform technologies. My goal was to identify blind spots and better understand tradeoffs between distributed data processing and GPU-based training. I reviewed available solutions including Kubernetes, Dask, and Polars, and considered their scalability, strengths, and limitations.

I learned that hybrid approaches combining GPUs with multi-node training exist, and that strategies like parameter servers are used when model weights exceed GPU memory. I also confirmed that Databricks has shifted away from supporting distributed training directly, instead emphasizing Spark for data transformations and deferring training workloads to multicore libraries like TensorFlow and PyTorch.

An interesting observation was that both Dask and Polars explicitly caution against use on datasets larger than ~1 TB, recommending Spark in those scenarios. These comparisons highlighted how different tools position themselves along the spectrum of data size and training complexity.

To share what I learned, I participated in an internal knowledge-sharing talk across teams, and published a rough first-draft blog post documenting my findings, here, https://michal.piekarczyk.xyz/post/2024-08-29--architectures/. The exercise not only improved my understanding of alternatives to Databricks, but also sparked useful conversations with colleagues about when and how we might apply these tools in practice.


## Automated monthly drift monitoring for clinical condition prevalence data, modularizing the code and reducing manual effort previously required., (2024-12-05)
Our ML Platform’s feature store contains a large amount of clinical data, including prevalence of conditions for our member population. To monitor data quality, we track prevalence rates over time and raise alerts when they shift unexpectedly, since such changes may indicate upstream issues. Previously, this drift monitoring was performed manually on a laptop using a CLI utility I had written.

To improve reliability and reduce manual work, I restructured the code into a clearer, modular design and automated it as a scheduled monthly job. The job samples condition prevalences over recent time series and produces drift information automatically, shortening the turnaround time for spotting and reacting to issues.

While some manual steps remain—such as opening a pull request when drift is detected—the automation has already reduced overhead and made the process more consistent. Longer term, the next step will be to fully automate those remaining tasks, but this milestone established an important foundation by moving from ad-hoc laptop runs to a reliable production job.


## Embedded Git commit hash into our databricks ML platform Python library (__build__), enabling precise traceability in CI/CD, testing, and production., (2024-12-09)
To improve traceability in our databricks ML platform, I added the Git commit hash as a member variable in our internal Python library. During CI/CD, the build process now automatically retrieves the current commit and stores it as a dunder attribute (e.g. __build__).

This small change has a big impact: it eliminates ambiguity about which code version is being executed. During both testing and production troubleshooting, the team can now reliably confirm the exact commit tied to a given library build. This makes debugging faster, improves confidence in deployments, and reduces the risk of running code that isn’t clearly identified.


## Designed and deployed a pgvector + PostGIS–based semantic search for restaurant dishes with geospatial filtering and optimized embedding storage, achieving 20× storage savings through selective embedding strategies., (2024)
I had the task of  building out semantic search on top of a restaurant dish corpus so that a user at a given location can free form type some kind of food and they can see the restaurants that match nearby, based on the specific dishes that matched the query at those restaurants. The first iteration of this task, was a pgvector implementation, with embeddings at the level of menu-subsets of dishes that each restaurant has, meaning that each restaurant has several menu-subsets where each subset can have 10 to 20 dishes, say, and these dishes were concatenated into blobs and those were embedded.  The end user accessible API took a latitude, longitude as well as a free form query. And the result was a ranked list of dishes and the restaurants they are available at, constrained by the location identified by the location given.

This project had many components, but began with taking an off the shelf embedding model, embedding a corpus of menu data into postgresql pgvector, along with a table of locations of restaurants and their postgis locations. A postgresql query was constructed, first with the relevant postgis subset as a CTE, since that was faster and then calculating the cosine similarity of the menu blobs with the target query and ranking that.

Then on the fly, embedding for individual menu items were calculated for the subset, in software. The reason here was that the pgvector data was actually really huge and by only storing the menu sections embedded, there was a 20x savings and the runtime embedding of the small under 100 typically subset was still reasonably fast and can be done as a second API call after a initial list of restaurants is populated for the user first.


## Developed a golden dataset and search evaluation suite to validate embedding models for semantic dish search, enabling a cost-saving model switch., (2025-01-11)
during the process of delivering a semantic search capability around a restaurant dish corpus, I took a detour to evaluate a 3rd party hosted solution, typesense, and I took this opportunity to develop a golden dataset for the search problem because my particular open source embedding model was not available on typesense, and I needed a good way of objectively comparing models. I ended up writing helper code to make it easier to build such a dataset and I built out evaluation code using the two tried and true algorithms, Mean Average Precision (MAP) and Mean Reciprocal Rank (MRR). Ultimately I was able to show that embedding model available on typesense that I was targetting was at least as good as the other one I was using and this was really impotant because it was a 768 as opposed to a 384 dimension model meaning I had evidence that half the cost was good enough for at least an equivalent result. And this gave motivation to continue building a larger golden dataset to get even more confidence about the choice.

## Enhanced semantic search validation by doubling dataset size and adding Precision@10, confirming the hosted model’s slight edge over baseline., (2025-02-01)
continuing the effort to help validate typesense embedding models as an alternative, I roughly doubled my golden evaluation dataset and introduced another strong evaluation metric, Precision@K=10 , into my existing suite of MAP and MRR. And good news is that now with more a larger evaluation dataset I could see that the new candidate embedding model was actually slightly outperforming the previous one. I am aware however that although these are strong industry standard information retrieval metrics, they are still proxies to business metrics which I do not have and would only be available through true customer facing a/b testing which I do not have yet but I felt the need to at least an initial method of evaluation before we can start testing with actual customers.

## One-line fix, six-month mystery: restored Git commit tagging in our ML deployment flow with a tiny tweak to the pipeline.


Traced and fixed a subtle bug that had silently broken Git commit injection in our ML deployment pipeline for over six months.
, (2025-03-07)
in our ml platform, we use a common deployment pipeline when updating ml pipelines and part of that is we have a step in the yaml deploy that during the deployment, takes the git commit hash and within databricks notebooks, replaces template placeholders with the actual git commit. there was a bug which for well over half a year caused this not to work and I made a simple update , just literally one line changing from one version of the Azure devops pipeline replacement function that did not work, to another that did work, and then boom fixed it. just no one else had noticed it maybe or no one else found the time to debug it troubleshoot it haha.

## Added histogram overlays by cohort to model integration tests, providing clearer visual evidence for troubleshooting score deviations., (2025-04-16)
To improve our model integration tests, I added histogram overlays that show output score distributions separately for each cohort. Previously, we only inspected delta difference distributions, which sometimes made it difficult to judge the scale or significance of deviations. In one case, I found that differences within a narrow score band were not obvious in the existing view, but overlaying the distributions made the impact clear. By incorporating this visualization into our standard tests, I created a more effective way for the team to diagnose whether observed differences were meaningful, improving confidence in code changes.


## Rebuilt and validated a legacy heart failure model with updated dependencies, preserving 99.9% fidelity and restoring it to production., (2025-04-?)
There was a model on our platform predicting the progression of coronary heart failure for our members, at risk of becoming defunct because of package dependencies and typically we hand this back to the person who built the model, but instead I tracked down the training data and training code, wrote a concise version of the training with newer dependencies, showed how to reproduce the full pipeline along with validation that demonstrates the new model produces 99.9% equivalent outcomes, got a vote of confidence from the original modeler and deployed this to production.


## Improved model repo integration tests by introducing top-driver recall as a clearer metric and fixing a join bug that masked missing feature drivers., (2025-05-13)
When we update model repository code, we run integration tests that compare new scores and their top feature drivers against reference outputs. Previously, we measured differences in top drivers by looking at absolute changes in unitless “impact” quantities. In practice, this was unintuitive and didn’t make it easy to understand whether the same drivers were being preserved across versions.

I introduced a clearer approach by calculating the recall of top driver features. For example, if a scored row has five top drivers but only four of those are still present in a new run, the recall is 0.80. Averaging this across rows provides a more interpretable measure of driver consistency between branches.

While implementing this, I also discovered and fixed a bug: our tests used an inner join on features, which meant that missing drivers were silently dropped rather than penalized. By switching to a left join, we could correctly capture cases where recall fell below 1.0, ensuring that shifts in top drivers are properly surfaced.

These changes made our integration tests both more intuitive and more accurate, reducing the risk of overlooking significant differences in model behavior.


## Automated ML platform repo search setup with a Bash script and screencast for the wiki, eliminating manual credential updates and data fetch steps., (2025-06)
In our Git-based ML platform, new repositories are frequently added and removed, making it valuable to search them directly via the file system. Previously, setting up for such searches required a manual series of steps: updating temporary Git and Databricks credentials, and fetching the latest intake CSV containing new business data. I created a Bash script to automate these steps, guiding the user through the setup without needing to remember specific commands, thereby reducing cognitive load and startup time. The script syncs all relevant repositories for immediate use, and I recorded a video screencast to walk through the setup process for easier onboarding.


## Simplified Databricks package cache updates by replacing a convoluted streaming/event-hub setup with a clear client–server design and a scheduled Azure DevOps pipeline., (2025-07)
Previously, adding new Python packages to our Databricks package cache relied on a convoluted two-part system: a continuously running streaming notebook listening to Event Hub messages, and a client-side Python wrapper that both pip installed packages locally and triggered the server-side notebook to install them again and cache the wheel files in ADLS. Both client and server code were complex and hard to follow. I refactored the client–server logic for clarity, replaced the Event Hub–driven streaming notebook with a simpler message-passing mechanism using timestamp-named files, and moved the server-side cache updater into an Azure DevOps pipeline running every six hours. This made the workflow easier to maintain and removed the need for a constantly running notebook.


## Automated metadata sync from Databricks registry to Git, reducing bulky PRs to minimal, targeted changes., (2025-03)
this was a mini task with the aim to synchronize metadata that may have been manually added on the databricks central model registry into our git version control. It was definitely mostly a laborious task that had to be done, but I ended up scripting out the pull requests at least since there were so many updates to be made. I had a script that compared data from the cmr side with data on our json git side, and I created pull requests on the git side. At first, the pull requests were very verbose because they altered the full settings.json we use for our model metadata so instead I found a way to only edit a small subset of the json metadata so that the pull requests were not so unwieldly.


## Future-proofed a production ML pipeline by replacing CVE-flagged legacy scikit-learn with ONNX, modularizing shared inference logic, and validating output scores to high precision., (2025-07-18)
I had a usecase where i had a multi notebook databricks ADF pipeline, where the scikitlearn used was an older version which was flagged by our pypi proxy with a medium CVE  but using a newer version 1.5.0 broke the model because of non backwards compatibility, so instead I used skl2onnx to convert the pipeline to onnx a object designed with backwards compatibility in mind , and then I updated the inference notebooks, also modularizing the parts loading the model and using it for scoring since it is used by both the scoring and top driver databricks notebooks, and I compared the spark dataframe score and top driver  results to previous  reference stable runs and got the same results proving my updates are non destructive. I also made updates to the feature engineering for reprodicibility, adding a new output copy because the previous scoring notebook logic  unfortunately over writes the feature engineering with additional data. So now i made the scoring notebook to read the new feature engineering separate output copy so that it can be rerun reproducibly and deterministically. 
And in order to test run the full pipeline, i adopted the new run databricks multi task job connecting my new notebooks, executing from git source directly, showing it is possible to step away from data factory orchestration where code is possible to be tampered with and into  run from source where tampering is not possible.


## Refactored a legacy ML platform package deployment into a single, simplified Azure DevOps pipeline, reducing tech debt and preventing staging environment conflicts., (2025-09-05)
Our ML platform team inherited an internal Python package that predated me, written by authors no longer on the team. Although much of its functionality had since been migrated into a newer package, several critical systems—including our feature store—still depended on it. Supporting this legacy code had become a long-avoided but necessary task.

When making a routine maintenance change to its deployment pipeline, I used the opportunity to tackle the accumulated sprawl. The repo contained five or six separate Azure DevOps pipelines, each handling deployments of not just the package but also various Databricks notebooks. The logic was complex, poorly documented, and still powering production systems. I carefully documented the sprawl, reverse-engineered its behavior, and consolidated everything into a single, smaller, easier-to-read pipeline.

As part of this refactor, I fixed a long-standing issue in CI testing: notebooks used absolute %run calls that forced CI to overwrite staging paths, potentially breaking others’ workflows. By switching to relative paths, I was able to redirect tests into a safe, isolated test location. To avoid interfering with production or staging, I settled on using a fixed test path that was cleared at the start of each run—a simpler, more reliable choice than the dynamic timestamped paths I had originally considered.

This work reduced duplication, eliminated fragile dependencies, and simplified ongoing maintenance for a package we still needed to support. Just as importantly, it was a learning experience for me: I practiced scoping my refactor carefully, resisting the temptation to add clever complexity, and shipping a smaller, safer change instead.
