module RM_IHPSG13_1P_1024x8_c2_bm_bist (
    input A_CLK,
    input A_MEN,
    input A_WEN,
    input A_REN,
    input [9:0] A_ADDR,
    input [7:0] A_DIN,
    input A_DLY,
    output [7:0] A_DOUT,
    input [7:0] A_BM,
    input A_BIST_CLK,
    input A_BIST_EN,
    input A_BIST_MEN,
    input A_BIST_WEN,
    input A_BIST_REN,
    input [9:0] A_BIST_ADDR,
    input [7:0] A_BIST_DIN,
    input [7:0] A_BIST_BM
);

endmodule
