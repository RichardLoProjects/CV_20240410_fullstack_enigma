from flask import Flask, render_template, request, jsonify
from enigma_machine import EnigmaMachine, Rotor

app = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend'
)
enigma_machine:EnigmaMachine = EnigmaMachine.default()
valid_actions:set = {'a','k','r','u','d','m'}
rotor_set:set = {'slow','midl','fast'}
box_of_rotor_ids:set = {1,2,3,4,5}

## At least 2 routes needed to: return html for rendering, and handle JS requests
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_requests', methods=['POST']) # If database, consider: 'GET','PATCH','DELETE'
def handle_request():
    data:dict = request.get_json()
    action = data['action']
    assert action in valid_actions
    match action:
        case 'a':
            # Expecting len-2 tuple of uppercase char A-Z
            enigma_machine.attach_plugs(*data['pair'])
            return jsonify({'status':'success'})
        case 'k':
            # Expecting len-1 uppercase char A-Z
            enigma_machine.detach_plugs(data['char'])
            return jsonify({'status':'success'})
        case 'r':
            assert data['rotor'] in rotor_set
            assert data['new_rotor'] in box_of_rotor_ids
            enigma_machine.change_rotor(data['rotor'], Rotor(int(data['new_rotor'])))
            return jsonify({'status':'success'})
        case 'u':
            assert data['rotor'] in rotor_set
            enigma_machine.turn_rotor_fwd(data['rotor'])
            return jsonify({'status':'success'})
        case 'd':
            assert data['rotor'] in rotor_set
            enigma_machine.turn_rotor_bwd(data['rotor'])
            return jsonify({'status':'success'})
        case 'g':
            return jsonify({
                'status':'success',
                'settings':enigma_machine.get_settings()
            })
        case 'm':
            # Expecting len-1 uppercase char A-Z
            return jsonify({
                'status':'success',
                'encrypted_char':enigma_machine.map(data['char'])
            })
        case _:
            pass


def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
