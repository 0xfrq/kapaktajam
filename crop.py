import os
import glob
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from PIL import Image

REFERENCE_IMAGE = "refference.png"
CROP_BOX = None
INPUT_DIR  = r"D:\autoscreenshot\screenshots\tiripanselatan"
OUTPUT_DIR = r"D:\autoscreenshot\cropped"
IMAGE_GLOB = "*.png"

selected_coords = {}


def on_select(eclick, erelease):
    x1, y1 = int(eclick.xdata),   int(eclick.ydata)
    x2, y2 = int(erelease.xdata), int(erelease.ydata)
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)
    selected_coords.update(x1=x1, y1=y1, x2=x2, y2=y2)
    print(f"\nCrop box -> (x1={x1}, y1={y1}, x2={x2}, y2={y2})")
    print(f"Width  = {x2 - x1} px")
    print(f"Height = {y2 - y1} px\n")


def pick_crop_region(image_path: str):
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    fig, ax = plt.subplots(figsize=(min(w / 80, 16), min(h / 80, 9)))
    ax.imshow(img)
    ax.set_title(f"{Path(image_path).name}   ({w}x{h})", fontsize=9)
    ax.set_xlabel("x  (pixels from left)")
    ax.set_ylabel("y  (pixels from top)")

    rs = RectangleSelector(
        ax, on_select,
        useblit=True,
        button=[1],
        minspanx=5, minspany=5,
        spancoords="pixels",
        interactive=True,
        props=dict(edgecolor="lime", linewidth=2, fill=False),
    )

    def on_move(event):
        if event.inaxes:
            ax.set_xlabel(f"x = {int(event.xdata)}   y = {int(event.ydata)}")
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_move)
    plt.tight_layout()
    plt.show()

    return selected_coords.get("x1"), selected_coords.get("y1"), \
           selected_coords.get("x2"), selected_coords.get("y2")


def batch_crop(crop_box, input_dir=INPUT_DIR, output_dir=OUTPUT_DIR, pattern=IMAGE_GLOB):
    x1, y1, x2, y2 = crop_box
    pil_box = (x1, y1, x2, y2)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    files = glob.glob(str(Path(input_dir) / pattern))
    if not files:
        print(f"No files found matching {input_dir}/{pattern}")
        return

    print(f"\nCropping {len(files)} image(s) -> {output_dir}/")
    for fpath in sorted(files):
        try:
            img = Image.open(fpath)
            cropped = img.crop(pil_box)
            out_file = out_path / Path(fpath).name
            cropped.save(out_file)
            print(f"  {Path(fpath).name}")
        except Exception as e:
            print(f"  {Path(fpath).name}: {e}")

    print("Done.")


if __name__ == "__main__":
    x1, y1, x2, y2 = pick_crop_region(REFERENCE_IMAGE)

    if x1 is None:
        print("No region selected — exiting.")
    else:
        print(f"Selected crop box: ({x1}, {y1}, {x2}, {y2})")
        answer = input("Apply this crop to all images in the folder? [y/N]: ").strip().lower()

        if answer == "y":
            batch_crop(
                crop_box=(x1, y1, x2, y2),
                input_dir=INPUT_DIR,
                output_dir=OUTPUT_DIR,
                pattern=IMAGE_GLOB,
            )
        else:
            print("Batch crop skipped.")
            print(f"CROP_BOX = ({x1}, {y1}, {x2}, {y2})")
            print(f"batch_crop(CROP_BOX)")