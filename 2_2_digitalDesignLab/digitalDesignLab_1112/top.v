`timescale 1ns / 1ps

module top;

wire [1:0] MAIN_SIG, CNTRY_SIG;
reg CAR_ON_CNTRY_RD;
reg CLOCK, CLEAR;
reg [2:0] y2r, r2g;

traffic_signal_controller tsc(.hwy(MAIN_SIG), .cntry(CNTRY_SIG), .X(CAR_ON_CNTRY_RD), .clock(CLOCK), .clear(CLEAR), .y2rdelay(y2r), .r2gdelay(r2g));

initial
begin
    y2r = 3'd3;
    r2g = 3'd2;
    CLOCK = 1'b0;
    forever #5 CLOCK = ~CLOCK;
end

initial
begin
    CLEAR = 1'b1;
    repeat (5) @(negedge CLOCK);
    CLEAR = 1'b0;
end

initial
begin
    CAR_ON_CNTRY_RD = 1'b0;
    
    repeat (20) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b1;
    repeat (10) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b0;
    
    repeat (20) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b1;
    repeat (10) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b0;
    
    repeat (20) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b1;
    repeat (10) @(negedge CLOCK); CAR_ON_CNTRY_RD = 1'b0;
    
    repeat (10) @(negedge CLOCK); $stop;
end
endmodule
