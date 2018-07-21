import csv_splitter
import sys
import os

def main(path):
    filePath = path
    csv_splitter.split(open(filePath, 'r'), ',', 300000, 'youtube_%s.csv', './output/', True)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
