from collections import defaultdict
from videoprops import get_video_properties
import glob
import tqdm
import os

fs = glob.glob('D:\\Colorful\\*.mp4')
dims = defaultdict(list)
for f in tqdm.tqdm(fs):
    props = get_video_properties(f)
    res = f"Resolution: {props['width']}×{props['height']}"
    dims[res].append(f.split('.')[0])
    if res != 'Resolution: 1920×1080':
        os.remove(f)
        print(f)
for k, v in dims.items():
    print(k, len(v))

