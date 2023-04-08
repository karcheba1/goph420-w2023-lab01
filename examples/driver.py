import numpy as np

from fem_1d_heat.geometry import (
    global_to_local,
    shape_matrix,
)


def main():
    print("successfully imported fem_1d_heat")

    z = 3.0
    z_e = np.array([0, 6])
    print(f"testing global_to_local({z}, {z_e}): {global_to_local(z, z_e)}")

    z = 2.0
    z_e = np.array([1, 4])
    print(f"testing global_to_local({z}, {z_e}): {global_to_local(z, z_e)}")

    s = 0.9
    print(f"testing shape_matrix({s}): {shape_matrix(s)}")


if __name__ == "__main__":
    main()
