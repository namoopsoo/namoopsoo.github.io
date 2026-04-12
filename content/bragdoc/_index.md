---
title: Careerlog
robots: noindex, nofollow
--- 

## Extended internal Databricks wrapper to generate Git-based workflow DAGs with validation, cluster inheritance, and docs., (2026-02-10)
Within our ML platform, we maintain a lightweight internal package that simplifies common Databricks workflows for data science users. As an incremental enhancement to our existing quickstart tooling, I added support for creating Git-based Databricks Workflow DAGs, complementing the earlier notebook-only approach that relied on workspace notebooks.

The update allows users to easily include notebooks stored in Git repositories when defining new workflow DAG YAML files. I extended the tooling to validate that referenced notebooks exist, automatically attach the cluster used by the control notebook, and generate clearer dependency documentation between workflow steps. The implementation integrates with the Databricks SDK to create, update, and run jobs directly from YAML definitions.

I presented the change at a community meeting and documented the workflow so that data scientists could adopt Git-backed pipelines more easily. The broader goal was to make native Databricks workflow capabilities more accessible while reducing setup friction for platform users.


## Migrated my personal Hugo site to vector-based semantic search in two weekends using Cloudflare AI., (2026-01-31, [link](https://michal.piekarczyk.xyz/note/2026-01-25-hook-up-cloudflare-rag-search/))
As a side project, I upgraded the default search on my personal Hugo-based static site, which previously relied on local edit-distance matching, to a vector-based semantic search. Wanting to move quickly and minimize infrastructure overhead, I chose to experiment with Cloudflare’s managed AI search offering.

Over the course of two Saturdays, I migrated my site’s DNS to Cloudflare, indexed my content using their out-of-the-box embedding model, and set up vector search using their documented workflow. I then updated the site’s JavaScript to query the new Cloudflare endpoint, integrating it cleanly into Hugo’s existing frontend.

The result was a working semantic search experience with minimal custom infrastructure, and a satisfying example of how managed vector search can be added incrementally to a static site. I documented the setup and tradeoffs in a short write-up for future reference.


## Formalized and documented our ML pipeline data-sensitivity policy, clarifying rules for handling predictive outputs and establishing default “sensitive-by-inheritance” guidance for mixed-source pipelines., (2025-12-09)
Our ML platform had long operated under an implicit understanding of how to handle sensitive data — but not a clearly written rule. The ambiguity showed up when discussing predictive pipeline outputs: if a model read from sensitive sources but wrote only pseudonymized results, should those outputs still be stored in a sensitive location?

Opinions varied across team members. Some argued that pseudonymization was sufficient to allow writing to a non-sensitive zone. Others felt that provenance mattered more — that any pipeline touching sensitive inputs should default to writing sensitive outputs, regardless of transformations.

To resolve this, I gathered the various viewpoints, and drafted explicit guidance in our internal wiki. With input from several colleagues, we agreed on a conservative principle:

"If any input to a predictive pipeline is sensitive, the output should also be treated as sensitive."

This decision recognized the reality that model code evolves, and it would be risky to depend on future reviews always catching subtle data-leak vectors. The new written policy gave everyone a clear rule of thumb, reducing confusion and ensuring a stronger default stance on data protection.


## Corrected a non-reproducible reference model by introducing workflow-based training and a DVC-style proposal for data and notebook lineage., (2025-11-17)
As part of an ongoing effort, I revisited a predictive pipeline on our ML platform that was being used as a canonical example repository. While attempting to retrain it, I discovered that its training code was no longer runnable end-to-end. The root cause turned out to be subtle but important: the code used to generate the model artifacts in MLflow no longer matched the code in the repository. Different algorithms and paths had been used for testing, hyperparameter tuning, and final model fitting, meaning the checked-in code could not faithfully reproduce the registered model.

I documented these gaps and traced how the repository had drifted into this state, clarifying where code had likely been modified after the original training runs. From there, I established a cleaner retraining precedent using Databricks Workflows. Although workflows have existed for some time, they are not yet widely adopted on our platform. Using them here allowed us to explicitly freeze and version the entire training process as a single unit — including feature construction, feature selection, train/test splits, hyperparameter tuning, and model fitting — rather than only capturing the final model artifact.

In parallel, I proposed a DVC-inspired approach to data and notebook lineage, extending beyond simple notebook sequencing to explicitly define what datasets each notebook consumes and produces. This would make training runs auditable, reproducible, and easier to reason about over time.

This effort establishes an important direction: moving our example repositories from “illustrative but fragile” toward fully reproducible, end-to-end training pipelines that better reflect best practices for production ML.


## Refreshed ML platform documentation on using Hugging Face pretrained models, replacing outdated examples with a safe, proxy-compatible workflow that loads models from local paths., (2025-11-06)
While reviewing a recent user question about integrating a Hugging Face pretrained model on our internal ML platform, I realized our documentation had grown outdated and confusing. Lack of clarity led to one of the issues the user was running into. Also the examples were not runnable.

To address this, I took the opportunity to revise the platform documentation. I removed legacy snippets, clarified the point of confusion and added a modern, runnable end-to-end example showing how to:

Download models once through the approved proxy,

Store them locally in a workspace or artifact path, and

Load them using Hugging Face APIs from a local directory rather than a remote URL.

This example made it much clearer how to safely and reproducibly use pretrained models within our company’s environment. It also will hopefully reduce future support questions.


## Fixed a Python package cache bug that left empty artifacts after failed copies, restoring reliable propagation of large dependencies like PyTorch., (2025-10-27)
I investigated intermittent failures in our Python package cache where large dependencies, such as PyTorch, were not reliably copied or propagated. After a failed copy, the system would still create an empty file, causing subsequent runs to incorrectly assume the package was present and skip future copy attempts.

Rather than adding complex retry logic, I fixed the issue by removing empty artifacts after failures, ensuring that subsequent scheduled runs would retry the copy correctly. This simplified the system and restored reliable package propagation for large dependencies.


## Refactored row-wise ML scoring UDFs into a reusable, closure-based utility, eliminating global state and improving correctness and reuse across the ML platform., (2025-10-07)
Across the ML platform, we had standardized on a Pandas UDF pattern for row-wise scoring with MLflow models, but the implementation was duplicated inline across repositories and relied on global state for the loaded model and feature names. This made the code less modular, harder to reason about, and easy to misuse.

While implementing a more complex scoring function for an ONNX model that required additional preprocessing steps, I introduced a closure-based approach that cleanly encapsulated the model, features, and scoring logic without relying on globals. Because this pattern needed to be reused in multiple places, I generalized it into a reusable utility.

I added this closure-based scoring function to the shared Python utilities package and updated example repository code to demonstrate the new approach. This reduced boilerplate, improved correctness, and provided a clearer, more Pythonic pattern for row-wise model scoring on the platform.


## Collaborated on diagnosing and fixing a subtle permissions issue that unblocked batched Python package installs on Databricks., (2025-10-02)
While revisiting an earlier refactor of our Databricks Python package installation workflow, I noticed a confusing permissions issue: users could successfully install packages, but the follow-on step that wrote a small “signal” file — used to notify a downstream batching system to populate our shared package cache — was failing with a permissions error.

As an interim measure, I first suppressed the noisy failure since it did not block the user-facing install path. However, the underlying issue still prevented the background batching mechanism from working as intended.

In collaboration with a colleague, we revisited the permissions model. I had originally configured write permissions assuming they would apply recursively, but my colleague suggested explicitly granting permissions on a lower-level directory as well. Once we made that change, the 403 errors disappeared and the end-to-end flow began working correctly.

This small but important fix completed the last missing piece of the earlier project: enabling a scheduled background job to reliably batch user package installation requests and populate our package cache. The result was a quieter, more robust system and a workflow that finally behaved as it had been designed to from the start.


## Resolved a flagged dependency vulnerability by removing an unused TensorFlow/Keras dependency and safely updating Transformers., (2025-09-24)
I investigated a reported vulnerability in a predictive model repository related to TensorFlow, Keras, and Transformers dependencies. Although the issue initially appeared complex, I determined that TensorFlow was not actually used by the model and that Keras was being pulled in unnecessarily as a transitive dependency.

By removing the unused TensorFlow/Keras dependency and updating Transformers, I resolved the vulnerability with minimal code changes and no functional impact to the model.


