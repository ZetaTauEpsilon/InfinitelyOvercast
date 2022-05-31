from flask import Flask, make_response
from feedgen.feed import FeedGenerator
from config.main import Config
from output.main import Queue, OutputGenerator

flask_app = Flask(__name__)
config = Config()
q = Queue(config)

@flask_app.route('/')
def index():
    fg = FeedGenerator()
    fg.load_extension('podcast')
    q.main()
    fg.title(config.title)
    fg.description(config.description)
    fg.link(href=config.url)
    
    OutputGenerator(q, config).buildXMLEntries(fg)
    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')

    return response

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=8080)