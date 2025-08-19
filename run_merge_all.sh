#!/bin/bash

# Example usage:
# ./run_merge_all.sh /abs/path/to/folder_corner1 /abs/path/to/folder_corner2 /abs/path/to/folder_corner3 /abs/path/to/folder_corner4 /abs/path/to/output

FOLDER_CORNER1="$1"  # e.g. bottom-left (no shift)
FOLDER_CORNER2="$2"  # e.g. bottom-right (shift +X)
FOLDER_CORNER3="$3"  # e.g. top-left (shift +Z)
FOLDER_CORNER4="$4"  # e.g. top-right (shift +X +Z)
OUTPUT_BASE="$5"

if [ $# -ne 5 ]; then
  echo "Usage: $0 <corner1> <corner2> <corner3> <corner4> <output_base>"
  exit 1
fi

xhost +local:root

docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$FOLDER_CORNER1":/app/corner1 \
  -v "$FOLDER_CORNER2":/app/corner2 \
  -v "$FOLDER_CORNER3":/app/corner3 \
  -v "$FOLDER_CORNER4":/app/corner4 \
  -v "$OUTPUT_BASE":/app/output \
  open3d-merge bash -c "
    python main.py --folder1 /app/corner1 --folder2 /app/corner2 --shift 700 0 0 --destination /app/output/step1 &&
    python main.py --folder1 /app/output/step1 --folder2 /app/corner3 --shift 0 0 700 --destination /app/output/step2 &&
    python main.py --folder1 /app/output/step2 --folder2 /app/corner4 --shift 700 0 700 --destination /app/output/final_square
  "