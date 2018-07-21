from progressbar import ProgressBar

import time,sys

progress = 0

def main():
    pb = ProgressBar(100)
    global progress
    while progress != 101:
        progress += 1
        pb.setProgress(progress)
        time.sleep(0.1)

if __name__ == "__main__":
    sys.exit(main())
