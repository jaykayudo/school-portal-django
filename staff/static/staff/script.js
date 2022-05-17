window.onload = function () {
    Smart('#calendar', class {
    get properties() {
        return {"selectedDates":[new Date(),"2022-7-17"]}
    }
});
// document.querySelector('smart-calendar').view = 'landscape';
}
var logoutModal = document.getElementById('logout-modal');
    var logoutModalClose = document.getElementById('logout-close');
    logoutModalClose.addEventListener('click',function(){
        logoutModal.classList.add('hidden');
    });
    var logoutModalOpen = document.getElementById('logout-open');
    logoutModalOpen.addEventListener('click',function(){
        logoutModal.classList.remove('hidden');
    });