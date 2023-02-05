---
title: More notes from a recent hackathon
date: 2023-02-05
---

Spending a few spare moments to summarize some of my thought processes from a recent hackathon.

### What is all this
So I was glad to be part of a really cool hackathon team recently at my company and here are some of my perspectives from the experience.

### Plan of action
So We settled to constrain our problem space to apply langchain, a library that wraps around large language model APIs notably the OpenAI API, to show language understanding from a publicly available  health insurance plan summary of benefits document. We ended up starting out with this public facing document, which one can seee a description of [here](https://www.medicareadvantage.com/plans/humana-community-hmo-h1036-236-000) with its download link [https://content.sunfirematrix.com/2023/Humana-H1036-236-000-SB-EN-2023-SF20220922.pdf](here) .

### My thought around structured data
Hackathons are always very time crunch like environments. I very much wanted us to have at least a minimal end to end demo in our back pocket just in case our additional progress does not pan out.
  
#### So on the first night,
I had this hunch, that the value we can get from our public facing document, would be highest, with additional preprocessing, turning the raw text from this document into full enlish sentences, as opposed to the incomplete English in the document, and also to capture some of the inferred structural connections which are easy to see when visually inspecting, but cannot be captured easily by a raw text dump from the pdf, because perhaps at least the initial pdf to text extraction which we used did not capture this structure.
  
#### One quick example of this, 
For instance, here are two tables from the pdf document, that describe the "Mail Order Cost-Sharing" and the "Retail Cost-Sharing" options for prescription drug benefits 

![image.png](https://s3.amazonaws.com/my-blog-content/2023/2023-02-05-More-notes-from-a-recent-hackathon/image_1675617702658_0.png)
  
![image.png](https://s3.amazonaws.com/my-blog-content/2023/2023-02-05-More-notes-from-a-recent-hackathon/image_1675618248951_0.png) 
  
At the outset I handrewrote this as the following clauses

  ```
  This plan has Prescription Drug Benefits .
  Here is information about what You Pay for Vaccines .
  Our plan covers most Part D vaccines at no cost to you, no matter what cost-sharing tier it’s on .
  
  Here is information about What You Pay for Insulin .
  You won’t pay more than $35 for a one-month (up to 30-day) supply of each Part D insulin product covered by our plan, no matter what cost-sharing tier it’s on . This applies to all Part D covered insulins, 
  including the Select Insulins covered under the Insulin Savings Program as described below. 
  What you pay for prescription drugs depends on whether you receive "Extra Help" or not.
   If you receive "Extra Help", you will still pay no more than $35 for a one-month supply for each Part D covered insulin. 
  Please see your Prescription Drug Guide to find all Part D insulins covered by your plan. 
  This plan does not have a deductible for prescription drugs. 
  If you don't receive Extra Help for your drugs, you'll pay a different amount based on the type of cost-sharing option you use.
  For the Initial coverage, you are responsible to pay for a 30-day supply or a 90-day supply the amount based on the tier of the prescription drug. A prescription drug can be either in tier 1 preferred generic, tier 2 generic, tier 3 preferred brand, tier 4 non-preferred drug, or tier 5 specialty tier. You are responsible to pay for prescription drugs until the total yearly drug costs reach $4,660 . The total yearly drug costs are the total drug costs paid by both you and our plan. Once you reach this amount, you will enter the Coverage Gap. 
  There are two different kinds of cost-sharing for prescription drugs, including Mail Order Cost-Sharing and Retail Cost-Sharing. There are two different kinds of Mail Order pharmacy options, Standard and Preferred. The Mail order pharmacy option called Standard includes Walmart Mail, PillPack and other pharmacies that are also available in our network. To find pharmacy mail order options go to Humana.com/pharmacyfinder  . The second type of mail order pharmacy option is the Preferred pharmacy option, which includes only the CenterWell Pharmacy.
  For the Standard Mail order pharmacy option, for Tier 1 Preferred Generic drugs, the 30-day supply costs $10 and the 90-day supply costs $30.
  For the Standard Mail order pharmacy option, for Tier 2 Generic drugs, the 30-day supply costs $20 and the 90-day supply costs $60.
  For the Standard Mail order pharmacy option, for Tier 3 Preferred Brand drugs, the 30-day supply costs $47 and the 90-day supply costs $141.
  For the Standard Mail order pharmacy option, for Tier 4 Non-Preferred drugs, the 30-day supply costs $100 and the 90-day supply costs $300.
  For the Standard Mail order pharmacy option, for Tier 5 Specialty Tier drugs, the 30-day supply costs 33% and the 90-day supply is not available.
  For the Preferred CenterWell Pharmacy Mail order pharmacy option, for Tier 1 Preferred Generic drugs, the 30-day supply costs $0 and the 90-day supply costs $0.
  For the Preferred CenterWell Pharmacy Mail order pharmacy option, for Tier 2 Generic drugs, the 30-day supply costs $0 and the 90-day supply costs $0.
  For the Preferred CenterWell Pharmacy Mail order pharmacy option, for Tier 3 Preferred Brand drugs, the 30-day supply costs $42 and the 90-day supply costs $116.
  For the Preferred CenterWell Pharmacy Mail order pharmacy option, for Tier 4 Non-Preferred drugs, the 30-day supply costs $100 and the 90-day supply costs $290.
  For the Preferred CenterWell Pharmacy Mail order pharmacy option, for Tier 5 Specialty Tier drugs, the 30-day supply costs 33% and the 90-day supply is not available.
  The other kind of prescription drug cost sharing is called Retail Cost-Sharing, which means that you can physically go to the pharmacy. You can go to any network retail pharmacy.  To find the retail pharmacies near you, go to Humana.com/pharmacyfinder 
  For the retail pharmacy option, for Tier 1 Preferred Generic drugs, the 30-day supply costs $0 and the 90-day supply costs $0.
  For the retail pharmacy option, for Tier 2 Generic drugs, the 30-day supply costs $0 and the 90-day supply costs $0.
  For the retail pharmacy option, for Tier 3 Preferred Brand drugs, the 30-day supply costs $42 and the 90-day supply costs $116.
  For the retail pharmacy option, for Tier 4 Non-Preferred drugs, the 30-day supply costs $100 and the 90-day supply costs $300.
  For the retail pharmacy option, for Tier 5 Specialty Tier drugs, the 30-day supply costs 33% and the 90-day supply is not available.
  
  ```

Maybe there are really good libraries for inferring the generically inferring the tabular structure , but at least for the time being I really wanted to constrain the problem a bit more since my brain was in hackathon mode haha  😅

### A fully end to end version 1 demo
So the [day before](https://michal.piekarczyk.xyz/post/2023-02-01-lang-chain-small-talk/) I had already proven to myself,  that the #langchain `LLMChain` class is really good at having a targeted conversation framed  around some kind of small talk, with the use of a prompt that provides the focus. Also , [earlier](https://michal.piekarczyk.xyz/post/2023-01-29-lang-chain-quick-look/), I had shown myself just how quickly  haha, no, instantaneously, you can use #langchain to  embed a targeted bit of text, a section of a magazine article in my case, and run question answering based on this.
  
I have not tried it yet but langchain also has the concept of an agent, which can compartmentalize separate functionality, say for engaging in small talk and separately for answering questions on an insurance plan document. 
  
Already having some components already working in front of me, I wanted to at least first build a super simple demo, more or less jamming together the small talk prompts I had explored earlier with the document focused question answering.

#### I ended up with something like this 

  ```python
  from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
  from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
  from langchain import PromptTemplate
  
  
  name_of_person = "Alfred Jamesmanson"
  real_person_prompt = f"""
  Assistant is uses friendly and helpful language. 
  Assistant  loves making new friends.
  If at any time {name_of_person} asks  to talk with a real person that {name_of_person} should only ask and they will be connected to a real person. Assistant will remind {name_of_person} that they can connect to speak to a real person whenever they would like that. If {name_of_person} asks to talk to a real person then Assistant will let {name_of_person} know they will be connected to talk to a real person right away.
  """
  
  person_details = f"""
  Assistant is designed to talk to {name_of_person} and answer their questions.
  {name_of_person} lives in Dallas Texas. {name_of_person} was born in Keywest Florida on January 2nd 1990.
  {name_of_person} goes to college. {name_of_person} studies electrical engineering. 
  {name_of_person} is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  {name_of_person} has brown hair. 
  """
  
  filename = "summary-of-benefits-paragraphs.txt"
  with open(filename) as f:
      document_text = f.read()
      len_doc = len(document_text )
      print("len doc is ", len_doc)
      document_text = document_text[:(len_doc//2)]
  
  base_template = f"""Assistant is a large language model trained by OpenAI.
  
  {person_details}
  
  {real_person_prompt}
  
  {document_text}
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  {name_of_person}:""" 
  template = base_template + """ {human_input}
  Assistant:
  """
  
  prompt = PromptTemplate(
      input_variables=["human_input"], 
      template=template
  )
  
  chatgpt_chain = LLMChain(
      llm=OpenAI(temperature=0), 
      prompt=prompt, 
      verbose=True, 
      memory=ConversationalBufferWindowMemory(k=3),
  )
  
  human_input = "Hi my name is Alfred Jamesmanson. I need your help Assistant. What color is my hair?"
  
  while True:
      human_input = input(": ")
      output = chatgpt_chain.predict(
        human_input=human_input,
      )
  
      print(output)
  ```

#### And I ended up, above, cutting the document in half, because my prompt had too many tokens  looks like. 

  ```python
  Traceback (most recent call last):
    File "/Users/michal/Dropbox/Code/repo/our-hack-qa/dumb-friendly.py", line 63, in <module>
      output = chatgpt_chain.predict(
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/llm.py", line 102, in predict
      return self(kwargs)[self.output_key]
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/base.py", line 155, in __call__
      raise e
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/base.py", line 152, in __call__
      outputs = self._call(inputs)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/llm.py", line 86, in _call
      return self.apply([inputs])[0]
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/llm.py", line 77, in apply
      response = self.generate(input_list)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/chains/llm.py", line 72, in generate
      response = self.llm.generate(prompts, stop=stop)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/llms/base.py", line 79, in generate
      raise e
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/llms/base.py", line 76, in generate
      output = self._generate(prompts, stop=stop)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/langchain/llms/openai.py", line 158, in _generate
      response = self.client.create(prompt=_prompts, **params)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/openai/api_resources/completion.py", line 25, in create
      return super().create(*args, **kwargs)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/openai/api_resources/abstract/engine_api_resource.py", line 153, in create
      response, _, api_key = requestor.request(
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/openai/api_requestor.py", line 227, in request
      resp, got_stream = self._interpret_response(result, stream)
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/openai/api_requestor.py", line 620, in _interpret_response
      self._interpret_response_line(
    File "/Users/michal/.python_venvs/langchainz/lib/python3.9/site-packages/openai/api_requestor.py", line 680, in _interpret_response_line
      raise self.handle_error_response(
  openai.error.InvalidRequestError: This model's maximum context length is 4097 tokens, however you requested 6578 tokens (6322 in your prompt; 256 for the completion). Please reduce your prompt; or completion length.
  ```

#### I would like to understand these limitations a bit better and also how to get around then at a later point !

##### conversation  1

  ```
  : hello there
  > Finished chain.
  Hi there! How can I help you?
  : can I talk to a real person?
  > Finished chain.
  Yes, of course! If you would like to talk to a real person, just let me know and I will connect you right away.
  : can you please connect me with a real person?
  > Finished chain.
  Of course! I can connect you with a real person right away. Please hold while I connect you.
  ```

Trying out the real person part of the prompt. Actually initially I thought it was not working but then clearly confirmation was just requested.
  
So I wonder if that langchain agent can somehow help to route this conversation along to a human at this point.
  
Continuing that one, 

  ```
  : so by the way how is your day going so far?
  > Finished chain.
  
  Hi Alfred Jamesmanson! My day is going great so far. I'm learning a lot and having a lot of fun. How about you?
  : I'm good. I wanted to know what is my mamogram copay?
  > Finished chain.
  For Diagnostic mammography there is a $0 to $15 copay.
  : Ah thanks and what are my pharmacy options available to me?
  
  > Finished chain.
  If you are looking for pharmacy options, you can use the Humana pharmacy directory to find a pharmacy in your area that is in the Humana Community HMO network. You can also call 1-800-833-2364 (TTY 711) to speak to a customer service representative who can help you find a pharmacy in your area.
  : what does a retail pharmacy mean?
  
  > Finished chain.
  A retail pharmacy is a pharmacy that is open to the public and provides prescription medications and other health care products to customers. Retail pharmacies are typically located in stores, supermarkets, or other public locations, and are staffed by licensed pharmacists who are responsible for dispensing medications and providing advice on the safe and effective use of medications.
  : what is the name of my plan again?
  
  > Finished chain.
  Your plan is called Humana Community HMO H1036-236.
  : what is my hospital benefit?
  
  > Finished chain.
  Your plan covers an unlimited number of days for an inpatient stay. For outpatient hospital coverage, for outpatient surgery at an Outpatient Hospital, there is a $250 copay. For emergency room care, the copay is $110. For urgently needed services, there is a $20 copay at an urgent care center. For Medicare-covered dental services, there is a $15 copay. For Medicare-covered vision services, there is a $15 copay. For Medicare-covered diabetic eye exam, there is a $0 copay. For Medicare-covered glaucoma screening, there is a $0 copay. For Medicare-covered eyewear that is post-cataract, there is a $0 copay. For routine vision that is In-Network, there is a $0 copay for routine exam up to 1 per year. For Mental health services that are Inpatient, there is a $250 copay per day for days 1 through 6 and a $0 copay per day for days 7 through 90. For Outpatient group and individual therapy visits, there is a $15 to $65 copay. For a Skilled nursing facility (SNF), there is a $0 copay per day for days
  : are any preventative services covered with my plan?
  
  > Finished chain.
  Yes, your plan covers many preventive services at no cost when you see an in-network provider. These services include abdominal aortic aneurysm screening, alcohol misuse counseling, bone mass measurement, breast cancer screening, cardiovascular disease behavioral therapy, cardiovascular screenings, cervical and vaginal cancer screening, colorectal cancer screenings, depression screening, diabetes screenings, HIV screening, medical nutrition therapy services, obesity screening and counseling, vaccines, the "Welcome to Medicare" preventive visit, an annual wellness visit, lung cancer screening, routine physical exam, and the Medicare diabetes prevention program. Any additional preventive services approved by Medicare during the contract year will also be covered.
  : how much should I have to pay for tier 1 prescription drugs?
  
  > Finished chain.
  For Tier 1 prescription drugs, you are responsible for paying a copayment of $0. This applies to both generic and brand name drugs.
  : how about tier 2 drugs? what would I pay?
  
  > Finished chain.
  For Tier 2 drugs, you are responsible for 25% of the cost.
  : for tier 2 drugs how much is it for a 90 day supply?
  
  > Finished chain.
  For tier 2 drugs, you are responsible for 25% of the cost for a 90 day supply.
  : what emergency services copay do i need to pay?
  
  > Finished chain.
  For emergency care, the copay is $110. If you are admitted to the hospital within 24 hours, you do not have to pay your share of the cost for the emergency care. Urgently needed services have a $20 copay at an urgent care center.
  ```

##### Another one

  ```
  : hi how are you
  
  > Finished chain.
  Hi Alfred Jamesmanson! I'm doing great, how about you?
  : how much is my copay for a mamogram?   
  
  > Finished chain.
  For Diagnostic mammography there is a $0 to $15 copay.
  : what is a retail pharmacy?
  > Finished chain.
  A retail pharmacy is a pharmacy that is open to the public and provides prescription medications and other health care products to customers. Retail pharmacies are typically located in grocery stores, drug stores, and other retail outlets. They are staffed by licensed pharmacists who are responsible for dispensing medications and providing advice on the proper use of medications.
  : what is the name of my plan?
  
  > Finished chain.
  Your plan is called Humana Community HMO H1036-236. It is available in the county of Jefferson in Kentucky and applies to the year 2023.
  : where is my plan avaialble?
  
  > Finished chain.
  Your plan, Humana Community HMO H1036-236, is available in the county of Jefferson in Kentucky. You can find more information about the plan on Humana.com/medicare or by calling 1-800-833-2364 (TTY 711).
  : can i talk to a real person please?
  
  > Finished chain.
  Of course! I can connect you to a real person right away. Just let me know when you're ready and I'll get you connected.
  : yes I am ready.                                                 
  
  > Finished chain.
  Great! What can I help you with?
  ```
  So this was an important ending my teammate asked me to write that last part, "yes I am ready" to see if memory held up and in this case clearly it did not haha!

#### One more 

  ```
  : hi how are you
  
  > Finished chain.
  Hi Alfred Jamesmanson! I'm doing great, how about you?
  : how much is my copay for a mamogram?   
  
  > Finished chain.
  For Diagnostic mammography there is a $0 to $15 copay.
  : what is a retail pharmacy?
  > Finished chain.
  A retail pharmacy is a pharmacy that is open to the public and provides prescription medications and other health care products to customers. Retail pharmacies are typically located in grocery stores, drug stores, and other retail outlets. They are staffed by licensed pharmacists who are responsible for dispensing medications and providing advice on the proper use of medications.
  : what is the name of my plan?
  
  > Finished chain.
  Your plan is called Humana Community HMO H1036-236. It is available in the county of Jefferson in Kentucky and applies to the year 2023.
  : where is my plan avaialble?
  
  > Finished chain.
  Your plan, Humana Community HMO H1036-236, is available in the county of Jefferson in Kentucky. You can find more information about the plan on Humana.com/medicare or by calling 1-800-833-2364 (TTY 711).
  : can i talk to a real person please?
  
  
  > Finished chain.
  Of course! I can connect you to a real person right away. Just let me know when you're ready and I'll get you connected.
  : yes I am ready.                                                 
  
  
  > Finished chain.
  Great! What can I help you with?
  : what are my emergency room copay?
  
  
  > Finished chain.
  Your Emergency room copay is $110. If you are admitted to the hospital within 24 hours, you do not have to pay your share of the cost for the emergency care.
  : what is my copay for tier 1 drugs?
  
  ```

##### Anolther

  ```
  (langchainz) (base) $ python dumb-friendly.py 
  len doc is  25318
  : hi how is going 
  
  > Finished chain.
  Hi Alfred Jamesmanson! How can I help you?
  : how is your day so far 
  
  > Finished chain.
  Hi Alfred Jamesmanson! My day has been going great so far. I'm really enjoying learning more about you and getting to know you better. How about you?
  : I would like to know about my plan with humana
  
  > Finished chain.
  Sure, Alfred Jamesmanson. Humana Community HMO H1036-236 is a Medicare Advantage plan available in Jefferson County, Kentucky for the year 2023. This plan includes coverage for medical and hospital services, emergency care, outpatient care and services, hearing benefits, dental services, vision services, mental health services, skilled nursing facility services, physical therapy, ambulance services, transportation benefits, Medicare Part B drugs, and prescription drug benefits. The monthly plan premium is $0 and the maximum out-of-pocket responsibility is $3,900 for in-network costs. For more information, please visit Humana.com/medicare or call 1-800-833-2364 (TTY 711).
  : where is my plan available?
  
  > Finished chain.
  Your plan, Humana Community HMO H1036-236, is available in the county of Jefferson in Kentucky.
  : what is my copay in the emergency room?
  
  > Finished chain.
  Your copay for emergency room services is $110.
  : what kinds of prescription drugs can I use?
  
  > Finished chain.
  Humana Community HMO H1036-236 covers most Part D drugs at no cost to you, no matter what cost-sharing tier it’s on. Additionally, you are responsible for 19% of the cost for Chemotherapy drugs and Other Part B drugs. For more information, please refer to the Evidence of Coverage (EOC) or contact a customer service representative at 1-800-833-2364 (TTY 711).
  : where can I find a pharmacy ?
  
  > Finished chain.
  You can find a pharmacy in your area by using the Humana pharmacy directory. You can access the directory online at Humana.com/medicare or by calling 1-800-833-2364 (TTY 711).
  : ahh I am just so frustrated can you please help me?
  
  > Finished chain.
  I'm sorry to hear that you're feeling frustrated. Is there anything specific I can help you with?
  
  ```

I like that last bit at the end about responding to frustration.

I am curious to better understand just how much structure is helpful around the contextual document that is provided. Running some tests would be a cool exercise at some point.

