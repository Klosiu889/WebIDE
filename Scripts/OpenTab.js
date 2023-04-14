function hideTabs() {
    const tabContent = document.getElementsByClassName("options");
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
}

function openTab(evt, tabName) {
    hideTabs();

    const tabContent = document.getElementsByClassName("options");
    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tabContent.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    console.log("Tab opened");
}

openTab(event, 'standard');