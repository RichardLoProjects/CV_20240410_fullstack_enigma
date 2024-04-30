import random
from enigma_machine import *

def randomised_enigma() -> EnigmaMachine:
    # Step 1a: sample 3 rotors from a box of 5
    rotor_indices:list = random.sample([0,1,2,3,4],k=3)
    rotor_list:list = [Rotor.default(rotor_indices[i]) for i in range(3)]
    # Step 1b: rotor positions
    for i in range(3):
        for _ in range(random.randint(0,26)):
            rotor_list[i].fwd_turn()
    # Step 2: add plugboard connections
    plugboard = Plugboard.default()
    available_char:set = {chr(ord('A')+i) for i in range(26)}
    for _ in range(random.randint(0,13)):
        chars:list = random.sample(list(available_char),k=2)
        for c in chars:
            available_char.remove(c)
        plugboard.attach_connection(*chars)
        chars = []
    # Step 3: return randomised: rotors, rotor positions, plugboard
    return EnigmaMachine(plugboard, RotorSet(*rotor_list), Reflector.default()).copy()



def test() -> None:
    ## TESTING CODE
    m1 = randomised_enigma()
    print(m1.read_config())
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