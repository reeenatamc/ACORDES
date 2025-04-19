<h1 align="center">🎶 ACORDES</h1>

<p align="center"><em>“La música debe ser una posibilidad, no un privilegio.”</em></p>

---

## 📝 Descripción del proyecto

**ACORDES** es una aplicación web desarrollada con el objetivo de democratizar la creación musical a través de inteligencia artificial. Utiliza el modelo [AudioCraft](https://github.com/facebookresearch/audiocraft) —específicamente MusicGen— para generar composiciones musicales a partir de descripciones textuales. Todo el proceso se ejecuta de forma **local**, sin depender de servicios en la nube ni de plataformas de terceros.

Este proyecto está construido con **Python 11**, aprovechando sus capacidades de rendimiento, sintaxis moderna y compatibilidad con bibliotecas de última generación.

---

## 🧠 ¿Qué es AudioCraft?

[AudioCraft](https://github.com/facebookresearch/audiocraft) es una iniciativa de Meta AI que permite generar música mediante modelos de lenguaje y audio. En particular, **MusicGen** transforma texto en audio musical de manera sorprendentemente precisa. En ACORDES, esta herramienta se integra directamente al backend del servidor, garantizando independencia, privacidad y eficiencia.

---

## 🧩 Tecnologías utilizadas

- **🐍 Backend:** [Django](https://www.djangoproject.com/)  
  Framework robusto y escalable en Python que gestiona el procesamiento de texto, la lógica del servidor y la interacción con AudioCraft.

- **🖥 Frontend:** HTML5 + [Bootstrap](https://getbootstrap.com/)  
  Interfaz web intuitiva y responsiva, orientada a la experiencia del usuario, que facilita la interacción con el sistema.

- **🎵 Generación musical:** [AudioCraft (MusicGen)](https://github.com/facebookresearch/audiocraft)  
  Motor creativo de IA que interpreta las descripciones del usuario y genera pistas musicales.

- **⚙️ Lenguaje principal:** **Python 3.11**  
  Se ha optado por esta versión por su comprobada estabilidad y compatibilidad con la versión actual de AudioCraft. Aunque no es la más reciente, garantiza un entorno robusto y plenamente funcional para el despliegue local del modelo.


---

## 🎯 Objetivo del proyecto

El propósito central de ACORDES es brindar una herramienta accesible, eficiente y profesional para la generación musical mediante inteligencia artificial, dirigida especialmente a:

- Artistas independientes en busca de inspiración o demos rápidas.
- Creadores de contenido que requieren música original sin depender de bancos de audio.
- Aficionados y exploradores sonoros interesados en experimentar sin barreras técnicas ni económicas.

Todo esto, desde un entorno **local**, sin requerimientos de pago ni conexión constante a servicios externos.

---

## 🖼 Captura de pantalla 

> En proceso...

---

## ⚙️ Instalación

Siga los pasos a continuación para poner en funcionamiento el proyecto en su máquina local:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/reeenatamc/ACORDES.git
   cd ACORDES
   ```

2. **Asegurarse de tener instalado Python 11.**

   Puede verificar su versión actual con:
   ```bash
   python --version
   ```

3. **Instalar las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar el servidor:**
   ```bash
   python manage.py runserver
   ```

5. **Acceder a la aplicación:**

   Abra su navegador en la siguiente URL:
   ```
   http://127.0.0.1:8000/
   ```

---

## 🤝 Contribuciones

Las contribuciones están abiertas y son bienvenidas. Si deseas colaborar, por favor realiza un fork del repositorio, crea una nueva rama con tus cambios y abre un pull request. Todo aporte que promueva la mejora de la experiencia musical será considerado.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---

## 📬 Contacto

Para dudas, sugerencias o propuestas, puedes escribir a: **ramaldonado8@utpl.edu.ec**


<p align="center">Hecho con pasión, tecnología y convicción musical.</p>


by renata <3 !

