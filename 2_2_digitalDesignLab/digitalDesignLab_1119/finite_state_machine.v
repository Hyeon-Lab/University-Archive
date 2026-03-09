`timescale 1ns / 1ps

module finite_state_machine(Y_OUT, CLK, nRST, X_IN);
output Y_OUT;
input CLK, nRST, X_IN;

reg Y_OUT;

parameter S0 = 2'd0, S1 = 2'd1, S2 = 2'd2;

reg [1:0] state;
reg [1:0] next_state;

always @(posedge CLK, nRST)
    if(!nRST)
        state <= S0;
    else
        state <= next_state;

always @(state)
begin
    Y_OUT = 1'b0;
    case(state)
        S0:;
        S1:Y_OUT = 1'b1;
        S2:Y_OUT = 1'b0;
    endcase
end

always @(state or X_IN)
    case (state)
        S0: if(X_IN)
                next_state = S1;
            else
                next_state = S0;
                
        S1: begin
            repeat(2) @(posedge CLK);
            next_state = S2;
            end
            
        S2:begin
           repeat(1) @(posedge CLK);
           next_state = S0;
           end
    endcase
endmodule
