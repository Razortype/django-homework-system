function openNav() {
    if(window.innerWidth<576){
    document.getElementById("mySidebar").style.width = "100%";
    }
    else{
      document.getElementById("mySidebar").style.width = "250px";
      document.getElementById("main").style.marginLeft = "250px";
    }
  }
  
  function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft= "0";
  }