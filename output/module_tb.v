`timescale 1ns / 1ps

module counter_4bit_overflow_tb;

    // Signals
    reg clk;
    reg rst_n;
    reg en;
    wire [3:0] count;
    wire overflow;

    // Instantiate the DUT (Device Under Test)
    counter_4bit_overflow dut (
        .clk(clk),
        .rst_n(rst_n),
        .en(en),
        .count(count),
        .overflow(overflow)
    );

    // Clock generation
    always #5 clk = ~clk;

    // Testbench procedure
    initial begin
        // Setup waveform dump
        $dumpfile("output/waveform.vcd");
        $dumpvars(0, counter_4bit_overflow_tb);

        // Initialize signals
        clk = 0;
        rst_n = 0;
        en = 0;

        // 1. Power-on Reset Test
        #10 rst_n = 1;
        #10;
        if (count == 4'b0000) $display("PASS: Power-on Reset");
        else $display("FAIL: Power-on Reset, count = %d", count);
        rst_n = 0;

        // 2. Normal Counting & Overflow Test
        en = 1;
        repeat(16) @(posedge clk);
        
        // Check overflow at count 15
        if (overflow == 1'b1 && count == 4'd15) $display("PASS: Overflow detected at 15");
        else $display("FAIL: Overflow logic error");

        // 3. Roll-over Behavior
        @(posedge clk);
        if (count == 4'd0) $display("PASS: Roll-over to 0");
        else $display("FAIL: Roll-over failed, count = %d", count);

        // 4. Enable Toggle (Hold state)
        en = 0;
        repeat(2) @(posedge clk);
        if (count == 4'd0) $display("PASS: Hold state maintained");
        else $display("FAIL: Hold state failed, count = %d", count);

        // 5. Asynchronous Reset during counting
        en = 1;
        repeat(5) @(posedge clk);
        rst_n = 1;
        #2; // Check mid-cycle
        if (count == 4'd0) $display("PASS: Asynchronous Reset during counting");
        else $display("FAIL: Asynchronous Reset failed, count = %d", count);
        
        #10;
        $display("Simulation Finished.");
        $finish;
    end

endmodule