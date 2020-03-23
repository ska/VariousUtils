import re
import glob

''' Def my regex class
'''
class myStyle():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[34m' + str(x)
    MAGENTA = lambda x: '\033[35m' + str(x)
    CYAN = lambda x: '\033[36m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)

''' Def my regex class
'''
class MyRegex:
    def __init__(self, regex, mdescript="", suggest=""):
        self.regex = regex
        self.description = mdescript
        self.suggest = suggest
        self.counter = 0
        self.linelist = []

    def appendlinenum(self, mlinenumber):
        self.linelist.append(mlinenumber)

    def match(self, mline, mfileline = None):
        x = re.findall(self.regex, mline)
        if x:
            self.counter += 1
            if mfileline is not None:
                self.appendlinenum(mfileline)
            return True
        return False

    def getcounter(self):
        return self.counter

    def getLineList(self):
        return self.linelist

    def geddescription(self):
        return self.description

    def getsuggest(self):
        return self.suggest

''' Def my file finder class
'''
class MyFileFinder:

    def __init__(self, path, extension):
        self.path = path
        self.extension = extension
        self.filelist = []

    def getAllFiles(self):
        filelist = []
        for ext in self.extension:
            print(str(ext))
            self.filelist += glob.glob(self.path + '/**/*.' + str(ext)[2:-2], recursive=True)
        return self.filelist

''' Def my file finder class
'''
class MyFileChecker:
    def __init__(self):
        self.file = ''
        self.regex = []

    def set_file(self, filename):
        self.file = filename

    def add_regex(self, regex):
        self.regex.append(regex)

    def check(self):
        line_count = 0;
        fd = open(self.file, "r", encoding="ISO-8859-1")
        line = fd.readline()
        while line:
            line_count += 1
            for reg in self.regex:
                reg.match(line, line_count)

            line = fd.readline()
        fd.close()

    def print_res(self, verbose=False, showlines=False):

        total_err = 0
        for reg in self.regex:
            total_err += reg.getcounter()

        if total_err or verbose:
            print("")
            print("Checking file: " + myStyle.BLUE(self.file) + myStyle.RESET(""))

        for reg in self.regex:
            if reg.getcounter():
                print(" Found " + str(reg.getcounter()) +
                      "\tregex ["+ str(reg.geddescription()) + " X] --> [" + str(reg.getsuggest()) + "]")
                if showlines:
                    print(" -Found at line[s]: " + myStyle.YELLOW(str(reg.getLineList())) + myStyle.RESET(""))

        if  total_err:
            print(myStyle.RED("Total regex found " + str(total_err)) + myStyle.RESET(""));

        else:
            if verbose:
                print(myStyle.GREEN(" 0 regex found")+myStyle.RESET(""));
