function addField() {
  const formContainer = document.getElementById("form-container");

  const formGroup = document.createElement("div");
  formGroup.classList.add("form-group");

  const input = document.createElement("input");
  input.type = "text";
  input.name = "song";
  input.placeholder = "Enter song name";
  input.required = "required";

  const removeButton = document.createElement("button");
  removeButton.type = "button";
  removeButton.classList.add("remove-button");
  removeButton.textContent = "Remove";
  removeButton.onclick = () => removeField(formGroup);

  formGroup.appendChild(input);
  formGroup.appendChild(removeButton);

  formContainer.appendChild(formGroup);
}

function removeField(formGroup) {
  const formContainer = document.getElementById("form-container");

  if (formContainer.children.length == 1) {
    alert("At least one field must be present.");
    return;
  }

  formContainer.removeChild(formGroup);
}

async function submitForm(event) {
  event.preventDefault();

  const songs = Array.from(document.querySelectorAll("input[name='song']"))
    .map((input) => input.value.trim().toLowerCase())
    .filter((song) => song);

  if (songs.length === 0) {
    alert("Please enter at least one song.");
    return;
  }

  const payload = { songs };

  try {
    const response = await fetch("http://localhost:5000/api/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(`Error: ${data.error || "An unexpected error occurred."}`);
      return;
    }

    if (data.songs.length === 0) {
      alert("No recommendations found.");
      return;
    }

    alert(`Recommendations:\n${data.songs.join(",\n")}`);
  } catch (error) {
    alert(`Error: ${error.message}`);
  }
}
