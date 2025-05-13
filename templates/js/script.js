document.getElementById("spam-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const emailText = document.getElementById("emailText").value;
    const resultDiv = document.getElementById("result");
  
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: emailText }),
    });
  
    const data = await response.json();
    resultDiv.classList.remove("d-none");
  
    if (data.prediction === "spam") {
      resultDiv.className = "alert alert-danger mt-4";
      resultDiv.innerText = "⚠️ This email is classified as SPAM.";
    } else {
      resultDiv.className = "alert alert-success mt-4";
      resultDiv.innerText = "✅ This email is NOT SPAM.";
    }
  });
  