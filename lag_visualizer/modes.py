class WebMode:
    def __init__(self, pg):
        from flask import Flask, make_response, render_template, jsonify

        self.pg = pg
        app = Flask(__name__)

        @app.route('/')
        def index_page():
            return make_response(render_template(
                "index.html",
            ))

        @app.route('/stats')
        def get():
            report = self.pg.lag
            return jsonify(report)

        app.run()


class MatplotlibMode:
    def __init__(self, pg):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        chart = fig.add_subplot(1, 1, 1)

        while True:
            xar = pg.lag["time"]
            yar = pg.lag["size"]
            chart.clear()
            chart.plot(xar, yar)
            plt.pause(1)
