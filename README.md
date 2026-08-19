# ACORDES

Generates original music from a text prompt, with the model running on your own
machine. No cloud service, no API key, nothing leaves the box.

## What it does

You describe what you want in a sentence. MusicGen turns it into audio, GPT-2
names the track, and the result lands in your library.

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

The models live on a module-level singleton in `musicapp/services.py`, loaded
lazily on first use. A worker pays the load cost once rather than on every
request, and nothing heavy is imported at module level, so the web process never
pulls torch into memory for code it will not run.

## Stack

Django 5 · Celery on Redis · MusicGen through AudioCraft and Transformers ·
PyTorch, CPU.

## Running it

You need a broker. With Redis on the default port:

```bash
pip install -r requirements.txt

# terminal 1, web
python manage.py migrate
python manage.py runserver

# terminal 2, worker
celery -A music_ai_project worker --loglevel=info --concurrency=1
```

Keep `--concurrency=1` unless you have the RAM for a full copy of the models per
worker process. Override `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` if your
broker lives elsewhere.

## Licences

The code here is MIT. The **MusicGen weights are CC BY-NC 4.0, which forbids
commercial use**, and the MIT licence on this repository grants you no rights to
them. Read [NOTICE](NOTICE) before building anything on top of this.
