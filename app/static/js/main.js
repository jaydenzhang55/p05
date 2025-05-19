// Will Nzeuton, Andy Shyklo, Kyle Lee, Margie Cao
// JOY ACROSS BORDERS 🔥🔥😵‍💫 by madeinguatemala
// SoftDev
// p04
// 2025-03-28

document.addEventListener("DOMContentLoaded", function () {

  const nav = document.getElementById("nav")
  nav.innerHTML = `
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="/">🔥🔥😵‍💫</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <a class="nav-link" href="/map">Map</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/profile">Profile</a>
      </li>
    </ul>

    <ul class="navbar-nav ml-auto">
      <li class="nav-item">
        <a class="nav-link" href="/login">Login</a>
      </li>        
      <li class="nav-item">
        <a class="nav-link" href="/register">Register</a>
      </li>
      <li class="nav-item">
        <form class="form-inline my-2 my-lg-0" method="POST" action="/logout">
          <button class="btn btn-outline-success my-2 my-sm-0" aria-label="Logout" type="submit">Logout</button>
        </form>
      </li>
    </ul>
  </div>
</nav>
  `

});

function openStat(evt, stat) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(stat).style.display = "block";
  evt.currentTarget.className += " active";
}
