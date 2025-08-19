# Dual PLY Video Merger

This repository provides a workflow for merging sequences of PLY point cloud frames (such as 8i Voxelized Full Bodies) into a single dataset using [Open3D](http://www.open3d.org/). It supports optional shifting, downsampling, and visualization.  
A special script is provided to merge **four point cloud folders into a square layout** using Docker.

---

## Features

- **Merge two or more PLY video folders** frame-by-frame into a new sequence.
- **Shift** each sequence in 3D space.
- **Visualize** the merged result for the first frame (optional).
- **Pause** after the first frame for inspection (optional).
- **Dockerized** for easy, reproducible setup with GUI support.
- **Automated square merge** for four PLY folders.

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (recommended)
- Or: Python 3.8+, [Open3D](https://pypi.org/project/open3d/), numpy, tqdm

---

## Quick Start: Merging Four PLY Folders into a Square

### 1. Build the Docker Image

```bash
docker build -t open3d-merge .
```

### 2. Prepare Your Data

Organize your four PLY folders so that each represents a corner of the square:

- **Corner 1:** bottom-left (no shift)
- **Corner 2:** bottom-right (shift +X)
- **Corner 3:** top-left (shift +Z)
- **Corner 4:** top-right (shift +X +Z)

### 3. Run the Automated Merge Script

```bash
chmod +x run_merge_all.sh
./run_merge_all.sh "/absolute/path/to/corner1" "/absolute/path/to/corner2" "/absolute/path/to/corner3" "/absolute/path/to/corner4" "/absolute/path/to/output"
```

**Example:**
```bash
./run_merge_all.sh "/data/ply_corner1" "/data/ply_corner2" "/data/ply_corner3" "/data/ply_corner4" "/data/merged_square_output"
```

This will:
- Merge corner1 and corner2 with a shift on X (`+700`)
- Merge the result with corner3 with a shift on Z (`+700`)
- Merge the result with corner4 with a shift on X and Z (`+700 +700`)
- The final merged square will be in `/data/merged_square_output/final_square`

**Note:** Adjust the shift values in `run_merge_all.sh` if your square size is different.

---

## Manual Usage (Two Folders)

You can also merge two folders manually:

```bash
xhost +local:root
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v '/data/ply_folder1':/app/folder1 \
  -v '/data/ply_folder2':/app/folder2 \
  -v '/data/output_folder':/app/output \
  open3d-merge \
  bash -c "./run.sh \
    --folder1 /app/folder1 \
    --folder2 /app/folder2 \
    --destination /app/output \
    --shift 700 0 0 \
    --max_frames 100 \
    --downsample 100000 \
    --verbose \
    --pause_first"
```

---

## Script Arguments

| Argument         | Description                                      | Example                        |
|------------------|--------------------------------------------------|--------------------------------|
| `--folder1`      | Path to first PLY video folder                   | `/data/ply1`                   |
| `--folder2`      | Path to second PLY video folder                  | `/data/ply2`                   |
| `--destination`  | Output folder for merged frames                  | `/data/merged`                 |
| `--shift`        | Shift `[x y z]` for second video (default: 0 0 0)| `700 0 0`                      |
| `--max_frames`   | Maximum frames to process                        | `100`                          |
| `--downsample`   | Downsample to N points per frame                 | `100000`                       |
| `--verbose`      | Visualize merged frame (first frame only)        | *(flag)*                       |
| `--pause_first`  | Pause after first frame for inspection           | *(flag)*                       |

---

## Example Output

- Merged PLY files will be saved in the destination folder, named as:  
  `<name1>_<name2>_<frame_number>.ply`

---

## Notes

- The script only visualizes the **first merged frame** if `--verbose` is set.
- If `--pause_first` is set, the script will pause after the first frame for user confirmation.
- Make sure your PLY files are named with a numeric suffix (e.g., `model_0001.ply`) for correct ordering.
- The automated merge script (`run_merge_all.sh`) is designed for four folders to be merged into a square.

---

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
