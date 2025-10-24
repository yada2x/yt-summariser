const btn = document.getElementById("summariseBtn");
const output = document.getElementById("output");
const textarea = document.getElementById("inputText");

btn.addEventListener("click", async () => {
  const response = await fetch("/summarise", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: textarea.value })
  });
  const data = await response.json();
  output.textContent = data.summary;
});
