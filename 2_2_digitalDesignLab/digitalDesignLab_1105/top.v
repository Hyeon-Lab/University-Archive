`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/11/05 11:23:11
// Design Name: 
// Module Name: top
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module top;
reg clk, nrst, x;
wire y;

sequenceDetector sd(.Y(y), .CLK(clk), .nRST(nrst), .X(x));

initial
begin
    clk = 1'b0;
    forever #5 clk = ~clk;
end

initial
begin
    nrst = 1'b0;
    #20 nrst = ~nrst;
end

initial
begin
    x = 1'b0;
    #40 x = ~x;
    #30 x = ~x;
    #20 x = ~x;
    #10 x = ~x;
    #20 x = ~x;
    #40 x = ~x;
    #30 $stop;
end
endmodule