$(document).ready(function() {
    "use strict"
    $(".btn_import_table").on("click", function(e){
        draw_chart(this);
    });

    $(".img_li").on("click", function(e){
        console.log($("input[name='ch_chart_type']:checked").prop("name"))
        draw_chart(this);
        console.log("this.id = " + $(this).children("input").attr("id"))
    });

    function draw_chart(th) {
        var t = $("input[name='ch_chart_type']:checked");
        var tbl_id = $(t).parent().parent().parent().find(" > div > div >select").val()
        var sheet_id = $(t).parent().parent().parent().find(" > div > div > input[name='sheet_id']").val()
        var sheet_name = $(t).parent().parent().parent().find(" > div > div > input[name='sheet_name']").val()
        // var sheet_row_count = $(t).parent().parent().parent().find(" > div > div > input[name='sheet_header']").val()
        var sheet_range = $(t).parent().parent().parent().find(" > div > div > input[name='sheet_range']").val()
        var chart_title = $(t).parent().parent().parent().find(" > div > div > input[name='chart_title']").val()
        console.log("chart_title = " + chart_title)
        var $tbl_area = $(t).parent().parent().parent().find(" > div[name='table_area']");
        var chart_type = "table";
        if ($(th).children("input").attr("id") == "btn_chart_columns") {
            chart_type = "columns";
        }else if ($(th).children("input").attr("id") == "btn_chart_combinations") {
            chart_type = "combinations";
        }else if ($(th).children("input").attr("id") == "btn_chart_bars") {
            chart_type = "bars";
        }else if ($(th).children("input").attr("id") == "btn_chart_funnel") {
            chart_type = "funnel";
        }else if ($(th).children("input").attr("id") == "btn_chart_lines") {
            chart_type = "lines";
        }else if ($(th).children("input").attr("id") == "btn_chart_area") {
            chart_type = "area";
        }else if ($(th).children("input").attr("id") == "btn_chart_pizza_1") {
            chart_type = "pizza_1";
        }else if ($(th).children("input").attr("id") == "btn_chart_pizza_2") {
            chart_type = "pizza_2";
        }else if ($(th).children("input").attr("id") == "btn_chart_radar") {
            chart_type = "radar";
        }else if ($(th).children("input").attr("id") == "btn_chart_histogram") {
            chart_type = "histogram";
        }
        $(t).parent().parent().parent().find(" > div > input[name='chart_type']").val(chart_type);
        $(t).parent().parent().find(" > div > input[name='ch_chart_type']").prop("checked", "true");
        $.ajax({
            url: "/get_sheet_data/" + sheet_id + "/" + sheet_name + "/" + sheet_range + "/" + chart_type + "/" + tbl_id + "/" + chart_title,
            type: "POST",
            datatype: "text",        
            success: function (result) { 
                $tbl_area.html(result)
                console.log(result)
            },
            error: function (error) {
                console.log(error)
            }       
        });
    }

    
    $("#btn_save_dashboard").on("click", function(e){
        var dash_name = $("#dashboard_name").val()
        // $.ajax({
        //     url: "/del_dash/" + dash_name,
        //     type: "POST",
        //     datatype: "text",        
        //     success: function (result) { 
        //         console.log(result)
        //     },
        //     error: function (error) {
        //         console.log(error)
        //     }       
        // });

        $("div[name='table_area']").each(function() {
            if ($(this).html() != "") {
                var tbl_id = $(this).parent().find(" > div > div >select").val()
                var sheet_id = $(this).parent().find(" > div > div > input[name='sheet_id']").val()
                var sheet_name = $(this).parent().find(" > div > div > input[name='sheet_name']").val()
                // var sheet_row_count = $(this).parent().find(" > div > div > input[name='sheet_header']").val()
                var sheet_range = $(this).parent().find(" > div > div > input[name='sheet_range']").val()
                var chart_title = $(this).parent().find(" > div > div > input[name='chart_title']").val()
                var $tbl_area = $(this).parent().find(" > div[name='table_area']");
                var chart_type = $(this).parent().find(" > div > input[name='chart_type']").val()
                var src = $(this).children("[name]").first().attr("name")
                console.log("this = " + $(this).html());
                console.log($(this).children("[name]").first().attr("name"));
                $.ajax({
                    url: "/save_dash/" + sheet_id + "/" + sheet_name + "/" + sheet_range + "/" + tbl_id + "/" + src + "/" + chart_title + "/" + dash_name + "/" + chart_type,
                    type: "POST",
                    datatype: "text",        
                    success: function (result) { 
                        console.log(result)
                    },
                    error: function (error) {
                        console.log(error)
                    }       
                });
            }
        });
    });

})