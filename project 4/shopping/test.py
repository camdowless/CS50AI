import csv


def load_data(filename):
    evidence = list()
    labels = list()

    with open(f"{filename}.csv", encoding="utf=8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            current_evidence = list()
            for c in row:
                if c != "Revenue":
                    if c == "Month":
                        months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'June': 6, 'Jul': 7, 'Aug': 8,
                                  'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
                        current_evidence.append(months.get(row[c]))
                    elif c == "VisitorType":
                        if row[c] == "Returning_Visitor":
                            current_evidence.append(1)
                        else:
                            current_evidence.append(0)
                    elif c == "Weekend":
                        if row[c] is True:
                            current_evidence.append(1)
                        else:
                            current_evidence.append(0)
                    else:
                        current_evidence.append(row[c])

                else:
                    if row[c] == "TRUE":
                        labels.append(1)
                    else:
                        labels.append(0)
            evidence.append(current_evidence)

        for i in range(0, len(evidence) - 1):
            print(evidence[i], labels[i])
load_data("test_data")