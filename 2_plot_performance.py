import glob
import os

import matplotlib.pyplot as plt
import numpy as np


def read_pass_at_one(file_path):
    with open(file_path, "r") as f:
        data = eval(f.read())
        return data.get("pass@1", None)


def main():
    folder_path = "data/"
    files = glob.glob(os.path.join(folder_path, "*_results.txt"))

    heat_map_data = {}

    for file_path in files:
        base_name = os.path.basename(file_path)
        parts = base_name.split("_")
        if len(parts) < 3:
            print(f"Skipping invalid file: {file_path}")
            continue

        temperature, top_p = float(parts[1]), float(parts[2])

        pass_at_one = read_pass_at_one(file_path)
        if pass_at_one is not None:
            heat_map_data[(temperature, top_p)] = pass_at_one

    unique_temperatures = sorted(set(x[0] for x in heat_map_data.keys()))
    unique_top_p = sorted(set(x[1] for x in heat_map_data.keys()))
    z_values = np.zeros((len(unique_temperatures), len(unique_top_p)))

    for i, temp in enumerate(unique_temperatures):
        for j, top in enumerate(unique_top_p):
            z_values[i, j] = heat_map_data.get((temp, top), 0)

    plt.imshow(z_values, aspect="auto", origin="lower")

    # extract colormap from plt.imshow
    cmap = plt.get_cmap("viridis")  # viridis is the default colormap of imshow
    norm = plt.Normalize(vmin=z_values.min(), vmax=z_values.max())

    # Annotate heatmap with the pass@1 values
    for i, temp in enumerate(unique_temperatures):
        for j, top in enumerate(unique_top_p):
            pass_at_one_value = heat_map_data.get((temp, top), None)
            if pass_at_one_value is not None:
                color = cmap(norm(pass_at_one_value))
                luminance = (
                    0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
                )  # formula to calculate luminance
                text_color = (
                    "black" if luminance > 0.5 else "white"
                )  # if luminance is high, use black, else white
                plt.text(
                    j,
                    i,
                    f"{pass_at_one_value:.2f}",
                    ha="center",
                    va="center",
                    color=text_color,
                )

    plt.colorbar(label="pass@1")
    plt.xlabel("top_p", fontsize=14)
    plt.ylabel("temperature", fontsize=14)

    # Set the tick labels for the x and y axes
    plt.xticks(np.arange(len(unique_top_p)), [str(round(p, 2)) for p in unique_top_p])
    plt.yticks(
        np.arange(len(unique_temperatures)),
        [str(round(t, 2)) for t in unique_temperatures],
    )

    plt.title("Heatmap of pass@1")

    plt.savefig("pass_at_one_heatmap.png")
    plt.show()

    


if __name__ == "__main__":
    main()
