import sys

COMP = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000',
 '!D':'0001101','!A':'0110001','-D':'0001111','-A':'0110011','D+1':'0011111',
 'A+1':'0110111','D-1':'0001110','A-1':'0110010','D+A':'0000010','D-A':'0010011',
 'A-D':'0000111','D&A':'0000000','D|A':'0010101',
 'M':'1110000','!M':'1110001','-M':'1110011','M+1':'1110111','M-1':'1110010',
 'D+M':'1000010','D-M':'1010011','M-D':'1000111','D&M':'1000000','D|M':'1010101'}
DEST = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

SYMBOLS = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
for i in range(16):
    SYMBOLS['R'+str(i)] = i

def clean(line):
    return line.split('//')[0].strip().replace(' ', '')

def assemble(path):
    lines = [clean(l) for l in open(path)]
    lines = [l for l in lines if l]

    # First pass: labels
    rom = 0
    code = []
    for l in lines:
        if l.startswith('('):
            SYMBOLS[l[1:-1]] = rom
        else:
            code.append(l)
            rom += 1

    # Second pass
    nextvar = 16
    out = []
    for l in code:
        if l.startswith('@'):
            s = l[1:]
            if s.isdigit():
                n = int(s)
            else:
                if s not in SYMBOLS:
                    SYMBOLS[s] = nextvar
                    nextvar += 1
                n = SYMBOLS[s]
            out.append(format(n, '016b'))
        else:
            dest = jump = ''
            if '=' in l:
                dest, l = l.split('=')
            if ';' in l:
                l, jump = l.split(';')
            out.append('111' + COMP[l] + DEST[dest] + JUMP[jump])
    return out

if __name__ == '__main__':
    inp = sys.argv[1]
    predefined = set(SYMBOLS.keys())
    result = assemble(inp)
    with open(inp.replace('.asm', '.hack'), 'w') as f:
        f.write('\n'.join(result) + '\n')

    # Extra feature (K mod 3 = 0): labels aur variables symbols.txt mein save
    with open('symbols.txt', 'w') as f:
        for name, addr in SYMBOLS.items():
            if name not in predefined:
                f.write(f'{name} = {addr}\n')