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

  RM_IHPSG13_1P_1024x8_c2_bm_bist sram (
      .A_CLK(clk),
      .A_MEN(rst_n),
      .A_WEN(ui_in[7] && !bank_select),
      .A_REN(~ui_in[7]),
      .A_ADDR(addr),
      .A_DIN(uio_in),
      .A_DLY(1'b1),
      .A_DOUT(uo_out),
      .A_BM(8'b11111111),
      .A_BIST_CLK(1'b0),
      .A_BIST_EN(1'b0),
      .A_BIST_MEN(1'b0),
      .A_BIST_WEN(1'b0),
      .A_BIST_REN(1'b0),
      .A_BIST_ADDR(10'b0),
      .A_BIST_DIN(8'b0),
      .A_BIST_BM(8'b0)
  );

endmodule