## Introduced a shared always-on Databricks dev cluster to eliminate startup delays for quick Python experiments and smoke tests., (2025-09-24)
Our team frequently needs to run quick, Databricks-specific Python experiments that cannot be easily replicated on a local laptop due to Databricks’ proprietary runtime and integrations. However, waiting several minutes for a cluster to start made this kind of lightweight iteration unnecessarily slow.

 I proposed and set up a shared, always-on single-node Databricks development cluster for the team. This provided a fast, low-friction environment for smoke tests and small experiments without the overhead of spinning up a dedicated cluster.

 The cluster saw regular adoption and was well received by the team, noticeably improving iteration speed for day-to-day development work.


## Prototyped a Databricks SDK–based export of job runs to improve SRE visibility and mitigate retention limitations., (2025-09-17)
I learned about an ongoing investigation into an issue where our SRE team could not access Databricks job runs, that Databricks permissions around run visibility are complex and not easily adjusted.

In parallel, I had previously experimented with the Databricks SDK for an unrelated idea: backing up production Databricks runs. Revisiting that work, I realized it could serve a second purpose. Using the SDK, I built a proof of concept that downloads and exports Databricks runs as notebooks (IPYNB), making execution context accessible outside the Databricks UI.

This approach addresses two problems at once: it provides a workaround for limited SRE access to run details, and it mitigates the fact that Databricks job run retention is fixed and not configurable. While the current implementation is intentionally scoped as a proof of concept, it demonstrates a feasible path toward regularly exporting runs via automation.

I shared the idea with a small group of colleagues, including SRE-adjacent teammates, and the feedback so far has been positive. The next step, if prioritized, would be productionizing and scheduling the export process to make run history consistently available for debugging and auditing.


## Simplified Python module imports on Databricks by replacing a custom sys.path workaround with native Repo-based imports, improving deploy reliability and developer ergonomics., (2025-09-16)
Previously, I introduced custom ML platform support to encourage users to move away from %run-based notebook imports toward modular, lintable Python files using Databricks’ native import capabilities. While the approach worked, it relied on helper code that modified sys.path, which added complexity and hidden coupling.

More recently, I discovered that this approach was incompatible with a multithreaded execution pattern used in parts of our platform, where dynamically modifying sys.path was not reliable within a Databricks session. This created an opportunity to simplify the design rather than further patch it.

I refactored the platform’s local module mechanism to align with how users already interact with Databricks through Repo folders, eliminating the need for sys.path manipulation entirely. This change improved robustness, made local experimentation easier for users, and better matched Databricks’ supported workflows. Implementing the update required coordinated changes across multiple YAML-based deployment pipelines, but ultimately resulted in a cleaner and more maintainable solution.


## Refactored a legacy ML platform package deployment into a single, simplified Azure DevOps pipeline, reducing tech debt and preventing staging environment conflicts., (2025-09-05)
Our ML platform team inherited an internal Python package that predated me, written by authors no longer on the team. Although much of its functionality had since been migrated into a newer package, several critical systems—including our feature store—still depended on it. Supporting this legacy code had become a long-avoided but necessary task.

When making a routine maintenance change to its deployment pipeline, I used the opportunity to tackle the accumulated sprawl. The repo contained five or six separate Azure DevOps pipelines, each handling deployments of not just the package but also various Databricks notebooks. The logic was complex, poorly documented, and still powering production systems. I carefully documented the sprawl, reverse-engineered its behavior, and consolidated everything into a single, smaller, easier-to-read pipeline.

As part of this refactor, I fixed a long-standing issue in CI testing: notebooks used absolute %run calls that forced CI to overwrite staging paths, potentially breaking others’ workflows. By switching to relative paths, I was able to redirect tests into a safe, isolated test location. To avoid interfering with production or staging, I settled on using a fixed test path that was cleared at the start of each run—a simpler, more reliable choice than the dynamic timestamped paths I had originally considered.

This work reduced duplication, eliminated fragile dependencies, and simplified ongoing maintenance for a package we still needed to support. Just as importantly, it was a learning experience for me: I practiced scoping my refactor carefully, resisting the temptation to add clever complexity, and shipping a smaller, safer change instead.


## Future-proofed a production ML pipeline by replacing CVE-flagged legacy scikit-learn with ONNX, modularizing shared inference logic, and validating output scores to high precision., (2025-08-20)
I had a usecase where i had a multi notebook databricks ADF pipeline, where the scikitlearn used was an older version which was flagged by our pypi proxy with a medium CVE  but using a newer version 1.5.0 broke the model because of non backwards compatibility, so instead I used skl2onnx to convert the pipeline to onnx a object designed with backwards compatibility in mind , and then I updated the inference notebooks, also modularizing the parts loading the model and using it for scoring since it is used by both the scoring and top driver databricks notebooks, and I compared the spark dataframe score and top driver  results to previous  reference stable runs and got the same results proving my updates are non destructive. I also made updates to the feature engineering for reprodicibility, adding a new output copy because the previous scoring notebook logic  unfortunately over writes the feature engineering with additional data. So now i made the scoring notebook to read the new feature engineering separate output copy so that it can be rerun reproducibly and deterministically. 
And in order to test run the full pipeline, i adopted the new run databricks multi task job connecting my new notebooks, executing from git source directly, showing it is possible to step away from data factory orchestration where code is possible to be tampered with and into  run from source where tampering is not possible.


## Added a lightweight helper to automatically detect the active Databricks workspace (staging vs. production) via hostname, enabling safer environment-specific behavior without parameter drift., (2025-08-14)
Our Databricks platform runs separate staging and production workspaces, which historically had nearly identical configurations for consistency. The problem was that certain features—extra logging, experimental capabilities, or in-progress integrations—needed to run only in staging, but our previous way of managing that distinction was clumsy: passing special notebook parameters at runtime. That created subtle inconsistencies between environments and was easy to forget during deployment.

To simplify this, I added a small but powerful helper that inspects the Databricks workspace hostname to determine the current environment. This provided a consistent, self-contained way to conditionally enable or disable functionality without modifying runtime arguments.

Initially, I used it to suppress time-consuming staging-only logging. Shortly after, a teammate used it to gate their experimental feature, preventing it from accidentally going live in production. The function quickly became one of those quietly indispensable utilities—simple, reliable, and broadly useful.


## Automated ML platform repo search setup with a Bash script and screencast for the wiki, eliminating manual credential updates and data fetch steps., (2025-06-01)
In our Git-based ML platform, new repositories are frequently added and removed, making it valuable to search them directly via the file system. Previously, setting up for such searches required a manual series of steps: updating temporary Git and Databricks credentials, and fetching the latest intake CSV containing new business data. I created a Bash script to automate these steps, guiding the user through the setup without needing to remember specific commands, thereby reducing cognitive load and startup time. The script syncs all relevant repositories for immediate use, and I recorded a video screencast to walk through the setup process for easier onboarding.


## Simplified Databricks package cache updates by replacing a convoluted streaming/event-hub setup with a clear client–server design and a scheduled Azure DevOps pipeline., (2025-05-29)
Previously, adding new Python packages to our Databricks package cache relied on a convoluted two-part system: a continuously running streaming notebook listening to Event Hub messages, and a client-side Python wrapper that both pip installed packages locally and triggered the server-side notebook to install them again and cache the wheel files in ADLS. Both client and server code were complex and hard to follow. I refactored the client–server logic for clarity, replaced the Event Hub–driven streaming notebook with a simpler message-passing mechanism using timestamp-named files, and moved the server-side cache updater into an Azure DevOps pipeline running every six hours. This made the workflow easier to maintain and made the constantly running notebook redundant. And there is opportunity to stop it in the future.


## Helped shift the team toward smaller, reviewable pull requests by introducing and socializing Google’s PR best practices., (2025-05-14)
Our team had been struggling with slow and inconsistent pull request reviews. Drawing on practices from a prior team, I introduced Google’s engineering guidance on code reviews, with a particular emphasis on smaller, more focused pull requests.

Adoption was gradual, but through repeated discussion and example-setting, the team began to converge on this approach. Over time, this improved reviewability and reduced friction in the code review process, helping unblock development work more quickly.


## Improved model repo integration tests by introducing top-driver recall as a clearer metric and fixing a join bug that masked missing feature drivers., (2025-05-13)
When we update model repository code, we run integration tests that compare new scores and their top feature drivers against reference outputs. Previously, we measured differences in top drivers by looking at absolute changes in unitless “impact” quantities. In practice, this was unintuitive and didn’t make it easy to understand whether the same drivers were being preserved across versions.

I introduced a clearer approach by calculating the recall of top driver features. For example, if a scored row has five top drivers but only four of those are still present in a new run, the recall is 0.80. Averaging this across rows provides a more interpretable measure of driver consistency between branches.

