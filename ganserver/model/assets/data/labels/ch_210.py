with open('210.txt', 'r') as rf:
    data = rf.read().split()

with open('210-cp.txt', 'w', encoding='utf-8') as wf:
    for i in data:
        wf.write(i)
        wf.write('\n')