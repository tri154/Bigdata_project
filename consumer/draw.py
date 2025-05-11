import numpy as np
from collections import defaultdict
import cv2

print('I am in the draw')
fps = 10
x_min_world = -30
y_min_world = -30
scale = 20
width = 800
height = 800

existed_colors = [(0, 0, 0)]
object_paths = defaultdict(list)
color_map = {}

previous_objects = set()
missed_objects = set()

# debug
# video_path = "object_tracking_output_opencv.mp4"
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video_writer = cv2.VideoWriter(video_path, fourcc, fps, (width, height))


def world_to_image(x_world, y_world):
    x_img = int((x_world - x_min_world) * scale)
    y_img = int((y_world - y_min_world) * scale)
    y_img = height - y_img  # Flip y-axis to match top-down image
    return x_img, y_img

def get_color(object_id, color_map, existed_colors):
    if object_id not in color_map:
        rand_color = (
            np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        while rand_color in existed_colors:
            rand_color = (
                np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        color_map[object_id] = rand_color
        existed_colors.append(rand_color)
    return color_map[object_id]

path_only_frame = np.ones((height, width, 3), dtype=np.uint8) * 255

def draw_image(data_array):
    global path_only_frame, previous_objects, missed_objects
    processing_frame = path_only_frame.copy()

    for arr in data_array:
        object_id = arr[1]
        x_world = arr[-3]
        y_world = arr[-2]
        x_img, y_img = world_to_image(x_world, y_world)
        color = get_color(object_id, color_map, existed_colors)

        if len(object_paths[object_id]) == 0:
            object_paths[object_id].append((x_img, y_img))
            continue
        previous_position = object_paths[object_id][-1]

        if object_id not in missed_objects:
            cv2.line(processing_frame, previous_position, (x_img, y_img), color, 2)
        else:
            missed_objects.remove(object_id)
        object_paths[object_id].append((x_img, y_img))

    current_objects = set(data_array[:, 1])
    miss_tracked_objects = previous_objects - current_objects
    missed_objects = missed_objects | miss_tracked_objects
    # process missing object.
    for miss_object in miss_tracked_objects:
        last_position = object_paths[miss_object][-1]
        # add text to it
        cv2.putText(
            processing_frame,
            f"(lost)",
            (last_position[0], last_position[1]),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.25,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
    path_only_frame = processing_frame.copy()

    for arr in data_array:
        object_id = arr[1]
        x_world = arr[-3]
        y_world = arr[-2]
        x_img, y_img = world_to_image(x_world, y_world)
        color = get_color(object_id, color_map, existed_colors)
        cv2.circle(img=processing_frame, center=(x_img, y_img), radius=5, color=color, thickness=-1)

    # put text
    for arr in data_array:
        object_id = arr[1]
        x_world = arr[-3]
        y_world = arr[-2]
        x_img, y_img = world_to_image(x_world, y_world)
        color = get_color(object_id, color_map, existed_colors)
        cv2.putText(
            processing_frame,
            f"{object_id}",
            (x_img, y_img - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            1,
            cv2.LINE_AA,
        )

    previous_objects = current_objects
    #debug
    # video_writer.write(processing_frame)
    return processing_frame