While implementing this, I also discovered and fixed a bug: our tests used an inner join on features, which meant that missing drivers were silently dropped rather than penalized. By switching to a left join, we could correctly capture cases where recall fell below 1.0, ensuring that shifts in top drivers are properly surfaced.

These changes made our integration tests both more intuitive and more accurate, reducing the risk of overlooking significant differences in model behavior.


## Added histogram overlays by cohort to model integration tests, providing clearer visual evidence for troubleshooting score deviations., (2025-04-16)
To improve our model integration tests, I added histogram overlays that show output score distributions separately for each cohort. Previously, we only inspected delta difference distributions, which sometimes made it difficult to judge the scale or significance of deviations. In one case, I found that differences within a narrow score band were not obvious in the existing view, but overlaying the distributions made the impact clear. By incorporating this visualization into our standard tests, I created a more effective way for the team to diagnose whether observed differences were meaningful, improving confidence in code changes.


## Made a critical infra package versioned, dependency-safe, and documented, reducing risk around breaking changes in production pipelines., (2025-04-09)
I addressed long-standing technical debt in an internal infrastructure package that had no versioning and no declared dependencies. As a result, any production process using it had to manually install dependencies and could not pin a specific version, making deployments fragile and increasing the risk of unintended breaking changes.

I updated the package so that consumers can pin versions and rely on declared dependencies, simplifying usage and making production deployments safer and more reproducible.

In addition, the repository defined multiple production pipelines that were undocumented. The original authors had left the team years earlier, and the lack of documentation had made the code effectively “hands-off.” Through reverse engineering, I documented how these pipelines function and how they are used in production, making the system understandable and maintainable again.


## .., (2025-04-08)
..

## Established a repeatable path for reviving defunct ML models by retraining a legacy heart failure model with 99.9% fidelity and shipping it back to production., (2025-04-01)
A legacy production model predicting heart failure progression was at risk of becoming defunct due to outdated package dependencies. Although such cases are typically handed back to the original author, I took ownership of restoring the model on the ML platform.

I located the original training data and code, refactored the workflow to remove exploratory logic, and rewrote it as a clean, reproducible training pipeline using modern dependencies. I validated the new model by comparing inference outputs against the original production model, demonstrating 99.9% equivalence. After reviewing the results with the original model author and receiving their endorsement, I deployed the retrained model to production without overwriting existing assets.

Along the way, I explored upgrading the original scikit-learn ensemble using LightGBM, CatBoost, and XGBoost in place, but determined this path was not viable with current dependencies. Instead, retraining proved to be the most reliable approach given the available artifacts.

This work provided the first concrete example on the platform that legacy models can be safely retrained and validated rather than retired, creating a precedent and reference for future model recovery efforts.


## .., (2025-03-25)
..

## Improved ML metadata correctness by allowing missing validation paths to be explicit null, preventing misleading configuration and surfacing unknown training data., (2025-03-18)
On the ML platform, we maintain metadata for predictive models that includes paths used for validation. I identified several cases where these paths were technically required but did not actually exist, resulting in misleading configuration that implied validation data was present when it was not.

I updated the metadata validation logic to allow these paths to be explicitly null when they do not exist. This change encourages accurate signaling of missing or unknown validation data rather than forcing users to provide non-existent placeholder paths.

By preferring explicit absence over incorrect data, this improvement surfaced cases where training or validation data was undefined and reduced the risk of silent misrepresentation in model metadata.


## One-line fix, six-month mystery: restored Git commit tagging in our ML deployment flow with a tiny tweak to the pipeline., (2025-03-07)
Our ML platform uses a shared deployment pipeline that injects the current Git commit hash into Databricks notebooks during deployment, enabling version traceability for production ML pipelines. This mechanism had been broken for over six months due to an incorrect Azure DevOps pipeline replacement function, but the failure went largely unnoticed because deployments continued to succeed without the metadata.

I investigated the issue and identified that a deprecated or incompatible replacement function was being used in the YAML pipeline. I fixed the problem with a single-line change to the correct Azure DevOps replacement function, immediately restoring commit hash propagation across deployments.

This resolved a long-standing reliability gap in the platform’s observability and ensured that deployed notebooks could once again be accurately traced back to their source code.


## Automated metadata sync from Databricks registry to Git, reducing bulky PRs to minimal, targeted changes., (2025-03-01)
This was a small but necessary task: synchronizing metadata from our Databricks Central Model Registry (CMR) into Git version control. Over time, some metadata updates had been made directly in CMR without being reflected in Git, leaving us with drift between the two.

Rather than manually reconciling dozens of differences, I wrote a script to compare CMR metadata with our Git-based JSON settings and automatically generate pull requests. At first, the pull requests were unwieldy because they rewrote the full settings.json files, making it difficult to review changes. To improve this, I refined the script to edit only the specific fields that had changed, producing cleaner, more focused pull requests.

The outcome was a faster, less error-prone way to keep CMR and Git in sync, saving time on a tedious maintenance task while making version control history more meaningful.


## Kicked off Databricks 14.3 upgrades on our ML platform, establishing a minimal upgrade pattern and unblocking dozens of future model runs., (2025-02-17)
During an end-of-support Databricks upgrade cycle, our ML platform needed to migrate multiple production model repositories to Databricks 14.3. I proactively spiked the upgrade on one of the most comprehensive repositories to establish a minimal, repeatable migration approach.

I produced a small, focused pull request that set the pattern for future upgrades, reducing unnecessary changes and making subsequent migrations significantly smoother across dozens of scheduled model runs on the platform.

While upgrading, I investigated and resolved a subtle Spark behavior change: StringType began stringifying as StringType() instead of StringType, causing string columns to be misidentified and preprocessing to silently fail. Identifying and fixing this issue prevented downstream data corruption and helped ensure the reliability of future upgrades.


## Introduced reusable methods for row- and column-level comparison of large DataFrames to debug integration test failures., (2025-02-06)
While investigating a puzzling top-driver integration test mismatch, I went deep into comparing very large DataFrames produced before and after a Databricks upgrade. 

I had written similar utilities in the past, here I had ended up with a few more granular ones.

As part of this exploration, I developed and documented several practical techniques that made large-scale DataFrame comparison more tractable:

1. Interleaving “before” and “after” columns after joining two DataFrames, making it easy to visually spot-check specific columns side by side.

2. Row-wise diff summaries, showing exactly which columns differ for a given row, rather than just flagging that a row mismatched.

These methods made it much easier to pinpoint the root cause of a subtle top-driver discrepancy and turned an otherwise opaque comparison problem into a debuggable one. I shared the techniques with a colleague, who later reused them while validating a feature store update during a Databricks migration.


## Enhanced semantic search validation by doubling dataset size and adding Precision@10, confirming the hosted model’s slight edge over baseline., (2025-02-01, [link](https://michal.piekarczyk.xyz/post/2025-02-01--model-metric-updates/))
Continuing the effort to help validate typesense embedding models as an alternative, I roughly doubled my golden evaluation dataset and introduced another strong evaluation metric, Precision@K=10 , into my existing suite of MAP and MRR. And good news is that now with more a larger evaluation dataset I could see that the new candidate embedding model was actually slightly outperforming the previous one. I am aware however that although these are strong industry standard information retrieval metrics, they are still proxies to business metrics which I do not have and would only be available through true customer facing a/b testing which I do not have yet but I felt the need to at least an initial method of evaluation before we can start testing with actual customers.

## Fixed a silent %run early-exit bug so both internal models correctly publish top-driver explanations for audits., (2025-01-28)
During a routine model update, I discovered a silent bug in a predictive pipeline that caused it to exit early before publishing the second half of its top-driver explanations. The pipeline contained two internal models, but due to this early exit, only one model’s row-level explanatory outputs were being produced.

The issue stemmed from a %run-style script that terminated without raising an error, which is why the problem had gone unnoticed. I corrected the control flow so both internal models now publish their full top-driver information as intended.

Fixing this ensured that downstream consumers and audit processes have access to a complete and accurate explanation of model behavior. As part of the investigation, I also documented runtime characteristics, including a ~4.5-hour execution profile, and shared these findings in a short internal write-up to make the failure mode more visible going forward.


## Fixed a long-standing integration test flaw that allowed stale outputs to mask production-breaking bugs, sparking a shift toward non-colliding run IDs., (2025-01-28)
I introduced a “clean slate” integration test update that deletes all previous staging outputs before running the model pipeline under test. This addressed a long-standing flaw where integration tests reused the same ADLS output directories across runs, allowing stale artifacts from prior executions to pollute new results.

