
class Test:

    title = 'tests'
    columns = ['exam_date']
    total = 0

    def __init__(self, exam_date):
        self.id = Test.total
        self.exam_date = exam_date
        self.values = ' TO_DATE(\'' + exam_date + '\', \'MM/DD/YYYY\') '
        Test.total += 1

    def get_id(self):
        return self.id
    def get_date(self):
        return self.exam_date
    def get_insert(self):
        return ins(Test.title, Test.columns, self.values)
    

class Prompt:

    title = 'prompts'
    columns = ['prompt_id', 'type_id', 'content']
    total = 0
    
    def __init__(self, section, content, conditions = [], questions = []):
        self.id = Prompt.total
        self.section = section
        self.content = content
        self.conditions = conditions
        self.questions = questions
        self.values = [Prompt.total, section, content]
        Prompt.total += 1

    def get_section(self):
        return self.section
    def get_id(self):
        return self.id
    def get_content(self):
        return self.content
    def get_conditions(self):
        return self.conditions
    def get_questions(self):
        return self.questions
    def get_insert(self):
        return ins(Prompt.title, Prompt.columns, self.values)

    def set_conditions(self, conditions):
        self.conditions = conditions
    def set_questions(self, questions):
        self.questions = questions

class Condition:
    
    title = 'conditions'
    columns = ['prompt_id', 'content']
    total = 0

    def __init__(self, prompt_id, content):
        self.id = Condition.total
        self.prompt_id = prompt_id
        self.content = content
        self.values = [prompt_id, content]
        Condition.total += 1

    def get_id(self):
        return self.id
    def get_prompt_id(self):
        return self.prompt_id
    def get_content(self):
        return self.content
    def get_insert(self):
        return ins( Condition.title, Condition.columns, self.values)
        

class Question:

    title = 'questions'
    columns = ['question_id', 'prompt_id', 'content']
    total = 0

    def __init__(self, prompt_id, content, answers = [], correct = 0):
        self.id = Question.total
        self.prompt_id = prompt_id
        self.content = content
        self.answers = answers
        self.correct = correct
        self.values = [Question.total, prompt_id, content]
        Question.total += 1

    def get_id(self):
        return self.id
    def get_prompt_id(self):
        return self.prompt_id
    def get_content(self):
        return self.content
    def get_answers(self):
        return self.answers
    def get_correct_answer():
        return self.answers[self.correct]
    def get_correct(self):
        return correct
    def get_insert(self):
        return ins(Question.title, Question.columns, self.values)

    def set_answers(self, answers):
        self.answers = answers
    def set_correct(self, correct):
        self.correct = correct
        if len(self.answers) == 5:
            self.answers[correct].set_is_correct(True)
            

class Answer:
    
    title = 'answers'
    columns = ['question_id', 'content', 'is_correct']
    total = 0

    def __init__(self, q_id, content, is_correct = False):
        self.id = Answer.total
        self.q_id = q_id
        self.content = content
        self.is_correct = is_correct
        self.values = [q_id, content, is_correct]
        Answer.total +=1

    def get_id(self):
        return self.id
    def get_q_id(self):
        return self.q_id
    def get_content(self):
        return self.content
    def get_is_correct(self):
        return self.is_correct
    def get_insert(self):
        return ins(Answer.title, Answer.columns, self.values)

    def set_is_correct(self, is_correct):
        self.is_correct = is_correct
        self.values[2] = is_correct



def ins(table, columns, values):
        str_columns = ''
        for item in columns:
            str_columns += item + ', '
        str_columns = str_columns[0:-2]
        return f"INSERT INTO {table} ({str_columns}) VALUES ({str(values)[1:-1]});"
