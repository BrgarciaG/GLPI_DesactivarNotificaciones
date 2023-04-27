# GLPI_DesactivarNotificaciones

El siguiente script tiene por objetivo desactivar las notificaciones por correo de todos los involucrados en las peticiones GLPI para evitar el bloqueo de envio de correos masivos cuando se cierran multiples .
Se accede al dominio usando scrapping (Beautifull Soup)

Para poder ejecutar el script se deben instalar los módulos necesarios

python3 -m pip install -r requirements.txt

Uso: 

deshabilitar_correo.py [id_petición desde] [id_peticion hasta]

también se considera un filtro por entidad para deshabilitar unicamente las notificaciones a una entidad específica.

