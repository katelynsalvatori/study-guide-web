function toggleDisplay(displayId) {
    var currDisplay = document.getElementById(displayId).style.display;
    document.getElementById(displayId).style.display = currDisplay === "none" ? "" : "none";
}