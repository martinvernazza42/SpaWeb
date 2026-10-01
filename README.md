# 🌸 Spa Sentirse Bien

**Spa Sentirse Bien** es una aplicación web desarrollada para la gestión y presentación de los servicios de un spa.

El proyecto combina una página web institucional con funcionalidades dinámicas desarrolladas en **Django**, permitiendo presentar los tratamientos y servicios ofrecidos y gestionar las reservas de los clientes desde un sistema centralizado.

> 🎓 **Proyecto final / académico — Desarrollo Web**

---

## 📖 Sobre el proyecto

El objetivo de **Spa Sentirse Bien** es digitalizar la presencia del spa y facilitar la gestión de sus servicios y reservas.

La aplicación fue desarrollada como un proyecto práctico para aplicar conocimientos de desarrollo web, bases de datos, programación backend y diseño de interfaces.

El sistema permite que los visitantes puedan conocer el spa y sus servicios desde la página web, mientras que la administración puede gestionar la información mediante las herramientas proporcionadas por Django.

---

## 🎯 Objetivos

Los principales objetivos del proyecto son:

* 🌐 Crear una presencia web para el spa.
* 💆 Mostrar los diferentes servicios y tratamientos.
* 📅 Facilitar la gestión de reservas.
* 📝 Registrar la información proporcionada por los clientes.
* 🛠️ Permitir la administración de los datos desde un panel centralizado.
* 🗄️ Utilizar una base de datos para almacenar la información.
* 📱 Crear una interfaz adaptable a diferentes dispositivos.

---

## ✨ Funcionalidades

### 🏠 Página principal

La página principal presenta la identidad del spa y permite al visitante acceder rápidamente a las diferentes secciones del sitio.

Se busca ofrecer una navegación sencilla y una experiencia visual acorde con la temática de bienestar y relajación.

### 💆 Servicios

Los usuarios pueden consultar los diferentes tratamientos y servicios disponibles.

Cada servicio puede incluir información relevante como:

* Nombre
* Descripción
* Imagen
* Precio
* Duración

La información se gestiona de forma dinámica desde el sistema.

### 📅 Reservas

El sistema incorpora un mecanismo para solicitar reservas.

Los clientes pueden proporcionar la información necesaria para realizar una reserva y el sistema almacena esos datos para su posterior gestión.

Esto permite reemplazar un proceso completamente manual por uno centralizado dentro de la aplicación.

### 🛠️ Panel de administración

Una de las principales ventajas de utilizar Django es la posibilidad de contar con un **panel administrativo**.

Desde allí se pueden gestionar los diferentes datos de la aplicación, por ejemplo:

* Servicios
* Reservas
* Información de clientes
* Imágenes
* Otros registros almacenados en la base de datos

Esto permite modificar información sin necesidad de cambiar directamente el código de la página.

---

## 🏗️ Tecnologías utilizadas

| Tecnología         | Utilización                          |
| ------------------ | ------------------------------------ |
| **Python**         | Lenguaje principal                   |
| **Django**         | Framework backend                    |
| **HTML5**          | Estructura de las páginas            |
| **CSS3**           | Estilos y diseño                     |
| **Bootstrap**      | Diseño responsive y componentes      |
| **JavaScript**     | Funcionalidades del lado del cliente |
| **SQLite**         | Base de datos durante el desarrollo  |
| **Git / GitHub**   | Control de versiones                 |
| **PythonAnywhere** | Despliegue de la aplicación          |

---

## 🧩 Arquitectura

El proyecto utiliza la arquitectura basada en **MVT (Model-View-Template)** proporcionada por Django.

```text
                    USUARIO
                       │
                       ▼
              ┌────────────────┐
              │     Browser    │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │     URLs       │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │     Views      │
              │    Django      │
              └───┬────────┬───┘
                  │        │
          ┌───────┘        └────────┐
          ▼                          ▼
   ┌──────────────┐          ┌──────────────┐
   │    Models    │          │   Templates  │
   │              │          │    HTML      │
   └──────┬───────┘          └──────────────┘
          │
          ▼
   ┌──────────────┐
   │   Database   │
   │    SQLite    │
   └──────────────┘
```

### ¿Cómo funciona?

De forma general, cuando un usuario accede a una sección:

1. El navegador realiza una solicitud.
2. Django recibe la solicitud mediante las URLs configuradas.
3. Una **View** procesa la petición.
4. Si es necesario, la View consulta o modifica información mediante los **Models**.
5. Los datos son obtenidos desde la base de datos.
6. Django utiliza un **Template** para generar la página.
7. El resultado es enviado nuevamente al navegador.

Esta separación permite mantener organizada la lógica de la aplicación.

---

## 📂 Estructura general

La estructura puede variar según la versión del proyecto, pero conceptualmente se organiza de la siguiente manera:

```text
SpaWeb/
│
├── manage.py
│
├── spa/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
│
├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── media/
│   └── ...
│
├── db.sqlite3
│
└── requirements.txt
```

### Principales componentes

**`models.py`**

Define las estructuras de datos utilizadas por la aplicación y su relación con la base de datos.

**`views.py`**

Contiene la lógica necesaria para procesar las solicitudes y determinar qué información debe mostrar el sistema.

