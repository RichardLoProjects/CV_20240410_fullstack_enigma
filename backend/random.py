import random
from enigma_machine import *

def randomised_enigma() -> EnigmaMachine:
    # enigma config = rotors (5x4x3) x rotor positions (26**3) x plugboard (lots)
    # Step 1: generate rotors
    rotor_indices:list = random.sample([0,1,2,3,4],3)
    rotor_list:list = [Rotor.default(rotor_indices[i]) for i in range(3)]
    # Step 2: turn rotors
    for i in range(3):
        for _ in range(random.randint(0,26)):
            rotor_list[i].fwd_turn()
    # Step 3: place rotors in rotor set
    rotors = RotorSet(*rotor_list)
    # Step 4: add plugboard connections
    plugboard = Plugboard.default()
    available_char:set = {chr(ord('A')+i) for i in range(26)}
    for _ in range(random.randint(0,13)):
        chars:list = random.sample(list(available_char),2)
        for c in chars:
            available_char.remove(c)
        plugboard.attach_connection(*chars)
        chars = []
    return EnigmaMachine(plugboard, rotors, Reflector.default()).copy()



def main():
    ## Testing code would go here
    m1 = randomised_enigma()
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

if __name__ == '__main__':
    main()