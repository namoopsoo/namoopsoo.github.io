---
date: 2024-05-24
title: issue experienced in typewise logseq interaction
---

An example that is around undo-ing auto-corrections,  when using the Logseq app. 
This is on on typewise 4.0.9 .

https://vimeo.com/909485587/55e0b4f639

{{ vimeo 909485587/55e0b4f639 }}

Issue occurs around 00:49:00 .

I write "[[refactoring]]" , which gets changed to "[[refarefactor" , then i hit the blue undo "refactori↩️" and that changes to "[[refarefactori" . Then i shake undo. That brings back the original text.

# one more example 
https://vimeo.com/948393509
{{ vimeo 948393509 }}


# Thoughts as to why 

The issue I suppose is that when one types some text, on typewise, a buffer of the immediate text is kept, so if typewise auto-corrects, and someone taps the "↩️" undo , typewise attempts to replace the suggestion with the previous buffer. And if typewise is being used in an app that, say, modifies the text after typewise captures its buffer, but then applies an autocorrect, then of course the undo will not make sense. But say if typewise captures its buffer instead, not right after the last typewise keystroke, but before typewise issues its autocorrect, then everything would be golden. 


