# APB UART IP - Design Verification Plan (vPlan)

## 1. Verification Objectives
The goal of this verification suite is to achieve 100% functional and protocol compliance for the **APB UART Controller**, verifying:
1. Complete adherence to the **AMBA 3 APB** bus protocol.
2. Accurate serialization/deserialization across programmed baud rates.
3. Robust FIFO management under normal, boundary, and stress conditions.
4. Correct generation of status flags and interrupt signaling.

---

## 2. Feature & Test Matrix

| Test ID | Feature Under Test | Scenario / Stimulus | Expected Result | Pass Criteria |
| :---: | :--- | :--- | :--- | :---: |
| **TC_RST_01** | Reset Verification | Assert `PRESETn` low, inspect all internal registers. | All registers reset to default states (`STATUS=0x01` - TX Empty). | PASS |
| **TC_APB_01** | APB Read/Write Timing | Perform 32-bit APB transfers to Baud and Control registers. | `PREADY` asserts on access phase; data read back matches written value. | PASS |
| **TC_BAUD_01**| Baudrate Divisor | Configure divisor register, monitor internal baud pulse rate. | Pulse generation rate matches expected frequency divider. | PASS |
| **TC_TX_01**  | Single-Byte TX | Write `0xA5` into `UART_DATA`, enable TX, observe `UART_TXD`. | Generates 1 start bit, 8 data bits (LSB first), 1 stop bit. | PASS |
| **TC_LOOP_01**| Internal Loopback Mode| Connect TX to RX internally, burst transmit multiple bytes. | All bytes received into RX FIFO with zero data corruption. | PASS |
| **TC_FIFO_01**| TX FIFO Overflow | Write 17 consecutive bytes into 16-deep TX FIFO without popping. | 16th byte accepted; 17th byte dropped; `TX_Full` asserted; no hang. | PASS |
| **TC_FIFO_02**| RX FIFO Underflow| Attempt APB read from empty RX FIFO. | Returns `0x00`; `RX_Empty` flag maintained; no corruption. | PASS |
| **TC_INT_01** | Interrupt Generation| Trigger RX Data Ready and TX Done conditions. | `UART_INT` asserts high; de-asserts upon servicing registers. | PASS |
| **TC_PROT_01**| APB Protocol Checker| Drive irregular bus sequences (`PENABLE` without `PSEL`). | IP ignores unauthorized access without corrupting state. | PASS |

---

## 3. Testbench Architecture (Self-Checking)
- **Bus Functional Model (BFM):** `apb_write()` and `apb_read()` tasks driving standard setup and access phases.
- **Scoreboard:** Tracks transmitted bytes in a golden queue and matches them against popped RX bytes.
- **Assertions:** Immediate & concurrent checks verifying protocol handshakes and data parity.
