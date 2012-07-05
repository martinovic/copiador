<?php

define("ORIGEN", "/var/www/Portal2");
define("DESTINO", "/media/244");
define("SSH", false);
define("REPOSITORIO", "svn://192.168.0.202/Portal2");

class copiador2{

	var $origen;

	var $destino;

	var $arrColores = array();

    var $arrRetorno = array();

	/**
	 * metodo lector de directorio
	 * @param string Ruta base de los archivos
	 * @return void
	 */
	public function reader($ruta){
        if ($gestor = opendir($ruta)) {
			/* Esta es la forma correcta de iterar sobre el directorio. */
			while (false !== ($entrada = readdir($gestor))) {
				if($entrada != "." && $entrada != ".." &&
						substr($entrada,0,1) != "." &&
						$entrada != "configurations" &&
						$entrada != "menues"  &&
						$entrada != "session" &&
						$entrada != "debug"  &&
						$entrada != "diseno_nuevo" &&
						$entrada != "accionesMasivasCsv" &&
						$entrada != "tem1" &&
						$entrada != "templates_c" &&
						$entrada != "upload" &&
						$entrada != "exportar"){
						
					if(is_dir($ruta."/".$entrada)){
						$this->reader($ruta."/".$entrada);
					} else {
						$archivo = $ruta."/".$entrada;
						$size = round((filesize($archivo)/1024), 2);
						$fileDate = date ("F d Y H:i:s.", filemtime($archivo));
						$directorios = str_replace("/var/www/Portal2", "/", $ruta);
						$file2 = $this->destino.$directorios."/".$entrada;
						
        
						//$crc1 = strtoupper(dechex(crc32(file_get_contents($archivo))));
                        $crc1= $fileDate = date ("F d Y H:i:s.", filemtime($archivo));
                        $this->arrRetorno[] = array($archivo => $crc1);
                    
					}
				}
			}
			closedir($gestor);
		}
        
        echo json_encode($this->arrRetorno);
        
        
    }
}
echo "iniciando la lectura";
$ruta = ORIGEN;
$destino = DESTINO;
$a = new copiador2();
$a->reader($ruta);

?>
