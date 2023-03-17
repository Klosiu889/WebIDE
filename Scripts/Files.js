function loadTextFile(fileName, textContainer) {
    fetch(fileName)
        .then(response => response.text())
        .then(text => {
            const lines = text.split("\n");
            let numberedText = "";
            for (let i = 0; i < lines.length; i++) {
                numberedText += `<p class="line"><span class="line-number">${i + 1}:</span> ${lines[i]}</p>`;
            }
            textContainer.innerHTML = numberedText;
            textContainer.style.whiteSpace = "pre-wrap";
        })
        .catch(error => {
            console.error(error);
            textContainer.textContent = "Failed to load text file.";
        });
}

const codeContainer = document.getElementById("code-container");
const fragmentContainer = document.getElementById("fragment-container");

loadTextFile("Files/TroysWorkshop.txt", codeContainer);
loadTextFile("Files/TroysWorkshopFragment.txt", fragmentContainer);