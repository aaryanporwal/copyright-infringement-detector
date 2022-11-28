import os
from math import ceil, sqrt
from typing import List

from PIL import Image
class MakeCollage:

    def __init__(
        self,
        image_list: List[str],
        output_path: str,
        collage_image_width: int = 1024,
    ) -> None:
       
        self.image_list = image_list
        self.number_of_images = len(self.image_list)
        self.output_path = output_path
        self.collage_image_width = collage_image_width

        self.images_per_row_in_collage = int(round(sqrt(self.number_of_images)))
        output_path_dir = os.path.dirname(self.output_path) + "/"
        self.make()

    def make(self) -> None:
        with Image.open(self.image_list[0]) as first_frame_image_in_list:
            frame_image_width, frame_image_height = first_frame_image_in_list.size

        scale = (self.collage_image_width) / (
            self.images_per_row_in_collage * frame_image_width
        )

        scaled_frame_image_width = ceil(frame_image_width * scale)
        scaled_frame_image_height = ceil(frame_image_height * scale)

        number_of_rows = ceil(self.number_of_images / self.images_per_row_in_collage)

        self.collage_image_height = ceil(scale * frame_image_height * number_of_rows)

        collage_image = Image.new(
            "RGB", (self.collage_image_width, self.collage_image_height)
        )

        i, j = (0, 0)

        for count, frame_path in enumerate(self.image_list):

            if (count % self.images_per_row_in_collage) == 0:
                i = 0
            frame = Image.open(frame_path)
            frame.thumbnail(
                (scaled_frame_image_width, scaled_frame_image_height), Image.ANTIALIAS
            )

            x = i
            y = (j // self.images_per_row_in_collage) * scaled_frame_image_height

            collage_image.paste(frame, (x, y))
            frame.close()

            i = i + scaled_frame_image_width
            j += 1

        collage_image.save(self.output_path, 'jpeg')
        collage_image.close()
