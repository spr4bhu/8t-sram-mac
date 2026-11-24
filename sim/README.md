# Simulation

Spectre netlists of the `sram8t_cim` cells and testbenches, and the initial-condition files that store data in the
cells. Model section `stat`, transient to 10 ns (80 ns for `tb_sram8t`).

| File | What it is |
|---|---|
| `netlists/sram8t.scs`, `netlists/cim_column8.scs` | The cells. |
| `netlists/tb_*.scs` | The testbenches. |
| `ic/column8_all_ones.scs` | Every cell in the column stores 1. Count sweep. |
| `ic/boolean_a*b*.scs` | Row 0 stores A, row 1 stores B. Boolean cases. |
| `ic/mac4x4_w15_10_5_3.scs` | Weights 15, 10, 5, 3 in `tb_mac4x4`. |
| `ic/mac4x4_w15_15_15_15.scs` | Weights 15, 15, 15, 15 in `tb_mac4x4`. |

A stored 1 is Q = 0 V, Qbar = 1.8 V.

| Testbench | Design variables |
|---|---|
| `tb_sram8t` | none |
| `tb_cim_column8` | `k` = rows read (0 to 8), `C_rbl` = 4p, `t_eval` = 1n |
| `tb_mac4x4` | `j` = cycle (0 to 3), `x0`..`x3` = inputs (0 to 15), `C_rbl` = 4p, `t_eval` = 1n |
