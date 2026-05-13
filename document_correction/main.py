"""Main entry point — CLI for single-image and batch processing."""

import os
import argparse
import glob
import sys

# Allow running from project root or document_correction/ directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Document Image Auto-Correction & Enhancement System"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input image or directory (for batch mode).",
    )
    parser.add_argument(
        "--output", default="./output",
        help="Output directory (default: ./output).",
    )
    parser.add_argument(
        "--save-steps", action="store_true",
        help="Save intermediate step images.",
    )
    parser.add_argument(
        "--batch", action="store_true",
        help="Process all images in the input directory.",
    )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.batch:
        if not os.path.isdir(args.input):
            print(f"[ERROR] --batch requires a directory, got: {args.input}")
            sys.exit(1)
        extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.JPG", "*.JPEG", "*.PNG", "*.BMP")
        image_files = []
        for ext in extensions:
            image_files.extend(glob.glob(os.path.join(args.input, ext)))
        image_files = sorted(set(image_files))
        if not image_files:
            print(f"[ERROR] No image files found in: {args.input}")
            sys.exit(1)

        success_count = 0
        total_time = 0.0
        for img_path in image_files:
            print(f"[INFO] Processing: {os.path.basename(img_path)}")
            result = run_pipeline(img_path, args.output, save_steps=args.save_steps)
            print(f"[INFO] Document detected: {result['success']}")
            print(f"[INFO] Processing time: {result['processing_time']:.2f}s")
            print(f"[INFO] Saved: {result['output_path']}")
            print()
            if result["success"]:
                success_count += 1
            total_time += result["processing_time"]

        total = len(image_files)
        print(f"[SUMMARY] Detection success: {success_count}/{total} ({100 * success_count / total:.1f}%)")
        print(f"[SUMMARY] Total processing time: {total_time:.2f}s")
    else:
        if not os.path.isfile(args.input):
            print(f"[ERROR] File not found: {args.input}")
            sys.exit(1)

        result = run_pipeline(args.input, args.output, save_steps=args.save_steps)
        print(f"[INFO] Processing: {os.path.basename(args.input)}")
        print(f"[INFO] Document detected: {result['success']}")
        print(f"[INFO] Processing time: {result['processing_time']:.2f}s")
        print(f"[INFO] Saved: {result['output_path']}")


if __name__ == "__main__":
    main()
