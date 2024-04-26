import random
from enigma_machine import *

def randomised_enigma() -> EnigmaMachine:
    # enigma config = rotors (5x4x3) x rotor positions (26**3) x plugboard (lots)
    # Step 1: fetch new deep copy (we don't want to mutate)
    enigma = EnigmaMachine.default()
    # Step 2: generate rotors
    rotor_indices = [0,1,2,3,4]
    random.shuffle(rotor_indices)
    rotor_indices.pop(0)
    rotor_indices.pop(0)
    rotors = RotorSet(
        Rotor.default(rotor_indices[0]),
        Rotor.default(rotor_indices[1]),
        Rotor.default(rotor_indices[2])
        )
    # Step 3: turn rotors
    rotor_positions = [random.randint(0,25), random.randint(0,25), random.randint(0,25)]
    # Step 4: add plugboard connections
    num_pairs = random.randint(0,13)
    return enigma



def main():
    ## Testing code would go here
    pass

if __name__ == '__main__':
    main()