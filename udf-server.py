from json import dumps as jsonify
from flask import Flask, request
from flask_cors import CORS
from trade import Trade
import time

app: Flask = Flask(__name__)
CORS(app)

trades = dict()
trades["NMXETH"] = Trade("NMXETH", "NMX / Ethereum")
trades["ETHSGD"] = Trade("ETHSGD", "Ethereum / Singaporean Dollar")
trades["ETHMYR"] = Trade("ETHMYR", "Ethereum / Malaysian Ringgit")
trades["ETHIDR"] = Trade("ETHIDR", "Ethereum / Indonesian Rupiah")

# TODO: Create a class and .info() for this kind of stuff like this
exchanges = dict()
exchanges['All'] = {"name": "All",
                    "value": "",
                    "desc": "All"}

exchanges['NuMoney'] = {"name": "NuMoney",
                        "value": "NuMoney",
                        "desc": "NuMoney"}


""""
@app.route("/")
def index():
    return "Hi There, are you otto ?"
"""


@app.route("/config", methods=["GET"])
def configHandler():
    return jsonify(config())


def config():
    return {
        'symbols_types': [
            {"name": "All", "value": ""},
            {"name": "Crypto", "value": "Crypto"},
        ],
        'exchanges': sorted([v for k, v in exchanges.items()],
                            key=lambda x: x["name"]),
        'supports_group_request': False,
        'supports_marks': False,
        'supports_search': True,
        'supports_timescale_marks': False}


@app.route("/symbols", methods=["GET"])
def symbolResolveHandler():
    symbol = request.args.get("symbol")
    return jsonify(trades[symbol].info())


@app.route("/search", methods=["GET"])
def searchHandler():
    print(request.args)
    query = request.args.get("query")
    tradeType = request.args.get("type")
    exchange = request.args.get("exchange")
    limit = request.args.get("limit")
    print("abcd")
    return jsonify(search(query, tradeType, exchange, limit))


# simple search
def search(query, tradeType, exchange, limit):
    results = [(symbol.find(query), trade)
               for symbol, trade in trades.items()
               if (exchange == "" or trade.exchange == exchange)
               if (tradeType == "" or trade.tradeType == tradeType)
               if symbol.find(query) != -1]
    results.sort(key=lambda x: x[0])
    results = results[:int(limit)]
    results = [searchFormat(b) for a, b in results]
    return results


def searchFormat(trade):
    return {
        "symbol": trade.symbol,
        "full_name": trade.description,
        "description": trade.description,
        "exchange": trade.exchange,
        "ticker": trade.exchange + ":" + trade.symbol,
        "type": trade.tradeType,
    }


@app.route("/history", methods=["GET"])
def barsHandler():
    symbol = request.args.get("symbol")
    start = request.args.get("from")
    end = request.args.get("to")
    resolution = request.args.get("resolution")
    return jsonify(bars(symbol, start, end, resolution))


def bars(symbol, start, end, resolution):
    pass


"""
app.route("/marks", methods=["GET"])
def marksHandler():
    symbol = request.args.get("symbol")
    start = request.args.get("from")
    end = request.args.get("to")
    resolution = request.args.get("resolution")
    return jsonify(marks(symbol, start, end, resolution))

def marks(symbol, start, end, resolution):
    pass
"""

"""
@app.route("/timescale_marks", methods=["GET"])
def timescaleMarksHandler():
    symbol = request.args.get("symbol")
    fromTime = request.args.get("from")
    toTime = request.args.get("to")
    resolution = request.args.get("resolution")
    return jsonify(timescaleMarks(symbol, start, end, resolution))

def timescaleMarks(symbol, start, end, resolution):
    pass
"""


@app.route("/time", methods=["GET"])
def timeHandler():
    return str(int(time.time()))


@app.route("/quotes", methods=["GET"])
def variableQuotesHandler():
    symbols = request.args.get("symbols")
    symbols = symbols.split(',')
    s = "ok"
    d = [quote(s) for s in symbols]
    return jsonify({
        "s": s,
        "d": d})


def quote(symbol):
    pass


if __name__ == "__main__":
    app.run(host='dev.localhost', port=4200, debug=True)
