
def main():
    # reads them in, cleans them, prints them out | SAVES ME THE HASSLE!
    lines = read_in()
    print_out(lines)
    

def read_in():
    '''
    Description: Reads in each line and replaces any lettering convention from paste to a new line command

    Returns: list of every single line in a file but scrubbed for use
    '''
    file = open('answers_pasted.txt','r',encoding='utf8')
    
    lines = file.readlines()
    cleaned_lines = [line.replace('(B) ', '\n') for line in lines]
    cleaned_lines = [line.replace('(C) ', '\n') for line in cleaned_lines]
    cleaned_lines = [line.replace('(D) ', '\n') for line in cleaned_lines]
    cleaned_lines = [line.replace('(E) ', '\n') for line in cleaned_lines]


    file.close()

    return cleaned_lines


def print_out(lines):
    '''
    Description: Prints each line to the master answers file

    Parameter: list of cleaned lines
    '''

    write_file = open('answers.txt','w',encoding='utf8')

    for line in lines:
        print(line, file=write_file, end='')

    write_file.close()
