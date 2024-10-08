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
        self.price_range_display = [self.current_underlying_price +self.current_underlying_price*(p/100) for p in range(positive_bound, -1*negative_bound-1,-1*step_size)]
        self.perc_price_range_display = [p for p in range(-1*negative_bound, positive_bound,step_size)]
        
    def calculate_price(self) -> Tuple[List[List[int]], List[List[int]]]:
        """Calculates value of European call and put option
        using the BlackScholes formula

        Returns:
            Tuple[List[List[int]], List[List[int]]]: values of the call and put option respectively over a given range of time to expiry and underlying prices
        """
        call_prices = []
        put_prices = []
        #print(self.price_range_display)
        for underlying_price in self.price_range_display:
            call_row = []
            put_row = []
            for dte in self.time_list_display:
                d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                               (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                d2 = d1 - self.volatility*np.sqrt(dte/365)
                # Call
                call_price = norm.cdf(d1,0,1)*underlying_price - norm.cdf(d2,0,1)*self.strike_price*np.exp(-1*self.risk_free_rate*(dte/365))
                call_row.append(round(call_price,3))
                # Put
                put_price = norm.cdf(-d2,0,1)*self.strike_price*np.exp(-self.risk_free_rate*dte/365) - norm.cdf(-d1,0,1)*underlying_price
                put_row.append(round(put_price,3))
            call_prices.append(call_row)
            put_prices.append(put_row)
        return (call_prices, put_prices)
    
    def calculate_greeks(self, greek:str) -> Tuple[List[List[int]], List[List[int]], List[List[int]], List[List[int]], List[List[int]]]:
        call_greeks = []
        put_greeks = []
        match greek:
            # Delta
            case "Delta":
                for underlying_price in self.price_range_display:
                    call_row = []
                    put_row = []
                    for dte in self.time_list_display:
                        d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                                    (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                        call_row.append(round(norm.cdf(d1),3))
                        put_row.append(round(-norm.cdf(-d1),3))
                    call_greeks.append(call_row)
                    put_greeks.append(put_row)
            
            case "Gamma":
                for underlying_price in self.price_range_display:
                    call_row = []
                    put_row = []
                    for dte in self.time_list_display:
                        d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                                    (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                        call_row.append(round(norm.pdf(d1)/(underlying_price*self.volatility*np.sqrt(dte/365)),3))
                        put_row.append(round(norm.pdf(d1)/(underlying_price*self.volatility*np.sqrt(dte/365)),3))
                    call_greeks.append(call_row)
                    put_greeks.append(put_row)
            
            case "Vega":
                for underlying_price in self.price_range_display:
                    call_row = []
                    put_row = []
                    for dte in self.time_list_display:
                        d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                                    (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                        call_row.append(round(underlying_price*norm.pdf(d1)*np.sqrt(dte/365)*0.01,3)) #want to look at change in vol per 1% change in underlying
                        put_row.append(round(underlying_price*norm.pdf(d1)*np.sqrt(dte/365)*0.01,3))
                    call_greeks.append(call_row)
                    put_greeks.append(put_row)
            
            case "Theta":
                for underlying_price in self.price_range_display:
                    call_row = []
                    put_row = []
                    for dte in self.time_list_display:
                        d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                                    (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                        d2 = d1 - self.volatility*np.sqrt(dte/365)
                        call_theta = ((-underlying_price*norm.pdf(d1)*self.volatility)/(2*np.sqrt(dte/365)))-self.risk_free_rate*self.strike_price*np.exp(-self.risk_free_rate*(dte/365))*norm.cdf(d2)
                        put_theta = ((-underlying_price*norm.pdf(d1)*self.volatility)/(2*np.sqrt(dte/365)))+self.risk_free_rate*self.strike_price*np.exp(-self.risk_free_rate*(dte/365))*norm.cdf(-d2)
                        call_row.append(round(call_theta/365,3)) #look at theta per day, hence divide by 365
                        put_row.append(round(put_theta/365,3))
                    call_greeks.append(call_row)
                    put_greeks.append(put_row)
            
            case "Rho":
                for underlying_price in self.price_range_display:
                    call_row = []
                    put_row = []
                    for dte in self.time_list_display:
                        d1 = (1/(self.volatility * np.sqrt(dte/365)))*(np.log(underlying_price/self.strike_price) +
                                                                    (self.risk_free_rate+(self.volatility*self.volatility)/2)*(dte/365))
                        d2 = d1 - self.volatility*np.sqrt(dte/365)
                        call_row.append(round(self.strike_price*(dte/365)*np.exp(-self.risk_free_rate*(dte/365))*norm.cdf(d2)*0.01,3)) # look at changes per 1% change, hence multiply 0.01
                        put_row.append(round(-self.strike_price*(dte/365)*np.exp(-self.risk_free_rate*(dte/365))*norm.cdf(-d2)*0.01,3))
                    call_greeks.append(call_row)
                    put_greeks.append(put_row)
        return call_greeks, put_greeks 
        
    
    @staticmethod
    def calculate_pnl(option_projected_val: List[List[int]], amount_paid: float, denomination: str) -> List[List[int]]:
        pnl = [[0.0 for cols in range(0, len(option_projected_val[0]))] for rows in range(0,len(option_projected_val))]
        if (denomination == 'P/L $' or denomination == 'P/L %'):
            for r in range(0, len(option_projected_val)):
                for c in range(0, len(option_projected_val[0])):
                    pnl[r][c] = round(option_projected_val[r][c] - amount_paid,3)
                    if (denomination == 'P/L %'): 
                        pnl[r][c] = round((pnl[r][c] / amount_paid) * 100,3)
        return pnl
     