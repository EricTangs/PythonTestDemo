import re

if __name__ == '__main__':
    m = re.match(r'end\b','aend')
    if m is not None:

        print(m.group())