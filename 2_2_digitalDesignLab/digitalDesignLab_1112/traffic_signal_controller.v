`timescale 1ns / 1ps

module traffic_signal_controller(hwy, cntry, X, clock, clear, y2rdelay, r2gdelay);

output [1:0] hwy, cntry;
reg[1:0] hwy, cntry;

input X;
input clock, clear;
input [2:0] y2rdelay, r2gdelay;

parameter RED = 2'd0, YELLOW = 2'd1, GREEN = 2'd2;
parameter S0 = 3'd0, S1 = 3'd1, S2 = 3'd2, S3 = 3'd3, S4 = 3'd4;

reg [2:0] state;
reg [2:0] next_state;
reg [2:0] y2rcounter;
reg [2:0] r2gcounter;

always @(posedge clock)
    if(clear)
    begin
        state <= S0;
        y2rcounter <= 3'd0;
        r2gcounter <= 3'd0;
    end
    else
        state <= next_state;
        
 always @(state)
 begin
    hwy = GREEN;
    cntry = RED;
    case(state)
        S0: ;
        S1: hwy = YELLOW;
        S2: hwy = RED;
        S3: begin
                hwy = RED;
                cntry = GREEN;
            end
        S4: begin
                hwy = RED;
                cntry = YELLOW;
            end
    endcase
end

always @(state or X or y2rcounter or r2gcounter)
begin
    case (state)
        S0: if (X)
                next_state = S1;
            else
                next_state = S0;
        S1: if(y2rcounter == y2rdelay)
            begin
                next_state = S2;
            end
        S2:if(r2gcounter == r2gdelay)
            begin
                next_state = S3;
            end
        S3: if(X)
                next_state = S3;
            else
                next_state = S4;
        S4: if(y2rcounter == y2rdelay)
            begin
                next_state = S0;
            end
        default: next_state = S0;
    endcase
end

always @(posedge clock)
    if(state == next_state)
    begin
        if(state == S2)
        begin
            r2gcounter = r2gcounter + 1;
            y2rcounter = 3'd0;
        end
        else if((state == S1) || (state == S4))
        begin
            y2rcounter = y2rcounter + 1;
            r2gcounter = 3'd0;
        end
    end
    else
    begin
        y2rcounter = 3'd0;
        r2gcounter = 3'd0;
    end
endmodule