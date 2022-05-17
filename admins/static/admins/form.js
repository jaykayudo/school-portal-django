var staffType = document.getElementById('staff_type');
var teachingBox = document.getElementById('teaching_box');
var teachingBoxHtml = teachingBox.innerHTML;
// if(localStorage.getItem('class') === 'none'){
//     teachingBox.classList.remove('hidden')
// }
// else if (localStorage.getItem('class') == 'hidden'){
//     teachingBox.classList.add('hidden')
// }

staffType.addEventListener('change',function(e){
    if(e.target.value != "" && e.target.value == "t"){
        teachingBox.classList.remove('hidden');
        teachingBox.innerHTML = teachingBoxHtml
        // localStorage.setItem('class','none')
    }else if(e.target.value == "s"){
        teachingBox.classList.add('hidden');
        // localStorage.getItem('class','hidden')
        teachingBox.innerHTML = '';
    }
    else{
        teachingBox.classList.add('hidden');
    }
})