from collections import namedtuple

URI = namedtuple(
    "URI",
    field_names=["path", "method", "signed", "params", "weight"],
    defaults=["get", False, [], 1],
)

URLS = {
    "BASE_URL": "https://www.bitrue.com/api",
    "API_VERSION": "v1",
}

symbol = "symbol"
limit = "limit"
limits = [5,10,20,50,100,500,1000]
default_limit = limits[4]
from_id = "fromId"
start_time = "startTime"
end_time = "endTime"
side = "side"
time_in_force = "timeInForce"
default_time_in_force = "GTT"

price = "price"
quantity = "quantity"
recvWindow = "recvWindow"
timestamp = "timestamp"
order_id = "orderId"


ORDER_STATUS_NEW = 'NEW'
ORDER_STATUS_PARTIALLY_FILLED = 'PARTIALLY_FILLED'
ORDER_STATUS_FILLED = 'FILLED'
ORDER_STATUS_CANCELED = 'CANCELED'
ORDER_STATUS_PENDING_CANCEL = 'PENDING_CANCEL'
ORDER_STATUS_REJECTED = 'REJECTED'
ORDER_STATUS_EXPIRED = 'EXPIRED'

SIDE_BUY = 'BUY'
SIDE_SELL = 'SELL'

ORDER_TYPE_LIMIT = 'LIMIT'
ORDER_TYPE_MARKET = 'MARKET'
ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'

TIME_IN_FORCE_GTC = 'GTC'  # Good till cancelled
TIME_IN_FORCE_IOC = 'IOC'  # Immediate or cancel
TIME_IN_FORCE_FOK = 'FOK'  # Fill or kill

ORDER_RESP_TYPE_ACK = 'ACK'
ORDER_RESP_TYPE_RESULT = 'RESULT'
ORDER_RESP_TYPE_FULL = 'FULL'

URI_PING = URI("ping")
URI_SERVER_TIME = URI("time")
URI_EXCHANGE_INFO = URI("exchangeInfo")

# market data
URI_ORDER_BOOK = URI("depth", params=[symbol, limit])
URI_RECENT_TRADES = URI("trades", params=[symbol, limit])
URI_HISTORIC_TRADES = URI("historicalTrades", params=[symbol, limit, from_id], weight=5)
URI_COMPRESSED_TRADES = URI("aggTrades",
                            params=[symbol, from_id, start_time, end_time, limit])
URI_24hr_PRICE_STATS = URI("24hr", params=[symbol], weight=40)
URI_PRICE = URI(price, params=[symbol])
URI_ORDER_BOOK = URI("bookTicker", params=[symbol])

# account endpoints
URI_PLACE_ORDER = URI(
    "order",
    method="post",
    signed=True,
    params=[symbol, side, "type", time_in_force, quantity, price, recvWindow, timestamp, quantity, price,]
)
URI_GET_ORDER = URI(
    "order",
    method="get",
    signed=True,
    params=[symbol, order_id, recvWindow, timestamp],
)
URI_CANCEL_ORDER = URI(
    "order",
    method="delete",
    signed=True,
    params=[symbol, order_id, recvWindow, timestamp],
)
URI_OPEN_ORDERS = URI(
    "openOrders",
    signed=True,
    params=[symbol, recvWindow, timestamp],
)
URI_ALL_ORDERS = URI(
    "allOrders",
    signed=True,
    params=[symbol, order_id, start_time, end_time, limit, recvWindow,  timestamp],
    weight=5,
)
URI_ACCOUNT_INFO = URI(
    "account",
    signed=True,
    params=[recvWindow, timestamp],
)
URI_MY_TRADES = URI(
    "myTrades",
    signed=True,
    params=[symbol, start_time, end_time, from_id, limit, recvWindow, timestamp],
)

URIS ={
    "ping": URI_PING,
    "time": URI_SERVER_TIME,
    "exchangeInfo": URI_EXCHANGE_INFO,

    "depth": URI_ORDER_BOOK,
    "trades": URI_RECENT_TRADES,
    "historicalTrades": URI_HISTORIC_TRADES,
    "aggTrades": URI_COMPRESSED_TRADES,
    "24hr": URI_24hr_PRICE_STATS,
    "price": URI_PRICE,
    "bookTicker": URI_ORDER_BOOK,

    "order": [URI_GET_ORDER, URI_PLACE_ORDER, URI_CANCEL_ORDER,],
    "openOrders": URI_OPEN_ORDERS,
    "allOrders": URI_ALL_ORDERS,
    "account": URI_ACCOUNT_INFO,
    "myTrades": URI_MY_TRADES,
}
