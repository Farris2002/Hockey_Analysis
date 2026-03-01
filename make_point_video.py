"""Create a simple video showing points per time on a white background.

Usage:
    python make_point_video.py --csv data.csv --output out.mp4 --xmin 0 --xmax 100 --ymin 0 --ymax 85

This writes one frame per unique `time` value in the CSV. Requires `opencv-python` and `pandas`.
"""
from __future__ import annotations

import argparse
import sys
from typing import Tuple

import numpy as np
import pandas as pd

try:
    import cv2
except Exception as e:  # pragma: no cover - runtime dependency
    raise ImportError("opencv-python is required (pip install opencv-python)") from e


def df_to_video(
    df: pd.DataFrame,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    output: str,
    fps: int = 30,
    size: Tuple[int, int] = (800, 600),
    radius: int = 3,
    Hcolor: Tuple[int, int, int] = (0, 0, 255),
    Acolor: Tuple[int, int, int] = (255,0,0),
    Pcolor: Tuple[int, int, int] = (0, 0, 0),
    bgcolor: Tuple[int, int, int] = (255, 255, 255),
) -> None:
    """Write a video with one frame per unique `time` in `df`.

    df must contain columns `x`, `y`, and `time`.
    Coordinates outside the given bounds are ignored.
    """
    width, height = size
    if xmax == xmin or ymax == ymin:
        raise ValueError("Invalid bounds: xmin!=xmax and ymin!=ymax required")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output, fourcc, float(fps), (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Failed to open video writer for '{output}'")

    times = sorted(pd.unique(df["time"]))

    for t in times:
        frame = np.full((height, width, 3), bgcolor, dtype=np.uint8)
        subset = df[df["time"] == t][["x", "y", "player_id"]].dropna()
        for _, row in subset.iterrows():
            x = row["x"]
            y = row["y"]
            player_id = row["player_id"] 
            # Determine color based on player_id prefix
            if isinstance(player_id, str):
                if player_id.startswith("H"):
                    color = Hcolor
                elif player_id.startswith("A"):
                    color = Acolor 
                elif player_id.startswith("P"):
                    color = Pcolor
                else:
                    color = (0,255,0)
            else:
                color = (0,255,0)
            
            # Go from starting in the center of the 200 by 100 grid to 
            # starting at the top left.
            x += 100
            y += 50
            # Now convert from 200 x 100 to 800 x 400 by x = x * W_new / W_old
            try:
                px = int(round(4 * x))
                py = int(round(4 * y))
            except Exception:
                continue

            if 0 <= px < width and 0 <= py < height:
                cv2.circle(frame, (px, py), radius, color, -1, lineType=cv2.LINE_AA)

        writer.write(frame)

    writer.release()

"""
def _parse_args(argv):
    p = argparse.ArgumentParser(description="Create a point-location video from CSV")
    p.add_argument("--csv", required=True, help="CSV file with columns x,y,time")
    p.add_argument("--output", required=True, help="Output MP4 file")
    p.add_argument("--xmin", type=float, required=True)
    p.add_argument("--xmax", type=float, required=True)
    p.add_argument("--ymin", type=float, required=True)
    p.add_argument("--ymax", type=float, required=True)
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--width", type=int, default=800)
    p.add_argument("--height", type=int, default=600)
    p.add_argument("--radius", type=int, default=5)
    p.add_argument("--color", type=str, default="0,0,255", help="B,G,R comma-separated")
    return p.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = _parse_args(argv)
    df = pd.read_csv(args.csv)
    if not {"x", "y", "time"}.issubset(df.columns):
        raise ValueError("CSV must contain columns: x, y, time")
    color = tuple(int(c) for c in args.color.split(","))
    df_to_video(
        df,
        args.xmin,
        args.xmax,
        args.ymin,
        args.ymax,
        args.output,
        fps=args.fps,
        size=(args.width, args.height),
        radius=args.radius,
        color=color,
    )


if __name__ == "__main__":
    main()


"""

df = pd.read_csv("data_files/cleaned/2024-10-25.Team.H.@.Team.G.-.Tracking_CLEAN.csv")


xmin = min(df["x"])
xmax = max(df["x"])
ymin = min(df["y"])
ymax = max(df["y"])
#df = df.drop_duplicates(subset=['player_id', 'time'], keep='first')
df_to_video(df,xmin,xmax,ymin,ymax,"video2.mp4",fps = 30)