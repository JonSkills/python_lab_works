fin = open('C:\\Users\\user\\Desktop\\LEC-PRAC\\3 course\\PYTHON 3# course\\6 apta\\mailbox.txt', 'r')
lines = fin.readlines()

count = 0
countf = 0

for line in lines:
    if line.startswith('Received:'):
        count+= 1
    elif line.startswith('From:'):
        countf+= 1

print("Number of lines starting with 'Received:':", count, "\nNumber of lines starting with 'From:':", countf)


fin.close()




