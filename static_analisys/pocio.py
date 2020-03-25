import re
import glob

''' Def singleton
'''
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class MyPrint(Singleton):
    def __init__(self):
        self.color = False

    def set_color(self, c):
        self.color = c

    def get_color(self):
        return self.color

    def __print_and_reset(self, s):
        print(str(s), end='')
        # print('\033[0m' if self.color else '', end='')
        print('\033[0m' if self.color else '')

    def black(self, s):
        print('\033[30m' if self.color else '', end='')
        self.__print_and_reset(s)

    def red(self, s):
        print('\033[31m' if self.color else '', end='')
        self.__print_and_reset(s)

    def green(self, s):
        print('\033[32m' if self.color else '', end='')
        self.__print_and_reset(s)

    def yellow(self, s):
        print('\033[33m' if self.color else '', end='')
        self.__print_and_reset(s)

    def blue(self, s):
        print('\033[34m' if self.color else '', end='')
        self.__print_and_reset(s)

    def magenta(self, s):
        print('\033[35m' if self.color else '', end='')
        self.__print_and_reset(s)

    def cyan(self, s):
        print('\033[36m' if self.color else '', end='')
        self.__print_and_reset(s)

    def white(self, s):
        print('\033[37m' if self.color else '', end='')
        self.__print_and_reset(s)

''' Def my regex class
'''
class MyRegex:
    def __init__(self, regex, suggest=""):
        self.regex = regex + "[\s]+[\w]+[\[0-9+\]]*[ *=xX0-9*]*[LlUu]*[;),]{1}"
        self.description = regex
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
            #print(str(ext))
            self.filelist += glob.glob(self.path + '/**/*.' + str(ext)[2:-2], recursive=True)
        return self.filelist

''' Def my file finder class
'''
class MyFileChecker:
    def __init__(self):
        self.file = ''
        self.regex = []
        self.color = False
        self.myprint = MyPrint.Instance()

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

    def print_with_color(self):
        self.color = True

    def print_res(self, verbose=False, showlines=False):

        total_err = 0
        for reg in self.regex:
            total_err += reg.getcounter()

        if total_err or verbose:
            print("")
            print("Checking file: ", end='')
            self.myprint.blue(str(self.file))

        for reg in self.regex:
            if reg.getcounter():
                print(" Found " + str(reg.getcounter()) +
                      "\tregex ["+ str(reg.geddescription()) + " X] --> [" + str(reg.getsuggest()) + "]")
                if showlines:
                    print(" -Found at line[s]: ", end='')
                    self.myprint.yellow(str(reg.getLineList()))

        if total_err:
            self.myprint.red("Total regex found " + str(total_err))
        else:
            if verbose:
                self.myprint.green(" 0 regex found")