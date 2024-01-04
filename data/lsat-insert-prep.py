from lsat_objects import Test, Prompt, Condition, Question, Answer

def sandbox():
    prompts = read_prompts()

    statements = [prompt.get_insert() for prompt in prompts]

    for statement in statements:
        print(statement)

def main():

    tests = read_tests()
    scores = read_scores()
    prompts = read_prompts()
    
    statements = []

    statements.append(test_table())
    
    test_id = int(input('test_id: '))
    section_totals, section_stmnts = sections_table(test_id)
    statements.append(scores_table(test_id, section_totals))
    statements.append(section_stmnts)
    prompt_stmnts, sect_prompts, starting_id = prompts_table(section_totals)
    statements.append(prompt_stmnts)
    condition_stmnts = conditions_table(sect_prompts[0], starting_id)
    statements.append(condition_stmnts)
    question_statements, qstart = questions_table(section_totals, sect_prompts, starting_id)
    statements.append(question_statements)
    statements.append(answers_table(section_totals, qstart))

    print_statements(statements)
    
    # make questions and answers a list of list of lists (order matters)
    # q_and_as = [['Insert question...', ['','','','','']], ['Insert question...' : ['','','','','']]]
    # allows me to do an answer sheet so I can go A = 0 B = 1 etc
    # from there I can go q_and_as[i][1][A] = (q_and_as[i][1][A])[:indexOf('FALSE')] + 'TRUE' + (q_and_as[i][1][A])[indexOf('FALSE') + 5:-1]
    

def read_tests():

    file = open('lsats-codified/tests.txt', 'r')
    tests = []

    line = file.readline()[:-1]

    while(line!=''):
        tests.append(Test(line).get_insert())
        line = file.readline()[:-1]

    file.close()
    return tests


def read_scores():

    file = open('lsats-codified/scores.txt', 'r')
    scores = {}
    metadata = file.readline()[:-1]

    for i in range(105):
        scores[i] = []

    line = file.readline()[:-1]
    
    while(line!=''):
        score_info = line.split(',')
        # map of all possible lsat scores for any given raw score
        # ie. raw score: 90   lsat score: 170, 169, 173, 171
        scores[int(scores_info[1])].append(scores_info[2])
        
        line = file.readline()[:-1]
        
    file.close()
    return scores
    

def read_prompts():

    file = open('lsats-codified/prompts.txt', 'r', encoding = 'utf8')
    prompts = []

    line = file.readline()[:-1]
    
    section = 1
    content = ''
    content_lines = []
    
    while(section !=5):

        if(line == '.'):
            section +=1
            line = file.readline()
        elif(line == ''):
            content = single_line(content_lines)
            prompts.append(Prompt(section, content))
            
            content_lines = []
        else:
            content_lines.append(line)
            
        line = file.readline()[:-1]

    file.close()
    return prompts
    
    
def read_questions():

    file = open('lsats-codified/questions.txt', 'r', encoding = 'utf8')
    questions = []

    line = file.readline()[:-1]
    section = 1
    content_lines = []
    content = ''
    prompt = 0

    while(section!=5):

        if(line=='.'):
            section += 1
            line = file.readline()
        elif(line =='-'):
            prompt +=1
            line = file.readline()
        elif(line==''):
            if(section==2 or section ==3):
                prompt+=1
            content = single_line(content_lines)
            questions.append(Question(prompt, content))
            content_lines = []
        else:
            content_lines.append(line)
            
        line = file.readline()[:-1]

    file.close()
    return questions


def single_line(lines):
    
    single_line = ''
    
    for line in lines:
        single_line += line + ' '
        
    return single_line[:-1]


    






    
    

def ins_stmnt(table, columns, values):
    str_columns = ''
    for item in columns:
        str_columns += item + ', '
    str_columns = str_columns[0:-2]
    return f"INSERT INTO {table} ({str_columns}) VALUES ({str(values)[1:-1]});"

def test_table():
    #Status: Finished!
    title = 'tests'
    columns = ['exam_date']
    print()
    values = ' TO_DATE(\'' + input('Exam date (MM/DD/YYYY): ') + '\', \'MM/DD/YYYY\') '

    return [ins_stmnt(title, columns, values)]

