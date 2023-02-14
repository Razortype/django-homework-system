let button = document.getElementById('topBtn')

const functionforscroll = function(id){
    const reqId = "#"+id;
    window.scrollTo(0, $(reqId).offset().top-85);
}

window.onscroll = () => {
    if(document.body.scrollTop > 700 || document.documentElement.scrollTop > 700 ){
        button.style.opacity = "1";
        button.style.pointerEvents = "all";
    }
    else {
        button.style.opacity = "0";
        button.style.pointerEvents = "none"
    }
}

const topFunction = () => {
    document.body.scrollTop=0;
    document.documentElement.scrollTop=0;
}
