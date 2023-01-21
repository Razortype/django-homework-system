const functionforscroll = function(id){
    const reqId = "#"+id;
    window.scrollTo(0, $(reqId).offset().top-85);
}