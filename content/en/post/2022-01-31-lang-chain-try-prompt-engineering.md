---
title: Try some lang chain prompt engineering
date: 2023-01-31
---


So I wonder would you use a prompt template with the name of the person maybe as an input variable, prior to a free chat open ended conversation?

I am particularly super curious can we use prompt engineering to convey that the person on the other end is a customer say, so they might use personal pronouns like "my", "me", etc ? Using https://langchain.readthedocs.io/en/latest/modules/memory/examples/chatgpt_clone.html to help try this.
  
  ```python
  from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
  from langchain.chains.conversation.memory import ConversationalBufferWindowMemory
  from langchain import PromptTemplate
  
  no_input_prompt = PromptTemplate(input_variables=[], template="Tell me a joke.")
  no_input_prompt.format()
  
  template = """Assistant is a large language model trained by OpenAI.
  
  Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
  Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
  Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
  Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  Alfred Jamesmanson has brown hair. 
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  Alfred Jamesmanson: {human_input}
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
      memory=ConversationalBufferWindowMemory(k=2),
  )
  
  output = chatgpt_chain.predict(
    human_input="Hi my name is Alfred Jamesmanson. I need your help Assistant. What color is my hair?")
  print(output)
  
  ```

  ```python
  > Entering new LLMChain chain...
  Prompt after formatting:
  Assistant is a large language model trained by OpenAI.
  
  Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
  Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
  Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
  Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  Alfred Jamesmanson has brown hair. 
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  Alfred Jamesmanson: Hi my name is Alfred Jamesmanson. I need your help Assistant. What color is my hair?
  Assistant:
  
  
  > Finished chain.
  Hello Alfred Jamesmanson, your hair is brown.
  ```

Ok so when I tried that above, I got one answer so that is nice, but I did not get into a long conversation.
  
Oh maybe I'm supposed to continue?
  
  ```python
  output = chatgpt_chain.predict(
    human_input="Thank you Assistant. I forget, who are my closest friends?")
  print(output)
  ```
  ```python
  
  > Entering new LLMChain chain...
  Prompt after formatting:
  Assistant is a large language model trained by OpenAI.
  
  Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
  Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
  Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
  Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  Alfred Jamesmanson has brown hair. 
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  Alfred Jamesmanson: Thank you Assistant. I forget, who are my closest friends?
  Assistant:
  
  
  > Finished chain.
  Your closest friends are Kelly Robin, Jesse Lambourghini, and Jackson Loggin.
  
  ```
  Ok nice , yes looks like it.
  
  ```python
  output = chatgpt_chain.predict(
    human_input="Ah ok. Where do I live? What is the closest airport to me ?")
  print(output)
  ```
  ```python
  
  > Entering new LLMChain chain...
  Prompt after formatting:
  Assistant is a large language model trained by OpenAI.
  
  Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
  Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
  Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
  Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  Alfred Jamesmanson has brown hair. 
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  Alfred Jamesmanson: Ah ok. Where do I live? What is the closest airport to me ?
  Assistant:
  
  
  > Finished chain.
  Alfred Jamesmanson lives in Dallas, Texas. The closest airport to Alfred Jamesmanson is Dallas/Fort Worth International Airport (DFW).
  
  ```
  wow nice.
  
  ```python
  output = chatgpt_chain.predict(
    human_input="Ah ok. Based on my education, what kind of jobs should I apply for?")
  print(output)
  ```
  
  ```python
  > Entering new LLMChain chain...
  Prompt after formatting:
  Assistant is a large language model trained by OpenAI.
  
  Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
  Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
  Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
  Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
  Alfred Jamesmanson has brown hair. 
  
  Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
  
  Alfred Jamesmanson: Ah ok. Based on my education, what kind of jobs should I apply for?
  Assistant:
  
  
  > Finished chain.
  Based on your education in electrical engineering, you should consider applying for jobs in the engineering field. You could look for positions in electrical engineering, computer engineering, software engineering, and other related fields. Additionally, you could consider applying for positions in research and development, product design, and other related fields.
  
  ```

Ok this is amazing. Let me try a meta question.

```python

In [27]: output = chatgpt_chain.predict(
    ...:   human_input="Thank you. Can we please go over what we just talked about one more time? Can 
    ...: you please summarize this for me?")
    ...: print(output)


> Entering new LLMChain chain...
Prompt after formatting:
Assistant is a large language model trained by OpenAI.

Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
Alfred Jamesmanson has brown hair. 

Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Alfred Jamesmanson: Thank you. Can we please go over what we just talked about one more time? Can you please summarize this for me?
Assistant:


> Finished chain.
Sure, Alfred. You told me that you live in Dallas, Texas, were born in Keywest, Florida on January 2nd, 1990, are studying electrical engineering in college, and have brown hair. You also mentioned that you are friends with Kelly Robin, Jesse Lambourghini, and Jackson Loggin.


```

Some math?

```python
In [28]: output = chatgpt_chain.predict(
    ...:   human_input="Thanks. Hey you did not wish me a happy birthday. Isn't it my birthday that ju
    ...: st passed? How old am I now?")
    ...: print(output)


> Entering new LLMChain chain...
Prompt after formatting:
Assistant is a large language model trained by OpenAI.

Assistant is designed to answer questions about a fictional person named Alfred Jamesmanson. 
Alfred Jamesmanson lives in Dallas Texas. Alfred Jamesmanson was born in Keywest Florida on January 2nd 1990.
Alfred Jamesmanson goes to college. Alfred Jamesmanson studies electrical engineering. 
Alfred Jamesmanson is friends with Kelly Robin, Jesse Lambourghini and Jackson Loggin.
Alfred Jamesmanson has brown hair. 

Assistant is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Alfred Jamesmanson: Thanks. Hey you did not wish me a happy birthday. Isn't it my birthday that just passed? How old am I now?
Assistant:


> Finished chain.
Happy belated birthday, Alfred! You are now 30 years old.


```
