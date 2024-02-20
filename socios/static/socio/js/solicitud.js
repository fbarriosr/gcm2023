$(document).ready(function () {
   $("#patente").parent().hide() 
   $("#acompanantes").parent().hide()
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

$("#carro").change(function() {
    if(this.checked) {
        $("#acompanantes").parent().show()
    }else{
        $("#acompanantes").parent().hide() 
    }
});


$("#auto").change(function() {
    if(this.checked) {
        $("#patente").parent().show()
    }else{
        $("#patente").parent().hide() 
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
            console.log(response.mensaje)  
        },
        error: function (error) {
            console.log(error) 

        }
    });
    

}

function updatePerfil(){
    var data = new FormData($('#form_edicion').get(0));
    console.log(data)
    $.ajax({
        data: $('#form_edicion').serialize(),
        url:  $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccessUrl('Actualizando', '../perfil')
            console.log(response.mensaje)   
        },
        error: function (error) {
            console.log(error)         
        }
    });
 
}

function updateRanking(){
    var data = new FormData($('#form_edicion').get(0));
    console.log(data)
    $.ajax({
        url:  $('#form_edicion').attr('action'),
        method: $('#form_edicion').attr('method'),
        type: $('#form_edicion').attr('method'),
        mimeType: $('#form_edicion').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'ranking')
            console.log(response.mensaje)   
        },
        error: function (error) {
            console.log(error)         
        }
    });
 
}
function updateNoticia(){
    var data = new FormData($('#form_edicion2').get(0));
    console.log(data)
    $.ajax({
        url:  $('#form_edicion2').attr('action'),
        method: $('#form_edicion2').attr('method'),
        type: $('#form_edicion2').attr('method'),
        mimeType: $('#form_edicion2').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'noticias')
            console.log(response.mensaje)   
        },
        error: function (error) {
            console.log(error)         
        }
    });
 
}

function createNoticia(){
    var data = new FormData($('#form_edicion2').get(0));
    console.log('data')
    console.log(data)
    $.ajax({
        url:  $('#form_edicion2').attr('action'),
        method: $('#form_edicion2').attr('method'),
        type: $('#form_edicion2').attr('method'),
        mimeType: $('#form_edicion2').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'noticias')
            console.log(response.mensaje)   
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                obj = $.parseJSON(mensaje);
                if(obj.error.titulo){
                    m = 'Titulo: '+ obj.error.titulo
                    notificacionError(m)
                }
                if(obj.error.fecha){
                    m = 'Fecha: '+ obj.error.fecha
                    notificacionError(m)
                }
                if(obj.error.resumen){
                    m = 'Resumen: '+ obj.error.resumen
                    notificacionError(m)
                }
                if(obj.error.info){
                    m = 'Información: '+ obj.error.info
                    notificacionError(m)
                }
                console.log(obj.error)
            }else{
                console.log(error) 
                notificacionError(error)
            }

                    
        }
    });
 
}

function eliminarNoticia(){
    confirmEliminar= $('#eliminarNoticiaConfirm').val();
    console.log('Eliminando'); 
    if (confirmEliminar == 'Eliminar'){
       console.log('Eliminado'); 
       $.ajax({
            data:{
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            url: '/noticiaDelete',
            type: 'post',
            success: function (response) {
                Cookies.remove('noticiaId');
                notificacionSuccessUrl(response.mensaje,'noticias')             
            },
            error: function (error) {
                console.log(error) 
                notificacionError(error);
            }
        });
       
    }
}
function abrir_modal_eliminacion(url) {
    id = '#'+url
    var newURL = window.location.protocol + "//" + window.location.host + "/" + url;
    console.log('id:', id)  
    console.log(newURL)

    $(id).load(newURL, function () {
        $(this).modal('show');
    });

}


function createTorneo(){
    var data = new FormData($('#form_edicion2').get(0));
    console.log('data')
    console.log(data)
    $.ajax({
        url:  $('#form_edicion2').attr('action'),
        method: $('#form_edicion2').attr('method'),
        type: $('#form_edicion2').attr('method'),
        mimeType: $('#form_edicion2').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'torneos')
            console.log(response.mensaje)   
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                obj = $.parseJSON(mensaje);
                if(obj.error.titulo){
                    m = 'Titulo: '+ obj.error.titulo
                    notificacionError(m)
                }
                if(obj.error.fecha){
                    m = 'Fecha: '+ obj.error.titulo
                    notificacionError(m)
                }
                if(obj.error.direccion){
                    m = 'Dirección: '+ obj.error.direccion
                    notificacionError(m)
                }
                if(obj.error.img){
                    m = 'Imagen: '+ obj.error.img
                    notificacionError(m)
                }
                console.log(obj.error)
            }else{
                console.log(error) 
                notificacionError(error)
            }
        
        }
    });
 
}

