$(document).ready(function() {
    // if ($("#msg").val() != "") {
    //     alert($("#msg").val());
    // }
    
    // console.log("OK");
    // console.log($("#msg").val());
})

$("#register").click(function() {
    if ($("#password").val() != $("#conf_password").val()) {
        alert("Senha incorreta");
        $("#conf_password").val("");
        $("#conf_password").focus();        
    }else {
        $("#myform").submit()
    }
})