document.querySelectorAll(".navbar a").forEach(link => {
  if (link.href === location.href) {
    link.classList.add("active");
  }
});
