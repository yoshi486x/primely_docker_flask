import pprint as pp

from primely.models import paycheck_analyzer


def paycheck_analysis():
    """Handles every process of paycheck-graph package."""
    full_analyzer = paycheck_analyzer.FullAnalyzer()
    full_analyzer.starting_msg()
    full_analyzer.create_input_queue()
    full_analyzer.process_all_input_data()
    full_analyzer.create_dataframe_in_time_series()
    # full_analyzer.visualize_income_timechart()
    # full_analyzer.plot_graph()
    full_analyzer.ending_msg()
