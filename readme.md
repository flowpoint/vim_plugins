# nvim autocomplete python plugin in <100 loc

only contains the boilerplate  so llm inference can be easily added/customized

the actual llm completions can be freely added with a simple python function

it uses pynvim, neovims builtin menuone/popupmenu, completefunc, and preview window

### test it out locally:

```
python -m venv venv
source venv/bin/activate
pip install pynvim
```

start vim with the local plugin (avoids installing)

```
nvim -u ./dev_vimrc
```

### usage

get line completions with "ctrl-x ctrl-u"

choose completion with ctrx-n ctrx-p and enter

you can use `:pc` to close the preview window

### notes:

the plugin itself sets the completefunc on vim start (bufenter)

you might need to run:

`UpdateRemotePlugins` to update the plugin

the completion is atm activated for .py files, see the autocmd pattern for bufenter
