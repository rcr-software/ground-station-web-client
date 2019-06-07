import sys

f = open('datastream', 'r')

while True:
    line = f.readline()
    if line != "":
        print(line, end='')
    else:
        break

#while True:
#    c = f.read(1)
#    if not c:
#        print('\n\nEOF')
#        break
#    print(c, end='')
#    sys.stdout.flush()
