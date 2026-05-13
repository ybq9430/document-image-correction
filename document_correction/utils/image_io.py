"""Image I/O utilities — cv2.imread, cv2.imwrite, matplotlib."""

import os
import cv2
import matplotlib.pyplot as plt


def load_image(path):
    """Load image from file path as BGR ndarray. Raises FileNotFoundError if missing.

    Uses: cv2.imread()
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image file not found: {path}")
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Image file not found: {path}")
    return img


def save_image(img, path):
    """Save image to disk.

    Uses: cv2.imwrite()
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    cv2.imwrite(path, img)


def save_step(img, output_dir, step_num, step_name):
    """Save intermediate result as '{step_num:02d}_{step_name}.jpg'.

    Uses: cv2.imwrite()
    """
    filename = f"{step_num:02d}_{step_name}.jpg"
    filepath = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(filepath, img)


def show_comparison(original, result, title="Comparison"):
    """Display original and result side-by-side using matplotlib.

    Uses: matplotlib.pyplot
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original")
    axes[0].axis("off")
    axes[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Result")
    axes[1].axis("off")
    fig.suptitle(title)
    plt.tight_layout()
    plt.show()
