start = 5
stop = 10

rawFile = "in.txt"
filFile = "out.txt"

fin = open(rawFile,"r")
fout = open(filFile,"w")

rawData = fin.read()

splitData = rawData.splitlines(True)

fout.write(splitData[0])

for it in range(1,len(splitData)):
    line = splitData[it]
    vals = line.split()
    print(line)
    if float(vals[0]) >= start and float(vals[0]) <= stop:
        fout.write(line)
