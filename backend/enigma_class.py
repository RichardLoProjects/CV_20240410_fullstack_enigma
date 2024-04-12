class EnigmaComponents:
    def __init__(self, wiring: dict) -> None:
        self.wiring: dict = {chr(ord('A')+i):chr(ord('A')+i) for i in range(26)}
        self.wiring.update(wiring)
    def map(self, char: str) -> str:
        return self.wiring[char]
    def validate_pairs(self) -> None:
        used_chars = set()
        for _, char in self.wiring.items():
            if char in used_chars:
                raise ValueError(f'Conflict in plugboard wiring: {char} is mapped to multiple characters.')
            used_chars.add(char)
        self.wiring.update({v:k for k,v in self.wiring.items()})
        if len(self.wiring) != 26:
            raise ValueError(f'The {type(self.wiring).__name__} does not contain 13 pairs.')

class Reflector(EnigmaComponents):
    def __init__(self, wiring: dict) -> None:
        super().__init__(wiring)
        self.validate_pairs()

class Rotor(EnigmaComponents):
    def __init__(self, wiring:dict , turnover: str) -> None:
        super().__init__(wiring)
        self.turnover: str = turnover
        self.position: int = 0
    def turn_fwd(self) -> None:
        self.position += 1
        self.position %= 26
    def turn_bkw(self) -> None:
        self.position += -1
        self.position %= 26

class Plugboard(EnigmaComponents):
    def __init__(self, wiring: dict) -> None:
        super().__init__(wiring)
        self.validate_pairs()

class EnigmaMachine:
    def __init__(self, plugboard: Plugboard, rotor1: Rotor, rotor2: Rotor,
                 rotor3: Rotor, reflector: Reflector) -> None:
        self.plugboard: Plugboard = plugboard
        self.rotors: list = [rotor1, rotor2, rotor3]
        self.reflector: Reflector = reflector
    def map(self, char: str) -> str:
        # map: plugb r1 r2 r3 refl r3 r2 r1 plugb
        char = self.plugboard.map(char)
        for i in range(len(self.rotors)):
            # 0,1,2
            char = self.rotors[i].map(char)
        char = self.reflector.map(char)
        for i in range(len(self.rotors)-1, -1, -1):
            # 2,1,0
            char = self.rotors[i].map(char)
        char = self.plugboard.map(char)
        return char

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