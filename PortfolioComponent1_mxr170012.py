# Portfolio Assignment 1: Text Processing with Python
# Motalib Rahim (mxr170012)

import sys  # for system parameter
import pathlib  # to import file on any platform
import re # regular expression operations
import pickle # saves dict as a pickle file


class Person:  # create an object class for person
    def __init__(self, data):
        parsed_data = self.process_lines(data)
        print(parsed_data)
        self.last = parsed_data[0]
        self.first = parsed_data[1]
        self.mi = parsed_data[2]
        self.id = parsed_data[3]
        self.phone = parsed_data[4]

    def display(self):  # display person information
        print(self.last, self.first, self.mi, self.id, self.phone)
        return self.last, self.first, self.mi, self.id, self.phone

    def process_lines(self, inputs):  # processing  the input data
        print(inputs)
        lines = inputs.strip().split(",")  # split on comma
        print(lines)

        # in_lst of indexing for last, mi, first and mi and checking upper lower case
        for in_lst in range(len(lines[:2])):
            lines[in_lst] = lines[in_lst].lower()
            lines[in_lst] = lines[in_lst][0].upper() + lines[in_lst][1:]
        if lines[2] == "": # middle initial empty
            lines[2] = 'X' # replaces with X
        else:
            lines[2].upper() # if mi exist then upper case

        # for id formatting
        id_format = "[A-Z]{2}\d{4}"
        while not re.match(id_format, lines[3]):  # regular expression to process text
            print('ID invalid', lines[3])
            print('ID is two letters followed by 4 digits. Please enter a valid id:')
            lines[3] = input()

            lines[3] = lines[3].upper()
            print(lines[3])

        # for processing phone number format
        phone_format = "\d{3}-\d{3}-\d{4}$"
        while not re.match(phone_format, lines[4]):
            print('Phone ' + lines[4] + " is invalid")
            print('Enter phone number in form 123-456-7890: ')
            lines[4] = input()
            print(lines[4])
        return lines
    # return lines


def in_file(filepath):

    print("\nEmployee list:") # gives full list of employees
# uses pathlib to open file with ease in any platform
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        inputs = f.readlines()[1:] # start after header
    print(inputs)

# person loop for inputs
    for person in inputs:
        x = Person(person)
    persons = {}


# save file to pickle
    pickle.dump(persons, open('persons.p', 'wb'))
# read the file of pickle
    persons_in = pickle.load(open('persons.p', 'rb'))
    print(persons_in)


# check for file validity
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please input a valid file as in system arg')
        quit()
    in_file('data/data.csv')

def in_file(filepath):

    print("\nEmployee list:") # gives full list of employees
# uses pathlib to open file with ease in any platform
    with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
        inputs = f.readlines()[1:] # start after header
    print(inputs)