output_file="DateFormatOutput"
input_file="DateFormatInput"
out = open(output_file, "w");

with open(input_file, "r") as input1:
    for line in input1:
        line = line.split(",")
        timestamp = line[4]
        time = timestamp.split(" ")
        Month = time[1]
        Day = time[2]
        Year = time[5]
        out.write ("%s,%s,%s,%s,%s-%s-%s" % (line[0], line[1], line[2], line[3], Month, Day, Year ))
