import sys
class ProgressBar():
    PROGRESS_BAR_LENGTH = float(50) 
    def __init__(self, end, start=0):  


        self.start = start
        self.end = end
        self.bar_length = self.PROGRESS_BAR_LENGTH
        self.setLevel(self.start) 
        self.plotted = False
    def setLevel(self, level, initial=False):  
                                            
        self.level = level
        if level < self.start:
            self.level = self.start
        if level > self.end:
            self.level = self.end
        self.ratio = float(self.level - self.start) / \
            float(self.end - self.start)
        self.level_string = int(self.ratio * self.bar_length)
    def drawProgress(self): # level이 설정된 만큼 그림을 그리는 함수
        sys.stdout.write("\r  %3i%% [%s%s]" % (
            int(self.ratio * 100.0),
            '#' * int(self.level_string),
            '-' * int(self.bar_length - self.level_string),
        ))
        sys.stdout.flush()
        self.plotted = True
    def setProgress(self, level):
        oldChars = self.level_string
        self.setLevel(level) 
        if (not self.plotted) or (oldChars != self.level_string):
            self.drawProgress() 
    def __del__(self): 
        sys.stdout.write("\n")
