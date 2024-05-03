from myhdl import *


# @block
# def Clock():
#     @instance
#     def drive_clk():
#         while True:
#             clk.next = not clk
#             yield delay(10)  # nanosecond


@block
def Memory(dout, din, addr, clk, we=True, depth=128):
    mem = [Signal(intbv(0)[16:]) for i in range(depth)]  # list of 128 rows of RAM (default: 0000000000000000)

    # clk = Signal(bool(0))
    # @instance
    # def drive_clk():
    #     while True:
    #         clk.next = not clk
    #         yield delay(10)


    @always(clk.posedge)
    def write():
        if we:
            mem[int(addr)].next = din

    @always_comb
    def read():
        dout.next = mem[int(addr)]

    return write, read



@block
def Buffer(data_in, data_out, wr_clk, wr_en=True, buffer_depth=8, data_width=8, block_width=2):
  """
  This module implements a simple write buffer with the following ports:

  - data_in: Input data signal (data_width bits)
  - data_out: Output data signal (data_width bits)
  - wr_clk: Write clock signal
  - wr_en: Write enable signal (active high)
  - buffer_depth: Depth of the write buffer (default: 16)
  - data_width: Width of the data signal (default: 8 bits)
  """

  index_width = buffer_depth.bit_length()
  tag_width = index_width
  # Internal memory (16 bit)
  mem = [Signal(intbv(0)[index_width + tag_width + block_width + data_width:]) for i in range(buffer_depth)]


  # Head and tail pointers
  head = Signal(intbv(0)[buffer_depth.bit_length():])
  tail = Signal(intbv(0)[buffer_depth.bit_length():])

  # Define output signals
  full = Signal(bool(0))
  empty = Signal(bool(0))

  # Write process
  @always(wr_clk.posedge)
  def write_process():
    if wr_en:
      mem[head].next = data_in
      head.next = (head + 1) % buffer_depth

  # Read process (always_comb for continuous output)
  @always_comb
  def read_process():
    if head != tail:
      data_out.next = mem[tail]
    else:
      data_out.next = 0  # Set output to 0 if buffer is empty

  # Full flag (always_comb for continuous output)
  @always_comb
  def full_flag():
    full.next = (head + 1) % buffer_depth == tail

  # Empty flag (always_comb for continuous output)
  @always_comb
  def empty_flag():
    empty.next = head == tail

  return write_process, read_process, full_flag, empty_flag



@block
def WriteBuffer():
    clk = Signal(bool(0))

    @instance
    def drive_clk():
        while True:
            clk.next = not clk
            yield delay(10)  # nanosecond
            

    dout = Signal(intbv(0)[16:])
    din = Signal(intbv(500)[16:])
    write_address = 2

    memory = Memory(dout, din, write_address, clk)

    # Write buffer
    data_in = Signal(intbv(0)[16:])
    data_out = Signal(intbv(0)[16:])

    buffer = Buffer(data_in, data_out, clk)

    return drive_clk, buffer, memory

inst = WriteBuffer()
inst.convert(hdl="VHDL")


# def convert(hdl):
#     clk = Clock()

#     dout = Signal(intbv(0)[16:])
#     din = Signal(intbv(500)[16:])
#     read_address = 2

#     memory = Memory(dout, din, read_address, clk)

#     memory.convert(hdl=hdl)

# convert(hdl="VHDL")