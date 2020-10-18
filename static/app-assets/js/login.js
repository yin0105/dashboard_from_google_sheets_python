$(document).ready(function() {
    if ($("#msg").val() != "") {
        alert($("#msg").val());
    }
    
    console.log("OK");
    console.log($("#msg").val());
})

$("#remember_me").change(function() {
    console.log("ok")
    console.log($(this).prop("checked"))
    $("input[name='remember']").val($(this).prop("checked"))
})