rho =2
topics = ["fluids",]
input_file='output'
output_file = "output1"
out = open(output_file, "w");

with open(input_file, "r") as input1:
    for line in input1:
        if line != '\n':
            line = line.split("\t")
            potential =0
            for word in topics:
                count = line[0].count(word)
                level =int(line[2])
                if count > 0 and level >0:
                    potential += count*pow(rho,level )
            out.write( line[0] + "\t" + line[1] + "\t" + line[2] +
        "\t" + line[3] + "\t" + line[4] + "\t" + line[5][:-1] + "\t"+str(potential)+"\n")