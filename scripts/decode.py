import csv
import os

RESULTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

# weights and inputs of each MAC run
MACS = {
    "mac4x4_default.csv": ([15, 10, 5, 3], [15, 6, 9, 12]),
    "mac4x4_worst_case.csv": ([15, 15, 15, 15], [15, 15, 15, 15]),
}


def read(file_name):
    with open(os.path.join(RESULTS, file_name)) as f:
        return list(csv.DictReader(f))


# the count whose level is closest to this voltage
def to_count(voltage, levels):
    distances = [abs(voltage - level) for level in levels]
    return distances.index(min(distances))


def count_sweep():
    levels = [float(row["V_rbl_V"]) for row in read("column8_count_sweep.csv")]
    print("Count sweep")
    for k, level in enumerate(levels):
        step = "" if k == 0 else "  step %3.0f mV" % ((levels[k - 1] - level) * 1000)
        print("  %d cells  %.3f V%s" % (k, level, step))
    return levels


def boolean(levels):
    print("\nBoolean (count = A + B)")
    for row in read("column8_boolean.csv"):
        count = to_count(float(row["V_rbl_V"]), levels)
        nor = 1 if count == 0 else 0
        xor = 1 if count == 1 else 0
        and_ = 1 if count == 2 else 0
        print("  A=%s B=%s  %s V  count %d  NOR %d  XOR %d  AND %d" % (row["A"], row["B"], row["V_rbl_V"], count, nor, xor, and_))


def mac(file_name, weights, inputs, levels):
    print("\n%s  w = %s  x = %s" % (file_name, weights, inputs))
    total = 0
    for row in read(file_name):
        cycle = int(row["j"])
        column = int(row["col"])
        count = to_count(float(row["V_rbl_V"]), levels)
        # count from column c in cycle j is worth 2^(j + c)
        place_value = 2 ** (cycle + column)
        total += count * place_value
        print("  cycle %d  column %d  %s V  count %d  x%d" % (cycle, column, row["V_rbl_V"], count, place_value))
    exact = sum(w * x for w, x in zip(weights, inputs))
    result = "MATCH" if total == exact else "MISMATCH"
    print("  MAC from memory = %d, exact = %d, %s" % (total, exact, result))


levels = count_sweep()
boolean(levels)
for file_name, (weights, inputs) in MACS.items():
    mac(file_name, weights, inputs, levels)
