import re
import sys
import os
import ast

MAX_LINE_LENGTH = 79
INDENTATION_FOUR = re.compile(r'^ *')
UNNECESSARY_SEMICOLON = re.compile(r"[^a-zA-Z0-9_ ];(?<!;;)|^    pass;")
INLINE_COMMENT_TWOSPACES = re.compile(r'(?!^) {0,}#.*?$')
TODO_FOUNDER = re.compile(r'\w*\s*#.*TODO.*$', flags=re.IGNORECASE)
BLANK_LINE = re.compile(r'^\s*$')
SPACES_AFTER_CONSTRUCTION_NAME = re.compile(r'(?=class|def)(class|def)\s{2,}')
CAMEL_CASE_NAME = re.compile(r'(([A-Z][a-z]+)([A-Z][a-z]+))|([A-Z][a-z]+)')
SNAKE_CASE_NAME = re.compile(r'^[a-z0-9_]+')
IMMUTABLE_LIST = [int, float, complex, ast.Str, ast.Tuple, frozenset, ast.Bytes(), ast.NameConstant, ast.Num, ast.Constant]


class ReadFile:
    def __init__(self, filepath):
        self.lines = open(filepath, 'r').readlines()
        self.tree = ast.parse(open(filepath, 'r').read())


class ErrorHunter:
    messages = []

    def __init__(self, msg=None):
        self.msg = msg
        self.messages.append(self)


class Errors(Exception):
    """Base class for error handling"""
    pass


class StringToLongError(Errors):
    """S001 - Raised when the length of a string more than 79"""
    pass


class NewIndentationError(Errors):
    """S002 - Raised when the indentation is not a multiple of four"""
    pass


class SemicolonError(Errors):
    """S003 - Raised when the unnecessary semicolon after a statement founded"""
    pass


class SpaceInlineCommentError(Errors):
    """S004 - Raised when there are less than two spaces before inline comments"""
    pass


class TODOError(Errors):
    """S005 - Raised when the TODO found"""
    pass


class BlankLinesError(Errors):
    """S006 - Raised when the more than two blank lines preceding a code line"""
    pass


class SpacesAfterConstructionNameError(Errors):
    """S007 - Raised when the more than too many spaces after construction_name (def or class)"""
    pass


class CaseNameError(Errors):
    """S008 - Raised when class name is not look a like CamelCase text"""
    """S009 - Raised when function name is not look a like snake_case text"""
    """S010 - Raises when function argument is not look a like snake_case text"""
    """S011 - Raises when function variable is not look a like snake_case text"""
    pass


class DefaultFunctionArgumentError(Errors):
    """S012 - Raises when function argument is mutable"""
    pass


class ErrorHandler():
    def __init__(self, pos=None, line=None, path=None, elem_name=None, elem_pos=None, elem_type=None):
        self.pos = pos
        self.line = line
        self.path = path
        self.elem_name = elem_name
        self.elem_pos = elem_pos
        self.elem_type = elem_type

    def S001(self, line, path):
        try:
            if len(line) > MAX_LINE_LENGTH:
                raise StringToLongError
        except StringToLongError as ee:
            ErrorHunter(f'{path}: Line {self}: {StringToLongError("S001 Too long line")}')

    def S002(self, line, path):
        try:
            if len(INDENTATION_FOUR.findall(line)[0]) % 4 != 0:
                raise NewIndentationError
        except NewIndentationError as ie:
            ErrorHunter(f'{path}: Line {self}: {NewIndentationError("S002 Indentation is not a multiple of four")}')

    def S003(self, line, path):
        try:
            if re.findall(UNNECESSARY_SEMICOLON, line):
                raise SemicolonError
        except SemicolonError as se:
            ErrorHunter(f'{path}: Line {self}: {SemicolonError("S003 Unnecessary semicolon")}')

    def S004(self, line, path):
        try:
            if re.findall(INLINE_COMMENT_TWOSPACES, line):
                if not bool(re.findall(re.compile(r'  #'), line)):
                    raise SpaceInlineCommentError
        except SpaceInlineCommentError as sle:
            ErrorHunter(
                f'{path}: Line {self}: {SpaceInlineCommentError("S004 At least two spaces required before inline comments")}')

    def S005(self, line, path):
        try:
            if re.findall(TODO_FOUNDER, line):
                raise TODOError
        except TODOError as tde:
            ErrorHunter(f'{path}: Line {self}: {TODOError("S005 TODO found")}')

    def S006(self, line, path):
        try:
            if not bool(re.findall(BLANK_LINE, line)):
                q = 0
                for i in range(4):
                    if re.findall(BLANK_LINE, file.lines[self - 1 - i]):
                        q += 1
                    if q > 2:
                        raise BlankLinesError
                else:
                    q = 0
        except BlankLinesError as ble:
            ErrorHunter(
                f'{path}: Line {self}: {BlankLinesError("S006 More than two blank lines used before this line")}')

    def S007(self, line, path):
        try:
            if re.findall(SPACES_AFTER_CONSTRUCTION_NAME, line):
                raise SpacesAfterConstructionNameError
        except SpacesAfterConstructionNameError as sacne:
            msg = f"S007 Too many spaces after '{re.findall(SPACES_AFTER_CONSTRUCTION_NAME, line)[0]}'"
            ErrorHunter(f'{path}: Line {self}: {SpacesAfterConstructionNameError(msg)}')

    def S008(path, elem_name, elem_pos, elem_type='Class'):
        """CamelCase"""
        try:
            if not bool(re.findall(CAMEL_CASE_NAME, elem_name)):
                raise CaseNameError
        except CaseNameError as cne:
            msg = f"S008 {elem_type} name '{elem_name}' should use CamelCase"
            ErrorHunter(f'{path}: Line {elem_pos}: {CaseNameError(msg)}')

    def S009(path, elem_name, elem_pos, elem_type='Function'):
        try:
            if not bool(re.findall(SNAKE_CASE_NAME, elem_name)):
                raise CaseNameError
        except CaseNameError as sne:
            msg = f"S009 {elem_type} name '{elem_name}' should be written in snake_case"
            ErrorHunter(f'{path}: Line {elem_pos}: {CaseNameError(msg)}')

    def S010(path, elem_name, elem_pos, elem_type='Argument'):
        try:
            if not bool(re.findall(SNAKE_CASE_NAME, elem_name)):
                raise CaseNameError
        except CaseNameError as sne:
            msg = f"S010 {elem_type} name '{elem_name}' should be written in snake_case"
            ErrorHunter(f'{path}: Line {elem_pos}: {CaseNameError(msg)}')

    def S011(path, elem_name, elem_pos, elem_type='Variable'):
        try:
            if not bool(re.findall(SNAKE_CASE_NAME, elem_name)):
                raise CaseNameError
        except CaseNameError as sne:
            msg = f"S011 {elem_type} name '{elem_name}' should be written in snake_case"
            ErrorHunter(f'{path}: Line {elem_pos}: {CaseNameError(msg)}')

    def S012(path, elem_name, elem_pos, elem_type):
        try:
            if elem_type not in IMMUTABLE_LIST:
                raise DefaultFunctionArgumentError
        except DefaultFunctionArgumentError as dfae:
            msg = f"S012 Default argument value is mutable"
            ErrorHunter(f'{path}: Line {elem_pos}: {DefaultFunctionArgumentError(msg)}')


