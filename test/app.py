import os
import json
from clean import clean_transcript
from jiwer import wer
import csv


human_dir = "./human"
# results_dir = "./results"
results_dir = "./test"
total_accuracy = 0
total_confidence = 0
difference = 0

human_files = os.listdir(human_dir)
result_files = os.listdir(results_dir)
header = False


def calc_wer(truth, hypothesis):
    return round(wer(truth, hypothesis) * 100, 2)


def calc_accuracy(truth, hypothesis):
    error = wer(truth, hypothesis)

    return round(100 - (error * 100), 2)


def write_csv(results):
        csv_columns = ["File Name", "WER", "Accuracy"]
        csv_file = "results.csv"
        global header

        try:
            with open(csv_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                if header is False:
                    writer.writeheader()
                    header = True
                for result in results:
                    writer.writerow(result)
        except IOError:
            print("I/O error")


for x in range(0, 1):

    human_transcript = ""
    result_transcript = ""
    result_response = {}

    # reads files
    with open(os.path.join("human", human_files[x]), "r") as f:
        human_transcript = f.read()

    with open(os.path.join("results", result_files[x]), "r") as f:
        result_transcript = f.read()

    # convert results file to json
    with open(os.path.join("results", result_files[x])) as result_responses:
        result_response = json.load(result_responses)['results']['channels'][0]['alternatives'][0]

    result_text = result_response["transcript"]

    human_transcript = clean_transcript(human_transcript)
    result_transcript = clean_transcript(result_text)

    total_accuracy = total_accuracy + calc_accuracy(human_transcript, result_text)

    results = [
        {
            "File Name": human_files[x],
            "WER": calc_wer(human_transcript, result_text),
            "Accuracy": calc_accuracy(human_transcript, result_text)
        } 
    ]

    write_csv(results)

print("CSV's successfully created!")
