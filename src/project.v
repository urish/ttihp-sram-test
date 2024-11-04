/*
 * Copyright (c) 2024 Uri Shkaed
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_urish_sram_test (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  assign uio_oe = 8'b0;  // All bidirectional IOs are inputs
  assign uio_out = 8'b0;

  wire       wen = ui_in[7];
  wire       bank_select = ui_in[6];
  wire [5:0] addr_low = ui_in[5:0];
  reg  [3:0] addr_high_reg;
  wire [3:0] addr_high_in = uio_in[3:0];
  wire [9:0] addr = {bank_select ? addr_high_in : addr_high_reg, addr_low};

  always @(posedge clk) begin
    if (~rst_n) begin
      addr_high_reg <= 0;
    end else begin
      if (bank_select) begin
        addr_high_reg <= addr_high_in;
      end
    end
  end

  assign uo_out = 0;

endmodule
