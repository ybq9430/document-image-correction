"""Document detection module — Step 4-6: Canny edge, contour, quad approximation."""

import cv2
import numpy as np


def detect_edges(blurred, low=75, high=200):
    """Extract edges from blurred grayscale image.

    Uses: cv2.Canny(blurred, low, high)
    """
    return cv2.Canny(blurred, low, high)


def dilate_edges(edges, kernel_size=(3, 3), iterations=2):
    """Dilate edge map to connect fragmented edge segments.

    Uses: cv2.dilate(edges, kernel, iterations=iterations)
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.dilate(edges, kernel, iterations=iterations)


def find_contours(edges):
    """Extract contours from edge map, sorted by area descending (top 10).

    Uses: cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    """
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[:10]


def _approx_quad(contour):
    """Try to approximate a contour to a quadrilateral at various epsilon ratios.

    Returns (4,1,2) ndarray on success, None otherwise.
    """
    peri = cv2.arcLength(contour, True)
    for ratio in (0.02, 0.03, 0.05, 0.08, 0.10):
        epsilon = ratio * peri
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            return approx
    return None


def find_document_contour(contours, img_area=0):
    """Return the best quadrilateral document candidate.

    Strategy:
      1. Try direct polygon approximation of each contour.
      2. For larger contours, also try convex-hull → polygon approximation.
      3. Reject quads covering less than 2% of the image area.

    Uses: cv2.approxPolyDP(), cv2.convexHull(), cv2.contourArea()
    Returns np.ndarray of shape (4,1,2) on success, None otherwise.
    """
    min_area = img_area * 0.02 if img_area > 0 else 5000

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        # Strategy 1: direct approximation
        quad = _approx_quad(contour)
        if quad is not None:
            return quad

        # Strategy 2: convex hull + approximation (for partial edges near frame)
        hull = cv2.convexHull(contour)
        quad = _approx_quad(hull)
        if quad is not None:
            return quad

    # Fallback: combine significant contours and try hull
    if len(contours) >= 2:
        combined = np.vstack(contours)
        hull = cv2.convexHull(combined)
        hull_area = cv2.contourArea(hull)
        if hull_area >= min_area:
            quad = _approx_quad(hull)
            if quad is not None:
                return quad

    return None


def draw_contour(img, contour):
    """Draw the detected document boundary in green on a copy of the image.

    Uses: cv2.drawContours(img, [contour], -1, (0,255,0), 2)
    Returns BGR image.
    """
    result = img.copy()
    cv2.drawContours(result, [contour], -1, (0, 255, 0), 3)
    return result
