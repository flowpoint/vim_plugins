# nvim autocomplete plugin in <100 loc python

only contains the boilerplate  so it llm inference can be easily added/customized
the actual llm completions can be freely added as a simple python function

it uses pynvim, neovims buildin menuone/popupmenu, completefunc, and preview window

test it out locally:

```
python -m venv venv
source venv/bin/activate
pip install pynvim
```

start vim with the local plugin (avoids installing)

```
nvim -u ./vimrc2
```

the plugin itself sets the completefunc on vim start (bufenter)

you might need to run:

UpdateRemotePlugins to update the plugin

tips: you can use :pc to close the preview window