The issue became clear after a production incident: a multi-step scoring pipeline failed with a PathNotFound error because an intermediate write path had been changed to a location that the downstream step did not expect. Although the change passed integration tests, it later emerged that those tests were falsely succeeding because data from earlier runs still existed at the expected paths. In effect, our tests had been providing false confidence.

The clean-slate approach removed this failure mode by ensuring each integration test starts from an empty output state, making path mismatches and missing artifacts visible immediately. This also surfaced the realization that this flaw had existed for the entire history of our integration testing on the platform.

The change sparked broader discussions about test integrity across the team. As a result, a colleague began developing a more robust long-term solution using unique, timestamp-based run_ids to ensure non-colliding outputs for every execution. While this approach is incrementally being rolled out and ultimately supersedes the clean-slate deletion strategy, I’m glad my fix helped expose the problem and catalyze a stronger testing model overall.


## Fixed incomplete global code searches by incorporating non-standard repositories from our wiki registry., (2025-01-28)
Our ML platform relies heavily on global code searches across many repositories to support development and troubleshooting. For this to work well, we need a complete and authoritative list of repositories available on engineers’ machines.

I discovered that our existing repository discovery logic was incomplete: it only pulled from sources that did not account for several repositories with non-standard naming conventions. As a result, those repositories were being silently excluded from global searches.

To fix this, I updated the discovery process to also include repositories listed in our internal wiki schedule, which has been much more carefully maintained over time. This brought several previously missing, non-standard repositories into scope.

As a result, our local MLP CLI–based code search now covers the full set of platform repositories more reliably, reducing blind spots during debugging and development and making cross-repo investigation more dependable.


## Developed a golden dataset and search evaluation suite to validate embedding models for semantic dish search, enabling a cost-saving model switch., (2025-01-11, [link](https://michal.piekarczyk.xyz/post/2025-01-11-comparing-embedding-models/))
During the process of delivering a semantic search capability around a restaurant dish corpus, I took a detour to evaluate a 3rd party hosted solution, typesense, and I took this opportunity to develop a golden dataset for the search problem because my particular open source embedding model was not available on typesense, and I needed a good way of objectively comparing models. I ended up writing helper code to make it easier to build such a dataset and I built out evaluation code using the two tried and true algorithms, Mean Average Precision (MAP) and Mean Reciprocal Rank (MRR). Ultimately I was able to show that the embedding model available on typesense that I was targeting was at least as good as the other one I was using and this was really important because it was a 768 as opposed to a 384 dimension model meaning I had evidence that half the cost was good enough for at least an equivalent result. And this gave motivation to continue building a larger golden dataset to get even more confidence about the choice.

One of the roadblocks was that in order to formally compare the model I had been using prior with the ones available on typesense, I needed to locally reproduce inference of the hugging face embedding model they were using. This involved downloading the onnx from hugging face and adapting it to match my local testing pattern for the other embedding model.

Also it was important to choose well between the two candidates models in particular, because it turned out that TypeSense at the time at least did not have a pause capability and so choosing a node and its embedding model  was permanent. And as I had learned in an earlier self hosted postgresql part of this challenge, uploading the data to the cloud is very time consuming. And this case was no different, because the simplicity of the typesense offering is that you pay for a cluster that  maintains its own self contained postgresql and switching between models is not really a straightforward operation.

The TypeSense detour was a bit bittersweet however, because one of the reasons for trying it out was that although I got to a point with a decent ~600ms query with a self hosted postgresql pgvector geopoint solution, there was a desire to get it even faster and TypeSense came up as strategy to at least get a benchmark for how fast our queries could be given a hosted solution that is presumably tuned very well out of the box. Though in hindsight of course nothing is really for free and there was also a learning curve to navigate the TypeSense documentation to develop a configuration enabling a hybrid cosine similarity and geopoint distance limited query.


## Advanced our Databricks modularization effort by maturing a shared Python package, adding testing, and pitching adoption as an internal OKR to reduce duplication and troubleshooting overhead., (2024-???)
As our Databricks-based ML platform grew, each model repository bundled not only feature engineering and scoring notebooks but also duplicated support code—installing packages, creating MLflow experiments, authenticating, configuring pipeline parameters, defining ingress data sources, and managing deployment YAML. This copy-paste approach meant every update required manually propagating changes from a template repo into many others, which was unsustainable.

Following a successful mini hackathon where colleagues began packaging common utilities into a shared Python library, I joined the effort to bring it to a higher level of maturity. My contributions included expanding test coverage, transitioning existing tests to pytest, and improving resilience as the shared code evolved. I also wrote a clear, compelling README to document usage and encourage adoption.

To build momentum, I collaborated with a colleague to pitch the initiative as a bottom-up internal OKR. We emphasized how modularizing platform utilities would simplify user-facing code, reduce repeated effort, and lower troubleshooting time. By formalizing the vision and contributing maturity work, I helped establish the foundation for shared abstractions to replace repeated notebook boilerplate.


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


## Introduced workspace file access in Databricks 11.x to unify redundant JSON and notebook configs, reducing duplication and black-box %run dependencies., (2024-?)
On our Databricks-centered ML platform, we version control ML pipeline notebooks and JSON settings in Azure Git. For years, a redundancy existed: each repository included a JSON settings file (with cluster runtime versions, integration test parameters, etc.) and a Databricks configuration notebook (defining blob ADLS storage paths and other setup details). The overlap was awkward, as both JSON and notebooks contained key metadata, forcing duplication and reliance on %run calls to bring in opaque configuration code.

With the release of Databricks 11.x, which added Pythonic access to workspace-resident arbitrary files (not just notebooks), I created our first wrapper to directly load repository JSON into notebooks. This marked the first step toward reconciling the two configuration styles. By doing so, we began reducing both duplication across ML pipeline repos and the dependency on %run-based configuration notebooks, which couldn’t be linted and were difficult to maintain.

Although the full migration required incremental effort across many repositories, this initial wrapper established the conceptual shift: moving from redundant, black-box configs toward a single, maintainable, lintable source of truth for pipeline metadata.


## Embedded Git commit hash into our databricks ML platform Python library (__build__), enabling precise traceability in CI/CD, testing, and production., (2024-12-09)
To improve traceability in our databricks ML platform, I added the Git commit hash as a member variable in our internal Python library. During CI/CD, the build process now automatically retrieves the current commit and stores it as a dunder attribute (e.g. __build__).

This small change has a big impact: it eliminates ambiguity about which code version is being executed. During both testing and production troubleshooting, the team can now reliably confirm the exact commit tied to a given library build. This makes debugging faster, improves confidence in deployments, and reduces the risk of running code that isn’t clearly identified.


## Automated monthly drift monitoring for clinical condition prevalence data, modularizing the code and reducing manual effort previously required., (2024-12-05)
Our ML Platform’s feature store contains a large amount of clinical data, including prevalence of conditions for our member population. To monitor data quality, we track prevalence rates over time and raise alerts when they shift unexpectedly, since such changes may indicate upstream issues. Previously, this drift monitoring was performed manually on a laptop using a CLI utility I had written.

To improve reliability and reduce manual work, I restructured the code into a clearer, modular design and automated it as a scheduled monthly job. The job samples condition prevalences over recent time series and produces drift information automatically, shortening the turnaround time for spotting and reacting to issues.

While some manual steps remain—such as opening a pull request when drift is detected—the automation has already reduced overhead and made the process more consistent. Longer term, the next step will be to fully automate those remaining tasks, but this milestone established an important foundation by moving from ad-hoc laptop runs to a reliable production job.


## Explored adjacent ML platform technologies (Kubernetes, Dask, Polars, distributed vs. GPU learning) to broaden perspective beyond Databricks, and shared findings in an internal tech talk and blog post., (2024-09-05)
Since much of my work centers on Databricks, I set out to broaden my perspective by surveying adjacent ML platform technologies. My goal was to identify blind spots and better understand tradeoffs between distributed data processing and GPU-based training. I reviewed available solutions including Kubernetes, Dask, and Polars, and considered their scalability, strengths, and limitations.

I learned that hybrid approaches combining GPUs with multi-node training exist, and that strategies like parameter servers are used when model weights exceed GPU memory. I also confirmed that Databricks has shifted away from supporting distributed training directly, instead emphasizing Spark for data transformations and deferring training workloads to multicore libraries like TensorFlow and PyTorch.

An interesting observation was that both Dask and Polars explicitly caution against use on datasets larger than ~1 TB, recommending Spark in those scenarios. These comparisons highlighted how different tools position themselves along the spectrum of data size and training complexity.

