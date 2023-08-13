import csv
import sys

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
        - Administrative, an integer 0
        - Administrative_Duration, a floating point number 1
        - Informational, an integer 2
        - Informational_Duration, a floating point number 3
        - ProductRelated, an integer 4
        - ProductRelated_Duration, a floating point number 5
        - BounceRates, a floating point number 6
        - ExitRates, a floating point number 7
        - PageValues, a floating point number 8
        - SpecialDay, a floating point number 9
        - Month, an index from 0 (January) to 11 (December) 10
        - OperatingSystems, an integer 11
        - Browser, an integer 12
        - Region, an integer 13
        - TrafficType, an integer 14 
        - VisitorType, an integer 0 (not returning) or 1 (returning) 15
        - Weekend, an integer 0 (if false) or 1 (if true) 16 

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    month_mapping = {'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}

    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')

        #skip labels
        next(reader)

        #each line get values
        for row in reader:
            temp = row
            revenue = temp.pop()

            #convert each element
            temp[0] = int(temp[0])
            temp[1] = float(temp[1])
            temp[2] = int(temp[2])
            temp[3] = float(temp[3])
            temp[4] = int(temp[4])
            temp[5] = float(temp[5])
            temp[6] = float(temp[6])
            temp[7] = float(temp[7])
            temp[8] = float(temp[8])
            temp[9] = float(temp[9])
            temp[10] = month_mapping[temp[10]]
            temp[11] = int(temp[11])
            temp[12] = int(temp[12])
            temp[13] = int(temp[13])
            temp[14] = int(temp[14])

            if temp[15] == 'Returning_Visitor':
                temp[15] = 1
            else:
                temp[15] = 0

            if temp[16] == 'TRUE':
                temp[16] = 1
            else:
                temp[16] = 0

            evidence.append(temp)

            if revenue == 'TRUE':
                revenue = 1
            else:
                revenue = 0
            
            labels.append(revenue)

    return((evidence, labels))

    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)

    return model

    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity_count = 0
    specificity_count = 0

    sensitivity_correct = 0
    specificity_correct = 0

    # count total of sensitivity and specificity and coutn total correct for each
    for i in range(len(labels)):

        #add to sensitivity
        if labels[i] == 1:
            sensitivity_count += 1

            #if match then add to correct count
            if predictions[i] == 1:
                sensitivity_correct += 1

        else:
            specificity_count += 1

            if predictions[i] == 0:
                specificity_correct += 1

    #print((sensitivity_correct/sensitivity_count, specificity_correct/specificity_count))

    return (sensitivity_correct/sensitivity_count, specificity_correct/specificity_count)

    raise NotImplementedError


if __name__ == "__main__":
    main()
