# SPDX-FileCopyrightText: © 2024 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

BANKSEL = 1 << 6
WE = 1 << 7

@cocotb.test()
async def test_sram(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("ena")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    dut._log.info("reset")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 2)

    # All the bidirectional ports are used for the din signal, so they should be inputs
    assert int(dut.uio_oe.value) == 0

    dut._log.info("write 4 bytes to addresses 8, 9, 10, 11")
    dut.ui_in.value = WE | 8
    dut.uio_in.value = 0x55
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 9
    dut.uio_in.value = 0x66
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 10
    dut.uio_in.value = 0x77
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 11
    dut.uio_in.value = 0x88
    await ClockCycles(dut.clk, 1)

    dut._log.info("read back the bytes and verify they are correct")
    dut.ui_in.value = 8
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x55

    dut.ui_in.value = 9
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x66

    dut.ui_in.value = 10
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x77

    dut.ui_in.value = 11
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x88

    dut._log.info("write a byte at address 12")
    dut.ui_in.value = WE | 12 
    dut.uio_in.value = 0x99
    await ClockCycles(dut.clk, 1)

    dut._log.info("overwrite the byte at address 10")
    dut.ui_in.value = WE | 10
    dut.uio_in.value = 0xaa
    await ClockCycles(dut.clk, 1)

    dut._log.info("read back the bytes and verify they are correct")
    dut.ui_in.value = 12
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x99

    dut.ui_in.value = 10
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xaa

    dut.ui_in.value = 8
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0x55

    dut._log.info("Switch to bank 3 and write a byte at addresses 10, 11")
    dut.ui_in.value = BANKSEL
    dut.uio_in.value = 3
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 10
    dut.uio_in.value = 0xbb
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 11
    dut.uio_in.value = 0xcc
    await ClockCycles(dut.clk, 1)

    dut._log.info("read back the bytes and verify they are correct")
    dut.ui_in.value = 10
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xbb

    dut._log.info("Switch to bank 8 and write a byte at addresses 10, 11")
    dut.ui_in = BANKSEL
    dut.uio_in.value = 8
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 10
    dut.uio_in.value = 0x10
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = WE | 11
    dut.uio_in.value = 0x11
    await ClockCycles(dut.clk, 1)

    dut._log.info("Switch to bank 0 and verify the byte at address 10 is still correct")
    dut.ui_in.value = BANKSEL
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 1)

    dut.ui_in.value = 10
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xaa

    dut._log.info("Bank select and read back the byte at addresses 11, 10")
    dut.ui_in.value = BANKSEL | 11
    dut.uio_in.value = 3
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xcc

    dut.ui_in.value = 10
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xbb

    dut._log.info("Chaning the bank while bank_sel is high and verify the data")

    dut.ui_in.value = BANKSEL | 10
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xaa

    dut.uio_in.value = 3
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xbb

    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 2)
    assert int(dut.uo_out.value) == 0xaa

    dut._log.info("all good!")
