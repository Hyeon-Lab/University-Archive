`timescale 1ns / 1ps

module top;

wire y_out;
reg x_in, clk, nrst;

finite_state_machine fsm(.Y_OUT(y_out), .X_IN(x_in), .CLK(clk), .nRST(nrst));

initial
begin
    clk = 1'b0;
    forever #5 clk = ~clk;
end

initial
begin
    nrst = 1'b0;
    #20 nrst = 1'b1;
end

initial
begin
    x_in = 1'b0;
    #40 x_in = 1'b1;
    #100 x_in = 1'b0;
    #50 x_in = 1'b1;
    #10 x_in = 1'b0;
    #80 $stop;
end
endmodule
