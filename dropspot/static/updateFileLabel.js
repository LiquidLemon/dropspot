function updateFileLabel(files) {
  let form = files.length == 1 ? "file" : "files";
  document.getElementById("files-label").innerHTML = files.length + " " + form + " selected";
}
