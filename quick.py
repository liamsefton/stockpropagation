f = open("stock_data.txt", "r")



#dirty data purifier
new_f  = open("training.txt", "a")
for line in f:
    if len(line.split(",")) > 25 or len(line.split(",")) < 25:
        pass
    else:
        line_split = line.split(",")
        valid_line = True
        for i in range(len(line_split)):
            line_split[i] = line_split[i].strip("0")
            line_split[i] = line_split[i].strip(".")
            if line_split[i] == " " or line_split[i] == "":
                valid_line = False
        line = ""
        for num in line_split:
            line += num + ","
        line = line[:-1]
        if line[0].isnumeric() and valid_line:
            new_f.write(line)

new_f.close()