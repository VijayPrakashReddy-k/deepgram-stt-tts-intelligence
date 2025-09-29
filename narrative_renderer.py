# narrative_renderer.py
# Usage:
#   from narrative_renderer import render_narrative
#
# Requirements:
#   pip install jinja2

from jinja2 import Template

# Jinja template for narrative (keeps top 5 topics)
NARRATIVE_TMPL = """
### Polarity / Sentiment
The overall sentiment of the text is **{{ sentiment.label }}** with a confidence score of **{{ "%.2f"|format(sentiment.score or 0) }}**.

### Topics
{% set top_topics = (topics | sort(attribute='score', reverse=True))[:5] %}
{% if top_topics %}
The main topics discussed include:
{% for t in top_topics %}
- {{ t.topic }} (confidence {{ "%.2f"|format(t.score or 0) }})
{% endfor %}
{% else %}
No significant topics were detected.
{% endif %}

### Intent
{% if intents and intents|length > 0 %}
The text suggests {% if intents|length > 1 %}multiple intents, including:{% else %}an intent of:{% endif %}
{% for i in intents %}
- {{ i.intent }} (confidence {{ "%.2f"|format(i.score or 0) }})
{% endfor %}
{% else %}
No clear intent was identified.
{% endif %}
""".strip()


def render_narrative(resp: dict, top_n: int = 5) -> str:
    """Render a narrative from Deepgram analyze minimal response."""
    sentiment = resp.get("sentiment") or {"label": "", "score": 0.0}
    topics = resp.get("topics") or []
    intents = resp.get("intents") or []

    tmpl = Template(NARRATIVE_TMPL)
    return tmpl.render(sentiment=sentiment, topics=topics, intents=intents, top_n=top_n)
