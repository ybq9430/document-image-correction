"""Image enhancement module — Step 9-10: CLAHE, adaptive threshold, morphology."""

import cv2
import numpy as np


def apply_clahe(img_gray, clip_limit=2.0, tile_size=(8, 8)):
    """Enhance local contrast using CLAHE.

    Uses: cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    return clahe.apply(img_gray)


def apply_adaptive_threshold(img_gray, block_size=11, C=2):
    """Binarize image with adaptive thresholding to handle uneven illumination.

    Uses: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, block_size, C)
    """
    return cv2.adaptiveThreshold(
        img_gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        block_size, C,
    )


def apply_morphology(img_binary, kernel_size=(3, 3)):
    """Clean binary image with morphological closing.

    Uses: cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
          cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel)


def enhance(warped):
    """Run full enhancement pipeline on the perspective-corrected image.

    Steps: grayscale → CLAHE → adaptive threshold → morphological close.
    Returns BGR image (converted from binary for consistent I/O).
    """
    gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    clahed = apply_clahe(gray)
    thresh = apply_adaptive_threshold(clahed)
    cleaned = apply_morphology(thresh)
    return cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)
