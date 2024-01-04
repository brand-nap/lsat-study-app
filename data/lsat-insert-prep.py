from lsat_objects import Test, Score, Prompt, Condition, Question, Answer

def sandbox():
    '''experimental space for testing stuff'''
    placeholder = True

def main():

    statements = []

    # Read in all the master files | Convert text to lists of objects
    tests = read_tests()
    scores = read_scores()
    prompts = read_prompts()
    questions = read_questions()
    answers = read_answers()
    conditions = read_conditions()

    # Place objects in their appropriate subcategories | Compute relational data
    map_qs_as(questions, answers)
    map_ps_qs(prompts, questions)
    map_ps_cs(prompts, conditions)

    # Retrieve the Insert statements for each collection | Append them to statements (list of lists)
    statements.append([test.get_insert() for test in tests])
    statements.append([score.get_insert() for score in scores])
    statements.append([prompt.get_insert() for prompt in prompts])
    statements.append([condition.get_insert() for condition in conditions])
    statements.append([question.get_insert() for question in questions])
    statements.append([answer.get_insert() for answer in answers])

    print_statements(statements) # Output for use! 
    
    
    
#--------------------------------------------------------------------------------------------------------
#-----------------------------------------FILE READ FUNCTIONS--------------------------------------------
#--------------------------------------------------------------------------------------------------------
    
def read_tests():
    """
    Returns: list of Test objects
    """

    file = open('lsats-codified/tests.txt', 'r')
    tests = []

    line = file.readline()[:-1]

    while(line!=''):
        tests.append(Test(line))
        line = file.readline()[:-1]

    file.close()
    return tests

def read_scores():
    """
    Returns: list of Score objects
    """

    file = open('lsats-codified/scores.txt', 'r')
    scores = []
    metadata = file.readline()[:-1]

    line = file.readline()[:-1]
    
    while(line!=''):
        test_id, raw_score, lsat_score = line.split(',')
        scores.append(Score(raw_score, lsat_score))
        
        line = file.readline()[:-1]
        
    file.close()
    return scores

def read_prompts():
    """
    Returns: list of Prompt objects
    """

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
    """
    Returns: list of Question objects
    """

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

def read_answers():
    """
    Returns: list of Answer objects
    """

    file = open('lsats-codified/answers.txt', 'r', encoding = 'utf8')
    answers = []

    line = file.readline()[:-1]
    section = 1
    content_lines = []
    content = ''
    q_id = 0

    while(section!=5):

        if(line=='.'):
            section +=1
            line = file.readline()
        elif(line==''):
            content = single_line(content_lines)
            answers.append(Answer(q_id//5, content))
            content_lines = []
            q_id+=1
        else:
            content_lines.append(line)

        line = file.readline()[:-1]
        
    file.close()
    return answers

def read_answer_sheet():
    """
    Returns: list of indeces for any given question's correct answer
             ie. Q1.C Q2.A Q3.D  ->  [2, 0, 3]
    """

    file = open('lsats-codified/answer_sheet.txt', 'r', encoding = 'utf8')
    answer_ind = []

    line = file.readline()[:-1]
    section = 1

    while(section!=5):

        if(line=='.'):
            section+=1
        else:
            answer_ind.append(0 if line == 'A' else 1 if line == 'B' else 2 if line == 'C' else 3 if line == 'D' else 4)
        line = file.readline()[:-1]

    file.close()

    return answer_ind

def read_conditions():
    """
    Returns: list of Condition objects
    """

    file = open('lsats-codified/conditions.txt','r',encoding = 'utf8')
    conditions = []

    line = file.readline()[:-1]
    content_lines = []
    content = ''
    prompt_id = 0

    while(True):

        if(line=='.'):
            break

        if(line=='-'):
            prompt_id += 1
            line = file.readline()
        elif(line==''):
            content = single_line(content_lines)
            conditions.append(Condition(prompt_id, content))
            content_lines = []
        else:
            content_lines.append(line)

        line = file.readline()[:-1]

    file.close()
    return conditions

#----------------------------------------------------------------------------------------------------------
#--------------------------------------OBJECT MAPPING FUNCTIONS--------------------------------------------
#----------------------------------------------------------------------------------------------------------

def map_qs_as(questions, answers):
    """
    Description: Ties list of 5 answers to their appropriate question counterpart, and flags
    the correct answer by referencing the answer sheet.
    
    Parameters: List of Question objs, List of Answer objs
    """
    
    answer_sheet = read_answer_sheet()

    for question, ans_ind in zip(questions, answer_sheet):
        question.set_answers(answers[question.get_id()*5:question.get_id()*5 + 5])
        question.set_correct(ans_ind)
        

def map_ps_qs(prompts, questions):
    """
    Description: Ties list of questions to their appropriate prompt counterpart.
    
    Parameters: List of Prompt objs, List of Question objs
    """

    for prompt in prompts:
        prompt.set_questions([])

    for question in questions:
        prompts[question.get_prompt_id()].append_questions(question)
        
def map_ps_cs(prompts, conditions):
    """
    Description: Ties list of conditions to their appropriate prompt counterpart.
    
    Parameters: List of Prompt objs, List of Condition objs
    """
    for prompt in prompts:
        prompt.set_conditions([])

    for condition in conditions:
        prompts[condition.get_prompt_id()].append_conditions(condition)

#--------------------------------------------------------------------------------------------------------
#----------------------------------------FORMATTING FUNCTIONS--------------------------------------------
#--------------------------------------------------------------------------------------------------------
        
def single_line(lines):
    """
    Description: Takes a list of lines (former paragraph) and converts to single very long line.
    
    Parameters: lines, type: list of strings
    Returns: single_line, type: string
    """
    
    single_line = ''
    
    for line in lines:
        single_line += line + ' '
        
    return single_line[:-1]

def print_statements(statements):
    """
    Description: Outputs Insert statements in a nice format.
    
    Parameters: statements, type: list of list of strings (ins statements)
    """
    
    for i in range(6):
        print()

    print('BEGIN TRANSACTION;')
    print()
    for table in statements:
        for statement in table:
            print(statement)
        print()
        print()
    print('COMMIT TRANSACTION;')
