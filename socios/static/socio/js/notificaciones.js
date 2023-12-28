function notificacionSuccess(mensaje){
    // Display a success toast, with a title
        
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "progressBar": false,
          "preventDuplicates": true,
          "positionClass": "toast-top-right",
          "onclick": null,
          "showDuration": "400",
          "hideDuration": "1000",
          "timeOut": "7000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "onHidden": function () {
                location.replace(document.referrer);
              }
        };
        toastr.success(mensaje)
       
}

function notificacionSuccessUrl(mensaje, url){
    // Display a success toast, with a title
        
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "progressBar": false,
          "preventDuplicates": true,
          "positionClass": "toast-top-right",
          "onclick": null,
          "showDuration": "400",
          "hideDuration": "1000",
          "timeOut": "7000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut",
          "onHidden": function () {
                location.replace(url);
              }
        };
        toastr.success(mensaje)
       
}

function notificacionError(mensaje){
    // Display a success toast, with a title
        
        toastr.options = {
          "closeButton": true,
          "debug": false,
          "progressBar": false,
          "preventDuplicates": true,
          "positionClass": "toast-top-right",
          "onclick": null,
          "showDuration": "400",
          "hideDuration": "1000",
          "timeOut": "7000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        };
        toastr.error(mensaje,'ERROR')
}
