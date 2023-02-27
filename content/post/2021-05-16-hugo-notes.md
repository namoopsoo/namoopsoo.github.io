---
date: 2021-05-16
title: Notes on hugo
description: "Switched from Jekyll to Hugo"
summary: "Switched from Jekyll to Hugo"
categories:
  - notes
---

### 2021-05-16

#### Trying to figure out
* My homepage only shows "posts" and not "portfolio" or "handy" . Also my "about" page.
* How to add "preview images" to posts

#### Homepage
* [this](https://gohugo.io/templates/homepage/) is a starting point I think.
* Create `content/_index.md` ...
* Confusing but I think "templates" are stored in the `/layouts` directory.
* The "homepage template" is `/layouts/index.html` . If that doesnt exist a default one will be used I think.
* I copied this example below from [here](https://bwaycer.github.io/hugo_tutorial.hugo/content/using-index-md/)  , and I had to create `/layouts/partials/header.html`, `/layouts/partials/summary.html` for some errors to disappear. But anyhow, that just produced a blank homepage.
```
{{ partial "header.html" . }}
    <main>
          {{ .Content }}
          {{ range .Paginator.Pages }}
              {{ partial "summary.html" . }}
          {{ end }}
          {{ partial "pagination.html" . }}
    </main>
  {{ partial "sidebar.html" . }}
  {{ partial "footer.html" . }}
```
* But I just want to modify the homepage ever so slightly not completely override it.

#### Base template
* Not sure if I'm ready to use it yet but [here](https://gohugo.io/templates/base/) , I learned you can define a base template `/layouts/_default/baseof.html` like

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{ block "title" . }}
      <!-- Blocks may include default content. -->
      {{ .Site.Title }}
    {{ end }}</title>
  </head>
  <body>
    <!-- Code that all your templates share, like a header -->
    {{ block "main" . }}
      <!-- The part of the page that begins to differ between templates -->
    {{ end }}
    {{ block "footer" . }}
    <!-- More shared code, perhaps a footer but that can be overridden if need be in  -->
    {{ end }}
  </body>
</html>
```
* But you need to create `/layouts/_default/list.html`

```html
{{ define "main" }}
  <h1>Posts</h1>
  {{ range .Pages }}
    <article>
      <h2>{{ .Title }}</h2>
      {{ .Content }}
    </article>
  {{ end }}
{{ end }}
```

* and `/layouts/_default/single.html`

```html
{{ define "title" }}
  <!-- This will override the default value set in baseof.html; i.e., "{{.Site.Title}}" in the original example-->
  {{ .Title }} &ndash; {{ .Site.Title }}
{{ end }}
{{ define "main" }}
  <h1>{{ .Title }}</h1>
  {{ .Content }}
{{ end }}
```

#### preview images
* Ok nice finally found how to set images , from [here](https://themes.gohugo.io/gohugo-theme-ananke/#change-the-hero-background)  , the page for the "Ananke" theme that I am using. Maybe this is different for other themes.

* So in the front matter ( between the `---` and `---`) , you can add `featured_image: 'https://example.com/blahblah.jpg'` and that will be displayed in the background for instance , when I put that into the `content/_index.md` the homepage index.

### 2021-05-29

#### Hmm trying this approach for embedding images
[Here](https://hugo-geekblog.geekdocs.de/posts/post-with-images/ ) , where you do something like this

```
---
resources:
  - name: forest-1
    src: "images/forest-1.jpg"
    title: Forest (1)
    params:
      credits: "[Jay Mantri](https://unsplash.com/@jaymantri) on [Unsplash](https://unsplash.com/s/photos/forest)"
---

{ { < img name="forest-1" size="large" lazy=false > } }
```


* But I just tried this out and I'm getting this error now

```html
Rebuild failed:

"/blah..../content/en/post/2021-01-07-steak-two.md:29:1": failed to extract shortcode: template for shortcode "img" not found

{ { < img name="sizzle" size="small" lazy=true > } }
```

* Not sure but maybe resources must be in a page bundle and cannot have a source that is a uri.
