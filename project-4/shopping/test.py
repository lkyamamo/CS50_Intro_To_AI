import csv
filename = 'shopping.csv'

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
        print("{0} {1}".format(temp, revenue))

print("{0} {1}".format(evidence[0], labels[0]))