let draggedTask = null;

function allowDrop(event) {
    event.preventDefault(); 
}

function drag(event) {
    draggedTask = event.target;
    event.dataTransfer.setData("text/plain", event.target.dataset.id);
}

function drop(event) {
    event.preventDefault();

    const taskId = event.dataTransfer.getData("text/plain");
    const container = event.target.closest(".task-container");

    if (!container) return;

    const newStatus = container.dataset.status;
    const taskElement = document.querySelector(`.task[data-id="${taskId}"]`);

    if (taskElement && container !== taskElement.parentElement) {
        container.appendChild(taskElement);

        fetch(`/update_task/${taskId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ status: newStatus })
        }).then(response => {
            if (!response.ok) {
                alert("Fehler beim Aktualisieren des Tasks.");
            }
        });
    }
}