def scores_table(test_id, section_totals):
    #Status: Finished!
    title = 'scores'
    columns = ['test_id', 'raw_score', 'lsat_score']
    values = []
    statements = []
    
    total_points = sum(section_totals)
    
    for i in range(total_points+1):
        values.append(test_id)
        values.append(i)
        values.append(150)#int(input(f'score for raw score of {i}: ')))
        statements.append(ins_stmnt(title, columns, values))
        values = []

    return statements

def sections_table(test_id):
    #Status: Finished!
    title = 'sections'
    columns = ['section_id', 'test_id', 'type_id', 'total_questions']
    values = []

    section_totals = []
    statements = []
    
    print()
    for i in range(4):
        values.append(i+1 + (test_id-1)*4)
        values.append(test_id)
        values.append(i+1)
        section_totals.append(int(input(f'number of questions in Section {i+1}: ' )))
        values.append(section_totals[i])
        statements.append(ins_stmnt(title, columns, values))
        values = []

    return section_totals, statements
        

def prompts_table(section_totals):
    #Status: Finished!
    title = 'prompts'
    columns = ['prompt_id', 'type_id', 'content']
    values = []
    statements = []
    sects = [i for i in section_totals]
    
    print()
    sects[0] = int(input('# of prompts in section 1: '))
    sects[3] = int(input('# of stories in section 4: '))
    starting = int(input('next id for prompts: '))

    for i in range(starting, sum(sects)+1):
        values.append(i)
        type_id = 1 if i-starting+1 >= sects[0] else 2 if i-starting+1 >= sects[1] else 3 if i-starting+1 >= sects[2] else 4
        values.append(type_id)
        values.append('')
        statements.append(ins_stmnt(title, columns, values))
        values = []

    return statements, sects, starting

def conditions_table(sect1_prompts, starting_id):
    #Status: Finished!
    title = 'conditions'
    columns = ['prompt_id', 'content']
    values = []
    statements = []

    for i in range(sect1_prompts):
        n = int(input(f'# conditions in prompt {i+1}: '))
        for j in range(n):
            values.append(i+starting_id)
            values.append('')
            statements.append(ins_stmnt(title, columns, values))
            values = []

    return statements

def questions_table(section_totals, sect_prompts, pstart):
    #Status: Finished!
    title = 'questions'
    columns = ['question_id', 'prompt_id', 'content']
    values = []
    statements = []
    print()
    initial_qstart = int(input('starting id for questions: '))
    qstart = initial_qstart

    for i in range(sect_prompts[0]):
        per_p = int(input(f'How many questions are in Prompt {i+1} of Section 1: '))
        for j in range(per_p):
            values.append(j+qstart)
            values.append(i+pstart)
            values.append('')
            statements.append(ins_stmnt(title, columns, values))
            values = []
        qstart += per_p
    pstart += sect_prompts[0]
            
    for i in range(sect_prompts[1] + sect_prompts[2]):
        values.append(i+qstart)
        values.append(i+pstart)
        values.append('')
        statements.append(ins_stmnt(title, columns, values))
        values = []
    pstart += sect_prompts[1] + sect_prompts[2]
    qstart += sect_prompts[1] + sect_prompts[2]
    
    for i in range(sect_prompts[3]):
        per_p = int(input(f'How many questions are in Story {i+1} of Section 4: '))
        for j in range(per_p):
            values.append(j+qstart)
            values.append(i+pstart)
            values.append('')
            statements.append(ins_stmnt(title, columns, values))
            values = []
        qstart += per_p
            
    return statements, initial_qstart
    
    

def answers_table(section_totals, qstart):
    #Status: Finished!
    title = 'answers'
    columns = ['question_id', 'content', 'is_correct']
    values = []
    statements = []

    total = (section_totals[0] + section_totals[1] + section_totals[2] + section_totals[3])

    for i in range(total):
        for j in range(5):
            values.append(i+qstart)
            values.append('')
            values.append('FALSE')
            statements.append(ins_stmnt(title, columns, values))
            values = []
        statements.append('')

    return statements

def print_statements(statements):
    print()
    print()
    for table in statements:
        for statement in table:
            print(statement)
        print()
        print()

def info_dump(filePath):


    print()