To share what I learned, I participated in an internal knowledge-sharing talk across teams, and published a rough first-draft blog post documenting my findings, here, https://michal.piekarczyk.xyz/post/2024-08-29--architectures/. The exercise not only improved my understanding of alternatives to Databricks, but also sparked useful conversations with colleagues about when and how we might apply these tools in practice.


## Standardized integration test code by introducing our shared internal Python library, replacing scattered custom logic with a uniform platform package., (2024-08-23)
Our ML platform’s integration tests had accumulated scattered custom Python code across different repositories, which made them inconsistent and harder to maintain. After we introduced a centralized internal platform library, I refactored the test code to use this package. This reduced duplication, brought consistency to how tests were written, and ensured they followed shared best practices—making the framework easier to maintain and extend.


## Published a semantic dish search demo combining vector search with BART topic detection and NER, backed by a Postgres vector store and documented via a Streamlit/Hugging Face prototype., (2024-07-20, [link](https://michal.piekarczyk.xyz/post/2024-07-20-streamlit-is-lit/))
I published a blog post describing a semantic search demo for restaurant dishes that I originally prototyped in Streamlit on Hugging Face Spaces. Since keeping the live demo running was relatively expensive, I instead recorded a short video walkthrough and documented the architecture and results in the post.

The system combines several NLP components. First, a BART entailment model (facebook/bart-large-mnli) evaluates whether a query appears to be on-topic before running the search. While this signal is currently displayed as diagnostic information, it was designed with the idea that it could later be used for routing decisions.

If the query is relevant, the system performs vector similarity search over embedded restaurant dish data. The original prototype used the all-MiniLM-L12-v2 sentence transformer model, but in this iteration I experimented with Cohere embeddings via LangChain. I also moved the vector store from an in-memory index to PostgreSQL with vector support, demonstrating how the same concept could scale beyond a small demo dataset.

The interface allows users to type a dish name and retrieve nearby matching dishes, enriched with restaurant location metadata. For additional exploration, I also integrated a named entity recognition model (bert-large-cased-conll03) to highlight location entities in the query text.

The project itself originated as a small prototype inspired by a friend’s interest in restaurant discovery. Early versions used the historical NYPL menu dataset, but I later switched to a much larger Uber Eats Kaggle dataset to make the search results more realistic. The blog post captures the architecture, experiments, and lessons learned from iterating on the demo.


## Introduced modular Python coding in Databricks 11.3 by enabling multi-file module imports and updating deployment pipelines to support plain files, moving beyond %run globals., (2024-01-23)
With the release of Databricks 11.3, our ML Platform gained a new capability: workspaces could now host not just notebooks, but also plain Python files. This opened the door to more modular, Pythonic development practices. Previously, our notebook code often relied on %run statements to pull in helper functions, which polluted the global namespace and discouraged clean module design.

I took the initiative to explore how far the new functionality could go. While Databricks’ documentation only described the simplest case—a single .py file—I tested whether it would support more complex structures. I confirmed that nested directories of Python files with __init__.py could indeed be imported as full Python modules, enabling us to organize code more professionally.

To prove the approach, I introduced this modular style into one of our model repositories, replacing %run calls in a feature engineering notebook with imports from a local module. To make the pattern sustainable, I extended our Azure DevOps deployment pipeline to automatically detect such modules in Git repositories and recursively push them into Databricks workspaces using the newly available Databricks SDK. This was a significant improvement over the old Databricks CLI, which had no support for plain files.

After successfully applying this pattern to a few additional repositories, I shared the results with colleagues. Interest grew quickly, and others began to adopt the approach. The impact was a meaningful cultural and technical shift: our team could now move away from hidden global-variable hacks and toward cleaner, modular, and maintainable code.


## Designed and deployed a pgvector + PostGIS–based semantic search for restaurant dishes with geospatial filtering and optimized embedding storage, achieving 10-20x storage savings through selective embedding strategies., (2024)
I had the task of  building out semantic search on top of a restaurant dish corpus so that a user at a given location can free form type some kind of food and they can see the restaurants that match nearby, based on the specific dishes that matched the query at those restaurants. The first iteration of this task, was a pgvector implementation, with embeddings at the level of menu-subsets of dishes that each restaurant has, meaning that each restaurant has several menu-subsets where each subset can have 10 to 20 dishes, say, and these dishes were concatenated into blobs and those were embedded.  The end user accessible API took a latitude, longitude as well as a free form query. And the result was a ranked list of dishes and the restaurants they are available at, constrained by the location identified by the location given.

This project had many components, but began with taking an off the shelf embedding model, embedding a corpus of menu data into postgresql pgvector, along with a table of locations of restaurants and their postgis locations. A postgresql query was constructed, first with the relevant postgis subset as a CTE, since that was faster and then calculating the cosine similarity of the menu blobs with the target query and ranking that.

Then on the fly, embedding for individual menu items were calculated for the subset, in software. The reason here was that the pgvector data was actually really huge and by only storing the menu sections embedded, there was a 10-20x savings and the runtime embedding of the small under 100 typically subset was still reasonably fast and can be done as a second API call after a initial list of restaurants is populated for the user first.

In hindsight, the on-the-fly approach is obvious, but at the time this was a kind of eureka moment and much needed, because going by the numbers, embedding each of the ~6 million menu section blobs with a `768` dimension embedding was already intense, since that is already 6million*768*32 bytes plus additional storage for its index, but then there were  ~50 million menu items to consider with the same kind of storage requirements.

There were many crazy micro challenges along the way, but one memorable epithany on 2024-11-10 was that I had a very slow query which was performing a scan on longitude,latitude in my table of restaurants when looking for restaurants within a particular distance of the user's location. This was mind boggling because I had a postgis index which was not getting used. But I realized the reason was that in my WHERE I was constructing and casting to geopoint on the fly , `WHERE ST_DWithin(ST_MakePoint(longitude, latitude)::geography, myblah.my_location, 1609.34)`, and simply changing to `WHERE ST_DWithin(geopoint, myblah.my_location, 16093.4)` to use the actual geopoint column I already had but forgot to use finally got the query to do an index scan, cutting from seconds to under a second!


## Productionized feature drift monitoring across ~18k features with scheduled Databricks/ADF jobs, CI smoke tests, and multiple drift algorithms, providing monthly situational awareness of drifting features., (2023?)
Building on a colleague’s earlier proof-of-concept with the Deepchecks library, I implemented a production-ready feature drift monitoring system for our ML platform. The goal was to provide recurring visibility into how clinical and other features in our feature store change over time, since drift can indicate data quality issues or modeling risks.

I formalized the code to run in Databricks and scheduled it with Azure Data Factory as a monthly job. The job can process multiple lines of business in parallel, parameterized by feature groups and historical comparison windows. To make testing practical, I added options to run on only a subset of features, which enabled a fast smoke test used in CI. I also added frozen drift data for CI validation, which helped me catch and fix a production bug early in the rollout.

The system supports configurable sample sizes (e.g. 10k vs. 100k rows) to compare sensitivity, and it parameterizes the drift algorithms used. For numerical features, we run PSI and the Kolmogorov–Smirnov test; for categorical features, we use Cramer’s V and Earth Mover’s Distance. Across ~18k features, the output is a ranked list of those most likely to be drifting.

While the internal marketing needed to promote user adoption has not yet happened, the job has been running in production for about a year, generating monthly drift reports. So at least the first step has been achieved: creating a systematic, repeatable way to detect and rank feature drift, giving us better situational awareness of the stability of our feature store.


## Used ChatGPT to kickstart a local Flask image-labeling app, iterated on API/CORS issues, and built a client that runs on laptop and iPad., (2023-05-04, [link](https://michal.piekarczyk.xyz/post/2023-05-14-chat-gpt-flask-kickstart/))
As a side exploration, I used ChatGPT to kickstart a simple Flask web app that serves a REST API for image labeling. My goal was to get a minimal Python app.py that could return image filenames from a folder via GET and accept user-submitted choices via POST, paired with a single-page HTML front end that interacts with the API.

ChatGPT generated a functional skeleton for the server and client, but when I started testing it locally, I ran into practical issues. For example, part of the generated HTML was truncated due to response size limits, and my browser blocked requests due to missing CORS headers. This reminded me that even simple client–server work can be thorny without the right middleware — so I appended flask-cors and enabled CORS cleanly rather than hacking around browser errors.

Over a couple of weekends, I got the prototype running on my laptop and accessible from my iPad, which was a fun little milestone. The experience forced me to think through REST endpoint behavior, local CORS configurations, and practical debugging of API–UI integration. I’ve posted the code and screens for future reference, and plan to flesh out the outline into a more complete write-up later.


