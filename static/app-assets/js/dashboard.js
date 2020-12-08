$(document).ready(function() {
    "use strict"
    
    $("div[name='table_area']").each(function() {        
        if ($(this).html() != "") {
            var content = $(this).html()
            content = content.replace(/&lt;/g, "<")
            content = content.replace(/&gt;/g, ">")
            $(this).html(content)
            console.log("html = " + content)
        }
    });

    $(".tab-pane").first().addClass("active")
    $("a[name='tab_names']").first().addClass("active")
})