function updateTorneo(){
    var data = new FormData($('#form_edicion2').get(0));
    console.log(data)
    $.ajax({
        url:  $('#form_edicion2').attr('action'),
        method: $('#form_edicion2').attr('method'),
        type: $('#form_edicion2').attr('method'),
        mimeType: $('#form_edicion2').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'torneos')
            console.log(response.mensaje)   
        },
        error: function (error) {
            console.log(error)         
        }
    });
 
}

function eliminarTorneo(){
    confirmEliminar= $('#eliminarTorneoConfirm').val();
    console.log('Eliminando'); 
    if (confirmEliminar == 'Eliminar'){
       console.log('Eliminado'); 
       $.ajax({
            data:{
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            url: '/torneoDelete',
            type: 'post',
            success: function (response) {
                Cookies.remove('torneoId');
                notificacionSuccessUrl(response.mensaje,'torneos')             
            },
            error: function (error) {
                console.log(error) 
                notificacionError(error);
            }
        });
       
    }
}

function solicitudId(id,url){
   console.log('solicitudId:',id); 
   console.log('url:',url); 
   Cookies.set('solicitudId', id);
   location.href = url
}

function setId(id,url,varname){
   console.log('Id:',id); 
   console.log('url:',url); 
   Cookies.set(varname, id);
   location.href = url
}


function updateSolicitud(){
    var data = new FormData($('#form_edicion2').get(0));
    console.log(data)
    $.ajax({
        url:  $('#form_edicion2').attr('action'),
        method: $('#form_edicion2').attr('method'),
        type: $('#form_edicion2').attr('method'),
        mimeType: $('#form_edicion2').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'solicitudes')
            console.log(response.mensaje)   
        },
        error: function (error) {
            console.log(error)         
        }
    });
 
}

function updateUsuario(){
    var data = new FormData($('#form_edicion').get(0));
    console.log(data)
    $.ajax({
        url:  $('#form_edicion').attr('action'),
        method: $('#form_edicion').attr('method'),
        type: $('#form_edicion').attr('method'),
        mimeType: $('#form_edicion').attr('enctype'),
        processData : false,
        contentType: false,
        cache: false,
        data: data,
        success: function (response) {
            notificacionSuccessUrl('Actualizando', 'listarUsuarios')
            console.log(response.mensaje)   
        },
         error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                obj = $.parseJSON(mensaje);
                if(obj.error.rut){
                    m = 'Rut: '+ obj.error.rut
                    notificacionError(m)
                }
                console.log(obj.error)
            }else{
                console.log(error) 
                notificacionError(error)
            }
        
        }
    });
 
}

function crearUsuario(){

    var data = new FormData($('#form_edicion').get(0));
    console.log(data);
    $.ajax({
        data: $('#form_edicion').serialize(),
        url:  $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        success: function (response) {
            notificacionSuccessUrl(response.mensaje, 'listarUsuarios')
            console.log(response.mensaje)  
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                obj = $.parseJSON(mensaje);
                if(obj.error.rut){
                    m = 'Rut: '+ obj.error.rut
                    notificacionError(m)
                }
                console.log(obj.error)
            }else{
                console.log(error) 
                notificacionError(error)
            }
        
        }
    });
    

}