console.log("I am running");

document.addEventListener('DOMContentLoaded', () => {
    const updateOutput = (message) => {
        const output = document.getElementById('output');
        output.textContent = message;
    };

    document.querySelectorAll('.turn-up').forEach(button => {
        button.addEventListener('click', () => {
            const rotorId = button.dataset.rotor;
            fetch('/turn_rotor', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ rotor_id: rotorId, direction: 'up' }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateOutput(`Rotor ${rotorId} turned up.`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });

    document.querySelectorAll('.turn-down').forEach(button => {
        button.addEventListener('click', () => {
            const rotorId = button.dataset.rotor;
            fetch('/turn_rotor', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ rotor_id: rotorId, direction: 'down' }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateOutput(`Rotor ${rotorId} turned down.`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });

    document.querySelectorAll('.add-plugboard').forEach(button => {
        button.addEventListener('click', () => {
            const plug1 = document.getElementById(button.dataset.plug1).value.toUpperCase();
            const plug2 = document.getElementById(button.dataset.plug2).value.toUpperCase();
            fetch('/add_plugboard_pair', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ pair: plug1 + plug2 }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateOutput(`Plugboard pair ${plug1}${plug2} added.`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });

    document.querySelectorAll('.remove-plugboard').forEach(button => {
        button.addEventListener('click', () => {
            const plug = document.getElementById(button.dataset.plug).value.toUpperCase();
            fetch('/remove_plugboard_pair', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ char: plug }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateOutput(`Plugboard pair ${plug} removed.`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });

    document.querySelectorAll('.keyboard-button').forEach(button => {
        button.addEventListener('click', () => {
            const char = button.textContent;
            fetch('/send_char', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ char: char }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.encrypted_char) {
                    updateOutput(`Encrypted Character: ${data.encrypted_char}`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });

    document.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', (event) => {
            const rotorId = event.target.id.replace('-select', '');
            const newRotorId = event.target.value;
            fetch('/change_rotor', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ old_rotor: rotorId, new_rotor_id: newRotorId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    updateOutput(`Rotor ${rotorId} changed to ${newRotorId}.`);
                } else {
                    updateOutput(`Error: ${data.error}`);
                }
            });
        });
    });
});
