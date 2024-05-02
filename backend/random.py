import random
from enigma_machine import *

def randomised_enigma() -> EnigmaMachine:
    # Step 1a: sample 3 rotors from a box of 5
    rotor_indices:list[int] = random.sample([1,2,3,4,5],k=3)
    rotors:list[Rotor] = [Rotor(rotor_indices[i]) for i in range(3)]
    # Step 1b: rotor positions
    for i in range(3):
        for _ in range(random.randint(0,26)):
            rotors[i].rotate()
    # Step 2: add plugboard connections
    plugboard = Plugboard()
    available_char:set = {chr(ord('A')+i) for i in range(26)}
    for _ in range(random.randint(0,13)):
        chars:list = random.sample(list(available_char),k=2)
        for c in chars:
            available_char.remove(c)
        plugboard.attach_pair(*chars)
        chars = []
    # Step 3: return randomised: rotors, rotor positions, plugboard
    return EnigmaMachine(rotors[0], rotors[1], rotors[2], plugboard)



def test() -> None:
    ## TESTING CODE
    m1 = randomised_enigma()
    print(m1.get_settings())
    m2 = m1.copy()
    s1 = 'HELLO WORLD... VERY LONG ENCRYPTED ENIGMA MACHINE SECRET MESSAGE!!'
    s2,s3 = '',''
    print(s1)
    for c in s1:
        s2 += m1.map(c)
    print(s2)
    for c in s2:
        s3 += m2.map(c)
    print(s3)

def main():
    for _ in range(3):
        test()

if __name__ == '__main__':
    main()