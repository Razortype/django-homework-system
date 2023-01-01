let nav=document.querySelector('nav')
let brand=document.querySelector('.navbar-brand')
let link=document.querySelectorAll('.header__list>li>a')
let toggle=document.querySelector('.navbar-toggler')
let buttons=document.querySelectorAll('.header__person__buttons > button')
if(toggle){
    toggle.addEventListener('click',showNav)
}
window.addEventListener("scroll",()=>{
    if(window.scrollY>375){
        nav.classList.remove('bg-transparent')
        nav.classList.add('bg-darkblue')
        nav.classList.add('navbar-dark')
    }
    else{
        nav.classList.remove('bg-darkblue')
        nav.classList.remove('navbar-dark')
    }   
})

function showNav(){
    nav.classList.remove('bg-transparent')
    nav.classList.add('bg-darkblue')
    nav.classList.add('navbar-dark')

}  


