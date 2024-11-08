---
title: odd prompt?
date: 2024-11-06
---

looked at someone's fun project, 
https://www.npmjs.com/package/@rhettlunn/is-odd-ai
That uses GPT 3.5 to see if a number is odd, for fun.

My friend was asking has anyone evaluated this, so hmm i took a quick look. 
https://github.com/rhettlunn/is-odd-ai/blob/main/index.js


# Spotted two interesting things. 

## Prompt injection attack 
not sure if i just made that up, but like a SQL injection , the code that places user input into the prompt asking about oddness, doesn't type check if it is a number, and doesn't therefore have any way of knowing will someone attempt to insert some text that will cause GPT to escape its sandbox. of course chat GPT is intentionally sandboxed for most purposes, but it can still typically do internet research and GPT analysis can execute code in a limited VM. 
 
```

        // Construct the request payload
        const requestData = {
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: `Is ${number} odd or even?` }],
            temperature: 0.7
        };

```

## the response is not checking for negatives
presumably the response might be "no this is not odd ", but this code will see the word "odd" and therefore the answer will be considered "odd" anyways. 

```

        // Determine if the response indicates odd or even
        if (answer.includes('odd')) {
            return true;
        } else if (answer.includes('even')) {
            return false;
        } else {
            throw new Error('Unable to determine if number is odd or even.');
        }
```


