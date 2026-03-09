`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/11/27 18:12:25
// Design Name: 
// Module Name: AES_128
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

module AES_128 (DONE, TEXTOUT, CLK, nRST, ENCDEC, START, KEY, TEXTIN);
    input CLK, nRST, ENCDEC, START;
    input [127:0] KEY, TEXTIN;
    output DONE;
    output [127:0] TEXTOUT;
    
    wire nRST, ENCDEC, START;
    wire [127:0] KEY, TEXTIN;
    reg DONE;
    reg [127:0] TEXTOUT;
    
    reg enc;                          //store ENCDEC
    reg [127:0] key;                  //store KEY
    reg [127:0] text;                 //store TEXTIN
    reg [127:0] state;                // Current AES state
    reg [127:0] round_key;            // Current round key
    reg [3:0] round_counter;          // Round counter (0-10)
    reg [1:0] current_state, next_state;

    // FSM States
    reg[3:0] IDLE  = 2'b00;
    reg[3:0] ROUND = 2'b01;
    reg[3:0] FINAL = 2'b10;

    // S-Box
    reg [7:0] SBox [0:255];
    initial
    begin
        SBox[8'h00] = 8'h63; SBox[8'h01] = 8'h7c; SBox[8'h02] = 8'h77; SBox[8'h03] = 8'h7b; SBox[8'h04] = 8'hf2; SBox[8'h05] = 8'h6b; SBox[8'h06] = 8'h6f; SBox[8'h07] = 8'hc5;
        SBox[8'h08] = 8'h30; SBox[8'h09] = 8'h01; SBox[8'h0a] = 8'h67; SBox[8'h0b] = 8'h2b; SBox[8'h0c] = 8'hfe; SBox[8'h0d] = 8'hd7; SBox[8'h0e] = 8'hab; SBox[8'h0f] = 8'h76;
        SBox[8'h10] = 8'hca; SBox[8'h11] = 8'h82; SBox[8'h12] = 8'hc9; SBox[8'h13] = 8'h7d; SBox[8'h14] = 8'hfa; SBox[8'h15] = 8'h59; SBox[8'h16] = 8'h47; SBox[8'h17] = 8'hf0;
        SBox[8'h18] = 8'had; SBox[8'h19] = 8'hd4; SBox[8'h1a] = 8'ha2; SBox[8'h1b] = 8'haf; SBox[8'h1c] = 8'h9c; SBox[8'h1d] = 8'ha4; SBox[8'h1e] = 8'h72; SBox[8'h1f] = 8'hc0;
        SBox[8'h20] = 8'hb7; SBox[8'h21] = 8'hfd; SBox[8'h22] = 8'h93; SBox[8'h23] = 8'h26; SBox[8'h24] = 8'h36; SBox[8'h25] = 8'h3f; SBox[8'h26] = 8'hf7; SBox[8'h27] = 8'hcc;
        SBox[8'h28] = 8'h34; SBox[8'h29] = 8'ha5; SBox[8'h2a] = 8'he5; SBox[8'h2b] = 8'hf1; SBox[8'h2c] = 8'h71; SBox[8'h2d] = 8'hd8; SBox[8'h2e] = 8'h31; SBox[8'h2f] = 8'h15;
        SBox[8'h30] = 8'h04; SBox[8'h31] = 8'hc7; SBox[8'h32] = 8'h23; SBox[8'h33] = 8'hc3; SBox[8'h34] = 8'h18; SBox[8'h35] = 8'h96; SBox[8'h36] = 8'h05; SBox[8'h37] = 8'h9a;
        SBox[8'h38] = 8'h07; SBox[8'h39] = 8'h12; SBox[8'h3a] = 8'h80; SBox[8'h3b] = 8'he2; SBox[8'h3c] = 8'heb; SBox[8'h3d] = 8'h27; SBox[8'h3e] = 8'hb2; SBox[8'h3f] = 8'h75;
        SBox[8'h40] = 8'h09; SBox[8'h41] = 8'h83; SBox[8'h42] = 8'h2c; SBox[8'h43] = 8'h1a; SBox[8'h44] = 8'h1b; SBox[8'h45] = 8'h6e; SBox[8'h46] = 8'h5a; SBox[8'h47] = 8'ha0;
        SBox[8'h48] = 8'h52; SBox[8'h49] = 8'h3b; SBox[8'h4a] = 8'hd6; SBox[8'h4b] = 8'hb3; SBox[8'h4c] = 8'h29; SBox[8'h4d] = 8'he3; SBox[8'h4e] = 8'h2f; SBox[8'h4f] = 8'h84;
        SBox[8'h50] = 8'h53; SBox[8'h51] = 8'hd1; SBox[8'h52] = 8'h00; SBox[8'h53] = 8'hed; SBox[8'h54] = 8'h20; SBox[8'h55] = 8'hfc; SBox[8'h56] = 8'hb1; SBox[8'h57] = 8'h5b;
        SBox[8'h58] = 8'h6a; SBox[8'h59] = 8'hcb; SBox[8'h5a] = 8'hbe; SBox[8'h5b] = 8'h39; SBox[8'h5c] = 8'h4a; SBox[8'h5d] = 8'h4c; SBox[8'h5e] = 8'h58; SBox[8'h5f] = 8'hcf;
        SBox[8'h60] = 8'hd0; SBox[8'h61] = 8'hef; SBox[8'h62] = 8'haa; SBox[8'h63] = 8'hfb; SBox[8'h64] = 8'h43; SBox[8'h65] = 8'h4d; SBox[8'h66] = 8'h33; SBox[8'h67] = 8'h85;
        SBox[8'h68] = 8'h45; SBox[8'h69] = 8'hf9; SBox[8'h6a] = 8'h02; SBox[8'h6b] = 8'h7f; SBox[8'h6c] = 8'h50; SBox[8'h6d] = 8'h3c; SBox[8'h6e] = 8'h9f; SBox[8'h6f] = 8'ha8;
        SBox[8'h70] = 8'h51; SBox[8'h71] = 8'ha3; SBox[8'h72] = 8'h40; SBox[8'h73] = 8'h8f; SBox[8'h74] = 8'h92; SBox[8'h75] = 8'h9d; SBox[8'h76] = 8'h38; SBox[8'h77] = 8'hf5;
        SBox[8'h78] = 8'hbc; SBox[8'h79] = 8'hb6; SBox[8'h7a] = 8'hda; SBox[8'h7b] = 8'h21; SBox[8'h7c] = 8'h10; SBox[8'h7d] = 8'hff; SBox[8'h7e] = 8'hf3; SBox[8'h7f] = 8'hd2;
        SBox[8'h80] = 8'hcd; SBox[8'h81] = 8'h0c; SBox[8'h82] = 8'h13; SBox[8'h83] = 8'hec; SBox[8'h84] = 8'h5f; SBox[8'h85] = 8'h97; SBox[8'h86] = 8'h44; SBox[8'h87] = 8'h17;
        SBox[8'h88] = 8'hc4; SBox[8'h89] = 8'ha7; SBox[8'h8a] = 8'h7e; SBox[8'h8b] = 8'h3d; SBox[8'h8c] = 8'h64; SBox[8'h8d] = 8'h5d; SBox[8'h8e] = 8'h19; SBox[8'h8f] = 8'h73;
        SBox[8'h90] = 8'h60; SBox[8'h91] = 8'h81; SBox[8'h92] = 8'h4f; SBox[8'h93] = 8'hdc; SBox[8'h94] = 8'h22; SBox[8'h95] = 8'h2a; SBox[8'h96] = 8'h90; SBox[8'h97] = 8'h88;
        SBox[8'h98] = 8'h46; SBox[8'h99] = 8'hee; SBox[8'h9a] = 8'hb8; SBox[8'h9b] = 8'h14; SBox[8'h9c] = 8'hde; SBox[8'h9d] = 8'h5e; SBox[8'h9e] = 8'h0b; SBox[8'h9f] = 8'hdb;
        SBox[8'ha0] = 8'he0; SBox[8'ha1] = 8'h32; SBox[8'ha2] = 8'h3a; SBox[8'ha3] = 8'h0a; SBox[8'ha4] = 8'h49; SBox[8'ha5] = 8'h06; SBox[8'ha6] = 8'h24; SBox[8'ha7] = 8'h5c;
        SBox[8'ha8] = 8'hc2; SBox[8'ha9] = 8'hd3; SBox[8'haa] = 8'hac; SBox[8'hab] = 8'h62; SBox[8'hac] = 8'h91; SBox[8'had] = 8'h95; SBox[8'hae] = 8'he4; SBox[8'haf] = 8'h79;
        SBox[8'hb0] = 8'he7; SBox[8'hb1] = 8'hc8; SBox[8'hb2] = 8'h37; SBox[8'hb3] = 8'h6d; SBox[8'hb4] = 8'h8d; SBox[8'hb5] = 8'hd5; SBox[8'hb6] = 8'h4e; SBox[8'hb7] = 8'ha9;
        SBox[8'hb8] = 8'h6c; SBox[8'hb9] = 8'h56; SBox[8'hba] = 8'hf4; SBox[8'hbb] = 8'hea; SBox[8'hbc] = 8'h65; SBox[8'hbd] = 8'h7a; SBox[8'hbe] = 8'hae; SBox[8'hbf] = 8'h08;
        SBox[8'hc0] = 8'hba; SBox[8'hc1] = 8'h78; SBox[8'hc2] = 8'h25; SBox[8'hc3] = 8'h2e; SBox[8'hc4] = 8'h1c; SBox[8'hc5] = 8'ha6; SBox[8'hc6] = 8'hb4; SBox[8'hc7] = 8'hc6;
        SBox[8'hc8] = 8'he8; SBox[8'hc9] = 8'hdd; SBox[8'hca] = 8'h74; SBox[8'hcb] = 8'h1f; SBox[8'hcc] = 8'h4b; SBox[8'hcd] = 8'hbd; SBox[8'hce] = 8'h8b; SBox[8'hcf] = 8'h8a;
        SBox[8'hd0] = 8'h70; SBox[8'hd1] = 8'h3e; SBox[8'hd2] = 8'hb5; SBox[8'hd3] = 8'h66; SBox[8'hd4] = 8'h48; SBox[8'hd5] = 8'h03; SBox[8'hd6] = 8'hf6; SBox[8'hd7] = 8'h0e;
        SBox[8'hd8] = 8'h61; SBox[8'hd9] = 8'h35; SBox[8'hda] = 8'h57; SBox[8'hdb] = 8'hb9; SBox[8'hdc] = 8'h86; SBox[8'hdd] = 8'hc1; SBox[8'hde] = 8'h1d; SBox[8'hdf] = 8'h9e;
        SBox[8'he0] = 8'he1; SBox[8'he1] = 8'hf8; SBox[8'he2] = 8'h98; SBox[8'he3] = 8'h11; SBox[8'he4] = 8'h69; SBox[8'he5] = 8'hd9; SBox[8'he6] = 8'h8e; SBox[8'he7] = 8'h94;
        SBox[8'he8] = 8'h9b; SBox[8'he9] = 8'h1e; SBox[8'hea] = 8'h87; SBox[8'heb] = 8'he9; SBox[8'hec] = 8'hce; SBox[8'hed] = 8'h55; SBox[8'hee] = 8'h28; SBox[8'hef] = 8'hdf;
        SBox[8'hf0] = 8'h8c; SBox[8'hf1] = 8'ha1; SBox[8'hf2] = 8'h89; SBox[8'hf3] = 8'h0d; SBox[8'hf4] = 8'hbf; SBox[8'hf5] = 8'he6; SBox[8'hf6] = 8'h42; SBox[8'hf7] = 8'h68;
        SBox[8'hf8] = 8'h41; SBox[8'hf9] = 8'h99; SBox[8'hfa] = 8'h2d; SBox[8'hfb] = 8'h0f; SBox[8'hfc] = 8'hb0; SBox[8'hfd] = 8'h54; SBox[8'hfe] = 8'hbb; SBox[8'hff] = 8'h16;
    end

    // Inverse S-Box
    reg [7:0] InvSBox [0:255];
    initial
    begin
        InvSBox[8'h00] = 8'h52; InvSBox[8'h01] = 8'h09; InvSBox[8'h02] = 8'h6a; InvSBox[8'h03] = 8'hd5; InvSBox[8'h04] = 8'h30; InvSBox[8'h05] = 8'h36; InvSBox[8'h06] = 8'ha5; InvSBox[8'h07] = 8'h38;
        InvSBox[8'h08] = 8'hbf; InvSBox[8'h09] = 8'h40; InvSBox[8'h0a] = 8'ha3; InvSBox[8'h0b] = 8'h9e; InvSBox[8'h0c] = 8'h81; InvSBox[8'h0d] = 8'hf3; InvSBox[8'h0e] = 8'hd7; InvSBox[8'h0f] = 8'hfb;
        InvSBox[8'h10] = 8'h7c; InvSBox[8'h11] = 8'he3; InvSBox[8'h12] = 8'h39; InvSBox[8'h13] = 8'h82; InvSBox[8'h14] = 8'h9b; InvSBox[8'h15] = 8'h2f; InvSBox[8'h16] = 8'hff; InvSBox[8'h17] = 8'h87;
        InvSBox[8'h18] = 8'h34; InvSBox[8'h19] = 8'h8e; InvSBox[8'h1a] = 8'h43; InvSBox[8'h1b] = 8'h44; InvSBox[8'h1c] = 8'hc4; InvSBox[8'h1d] = 8'hde; InvSBox[8'h1e] = 8'he9; InvSBox[8'h1f] = 8'hcb;
        InvSBox[8'h20] = 8'h54; InvSBox[8'h21] = 8'h7b; InvSBox[8'h22] = 8'h94; InvSBox[8'h23] = 8'h32; InvSBox[8'h24] = 8'ha6; InvSBox[8'h25] = 8'hc2; InvSBox[8'h26] = 8'h23; InvSBox[8'h27] = 8'h3d;
        InvSBox[8'h28] = 8'hee; InvSBox[8'h29] = 8'h4c; InvSBox[8'h2a] = 8'h95; InvSBox[8'h2b] = 8'h0b; InvSBox[8'h2c] = 8'h42; InvSBox[8'h2d] = 8'hfa; InvSBox[8'h2e] = 8'hc3; InvSBox[8'h2f] = 8'h4e;
        InvSBox[8'h30] = 8'h08; InvSBox[8'h31] = 8'h2e; InvSBox[8'h32] = 8'ha1; InvSBox[8'h33] = 8'h66; InvSBox[8'h34] = 8'h28; InvSBox[8'h35] = 8'hd9; InvSBox[8'h36] = 8'h24; InvSBox[8'h37] = 8'hb2;
        InvSBox[8'h38] = 8'h76; InvSBox[8'h39] = 8'h5b; InvSBox[8'h3a] = 8'ha2; InvSBox[8'h3b] = 8'h49; InvSBox[8'h3c] = 8'h6d; InvSBox[8'h3d] = 8'h8b; InvSBox[8'h3e] = 8'hd1; InvSBox[8'h3f] = 8'h25;
        InvSBox[8'h40] = 8'h72; InvSBox[8'h41] = 8'hf8; InvSBox[8'h42] = 8'hf6; InvSBox[8'h43] = 8'h64; InvSBox[8'h44] = 8'h86; InvSBox[8'h45] = 8'h68; InvSBox[8'h46] = 8'h98; InvSBox[8'h47] = 8'h16;
        InvSBox[8'h48] = 8'hd4; InvSBox[8'h49] = 8'ha4; InvSBox[8'h4a] = 8'h5c; InvSBox[8'h4b] = 8'hcc; InvSBox[8'h4c] = 8'h5d; InvSBox[8'h4d] = 8'h65; InvSBox[8'h4e] = 8'hb6; InvSBox[8'h4f] = 8'h92;
        InvSBox[8'h50] = 8'h6c; InvSBox[8'h51] = 8'h70; InvSBox[8'h52] = 8'h48; InvSBox[8'h53] = 8'h50; InvSBox[8'h54] = 8'hfd; InvSBox[8'h55] = 8'hed; InvSBox[8'h56] = 8'hb9; InvSBox[8'h57] = 8'hda;
        InvSBox[8'h58] = 8'h5e; InvSBox[8'h59] = 8'h15; InvSBox[8'h5a] = 8'h46; InvSBox[8'h5b] = 8'h57; InvSBox[8'h5c] = 8'ha7; InvSBox[8'h5d] = 8'h8d; InvSBox[8'h5e] = 8'h9d; InvSBox[8'h5f] = 8'h84;
        InvSBox[8'h60] = 8'h90; InvSBox[8'h61] = 8'hd8; InvSBox[8'h62] = 8'hab; InvSBox[8'h63] = 8'h00; InvSBox[8'h64] = 8'h8c; InvSBox[8'h65] = 8'hbc; InvSBox[8'h66] = 8'hd3; InvSBox[8'h67] = 8'h0a;
        InvSBox[8'h68] = 8'hf7; InvSBox[8'h69] = 8'he4; InvSBox[8'h6a] = 8'h58; InvSBox[8'h6b] = 8'h05; InvSBox[8'h6c] = 8'hb8; InvSBox[8'h6d] = 8'hb3; InvSBox[8'h6e] = 8'h45; InvSBox[8'h6f] = 8'h06;
        InvSBox[8'h70] = 8'hd0; InvSBox[8'h71] = 8'h2c; InvSBox[8'h72] = 8'h1e; InvSBox[8'h73] = 8'h8f; InvSBox[8'h74] = 8'hca; InvSBox[8'h75] = 8'h3f; InvSBox[8'h76] = 8'h0f; InvSBox[8'h77] = 8'h02;
        InvSBox[8'h78] = 8'hc1; InvSBox[8'h79] = 8'haf; InvSBox[8'h7a] = 8'hbd; InvSBox[8'h7b] = 8'h03; InvSBox[8'h7c] = 8'h01; InvSBox[8'h7d] = 8'h13; InvSBox[8'h7e] = 8'h8a; InvSBox[8'h7f] = 8'h6b;
        InvSBox[8'h80] = 8'h3a; InvSBox[8'h81] = 8'h91; InvSBox[8'h82] = 8'h11; InvSBox[8'h83] = 8'h41; InvSBox[8'h84] = 8'h4f; InvSBox[8'h85] = 8'h67; InvSBox[8'h86] = 8'hdc; InvSBox[8'h87] = 8'hea;
        InvSBox[8'h88] = 8'h97; InvSBox[8'h89] = 8'hf2; InvSBox[8'h8a] = 8'hcf; InvSBox[8'h8b] = 8'hce; InvSBox[8'h8c] = 8'hf0; InvSBox[8'h8d] = 8'hb4; InvSBox[8'h8e] = 8'he6; InvSBox[8'h8f] = 8'h73;
        InvSBox[8'h90] = 8'h96; InvSBox[8'h91] = 8'hac; InvSBox[8'h92] = 8'h74; InvSBox[8'h93] = 8'h22; InvSBox[8'h94] = 8'he7; InvSBox[8'h95] = 8'had; InvSBox[8'h96] = 8'h35; InvSBox[8'h97] = 8'h85;
        InvSBox[8'h98] = 8'he2; InvSBox[8'h99] = 8'hf9; InvSBox[8'h9a] = 8'h37; InvSBox[8'h9b] = 8'he8; InvSBox[8'h9c] = 8'h1c; InvSBox[8'h9d] = 8'h75; InvSBox[8'h9e] = 8'hdf; InvSBox[8'h9f] = 8'h6e;
        InvSBox[8'ha0] = 8'h47; InvSBox[8'ha1] = 8'hf1; InvSBox[8'ha2] = 8'h1a; InvSBox[8'ha3] = 8'h71; InvSBox[8'ha4] = 8'h1d; InvSBox[8'ha5] = 8'h29; InvSBox[8'ha6] = 8'hc5; InvSBox[8'ha7] = 8'h89;
        InvSBox[8'ha8] = 8'h6f; InvSBox[8'ha9] = 8'hb7; InvSBox[8'haa] = 8'h62; InvSBox[8'hab] = 8'h0e; InvSBox[8'hac] = 8'haa; InvSBox[8'had] = 8'h18; InvSBox[8'hae] = 8'hbe; InvSBox[8'haf] = 8'h1b;
        InvSBox[8'hb0] = 8'hfc; InvSBox[8'hb1] = 8'h56; InvSBox[8'hb2] = 8'h3e; InvSBox[8'hb3] = 8'h4b; InvSBox[8'hb4] = 8'hc6; InvSBox[8'hb5] = 8'hd2; InvSBox[8'hb6] = 8'h79; InvSBox[8'hb7] = 8'h20;
        InvSBox[8'hb8] = 8'h9a; InvSBox[8'hb9] = 8'hdb; InvSBox[8'hba] = 8'hc0; InvSBox[8'hbb] = 8'hfe; InvSBox[8'hbc] = 8'h78; InvSBox[8'hbd] = 8'hcd; InvSBox[8'hbe] = 8'h5a; InvSBox[8'hbf] = 8'hf4;
        InvSBox[8'hc0] = 8'h1f; InvSBox[8'hc1] = 8'hdd; InvSBox[8'hc2] = 8'ha8; InvSBox[8'hc3] = 8'h33; InvSBox[8'hc4] = 8'h88; InvSBox[8'hc5] = 8'h07; InvSBox[8'hc6] = 8'hc7; InvSBox[8'hc7] = 8'h31;
        InvSBox[8'hc8] = 8'hb1; InvSBox[8'hc9] = 8'h12; InvSBox[8'hca] = 8'h10; InvSBox[8'hcb] = 8'h59; InvSBox[8'hcc] = 8'h27; InvSBox[8'hcd] = 8'h80; InvSBox[8'hce] = 8'hec; InvSBox[8'hcf] = 8'h5f;
        InvSBox[8'hd0] = 8'h60; InvSBox[8'hd1] = 8'h51; InvSBox[8'hd2] = 8'h7f; InvSBox[8'hd3] = 8'ha9; InvSBox[8'hd4] = 8'h19; InvSBox[8'hd5] = 8'hb5; InvSBox[8'hd6] = 8'h4a; InvSBox[8'hd7] = 8'h0d;
        InvSBox[8'hd8] = 8'h2d; InvSBox[8'hd9] = 8'he5; InvSBox[8'hda] = 8'h7a; InvSBox[8'hdb] = 8'h9f; InvSBox[8'hdc] = 8'h93; InvSBox[8'hdd] = 8'hc9; InvSBox[8'hde] = 8'h9c; InvSBox[8'hdf] = 8'hef;
        InvSBox[8'he0] = 8'ha0; InvSBox[8'he1] = 8'he0; InvSBox[8'he2] = 8'h3b; InvSBox[8'he3] = 8'h4d; InvSBox[8'he4] = 8'hae; InvSBox[8'he5] = 8'h2a; InvSBox[8'he6] = 8'hf5; InvSBox[8'he7] = 8'hb0;
        InvSBox[8'he8] = 8'hc8; InvSBox[8'he9] = 8'heb; InvSBox[8'hea] = 8'hbb; InvSBox[8'heb] = 8'h3c; InvSBox[8'hec] = 8'h83; InvSBox[8'hed] = 8'h53; InvSBox[8'hee] = 8'h99; InvSBox[8'hef] = 8'h61;
        InvSBox[8'hf0] = 8'h17; InvSBox[8'hf1] = 8'h2b; InvSBox[8'hf2] = 8'h04; InvSBox[8'hf3] = 8'h7e; InvSBox[8'hf4] = 8'hba; InvSBox[8'hf5] = 8'h77; InvSBox[8'hf6] = 8'hd6; InvSBox[8'hf7] = 8'h26;
        InvSBox[8'hf8] = 8'he1; InvSBox[8'hf9] = 8'h69; InvSBox[8'hfa] = 8'h14; InvSBox[8'hfb] = 8'h63; InvSBox[8'hfc] = 8'h55; InvSBox[8'hfd] = 8'h21; InvSBox[8'hfe] = 8'h0c; InvSBox[8'hff] = 8'h7d;
    end

    // Rcon for Key Expansion
    reg [31:0] Rcon [0:10];
    initial begin
        Rcon[0] = 32'h00_00_00_00;
        Rcon[1] = 32'h01_00_00_00;
        Rcon[2] = 32'h02_00_00_00;
        Rcon[3] = 32'h04_00_00_00;
        Rcon[4] = 32'h08_00_00_00;
        Rcon[5] = 32'h10_00_00_00;
        Rcon[6] = 32'h20_00_00_00;
        Rcon[7] = 32'h40_00_00_00;
        Rcon[8] = 32'h80_00_00_00;
        Rcon[9] = 32'h1B_00_00_00;
        Rcon[10] = 32'h36_00_00_00;
    end

    // SubBytes and Inverse SubBytes
    function [127:0] SubBytes(input [127:0] data_in, input ENCDEC);
        integer i;
        reg [7:0] temp[0:15];
        begin
            for (i = 0; i < 16; i = i + 1)
            begin
                if (ENCDEC == 1) //ENC
                    temp[i] = SBox[data_in[127 - (i * 8) -: 8]];
                else             //DEC
                    temp[i] = InvSBox[data_in[127 - (i * 8) -: 8]];
            end
            SubBytes = {temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8],
                        temp[9], temp[10], temp[11], temp[12], temp[13], temp[14], temp[15]};
            $display("SubBytes = %h", SubBytes);
        end
    endfunction

    // ShiftRows and Inverse ShiftRows
    function [127:0] ShiftRows(input [127:0] data_in, input ENCDEC);
        reg [7:0] temp[0:11];
        begin
            if (ENCDEC == 1) //ENC
            begin
                temp[0]  = data_in[87:80];   temp[1]  = data_in[79:72];    temp[2]  = data_in[71:64];    temp[3]  = data_in[95:88];
                temp[4]  = data_in[47:40];   temp[5]  = data_in[39:32];    temp[6] = data_in[63:56];     temp[7] = data_in[55:48];
                temp[8] = data_in[7:0];      temp[9] = data_in[31:24];     temp[10] = data_in[23:16];    temp[11] = data_in[15:8];
            end
            else             //DEC
            begin
                temp[0]  = data_in[71:64];   temp[1]  = data_in[95:88];    temp[2]  = data_in[87:80];    temp[3]  = data_in[79:72];
                temp[4] = data_in[47:40];    temp[5]  = data_in[39:32];    temp[6] = data_in[63:56];     temp[7] = data_in[55:48];
                temp[8] = data_in[23:16];    temp[9] = data_in[15:8];      temp[10] = data_in[7:0];      temp[11] = data_in[31:24];
            end
            ShiftRows = {data_in[127:96], temp[0], temp[1], temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9], temp[10], temp[11]};
            $display("ShiftRows = %h", ShiftRows);
        end
    endfunction

    // AddRoundKey
    function [127:0] AddRoundKey(input [127:0] state_in, input [127:0] round_key);
        begin
            AddRoundKey = state_in ^ round_key;
            $display("AddRoundKey = %h\n", AddRoundKey);
        end
    endfunction
    
    // MixColumns 및 Inverse MixColumns 함수 구현
    function [127:0] MixColumns(input [127:0] state_in, input ENCDEC);
        reg [7:0] col[0:3];    // 열(column) 데이터를 임시 저장
        reg [7:0] result[0:3]; // 연산 결과 저장
        integer i;
        begin
            for (i = 0; i < 4; i = i + 1)
            begin
                // 각 열 데이터 추출
                col[0] = state_in[(127 - i*8) -: 8];
                col[1] = state_in[(95 - i*8) -: 8];
                col[2] = state_in[(63 - i*8) -: 8];
                col[3] = state_in[(31 - i*8) -: 8];

                if (ENCDEC == 1) //ENC
                begin
                    result[0] = gmul(col[0], 8'h02) ^ gmul(col[1], 8'h03) ^ col[2] ^ col[3];
                    result[1] = col[0] ^ gmul(col[1], 8'h02) ^ gmul(col[2], 8'h03) ^ col[3];
                    result[2] = col[0] ^ col[1] ^ gmul(col[2], 8'h02) ^ gmul(col[3], 8'h03);
                    result[3] = gmul(col[0], 8'h03) ^ col[1] ^ col[2] ^ gmul(col[3], 8'h02);
                end
                else             //DEC
                begin
                    result[0] = gmul(col[0], 8'h0e) ^ gmul(col[1], 8'h0b) ^ gmul(col[2], 8'h0d) ^ gmul(col[3], 8'h09);
                    result[1] = gmul(col[0], 8'h09) ^ gmul(col[1], 8'h0e) ^ gmul(col[2], 8'h0b) ^ gmul(col[3], 8'h0d);
                    result[2] = gmul(col[0], 8'h0d) ^ gmul(col[1], 8'h09) ^ gmul(col[2], 8'h0e) ^ gmul(col[3], 8'h0b);
                    result[3] = gmul(col[0], 8'h0b) ^ gmul(col[1], 8'h0d) ^ gmul(col[2], 8'h09) ^ gmul(col[3], 8'h0e);
                end
                MixColumns[(127 - i*8) -: 8] = result[0];
                MixColumns[(95 - i*8) -: 8] = result[1];
                MixColumns[(63 - i*8) -: 8] = result[2];
                MixColumns[(31 - i*8) -: 8] = result[3];
            end
            $display("MixColumns = %h", MixColumns);
        end
    endfunction

    // GF(2^8) 상에서 곱셈 함수
    function [7:0] gmul(input [7:0] a, input [7:0] b);
        reg [7:0] result;
        reg [7:0] msb;
        integer i;
        begin
            result = 8'h00;
            for (i = 0; i < 8; i = i + 1)
            begin
                if (b[i] == 1'b1)       
                    result = result ^ a;         
                msb = a & 8'h80; 
                a = a << 1;             
                if (msb != 0)    
                    a = a ^ 8'h1b;
            end
            gmul = result;
        end
    endfunction

    // FSM Logic
    always @(posedge CLK or negedge nRST)
    begin
        if (!nRST)                                 //nRST가 0일때
        begin                          
            current_state <= IDLE;                 //초기화
            DONE <= 0;
            state <= 0;
            round_counter <= 0;
        end
        else                                       //nRST가 1일때
        begin
            current_state <= next_state;           //state를 next state로
            case (current_state)
                IDLE:                              //state가 IDLE면
                begin
                    if (START)                     //START가 1일때 
                    begin
                        text <= TEXTIN;           //입력받은 TEXTIN, ENCDEC, KEY를 저장
                        enc <= ENCDEC;
                        key <= KEY;
                        state <= TEXTIN;
                        round_key <= KEY;
                        round_counter <= 0;
                        DONE <= 0;
                    end
                    else                            //start가 0이면(작동이 끝난 다음 clock)
                    begin
                        current_state <= IDLE;      //초기화
                        DONE <= 0;
                        state <= 0;
                        round_counter <= 0;
                        key <= 127'hX;
                        round_key <= 127'hX;
                        TEXTOUT <= 127'hX;
                    end
                end
                ROUND:                              //state가 ROUND면
                begin
                    if (round_counter < 1)          //round가 0일때
                    begin
                        round_key = KeyExpansion(key, enc, round_counter);
                        state = AddRoundKey(state, round_key);
                        round_counter = round_counter + 1;
                    end
                    else if (round_counter <= 9)     //round가 0~9일때  
                    begin
                        round_key = KeyExpansion(key, enc, round_counter);
                        state = (enc)? AddRoundKey(MixColumns(ShiftRows(SubBytes(state, enc), enc), enc), round_key):
                                       MixColumns(AddRoundKey(SubBytes(ShiftRows(state, enc), enc), round_key), enc);
                        round_counter = round_counter + 1;
                    end
                end
                FINAL:                              //state가 FINAL이면 (마지막 라운드)
                begin
                    round_key = KeyExpansion(key, enc, round_counter);
                    state = (enc)? AddRoundKey(ShiftRows(SubBytes(state, enc), enc), round_key):
                                   AddRoundKey(SubBytes(ShiftRows(state, enc), enc), round_key);
                    round_counter = round_counter + 1;
                    DONE <= 1;
                    TEXTOUT <= state;
                    $display("ENCDEC = %d, %h -> %h", enc,  text, state);
                end
            endcase
        end
    end

    // Next State Logic
    always @(*)
    begin
        case (current_state)
            IDLE: next_state = (START) ? ROUND : IDLE;
            ROUND: next_state = (round_counter == 9) ? FINAL : ROUND;
            FINAL: next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // Key Expansion
    function [127:0] KeyExpansion(input [127:0] key, input ENCDEC, input [3:0] round);
        reg [127:0] expanded_key;
        reg [31:0] temp;
        reg [3:0] r; //각 과정에 맞는 round key를 만들기 위한 반복 횟수 (0~10)
        integer i;
        integer j;
        begin
            r = (ENCDEC)? round : 10 - round;
            $display("ENCDEC = %d, round = %d, r = %d", ENCDEC, round, r);
        
            expanded_key = key;
            i = 0;
             $display("%d %h%h%h%h", i, expanded_key[127:96], expanded_key[95:64], expanded_key[63:32], expanded_key[31:0]);
            for(i = 1; i <= r; i = i + 1)
            begin
                temp = {expanded_key[103:96], expanded_key[71:64], expanded_key[39:32], expanded_key[7:0]}; //전 round key의 마지막 열(ENC기준)
                temp = {SBox[temp[23:16]], SBox[temp[15:8]], SBox[temp[7:0]], SBox[temp[31:24]]} ^ Rcon[i];
                for(j = 0; j < 4; j = j + 1)
                begin
                    if (j % 4 == 0) //expanded_key의 첫번째 열 생성
                    begin
                        temp = temp ^ {expanded_key[127 - (8 * j)-:8], expanded_key[95 - (8 * j)-:8], 
                                       expanded_key[63 - (8 * j)-:8], expanded_key[31 - (8 * j)-:8]};
                        {expanded_key[127 - (8 * j)-:8], expanded_key[95 - (8 * j)-:8], 
                        expanded_key[63 - (8 * j)-:8], expanded_key[31 - (8 * j)-:8]}   = temp;
                    end
                    else            //expanded_key의 나머지 열 생성
                    {expanded_key[127-(8*j)-:8], expanded_key[95-(8*j)-:8], expanded_key[63-(8*j)-:8], expanded_key[31-(8*j)-:8]} = 
                    {expanded_key[127-(8*j)-:8], expanded_key[95-(8*j)-:8], expanded_key[63-(8*j)-:8], expanded_key[31-(8*j)-:8]} ^
                    {expanded_key[127-(8*(j-1))-:8], expanded_key[95-(8*(j-1))-:8], expanded_key[63-(8*(j-1))-:8], expanded_key[31-(8*(j-1))-:8]};
                end
                $display("%d %h", i,  expanded_key);
            end
            KeyExpansion = expanded_key;
        end
    endfunction
    
endmodule
