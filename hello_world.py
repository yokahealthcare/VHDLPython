from myhdl import *

@block
def HelloWorld():

    clk = Signal(bool(0))

    @instance
    def drive_clk():
        while True:
            clk.next = not clk
            yield delay(10)



    @always(clk.posedge)
    def say_hello():
        print("Hello World!")

    return drive_clk, say_hello



inst = HelloWorld()
inst.convert(hdl="VHDL")
# inst.run_sim(50)