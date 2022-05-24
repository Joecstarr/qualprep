import genanki
import re
import html
import os
from pathlib import Path

cwd = Path(os.getcwd())

preamble = r"""

<script>
var ua = navigator.userAgent.toLowerCase();
var isAndroid = ua.indexOf("android") > -1;
if(isAndroid == false)
{
var els = document.querySelectorAll("a[href='https://ankiweb.net/']");
var length = els.length;
if (length == 0) {
    MathJax.config.tex['extensions'] = ["AMSmath.js", "AMSsymbols.js", "AMScd.js"];
    MathJax.config.tex['processEscapes'] = true;
    MathJax.config.tex['processEnvironments'] = true;
    MathJax.startup.getComponents();
}
else {
  MathJax = {
    tex: {
      inlineMath: [['\\(', '\\)']],
      displayMath: [['\\[', '\\]']],
      processEscapes: true,
      processEnvironments: true,
      extensions: ["AMSmath.js", "AMSsymbols.js", "AMScd.js"],
    },
    options: {
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
    }
  };
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
  document.body.appendChild(script);
}}
</script>

<div style="display: none;">

\(\newcommand{\N}{\mathbb{N}}\)
\(\newcommand{\C}{\mathbb{C}}\)
\(\newcommand{\Z}{\mathbb{Z}}\)
\(\newcommand{\Q}{\mathbb{Q}}\)
\(\newcommand{\R}{\mathbb{R}}\)
\(\newcommand{\LP}{\left(}\)
\(\newcommand{\RP}{\right)}\)
\(\newcommand{\LS}{\left\lbrace}\)
\(\newcommand{\RS}{\right\rbrace}\)
\(\newcommand{\LB}{\left[}\)
\(\newcommand{\RB}{\right]}\)
\(\newcommand{\MM}{\ \middle|\ }\)
\(\newcommand{\abs}[1]{\left\vert#1\right\vert}\)
\(\newcommand{\norm}[1]{\left\vert\left\vert#1\right\vert\right\vert}\)
\(\newcommand{\msr}[1]{m\left(#1\right)}\)
\(\newcommand{\Diff}[3]{Diff_{#1}#2\left(#3\right)}\)
\(\newcommand{\Av}[3]{Av_{#1}#2\left(#3\right)}\)
\(\newcommand{\met}[1]{\rho\LP#1\RP}\)
\(\newcommand{\ball}[2]{B_{#1}\left(#2\right)}\)
\(\newcommand{\cball}[2]{\overline{B}_{#1}\left(#2\right)}\)
\(\newcommand{\opn}{\mathcal{O}}\)
\(\newcommand{\diam}{\operatorname{diam}}\)
\(\newcommand{\ext}{\operatorname{ext}}\)
\(\newcommand{\inter}{\operatorname{int}}\)
\(\newcommand{\bd}{\operatorname{bd}}\)
\(\renewcommand{\bar}[1]{\overline{#1}}\)
</div>
"""
def_model = genanki.Model(
  1607392319,
  'Math model',
  fields=[
    {'name': 'Name'},
    {'name': 'Defintion'},
  ],
  templates=[
    {
      'name': 'Defintion',
      'qfmt': preamble+"{{Name}}",
      'afmt': preamble+"<p>{{FrontSide}}</p><hr id=\"answer\"><br><br><p>{{Defintion}}</p>",
    },
  ])

def_deck = genanki.Deck(
  2059400110,
  'prepsheet')
def_deck.add_model(def_model)


reg = r"\\boxset\{(.*?)\}\n\{([\w\W]*?)\}\n"

with open(cwd / "prepsheet.tex") as file:

  data = file.read()

  finds = re.findall( reg, data)
  for find in finds:
    name = html.escape(re.sub(r"\$(.*?)\$",r"\(\1\)",find[0]))
    defintion = html.escape(re.sub(r"\$(.*?)\$",r"\(\1\)",find[1]))
    my_note = genanki.Note(
              model=def_model,
              fields=[name, defintion],
              guid=f"{cwd.name}-prepsheet.tex-{name}",
              tags=["prepsheet",cwd.name]
              )
    def_deck.add_note(my_note)
  genanki.Package(def_deck).write_to_file(f"{cwd.name}_prepsheet.apkg")