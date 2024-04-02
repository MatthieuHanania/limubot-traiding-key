def one_buy_strategy(strategy,cash,last_price,quantity,probability,sentiment):
    if strategy.last_trade==None:
        order = strategy.create_order(
            strategy.symbol,
            quantity,
            "buy",
            type = "bracket",
            take_profit_price=last_price*1.20,
            stop_loss_price= last_price*0.95
            )
        strategy.submit_order(order)
        strategy.last_trade = "buy"
        strategy.quantity_long += quantity

# def one_buy_strategy(strategy, cash, last_price, quantity, probability, sentiment):
#     if strategy.last_trade is None and sentiment == "positive" and probability > 0.999:
#         strategy.create_order(strategy.symbol, quantity, "buy", "market")
#         strategy.last_trade = "buy"
#         strategy.quantity_long += quantity
#         print(f"Placed a buy order for {quantity} shares of {strategy.symbol} at market price.")


def buy_sell_sentiment_strategy(strategy,cash,last_price,quantity,probability,sentiment):
    if cash > last_price:
        if sentiment =="positive" and probability >0.999:
            if strategy.last_trade =="sell":
                print("SELL OUT")
                strategy.sell_all()               
                    
            order = strategy.create_order(
                strategy.symbol,
                quantity,
                "buy",
                type = "market",
            )
            strategy.submit_order(order)
            strategy.last_trade = "buy"

        elif sentiment =="negative" and probability >0.999:
            if strategy.last_trade =="buy":
                strategy.sell_all()
            
            #Eviter de commencer par une vente
            if strategy.quantity_long > 1:
                order = strategy.create_order(
                    strategy.symbol,
                    quantity,
                    "sell",
                    type = "market",
                )
                strategy.submit_order(order)
                strategy.last_trade = "sell"
                strategy.quantity_long -= quantity


# def buy_sell_sentiment_strategy(strategy, cash, last_price, quantity, probability, sentiment):
#     if cash > last_price:
#         if sentiment == "positive" and probability > 0.999:
#             if strategy.last_trade == "sell" or strategy.last_trade is None:
#                 strategy.create_order(strategy.symbol, quantity, "buy", "market")
#                 strategy.last_trade = "buy"
#                 strategy.quantity_long += quantity
#                 print(f"Placed a buy order for {quantity} shares of {strategy.symbol} at market price.")
#         elif sentiment == "negative" and probability > 0.999:
#             if strategy.last_trade == "buy" and strategy.quantity_long > 0:
#                 strategy.sell_all()
#                 strategy.last_trade = "sell"
#                 strategy.quantity_long = 0
#                 print(f"Sold all holdings of {strategy.symbol}.")
                


def short_long_sentiment_strategy(strategy,cash,last_price,quantity,probability,sentiment):
    if cash > last_price:
        if sentiment =="positive" and probability >0.999:
            if strategy.last_trade =="sell":
                print("SELL ALL")
                strategy.sell_all()               
            
            order = strategy.create_order(
                strategy.symbol,
                quantity,
                "buy",
                type = "bracket",
                take_profit_price=last_price*1.20,
                stop_loss_price= last_price*0.95
            )
            strategy.submit_order(order)
            strategy.last_trade = "buy"
            strategy.quantity_long += quantity

        elif sentiment =="negative" and probability >0.999:
            if strategy.last_trade =="buy":
                strategy.sell_all()
              
            # if strategy.quantity_long > 1:
            order = strategy.create_order(
                strategy.symbol,
                quantity,
                "sell",
                type = "bracket",
                take_profit_price=last_price*0.8,
                stop_loss_price= last_price*1.05
            )
            strategy.submit_order(order)
            strategy.last_trade = "sell_short"
            strategy.quantity_long -= quantity

# def short_long_sentiment_strategy(strategy, cash, last_price, quantity, probability, sentiment):
#     if cash > last_price:
#         if sentiment == "positive" and probability > 0.999:
#             if strategy.last_trade == "sell_short":
#                 strategy.buy_to_cover(strategy.symbol, strategy.quantity_short)
#                 strategy.last_trade = "buy_cover"
#                 strategy.quantity_short = 0
#                 print(f"Covered all short positions of {strategy.symbol}.")

#             # Proceed to buy only if not currently holding a long position
#             if strategy.quantity_long == 0:
#                 strategy.create_order(strategy.symbol, quantity, "buy", "market")
#                 strategy.last_trade = "buy"
#                 strategy.quantity_long += quantity
#                 print(f"Placed a buy order for {quantity} shares of {strategy.symbol} at market price.")

#         elif sentiment == "negative" and probability > 0.999:
#             if strategy.last_trade == "buy" and strategy.quantity_long > 0:
#                 strategy.sell_all()
#                 strategy.last_trade = "sell"
#                 strategy.quantity_long = 0
#                 print(f"Sold all holdings of {strategy.symbol}.")

#             if strategy.quantity_short == 0:
#                 strategy.sell_short(strategy.symbol, quantity)
#                 strategy.last_trade = "sell_short"
#                 strategy.quantity_short += quantity
#                 print(f"Placed a short sell order for {quantity} shares of {strategy.symbol}.")
