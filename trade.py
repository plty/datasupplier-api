from math import floor


def fraction10(val):
    """ Convert float value with denominator of 10**y.
        val --> x / (10**y)
    """
    for y in range(12):
        scale = 10 ** y
        x = floor(val * scale)
        if x == 0:
            continue
        if val * scale - x < 1e-9:
            return (x, y)
    return (floor(val * 10**20), 20)


class Trade:
    def __init__(self,
                 symbol,
                 description=None,
                 minInc=0.01,

                 exchange="NuMoney",
                 tradeType="Crypto",
                 timezone="Asia/Singapore",
                 session="24x7",

                 resolutions=('1', '5', '15', '30', '60', '1D', '1W', '1M'),

                 hasSeconds=False,
                 secondsMultipliers=(),

                 hasIntraday=True,
                 intradayMultipliers=("1", "60"),

                 hasDaily=False,
                 hasWeekly=False,
                 hasMonthly=False,

                 hasVolume=False,

                 hasEmptyBars=False,
                 forceSessionRebuild=True,
                 ):

        if description is None:
            description = symbol

        self.symbol = symbol
        self.description = description
        self.minInc = minInc

        self.exchange = exchange
        self.tradeType = tradeType
        self.timezone = timezone
        self.session = session

        self.resolutions = resolutions

        self.hasSeconds = hasSeconds
        self.secondsMultipliers = secondsMultipliers

        self.hasIntraday = hasIntraday
        self.intradayMultipliers = intradayMultipliers

        self.hasDaily = hasDaily
        self.hasWeekly = hasWeekly
        self.hasMonthly = hasMonthly

        self.hasVolume = hasVolume
        self.hasEmptyBars = hasEmptyBars
        self.forceSessionRebuild = forceSessionRebuild

    def info(self):
        (minMov, precision) = fraction10(self.minInc)

        tradeProperty = {
            "symbol": self.symbol,
            "description": self.description,
            "exchange-listed": self.exchange,
            "minmov": minMov,
            "minmov2": 0,
            "fractional": False,
            "pricescale": 10 ** precision,
            "has-intraday": self.hasIntraday,
            "has-no-volume": not self.hasVolume,
            "type": self.tradeType,
            "ticker": self.exchange + ":" + self.symbol,
            "timezone": self.timezone,
            "session-regular": self.session,
            "supported-resolutions": self.resolutions,
            "force-session-rebuild": self.forceSessionRebuild,
            "has-daily": self.hasDaily,
            "intraday-multipliers": self.intradayMultipliers,
            "volume_precision": precision,
            "has-weekly-and-monthly": self.hasWeekly and self.hasMonthly,
            "has-empty-bars": self.hasEmptyBars
        }
        return tradeProperty
