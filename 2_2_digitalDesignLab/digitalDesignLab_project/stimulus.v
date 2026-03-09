`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/11/27 18:12:50
// Design Name: 
// Module Name: stimulus
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

module stimulus();
    reg CLK, nRST, ENCDEC, START;
    reg [127:0] KEY, TEXTIN;
    wire DONE;
    wire [127:0] TEXTOUT;
    AES_128 aes(.DONE(DONE), .TEXTOUT(TEXTOUT), .CLK(CLK), .nRST(nRST), .ENCDEC(ENCDEC), .START(START), .KEY(KEY), .TEXTIN(TEXTIN));
    
    initial
    begin
        //ENC
        CLK = 0; ENCDEC = 0; nRST = 0; START = 0;
        @(negedge CLK);
        nRST = 1;
        @(negedge CLK);
        ENCDEC = 1; START = 1; TEXTIN = 128'h328831e0435a3137f6309807a88da234; KEY = 128'h2b28ab097eaef7cf15d2154f16a6883c;
        @(negedge CLK);
        TEXTIN = 128'hX; KEY = 128'hx; ENCDEC = 0; START = 0;
        
        //DEC
        #500 ENCDEC = 0; nRST = 0; START = 0;
        @(negedge CLK);
        nRST = 1;
        @(negedge CLK);
        ENCDEC = 0; START = 1; TEXTIN = 128'h3902dc1925dc116a8409850b1dfb9732; KEY = 128'h2b28ab097eaef7cf15d2154f16a6883c;
        @(negedge CLK);
        TEXTIN = 128'hX; KEY = 128'hx; ENCDEC = 0; START = 0;
        
        #650 $stop;
    end
    always
    begin
        #20 CLK = ~CLK;
    end
endmodule
