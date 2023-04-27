import time
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import sys

disable_warnings(InsecureRequestWarning)

dominio = ""
usuario =""
clave =""
ubicacion=""

ingresar = f'https://{dominio}/front/login.php'
seguimiento =f'https://{dominio}/front/ticket_user.form.php?id=' # modificar el seguimiento por correo
buscar_id_p1 = f'https://{dominio}/ajax/common.tabs.php?_target=/front/ticket.form.php&_itemtype=Ticket&_glpi_tab=Ticket$main&id='
enlace_valida_sesion=f'https://{dominio}/front/ticket.php'

with requests.session() as s:
# Aqui se buscan los campos mediante scrapping para el ingreso de los datos de inicio de sesión
	s2 = s.get(ingresar, verify = False)
	soup = BeautifulSoup(s2.content, "html.parser")
	username 	= soup.find("input",{"id":"login_name"})['name']
	password	= soup.find("input",{"id":"login_password"})['name']
	recuerdame 	= soup.find("input",{"id":"login_remember"})['name']
	token 		= '_glpi_csrf_token'
	valor_token = soup.find("input",{"name":"_glpi_csrf_token"})['value']

	payload = {
		'noAUTO'	: 1,
		username	: usuario,
		password	: clave,
		'auth'		: 'ldap-1',
		recuerdame	: 'on',
		token		: valor_token
		}
	# Se usa requests.session para mantener la sesion iniciada se envía el form con los datos
	s.post(ingresar, data=payload, verify = False)
	time.sleep(1)

	def deshabilita_correo(i,id):

		r = f'{seguimiento}{i}'

		p = s.get(r, verify = False)
		soup2 = BeautifulSoup(p.content, "html.parser")

		if soup2.find('input',{'name':'_glpi_csrf_token'}) == None:
			print(f'Id {i} es None')
		else:
			token2 = soup2.find("input",{"name":"_glpi_csrf_token"})['value']

			payload2 = {
			'use_notification'	: 0,
			'update'			: 'Guardar',
			'id'				: i,
			'_glpi_csrf_token'	: token2
			}

			s.post(r, data = payload2, verify = False)

			print(f"Peticion id: {id} - {i} - Ok")

	for x in range (int(sys.argv[1]),int(sys.argv[2])):
		buscar_id = f"{buscar_id_p1}{x}"
		b_id = s.get(buscar_id, verify = False)
		soup3 = BeautifulSoup(b_id.content, "html.parser")
		entidad = soup3.find('th',{'colspan':'4'})

# Aqui se filtra por entidad, se debe indicar la posicion del nombre de la entidad para comparar con la ubicacion deseada
		if str(entidad)[85:120] == ubicacion:
			enlaces = soup3.find_all('a',{'class':'pointer'})
			for lineas in enlaces:
				lin = str(lineas)
				if lin.startswith("<a class=\"pointer\" onclick=\" submitGetLink('/front/ticket_user.form.php', {'delete': 'delete'"):
					deshabilita_correo(int(lin[102:108]),x)
