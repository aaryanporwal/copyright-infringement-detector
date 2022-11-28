import os
from subprocess import PIPE, Popen, check_output
import subprocess
import time

class FrameExtractor:
    def __init__(
        self,
        src_video: str,
        frames_output_dir: str,
    ) -> None:
        self.src_video = src_video
        self.frames_output_dir = frames_output_dir
        self.extract()
        #self.delete_all_frames()
        
    def extract(self):
        src_video = self.src_video
        frames_output_dir = self.frames_output_dir
        
        ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg.exe")
        path = os.path.join(os.getcwd(), frames_output_dir, "video_frame_%07d.jpeg")
        
        """
        ffpeg command arg description:
            -i: Input video
            -s: Size of output frames
            -r: Frame rate
        """
        command = "ffmpeg -i {src_video} -s 144x144 -r 1 {path}".format(src_video=src_video, path=path)

        subprocess.run(command, shell=True, check=True)

#  Delete all frames after calculating hashes
    def delete_all_frames(self):
        # wait 2 seconds
        time.sleep(5) # TODO: Remove this after completing hash calculation
        frames_output_dir = self.frames_output_dir
        for root, dirs, files in os.walk(frames_output_dir):
            for file in files:
                os.remove(os.path.join(root, file))
                