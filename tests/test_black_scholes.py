from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho
import pytest
from black_scholes.BlackScholes import BlackScholes
from TestData.BlackScholesData import BlackScholesData


class TestBlackScholes:
    
    @pytest.fixture(params=BlackScholesData.test_BlackScholes_data)
    def getData(self, request):
        return request.param
    
    def test_option_values(self, getData):
        # Instantiate new black_scholes object per data set
        testBlackScholes = BlackScholes(getData["current_underlying_price"], getData["dte"], getData["strike_price"], getData["risk_free_rate"], getData["volatility"], getData["price_range_to_display"])
        # compute and assert option values against py_vollib's model
        call_prices = []
        put_prices = []
        for underlying_price in testBlackScholes.price_range_display:
            call_row = []
            put_row = []
            for dte in testBlackScholes.time_list_display:
                
                # Call
                call_row.append(round(bs("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                # Put
                put_row.append(round(bs("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
            call_prices.append(call_row)
            put_prices.append(put_row)
        own_call, own_put = testBlackScholes.calculate_price()
        assert own_call == call_prices
        assert own_put == put_prices
    
    def test_option_greeks(self, getData):
        pass