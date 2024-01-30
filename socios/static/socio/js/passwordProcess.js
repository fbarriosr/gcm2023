$(document).ready(function(){

// Example 1
    var options1 = {};
    options1.ui = {
        container: "#pwd-container1",
        showVerdictsInsideProgressBar: true,
        viewports: {
            progress: ".pwstrength_viewport_progress1"
        }
    };
    options1.common = {
        debug: false,
    };
    $('.progressPassword').pwstrength(options1);
});

function cambiarPassword(){
    $.ajax({
        data: $('#form_edicion').serialize(),
        url:  $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccess(response.mensaje);
        },
        error: function (error) {
            console.log(error.responseJSON.error)
            if (error.responseJSON.error.password2)
                notificacionError(error.responseJSON.error.password2);
            else 
                notificacionError(error.responseJSON.error);
        }
    });
}
