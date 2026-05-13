"""Preprocessing module — Step 2-3: Grayscale conversion and Gaussian blur."""

import cv2


def to_grayscale(img):
    """Convert BGR image to grayscale using weighted sum.

    Formula: Gray = 0.299*R + 0.587*G + 0.114*B
    Uses: cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def apply_gaussian_blur(gray, kernel_size=(5, 5), sigma=0):
    """Apply Gaussian filter to suppress high-frequency noise.

    Uses: cv2.GaussianBlur(gray, kernel_size, sigma)
    """
    return cv2.GaussianBlur(gray, kernel_size, sigma)
