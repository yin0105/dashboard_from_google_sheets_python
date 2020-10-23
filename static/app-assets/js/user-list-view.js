/*=========================================================================================
    File Name: data-list-view.js
    Description: List View
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy  - Vuejs, HTML & Laravel Admin Dashboard Template
    Author: PIXINVENT
    Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

$(document).ready(function() {
  "use strict"
  // init list view datatable
  function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
  }

  $("#main-menu-navigation > li:contains('User')").addClass("active");

  $("input[name='user_id']").each(function () {
    console.log("user_id = " + $(this).prop("value"))
  });

  if (getCookie("admin") == '0') {
    $("#approve_field").css("display", "none");
  }
 
  // $('td[name="photo"] > img').each(function() {
  //   var img_src = $(this).prop("src")
  //   if (img_src.substring(img_src.length - 6, img_src.length) == "photo/") {
  //     $(this).parent("td").html("<input type='file' name='photo_file'>");
  //   }
  // });

  $("input[name='photo_file']").change(function() {
    if ($(this).val() != "") {
      $(this).parent().parent().children("input[name='update_type']").val("photo");
      $(this).parent().parent().parent().submit();
    }
  });

  $("select[name='company']").change(function() {
    console.log("company = " + $(this).val())
  });

  $('#company').multiselect({
    // columns: 3,
    placeholder: 'Select Companies',
    search: true,
    searchOptions: {
        'default': 'Search Companies'
    },
    selectAll: true
  });
    
  var dataListView = $(".data-list-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
        checkboxes: { selectRow: true }
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[4, 10, 15, 20], [4, 10, 15, 20]],
    select: {
      style: "multi"
    },
    order: [[1, "asc"]],
    bInfo: false,
    pageLength: 4,
    buttons: [
      {
        text: "<i class='feather icon-plus'></i> Add New aaa",
        action: function() {
          $(this).removeClass("btn-secondary")
          $(".add-new-data").addClass("show")
          $(".overlay-bg").addClass("show")
          $("#data-name, #data-price").val("")
          $("#data-category, #data-status").prop("selectedIndex", 0)
        },
        className: "btn-outline-primary"
      }
    ],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  });

  dataListView.on('draw.dt', function(){
    setTimeout(function(){
      if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
      }
    }, 50);
  });

  // init thumb view datatable
  var dataThumbView = $(".data-thumb-view").DataTable({
    responsive: false,
    columnDefs: [
      {
        orderable: true,
        targets: 0,
        checkboxes: { selectRow: true }
      }
    ],
    dom:
      '<"top"<"actions action-btns"B><"action-filters"lf>><"clear">rt<"bottom"<"actions">p>',
    oLanguage: {
      sLengthMenu: "_MENU_",
      sSearch: ""
    },
    aLengthMenu: [[4, 10, 15, 20], [4, 10, 15, 20]],
    select: {
      style: "multi"
    },
    order: [[1, "asc"]],
    bInfo: false,
    pageLength: 4,
    buttons: [
    ],
    initComplete: function(settings, json) {
      $(".dt-buttons .btn").removeClass("btn-secondary")
    }
  })

  dataThumbView.on('draw.dt', function(){
    setTimeout(function(){
      if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
      }
    }, 50);
  });

  // To append actions dropdown before add new button
  var actionDropdown = $(".actions-dropodown")
  actionDropdown.insertBefore($(".top .actions .dt-buttons"))


  // Scrollbar
  if ($(".data-items").length > 0) {
    new PerfectScrollbar(".data-items", { wheelPropagation: false })
  }

  // Close sidebar
  $(".hide-data-sidebar, .cancel-data-btn, .overlay-bg").on("click", function() {
    $(".add-new-data").removeClass("show")
    $(".overlay-bg").removeClass("show")
    $("#data-name, #data-price").val("")
    $("#data-category, #data-status").prop("selectedIndex", 0)
  })   

  // dropzone init
  Dropzone.options.dataListUpload = {
    complete: function(files) {
      var _this = this
      // checks files in class dropzone and remove that files
      $(".hide-data-sidebar, .cancel-data-btn, .actions .dt-buttons").on(
        "click",
        function() {
          $(".dropzone")[0].dropzone.files.forEach(function(file) {
            file.previewElement.remove()
          })
          $(".dropzone").removeClass("dz-started")
        }
      )
    }
  }
  Dropzone.options.dataListUpload.complete()

  // mac chrome checkbox fix
  if (navigator.userAgent.indexOf("Mac OS X") != -1) {
    $(".dt-checkboxes-cell input, .dt-checkboxes").addClass("mac-checkbox")
  }
})



// On Edit
$('.action-edit').on("click",function(e){
  e.stopPropagation();
  $(".add-new-data").addClass("show");
  $(".overlay-bg").addClass("show");
  
  $("#user_name").val($(this).parent().siblings("[name='user_name']").text())
  $("#lastname").val($(this).parent().siblings("[name='lastname']").text())
  $("#email").val($(this).parent().siblings("[name='email']").text())
  $("#password").val($(this).parent().siblings("[name='password']").text())
  if ($(this).parent().siblings("[name='approve']").text() == "True") {
    $("#approve").prop("checked", true)
  }else {
    $("#approve").prop("checked", false)
  }
  
  $("#company").val($(this).parent().siblings("[name='companies']").text())

  $("#cur_user").val($(this).parent().siblings("[name='user_id']").prop("value"))
  $("#btn_add_data").html("Dados de atualização")
});

// On Delete
$('.action-delete').on("click", function(e){
  e.stopPropagation();
  location.href = "/remove_user/" + $(this).parent().siblings("[name='user_id']").val()
 
});

$('td[name="photo"] > img').on("click", function(e){
  e.stopPropagation();
  console.log("img clicked")
 
});
