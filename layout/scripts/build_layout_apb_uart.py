#!/usr/bin/env python3
import os
from build_layout_engine import build_asic_layout

if __name__ == "__main__":
    lay_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gds_out = os.path.join(lay_root, "gds", "apb_uart_top.gds")
    rep_out = os.path.join(lay_root, "reports", "drc_report.txt")
    build_asic_layout(
        gds_path=gds_out,
        report_path=rep_out,
        top_name="apb_uart_top",
        libname="APB_UART_TOP_LIB",
        die_w=240000,
        die_h=240000,
        macro_cols=2,
        macro_rows=2,
        pad_count_per_side=4,
    )
