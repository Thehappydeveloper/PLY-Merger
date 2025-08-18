# Dual 8i PLY Video Merger

This repository provides a workflow for merging two sequences of PLY point cloud frames (such as 8i Voxelized Full Bodies) into a single dataset using [Open3D](http://www.open3d.org/). It supports optional shifting, downsampling, and visualization.

---

## Features

- **Merge two PLY video folders** frame-by-frame into a new sequence.
- **Shift** the second sequence in 3D space.
- **Downsample** point clouds to a fixed number of points per frame.
- **Visualize** the merged result for the first frame (optional).
- **Pause** after the first frame for inspection (optional).
- **Dockerized** for easy, reproducible setup with GUI support.

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/) (recommended)
- Or: Python 3.8+, [Open3D](https://pypi.org/project/open3d/), numpy, tqdm

---

## Quick Start (Docker, Generic Linux)

### 1. Build the Docker Image

```bash
docker build -t open3d-merge .
```

### 2. Run the Merger

Replace the folder paths as needed:

```bash
xhost +local:root
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v '/home/youruser/ply_folder1':/app/folder1 \
  -v '/home/youruser/ply_folder2':/app/folder2 \
  -v '/home/youruser/output_folder':/app/output \
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

---

## License

This software is **closed source** and intended for internal use only by the IN2GM laboratory.
Redistribution or use outside IN2GM is not permitted.