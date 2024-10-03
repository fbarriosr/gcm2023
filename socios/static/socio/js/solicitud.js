$(document).ready(function () {
   $("#patente").parent().hide() 
   $("#acompanantes").parent().hide()
   $("#auto").parent().hide()
   $("#autoLabel").hide()

   deuda = $('#deuda').val()
   recargo = $('#recargo').val()

   $('#cuota').css('border', '2px solid #BF9D5E');
   $('#recargo').css('border', '2px solid #BF9D5E');

   if (Number($('#recargo_invitado').val())== 0 ){

        $('#recargo_invitado').parent().hide()
        $("#cancela_deuda_socio").show()
        $('#deudaLabel').show()
        $('#recargo').parent().show()
        $('#deuda').parent().show()
        $('#detalle_cuotas_pagadas').parent().show()
        
        if (Number(deuda)== 0){
           $('#recargo').val(0)
           $("#cancela_deuda_socio").hide()
           $('#deudaLabel').hide()
           $('#recargoInvitado').hide()

       }


   }else{
        $("#cancela_deuda_socio").hide()
        $('#deudaLabel').hide()
        $('#recargo').parent().hide()
        $('#deuda').parent().hide()
        $('#detalle_cuotas_pagadas').parent().hide()

   }


   
   
   recargoInvitado = $('#recargo_invitado').val()
   cuota = $('#cuota').val()
   total =  Number(recargo) + Number(cuota) +Number(recargoInvitado) 
   $('#total').val(total)

});

$("#cancela_deuda_socio").change(function() {
    if(this.checked) {
      $('#deuda').css('border', '2px solid #BF9D5E');
      $('#recargo').css('border', '1px solid #dee2e6');

      recargoInvitado = $('#recargo_invitado').val()
      deuda = $('#deuda').val()
      cuota = $('#cuota').val()
      total =  Number(deuda) + Number(cuota)+ Number(recargoInvitado) 
      $('#total').val(total)
    }else{
      $('#recargo').css('border', '2px solid #BF9D5E');
      $('#deuda').css('border', '1px solid #dee2e6');
      recargo = $('#recargo').val()
      recargoInvitado = $('#recargo_invitado').val()
      cuota = $('#cuota').val()
      total =  Number(recargo) + Number(cuota)+ Number(recargoInvitado) 
      $('#total').val(total)
    }
});

$("#busCGM").change(function() {
    if(this.checked) {
        $('#recargo_bus').css('border', '2px solid #BF9D5E');
        x =  Number($('#recargo_bus').val())
        t =  Number($('#total').val())
        $('#total').val(t+x)
        $("#auto").prop("checked", false);
        $("#auto").parent().show()
        $("#autoLabel").show()

        
    }else{
        x =  Number($('#recargo_bus').val())
        t =  Number($('#total').val())
        $('#total').val(t-x)
        $('#recargo_bus').css('border', '1px solid #dee2e6');
        $("#auto").parent().hide()
        $("#autoLabel").hide()
        $("#patente").parent().hide() 
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
            if (error.responseText){
                mensaje= error.responseText
                //console.log(mensaje)
               
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
                if(obj.error.img){
                    m = 'Imagen Principal: '+ obj.error.img
                    notificacionError(m)
                }
                if(obj.error.img_files){
                    m = 'Lista de imagenes: '+ obj.error.img_files
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
            notificacionSuccessUrl('Creando Noticias', 'noticias')
            console.log(response.mensaje)   
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                //console.log(mensaje)
               
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
                if(obj.error.img){
                    m = 'Imagen Principal: '+ obj.error.img
                    notificacionError(m)
                }
                if(obj.error.img_files){
                    m = 'Lista de imagenes: '+ obj.error.img_files
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

function updateMultimedia(){
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
            notificacionSuccessUrl('Actualizando', 'multimedias')
            console.log(response.mensaje)   
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                //console.log(mensaje)
               
                obj = $.parseJSON(mensaje);
                if(obj.error.titulo){
                    m = 'Titulo: '+ obj.error.titulo
                    notificacionError(m)
                }
                if(obj.error.fecha){
                    m = 'Fecha: '+ obj.error.fecha
                    notificacionError(m)
                }
                if(obj.error.img){
                    m = 'Imagen Principal: '+ obj.error.img
                    notificacionError(m)
                }
                if(obj.error.img_files){
                    m = 'Lista de imagenes: '+ obj.error.img_files
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

function createMultimedia(){
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
            notificacionSuccessUrl('Creando Multimedias', 'multimedias')
            console.log(response.mensaje)   
        },
        error: function (error) {
            if (error.responseText){
                mensaje= error.responseText
                //console.log(mensaje)
               
                obj = $.parseJSON(mensaje);
                if(obj.error.titulo){
                    m = 'Titulo: '+ obj.error.titulo
                    notificacionError(m)
                }
                if(obj.error.fecha){
                    m = 'Fecha: '+ obj.error.fecha
                    notificacionError(m)
                }
                if(obj.error.img){
                    m = 'Imagen Principal: '+ obj.error.img
                    notificacionError(m)
                }
                if(obj.error.img_files){
                    m = 'Lista de imagenes: '+ obj.error.img_files
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

function eliminarMultimedia(){
    confirmEliminar= $('#eliminarMultimediaConfirm').val();
    console.log('Eliminando'); 
    if (confirmEliminar == 'Eliminar'){
       console.log('Eliminado'); 
       $.ajax({
            data:{
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
            },
            url: '/multimediaDelete',
            type: 'post',
            success: function (response) {
                Cookies.remove('multimediaId');
                notificacionSuccessUrl(response.mensaje,'multimedias')             
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
            notificacionSuccessUrl('Actualizando', 'calendario')
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
            notificacionSuccessUrl('Actualizando', 'calendario')
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
                notificacionSuccessUrl(response.mensaje,'calendario')             
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

function crearCookie(nombre, valor, url) {
    document.cookie = nombre + "=" + valor + ";path=/";
    console.log('cookie');
    window.location.href = url;
}
