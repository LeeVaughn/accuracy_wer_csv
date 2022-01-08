import os
import json
from clean import clean_transcript
from jiwer import wer
import csv


human_dir = "./human"
results_dir = "./results"
human_files = os.listdir(human_dir)
result_files = os.listdir(results_dir)
header = False


def calc_wer(truth, hypothesis):
    return wer(truth, hypothesis)


def calc_accuracy(truth, hypothesis):
    error = wer(truth, hypothesis)

    return round(100 - (error * 100), 2)


def write_csv(results):
        csv_columns = ["File Name", "WER", "Accuracy %"]
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


# adjust the range based on the number of files being processed
for x in range(0, 596):

    human_transcript = ""
    result_transcript = ""
    result_response = {}
    total_accuracy = 0

    # reads files
    with open(os.path.join("human", human_files[x]), "r") as f:
        human_transcript = f.read()

    with open(os.path.join("results", result_files[x]), "r") as f:
        result_transcript = f.read()

    # # convert results file to json
    # with open(os.path.join("results", result_files[x])) as result_responses:
    #     result_response = json.load(result_responses)

    # result_text = result_transcript["text"]

    human_transcript = clean_transcript(human_transcript)
    result_transcript = clean_transcript(result_transcript)

    total_accuracy = total_accuracy + calc_accuracy(human_transcript, result_transcript)

    results = [
        {
            "File Name": human_files[x],
            "WER": calc_wer(human_transcript, result_transcript),
            "Accuracy %": calc_accuracy(human_transcript, result_transcript)
        } 
    ]

    write_csv(results)

print("CSV's successfully created!")
