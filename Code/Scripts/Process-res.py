import csv

Final_deadline=[20,25,30,35,40]
variance = [1,2,3,4,5]
#variance = [5,6,7,8,9]

for deadline in Final_deadline:
    folder = ("Results/novar/"+str(deadline)+"/")
    filename = folder+"best_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"best_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])

    filename = folder+"chosen_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"chosen_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])

for deadline in Final_deadline:
    folder = ("Results/Dynamic/"+str(deadline)+"/")
    filename = folder+"best_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"best_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])
    filename = folder+"chosen_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"chosen_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])

for var in variance:
    for deadline in Final_deadline:
        folder = ("Results/Var/normal/"+str(deadline)+"/"+str(var)+"/")
        filename = folder+"best_path.csv"
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(open(folder+"best_path_proc.csv", "a+"))
            eps = []
            path = []
            for row in csv_reader:
                eps = row[0]
                path = row[1:]
                if(path == ['i','t']):
                    value = 0
                elif(path == ['i','i','t']):
                    value = 0
                elif(path == ['i','i','i','t']):
                    value = 0
                elif(path == ['i','x','t']):
                    value = 1
                elif(path == ['i','x','y','t']):
                    value = 2
                elif(path == ['i','x','z','t']):
                    value = 3
                else:
                    value = 9
                csv_writer.writerow([eps, value])
        filename = folder+"chosen_path.csv"
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(open(folder+"chosen_path_proc.csv", "a+"))
            eps = []
            path = []
            for row in csv_reader:
                eps = row[0]
                path = row[1:]
                if(path == ['i','t']):
                    value = 0
                elif(path == ['i','i','i','t']):
                    value = 0
                elif(path == ['i','x','t']):
                    value = 1
                elif(path == ['i','x','y','t']):
                    value = 2
                elif(path == ['i','x','z','t']):
                    value = 3
                else:
                    value = 9
                csv_writer.writerow([eps, value])

for var in variance:
    for deadline in Final_deadline:
        folder = ("Results/Var/uniform/"+str(deadline)+"/"+str(var)+"/")
        filename = folder+"best_path.csv"
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(open(folder+"best_path_proc.csv", "a+"))
            eps = []
            path = []
            for row in csv_reader:
                eps = row[0]
                path = row[1:]
                if(path == ['i','t']):
                    value = 0
                elif(path == ['i','i','t']):
                    value = 0
                elif(path == ['i','i','i','t']):
                    value = 0
                elif(path == ['i','x','t']):
                    value = 1
                elif(path == ['i','x','y','t']):
                    value = 2
                elif(path == ['i','x','z','t']):
                    value = 3
                else:
                    value = 9
                csv_writer.writerow([eps, value])
        filename = folder+"chosen_path.csv"
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_writer = csv.writer(open(folder+"chosen_path_proc.csv", "a+"))
            eps = []
            path = []
            for row in csv_reader:
                eps = row[0]
                path = row[1:]
                if(path == ['i','t']):
                    value = 0
                elif(path == ['i','i','i','t']):
                    value = 0
                elif(path == ['i','x','t']):
                    value = 1
                elif(path == ['i','x','y','t']):
                    value = 2
                elif(path == ['i','x','z','t']):
                    value = 3
                else:
                    value = 9
                csv_writer.writerow([eps, value])

for deadline in Final_deadline:
    folder = ("Results/uniform-wc/"+str(deadline)+"/")
    filename = folder+"best_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"best_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])
    filename = folder+"chosen_path.csv"
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_writer = csv.writer(open(folder+"chosen_path_proc.csv", "a+"))
        eps = []
        path = []
        for row in csv_reader:
            eps = row[0]
            path = row[1:]
            if(path == ['i','t']):
                value = 0
            elif(path == ['i','i','i','t']):
                value = 0
            elif(path == ['i','x','t']):
                value = 1
            elif(path == ['i','x','y','t']):
                value = 2
            elif(path == ['i','x','z','t']):
                value = 3
            else:
                value = 9
            csv_writer.writerow([eps, value])
