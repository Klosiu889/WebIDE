const tabContent = document.getElementsByClassName("options");
const processorOptions = document.getElementsByClassName("processor-radio");

for (let i = 0; i < processorOptions.length; i++) {
    processorOptions[i].addEventListener("click", (evt) => changeDependant(evt));
}

function changeDependant(evt) {
    const processorOptionID = evt.target.id;
    const dependentTab = document.getElementById("dependent-button");

    switch (processorOptionID) {
        case "mcs51":
            dependentTab.onclick = function() {openTab(event, 'dependent-mcs51')};
            break;
        case "z80":
            dependentTab.onclick = function() {openTab(event, 'dependent-z80')};
            break;
        case "stm8":
            dependentTab.onclick = function() {openTab(event, 'dependent-stm8')};
            break;
        default:
            dependentTab.onclick = function() {openTab(event, 'dependent')};
    }
}

function hideTabs() {
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
}

function openTab(evt, tabName) {
    hideTabs();
    document.getElementById(tabName).style.display = "block";
}

openTab(event, 'standard');