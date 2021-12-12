from stocker import Stocker
import matplotlib as plt
import quandl
import yfinance as yf

# msft = yf.Ticker("MSFT")
#
# hist = msft.history(period="max")
# print(hist)

# mydata = quandl.get_table('ZACKS/FC', ticker='AAPL')
# quandl.ApiConfig.verify_ssl = False
# quandl.ApiConfig.api_key = '9YuwuZ2Su2Fn33EEoiGo'

# mydata = quandl.get('WIKI/AAPL', authtoken=quandl.ApiConfig.api_key, rows=5)
# print(mydata)
# mydata = quandl.get_table('ZACKS/FC', ticker='AAPL')['last_changed_date']
# for i in mydata:
#     print(i)
# print(mydata[0])

microsoft = Stocker('AAPL')

# model, model_data = microsoft.create_prophet_model()
# model.plot_components(model_data)
# plt.show()

# microsoft.evaluate_prediction()
print(microsoft.predict_future(days=10))
