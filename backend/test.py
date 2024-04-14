from backend.enigma_machine import *


def main():
    x = EnigmaMachine(DEFAULT_PLUGBOARD, DEFAULT_ROTORS, DEFAULT_REFLECTOR)
    s = 'HELLO WORLD... VERY LONG ENCRYPTED ENIGMA MACHINE SECRET MESSAGE HERE!!'
    print(s)
    s2 = ''
    for c in s:
        if c in ALPHABET:
            s2 += x.map(c)
        else:
            s2 += c
    print(s2)
    input('Press Enter to close the script...')

if __name__ == '__main__':
    main()