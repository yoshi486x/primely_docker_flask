import pprint as pp

from primely.models import paycheck_analyzer


def paycheck_analysis():
    """Handles every process of paycheck-graph package."""
    full_analyzer = paycheck_analyzer.FullAnalyzer()
    full_analyzer.process_all_data()
    full_analyzer.visualize_income_timechart()
