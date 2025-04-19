from django.template.loader import render_to_string

class Email:
    @classmethod
    def dynamic_email(cls, item, template_route):
        audio_url = f"http://localhost:8000/media/{item.audio_file}"
        return render_to_string(template_route, {
            'item': item,
            'audio_url': audio_url,
        })
