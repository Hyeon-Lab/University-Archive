`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/11/05 11:22:17
// Design Name: 
// Module Name: sequenceDetector
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


module sequenceDetector(Y, CLK, nRST, X);
input CLK, nRST, X;
output Y;
reg Y;

parameter S0 = 3'd0, S1 = 3'd1, S2 = 3'd2, S3 = 3'd3;
reg [1:0] state;
reg [1:0] nextstate;

always @(posedge CLK, negedge nRST)
    if(!nRST)
        state <= S0;
    else
        state <= nextstate;

always @(state)
begin
    case(state)
        S0: Y=0;
        S1: Y=0;
        S2: Y=0;
        S3: Y=1;
    endcase
end

always @(state, X)
begin
    case(state)
        S0: if(X)
                nextstate = S1;
            else
                nextstate = S0;
        S1: if(X)
                nextstate = S2;
            else
                nextstate = S0;
        S2: if(X)
                nextstate = S3;
            else
                nextstate = S0;
        S3: if(X)
                nextstate = S3;
            else
                nextstate = S0;
        default: nextstate = S0;
    endcase
end

endmodule
