import csv
import sys

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
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
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    labels = np.array(labels)
    predictions = np.array(predictions)
    actual_pos = np.sum(labels == 1) # n1
    pred_pos = np.sum((labels == 1) & (predictions == 1))
    sensitivity = pred_pos / actual_pos

    actual_neg = np.sum(labels == 0)  # n3
    pred_neg = np.sum((labels == 0) & (predictions == 0))

    specificity = pred_neg / actual_neg
    return sensitivity, specificity


if __name__ == "__main__":
    main()
