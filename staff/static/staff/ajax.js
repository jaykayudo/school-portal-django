function getSchedule(Element,data){
    var loader = document.getElementById('loader');
    Element.innerHTML = ""
        if(loader){
            loader.classList.remove('hidden')
            }
    $.ajax({
        url:"get-schedule/",
        type:"get",
        data:{date:data},
        success:function(response){
            if(response.schedule.length > 0){
                
                var html = ""
                for(var x = 0; x < response.schedule.length; x++){
                    html = `<div class='box-content'><p>${response.schedule[x].description}</p><footer class='flex-between' style='padding: 5px 2px;'><span>${response.schedule[x]['_class__name']?response.schedule[x]._class__name:'No class involved'}</span><span><i class='fa-solid fa-clock'>&nbsp;${response.schedule[x].time}</i></span></footer></div>`
                      Element.innerHTML += html
                }
                if(loader){
                    loader.classList.add('hidden')
                }
            // response.forEach(element => {
            //     html = "<div class='box-content'><p>`${element.description}`</p><footer class='flex-between' style='padding: 5px 2px;'><span>`${reponse.class?response.class:'No class involved'}`</span><span><i class='fa-solid fa-clock'>&nbsp;{{response.time}}</i></span></footer></div>"
            //     Element.innerHtml+= html
            // });
            // console.log(response.schedule)
            }
            else{
                // console.log('hey')
                if(loader){
                    loader.classList.add('hidden')
                }
                Element.innerHTML = "<div class='no-item'><p>No Schedule Uploads yet</p></div>"
            }
            
        },
        error:function(error){
            console.log(error);
            // alert(error);
            if(loader){
                loader.classList.add('hidden')
            }
            Element.innerHTML = "<div class='no-item'><p> Error fetching data</p></div>"
        }
    })
}