**`urls.py`**

Define las rutas disponibles dentro de la aplicación.

**`templates/`**

Contiene las páginas HTML que se muestran al usuario.

**`static/`**

Contiene los recursos estáticos del proyecto, como CSS, JavaScript e imágenes.

**`media/`**

Almacena archivos multimedia gestionados dinámicamente por la aplicación.

**`admin.py`**

Configura los modelos que pueden administrarse desde el panel de Django.

---

## 🎨 Diseño

La interfaz utiliza una estética relacionada con el concepto de bienestar y relajación.

La paleta principal utiliza tonos suaves:

```text
#FFB8C9
#FFCAD6
#FFEDF1
#FFFFFF
```

El diseño utiliza **Bootstrap** para facilitar la adaptación del sitio a diferentes tamaños de pantalla.

La aplicación busca mantener una interfaz:

* 🌸 Simple
* 📱 Responsive
* 🧘 Relacionada con la identidad del spa
* 🧭 Fácil de navegar
* ✨ Visualmente limpia

---

## 🗄️ Base de datos

La aplicación utiliza una base de datos para almacenar la información dinámica del sistema.

Durante el desarrollo se utilizó **SQLite**, debido a su facilidad de configuración y a que permite trabajar con Django sin necesidad de instalar un servidor de base de datos independiente.

Django proporciona un ORM (**Object-Relational Mapping**) que permite trabajar con los datos mediante modelos de Python.

Por ejemplo:

```python
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
```

De esta manera, Django se encarga de traducir las operaciones realizadas sobre los modelos a consultas sobre la base de datos.

---

## 🔐 Administración

El proyecto utiliza el sistema de autenticación y administración proporcionado por Django.

El administrador puede acceder al panel correspondiente y gestionar los datos registrados en el sistema.

Esto permite separar la experiencia del visitante de las tareas administrativas del spa.

---

## 🚀 Instalación

### Requisitos

Para ejecutar el proyecto localmente se necesita:

* Python 3.x
* pip
* Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/martinvernazza42/SpaWeb.git
```

Entrar en el directorio:

```bash
cd SpaWeb
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

Activarlo en Windows:

```bash
venv\Scripts\activate
```

En Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Crear un usuario administrador

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible normalmente en:

```text
http://127.0.0.1:8000/
```

---

## ☁️ Deploy

El proyecto fue desplegado utilizando **PythonAnywhere**, permitiendo ejecutar la aplicación Django en un entorno accesible desde Internet.

El despliegue permitió aplicar conceptos relacionados con:

* Configuración de servidores.
* Variables de entorno.
* Archivos estáticos.
* Archivos multimedia.
* Configuración de Django para producción.
* Deploy de aplicaciones Python.

---

## 🔄 Flujo general de una reserva

De manera simplificada, el proceso puede representarse de la siguiente forma:

```text
       CLIENTE
          │
          ▼
   Consulta servicios
          │
          ▼
   Selecciona servicio
          │
          ▼
   Completa formulario
          │
          ▼
    Envía solicitud
          │
          ▼
      DJANGO
          │
          ▼
      DATABASE
          │
          ▼
      RESERVA
          │
          ▼
   Gestión administrativa
```

Esto permite centralizar la información y facilitar posteriormente la administración de las reservas.

---

## 📚 Conocimientos aplicados

Este proyecto permitió poner en práctica conocimientos relacionados con:

* Desarrollo web backend.
* Python.
* Framework Django.
* Arquitectura MVT.
* Programación orientada a objetos.
* Bases de datos relacionales.
* ORM.
* HTML y CSS.
* Bootstrap.
* JavaScript.
* Formularios.
* CRUD.
* Autenticación.
* Panel administrativo.
* Gestión de archivos e imágenes.
* Git y GitHub.
* Deployment.

---

## 🚧 Posibles mejoras

El proyecto puede continuar evolucionando mediante funcionalidades como:

* [ ] Sistema avanzado de disponibilidad de turnos.
* [ ] Confirmación automática de reservas.
* [ ] Notificaciones por email.
* [ ] Calendario de turnos.
* [ ] Sistema de usuarios para clientes.
* [ ] Historial de reservas.
* [ ] Diferentes roles administrativos.
* [ ] Integración con métodos de pago.
* [ ] Dashboard con estadísticas.
* [ ] API REST para una futura aplicación móvil.
* [ ] Migración a PostgreSQL para producción.
* [ ] Mejoras de seguridad y configuración de producción.

---

## 🎓 Contexto académico

**Spa Sentirse Bien** fue desarrollado como proyecto final para aplicar de manera integral los conocimientos adquiridos durante la formación en desarrollo web.

Más allá de la interfaz visual, el proyecto busca demostrar la implementación de una aplicación web completa, incluyendo **frontend, backend, persistencia de datos, gestión administrativa y despliegue**.

---

## 👨‍💻 Autor

**Martin Vernazza**

Proyecto desarrollado como parte de mi formación como desarrollador y utilizado como proyecto de portfolio.

---

## 📄 Licencia

Este proyecto fue desarrollado principalmente con fines **educativos y de portfolio**.

Las condiciones de uso y distribución pueden definirse posteriormente según la evolución del proyecto.
