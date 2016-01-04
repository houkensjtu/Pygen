with open('source.dat','r') as source, open('target.dat','w') as target:
    count = 1
    for line in source:
        count += 1
        if count%2 == 0:
            target.write(line)
