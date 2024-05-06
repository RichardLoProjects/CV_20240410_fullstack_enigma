document.getElementById('getDataBtn').addEventListener('click', function() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('output').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
