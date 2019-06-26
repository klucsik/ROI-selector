__version__ = 'v0.1-dev'
import roi_select.cli
import roi_select.scanner
def main():
    """Entry point for running main ROI-select program.

    """
    # Parse the user-supplied CLI arguments.
    args = roi_select.cli.get_cli_parser().parse_args()
    # Create and initialize a new ScanContext using the supplied arguments.
    sctx = roi_select.scanner.GetROI(args)
    # If the context was successfully initialized, we can process the video(s).
    if sctx.initialized is True:
        sctx.get_ROI()

