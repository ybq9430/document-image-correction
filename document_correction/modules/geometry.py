"""Geometry correction module — Step 7-8: Corner ordering and perspective transform."""

import cv2
import numpy as np


def _dist(p1, p2):
    """Euclidean distance between two points."""
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def order_points(pts):
    """Order 4 corner points as [TL, TR, BR, BL].

    TL: min x+y,  BR: max x+y,  TR: max x-y,  BL: min x-y.
    Returns shape (4, 2) float32 ndarray.
    """
    pts = pts.reshape(4, 2)
    ordered = np.zeros((4, 2), dtype=np.float32)

    sums = pts.sum(axis=1)
    diffs = np.diff(pts, axis=1)

    ordered[0] = pts[np.argmin(sums)]   # TL
    ordered[2] = pts[np.argmax(sums)]   # BR
    ordered[1] = pts[np.argmax(diffs)]  # TR
    ordered[3] = pts[np.argmin(diffs)]  # BL

    return ordered


def calculate_output_size(ordered_pts):
    """Compute output width and height from ordered corner points.

    width  = max(dist(BL,BR), dist(TL,TR))
    height = max(dist(TR,BR), dist(TL,BL))
    """
    tl, tr, br, bl = ordered_pts
    width = int(max(_dist(bl, br), _dist(tl, tr)))
    height = int(max(_dist(tr, br), _dist(tl, bl)))
    return width, height


def apply_perspective_transform(img, ordered_pts):
    """Apply perspective correction to straighten the document.

    Uses: cv2.getPerspectiveTransform(src_pts, dst_pts)
          cv2.warpPerspective(img, M, (width, height))
    """
    width, height = calculate_output_size(ordered_pts)
    dst_pts = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1],
    ], dtype=np.float32)

    M = cv2.getPerspectiveTransform(ordered_pts, dst_pts)
    warped = cv2.warpPerspective(img, M, (width, height))
    return warped
