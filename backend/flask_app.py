from flask import Flask, render_template, request, jsonify
from enigma_machine import EnigmaMachine, Rotor

app = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend'
)
enigma_machine = EnigmaMachine.default()
rotor_set = {'slow','midl','fast'}
box_of_rotor_ids = {1,2,3,4,5}

@app.route('/')
def index():
    return render_template('index.html')

# a, k, r, u, d, g, m
@app.route('/add_plugboard_pair', methods=['POST'])
def add_plugboard_pair():
    data = request.get_json()
    pair = data.get('pair', '').upper()
    if len(pair) == 2 and pair.isalpha():
        enigma_machine.attach_plugs(pair[0], pair[1])
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Invalid plugboard pair. Must be two letters.'}), 400

@app.route('/remove_plugboard_pair', methods=['DELETE'])
def remove_plugboard_pair():
    data = request.get_json()
    char = data.get('char', '').upper()
    if char.isalpha() and len(char) == 1:
        enigma_machine.detach_plugs(char)
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Need a valid letter to delete plugboard pair.'}), 400

@app.route('/change_rotor', methods=['PATCH'])
def change_rotor():
    data = request.get_json()
    old_rotor = data['old_rotor']
    new_rotor_id = int(data['new_rotor_id'])
    if old_rotor in rotor_set and new_rotor_id in box_of_rotor_ids:
        enigma_machine.change_rotor(old_rotor, Rotor(new_rotor_id))
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Need a valid rotors.'}), 400

@app.route('/turn_rotor', methods=['PATCH'])
def turn_rotor():
    data = request.get_json()
    direction = data['direction']
    rotor_id = data['rotor_id']
    if rotor_id in rotor_set:
        match direction:
            case 'up':
                enigma_machine.turn_rotor_fwd(rotor_id)
            case 'down':
                enigma_machine.turn_rotor_bwd(rotor_id)
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Cannot turn invalid rotor.'}), 400

@app.route('/send_char', methods=['POST'])
def send_char():
    data = request.get_json()
    old_char = data['char'].upper()
    new_char = enigma_machine.map(old_char)
    return jsonify({'encrypted_char': new_char})



def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
