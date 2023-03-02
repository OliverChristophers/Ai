import os, json

def stringlist_to_list(list_as_string):
    list_as_list = json.loads(list_as_string)
    return list_as_list


n_bookmakers = 7
n_outcomes = 3

f = open(os.path.realpath(rf'generated_data.txt'), 'r').read()
list_first = f.split('\n')
list_lists_all = []
with open(os.path.realpath(rf'structured_g_data.txt'), 'a') as f:
    for item in list_first:
        inner_list = item.split('; ')
        new_list = []
        for item in inner_list:
            new_list.append(stringlist_to_list(item))
        final_list = [new_list[0], new_list[1]]
        for i in range(n_outcomes):
            final_list.append(new_list[2][i*n_bookmakers:(i+1)*n_bookmakers])
        text = f'{final_list[0]}; {final_list[1]}'
        for i in range(2, 2+n_outcomes):
            text += f'; {final_list[i]}'
        f.write(f'\n{text}')
