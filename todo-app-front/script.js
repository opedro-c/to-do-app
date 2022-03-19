// switch mode
// gerais
let body = document.querySelector('body')
let h1 = document.querySelector('h1')
let a = document.querySelectorAll('a')

// especificos
let btnSwitchMode = document.querySelector(".btnSwitchMode")
let iSwitchMode = document.querySelector(".iSwitchMode")
let wrapper = document.querySelector('.wrapper')
let controls = document.querySelector('.filters')
let btnClearAll = document.querySelector('.clear-btn')
let spanActive = document.querySelector('span.active')

btnSwitchMode.addEventListener('click', () => {
    const darkMode = iSwitchMode.classList.toggle('uil-sun')
    
    if(darkMode) {
        body.style.background = 'var(--invert-main-collor)'
        h1.style.color = 'white'

        wrapper.style.background = 'slategray'
        wrapper.style.boxShadow  = '4px 4px rgba(0, 0, 0, 0.25)'
        controls.style.color = 'white'
        btnClearAll.style.background = 'var(--invert-main-collor)'

    } else {
        body.style.background = ''
        h1.style.color = ''

        wrapper.style.background = ''
        wrapper.style.boxShadow = ''
        controls.style.color = ''
        btnClearAll.style.background = ''
    }
})

// system time and date
function relogio(){
    var data = new Date();
    var hor = data.getHours();
    var min = data.getMinutes();
    var seg = data.getSeconds();
    
    if(hor < 10){
        hor = "0" + hor;
    }
    if(min < 10){
        min = "0" + min;
    }
    if(seg < 10){
        seg = "0" + seg;
    }
    
    var horas = hor + ":" + min + ":" + seg;
    document.getElementById("rel").value = horas;
}

var timer = setInterval(relogio);

