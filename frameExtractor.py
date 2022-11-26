import os

class FrameExtractor:
    def __init__(
        self,
        video_path: str,
        output_dir: str,
        ffmpeg_path: Optional[str] = None,
    ) -> None:
    def extract(self) -> None:
        """
        Extract the frames at every n seconds where n is the
        integer set to self.interval.

        :return: None

        :rtype: NoneType
        """

        ffmpeg_path = self.ffmpeg_path
        video_path = self.video_path
        output_dir = self.output_dir

        # if os.name == "posix":
        #   ffmpeg_path = shlex.quote(self.ffmpeg_path)
        #   video_path = shlex.quote(self.video_path)
        #   output_dir = shlex.quote(self.output_dir)



        command = (
        f'"{ffmpeg_path}"'
        + " -i "
        + f'"{video_path}"'
        + " -s 144x144 "
        + " -r "
        + "1"
        + " "
        + '"'
        + output_dir
        + "video_frame_%07d.jpeg"
        + '"'
        )

        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = process.communicate()

        ffmpeg_output = output.decode()
        ffmpeg_error = error.decode()

        if len(os.listdir(self.output_dir)) == 0:

            raise FFmpegFailedToExtractFrames(
                f"FFmpeg could not extract any frames.\n{command}\n{ffmpeg_output}\n{ffmpeg_error}"
            )
