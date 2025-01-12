from flask import Flask, jsonify, request
from market_data_scraper import MarketDataScraper
from market_predictor import MarketPredictor
from trading_executor import TradingExecutor, MockExchangeAPI
from risk_manager import RiskManager

app = Flask(__name__)

# Initialize modules
market_scraper = MarketDataScraper()
market_predictor = MarketPredictor()
exchange_api = MockExchangeAPI()
trading_executor = TradingExecutor(exchange_api, None)
risk_manager = RiskManager()

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Raelis AI Agent API. Use /market_data to get market data, /predict to get market prediction, and /risk_assessment to assess risk."
    })

@app.route('/market_data', methods=['GET'])
def get_market_data():
    crypto_ids = request.args.get('crypto_ids', default='bitcoin,ethereum', type=str).split(',')
    market_data = market_scraper.get_market_data(crypto_ids)
    return jsonify(market_data)

@app.route('/predict', methods=['POST'])
def predict_price():
    # Get the last 30 days of market data for prediction
    crypto_id = request.json.get('crypto_id', 'bitcoin')
    days = request.json.get('days', 30)
    
    historical_data = market_scraper.get_historical_data(crypto_id, days)
    market_predictor.train(historical_data)
    
    future_date = request.json.get('future_date', 1616524800)  # Default to a timestamp
    predicted_price = market_predictor.predict(future_date)
    
    return jsonify({
        "crypto_id": crypto_id,
        "predicted_price": predicted_price[0]
    })

@app.route('/trade', methods=['POST'])
def execute_trade():
    action = request.json.get('action', 'buy')  # 'buy' or 'sell'
    amount = request.json.get('amount', 1)
    price = request.json.get('price', 50000)  # Default price
    
    trading_executor.execute_trade(action, amount, price)
    
    return jsonify({
        "message": f"Trade executed: {action} {amount} units at {price} USD."
    })

@app.route('/risk_assessment', methods=['POST'])
def assess_risk():
    current_balance = request.json.get('current_balance', 50000)  # Default balance: $50,000
    market_volatility = request.json.get('market_volatility', 0.05)  # Default volatility: 5%
    
    risk_manager.assess_risk(current_balance, market_volatility)
    
    return jsonify({
        "message": "Risk assessment completed. Check your console for warnings."
    })

if __name__ == '__main__':
    app.run(debug=True)
