# Control de Gastos
> Pablo Uribe Zuluaga


Se propone una aplicacion para llevar el control de ingresos y egresos de las personas para saber si derrochan dinero o si destinan mas dinero de lo necesario a algo en concreto.

## Endpoints

> PREFIJO GLOBAL /api/v2

<br>

Usuarios
> PREFIJO /users

|DESCRIPCION|VERBO|URI|DATA ENVIADA|ESTADO|
|-|-|-|-|-|
|Crea un usuario|POST|/|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"id": "1054398068",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"email": "pablo.uribez@autonoma.edu.co",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"name": "Pablo",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"lastname": "Uribe",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"status": "active"<br>}|201|
|Lista todos los usuarios|GET|/|-|200|
|Detalle de un usuario|GET|/{id}|-|200|
|Actualiza un usuario|PUT|/{id}|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"id": "1054398068",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"email": "pablo.uribez@autonoma.edu.co",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"name": "Pablo",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"lastname": "Uribe",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"status": "active"<br>}|201|
|Elimina un usuario|DELETE|/{id}|-|200|

<br><br>

Categorías
> PREFIJO /categories

|DESCRIPCION|VERBO|URI|DATA ENVIADA|ESTADO|
|-|-|-|-|-|
|Crea una categoria|POST|/|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"type": "income",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"name": "Bienes raices",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"description": "Monthly rent",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"user": "1054398068"<br>}|201|
|Lista todas las categorias|GET|/|-|200|
|Detalle de una categoria|GET|/{id}|-|200|
|Actualiza una categoria|PUT|/{id}|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"type": "income",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"name": "Bienes raices",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"description": "Monthly rent"<br>}|201|
|Elimina una categoria|DELETE|/{id}|-|200|

<br><br>

Ingresos
> PREFIJO /incomes

|DESCRIPCION|VERBO|URI|DATA ENVIADA|ESTADO|
|-|-|-|-|-|
|Crea un ingreso|POST|/|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"description": "4 horas de trading",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"amount": 250000,<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"category": 2<br>}|201|
|Lista todos los ingresos|GET|/|-|200|
|Detalle de un ingreso|GET|/{id}|-|200|
|Elimina un ingreso|DELETE|/{id}|-|200|

<br><br>

Egresos
> PREFIJO /expenses

|DESCRIPCION|VERBO|URI|DATA ENVIADA|ESTADO|
|-|-|-|-|-|
|Crea un egreso|POST|/|{<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"description": "4 horas de trading",<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"amount": 250000,<br><span>&nbsp;&nbsp;&nbsp;&nbsp;</span>"category": 2<br>}|201|
|Lista todos los egresos|GET|/|-|200|
|Detalle de un egreso|GET|/{id}|-|200|
|Elimina un egreso|DELETE|/{id}|-|200|

<br><br>

Reportes
> PREFIJO /users/{id}/reports

|DESCRIPCION|VERBO|URI|DATA ENVIADA|ESTADO|
|-|-|-|-|-|
|Reporte basico|GET|/basic|-|200|
|Reporte detalladdo|GET|/extended|-|200|

<br><br>


### Ejecutar en local

1. Clonar el repositorio en tu computadora. Puedes utilizar `git clone https://github.com/PabloUribe-UAM/control-gastos.git`

2. Entrar al directorio de trabajo: `mkdir control-gastos`

3. Crear el `.env` a partir de `.env.example` y establecer las variables.

4. Ejecutar con docker: `docker compose -f docker-compose-dev.yml --env-file .env up`

5. Abre la documentacion en [http://localhost:8000/docs](http://localhost:8000/docs) o [http://localhost:8000/redoc](http://localhost:8000/redoc)