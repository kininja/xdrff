#!/usr/bin/python3
# 
# xdrff - XDR File Formatter
# 
# Mon Mar 30 21:39:35 PDT 2020
#
# Main functionality is in fix(), see that function's doc. 


import sys, getopt, re

HELP_STRING = "Usage: xdrff.py -i, --ifile <inputfile> -o, --ofile <outputfile>"
TAB_SEPARATOR = '\t'
SPACE_SEPARATOR = ' '
TIME_SEPARATOR = ':'
DELIM = '\t'

def init(argv):
    '''Initializing function which gathers arguments and options to script when called or prints out help message HELP_STRING.

    Keyword arguments:
    -i, --ifile -- input file, otherwise uses default.
    -o, --ofile -- output file to write to, otherwise uses default. 

    Returns: A tuple of Input file name and output file name.

    '''

    inputfile = 'querytest.tsv'
    outputfile = 'output.tsv'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(HELP_STRING)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print (HELP_STRING)
            sys.exit()
        elif opt in ("-i", "--ifile"): 
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    return inputfile, outputfile

def readInFile(fileName):
    '''Read in a tsv formatted file from Cortex XDR 2 query output.

    Keyword arguments:
    fileName -- name of the file

    Expects: A file name for the os to open.
    Returns: A list of one line per element as read in from the file. 

    '''

    with open(fileName, 'r', encoding='utf-8') as a_file:
        line_list = a_file.readlines()

    return line_list

def reformatLine(line):
    '''Reformat a single line from XDR, breaking out time and date so it can be easily sorted by hour and minute and second, as well as breaking out rest of tab delimitted file to elements in a list.

    Keyword arguments:
    line -- Expects one row of text, with the XDR formatting including tab delimits in a specific order.

    Returns: A formatted list of elements.
    '''

    # split out each tab separated value to a cell element 
    cells = line.split(TAB_SEPARATOR)
    # split out the "Timestamp" field specifically, since you can't sort this easily in a spreadsheet
    date_cell = cells[0].split(SPACE_SEPARATOR)
    time_cell = date_cell[3].split(TIME_SEPARATOR)

    # delete unbroken time cell
    del date_cell[3]
    # start creation of new line
    new_line = date_cell
    # add time broken into three elements, hour, minute, seconds
    for i in range(len(time_cell)):
        new_line.append(time_cell[i])
    # add rest of original cells, minus the first element of time which we broke out above
    for i in range(1, len(cells)):
        new_line.append(cells[i])

    return new_line

def reformatHeaders(line):
    '''Expects a string representing the tab-separated first row of XDR query results output. This takes the original headers from XDR results and updates with broken out time columns based on format in reformatLine().

    Keyword arguments:
    line -- Expects a string representing the tab-separated first row of XDR query results output. 

    Returns: List of elements updated for only the header row.
    '''
    # since we broke out the "Timestamp" field in reformatLine, we need to do the same in the headers
    new_line = []
    new_time_headers = ['Month', 'Day', 'Year', 'Hour', 'Minute', 'Second']

    # load up the new object with the headers
    for i in range(len(new_time_headers)):
        new_line.append(new_time_headers[i])

    # start adding all elements from split on tab
    split_list = line.split(TAB_SEPARATOR)
    for i in range(len(split_list)):
        new_line.append(split_list[i])
    # get rid of now erroneous original time header cell value
    del new_line[6]
    return new_line

def reformat(fileInput):
    '''Reformat list of lines from XDR query results input read. 

    Keyword arguments: 
    fileInput - Expects a list of lists, the first list for each row, and each list in each row for all the column elements.

    Returns: List of lines formatted using reformatLine() function.
    '''

    # write header from orignal
    # still need to insert five additional blank columns for the expanded time cells
    new_headers = []
    formatted_output = []

    #new_headers = reformatHeaders(fileInput[0])
    formatted_output.insert(0, reformatHeaders(fileInput[0]))
    # print headers up until last one to avoid hanging comma
    #for i in range(len(new_headers)):
    #    formatted_output.append(new_headers[i])

    # format remaining lines and load into formatted_output
    for i in range(1, len(fileInput)):
        formatted_output.append(reformatLine(fileInput[i]))
        #debug print
        #print (fileInput[i-1])

    return formatted_output

def writeOut(outputFileName, inputData):
    '''Take inputData expecting it to be a list of lists and writing out to the outputFileName.
    
    Keyword arguments:
    outputFilename - String name of the file to be written to disk.
    inputData - List of lists, elements for each column in a row, each row a list. 
    
    Returns: Nothing. It writes to disk.
    '''
    # open output file and print out to it
    with open(outputFileName, mode='w', encoding='utf-8') as write_file:
        # begin writing each row, we have a list of lists in inputData now
        # for each list in the list:
        for i in range(len(inputData)):
            # for each element in the list (row), minus one to leave last one without a comma on end
            for j in range(len(inputData[i])-1):
                    write_file.write(inputData[i][j])
                    write_file.write(DELIM)
            #write last element without a comma, these are expected to come with carriage returns from source file
            write_file.write(inputData[i][j+1])

    return


def fix(inFile, outFile):
    '''Fix() takes a file, formatted as the tsv file exported from an XDR query, and a name for an output file, and fixes the timestamps to make it sortable in Excel. Output is still a tsv file which is needed to preserve long strings with commas, such as Event log descriptions and company names for software.

    For example, the default XDR 2 query results outputs useful data, but with the first column formatted like so:
    
        | Timestamp              |
        | Mar 24th 2020 05:00:13 |

    Sorting or filtering on this column in a spreadsheet is impossible. This function, and the functions it calls, will output the tsv file with a fixed header and column data to match:

        | Month | Day  | Year | Hour | Minute | Second |
        | Mar   | 24th | 2020 | 5    | 0      | 13     |

    Keyword arguments:
    inFile - Name of file to read from disk and reformat.
    outFile - Name of file to write out to disk.

    Returns: Nothing. 
    '''
    # read in from tsv file to reformat time
    file_data  = readInFile(inFile)

    # reformat the time column headers and the data
    formatted_data = reformat(file_data)

    # write out to a tsv formatted file to preserve special chars in fields
    writeOut(outFile, formatted_data)


if __name__ == '__main__':
    inputf, outputf = init(sys.argv[1:])
    message = 'Using "' + inputf + '" as an input file, and "' + outputf + '" as the output file...'
    print (message)

    fix(inputf, outputf)






