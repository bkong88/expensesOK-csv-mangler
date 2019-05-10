
# This program extracts the csv lines from ExpensesOK iOS application and converts it into a Excel friendly copy
# pastable format.
# ExpensesOK does not provide support for income, so this app separates an 'income' and 'expenses' category for you.
import csv, os, re, datetime

#### EDIT VARIABLES BELOW AND PROGRAM SHOULD WORK ACCORDINGLY ####
NUM_USERS = 2 ## Number of people in your household using the expenses app.
FILE_NAME_CONTAINS = r"MoneyOK"
FILE_TYPE = r"csv"
PREFERRED_FORMAT = ["Date", "Amount", "Category", "Category group", "Note"] ## ordering of columns in final file (eg. date, in/out, category, subcategory, amount)
DESKTOP_ABS_PATH = os.sep.join((os.path.expanduser("~"), "Desktop"))
AMOUNT_COL_TITLE = "Amount"
CURRENCY = "KRW"
DATE_TIME_FORMAT = "%Y.%m.%d" ## Format of the date string to change into datetime object
DELIMITER = "\t" ## Separate columns with tabs
SALARY_STRING_NAME = "급여" ## What did you write to mean "Salary" in Categories section?
#### EDIT VARIABLES ABOVE AND PROGRAM SHOULD WORK ACCORDINGLY ####

def find_csv_files():
    """This function returns a list of num_users items, all of which will contain 'MoneyOK' in their names."""
    file_list = []
    file_search_regex = re.compile(r".*" + FILE_NAME_CONTAINS.lower() + r".*\." + FILE_TYPE)
    for dir, subdirs, files in os.walk(DESKTOP_ABS_PATH):
        if dir == DESKTOP_ABS_PATH:
            for file in files:
                file = file.lower()
                if file.endswith("." + FILE_TYPE) and file_search_regex.search(file) is not None:
                    file_list.append(file)
    assert (len(file_list) == NUM_USERS), f"There are {len(file_list)} files on your desktop but expected {NUM_USERS} files. Please change the variable 'num_users' at the top of the file."
    return file_list

def create_rows_list(csv_reader):
    """Returns a 2D list with the very first row containing the name of the columns, and the subsequent rows
    representing the values for each column.
    csv_reader: a csv file reader using csv module"""
    rows_list = []
    for row in csv_reader:
        rows_list.append(row)
    return rows_list

def create_list_of_data(rows_list):
    """This function returns a list of dicts which define the values of each row in the original csv file.
    rows_list: a 2D list with the very first row containing the keys for the dicts
    corresponding columns underneath the first row are the values for the dicts
    Returns list in following format:
    [{"Date": "2019-05-09", "Amount": 5000, ...},{"Date": "2019-05-08", "Amount": 9000, ...}, etc]"""
    list_data = []
    first_row = 0
    num_rows = len(rows_list)
    num_cols = len(rows_list[first_row])
    for row in range(first_row + 1, num_rows):
        dict_data = {}
        for col in range(num_cols):
            col_title = rows_list[first_row][col]
            cur_item = rows_list[row][col]
            if col_title in PREFERRED_FORMAT:
                dict_data[col_title] = cur_item
        list_data.append(dict_data)
    return list_data

def list_data_strings_to_python_objects(list_data):
    """Void function; changes list_data but with Python objects rather than all strings
    eg. if key == 'Date', changes value to datetime object
    if key == 'Amount', changes value to positive integer (if KRW)
    """
    for dic_data in list_data:
        for title in PREFERRED_FORMAT:
            if dic_data[title] == "":
                dic_data[title] = None
            else:
                if title.lower() == "date":
                    datetime_object = datetime.datetime.strptime(dic_data[title], DATE_TIME_FORMAT)
                    date_object = datetime.date(datetime_object.year, datetime_object.month, datetime_object.day)
                    dic_data[title] = date_object
                elif title.lower() == "amount":
                    dic_data[title] = abs(float(dic_data[title]))
                    if CURRENCY.lower() == "krw":
                        dic_data[title] = int(dic_data[title])

#todo: take list_data and return new list_data that only contains the month of data the user wants
def extract_month(list_data, month):
    """returns list_data with only the month the user wanted
    month: string in the form YYYY-MM"""
    ## add an assert that month is YYYY-MM format (use regex?)
    target_month = datetime.datetime.strptime(month, "%Y-%m")
    # month_after_target_month = target_month(m+=1)

#todo: take list_data and convert it from python data types list_data with tuples only (preparing for final writing; which will just use writelines)

#todo: output list_data to a txt file (or directly to xlsx/open office file?)
def output_list_data_to_txt(list_data, delim, append_to_file=False, enc="utf-8"):
    """void function; takes the data from list_data and outputs it into a txt file
    rows are each list item
    columns are each key; separated by delim
    list_data: list of tuples, each tuple contains the values to be written
    delim: the deliminator that separates each column (eg. "\t" or "," etc.
    append_to_file: whether to open file in write or append mode"""
    import platform
    is_windows = False
    if "windows" in platform.system().lower(): is_windows = True

    write_mode = "w"
    if append_to_file: write_mode = "a"
    new_line = "\n"
    if is_windows: new_line = "\r\n"

    file_path = os.path.join(DESKTOP_ABS_PATH, "expenses_output.txt")
    working_file = open(file_path, write_mode, encoding=enc, newline="")
    working_file_writer = csv.writer(working_file, delimiter=delim, lineterminator=new_line)
    for line in list_data:
        working_file_writer.writerow(line)
    working_file.close()

# origFile = open(os.path.join(DESKTOP_ABS_PATH, "unixMoneyOK - Copy.csv"), "r", encoding="utf-8")
# origFileReader = csv.reader(origFile, delimiter="\t")
#
# rlist = create_rows_list(origFileReader)
# ldata = create_list_of_data(rlist)
# list_data_strings_to_python_objects(ldata)
# print(ldata)
# ldata = [(5500, "tongshin", None),(7500, "geub", None),(-1500, "Hi", "Yes")]
# output_list_data_to_txt(ldata, DELIMITER)