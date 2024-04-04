import pynvim

from inference_api.router import call_infer

#set omnifunc=Ofu1 ctrl-x ctrl-o
# or
#set completefunc=Ofu1 ctrl-x ctrl-u

def inf(prompt):
    max_length=200
    system_prompt = 'only answer with succinct code. '
    prompt += system_prompt
    
    model_name = 'mistralai/Mistral-7B-Instruct-v0.2'
    res, control, debuginfo  = call_infer(prompt, max_length, model_name)
    result = res.get(timeout=299)
    return result['result']

def suggest(prompt):
    if prompt.strip().endswith('hello'):
        return ' world'
    else:
        return None

@pynvim.plugin
class TestPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    # then set omnifunc=Ofu1
    @pynvim.function('Ofu1', sync=True)
    def testfunction(self, args):
        findstart = args[0]
        base = args[1]
        win = self.nvim.current.window
        buf = self.nvim.current.buffer
        curpos = win.cursor
        l = self.nvim.current.line

        if findstart == 1:
            return 0
        else:
            #return list(base.split(' '))
            res = inf(base)
            lineno, colno = curpos
            #buf[lineno+2] =  res
            #return [base + ' ' + res, 'test']
            compldict1 = {'word': base + ' ' + res.split('\n')[0], 
                          'menu':"menutext", 
                          'kind':'f',
                          'user_data': (curpos, res),
                          }
            compldict2 = {'word': base}
            return [compldict1, compldict2]

    #nvim.subscribe

    #@pynvim.command('TestCommand', nargs='*', range='')
    @pynvim.function('TestFn', sync=True)
    #def testcommand(self, args, range):
    def testfunction2(self, args):
        '''
        self.nvim.current.line = ('Command with args: {}, range: {}'
                                  .format(args, range))
        '''
        info = self.nvim.eval('complete_info()')
        buf = self.nvim.current.buffer

        completions = info['items']
        selected = int(info['selected'])

        actual_completion = completions[selected]
        da = actual_completion['user_data']
        curpos, res = da
        curline, curcol = curpos
        '''
        {'pum_visible': 1, 'mode': 'function', 'selected': 0, 
        'items': [
        {'word': "hello I'm an AI language model and don't have the ability to write or execute code directly. However,", 'menu': 'menutext', 'user_data': [[5, 0], "I'm an AI language model and don't have the ability to write or execute code directly. However,"], 'info': '', 'kind': 'f', 'abbr': ''}, 
        {'word': 'hello', 'menu': '', 'user_data': '', 'info': '', 'kind': '', 'abbr': ''}]}
        '''

        reslines = res.split('\n')[1:]

        for offset,resline in enumerate(reslines):
            blen = len(buf)
            nl = curline+offset
            if nl >= blen:
                buf.append(str(resline))
            else:
                buf[curline+offset] = str(resline)
        #buf[3] = str(args)
        #print(args)
        #buf[
        return 1

    '''
    @pynvim.command('TestComplete', pattern='*.py', eval='expand("<afile>")', sync=True)
    def testcomplete(self, args, range):
        #self.nvim.current.line = (.format(args, range))
        pass
    '''
        
    #@pynvim.autocmd('TestComplete2', pattern='CursorMovedI', eval='expand("<afile>")',sync=True)
    #@pynvim.autocmd('CursorMovedI', pattern='*.py', eval='expand("<afile>")', sync=True)
    #@pynvim.autocmd('CursorMovedI', pattern='*.py', eval='nvim_win', sync=True)
    def testcomplete2(self, args):
        #self.nvim.out_write('testcomplete is in')
        #self.nvim.out_write(f'args: {args}')
        print(args)
        win = self.nvim.current.window
        buf = self.nvim.current.buffer

        # line, col
        curpos = win.cursor
        l = self.nvim.current.line
        s = suggest(l)
        #s = str(args)
        src = self.nvim.new_highlight_source()
        if s is not None:
            #for li in range(
            # group, line, colstart, colend
            self.nvim.current.line = l + s
            buf.add_highlight("String", curpos[0]-1, curpos[1], curpos[1] + len(s), src_id=src)
        #self.nvim.out_write(f'args: {

    @pynvim.autocmd('BufEnter', pattern='*.py', eval='expand("<afile>")', sync=True)
    def on_bufenter(self, filename):
        self.nvim.out_write('testplugin is in ' + filename + '\n')
        self.nvim.command("set completefunc=Ofu1")
        #self.nvim.command('autocmd! CompleteDonePre * TestCommand')
        #self.nvim.command('autocmd! CompleteDonePre * TestCommand')
        self.nvim.command('autocmd! CompleteDonePre * call TestFn()')
        #self.nvim.command('autocmd! CompleteChanged * TestCommand')
