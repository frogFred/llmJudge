function askAI() {
    const userInput = document.getElementById("user-input").value.trim();

    if (!userInput) {
        alert("請輸入問題");
        return;
    }

    // 顯示使用者的問題到對話區
    const chatBox = document.getElementById("chat-history");
    const userMessage = document.createElement("div");
    userMessage.classList.add("user-message");
    userMessage.innerHTML = "你: " + userInput;
    chatBox.appendChild(userMessage);

    // 清空輸入框
    document.getElementById("user-input").value = "";

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
            displayMessage("AI: " + data.error, "ai-message");
            return;
        }

        displayMessage("AI: " + data.answer, "ai-message");
        document.getElementById("judge_1").innerHTML = "評審 1: " + data.judges.judge_1;
        document.getElementById("judge_2").innerHTML = "評審 2: " + data.judges.judge_2;
    })
    .catch(error => {
        displayMessage("AI: 伺服器錯誤", "ai-message");
        console.error("Error:", error);
    });
}

// 用來顯示訊息在對話區
function displayMessage(message, className) {
    const chatBox = document.getElementById("chat-history");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(className);
    messageDiv.innerHTML = message;
    chatBox.appendChild(messageDiv);
}
