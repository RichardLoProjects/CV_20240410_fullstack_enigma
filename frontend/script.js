console.log("Hello World");

/*


rotor
(rotor{i}{part} -- i=1,2,3 -- part=box,pos,up,down)
	dropdown box [1-5] (back)
	up/down button (back)
	position (fwd)
lamp
lamp
	char (fwd)
keyboard
{c} -- A,B,C,...,Z
	button (back)
plugboard
plug{i}a plug{i}b -- i=1,2,3,...,13
	verify available char then (back)


THE PLAN

function pingBackend(action, data){}

document.getElementbyId().addEventListener
rotor up/down
keyboard buttons

find a way to constantly get enigma settings
(up to date rotor, rotor pos)

find a way to do rotor dropdownboxes
find a way to do plugboard dropdownboxes

how to code lamp output


*/

document.addEventListener('DOMContentLoaded', function(){
    // Handle requests
    function sendRequest(action, data){
        console.log(`action:${action}, data:${data}, char:${data['char']}, pair:${data['pair']}, rotor:${data['rotor']}`);
    }
    // End requests

    // Rotor (box, pos-GET, up, down)
    const rotorLabel = ['slow', 'midl', 'fast']
    for (let i=1; i<=3; i++){
        document.getElementById(`rotor${i}box`).addEventListener('change', function(){
            sendRequest(
                'r',
                {
                    'rotor':rotorLabel[i-1],
                    'new_rotor':document.getElementById(`rotor${i}box`).value
                }
            );
        });
        document.getElementById(`rotor${i}up`).addEventListener('click', function(){
            sendRequest('u', {'rotor':rotorLabel[i-1]});
        });
        document.getElementById(`rotor${i}down`).addEventListener('click', function(){
            sendRequest('d', {'rotor':rotorLabel[i-1]});
        });
    }
    // End rotor

    // Lampboard (char-GET)
    // End Lamp

    // Keyboard
    const keyboard = document.querySelectorAll('.keyboard button');
    keyboard.forEach(button => {
        button.addEventListener('click', function(){
            sendRequest('m', {'char':button.id});
        });
    });
    // End keyboard

    // Plugboard
    const maxPlugboardPairs = 13;
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    let selectedLetters = new Set();
    function populatePlug (elementId){
        const select = document.getElementById(elementId);
        const currentValue = select.value;
        select.innerHTML = '';
        const defaultOption = document.createElement('option');
        defaultOption.value = ' ';
        defaultOption.textContent = ' ';
        select.appendChild(defaultOption);
        alphabet.split('').forEach(letter => {
            const option = document.createElement('option');
            option.value = letter;
            option.textContent = letter;
            if (selectedLetters.has(letter) && letter !== currentValue){
                option.disabled = true;
            }
            if (letter === currentValue){
                option.selected = true;
            }
            select.appendChild(option);
        });
    }
    function populatePlugboard (){
        for (let i=1; i<=maxPlugboardPairs; i++){
            populatePlug(`plug${i}a`);
            populatePlug(`plug${i}b`);
        }
    }
    function getSelectedLetters (){
        selectedLetters.clear();
        for (let i=0; i<maxPlugboardPairs; i++){
            const selectA = document.getElementById(`plug${i}a`);
            const selectB = document.getElementById(`plug${i}b`);
            if (selectA && selectA.value) selectedLetters.add(selectA.value);
            if (selectB && selectB.value) selectedLetters.add(selectB.value);
        }
    }
    populatePlugboard();
    for (let i=1; i<=maxPlugboardPairs; i++){
        const selectA = document.getElementById(`plug${i}a`);
        const selectB = document.getElementById(`plug${i}b`);
        function handleChange(){
            getSelectedLetters();
            populatePlugboard();
            if (alphabet.includes(selectA.value) && alphabet.includes(selectB.value)){
                console.log(`A:${selectA.value} and B:${selectB.value}`)
                sendRequest('a', {'pair':[selectA.value, selectB.value]});
            } else {
                if (selectA.value && selectA.value != ' ') sendRequest('k', {'char':selectA.value});
                if (selectB.value && selectB.value != ' ') sendRequest('k', {'char':selectB.value});
            }
        }
        if (selectA) selectA.addEventListener('change', handleChange);
        if (selectB) selectB.addEventListener('change', handleChange);
    }
    // End plugboard
});
    
