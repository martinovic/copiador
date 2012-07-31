/**
 * Esto es para submitir y hacer la busqueda sobre un
 * servidor en particular
 */
function submitirFormEntorno(){
    alert('Ha seleccionado cambiar de entorno');
    $('#form1').attr('action','/copiador');
}

function submitirFiltro(){
    alert('Cambiando el filtro');
    $('#form1').attr('action','/copiador');
}