## Eliminated template sprawl in our ML deployment system by centralizing and parameterizing ADF logic across staging, prod, and feature variants, from 16 templates to 1., (2023-03-20)
within our ML platform, we were supporting the onboarding deployment and running of 100 plus git repo based models and in our deploy design, we had a large amount of duplication. we had the same Azure DataFActory ADF arm template duplicated with respect to the existance or non existance of a databricks notebook used for measuring feature importance , and also w.r.t. a notebook used to save output data in a certain way . And this was bifurcated yet again w.r.t. staging and production, so there were therefore a total of 2x2x2 = 8 copies of essentially the same arm template with small tweaks. And on top of that, I was about to introduce another bifurcation w.r.t. a databricks notebook used to build ground truth data. So instead I took this opportunity, to actually pay down the tech debt and I parameterized all the arm templates so instead of 2x2x2x2 = 16 copies there was now only 1. On top of that, another area of duplication was that the json templates  for the different variations of arm templates parameters existed in all of the 100+ model repositories. And I removed this so the logic was now getting handled in our centralization repository instead. So therefore now both the deployment centralization code and the model repository code was simpler and leaner.

## Contributed preprocessing, prompt engineering, and system integration to a team hackathon project on health plan documents, while also delivering an early fallback RAG-style demo., (2023-02-15)
During a 2.5-day internal hackathon, I joined a small team focused on applying LangChain and GPT to health insurance plan documents. These documents are highly tabular and difficult to parse, so on the first day I experimented with manually restructuring raw PDF text into contextual sentences. While time constraints kept me from automating this fully, it helped hedge against LangChain’s default handling of dense table dumps and may have improved the clarity of responses.

At the same time, I explored prompt engineering around empathy, since health plan Q&A could benefit from a friendlier tone. With minimal changes, I was able to shift answers toward warmer, more approachable responses, even experimenting with light backstories for context.

To ensure we’d have something working by the deadline, I also built a fallback demo loop: directly injecting parsed plan text into LangChain prompts for basic question answering. Meanwhile, teammates created separate Gradio apps—one for Q&A over embeddings stored on Hugging Face, and another for speech-to-speech interaction. I played a key role in integrating these efforts, gluing the two systems together into a unified demo that allowed both chat and audio-based Q&A over plan documents.

Although we didn’t measure accuracy improvements from my early sentence wrangling, from what I saw it was anecdotally clear to me that existing PDF-to-text tools lost the original context with table-heavy documents, so  I am curious to better measure this impact in the future.


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

I began converting our notebooks to use dbutils.notebook.run, which allows explicit parameter passing and provides full contextual input/output when running child notebooks. One major challenge was ensuring that large Spark DataFrames could be safely passed between notebooks. Unlike %run, where globals are directly shared, dbutils.notebook.run requires a different mechanism. I discovered that Spark’s global temp views could be used to pass DataFrame references across caller and callee notebooks within the same JVM. While the documentation only demonstrated this with toy examples of a few rows, I successfully validated the approach at production scale, handling millions of rows across multiple DataFrames with reusable code. Interestingly, when I discussed this method during a Databricks office hour, even the Databricks team admitted they hadn’t seen this “hidden gem” of functionality in practice before. Prior to demonstrating that passing a multi-million row dataset across this interface, my colleague argued that it was likely serializing and the larger test was needed to be convincing. once I showed that spark lazy behavior was consistent even on the larger datasets, my colleague was sold.

To roll out the change safely, I built a standalone Azure Data Factory job that acted as a 3-way QA comparison. For each notebook under test, it would:
1. Run the current master branch with %run (baseline).
2. Run my new branch still using %run (backward compatibility check).
3. Run my new branch with dbutils.notebook.run (new approach).

It then compared all DataFrame outputs across the three runs to confirm that behavior remained consistent. This systematic approach gave the team confidence that the migration was safe.

A bonus outcome of using dbutils.notebook.run was the ability to introduce end-to-end integration tests for our production feature notebooks. Previously, our CI/CD pipeline only tested isolated functions. Now we could validate the entire notebook flow, improving trust and reliability in continuous integration.

In summary, this effort proved that production-grade Databricks notebooks don’t need to rely on hidden globals via %run. By switching to dbutils.notebook.run, we introduced rigorous isolation, parameterized execution, backward-compatible safety checks, and stronger end-to-end test coverage, while retaining the benefits of distributed Databricks workflows.


## Designed a scalable integration test for comparing multi-million-row DataFrames under dbutils.notebook.run, optimizing comparisons with join-based logic and tolerance handling., (2022)
As part of validating our migration from %run to dbutils.notebook.run in Databricks, I needed to prove that very large DataFrames—up to 8M rows × 3,000 columns—could be passed safely between notebooks. To do this, I set up an integration test that compared outputs generated by both methods to confirm they were equivalent.

Initially, I tried the common df1.subtract(df2) approach, but it was far too slow—essentially an O(n²) operation. Instead, I realized we could “cheat” by leveraging known index columns: join the two DataFrames on their indexes first, and then compare values row by row. This dramatically improved performance.

Along the way, I ran into several tricky edge cases:

Floating-point noise: Rounding introduced spurious deltas, so I switched to comparing raw differences with a tolerance (e.g., |Δ| < 0.01). This reduced false positives and improved reliability.

Integers stored as doubles: Columns that were technically double but functionally integer triggered unnecessary mismatches. I detected these by checking column means and coerced them into integer comparisons.

These adjustments turned the test into a practical, reliable way to validate equivalence across huge DataFrames—something critical for building confidence in the new execution model.


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


## Resolved an out-of-memory issue during Databricks runtime upgrade by replacing a costly nested one-hot encoding loop with a streamlined manual transformation., (2022)
As part of upgrading our hosted model repositories to the Databricks 10.4 general release runtime—both to access new optimizations and because earlier runtimes were approaching end-of-support—I encountered an out-of-memory error in the feature engineering step of one repository.

The root cause was a combination of Databricks’ native OneHotEncoder and a custom double-nested for loop that iterated over hundreds of columns and their values to produce additional one-hot encodings. In this model’s case, the final feature set had already been selected, leaving only about 15 relevant columns. I opted to bypass the nested loop entirely and manually code the one-hot transformations for this small set.

While I initially considered switching to Spark’s built-in one-hot encoder, the existing code relied on a custom naming convention for new columns, which made a direct swap impractical. By unrolling the loop and explicitly writing the transformations, I eliminated the driver-side processing bottleneck, removed the memory issue, and enabled the model pipeline to run successfully on the newer Databricks runtime.


## Rebuilt underwriting pipeline with AWS Step Functions + Lambda for disaster recovery, reducing legacy Django dependencies and improving resilience, explainability, and auditability., (2021?)
Following a double hit—a pre-Thanksgiving AWS outage and an information security incident—we prioritized strengthening the resilience of our underwriting infrastructure. At the same time, stricter PCI compliance and lingering reliance on a legacy Python 2 Django monolith pushed us to decouple risk-related flows from the broader customer experience. Cleaner separation meant better explainability, simpler auditing, and reduced operational risk.

To achieve this, I redesigned the pipeline using AWS Step Functions State Machines with Lambda-based microservices. This “football-passing” control flow replaced our prior orchestrated design, lowering inter-Lambda overhead and making the system fully serverless. I also carefully minimized the size of data passed between Lambdas, improving runtime efficiency. To ensure disaster recovery readiness, I built the stack with CloudFormation, giving us infrastructure-as-code repeatability.

We rolled out the new system incrementally in canary style, starting with smaller retailers and later migrating larger partners once stability was proven. A highlight of this architecture was its replay capability: we could feed past payloads through the pipeline to validate new rules or architecture changes. I worked closely with a colleague to test rule modifications, comparing before-and-after outputs meticulously to ensure no unintended changes in business logic.

The result was a serverless underwriting pipeline that improved disaster recovery, reduced reliance on legacy systems, and simplified future development. It provided not only technical resilience but also operational clarity, positioning the platform for safer iteration and long-term maintainability.

However, at the very end of the project, a colleague pointed out that I might hafe gotten used to the json style representation that AWS step functions use, but that others might not understand it so quickly and so we collaborated on a POC to test a variation where the routing was all in python as opposed to using the AWS logic for routing. Although initially I felt the documentation was really mature, I conceded that python would be way simpler to understand and modify quickly as needed in our fast paced environment. 


