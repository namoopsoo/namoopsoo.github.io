---
title: "Without a Paddle"
# slug: "2026-06-19-without-a-paddle"
date: 2026-06-19T16:40:44-04:00
# draft: true

# optional thumbnail
# images:
#   - "THUMBNAIL_PLACEHOLDER"
# cover:
#   image: "THUMBNAIL_PLACEHOLDER"
---

I have been using apple macos transcription on my handwritten notes every once in a while, where you manually select text from some png or pdf and copy paste, into a text document, but it is pretty awful. Is bad because it misses many of the bounding boxes and even then makes so many transcription errors, that I might as well just transcribe it myself. And so ultimately I was wondering if a hugging face model is better at the transcription. I learned about https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5 from chatgpt. 

I had some missteps, but eventually got it to run on my 2017 macbook. However wow this is a powerful model and although it seems to do better on my handwriting and does box bounding out of the box, but it took 9 minutes to process one 1MB pdf file on my laptop, so I think I need to find a simpler model.


#### image I was processing

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-06-19-without-a-paddle/image_1781902152131_0.png" width="50%">}}

#### The table output produced by the model

<table><tr><td>Reference Data</td><td>Features</td><td>Scores</td><td>Top-drivers</td></tr><tr><td rowspan="3">Actual Data</td><td>bootshop</td><td>bootshop</td><td></td></tr><tr><td>features</td><td>scores</td><td>top-drivers</td></tr><tr><td></td><td>write</td><td>model scores check</td></tr><tr><td>AppTeam</td><td>bootshop</td><td>generate top drivers</td><td>pass/fail</td></tr><tr><td>P64FirmTeam</td><td></td><td></td><td></td></tr></table>

# references

1. https://huggingface.co/PaddlePaddle/PaddleOCR-VL-1.5
2. https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/install/docker/linux-docker_en.html
3. https://github.com/PaddlePaddle/PaddleOCR
4. https://www.paddleocr.ai/latest/en/version3.x/pipeline_usage/PaddleOCR-VL.html#manual-install-inference-engine-and-paddleocr

