<h1 align="center">🎶 ACORDES </h1>

<p align="center"><em>"Music should be a possibility, not a privilege."</em></p>

---

## 📝 Project Description

**ACORDES** is a web application developed with the goal of democratizing music creation through artificial intelligence. It uses the [AudioCraft](https://github.com/facebookresearch/audiocraft) model —specifically MusicGen— to generate musical compositions from textual descriptions. The entire process runs **locally**, without relying on cloud services or third-party platforms.

This project is built with **Python 11**, leveraging its performance capabilities, modern syntax, and compatibility with cutting-edge libraries.

---

## 🧠 What is AudioCraft?

[AudioCraft](https://github.com/facebookresearch/audiocraft) is an initiative by Meta AI that enables music generation using language and audio models. Specifically, **MusicGen** transforms text into musical audio with remarkable accuracy. In CHORDS, this tool is integrated directly into the server's backend, ensuring independence, privacy, and efficiency.

---

## 🧩 Technologies Used

- **🐍 Backend:** [Django](https://www.djangoproject.com/)  
  A robust and scalable Python framework that handles text processing, server logic, and interaction with AudioCraft.

- **🖥 Frontend:** HTML5 + [Bootstrap](https://getbootstrap.com/)  
  An intuitive and responsive web interface focused on user experience, facilitating interaction with the system.

- **🎵 Music Generation:** [AudioCraft (MusicGen)](https://github.com/facebookresearch/audiocraft)  
  An AI creative engine that interprets user descriptions and generates music tracks.

- **⚙️ Main Language:** **Python 3.11**  
  This version was chosen for its proven stability and compatibility with the current version of AudioCraft. While not the latest, it guarantees a robust and fully functional environment for local model deployment.

---

## 🎯 Project Objective

The main goal of CHORDS is to provide an accessible, efficient, and professional tool for music generation using artificial intelligence, specifically aimed at:

- Independent artists looking for inspiration or quick demos.
- Content creators needing original music without relying on audio banks.
- Hobbyists and sound explorers interested in experimenting without technical or economic barriers.

All this, in a **local** environment, with no payment requirements or constant connection to external services.

---

## 🖼 Screenshot

![image](https://github.com/user-attachments/assets/0ca51fb1-92b3-466f-bec9-f2b941f66d30)


---

## ⚙️ Installation

Follow the steps below to get the project running on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/reeenatamc/ACORDES.git
   cd ACORDES
   ```

2. **Make sure you have Python 11 installed.**

   You can check your current version with:
   ```bash
   python --version
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**

   Open your browser to the following URL:
   ```
   http://127.0.0.1:8000/
   ```

---

## How generation runs

Generating eight seconds of audio loads several hundred megabytes of models and
takes minutes on CPU. None of that can happen inside an HTTP request, so the web
process only records the prompt and queues the work:

```
POST /  ->  UserPrompt row  ->  generate_song.delay()  ->  redirect
                                        |
                                   Celery worker
                                   (models loaded once per process,
                                    reused for every later task)
                                        |
                                   SongCreated row
```

The page then polls `GET /generation/<task_id>/status/`, which returns the task
state and, once finished, the title and the path of the generated track.

The models live on a module-level singleton in `musicapp/services.py` and are
loaded lazily on first use, so a worker pays the load cost once rather than on
every request.

### Running it

You need a broker. With Redis on the default port:

```bash
# terminal 1 -- web
python manage.py runserver

# terminal 2 -- worker
celery -A music_ai_project worker --loglevel=info --concurrency=1
```

Keep `--concurrency=1` unless you have the RAM for a full copy of the models per
worker process. Override `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` if your
broker lives elsewhere.

## 🤝 Contributions

Contributions are open and welcome. If you would like to collaborate, please fork the repository, create a new branch with your changes, and open a pull request. Any contribution that improves the musical experience will be considered.

---

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more information.

---

## 📬 Contact

For questions, suggestions, or proposals, you can reach out at: **ramaldonado8@utpl.edu.ec**

<p align="center">Made with passion, technology, and musical conviction.</p>

by renata <3 !
