import pynvim

try:
    # import you llm backends here
    pass
except ImportError:
    pass


def suggest(prompt: str) -> list[str]:
    ''' takes a prompt and suggests a list of completions '''
    # call your llm backend here
    max_length=300
    system_prompt = 'Complete the code:'
    prompt = f'{system_prompt} {prompt}'
    completions = ['example_completion0', 'example_completion1', 
                   'big completion'+'\nline'*20]
    return completions


def format_completion(prompt, completion, curpos):
    lineno, colno = curpos
    return {'word': prompt + ' ' + completion.split('\n')[0], 
             'info': prompt + ' ' + completion,
              'kind':'f',
              'user_data': (curpos, completion),
              }

@pynvim.plugin
class TestPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim
        loop = nvim.loop

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
            return [format_completion(base, x, curpos) for x in suggest(base)]

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

    @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        self.nvim.command("set completefunc=FlowComplete")
        self.nvim.command('autocmd! CompleteDonePre * call FlowCompleteInsert()')
        # close the preview window after inserting
        self.nvim.command('autocmd! CompleteDone * silent! pclose!')
        #self.nvim.command('set completeopt="menuone,preview')
