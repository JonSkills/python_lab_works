fin = open('C:\\Users\\user\\Desktop\\LEC-PRAC\\3 course\\PYTHON 3# course\\6 apta\\mailbox.txt', 'r')
lines = fin.readlines()

fout = open('C:\\Users\\user\\Desktop\\LEC-PRAC\\3 course\\PYTHON 3# course\\6 apta\\mailbox_output.txt', 'w')

name_list = []

for line in lines:
    if line.startswith('From:'):
        newline = line.split("@")[0].split()[1]
        if newline not in name_list:
            name_list.append(newline)
            fout.write(newline + "\n")


name_list.sort()
print(name_list)
fin.close()
fout.close()


