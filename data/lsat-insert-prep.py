
def main():
    insert_statements = []
    test_table();

def ins_stmnt(table, columns, values):
    str_columns = ''
    for item in columns:
        str_columns += item + ', '
    str_columns = str_columns[0:-2]
    return f"INSERT INTO {table} ({str_columns}) VALUES ({str(values)[1:-1]});"

def test_table():
    column = ['exam_date']
    value = ' TO_DATE(\'' + input('What is the exam date (MM/DD/YYYY): ') + '\', \'MM/DD/YYYY\') '

    print(ins_stmnt("tests", column, value))
    return ins_stmnt("tests", column, value)
