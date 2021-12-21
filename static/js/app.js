async function fetchDirectories() {
    const res = await fetch('/api/dirs');
    const dirs = await res.json();
    return dirs
}

fetchDirectories().then(dirs => {
    let directory_browser = document.getElementById("directory_browser");
    dirs.forEach(dir => {
        directory_browser.innerHTML += "<li>" + dir['name'] + "</li>";
    });
})
