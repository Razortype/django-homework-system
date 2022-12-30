let nav=document.querySelector('nav')
let brand=document.querySelector('.navbar-brand')
let link=document.querySelectorAll('.header__list>li>a')
let toggle=document.querySelector('.navbar-toggler')
toggle.addEventListener('click',showNav)
window.addEventListener("scroll",()=>{
    if(window.scrollY>375){
        nav.classList.remove('bg-transparent')
        nav.classList.add('bg-darkblue')
        brand.classList.remove('text-dark')
        brand.classList.add('text-light')
        link.forEach((a)=>{
            a.classList.add('text-light')
        })
    }
    else{
        nav.classList.add('bg-transparent')
        brand.classList.remove('text-white')
        brand.classList.add('text-dark')
        link.forEach((a)=>{
            a.classList.remove('text-light')
        })
    }   
})

function showNav(){
    nav.classList.remove('bg-transparent')
    nav.classList.add('bg-darkblue')
    brand.classList.remove('text-dark')
    brand.classList.add('text-light')
    link.forEach((a)=>{
        a.classList.add('text-light')
    })

}  


