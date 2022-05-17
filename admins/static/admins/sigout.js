var logoutModal = document.getElementById("logout-modal");
var logoutModalClose = document.getElementById("logout-close");
logoutModalClose.addEventListener("click", function () {
  logoutModal.classList.add("hidden");
});
var logoutModalOpen = document.getElementById("logout-open");
logoutModalOpen.addEventListener("click", function () {
  logoutModal.classList.remove("hidden");
});
