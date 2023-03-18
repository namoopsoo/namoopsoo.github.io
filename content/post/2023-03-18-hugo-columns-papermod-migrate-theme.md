---
date: 2023-03-17
title: adjustments when migrating to hugo paper mod theme
---

## Quick note, I had moved to the  [PaperMod](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs) theme last month and have been slowly fixing a few things that borked.

### Images disappeared?
So first, my images disappeared all together , from [this post](/post/2020-06-06-heart-datar/)
I had them like 
```html
 <table>
 <tr>
    <td><img src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.42.png" width="30%"/></td>
    <td><img src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.49.png" width="30%" /></td>
    <td><img src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.44.39.png" width="30%" /></td>
 </tr>
 </table>
```
and I had to change them to be using the hugo language, below, then I saw the images again.
```html
 <table>
 <tr>
    <td> {{</* figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.42.png" width="30%"  */>}} </td>
    <td> {{</* figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.39.49.png" width="30%"  */>}} </td>
    <td> {{</* figure src="https://my-blog-content.s3.amazonaws.com/2020/06/06/wahoo/2020-06-06+11.44.39.png" width="30%"  */>}} </td>
 </tr>
 </table>
```
However, they were stacked on top of each other as opposed to three images like three columns in a table.

### Images in column layout
Prior to PaperMod, I had `<table><row><td>blah</td><td>blah</td><td>blah</td></row></table>` to lay out those three images in [this post](/post/2020-06-06-heart-datar/), but afterwards that broke. I read  that style is not data on [mozilla](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Multiple-column_Layout) that as a history lesson haha, using tables for layout is a thing of the past. Okay maybe that is why it broke? 

I read [here](https://discourse.gohugo.io/t/how-can-i-add-columns-into-my-page-using-shortcode/20201) about adding 

```
layouts/shortcodes/column.html
<div class="col-md">{{ .Inner }}</div>

layouts/shortcodes/row.html
<div class="row">{{ .Inner }}</div>
```

and 
```
{{</* row */>}}
{{</* column */>}} something1 {{</* /column */>}}
{{</* column */>}} something1 {{</* /column */>}}
{{</* column */>}} something1 {{</* /column */>}}
{{</* /row */>}} 
```

to do this job, but that did not work. And I suspected it was because I did not have `row` and `col-md` css classes defined anywhere. So I copied some interesting looking css from [here](https://getbootstrap.com/docs/4.0/layout/grid/) , 

```css
.row {
    display: -webkit-box;
    display: flex;
    flex-wrap: wrap;
}

.col-md {

    flex-basis: 0;
    -webkit-box-flex: 1;
    flex-grow: 1;
    max-width: 100%;
}
```
I tested this locally and it worked nicely. 

### But how to persist the style?
So Hugo uses git submodules for themes. Before, I was using the ananke theme, but I did not make any customizations to the css.

And now I `git clone` -d from [here](https://github.com/adityatelange/hugo-PaperMod) and according to 

[the faq on PaperMod](https://github.com/adityatelange/hugo-PaperMod/wiki/FAQs#bundling-custom-css-with-themes-assets), to update the css, one can do that with 

```
.(site root)
├── config.yml
├── content/
├── theme/hugo-PaperMod/
└── assets/
    └── css/
        └── extended/  <---
            ├── custom_css1.css <---
            └── any_name.css   <---
```
but for some reason the style on my custom branch was not taking when I published to github.io . 

I think that is because somewhere in there only the master branch was getting freshly pulled through Github Actions, so I forked  https://github.com/adityatelange/hugo-PaperMod, made the custom css updates in my fork, and that did the trick for me.


### Code wrapping!
I did not mention this above yet but actually my first custom css that I needed in `hugo-PaperMod` was the use of 

```css
code {
    white-space: pre-wrap !important;
}
```
which I had read about on stackoverflow, earlier as the solution with the most votes.

The lack of code wrapping had been bugging me for over a year and now with this simple custom css it was a reality!! Finally you don't need to endlessly scroll horizontally to actually read the code in a blog post.

