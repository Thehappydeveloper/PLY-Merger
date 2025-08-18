import argparse
import os
import re
import open3d as o3d
import numpy as np
import logging
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description="Merge two 8i PLY videos into a single dataset.")
    parser.add_argument("--folder1", type=str, required=True, help="Path to first video folder")
    parser.add_argument("--folder2", type=str, required=True, help="Path to second video folder")
    parser.add_argument("--shift", type=float, nargs=3, default=[0.0, 0.0, 0.0],
                        help="Shift for second video [x y z]")
    parser.add_argument("--max_frames", type=int, default=None, help="Maximum number of frames to merge")
    parser.add_argument("--downsample", type=int, default=None, help="Number of points per frame")
    parser.add_argument("--destination", type=str, required=True, help="Destination folder for merged frames")
    parser.add_argument("--verbose", action="store_true", help="Visualize merged frames")
    parser.add_argument("--pause_first", action="store_true", help="Pause on first frame for user input")
    return parser.parse_args()

def sorted_ply_files(folder):
    # Extract numeric suffix for sorting
    ply_files = [f for f in os.listdir(folder) if f.endswith(".ply")]
    if not ply_files:
        logging.warning(f"No PLY files found in folder: {folder}")
        return []
    def get_index(f):
        match = re.search(r'_(\d+)\.ply$', f)
        return int(match.group(1)) if match else -1
    return sorted([os.path.join(folder, f) for f in ply_files], key=get_index)

def get_first_word(filename):
    return os.path.basename(filename).split("_")[0]

def downsample_pcd(pcd, num_points):
    points = np.asarray(pcd.points)
    if len(points) <= num_points:
        return pcd
    idx = np.random.choice(len(points), num_points, replace=False)
    down_pcd = o3d.geometry.PointCloud()
    down_pcd.points = o3d.utility.Vector3dVector(points[idx])
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)
        down_pcd.colors = o3d.utility.Vector3dVector(colors[idx])
    return down_pcd

def merge_videos(args):
    folder1_files = sorted_ply_files(args.folder1)
    folder2_files = sorted_ply_files(args.folder2)

    if not folder1_files or not folder2_files:
        logging.error("One or both folders have no PLY files. Exiting.")
        return

    total_frames = min(len(folder1_files), len(folder2_files))
    if args.max_frames:
        total_frames = min(total_frames, args.max_frames)

    os.makedirs(args.destination, exist_ok=True)
    logging.info(f"Starting merge: {total_frames} frames will be processed.")

    pause_done = False
    visualized = False  # Track if visualization has been shown
    for i in tqdm(range(total_frames), desc="Merging frames"):
        try:
            pcd1 = o3d.io.read_point_cloud(folder1_files[i])
            pcd2 = o3d.io.read_point_cloud(folder2_files[i])
        except Exception as e:
            logging.warning(f"Skipping frame {i} due to read error: {e}")
            continue

        # Shift second PLY
        shift_vec = np.array(args.shift, dtype=np.float64)
        points2 = np.asarray(pcd2.points) + shift_vec
        pcd2.points = o3d.utility.Vector3dVector(points2)

        # Downsample
        if args.downsample:
            pcd1 = downsample_pcd(pcd1, args.downsample)
            pcd2 = downsample_pcd(pcd2, args.downsample)

        # Merge
        merged = pcd1 + pcd2

        # Output filename
        name1 = get_first_word(folder1_files[i])
        name2 = get_first_word(folder2_files[i])
        out_filename = os.path.join(args.destination, f"{name1}_{name2}_{i+1:04d}.ply")
        o3d.io.write_point_cloud(out_filename, merged)

        # Show visualization only for the first frame if verbose is set
        if args.verbose and not visualized:
            o3d.visualization.draw_geometries([merged])
            visualized = True

        # Pause first frame if requested
        if args.pause_first and not pause_done:
            print(f"Paused on first frame: {out_filename}")
            ans = input("Continue processing? (y/n): ").strip().lower()
            if ans != "y":
                print("Exiting process.")
                break
            pause_done = True

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_args()
    merge_videos(args)
