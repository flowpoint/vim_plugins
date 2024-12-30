# llm nvim autocomplete python plugin in <100 loc

a minimal llm autocomplete plugin with pynvim and qwen2.5-coder-0.5B-instruct

* its entirely offline and local, after setup
* its slow, but usable even on cpu. 
* fully open source, since qwen is apache-2
* very hackable 

it uses pynvim, neovims builtin menuone/popupmenu, completefunc, and preview window

many more optimizations are possible (speed, quality, ..., fewer dependencies)

### setup

it requires python and the following packages

```
pip install pynvim torch transformers accelerate
```

the qwen model needs to be in huggingface-cache

it will be autodownloaded, but its recommended to manually cache it:

```
python -c 'from transformers import AutoModelForCausalLM; \
    model = AutoModelForCausalLM.from_pretrained( \
    "Qwen/Qwen2.5-Coder-0.5B-Instruct", \
        torch_dtype="auto", device_map="auto")'
```

then, try it out with the example-vimrc

```
nvim -u ./example_vimrc example.py
```

then, run `:UpdateRemotePlugins` in nvim

to install, copy the plugin to your nvim runtimepath (`:set runtimepath`)

```
cp -r rplugin ~/.config/nvim/
```

and the example_vimrc variables to your vimrc

and run `:UpdateRemotePlugins` again

the `UpdateRemotePlugins` command has to be run whenever the remote plugins change, see https://neovim.io/doc/user/remote_plugin.html#%3AUpdateRemotePlugins


### usage hints

get line completions with "ctrl-x_ctrl-u"

choose completion with ctrl-n ctrl-p and enter

cancel completion with ctrl-e

you can use `:pc` to close the preview window
