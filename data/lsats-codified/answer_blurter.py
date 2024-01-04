
def main():
    lines = read_in()
    print_out(lines)
    

def read_in():
    file = open('answers_pasted.txt','r',encoding='utf8')
    
    lines = file.readlines()
    cleaned_lines = [line.replace('(B) ', '\n') for line in lines]
    cleaned_lines = [line.replace('(C) ', '\n') for line in cleaned_lines]
    cleaned_lines = [line.replace('(D) ', '\n') for line in cleaned_lines]
    cleaned_lines = [line.replace('(E) ', '\n') for line in cleaned_lines]


    file.close()

    return cleaned_lines


def print_out(lines):

    write_file = open('answers.txt','w',encoding='utf8')

    for line in lines:
        print(line, file=write_file, end='')

    write_file.close()