def func_handler(path, stmt):
    ErrorHandler.S009(path=path, elem_name=stmt.name, elem_pos=stmt.lineno)
    for function_arg in stmt.args.defaults:
        ErrorHandler.S012(path=path, elem_name=None, elem_pos=function_arg.lineno, elem_type=type(function_arg))
    for function_arg in stmt.args.args:
        ErrorHandler.S010(path=path, elem_name=function_arg.arg, elem_pos=function_arg.lineno)
    for variable in stmt.body:
        if isinstance(variable, ast.Assign):
            ErrorHandler.S011(path=path, elem_name=variable.targets[-1].id, elem_pos=variable.lineno)


def class_handler(path, stmt):
    ErrorHandler.S008(path=path, elem_name=stmt.name, elem_pos=stmt.lineno)
    for subbody in stmt.body:
        if isinstance(subbody, ast.FunctionDef):
            ErrorHandler.S009(path=path, elem_name=subbody.name, elem_pos=subbody.lineno)
            for function_arg in subbody.args.defaults:
                ErrorHandler.S012(path=path, elem_name=None, elem_pos=subbody.lineno, elem_type=type(function_arg))
            for function_arg in subbody.args.args:
                ErrorHandler.S010(path=path, elem_name=function_arg.arg, elem_pos=function_arg.lineno)
            for variable in subbody.body:
                if isinstance(variable, ast.Assign):
                    variable_pos = variable.lineno
                    variable_name = variable.targets
                    for item in variable_name:
                        try:
                            for item in variable_name:
                                ErrorHandler.S011(path=path, elem_name=item.attr, elem_pos=variable.lineno)
                        except:
                            for item in variable_name:
                                ErrorHandler.S011(path=path, elem_name=item.id, elem_pos=variable.lineno)

def error_collector(path, file):
    for pos, line in enumerate(file.lines, start=1):
        ErrorHandler.S001(pos, line, path)
        ErrorHandler.S002(pos, line, path)
        ErrorHandler.S003(pos, line, path)
        ErrorHandler.S004(pos, line, path)
        ErrorHandler.S005(pos, line, path)
        ErrorHandler.S006(pos, line, path)
        ErrorHandler.S007(pos, line, path)
    for stmt in file.tree.body:
        if isinstance(stmt, ast.FunctionDef):
            func_handler(path, stmt)
        if isinstance(stmt, ast.ClassDef):
            class_handler(path, stmt)

if __name__ == '__main__':
    args = ' '.join(sys.argv[1:])
    if args.endswith('.py'):
        path = args
        file = ReadFile(path)
        error_collector(path, file)
    if os.path.exists(args):
        for dir, folder, files in os.walk(args):
            for f in files:
                if f.endswith('.py'):
                    path = os.path.join(dir, f)
                    file = ReadFile(path)
                    error_collector(path,file)
    for i in ErrorHunter.messages:
        if i.msg:
            print(i.msg)
