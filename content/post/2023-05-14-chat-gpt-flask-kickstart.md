---
date: 2023-05-04
title: Using ChatGPT to kickstart a flask app?
---


## Context
Per an [earlier on-going interlude](https://michal.piekarczyk.xyz/post/2022-11-12-food-not-food/), I've been trying to more easily curate the photos I care to reference in passing in a conversation. This started out as [deduping photos and splitting out the photos of food](https://github.com/namoopsoo/manage-my-photos),  but at some point I realized I have so many photos I take as notes, taking those out by hand was getting tedious. I used this as an opportunity to test chat GPT's code-generating skills.

## Basically, I asked for a web interface around a flask app to help me out.
Here was my prompt
> can you please write a minimal simple python flask web app called "app.py" that will read a folder on my laptop that contains image files and has a simple REST API interface where GET will return the filename of a single image as json, say '{"filename": "some_file.jpg"}' and a POST will take a json input with a filename key and choice key for example like '{"filename": "some_file.jpg", "choice": "some_choice"}' and the "app.py" will move "some_file.jpg" into another folder named "some_choice". And then please create a minimal  single page html5 app called "choose_front_end.html" that can interact with the REST API of the flask app "app.py" previously described using the REST API GET and POST interface. I want to be able to open the "choose_front_end.html" in my web browser and have the GET API be called on "app.py" and I want to see the next image to get displayed and I want to be able to write into a text box a choice and I want then that choice that I write to be submitted as part of a POST to "app.py" . I want to be able to run both the flask "app.py" and the "choose_front_end.html" locally on my laptop on localhost.

And the response was pretty cool, with an `app.py` and `choose_front_end.html` like I asked, 

              {{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-05-04-Using-ChatGPT-to-kickstart-a-flask-app%3F/image_1684112637599_0.png" width="150%">}}

              {{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-05-04-Using-ChatGPT-to-kickstart-a-flask-app%3F/image_1684112678401_0.png" width="150%">}}

along with some helpful instructions on how to use this more or less.

## However, when I started test driving this, I realized some initial issues. 
First I noticed actually perhaps because of the output size limitations of the free version, the `choose_front_end.html` file was actually cut off in the middle, so I got the `displayNextImage` func but the `submitChoice` func was without a body.

## I also started testing out just the `GET` part since I did have the full `app.py` of the flask app, however this did not run because yea of course CORS was not setup here. 
And CORS is one of those notoriously difficult pieces of boilerplate to setup in any client server application communication even if you are just debugging something locally on your laptop.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-05-04-Using-ChatGPT-to-kickstart-a-flask-app%3F/image_1681606890326_0.png" width="100%">}}

```sh
  Access to fetch at 'http://127.0.0.1:5000/' from origin 'null' has been blocked 
  by CORS policy: No 'Access-Control-Allow-Origin' header is present on the 
  requested resource. If an opaque response serves your needs, set the 
  request's mode to 'no-cors' to fetch the resource with CORS disabled.
```

I had setup CORS within many web frameworks in the past but I have trouble with this every time. But after a bit of troubleshooting, I stumbled upon the fact that `flask` actually has some built-in CORS functionality syntactic sugar and I took advantage of that nicely!

### If you pip install, `pip install flask-cors`, you can basically do the CORS part with the few additional lines at the top here, 
                  
```python
from flask_cors import CORS

app = Flask("blah")
CORS(app)

@app.route("/", methods=["GET"])
def get_image():
    return make_response({"blah": "blah"})
def make_response(data):
  str_payload = json.dumps(data)

  mimetype = "application/json"
  response = flask.Response(response=str_payload,
                            status=200,
                            mimetype=mimetype)
  # response.headers["Access-Control-Allow-Origin"] = "*"
  # CORS_ORIGIN_ALLOW_ALL = True?
  # response.headers["Content-Type"] = "application/json"

  return response
```

## Ultimately after building out a good bit of functionality additional I did not realize I also wanted, I ended up with a solution I was able to run from my laptop and access from my ipad, for convenience,
              
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-05-04-Using-ChatGPT-to-kickstart-a-flask-app%3F/IMG_2585_1684089122525_0.jpeg" width="70%">}}

Definitely skipped a lot of details here! But will update more here later.

