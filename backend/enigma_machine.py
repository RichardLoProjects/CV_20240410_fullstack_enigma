'''
press button -> backend does logic -> square lights up ... press light (pressing removes prev light)
lights clear after next button press or 10 seconds pass

rotor colours (red, green blue yellow, neonpink)
ability to randomise all settings (show user what config is set to)

todo
ability to manually customise: rotors, rotor pos, plugboard (set-data methods in enigma class)

result:
open python
open js

there is a enigma machine (plugboard buttons, keyboard, rotors displaying position, rotor buttons)
can choose rotor based on dropdown box (omit rotors already used)
can turn rotor (up button, down button)
can construct plugboard 1 pair at a time (26 dropdown boxes- omit char already used - incl option to remove)
show keyboard (keyboard buttons light up)
user input (click or type -- only accept alphabet A-Z)

change setting (frontend graphic done internally) frontend -> change enigma backend -> (does not output to front)
input char frontend -> enigma backend -> output char to lamp frontend
'''

class EnigmaUtils:
    ALPHABET_UPPER:frozenset = frozenset({chr(ord('A')+i) for i in range(26)})
    ALPHABET_LOWER:frozenset = frozenset({chr(ord('a')+i) for i in range(26)})
    # https://realpython.com/python-mutable-vs-immutable-types/#mutability-in-custom-classes
    # list, set, dict, customUserClasses are mutable
    #
    # https://en.wikipedia.org/wiki/Enigma_rotor_details#Rotor_wiring_tables
    # https://en.wikipedia.org/wiki/Enigma_machine#Turnover
    #
    # https://youtu.be/G2_Q9FoD-oQ
    # Possible configurations for enigma...
    #     60 rotors (choose 3 from box of 5): 60 == 5x4x3
    #     17,576 rotor positions: 17576 == 26**3
    #     150,738,274,937,250 plugboard (assume 10 pairs): 150738274937250 == 26!/((6!)(10!)(2**10))
    # == 158,962,555,217,826,360,000
    # ie... enigma config = rotors (5x4x3) x rotor positions (26**3) x plugboard (lots)

class FrozenDict(dict):
    def __setitem__(self, key, value) -> None:
        raise TypeError("FrozenDict does not support item assignment.")
    def __delitem__(self, key) -> None:
        raise TypeError("FrozenDict does not support item deletion.")
    def clear(self) -> None:
        raise TypeError("FrozenDict does not support clear.")
    def pop(self, key, default=None) -> None:
        raise TypeError("FrozenDict does not support pop.")
    def popitem(self) -> None:
        raise TypeError("FrozenDict does not support popitem.")
    def setdefault(self, key, default=None) -> None:
        raise TypeError("FrozenDict does not support setdefault.")
    def update(self, *args, **kwargs) -> None:
        raise TypeError("FrozenDict does not support update.")
    def __repr__(self) -> str:
        return f"FrozenDictionary({super().__repr__()})"

