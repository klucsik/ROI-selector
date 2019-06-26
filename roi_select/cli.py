import argparse
import roi_select
def get_cli_parser():
    """Creates the ROI-select argparse command-line interface.

        Returns:
            ArgumentParser object, which parse_args() can be called with.
        """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = 'arguments'

    parser.add_argument(
        '-i', '--input', metavar='VIDEO_FILE',
        required=True, type=argparse.FileType('r'), action='append',
        help=('[REQUIRED] Path to input video.'
              ))

    parser.add_argument(
        '-st', '--start-time', metavar = 'time', dest = 'start_time',
        type = timecode_type_check('time'), default = None,
        help = ('Time to seek to in video before performing detection. Can be'
                ' given in number of frames (12345), seconds (number followed'
                ' by s, e.g. 123s or 123.45s), or timecode (HH:MM:SS[.nnn]).'))
    return parser

def timecode_type_check(metavar = None):
    """ Creates an argparse type for a user-inputted timecode.

    The passed argument is declared valid if it meets one of three valid forms:
      1) Standard timecode; in form HH:MM:SS or HH:MM:SS.nnn
      2) Number of seconds; type # of seconds, followed by s (e.g. 54s, 0.001s)
      3) Exact number of frames; type # of frames (e.g. 54, 1000)
     valid integer which
    is greater than or equal to min_val, and if max_val is specified,
    less than or equal to max_val.

    Returns:
        A function which can be passed as an argument type, when calling
        add_argument on an ArgumentParser object

    Raises:
        ArgumentTypeError: Passed argument must be integer within proper range.
    """
    metavar = 'value' if metavar is None else metavar
    def _type_checker(value):
        valid = False
        value = str(value).lower().strip()
        # Integer number of frames.
        if value.isdigit():
            # All characters in string are digits, just parse as integer.
            frames = int(value)
            if frames >= 0:
                valid = True
                value = frames
        # Integer or real/floating-point number of seconds.
        elif value.endswith('s'):
            secs = value[:-1]
            if secs.replace('.', '').isdigit():
                secs = float(secs)
                if secs >= 0.0:
                    valid = True
                    value = secs
        # Timecode in HH:MM:SS[.nnn] format.
        elif ':' in value:
            tc_val = value.split(':')
            if (len(tc_val) == 3 and tc_val[0].isdigit() and tc_val[1].isdigit()
                    and tc_val[2].replace('.', '').isdigit()):
                hrs, mins = int(tc_val[0]), int(tc_val[1])
                secs = float(tc_val[2]) if '.' in tc_val[2] else int(tc_val[2])
                if (hrs >= 0 and mins >= 0 and secs >= 0 and mins < 60
                        and secs < 60):
                    valid = True
                    value = [hrs, mins, secs]
        msg = ('invalid timecode: %s (timecode must conform to one of the'
               ' formats the dvr-scan --help message)' % value)
        if not valid:
            raise argparse.ArgumentTypeError(msg)
        return value
    return _type_checker