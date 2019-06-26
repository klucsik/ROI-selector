import os

# Third-Party Library Imports
from roi_select.timecode import FrameTimecode
import cv2


class GetROI(object):
    """ The ScanContext object represents the DVR-Scan program state,
    which includes application initialization, handling the options,
    and coordinating overall application logic (via scan_motion()). """

    def __init__(self, args):
        """ Initializes the ScanContext with the supplied arguments. """

        self.roi = None
        self.event_list = []

        self.frames_read = -1
        self.frames_processed = -1
        self._cap = None
        self._cap_path = None

        self.video_resolution = None
        self.start_time = args.start_time


        self.video_paths = [input_file.name for input_file in args.input]
        # We close the open file handles, as only the paths are required.
        for input_file in args.input:
            input_file.close()


        self.initialized = True

    def _get_next_frame(self, retrieve = True):
        """ Returns a new frame from the current series of video files,
        or None when no more frames are available. """
        if self._cap:
            if retrieve:
                (ret_val, frame) = self._cap.read()
            else:
                ret_val = self._cap.grab()
                frame = True
            if ret_val:
                return frame
            else:
                self._cap.release()
                self._cap = None

        if self._cap is None and len(self.video_paths) > 0:
            self._cap_path = self.video_paths[0]
            self.video_paths = self.video_paths[1:]
            self._cap = cv2.VideoCapture(self._cap_path)
            if self._cap.isOpened():
                return self._get_next_frame()
            else:
                print("[DVR-Scan] Error: Unable to load video for processing.")
                self._cap = None

        return None

    def _stampText(self, frame, text, line):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        margin = 5
        thickness = 2
        color = (255, 255, 255)

        size = cv2.getTextSize(text, font, font_scale, thickness)

        text_width = size[0][0]
        text_height = size[0][1]
        line_height = text_height + size[1] + margin

        x = margin
        y = margin + size[0][1] + line * line_height
        cv2.rectangle(frame, (margin, margin), (margin+text_width, margin+text_height+2), (0, 0, 0), -1)
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        return None

    def get_ROI(self):




        for video_path in self.video_paths:
            cap = cv2.VideoCapture()
            cap.open(video_path)
            video_name = os.path.basename(video_path)
            self.video_fps = cap.get(cv2.CAP_PROP_FPS)
            curr_resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.video_resolution = curr_resolution
            if self.start_time is not None:
                self.start_time = FrameTimecode(self.video_fps, self.start_time)
            print("[ROI-select] Opened video %s (%d x %d at %2.3f FPS)." % (
                video_name, self.video_resolution[0],
                self.video_resolution[1], self.video_fps))

        curr_pos = FrameTimecode(self.video_fps, 0)
        num_frames_read = 0


        # Seek to starting position if required.
        if self.start_time is not None:
            while curr_pos.frame_num < self.start_time.frame_num:
                if self._get_next_frame() is None:
                    break
                num_frames_read += 1
                curr_pos.frame_num += 1

        # area selection
        print("[ROI-select] selecting area of interest:")
        frame_for_crop = self._get_next_frame()

        self._stampText(frame_for_crop, curr_pos.get_timecode(), 0)
        self.roi = cv2.selectROI("Image", frame_for_crop)
        cv2.destroyAllWindows()
        print("[ROI-select] area selected.")
        print("[ROI-select] area selected(x,y,w,h): " + str(self.roi))
        print('[ROI-select] command line code snippet: -roi ' + str(self.roi[0]) + " " + str(self.roi[1]) + " " + str(self.roi[2]) + " " + str(self.roi[3]))
        return

