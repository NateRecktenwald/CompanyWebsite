function toggle_style() {
    let classes = document.getElementById("body").classList;
    if(classes[0] == "dark") {
        classes.remove("dark");
        localStorage.removeItem("theme");
    }
    else {
        classes.add("dark")
        localStorage.setItem("theme", "dark");
    }
}

if(localStorage.getItem("theme") != null) {
    document.getElementById("body").classList.add("dark");
}
else {
    document.getElementById("body").classList.remove("dark");
}

let button = document.getElementById("theme");
button.addEventListener('click', toggle_style);