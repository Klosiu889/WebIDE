const gridContainer = document.getElementById("grid-container");

if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)){
    gridContainer.classList.add("grid-container-mobile");
} else {
    gridContainer.classList.add("grid-container-desktop");
}