## Rebooted earlier Citibike destination-prediction project with XGBoost, custom K-area metric, and SageMaker-hosted demo site—combining model experimentation with hands-on MLOps deployment., (2020-10-20, [link](https://michal.piekarczyk.xyz/project/2020-10-20-bike-share-learn-reboot/))
... 
Several years after my first Citibike destination-prediction experiment, I revisited the idea—this time applying everything I’d learned since, both in modeling and deployment. The goal remained the same: given a rider’s start time and location, predict the neighborhood where their trip would end.

This version used XGBoost rather than scikit-learn Random Forest,  along with new temporal and categorical features and a complete hyperparameter-tuning workflow. I explored both the functional API (xgboost.train) and the scikit-learn-style API (XGBClassifier().fit), discovering that the former exploited parallelism much better—4 minutes vs 49 minutes wall time for the same result. I also learned that, at the time, neither API fully supported batch or incremental training, which was something I’d hoped to test for online-learning scenarios.

Feature engineering included weekday flags and time-of-day bucketing (five coarse periods instead of 24 hourly bins). EDA confirmed clear differences between weekday and weekend behavior—two commute-time peaks during the week versus one broader weekend curve—and the new weekday feature turned out to be the model’s most predictive input.

To evaluate performance, I devised a new metric called “K-area”, inspired by top-K accuracy, which I had used in the previous project. Instead of just measuring the proportion of correct top-1 predictions, it averaged cumulative accuracies across ranks, giving a more nuanced sense of how close predictions were to the right neighborhood. Looking back, it was effectively a uniform-weighted version of MRR (Mean Reciprocal Rank).

I ran over a thousand model variations, tracking metrics per epoch and across parameter combinations, and used the results to analyze performance curves. To make the work more tangible, I built a small demo site: a web page with a map plotting predicted destinations, backed by a SageMaker “bring-your-own-Docker” endpoint and a Google Static Maps API overlay.

In the end, this reboot blended machine-learning experimentation and production engineering—a full MLE + MLOps loop in miniature. The project deepened my intuition for feature importance, evaluation metrics, and the practical trade-offs of serving real models online.


## Re-engineered SQL-based logistic regression for returning-customer underwriting, cutting runtime from 6+ hours to <1 hour with batching, normalization, and query optimizations., (2020)
As our customer base grew, we needed better underwriting models for returning customers. Initially, our approach was a slow, SQL-based logistic regression pipeline that took over six hours to run—too long for daily operational use. A colleague developed features that showed promise, but integrating them highlighted multiple challenges: inconsistent use of “days past due” calculations, gaps in scoring customers without active leases, and assumptions about live vs. historical data.

I tackled the problem by re-engineering the pipeline in Python with Docker orchestration, while retaining SQL feature logic. To improve performance, I normalized a key data provider table, converting JSON string fields into JSONB and columnar formats for faster lookups. I also restructured the table by user ID, making it easier to retrieve earliest and latest interactions via window functions.

Several SQL optimizations contributed to major speed gains:

- Switching to indexed snapshot tables instead of live tables.

- Refactoring queries with >7 joins to force PostgreSQL to optimize join ordering.

- Adjusting batch sizes: discovering 10k-row partitions ran as fast as 2k-row ones, delivering a 5x free speedup.

- Refactoring CTEs with explicit partitioning to avoid full materialization overhead.

The result was a runtime reduction from over six hours to under an hour. I also added versioning to output scores, so we could trace back exactly which code generated results—critical when later adjustments were required.

This project both improved underwriting decisions for returning customers and laid a foundation for more disciplined model versioning. It also taught me to combine SQL tuning, data normalization, and batch strategy in practical ways to achieve substantial performance gains.


## Optimized live underwriting pipeline by pruning features and rewriting feature engineering code, reducing latency by ~2.5s while maintaining accuracy to support a key retail partner., (2019-04-26)
Our live underwriting model pipeline had become too slow, exceeding 10 seconds in some cases, which was hurting conversion rates and jeopardizing relationships with major retail partners. The challenge was to speed up predictions without sacrificing accuracy.

First, I focused on feature selection. I was curious if cutting that down could yield a model with faster inference and equivalent performance. Using scikit-learn’s SelectKBest with the ANOVA F-statistic, I pruned features from 1,829 down to 1,000. Change in performancve was negligible. However, cutting further to 500 degraded accuracy noticeably. After discussion with colleagues, we settled on the top 1,000 features, which shaved ~1 second from runtime while keeping model performance essentially unchanged.

Next, I rewrote our feature engineering code almost from scratch. The existing implementation was pandas-heavy and overly object-oriented, making it both inefficient and hard to profile. By switching to raw Python and JSON-based feature definitions, I tailored the pipeline for single-row evaluation, which was the performance-critical case. I also separated “layer 1” raw features from “layer 2” derived features, simplifying both readability and extensibility. Historical-data paths, which were no longer in use, were stripped out, reducing unnecessary overhead.

This rewrite reduced latency by an additional 1.5–2 seconds. To validate correctness, I used Athena logs and S3-stored dataframe pickles to compare outputs between the new and old code paths. With only negligible precision differences, we gained confidence to deploy quickly.

Overall, the combined optimizations cut ~2.5 seconds from live underwriting latency while preserving model accuracy. This made our pipeline more competitive in a waterfall setup against other services, directly supporting improved conversion with one of our biggest retail partners.


## Rebuilt underwriting model with XGBoost + SageMaker after sudden data provider deprecation, ensuring business continuity and demonstrating the value of prior Dockerization and pipeline modularization., (2019)
When our main data provider abruptly deprecated their products, we had to rebuild our underwriting pipeline on very short notice to avoid losing a core business function.

I collaborated with a colleague to refresh the model and pipeline. My colleague incorporated the new features into our feature store and produced a fresh dataset. From there, I took on the feature engineering with the new data. Drawing on prior experience with XGBoost, I recognized it as a strong fit compared to our previous logistic regression model, since it handled missing values and scaling gracefully. This let me focus on one-hot encoding, binning, and categorical transforms with scikit-learn. I iterated quickly on models in SageMaker’s managed environment, validating with KS and logloss metrics, and ran overnight hyperparameter tuning jobs. We defined the stopping point by comparing the performance of new candidates directly against the prior production model, making the decision straightforward.

Because I had Dockerized our modeling pipeline the year prior, deployment was smooth: once we had a good candidate, I only needed to update the Dockerfile and add preprocessing code to a new branch. This made the model production-ready without major rework. While I briefly traveled abroad, my colleague continued iterating using the setup I had built—trimming non-contributory features and testing new Docker image versions.

The outcome was a new end-to-end underwriting pipeline and model, delivered under severe time constraints, that kept the business operating without interruption. Beyond the immediate win, the work demonstrated the value of earlier investments in containerization and modular pipeline design, which paid off when we needed agility most.


## Built custom PSI-based drift monitor to detect shifts in provider data, catching feature degradation early and flagging upstream product changes before they impacted model outputs for too long., (2019)
To monitor risks from shifts in our input data provider feeds, I implemented a Population Stability Index (PSI) measure on our top features. At the time, I didn’t find a reliable off-the-shelf solution, so I wrote the PSI logic from scratch using NumPy. The goal was to catch distribution drift between live data and training data before it silently degraded model performance.

The value of this approach did show up: the monitor flagged a significant drift in one of our most important features. With this evidence in hand, we engaged our data provider and confirmed that they had updated their product—without advance notice. By detecting the issue at the feature level, we were able to respond proactively, rather than waiting for degradation to surface through model outputs or downstream business metrics, which would have been slower and less informative.

This gave us an earlier warning system for data quality issues, reinforcing the importance of feature-level monitoring alongside model-level metrics.


## Tackled my first Kaggle project on aviation physiology with TensorFlow LSTMs, learning hard lessons in 3D time series data, scaling, and deep learning practice through months of weekend experiments., (2019, [link](https://michal.piekarczyk.xyz/project/2020-04-05-aviation-kaggle-low-level/))
My first (and only so far) Kaggle project was the Aviation Safety physiology classification challenge, which asked whether pilot state could be inferred from respiration, ECG, GSR, and EEG time-series data. I used it as an opportunity to dive into TensorFlow and LSTMs.

One of my early realizations was just how different time series data is: moving from 2D to 3D meant the 1.1 GB dataset could balloon to 256 GB if I wasn’t careful with sequence windows. This forced me to learn much more about NumPy’s reshaping tricks, h5py for chunked data, and how to avoid crashes during training. I also discovered that LSTMs are extremely sensitive to unscaled inputs—only after applying scaling did my logloss improve.

