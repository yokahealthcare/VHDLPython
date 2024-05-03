#https://github.com/leonbeier/MyHDL
from myhdl import *

@block
def Python_Example(clk_i, led_o):

    cnt = Signal(intbv(0, 0, 6000000))
    tgl = Signal(bool(0))

    @always_seq(clk_i.posedge, reset=None)
    def counter():
        if cnt == cnt.max-1:
            tgl.next = ~tgl
            led_o.next = tgl
            cnt.next = 0
        else:
            cnt.next = cnt + 1

    return counter

clk_i = Signal(bool(0))
led_o = Signal(bool(0))
top = Python_Example(clk_i, led_o)
top.convert(hdl='VHDL')