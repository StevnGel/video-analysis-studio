#!/usr/bin/env python3
import os
import subprocess

OUTPUT_DIR = "/Users/zengwenhua/py_workspace/video-analysis-studio/data/videos"

TRAFFIC_VIDEO_URLS = [
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4", "Big Buck Bunny"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_2mb.mp4", "Big Buck Bunny 2"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_5mb.mp4", "Big Buck Bunny 5"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_10mb.mp4", "Big Buck Bunny 10"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_20mb.mp4", "Big Buck Bunny 20"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_30mb.mp4", "Big Buck Bunny 30"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_50mb.mp4", "Big Buck Bunny 50"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_80mb.mp4", "Big Buck Bunny 80"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_100mb.mp4", "Big Buck Bunny 100"),
    ("https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_200mb.mp4", "Big Buck Bunny 200"),
]

def download_video(url, output_path, name):
    try:
        print(f"Downloading: {name}")
        result = subprocess.run(
            ["curl", "-L", "-o", output_path, "--retry", "3", "--connect-timeout", "30", url],
            capture_output=True,
            timeout=300
        )
        
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            if size > 10000:
                print(f"  Success! ({size / 1024 / 1024:.1f} MB)")
                return True
            else:
                os.remove(output_path)
                return False
        return False
    except Exception as e:
        print(f"  Error: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    downloaded = 0
    for i, (url, name) in enumerate(TRAFFIC_VIDEO_URLS):
        if downloaded >= 10:
            break
            
        output_file = os.path.join(OUTPUT_DIR, f"traffic_video_{downloaded + 1}.mp4")
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 10000:
            print(f"  [{downloaded + 1}] Already exists, skipping")
            downloaded += 1
            continue
            
        if download_video(url, output_file, name):
            downloaded += 1
        else:
            print(f"  Failed!")
    
    print(f"\n\nTotal downloaded: {downloaded}")

if __name__ == "__main__":
    main()
