
import argparse
import sys
import re
#объiявление переменны

#вывод строк
def output(line):
    print(line)



mas=[] #массив стро
def reg_compile(params):
    i=0
    before1=''
    k=0
    while i<len(params):
        if (params[i]=="?") or (params[i]=="*"):
            k+=1
            before=before1
            if i<(len(params)-1):
                after=params[i+1]
            else:
                after=''
        else:
            before1=params[i]
        i+=1
    if "?" in params:
        search_str=re.compile('%s([A-Za-z0-9]){%s}%s'%(before, k, after))
    elif "*" in params:
        search_str=re.compile('%s([A-Za-z0-9])+%s'%(before, after))
    regexp=re.compile(search_str)
    return(regexp)

def match(lines, params):
    if params.ignore_case:
        (param, line) = (params.pattern.lower(), lines.lower())
    else:
        (param, line) = (params.pattern, lines)
    #
    i=0
    before1=''
    k=0
    if ("?" in param) or ("*" in param):
        regexp=reg_compile(param)
        if regexp.findall(line):
            return(True)

    if params.invert:
        if param not in line:
            return(True)
        else:
            return(False)
    else:
        if param in line:
            return(True)
        else:
            return(False)


#ищет паттерн
def grep(lines, params):
    counter_after_match=0 
    counter=0 #совпадение с шаблоном
    num=0 #номер строки
    if params.context:
        if not params.after_context:
            params.after_context=params.context 
        if not params.before_context:
            params.before_context=params.context

#################################################################
    for line in lines:
        num+=1
        n=params.line_number
        line = line.rstrip() 
        line_pattern='{0}{1}{2}'.format(str(num), ":", line)
        if(match(line,params)):

            if not params.count:
                for i in mas:
                    output(i)
                mas.clear()
                output(line_pattern) if n else output(line) 
                counter_after_match=params.after_context
            if params.count:
                counter+=1

        elif not params.count:
            if (counter_after_match<=params.after_context and counter_after_match>0):
                line3=line_pattern.replace(":", "-")
                output(line3) if n else output(line)
                counter_after_match-=1
            else:
                line_n='{0}{1}{2}'.format(str(num), "-", line)
                mas.append(line_n) if n else mas.append(line)
 
        if len(mas)>params.before_context:
            mas.pop(0)
        

      
    if params.count:
         output(str(counter))
def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
       
    grep(sys.stdin.readlines(), params)

if __name__ == '__main__':
    main()


