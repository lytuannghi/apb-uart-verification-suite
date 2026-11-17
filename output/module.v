module counter_4bit_overflow (
    input  wire       clk,
    input  wire       rst_n,
    input  wire       en,
    output reg  [3:0] count,
    output wire       overflow
);

    // Logic đếm: Reset bất đồng bộ (Active High), tăng giá trị khi en = 1
    always @(posedge clk or posedge rst_n) begin
        if (rst_n) begin
            count <= 4'b0000;
        end else if (en) begin
            count <= count + 4'b0001;
        end
    end

    // Cờ báo tràn: Tích cực khi count đạt 15 và en đang ở mức cao
    // Logic này đảm bảo overflow xuất hiện đúng chu kỳ count đạt 15
    assign overflow = (count == 4'd15) && en;

endmodule