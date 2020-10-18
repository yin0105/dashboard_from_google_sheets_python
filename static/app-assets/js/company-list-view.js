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
  $("#main-menu-navigation > li:contains('Company')").addClass("active");
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
      {
        text: "<i class='feather icon-plus'></i> Adicionar novo",
        action: function() {
          $("#cur_cnpj").val("---")
          $("#comp_name").val("")
          $("#cnpj").val("")
          $("#email").val("")
          $("#standard_rate").val("")
          $("#improved_rate").val("")
          $("#btn_add_data").html("Adicionar Dados")
          
          $(this).removeClass("btn-secondary")
          $(".add-new-data").addClass("show")
          $(".overlay-bg").addClass("show")
        },
        className: "btn-outline-primary"
      }
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
  // Dropzone.options.dataListUpload = {
  //   complete: function(files) {
  //     var _this = this
  //     // checks files in class dropzone and remove that files
  //     $(".hide-data-sidebar, .cancel-data-btn, .actions .dt-buttons").on(
  //       "click",
  //       function() {
  //         $(".dropzone")[0].dropzone.files.forEach(function(file) {
  //           file.previewElement.remove()
  //         })
  //         $(".dropzone").removeClass("dz-started")
  //       }
  //     )
  //   }
  // }
  // Dropzone.options.dataListUpload.complete()

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
  
  $("#comp_name").val($(this).parent().siblings("[name='comp_name']").text())
  $("#cnpj").val($(this).parent().siblings("[name='cnpj']").text())
  $("#email").val($(this).parent().siblings("[name='email']").text())
  $("#standard_rate").val($(this).parent().siblings("[name='standard_rate']").text())
  $("#improved_rate").val($(this).parent().siblings("[name='improved_rate']").text())
  $("#logo").val($(this).parent().siblings("[name='logo']").text())
  $("#cur_cnpj").val($(this).parent().siblings("[name='cnpj']").text())
  $("#btn_add_data").html("Dados de atualização")
});

// On Delete
$('.action-delete').on("click", function(e){
  alert("del: " + $(this).parent().siblings("[name='cnpj']").text())
  e.stopPropagation();
  location.href = "/remove_company/" + $(this).parent().siblings("[name='cnpj']").text()
  
});
