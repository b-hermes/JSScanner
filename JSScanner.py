import concurrent.futures
import requests
from concurrent import futures
import re
import urllib3
import os
import colored
from colored import stylize
import argparse  # Importing the argparse library

urllib3.disable_warnings()

# Setup argparse for command line arguments
parser = argparse.ArgumentParser(description="Tool for finding secrets in JS files using regex.")
parser.add_argument('-f', '--file', help="Path to the file containing URLs to scan", required=True)
parser.add_argument('-r', '--regex', help="Path to the regex/pattern file", required=True)
parser.add_argument('-o', '--output', help="Output file to save results", required=True)

args = parser.parse_args()

path = args.file
reg = args.regex
output_file = args.output

list = []
file1 = open(path, 'r')
Lines = file1.readlines()
count = 0

for line in Lines:
    ip = line.strip()
    print(stylize(ip, colored.fg("white")))
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(
                    lambda: requests.get(ip, verify=False))
                for _ in range(1)
            ]

            results = [
                f.result().text
                for f in futures
            ]

            file2 = open(reg, 'r')
            Lines2 = file2.readlines()
            for line2 in Lines2:
                regex = line2.strip()
                matches = re.finditer(regex, str(results), re.MULTILINE)
                for matchNum, match in enumerate(matches, start=1):
                    print(stylize("Regex: " + regex, colored.fg("green")))
                    print(stylize("Match {matchNum} was found at: {match}".format(matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()), colored.fg("red")))
                    with open(output_file, 'a') as f:
                        L = [ip, '\n', "Regex: ", regex, '\n', "Match {matchNum} was found at : {match}".format(matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()), '\n']
                        f.writelines(L)

    except requests.exceptions.RequestException as e:
        print("Error: {}".format(e))
