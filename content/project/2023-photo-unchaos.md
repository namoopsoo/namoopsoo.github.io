---
title: How to unchaos your photos?
date: 2023-05-29
summary: an interlude to having better grasp of an unwieldly photo situation
---

## Briefly
I want to have a curated photo gallery, but I take way too many photos for notes, so I need weed them out. 

The main idea is in this setup, both the Apple icloud photo thing and the Dropbox photo thing are both used. And python scripts are run to move what gets saved into the initial Dropbox "~/Dropbox/Camera Uploads/" area, to a "~/Dropbox/myphotos/" area, separated by month-dates like "2020/2020-05", "2020/2020-06" where python scripts next can be run to clean things up.

The python scripts live on [github](https://github.com/namoopsoo/manage-my-photos).

There are a few logical components.

- The script that moves photos to their year/month directories.
- The script that deduplicates (aka dedupes) photos.
- The food-not-food Docker server to identify photos of food.
- The flask server that helps to curate the rest.

## Dig deeper
### What's with the food photos?
There are some [earlier notes here](/post/2022-11-12-food-not-food/) about how the food photos get split out. The purpose here is that at one point I was inspired by a Peter Attia statement about how you might have various fluctuations in your metabolic health, but that you can typically look back at what you were eating when you were doing more or less well. Looking at the macro nutrient data like [in this post](/post/2023-03-25--alternate-day-fasting/) is great too, but it is also nice to have the parallel photographic information to help inform you what it is that you are eating.

### Making curating the photos slightly less tedious
Earlier [here](/post/2023-05-14-chat-gpt-flask-kickstart/), I described building a local flask app that can be accessed by ipad say, to help other photos that cannot yet be automatically sorted by a model such as the food-not-food model.

### Future though
But later on the food-not-food model can be extended to also sort out receipts and any other photos I don't exactly want in my pristine gallery.


