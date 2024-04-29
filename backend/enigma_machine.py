'''
press button -> backend does logic -> square lights up ... press light (pressing removes prev light)
lights clear after next button press 

enigma config = rotors (5x4x3) x rotor positions (26**3) x plugboard (lots)

rotor colours (red, green blue yellow, neonpink)
ability to manually turn the rotor
ability to choose the plugboard

ability to randomise all settings (show user what config is set to)
'''


class Reflector:
    ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
    _wiring:set = {
        ('A','Y'), ('B','R'), ('C','U'), ('D','H'), ('E','Q'), ('F','S'),
        ('G','L'), ('I','P'), ('J','X'), ('K','N'), ('M','O'), ('T','Z'), ('V','W')
        } # UKW-B reflector's wiring
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
                'Conflicting wiring in Reflector class.'
            used_chars.update({pair[0], pair[1]})
        assert len(used_chars)==26, 'Wiring in Reflector class does not contain 26 letters.'
        assert used_chars==Reflector.ALPHABET, 'Wiring in Reflector class is not uppercase alphabet.'
    @classmethod
    def default(cls):
        return Reflector(cls._wiring.copy())
    def copy(self):
        return Reflector(self.wiring.copy())
    def reflect(self, char:str) -> str:
        for pair in self.wiring:
            if char == pair[0]:
                return pair[1]
            elif char == pair[1]:
                return pair[0]

class Rotor:
    ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
    _DEFAULT:list = [
        ('R','EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
        ('F','AJDKSIRUXBLHWTMCQGZNPYFVOE'),
        ('W','BDFHJLCPRTXVZNYEIWGAKMUSQO'),
        ('K','ESOVPZJAYQUIRHXLNFTGKDCMWB'),
        ('A','VZBRGITYUPSDNHLXAWMJQOFECK'),
        ] # i, ii, iii, iv, v
    # https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables
    # https://en.wikipedia.org/wiki/Enigma_machine#Turnover
    def __init__(self, turnover:str, wiring:str) -> None:
        self.validate_rotor(turnover, wiring)
        self.turnover:str = turnover
        self.wiring:str = wiring[:]
        self.signature:str = wiring[:]
    def validate_rotor(self, turnover:str, wiring:str) -> None:
        assert len(turnover)==1, 'Turnover in Rotor class contains too many characters.'
        assert turnover.isalpha(), 'Turnover in Rotor class needs to be a letter.'
        assert wiring.isalpha(), 'Wiring in Rotor class contains non-letters.'
        assert len(set(wiring))==26 and len(wiring)==26, 'Wiring in Rotor class does not contain 26 letters.'
        assert set(wiring)==Rotor.ALPHABET, 'Wiring in Rotor class is not uppercase alphabet.'
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
    def copy(self):
        return Rotor(self.turnover[:], self.wiring[:])
    @classmethod
    def default(cls, rotor_id:int):
        return Rotor(cls._DEFAULT[:][rotor_id][0], cls._DEFAULT[:][rotor_id][1]).copy()

class RotorSet:
    ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
    def __init__(self, rotor1:Rotor, rotor2:Rotor, rotor3:Rotor) -> None:
        self.rotors:list = [rotor1.copy(), rotor2.copy(), rotor3.copy()]
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
    def copy(self):
        return RotorSet(*[rotor.copy() for rotor in self.rotors])
    @classmethod
    def default(cls):
        return RotorSet(Rotor.default(0), Rotor.default(1), Rotor.default(2))

class Plugboard:
    ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
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
    def copy(self):
        copied_plugboard = Plugboard()
        copied_plugboard.wiring = self.wiring.copy()
        copied_plugboard.connections = self.connections.copy()
        return copied_plugboard
    @classmethod
    def default(cls):
        return Plugboard().copy()

class EnigmaMachine:
    ALPHABET:set = {chr(ord('A')+i) for i in range(26)}
    def __init__(self, plugboard:Plugboard, rotors:RotorSet, reflector:Reflector) -> None:
        self.plugboard:Plugboard = plugboard
        self.rotors:RotorSet = rotors
        self.reflector:Reflector = reflector
    def map(self, char:str) -> str:
        assert not (ord('a')<=ord(char)<=ord('z')), 'This enigma machine does not handle lowercase letters.'
        return self._map(char) if ord('A') <= ord(char) <= ord('Z') else char
    def _map(self, char:str) -> str:
        self.rotors.rotate()
        char = self.plugboard.swap(char)
        char = self.rotors.push(char) # r1 r2 r3
        char = self.reflector.reflect(char)
        char = self.rotors.pull(char) # r3 r2 r1
        char = self.plugboard.swap(char)
        return char
    def copy(self):
        # https://realpython.com/python-mutable-vs-immutable-types/#mutability-in-custom-classes
        return EnigmaMachine(self.plugboard.copy(), self.rotors.copy(), self.reflector.copy())
    @classmethod
    def default(cls):
        return EnigmaMachine(Plugboard.default(), RotorSet.default(), Reflector.default()).copy()


def main():
    ## TESTING CODE
    ## The main function just tests the 5 classes defined above.
    ## make 2 enigma machine instances
    ## define some strings
    ## get s2 by encrypting s1
    ## get s3 by decrypting s2 (assert s1==s3)
    ## get s5 by encrypting s4 (showcase same char maps to diff letters)
    m1 = EnigmaMachine.default()
    m2 = EnigmaMachine.default()
    s1 = 'HELLO WORLD... VERY LONG ENCRYPTED ENIGMA MACHINE SECRET MESSAGE!!'
    s2,s3,s5 = '','',''
    s4 = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    print(s1)
    for c in s1:
        s2 += m1.map(c)
    print(s2)
    for c in s2:
        s3 += m2.map(c)
    print(s3)
    print(s4)
    for c in s4:
        s5 += m1.map(c)
    print(s5)

if __name__ == '__main__':
    main()