from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import delta, gamma, vega, theta, rho
import pytest
from black_scholes.BlackScholes import BlackScholes
from TestData.BlackScholesData import BlackScholesData
import numpy as np


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
        # Instantiate new black_scholes object per data set
        testBlackScholes = BlackScholes(getData["current_underlying_price"], getData["dte"], getData["strike_price"], getData["risk_free_rate"], getData["volatility"], getData["price_range_to_display"])
        # compute and assert option values against py_vollib's model
        call_delta = []
        put_delta = []
        call_gamma = []
        put_gamma = []
        call_theta = []
        put_theta = []
        call_vega = []
        put_vega = []
        call_rho = []
        put_rho = []
        for underlying_price in testBlackScholes.price_range_display:
            call_delta_row = []
            put_delta_row = []
            call_gamma_row = []
            put_gamma_row = []
            call_theta_row = []
            put_theta_row = []
            call_vega_row = []
            put_vega_row = []
            call_rho_row = []
            put_rho_row = []
            for dte in testBlackScholes.time_list_display:
                
                # Call
                call_delta_row.append(round(delta("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                call_gamma_row.append(round(gamma("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                call_theta_row.append(round(theta("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                call_vega_row.append(round(vega("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                call_rho_row.append(round(rho("c",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                # Put
                put_delta_row.append(round(delta("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                put_gamma_row.append(round(gamma("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                put_theta_row.append(round(theta("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                put_vega_row.append(round(vega("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
                put_rho_row.append(round(rho("p",underlying_price,getData["strike_price"],dte/365,getData["risk_free_rate"], getData["volatility"]),3))
            
            call_delta.append(call_delta_row)
            call_gamma.append(call_gamma_row)
            call_theta.append(call_theta_row)
            call_vega.append(call_vega_row)
            call_rho.append(call_rho_row)
            
            
            put_delta.append(put_delta_row)
            put_gamma.append(put_gamma_row)
            put_theta.append(put_theta_row)
            put_vega.append(put_vega_row)
            put_rho.append(put_rho_row)
            
        own_call, own_put = testBlackScholes.calculate_greeks("Delta")
    
        assert own_call == call_delta
        assert own_put == put_delta
        own_call, own_put = testBlackScholes.calculate_greeks("Gamma")
        assert own_call == call_gamma
        assert own_put == put_gamma
        own_call, own_put = testBlackScholes.calculate_greeks("Theta")
        assert own_call == call_theta
        assert own_put == put_theta
        own_call, own_put = testBlackScholes.calculate_greeks("Vega")
        assert own_call == call_vega
        assert own_put == put_vega
        own_call, own_put = testBlackScholes.calculate_greeks("Rho")
        assert own_call == call_rho
        assert own_put == put_rho