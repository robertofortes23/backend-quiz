const quizContainer = document.getElementById("quiz-container");

const showQuiz = (questions) => {
  let html = "";
  questions.forEach((question) => {
    html += `<h2>${question.question_text}</h2>
             <h3>${question.subject}</h3>
             <h3>${question.topic}</h3>
             <h3>Ano: ${question.year}</h3>
             <button onclick="deleteQuestion(${question.id})">Delete</button>`;
    question.alternatives.forEach((alternative, index) => {
      html += `<label><input type="radio" name="${question.id}" value="${index}" /> ${alternative}</label><br />`;
    });
    html += "<br />";
  });
  quizContainer.innerHTML = html;
};

const deleteQuestion = (id) => {
  fetch(`http://localhost:5000/quiz/${id}`, { method: "DELETE" })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      getQuiz();
    })
    .catch((error) => console.error(error));
};

const getQuiz = () => {
  const subject = document.getElementById("subject").value;
  const year = document.getElementById("year").value;
  const topic = document.getElementById("topic").value;
  const random = document.getElementById("random").checked;
  const url = `http://localhost:5000/quiz?subject=${subject}&year=${year}&topic=${topic}&random=${random}`;
  fetch(url)
    .then((response) => response.json())
    .then((data) => showQuiz(data))
    .catch((error) => console.error(error));
};

const form = document.querySelector("form");
form.addEventListener("submit", (e) => {
  e.preventDefault();
  getQuiz();
});
