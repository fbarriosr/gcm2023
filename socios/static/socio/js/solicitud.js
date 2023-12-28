
$(document).ready(function () {
   deuda = $('#deuda').val()
   if (Number(deuda)== 0){
       $('#recargo').val(0)
       $("#cancela_deuda_socio").hide()
       $('#deudaLabel').hide()

   }
   recargo = $('#recargo').val()
   cuota = $('#cuota').val()
   total =  Number(recargo) + Number(cuota)
   $('#total').val(total)

});

$("#cancela_deuda_socio").change(function() {
    if(this.checked) {
      deuda = $('#deuda').val()
      cuota = $('#cuota').val()
      total =  Number(deuda) + Number(cuota)
      $('#total').val(total)
    }else{
      recargo = $('#recargo').val()
      cuota = $('#cuota').val()
      total =  Number(recargo) + Number(cuota)
      $('#total').val(total)
    }
});



function crearSolicitud(){

    var data = new FormData($('#form_edicion').get(0));
    console.log(data);
    $.ajax({
        data: $('#form_edicion').serialize(),
        url:  $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccessUrl(response.mensaje, '../torneos')
            //notificacionSuccess(response.mensaje)
            console.log(response.mensaje)  
        },
        error: function (error) {
            console.log(error.responseJSON.error)

        }
    });
    

}
