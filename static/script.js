let quizData = [];
let currentQuestionIndex = 0;
let questionResults = [];
let startTime, timerInterval, mistakesThisQuestion = 0;

async function fetchQuestions() {
  const res = await fetch("/api/questions");
  quizData = await res.json();
  loadQuestion();
}

function startTimer() {
  startTime = performance.now();
  timerInterval = setInterval(updateTimer, 100);
}

function stopTimer() {
  clearInterval(timerInterval);
}

function updateTimer() {
  const now = performance.now();
  const elapsed = ((now - startTime) / 1000).toFixed(2);
  document.getElementById("timer").textContent = `${elapsed} 秒`;
}

function loadQuestion() {
  const q = quizData[currentQuestionIndex];
  mistakesThisQuestion = 0;
  document.getElementById("result").textContent = "";
  document.getElementById("nextContainer").style.display = "none";
  document.getElementById("timer").textContent = "0.00 秒";
  document.getElementById("question").textContent = `Q${currentQuestionIndex + 1}: ${q.question}`;
  const optionsContainer = document.getElementById("options");
  optionsContainer.innerHTML = "";

  q.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.textContent = option;
    button.onclick = () => checkAnswer(index);
    optionsContainer.appendChild(button);
  });

  startTimer();
}

function checkAnswer(selectedIndex) {
  const q = quizData[currentQuestionIndex];
  const result = document.getElementById("result");

  if (selectedIndex === q.correct) {
    stopTimer();
    const elapsed = ((performance.now() - startTime) / 1000).toFixed(2);
    result.textContent = `正解！ 解答時間：${elapsed} 秒／ 間違い：${mistakesThisQuestion} 回`;
    result.style.color = "green";

    fetch("/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question_id: q.id,
        time: parseFloat(elapsed),
        mistakes: mistakesThisQuestion
      })
    });

    document.querySelectorAll("#options button").forEach(btn => btn.disabled = true);
    document.getElementById("nextContainer").style.display = "block";
  } else {
    mistakesThisQuestion++;
    result.textContent = `不正解… ${mistakesThisQuestion} 回目のミスです`;
    result.style.color = "red";
  }
}

function nextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < quizData.length) {
    loadQuestion();
  } else {
    showFinalResult();
  }
}

function showFinalResult() {
  document.querySelector(".quiz").innerHTML = `<h2>クイズ終了！</h2><p>お疲れさまでした！</p>`;
}

window.onload = fetchQuestions;
