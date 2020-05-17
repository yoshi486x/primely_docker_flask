from primely.models import paycheck_analyzer


def paycheck_analysis():
    """Handles every process of paycheck-graph package."""
    full_analyzer = paycheck_analyzer.FullAnalyzer()

    try:
        # top 
        full_analyzer.starting_msg()
        full_analyzer.create_input_queue()
        
        # middle
        full_analyzer.process_all_input_data()
        full_analyzer.create_dataframe_in_time_series()
        paycheck_series = full_analyzer.get_packaged_paycheck_series()
        
        # bottom
        full_analyzer.export_in_jsonfile(paycheck_series)
        full_analyzer.export_income_timeline()
        full_analyzer.ending_msg()
    except:
        return False
    else:
        return True
