import csv


def logfilestart():
    header = "filename, cases_count, timestamps"
    with open('submissions.csv', 'w', newline='') as file:
        file.write(header + '\n')


def logonefile(filename, timestamps, count):
    with open('submissions.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([filename, count, timestamps])

