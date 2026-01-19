from tools.breakeven.ui import show_break_even_shift_calculator
from tools.substitution.ui import show_substitution_analysis
from tools.complementary.ui import show_complementary_analysis
from tools.price_cut.ui import show_price_cut
from tools.clv.ui import show_clv_calculator

def run_engine(scenario, state):
    if scenario == "Price Change":
        show_price_cut(state)
    elif scenario == "Discount with Complementary Products":
        show_complementary(state)
    elif scenario == "Product Substitution":
        show_substitution(state)
    elif scenario == "Break-Even Shift":
        show_break_even_shift_calculator(state)
    elif scenario == "Customer Lifetime Value":
        show_clv(state)
