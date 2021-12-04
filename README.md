# ixigua_scraper
Download all videos under creator's homepage of XIGUA Video(西瓜视频)

1. Retrieve video list by ```python get_creator_video_list.py```
   Modify variables in ```CREATOR_HOME_URL, SAVE_LIST_FILE``` before run
2. Download videos from list by ```python download_video_from_list.py```
   Modify variables in ```DOWNLOAD_FOLDER, NUM_PROC, LIST_FILE``` before download