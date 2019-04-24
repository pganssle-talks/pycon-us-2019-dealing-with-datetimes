{%- extends 'basic.tpl' -%}

{%- block any_cell scoped -%}
{%- if cell.metadata.get('slide_start', False) -%}
<section>
{%- endif -%} {%- if cell.metadata.get('subslide_start', False) -%}
<section>
{%- endif -%}
{%- if cell.metadata.get('fragment_start', False) -%}
<div class="fragment">
{%- endif -%}

{%- if cell.metadata.slide_type == 'notes' -%}
<aside class="notes">
{{ super() }}
</aside>
{%- elif cell.metadata.slide_type == 'skip' -%}
{%- else -%}
{{ super() }}
{%- endif -%}

{%- if cell.metadata.get('fragment_end', False) -%}
</div>
{%- endif -%}
{%- if cell.metadata.get('subslide_end', False) -%}
</section>
{%- endif -%}
{%- if cell.metadata.get('slide_end', False) -%}
</section>
{%- endif -%}

{%- endblock any_cell -%}

{% block header %}
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8" />
<meta http-equiv="X-UA-Compatible" content="chrome=1" />

<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />

<title>Expressing recurring events</title>

<!-- General and theme style sheets -->
<link rel="stylesheet" href="{{resources.reveal.url_prefix}}/css/reveal.css">
<!--
<link rel="stylesheet" href="{{resources.reveal.url_prefix}}/css/theme/simple.css" id="theme">
-->

<!-- If the query includes 'print-pdf', include the PDF print sheet -->
<script>
if( window.location.search.match( /print-pdf/gi ) ) {
        var link = document.createElement( 'link' );
        link.rel = 'stylesheet';
        link.type = 'text/css';
        link.href = '{{resources.reveal.url_prefix}}/css/print/pdf.css';
        document.getElementsByTagName( 'head' )[0].appendChild( link );
}

</script>


{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
.reveal {
  font-size: 160%;
  overflow-y: scroll;
}
.reveal pre {
  width: inherit;
  padding: 0.4em;
  margin: 0px;
  font-family: monospace, sans-serif;
  font-size: 80%;
  box-shadow: 0px 0px 0px rgba(0, 0, 0, 0);
}
.reveal pre code {
  padding: 0px;
}
.reveal section img {
  border: 0px solid black;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0);
}
/*
.reveal i {
  font-style: normal;
  font-family: FontAwesome;
  font-size: 2em;
}
*/
.reveal .slides {
  text-align: left;
}
.reveal.fade {
  opacity: 1;
}
.reveal .progress {
  position: static;
}

.reveal .slides section .fragment.togglebold {
    opacity: 1 !important;
    visibility: visible !important;
}

.reveal .slides section .fragment.togglebold.current-fragment {
    font-weight: bold;
}

div.input_area {
  padding: 0.06em;
}
div.code_cell {
  background-color: transparent;
}
div.prompt {
  width: 11ex;
  padding: 0.4em;
  margin: 0px;
  font-family: monospace, sans-serif;
  font-size: 80%;
  text-align: right;
}
div.output_area pre {
  font-family: monospace, sans-serif;
  font-size: 80%;
}
div.output_prompt {
  /* 5px right shift to account for margin in parent container */
  margin: 5px 5px 0 0;
}
div.text_cell.rendered .rendered_html {
  /* The H1 height seems miscalculated, we are just hidding the scrollbar */
  overflow-y: hidden;
}

.rendered_html h1:first-child,
.rendered_html h2:first-child,
.rendered_html h3:first-child,
.rendered_html h4:first-child,
.rendered_html h5:first-child,
.rendered_html h6:first-child {
  margin-top: auto;
}

a.anchor-link {
  /* There is still an anchor, we are only hidding it */
  display: none;
}
.rendered_html p {
  text-align: inherit;
}
</style>

<!-- Custom stylesheet, it must be in the same directory as the html file -->
<link rel="stylesheet" href="custom.css">

</head>
{% endblock header%}


{% block body %}
{% block pre_slides %}
<body>
{% endblock pre_slides %}

<div class="reveal">
<div class="slides">
{{ super() }}
</div>
<div class="footer">
<span id="logo"><img src='images/zero-gray.svg'></span>
<span id="twitter">@pganssle</span>
<span id="website">https://ganssle.io</span>
</div>
<div class="footer">
</div>
</div>
{% block post_slides %}

<script src="{{resources.reveal.url_prefix}}/lib/js/head.min.js" ></script>
<script src="{{resources.reveal.url_prefix}}/js/reveal.js"></script>

<script>

Reveal.initialize({
    controls: true,
    progress: true,
    history: true,
    height: '95%',
    width: '95%',
    center: true,
    theme: Reveal.getQueryHash().theme, // available themes are in /css/theme
    transition: Reveal.getQueryHash().transition || 'linear', // default/cube/page/concave/zoom/linear/none

    // Optional libraries used to extend on reveal.js
    dependencies: [
        { src: "{{resources.reveal.url_prefix}}/lib/js/classList.js",
          condition: function() { return !document.body.classList; } },
        { src: "{{resources.reveal.url_prefix}}/plugin/notes/notes.js",
          async: true,
          condition: function() { return !!document.body.classList; } }
    ]
});


var update_scroll = function(event){
  $(".reveal").scrollTop(0);
};

Reveal.addEventListener('slidechanged', update_scroll);

</script>

</body>
{% endblock post_slides %}
{% endblock body %}

{% block footer %}
</html>
{% endblock footer %}
