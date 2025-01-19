
function askAI() {
    const userInput = document.getElementById("user-input").value;

    if (!userInput.trim()) {
        alert("請輸入問題");
        return;
    }

    fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("ai-response").innerHTML = "AI: " + data.error;
            return;
        }
        document.getElementById("ai-response").innerHTML = "AI: " + data.answer;
        document.getElementById("judge_1").innerHTML = "評審 1: " + data.judges.judge_1;
        document.getElementById("judge_2").innerHTML = "評審 2: " + data.judges.judge_2;
    })
    .catch(error => {
        document.getElementById("ai-response").innerHTML = "AI: 伺服器錯誤";
        console.error("Error:", error);
    });
}
