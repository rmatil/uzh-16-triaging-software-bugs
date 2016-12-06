import csv
writer = csv.writer(open("Eclipse/cc_cleaned.csv", "wb")) 
reader = csv.reader(open("Eclipse/cc.csv", "rb"))
for row in reader:
	length_row = len(row)
	str = row[1]
	if length_row>4:
		for x in xrange(2,2+length_row-4):
			str = str + ',' + row[x].strip()
		row[1] = str
		row[2] = row[2+length_row-4]
		row[3] = row[3+length_row-4]
		del row[4-length_row]
	writer.writerow(row)
	