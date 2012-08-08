/**
 * Esto es para submitir y hacer la busqueda sobre un
 * servidor en particular
 */
function submitirFormEntorno(){
    // alert('Ha seleccionado cambiar de entorno');
    generate('center', 'Ha seleccionado cambiar de entorno', 'alert');
    $('#form1').attr('action','/copiador');
}

function submitirFiltro(){
    //alert('Cambiando el filtro');
    generate('center', 'Cambiando el filtro', 'alert');
    $('#form1').attr('action','/copiador');
}
