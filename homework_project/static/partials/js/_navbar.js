const url=window.location.href
const blueNav=["/homeworks","/homeworks/","/homeoworks/id","/profile"]
const transparentNav=["homepage","/register"]
const nav=document.querySelector('nav')
const toggle=document.querySelector('.navbar-toggler')

if(toggle){
    toggle.addEventListener('click',makeNavBlue)
}

blueNav.map((blue)=>{
    if(url.includes(blue)){
      makeNavBlue()
    }
})

transparentNav.map((tr)=>{
    if(url==="http://127.0.0.1:8000/"){
        makeTransparentByScroll(375)
    }
    else if(url.includes(tr)){
        makeTransparentByScroll(10)
    }
})


function makeNavBlue(){
    nav.classList.remove('bg-transparent')
    nav.classList.add('bg-darkblue')
    nav.classList.add('navbar-dark')
}


function makeTransparentByScroll(height){
    window.addEventListener("scroll",()=>{
        if(window.scrollY>height){
            nav.classList.remove('bg-transparent')
            nav.classList.add('bg-darkblue')
            nav.classList.add('navbar-dark')
        }
        else{
            nav.classList.remove('bg-darkblue')
            nav.classList.remove('navbar-dark')
        }   
    })
}