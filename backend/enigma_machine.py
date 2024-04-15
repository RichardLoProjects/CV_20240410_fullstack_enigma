class Reflector:
    def __init__(self, wiring:set) -> None:
        self.validate_reflector(wiring)
        self.wiring:set = wiring
    def validate_reflector(self, wiring:set) -> None:
        assert all(isinstance(pair, tuple) and len(pair) == 2 for pair in wiring
                   ), 'Reflector contains non-tuple elements or tuples of incorrect length.'
        assert len(wiring)==13, 'Wiring in Reflector class does not contain 13 pairs.'
        used_chars = set()
        for pair in wiring:
            assert (pair[0] not in used_chars) and (pair[1] not in used_chars),\
                'Conflict wiring in Reflector class.'
            used_chars.update({pair[0], pair[1]})
        assert len(used_chars)==26, 'Wiring in Reflector class does not contain 26 letters.'
        assert used_chars==ALPHABET, 'Wiring in Reflector class is not uppercase alphabet.'
    def reflect(self, char:str) -> str:
        for pair in self.wiring:
            if char == pair[0]:
                return pair[1]
            elif char == pair[1]:
                return pair[0]

class Rotor:
    def __init__(self, turnover:str, wiring:str) -> None:
        self.validate_rotor(turnover, wiring)
        self.turnover:str = turnover
        self.wiring:str = wiring
        self.signature:str = wiring
    def validate_rotor(self, turnover:str, wiring:str) -> None:
        assert len(turnover)==1, 'Turnover in Rotor class contains too many characters.'
        assert turnover.isalpha(), 'Turnover in Rotor class needs to be a letter.'
        assert wiring.isalpha(), 'Wiring in Rotor class contains non-letters.'
        assert len(set(wiring))==26 and len(wiring)==26, 'Wiring in Rotor class does not contain 26 letters.'
        assert set(wiring)==ALPHABET, 'Wiring in Rotor class is not uppercase alphabet.'
    def push(self, char:str) -> str:
        return self.wiring[ord(char)-ord('A')]
    def pull(self, char:str) -> str:
        return [chr(ord('A')+i) for i in range(26) if self.wiring[i]==char][0]
    def fwd_turn(self) -> None:
        self.wiring:str = self.wiring[1:] + self.wiring[0]
    def bkw_turn(self) -> None:
        self.wiring:str = self.wiring[-1] + self.wiring[:-1]
    def turn_next(self) -> bool:
        return self.turnover == self.wiring[0]

class RotorSet:
    def __init__(self, rotor1:Rotor, rotor2:Rotor, rotor3:Rotor) -> None:
        self.rotors:list = [rotor1, rotor2, rotor3]
    def rotate(self) -> None:
        self.rotors[0].fwd_turn()
        self.rotors[1].fwd_turn() if self.rotors[0].turn_next() else None
        self.rotors[2].fwd_turn() if self.rotors[1].turn_next() else None
    def push(self, char:str) -> str:
        for rotor in self.rotors:
            char = rotor.push(char)
        return char
    def pull(self, char:str) -> str:
        for rotor in reversed(self.rotors):
            char = rotor.pull(char)
        return char

class Plugboard:
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self.wiring = dict()
        self.connections = set()
    def attach_connection(self, char1:str, char2:str) -> None:
        assert all([ord('A')<=char<=ord('Z') for char in [char1, char2]]),\
            'Plugboard does not handle non-uppercase characters.'
        self.detach_connection(char1)
        self.detach_connection(char2)
        self.connections.update({char1, char2})
        self.wiring[char1] = char2
        self.wiring[char2] = char1
    def detach_connection(self, char:str) -> None:
        if char in self.connections:
            partner = self.wiring[char]
            del self.wiring[partner]
            self.connections.discard(partner)
            del self.wiring[char]
            self.connections.discard(char)
    def swap(self, char:str) -> str:
        return self.wiring.get(char, char)

class EnigmaMachine: # Assertion: no lowercase letters.
    def __init__(self, plugboard:Plugboard, rotors:RotorSet, reflector:Reflector) -> None:
        self.plugboard:Plugboard = plugboard
        self.rotors:RotorSet = rotors
        self.reflector:Reflector = reflector
    def map(self, char:str) -> str:
        self.rotors.rotate()
        char = self.plugboard.swap(char)
        char = self.rotors.push(char) # r1 r2 r3
        char = self.reflector.reflect(char)
        char = self.rotors.pull(char) # r3 r2 r1
        char = self.plugboard.swap(char)
        return char


ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
DEFAULT_REFLECTOR = Reflector({
    ('A','Y'), ('B','R'), ('C','U'),
    ('D','H'), ('E','Q'), ('F','S'),
    ('G','L'),
    ('I','P'), ('J','X'), ('K','N'),
    ('M','O'), ('T','Z'), ('V','W')
    }) # UKW-B reflector
BOX_OF_ROTORS = [
    Rotor('R','EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
    Rotor('F','AJDKSIRUXBLHWTMCQGZNPYFVOE'),
    Rotor('W','BDFHJLCPRTXVZNYEIWGAKMUSQO'),
    Rotor('K','ESOVPZJAYQUIRHXLNFTGKDCMWB'),
    Rotor('A','VZBRGITYUPSDNHLXAWMJQOFECK'),
    ] # i, ii, iii, iv, v
# https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables
# https://en.wikipedia.org/wiki/Enigma_machine#Turnover
DEFAULT_ROTORS = RotorSet(BOX_OF_ROTORS[0], BOX_OF_ROTORS[1], BOX_OF_ROTORS[2])
DEFAULT_PLUGBOARD = Plugboard()


'''
open website
press button -> backend does logic -> square lights up ... press light (pressing removes prev light)
lights clear after next button press 

enigma config
ability to randomise all settings (show user what config is set to)
choose 3 rotors from 5 (red, green blue yellow, neonpink)
ability to manually turn the rotor
ability to choose the plugboard
'''



def main():
    pass

if __name__ == '__main__':
    main()