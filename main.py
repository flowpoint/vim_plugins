from pynvim import attach
#nvim = attach('socket', path='127.0.0.1:6666')
nvim = attach('socket', path='/tmp/nvim2')

a = nvim.exec_lua("""
events = {}
vim.api.nvim_buf_attach(0, false, {
  on_lines = function(...)
    table.insert(events, {...})
  end,
})
""")

nvim.exec_lua("""
   local a = vim.api
   local function add(a,b)
       return a+b
   end

   local function buffer_ticks()
      local ticks = {}
      for _, buf in ipairs(a.nvim_list_bufs()) do
          ticks[#ticks+1] = a.nvim_buf_get_changedtick(buf)
      end
      return ticks
   end

    events = {}
    vim.api.nvim_buf_attach(0, false, {
      on_lines = function(...)
        table.insert(events, {...})
      end,
    })

    local function penv()
    return events
    end

   _testplugin = {add=add, buffer_ticks=buffer_ticks, penv=penv}
""")

b = nvim.exec_lua("""
          print(events)
          """)

mod = nvim.lua._testplugin

# get buffer events:
"""
table = mod.penv()
for linechange in table:
    "lines", buffer_handle, changedtick, first_line_change, last_line_change, last_line_in_update_range, byte_count_of_pref_contents
"""

while 1:
    try:
        buf = nvim.current.buffer
        leng = buf.api.line_count()-1
        ctext = []
        for r in range(min(leng,1000)):
            t = buf[r]
            ctext.append(t)

        if r < 50:
            buf.append([])
            buf.append(t)

        buf[-1] = t

        print(ctext)
    except KeyboardInterrupt:
        break

