import pynvim
from transformers import AutoModelForCausalLM, AutoTokenizer
model, tokenizer = None, None

def infer_qwen(prompt, max_new_tokens=512):
    # lazy load model, tokenizer
    global model, tokenizer
    model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype="auto", device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    messages = [
        {"role": "system", "content": "You are a helpful code-assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs, max_new_tokens=max_new_tokens
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

def suggest(prompt: str, current_buffer: str, curpos) -> list[str]:
    ''' takes a prompt and suggests a list of completions '''
    # example: just follow instruction on the current line or do so with previous lines as context
    context = '\n'.join(current_buffer[:curpos[0]])
    completion_fns = [infer_qwen, lambda x: infer_qwen(f'context: {context}\ninstruction: {prompt}')]
    completions = [fn(prompt) for fn in completion_fns]
    return completions


def format_completion(prompt, completion, curpos):
    lineno, colno = curpos
    return {'word': prompt + ' ' + completion.split('\n')[0], 
             'info': prompt + ' ' + completion,
              'kind':'f',
              'user_data': (curpos, completion),
              }

@pynvim.plugin
class CompletePlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.function('FlowComplete', sync=True)
    def get_completion(self, args):
        findstart = args[0]
        base = args[1]
        win = self.nvim.current.window
        curpos = win.cursor

        # start completion at beginning of line (see neovim docs)
        if findstart == 1:
            return 0
        else:
            return [format_completion(base, x, curpos) for x in suggest(base, self.nvim.current.buffer, curpos)]

    @pynvim.function('FlowCompleteInsert', sync=True)
    def insert_completions(self, args):
        info = self.nvim.eval('complete_info()')
        completed_item = self.nvim.eval('v:completed_item')

        # completion aborted
        if completed_item == {}:
            return 1

        buf = self.nvim.current.buffer
        completions = info['items']
        selected = int(info['selected'])
        actual_completion = completions[selected]
        curpos, res = actual_completion['user_data']
        curline, curcol = curpos
        reslines = res.split('\n')[1:]

        for offset,resline in enumerate(reslines):
            blen = len(buf)
            nl = curline+offset
            if nl >= blen:
                buf.append(str(resline))
            else:
                oldrest = buf[nl:]
                buf[nl] = str(resline)
                buf[nl+1:] = oldrest
        return 1

    # this can be used to set the commpletion for python files only, alternative to a normal vim config
    #@pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    #def on_bufenter(self, filename):
        #self.nvim.command("set completefunc=FlowComplete")
        #self.nvim.command('autocmd! CompleteDonePre * call FlowCompleteInsert()')
        # auto-close the preview window after inserting
        #self.nvim.command('autocmd! CompleteDone * silent! pclose!')
