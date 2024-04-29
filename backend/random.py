import random
from enigma_machine import *

def randomised_enigma() -> EnigmaMachine:
    # enigma config = rotors (5x4x3) x rotor positions (26**3) x plugboard (lots)
    # Step 1: generate rotors
    rotor_indices = [0,1,2,3,4]
    random.shuffle(rotor_indices)
    rotor_indices.pop(0)
    rotor_indices.pop(0)
    rotor_list:list = [
        Rotor.default(rotor_indices[0]),
        Rotor.default(rotor_indices[1]),
        Rotor.default(rotor_indices[2])
        ]
    # Step 2: turn rotors
    for i in range(3):
        for _ in range(random.randint(0,25)+1):
            rotor_list[i].fwd_turn()
    # Step 3: place rotors in rotor set
    rotors = RotorSet(*rotor_list)
    # Step 4: add plugboard connections
    available_char:set = {chr(ord('A')+i) for i in range(26)}
    for _ in range(random.randint(0,13)+1):
        pass
    return EnigmaMachine(Plugboard.default(), rotors, Reflector.default()).copy()



def main():
    ## Testing code would go here
    pass

if __name__ == '__main__':
    main()