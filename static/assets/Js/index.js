function loading() {
  if (document.getElementById("file").value == "") return;
  el = document.querySelector(".loader");
  content = document.querySelector(".card-inner");
  el.style.display = "block";
  content.style.display = "none";
}
