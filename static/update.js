document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('add_step_btn').addEventListener('click', addStep);
    document.getElementById('clear_steps_btn').addEventListener('click', clearSteps);
});

function addStep() {
    let steps = document.getElementById('steps').value;
    let date = document.getElementById('date').value;
    fetch('/add_step', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'steps': steps, 'date': date})
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            location.reload();
        }
    });
}

function clearSteps() {
    fetch('/clear_steps', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            location.reload();
        }
    });
}
