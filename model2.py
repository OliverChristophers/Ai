import os


o = open(os.path.realpath(rf'new_generated_data.txt'), 'r').read()

s = open(os.path.realpath(rf'structured_g_data.txt'), 'r').read()

with open(os.path.realpath(rf'new.txt'), 'a') as f:
    for line in o:
        f.write(line)
    f.write('\n')
    for line in s:
        f.write(line)
