#!/usr/bin/env python3

import re
from pathlib import Path
from functools import reduce
import os
import os.path

def main():
    dirname = os.path.dirname(os.path.realpath(__file__))
    with open(dirname+'/README.md') as f:
        contents = f.read()

    codeBlocks = re.findall(r'\`\`\`.*?\n(.*?)\`\`\`', contents, re.DOTALL)
    bashrc = []
    bashAliases = []
    for block in codeBlocks:
        commentBuffer = []
        functionMode = False
        for line in block.split('\n'):
            stripLine = line.strip()

            if functionMode:
                bashAliases += [line]
                if stripLine.startswith('}') and len(stripLine) == 1:
                    functionMode = False
                continue

            if len(stripLine) == 0:
                bashrc += commentBuffer
                commentBuffer = []
            elif stripLine.startswith('export') or stripLine.startswith('alias'):
                bashAliases += commentBuffer
                bashAliases += [line]
                commentBuffer = []
            elif stripLine.startswith('function'):
                bashAliases += commentBuffer
                bashAliases += [line]
                commentBuffer = []
                functionMode = True
            else:
                commentBuffer += [line]
        bashrc += commentBuffer
    
    bashAliases = reduce(lambda a,b: a+"\n"+b, bashAliases)
    bashrc = reduce(lambda a,b: a+"\n"+b, bashrc)

    with open(str(Path.home()) + "/.bash_aliases", 'w') as f:
        f.write(bashAliases)
    with open(str(Path.home()) + "/.bashrc", 'w') as f:
        f.write(bashrc)

    print("Successfully installed, please run `. ~/.bashrc` or reload your shell to update")


if __name__=='__main__':
    main()
