from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='static', static_url_path='/static')

# список для хранения торговых пар
trading_pairs = []

# словарь для харнения параметров StopLoss и TakeProfit
parameters = {}

# словарь для хранения статистики
statistics = {'hour': {'tp': 0, 'sl': 0, 'tp_value': 0, 'sl_value': 0},
              'four_hours': {'tp': 0, 'sl': 0, 'tp_value': 0, 'sl_value': 0},
              'day': {'tp': 0, 'sl': 0, 'tp_value': 0, 'sl_value': 0},
              'week': {'tp': 0, 'sl': 0, 'tp_value': 0, 'sl_value': 0},
              'month': {'tp': 0, 'sl': 0, 'tp_value': 0, 'sl_value': 0}}

# Добавим переменные для лимита на продажу и параметра в процентах
sell_limit = 10  # Лимит на продажу
percent_threshold = 1  # Параметр в процентах

@app.route('/')
def index():
    return render_template('index.html', trading_pairs=trading_pairs, parameters=parameters)

@app.route('/add_pair', methods=['POST'])
def add_pair():
    if len(trading_pairs) < 10:
        pair = request.form.get('pair')
        trading_pairs.append(pair)
        parameters[pair] = {'stop_loss': None, 'take_profit': None}

    return redirect('/')

@app.route('/edit_parameters', methods=['POST'])
def edit_parameters():
    pair = request.form.get('pair')
    stop_loss = request.form.get('stop_loss')
    take_profit = request.form.get('take_profit')

    parameters[pair]['stop_loss'] = stop_loss
    parameters[pair]['take_profit'] = take_profit

    return redirect('/')

@app.route('/activate_pair/<pair>')
def activate_pair(pair):
    # Предполагаем, что у вас есть какие-то функции для активации пары, например:
    # activate_trading_pair(pair)

    # Здесь вы можете добавить логику для проверки условий перед продажей
    current_price = get_current_price(pair)  # Замените на вашу функцию получения текущей цены
    highest_price = get_highest_price(pair)  # Замените на вашу функцию получения самой высокой цены

    if current_price > sell_limit:
        # Если текущая цена выше лимита на продажу, проверяем параметр в процентах
        percent_difference = ((current_price - highest_price) / highest_price) * 100
        if percent_difference >= percent_threshold:
            # Продаем, так как разница в процентах превышает порог
            sell_trading_pair(pair)
            return f"Sold {pair} at {current_price} because the percent difference exceeded the threshold."
        else:
            # Ждем, так как разница в процентах не превышает порог
            return f"Waiting for a higher price for {pair}. Current price: {current_price}"
    else:
        # Если текущая цена не превышает лимита на продажу, можно активировать пару без проверок
        activate_trading_pair(pair)
        return f"Activated {pair} without sell conditions."

@app.route('/active_pairs')
def active_pairs():
    return render_template('active_pairs.html', trading_pairs=trading_pairs, parameters=parameters)

@app.route('/statistics')
def show_statistics():
    return render_template('statistics.html', statistics=statistics)

if __name__ == '__main__':
    app.run(debug=True)
