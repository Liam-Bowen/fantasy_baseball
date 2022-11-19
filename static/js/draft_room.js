    function myFunction() {
        document.getElementById("myDropdown").classList.toggle("show");
    }
    window.onclick = function(event) {
        if(!event.target.matches('.drop')){
            var dropdowns = document.getElementsByClassName("dropdown-event");
            var i;
            for(i=0; i < dropdowns.length; i++){
                var openDropdown = dropdowns[i];
                if(openDropdown.classList.contains('show')){
                openDropdown.classList.remove('show');
                }
            }
        }
    }
    function pitchers(){
        var x = document.getElementById("pitchers");
        var y = document.getElementById("batters");
        if (window.getComputedStyle(x, null).getPropertyValue("display") === "none"){
            x.style.display = "block";
            y.style.display = "none";
        }
    }
    function batters(){
        var x = document.getElementById("pitchers");
        var y = document.getElementById("batters");
        if (window.getComputedStyle(x, null).getPropertyValue("display") === "block"){
            y.style.display = "block";
            x.style.display = "none";
        }
    }


