<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This is a 1 kbyte SRAM controller module. It allows reading or writing a single byte at a time. 

There are 10 address lines, 8 data lines, and 1 write enable line. 

To read a byte, set the write enable line (wen) to 0, and the data lines (dout[7:0]) will be set to the value of the byte at the address specified by the address lines (addr[5:0]).

To write a byte, set the write enable line (wen) to 1, and set the data lines (din[7:0]) to the desired value. Writing is only possible
when the bank_sel line is 0.

The lower 6 address bits (addr[5:0]) are exposed as input pins. 

The upper 4 address lines are stored in the address_bank register. To change the upper address bits, set the bank_sel line to 1, and set the data lines (addr[9:6] / uio[3:0]) to the desired value.

## How to test

1. Set addr[5:0] to the desired address, set din[7:0] to the desired value, set wen to 1, and set bank_sel to 0, then pulse the clock line. The value at the specified address should be updated to the value of din[7:0].
2. Set addr[5:0] to the desired address, set wen to 0, and set bank_sel to 0, then pulse the clock line. The value at the specified address should be output on dout[7:0].
3. Set addr[9:6] to the desired value, set bank_sel to 1, then pulse the clock line. The upper address bits should be updated to the value of addr[9:6].

## External hardware

None
