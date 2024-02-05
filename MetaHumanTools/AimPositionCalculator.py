import numpy as np
import pandas as pd

LEFT_EYE_POS = np.array([3.044442, 8.057392, 149.135620])
LEFT_AIM_ORIGIN = np.array([3.107691, 30.000000, 149.142349])

RIGHT_EYE_POS = np.array([3.045077, 8.035566, 149.161366])
RIGHT_AIM_ORIGIN = np.array([3.108326, 30.000000, 149.154637])

HORIZONTAL_RANGE = 120
VERTICAL_RANGE = 70
STEP = 5

ROUNDED_DECIMALS = 5
OUTPUT_FILE = "gaze_dataset.csv"

def aim_box_transition_from_gaze(eye_pos: np.array, aim_origin: np.array, gaze: np.array):
    # project gaze onto the aim box plane
    gaze_y = gaze[1]
    aim_box_dist = aim_origin[1] - eye_pos[1]
    gaze_projected = gaze * (aim_box_dist / gaze_y)
    return np.flip(gaze_projected + eye_pos - aim_origin)

def aim_box_transition_from_angle(eye_pos: np.array, aim_origin: np.array, horizontal: float=0, vertical:float = 0):
    aim_box_dist = aim_origin[1] - eye_pos[1]
    delta_x = np.tan(np.deg2rad(-horizontal)) * aim_box_dist
    delta_z = np.tan(np.deg2rad(vertical)) * aim_box_dist
    return np.flip(np.array([delta_x, 0, delta_z]))

def gaze_from_transition(eye_pos: np.array, aim_origin: np.array, aim_transition: np.array):
    gaze = aim_origin + np.flip(aim_transition) - eye_pos
    return gaze / np.linalg.norm(gaze, ord=1)

if __name__ == '__main__':
    print(aim_box_transition_from_gaze(LEFT_EYE_POS, LEFT_AIM_ORIGIN, np.array([10.063249, 21.942608, 0.006729])))
    print(aim_box_transition_from_gaze(LEFT_EYE_POS, LEFT_AIM_ORIGIN, np.array([10.063249, 21.942608, -4.9932])))
    print(aim_box_transition_from_angle(LEFT_EYE_POS, LEFT_AIM_ORIGIN, horizontal=30, vertical=35))

    eye_pos_avg = LEFT_EYE_POS + RIGHT_EYE_POS / 2
    aim_origin_avg = LEFT_AIM_ORIGIN + RIGHT_AIM_ORIGIN / 2

    horizontal_angles = np.arange(start=-HORIZONTAL_RANGE / 2, stop=HORIZONTAL_RANGE/2 + STEP, step=STEP)
    vertical_angles = np.arange(start=-VERTICAL_RANGE / 2, stop=VERTICAL_RANGE/2 + STEP, step=STEP)
    print(vertical_angles)

    data = []
    index = 0
    for h_angle in horizontal_angles:
        for v_angle in vertical_angles:
            transition = aim_box_transition_from_angle(eye_pos_avg, aim_origin_avg, h_angle, v_angle)
            gaze_vector = gaze_from_transition(eye_pos_avg, aim_origin_avg, transition)
            print("{} horizontal, {} vertical, {} gaze: {}".format(str(h_angle), str(v_angle), str(gaze_vector), str(transition)))
            #   [index, horizontal angle, vertical angle, gaze x, gaze y, gaze z, aim x, aim y, aim z]
            transition = np.round(transition, decimals=ROUNDED_DECIMALS)
            gaze_vector = np.round(gaze_vector, decimals=ROUNDED_DECIMALS)
            entry = [h_angle, v_angle, gaze_vector[0], gaze_vector[1], gaze_vector[2], transition[0], transition[1], transition[2]]
            data.append(entry)
            index += 1
    print(data)
    data_df = pd.DataFrame(np.array(data), columns=["horizontal angle", "vertical angle", "gaze x", "gaze y", "gaze z", "aim x", "aim y", "aim z"])
    data_df.to_csv(OUTPUT_FILE)

