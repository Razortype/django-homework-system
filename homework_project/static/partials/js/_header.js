let nav=document.querySelector('nav')

window.addEventListener("scroll",()=>{
    if(window.scrollY>30){
        nav.classList.remove('bg-transparent')
        nav.classList.add('bg-dark')
    }
    else{
        nav.classList.add('bg-transparent')
    }   
})