Along the way, I sharpened my tooling habits:

- Visualization: raw Matplotlib plots helped me track logloss and inspect time series.

- Workflow hygiene: I got disciplined with Jupyter Notebook experiments to avoid mixing datasets or models across days.

- Data balancing: because the dataset was so skewed, I compared balanced weights vs balanced training sets, eventually preferring balanced datasets to simplify preprocessing.

- Messy data reality: despite expectations of “clean Kaggle data,” I discovered the time series wasn’t even sorted by time—a frustrating but instructive experience.

I invested nearly half a year of weekends, often slotting in training runs before bed, before going on runs, or even while waiting at the Boston Amtrak terminal (where I once almost missed a bus while mulling over logits vs softmax probabilities!). I also had fun moments along the way, like reading Yann LeCun’s warning about large minibatches and immediately tweaking my SGD batch size, or realizing at a family birthday party that I finally understood the idea of neural network “capacity.”

Most competitors used gradient boosting (LightGBM/XGBoost), but I stuck with my LSTM path—it was less about leaderboard placement and more about learning deeply. While the final score wasn’t strong, the project gave me my first real immersion in deep learning practice: scaling, batching, managing experiments, wrangling messy time-series data, and living with the grind of trial and error.


## Parallelized and refactored third-party data provider pulls into fault-tolerant microservices, cutting underwriting latency by several seconds and improving resilience., (2018?)
An important retail partner challenged us to reduce live underwriting latency below five seconds, but our system was taking more than double that. A major bottleneck was the sequential way we called multiple third-party data providers during underwriting, and I proposed parallelizing these calls.

I refactored the relevant section of our monolith into an AWS Lambda-based microservice, using Python multiprocessing to fan out provider requests. For fault tolerance, I introduced S3 as a caching layer and designed the service with a clean API contract: a list of provider names in, transformed data out. Importantly, the function was written side-effect-free, using mocked provider data during tests, which made it easy to validate and extend.

During development, I also discovered that the true performance drag wasn’t only in provider pulls—it was in our feature engineering code. I optimized those transformations as well, shaving off additional seconds in dataframe construction.

The new design delivered two key benefits:

Speed – Vendor call latency was cut roughly in half, bringing us much closer to our performance target.

Resilience and maintainability – I added walltime monitoring and error handling so that if one provider failed, the pipeline could still proceed with partial data. It also became easier to add new providers or adjust existing logic within a smaller, testable service.

This project not only reduced underwriting time but also moved us toward a more modular, resilient architecture, setting the stage for future improvements (including later Step Functions-based orchestration).


## Decoupled underwriting ML pipeline from monolith into a SageMaker + Lambda microservice, enabling faster, safer model deployments with Dockerized scikit-learn under distinct versions of python., (2018)
At one point, our underwriting models were too tightly coupled to the company’s monolithic application. Feature engineering was abstracted behind layers of object-oriented code, making bugs hard to isolate. Even small changes required redeploying the entire monolith—an error-prone process that risked outages (and had already caused them).

To break this bottleneck, I designed and implemented a microservice-based approach using AWS SageMaker and Lambda. I began by containerizing one of our existing model artifacts, building a Docker-based pipeline that handled both feature preprocessing and model serving. From there, I rewrote the feature engineering code in a functional style, added unit tests, and integrated the service with an AWS Lambda + API Gateway stack. This allowed us to call SageMaker endpoints from Lambda for real-time predictions.

The decoupling effort gave us critical flexibility: the Dockerized approach supported models of different version of scikit-learn and python, and by splitting our underwriting stack into its own Git repo we reduced shared dependency conflicts with the monolith. Over many months of iterations and deployments, this system proved stable and significantly improved our ability to test, deploy, and evolve models independently.

Along the way, I encountered and fixed issues typical of building new infrastructure. One memorable debugging moment—the “Sweetgreen story”—involved accidentally caching QA database connections globally, which risked being reused in production Lambda calls. I caught the bug while debugging at a Sweetgreen restaurant, removed the global variable, and ensured environment isolation going forward.

This project was one of the first major steps in transforming our underwriting ML stack from brittle, tightly coupled code into a modular, testable, and resilient production system.


## Built an end-to-end bike-share destination prediction pipeline with feature engineering, SageMaker training, and geospatial preprocessing, blending hobby and learning to explore model performance and evaluation., (2017)
As a side project combining my biking hobby with data science, I worked on predicting Citibike rider destinations from trip and user attributes. My idea was to model a rider’s likely endpoint based on start time, location, and demographics — effectively, a small urban mobility prediction problem.

Early on, I realized predicting exact station IDs was too granular, so I broadened the prediction to neighborhoods, enriching the data with Google Geolocation API to get zip codes and neighborhood metadata. I also learned that timestamp precision (4:05 vs 4:06 p.m.) didn’t meaningfully affect outcomes, so I engineered time-based features using coarser hourly buckets.

Working through preprocessing taught me the subtle power of data handling: applying StandardScaler improved results; randomizing training splits reduced bias; and ensuring consistent test sets prevented misleading gains.

The project turned into a sandbox for modeling experimentation. I explored one-hot encoding, balanced training sets, and even switched evaluation to Top-K accuracy (a lesson borrowed from information retrieval). That’s when I discovered a big insight: although top-1 accuracy across 28 neighborhoods hovered around 0.5, top-3 accuracy reached 0.77 — a reminder that ranking metrics can be far more meaningful than single-class hits.

I eventually Dockerized and deployed the model using AWS SageMaker, gaining hands-on experience with reproducible training environments, hyperparameter tuning jobs, and model serving endpoints. A later debugging adventure taught me that missing geolocation data (and a lapsed Google API key!) could tank performance — an invaluable “garbage in, garbage out” lesson.

Overall, this project connected data science theory with real, messy data and real-world systems. It sharpened my understanding of geospatial features, temporal modeling, and production ML workflows, and it ultimately convinced my colleagues that I was serious about machine learning — leading to my formal move into our company’s data science team soon after.


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


## Reduced unnecessary address rejections by improving validation pass rates from ~85% to ~95%, through log analysis, Athena-based monitoring, and integration of Google Geocoding API for smarter normalization., (2017)
Our retailer operations team suspected that poor address validation was reducing conversion, so I took the initiative to investigate. I started by analyzing our existing logs in Sentry but quickly realized they were sampled (~10%), making them unreliable for analytical conclusions. This insight prompted me to build our first AWS Athena table for ingesting raw JSON logs, so we could properly measure address validation outcomes at full fidelity.

With this new infrastructure in place, I defined a new “pass rate” metric—the proportion of addresses successfully recognized by our downstream SmartyStreets USPS validator. The existing approach often failed to normalize addresses properly before validation, which led to unnecessary rejections.

Leveraging my experience with the Google Geocoding API, I introduced an additional normalization step to clean up addresses before sending them to SmartyStreets. This dramatically improved our pass rate—from around 85% to roughly 95%—and gave us much more reliable address recognition.

To help visualize progress, I built a quick Matplotlib stacked area chart in Jupyter, showing the pass rate improvement over time. I also collaborated with our business analytics team to make the new Athena dataset easily accessible for ongoing analysis.

Overall, this effort replaced ad hoc log sampling with a measurable, data-driven feedback loop, directly improving the customer experience and reducing operational friction for address validation.


## Built infrastructure to serve my company’s first ML underwriting model in 2015, using Redis + Django to deliver real-time predictions., (2015)
When I joined my first ML startup in 2015, we barely had any customer data—so our early system relied entirely on heuristics. By the time we landed our first paying customer, I volunteered to take a stab at training our first real model from the new data we’d started collecting.

Coming out of school, I knew ML theory but not practice. I reached for Weka (which I’d used academically), unaware that scikit-learn was already the industry standard. My results were underwhelming compared to those of a newly hired Data Scientist, who had prior experience and quickly outperformed me. Looking back, it was a humbling and pivotal moment: my academic background didn’t directly translate into production-ready applied ML.

I learned scikit-learn from him, and with the data we had—default customer data plus our first provider—I trained my first Random Forest model. While my colleague’s model ultimately won on AUC and was chosen for deployment, I contributed by building the infrastructure to host it.

I used Redis to cache the model, integrated it into our Django web server, and wrote the glue code to call `predict_proba` on new prospective customer data. This supported underwriting decisions in real time. To manage multiple models, I keyed them by retailer, allowing us to segment and transition more deliberately as we added new versions.

Though humbling, it was a defining career moment: a hands-on education in the difference between academic ML and applied ML, and my first experience building real infrastructure to bring a model into production.
