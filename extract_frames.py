import os
from subprocess import PIPE, Popen, check_output

class FrameExtractor:
    def __init__(
        self,
        src_video: str,
        frames_output_dir: str,
    ) -> None:
        self.src_video = src_video
        self.frames_output_dir = frames_output_dir
        self.extract()
        
    def extract(self) -> None:
        """
        Extract the frames at every n seconds where n is the
        integer set to self.interval.

        :return: None

        :rtype: NoneType
        """

        ffmpeg_path = "/c/Users/abc/scoop/shims/ffmpeg.exe"
        src_video = self.src_video
        frames_output_dir = self.frames_output_dir
        
        # if os.name == "posix":
        #   ffmpeg_path = shlex.quote(self.ffmpeg_path)
        #   video_path = shlex.quote(self.video_path)
        #   output_dir = shlex.quote(self.output_dir)



        command = (
        f'"{ffmpeg_path}"'
        + " -i "
        + f'"{src_video}"'
        + " -s 144x144 "
        + "-r "
        + "1"
        + " "
        + '"'
        + frames_output_dir
        + "/frame-%07d.jpg"
        + '"'
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        ffmpeg_output = output.decode()
        ffmpeg_error = error.decode()

        # if len(os.listdir(self.frames_output_dir)) == 0:
        #     print("No frames extracted. Check the video path and try again.")
        #     print(f"FFmpeg could not extract any frames.{command}\n{ffmpeg_output}\n{ffmpeg_error}")
            