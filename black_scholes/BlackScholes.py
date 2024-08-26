from typing import Tuple, List
import numpy as np
from scipy.stats import norm
class BlackScholes:
    def __init__(self, current_underlying_price, 
                 time_to_exp_days, strike_price, 
                 risk_free_rate, volatility, 
                 price_range_to_display) -> None:
        self.current_underlying_price = current_underlying_price
        self.time_to_exp_days = time_to_exp_days
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.d1 = None
        self.d2 = None
        self.time_list_display = []
        if time_to_exp_days < 7:
            self.time_list_display = [d for d in range(time_to_exp_days,0,-1)]
        else:
            self.time_list_display = [time_to_exp_days - (n*(np.ceil(time_to_exp_days/7))) for n in range(0,7)]
        self.price_range_display = []
        positive_bound = price_range_to_display
        negative_bound = price_range_to_display
        if price_range_to_display >= 100:
            negative_bound = -1*max(-98, -1*price_range_to_display)
        step_size = np.ceil((negative_bound + positive_bound)/18).astype(np.int64)
        self.price_range_display = [self.current_underlying_price +self.current_underlying_price*(p/100) for p in range(-1*negative_bound, positive_bound,step_size)]
        self.perc_price_range_display = [p for p in range(-1*negative_bound, positive_bound,step_size)]
        
    def calculate_price(self) -> Tuple[List[List[int]], List[List[int]]]:
        """Calculates value of European call and put option
        using the BlackScholes formula

        Returns:
            Tuple[List[List[int]], List[List[int]]]: values of the call and put option respectively over a given range of time to expiry and underlying prices
        """
        call_prices = []
        put_prices = []
        for dte in self.time_list_display:
            call_row = []
            put_row = []
            for underlying_price in self.price_range_display:
                d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                               (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte))
                d2 = d1 - self.volatility*np.sqrt(dte)
                # Call
                call_price = norm.cdf(d1)*underlying_price - norm.cdf(d2)*self.strike_price*np.exp(-1*self.risk_free_rate*dte)
                call_row.append(call_price)
                # Put
                put_price = norm.cdf(-1*d2)*self.strike_price*np.exp(-1*self.risk_free_rate*dte) - norm.cdf(-1*d1)*underlying_price
                put_row.append(put_price)
            call_prices.append(call_row)
            put_prices.append(put_row)
        return (call_prices, put_prices)
    
    def calculate_greeks(self) -> Tuple[List[int], List[int], List[int], List[int], List[int]]:
        pass
    
    @staticmethod
    def calculate_pnl(option_projected_val: List[int], amount_paid: int, denomination: str) -> List[int]:
        pass
     