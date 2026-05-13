"""Full processing pipeline orchestrating all 11 steps."""

import os
import time

from utils.image_io import load_image, save_image, save_step
from modules.preprocessing import to_grayscale, apply_gaussian_blur
from modules.detection import detect_edges, dilate_edges, find_contours, find_document_contour, draw_contour
from modules.geometry import order_points, apply_perspective_transform
from modules.enhancement import enhance


def run_pipeline(input_path, output_dir, save_steps=False):
    """Run the full document correction pipeline on a single image.

    Args:
        input_path: Path to input image.
        output_dir: Directory for output images.
        save_steps: If True, save 7 intermediate step images.

    Returns:
        dict: {success: bool, output_path: str, processing_time: float}
    """
    start_time = time.time()
    basename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{basename}_corrected.jpg")
    steps_dir = os.path.join(output_dir, f"{basename}_steps") if save_steps else None

    # Step 1: Load
    original = load_image(input_path)
    if save_steps:
        save_step(original, steps_dir, 1, "original")

    # Step 2: Grayscale
    gray = to_grayscale(original)
    if save_steps:
        save_step(gray, steps_dir, 2, "grayscale")

    # Step 3: Gaussian blur
    blurred = apply_gaussian_blur(gray)
    if save_steps:
        save_step(blurred, steps_dir, 3, "blurred")

    # Step 4: Canny edge detection
    edges = detect_edges(blurred)
    if save_steps:
        save_step(edges, steps_dir, 4, "edges")

    # Step 4b: Dilate edges to connect fragmented segments
    dilated = dilate_edges(edges)

    # Step 5-6: Contour detection + quadrilateral approximation
    contours = find_contours(dilated)
    img_area = original.shape[0] * original.shape[1]
    doc_contour = find_document_contour(contours, img_area)

    if save_steps and contours:
        display_contour = doc_contour if doc_contour is not None else contours[0]
        contour_img = draw_contour(original, display_contour)
        save_step(contour_img, steps_dir, 5, "contours")

    if doc_contour is not None:
        # Step 7-8: Corner ordering + perspective transform
        ordered_pts = order_points(doc_contour)
        warped = apply_perspective_transform(original, ordered_pts)
        if save_steps:
            save_step(warped, steps_dir, 6, "perspective")

        # Step 9-10: Enhancement
        result = enhance(warped)
        if save_steps:
            save_step(result, steps_dir, 7, "enhanced")

        success = True
    else:
        # Detection failed — apply enhancement directly on original
        result = enhance(original)
        if save_steps:
            save_step(original, steps_dir, 6, "perspective")
            save_step(result, steps_dir, 7, "enhanced")

        success = False

    save_image(result, output_path)
    elapsed = time.time() - start_time

    return {
        "success": success,
        "output_path": output_path,
        "processing_time": elapsed,
    }
