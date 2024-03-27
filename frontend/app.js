document.addEventListener("DOMContentLoaded", () => {
    const taskInput = document.getElementById("task-input");
    const runTaskBtn = document.getElementById("run-task-btn");
    const outputText = document.getElementById("output-text");

    runTaskBtn.addEventListener("click", async () => {
        const task = taskInput.value;
        if (task) {
            const response = await fetch("/api/run-task", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ task }),
            });

            if (response.ok) {
                const data = await response.json();
                outputText.textContent = data.output;
            } else {
                outputText.textContent = "Error running task.";
            }
        }
    });
});