class Rotor:
    NUMBER:FrozenDict = FrozenDict({'R':1, 'F':2, 'W':3, 'K':4, 'A':5})
    BOX:FrozenDict = FrozenDict({
        1:tuple('R'+'EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
        2:tuple('F'+'AJDKSIRUXBLHWTMCQGZNPYFVOE'),
        3:tuple('W'+'BDFHJLCPRTXVZNYEIWGAKMUSQO'),
        4:tuple('K'+'ESOVPZJAYQUIRHXLNFTGKDCMWB'),
        5:tuple('A'+'VZBRGITYUPSDNHLXAWMJQOFECK'),
    })
    def __init__(self, rotor_id:int, position:int=0) -> None:
        self._ID:int = rotor_id
        self._NOTCH:str = Rotor.BOX[rotor_id][0]
        self._WIRING:tuple[str] = tuple(Rotor.BOX[rotor_id][1:])
        self._position:int = position
    def forward(self, char:str) -> str:
        index = (ord(char)-ord('A') + self._position)%26
        return self._WIRING[index]
    def bakward(self, char:str) -> str:
        index = (self._WIRING.index(char) - self._position)%26
        return chr(ord('A') + index)
    def at_notch(self) -> bool:
        return self._position == ord(self._NOTCH)-ord('A')
    def rotate(self) -> None:
        self._position = (self._position+1)%26
    def reverse(self) -> None:
        self._position = (self._position-1)%26
    def set_position(self, position:int) -> None:
        while self._position != (position%26):
            self.rotate()
    def get_settings(self) -> tuple:
        return (self._ID, self._position)
    def copy(self):
        return Rotor(self._ID, self._position)

class Plugboard:
    def __init__(self) -> None:
        self._wiring:dict = dict()
        self._connections:set = set()
    def swap(self, char:str) -> str:
        return self._wiring.get(char, char)
    def attach_pair(self, char1:str, char2:str) -> None:
        assert all([char in EnigmaUtils.ALPHABET_UPPER for char in [char1, char2]]),\
            'Plugboard does not handle non-uppercase characters.'
        self.detach_pair(char1)
        self.detach_pair(char2)
        self._connections.update({char1, char2})
        self._wiring[char1] = char2
        self._wiring[char2] = char1
    def detach_pair(self, char:str) -> None:
        assert char in EnigmaUtils.ALPHABET_UPPER,\
            'Plugboard does not handle non-uppercase characters.'
        if char in self._connections:
            partner = self._wiring[char]
            del self._wiring[partner]
            self._connections.discard(partner)
            del self._wiring[char]
            self._connections.discard(char)
    def reset(self) -> None:
        for c in self._connections.copy():
            self.detach_pair(c)
    def get_settings(self) -> set:
        return {(k,v) for k,v in self._wiring.items() if (k < v)}
    def copy(self):
        copied_plugboard:Plugboard = Plugboard()
        copied_plugboard._wiring = self._wiring.copy()
        copied_plugboard._connections = self._connections.copy()
        return copied_plugboard

class EnigmaMachine:
    ## User methods: add/remove plugboard pair, pick rotor, turn rotor up/down, map
    _REFLECT = FrozenDict({
        'A':'Y','B':'R','C':'U','D':'H','E':'Q','F':'S','G':'L','I':'P','J':'X','K':'N','M':'O','T':'Z','V':'W',
        'Y':'A','R':'B','U':'C','H':'D','Q':'E','S':'F','L':'G','P':'I','X':'J','N':'K','O':'M','Z':'T','W':'V'
    }) # UKW-B reflector
    def __init__(self, slow_rotor:Rotor, mid_rotor:Rotor, fast_rotor:Rotor, plugboard:Plugboard) -> None:
        self._plugboard:Plugboard = plugboard
        self._rotors:dict[str,Rotor] = {'slow':slow_rotor, 'midl':mid_rotor, 'fast':fast_rotor}
    def attach_plugs(self, char1:str, char2:str) -> None:
        assert all(c in EnigmaUtils.ALPHABET_UPPER for c in [char1, char2]),\
            'Plugboard does not handle non-uppercase characters.'
        self._plugboard.attach_pair(char1, char2)
    def detach_plugs(self, char:str) -> None:
        assert char in EnigmaUtils.ALPHABET_UPPER,\
            'Plugboard does not handle non-uppercase characters.'
        self._plugboard.detach_pair(char)
    def change_rotor(self, old_rotor_label:str, new_rotor:Rotor) -> None:
        assert old_rotor_label in {'slow', 'midl', 'fast'}, 'Invalid rotor label.'
        self._rotors[old_rotor_label] = new_rotor
    def turn_rotor_fwd(self, rotor_label:str) -> None:
        self._rotors[rotor_label].rotate()
    def turn_rotor_bwd(self, rotor_label:str) -> None:
        self._rotors[rotor_label].reverse()
    def map(self, char:str) -> str:
        assert char not in EnigmaUtils.ALPHABET_LOWER, 'Enigma machine does not handle lowercase letters.'
        return self._map(char) if char in EnigmaUtils.ALPHABET_UPPER else char
    def _map(self, char:str) -> str:
        self._rotate()
        char = self._plugboard.swap(char)
        char = self._rotors['fast'].forward(char)
        char = self._rotors['midl'].forward(char)
        char = self._rotors['slow'].forward(char)
        char = EnigmaMachine._REFLECT[char]
        char = self._rotors['slow'].bakward(char)
        char = self._rotors['midl'].bakward(char)
        char = self._rotors['fast'].bakward(char)
        char = self._plugboard.swap(char)
        return char
    def _rotate(self) -> None:
        self._rotors['fast'].rotate()
        self._rotors['midl'].rotate() if self._rotors['fast'].at_notch() else None
        self._rotors['slow'].rotate() if self._rotors['midl'].at_notch() else None
    def get_settings(self) -> tuple:
        return (
            self._rotors['slow'].get_settings(),
            self._rotors['midl'].get_settings(),
            self._rotors['fast'].get_settings(),
            self._plugboard.get_settings()
        )
    def copy(self):
        return EnigmaMachine(
            self._rotors['slow'].copy(),
            self._rotors['midl'].copy(),
            self._rotors['fast'].copy(),
            self._plugboard.copy()
        )
    @classmethod
    def default(cls):
        return EnigmaMachine(Rotor(3), Rotor(2), Rotor(1), Plugboard())


def test():
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

def main():
    enigma_machine = EnigmaMachine.default()
    action = ''
    action_prompt = (
        '\n'
        'Actions: '
        'Add plug (a), '
        'Kill plug (k), '
        'Change rotor (r), '
        'Turn rotor up (u), '
        'Turn rotor down (d), '
        'Set rotor position (s)'
        'Get settings (g), '
        'Send message (m)'
        '\n'
        'Desired user action: '
    )
    print('To quit, type "quit" when prompted for an action.')
    while action != 'quit':
        action = input(action_prompt)
        match action: # a, k, r, u, d, s, g, m, quit
            case 'a': # Add pair to plugboard
                c1 = input('Char 1: ').upper()
                c2 = input('Char 2: ').upper()
                enigma_machine.attach_plugs(c1, c2)
            case 'k': # Remove pair from plugboard
                c_ = input('Char: ').upper()
                enigma_machine.detach_plugs(c_)
            case 'r': # Change existing rotor for new rotor
                old_rotor = input('Current rotor (slow, midl, fast): ')
                new_rotor = int(input('New rotor ID (1-5): '))
                enigma_machine.change_rotor(old_rotor, Rotor(new_rotor))
            case 'u': # Turn rotor up
                rotor_id = input('Current rotor (slow, midl, fast): ')
                num_turns = int(input('Number of turns: '))
                for _ in range(num_turns):
                    enigma_machine.turn_rotor_fwd(rotor_id)
            case 'd': # Turn rotor down
                rotor_id = input('Current rotor (slow, midl, fast): ')
                num_turns = int(input('Number of turns: '))
                for _ in range(num_turns):
                    enigma_machine.turn_rotor_bwd(rotor_id)
            case 's': # Set rotor position
                rotor_id = input('Current rotor (slow, midl, fast): ')
                rotor_pos = int(input('Set rotor position to '))
                id_to_index = {'slow':0, 'midl':1, 'fast':2}
                while rotor_pos != enigma_machine.get_settings()[id_to_index[rotor_id]][1]:
                    enigma_machine.turn_rotor_fwd(rotor_id)
            case 'g': # Show enigma settings
                print(enigma_machine.get_settings())
            case 'm': # Encrypt/decrypt a message
                msg = input('Your message: ')
                encrypted_msg = ''
                for c in msg:
                    encrypted_msg += enigma_machine.map(c.upper())
                print(f'Encrypted message: {encrypted_msg}')
            case _:
                pass

if __name__ == '__main__':
    main()