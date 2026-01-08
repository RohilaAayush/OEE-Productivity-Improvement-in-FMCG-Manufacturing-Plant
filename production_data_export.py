"""
Export Production Data to Excel Format
======================================

FMCG Manufacturing Plant - OEE Analysis Project
"""

import pandas as pd
from oee_analysis import OEEAnalyzer
from detailed_analysis import DetailedOEEAnalysis
import warnings
warnings.filterwarnings('ignore')

def export_production_data_to_excel():
    """
    Export all production data and analysis results to Excel format
    """
    print("Generating Excel export of production data...")
    
    # Initialize and run analysis
    analyzer = OEEAnalyzer()
    production_data = analyzer.generate_production_data(4000)
    oee_data = analyzer.calculate_oee_metrics(production_data)
    
    detailed_analyzer = DetailedOEEAnalysis(analyzer)
    
    # Create Excel writer with multiple sheets
    with pd.ExcelWriter('c:/Users/rohil/Downloads/project 1/OEE_Analysis_Data.xlsx', engine='openpyxl') as writer:
        
        # Sheet 1: Raw Production Data
        print("Exporting Raw Production Data...")
        raw_data_export = production_data.copy()
        raw_data_export['Date'] = pd.to_datetime(raw_data_export['Date'])
        raw_data_export = raw_data_export.sort_values(['Date', 'Shift', 'Machine_Name'])
        raw_data_export.to_excel(writer, sheet_name='Raw_Production_Data', index=False)
        
        # Sheet 2: OEE Calculated Data
        print("Exporting OEE Calculated Data...")
        oee_export = oee_data.copy()
        oee_export['Date'] = pd.to_datetime(oee_export['Date'])
        oee_export = oee_export.sort_values(['Date', 'Shift', 'Machine_Name'])
        
        # Reorder columns for better readability
        oee_columns = ['Date', 'Shift', 'Machine_Name', 'Planned_Production_Time', 
                      'Downtime_Minutes', 'Downtime_Reason', 'Ideal_Cycle_Time', 
                      'Actual_Cycle_Time', 'Total_Units_Produced', 'Defective_Units', 
                      'Good_Units', 'Availability', 'Performance', 'Quality', 'OEE']
        oee_export = oee_export[oee_columns]
        oee_export.to_excel(writer, sheet_name='OEE_Calculated_Data', index=False)
        
        # Sheet 3: Machine-wise Analysis
        print("Exporting Machine-wise Analysis...")
        machine_analysis = analyzer.machine_wise_analysis(oee_data)
        machine_analysis.to_excel(writer, sheet_name='Machine_Analysis')
        
        # Sheet 4: Shift-wise Analysis
        print("Exporting Shift-wise Analysis...")
        shift_analysis = analyzer.shift_wise_analysis(oee_data)
        shift_analysis.to_excel(writer, sheet_name='Shift_Analysis')
        
        # Sheet 5: Monthly Trend Analysis
        print("Exporting Monthly Trend Analysis...")
        monthly_analysis = analyzer.monthly_trend_analysis(oee_data)
        monthly_analysis.to_excel(writer, sheet_name='Monthly_Trends')
        
        # Sheet 6: Downtime Analysis
        print("Exporting Downtime Analysis...")
        downtime_summary, machine_downtime = detailed_analyzer.downtime_pareto_analysis()
        downtime_summary.to_excel(writer, sheet_name='Downtime_Summary')
        
        # Sheet 7: Speed Loss Analysis
        print("Exporting Speed Loss Analysis...")
        speed_loss_summary, worst_speed = detailed_analyzer.speed_loss_analysis()
        speed_loss_summary.to_excel(writer, sheet_name='Speed_Loss_Analysis')
        worst_speed.to_excel(writer, sheet_name='Worst_Speed_Records', index=False)
        
        # Sheet 8: Quality Loss Analysis
        print("Exporting Quality Loss Analysis...")
        quality_summary, shift_quality = detailed_analyzer.quality_loss_analysis()
        quality_summary.to_excel(writer, sheet_name='Quality_Analysis')
        shift_quality.to_excel(writer, sheet_name='Shift_Quality')
        
        # Sheet 9: Data Summary Statistics
        print("Exporting Summary Statistics...")
        summary_stats = pd.DataFrame({
            'Metric': [
                'Total Records',
                'Date Range Start',
                'Date Range End',
                'Total Machines',
                'Total Shifts',
                'Total Units Produced',
                'Total Defective Units',
                'Average OEE (%)',
                'Average Availability (%)',
                'Average Performance (%)',
                'Average Quality (%)',
                'Total Downtime (Minutes)',
                'Average Cycle Time (Seconds)',
                'Production Days'
            ],
            'Value': [
                len(oee_data),
                oee_data['Date'].min(),
                oee_data['Date'].max(),
                len(oee_data['Machine_Name'].unique()),
                len(oee_data['Shift'].unique()),
                oee_data['Total_Units_Produced'].sum(),
                oee_data['Defective_Units'].sum(),
                round(oee_data['OEE'].mean(), 2),
                round(oee_data['Availability'].mean(), 2),
                round(oee_data['Performance'].mean(), 2),
                round(oee_data['Quality'].mean(), 2),
                oee_data['Downtime_Minutes'].sum(),
                round(oee_data['Actual_Cycle_Time'].mean(), 2),
                len(oee_data['Date'].unique())
            ]
        })
        summary_stats.to_excel(writer, sheet_name='Summary_Statistics', index=False)
        
        # Sheet 10: Top Performers
        print("Exporting Top Performers...")
        top_performers = pd.DataFrame({
            'Category': [
                'Best OEE Performance',
                'Worst OEE Performance',
                'Best Availability',
                'Best Performance',
                'Best Quality',
                'Highest Production',
                'Lowest Downtime',
                'Best Shift Performance'
            ],
            'Machine/Shift': [
                oee_data.loc[oee_data['OEE'].idxmax(), 'Machine_Name'],
                oee_data.loc[oee_data['OEE'].idxmin(), 'Machine_Name'],
                oee_data.loc[oee_data['Availability'].idxmax(), 'Machine_Name'],
                oee_data.loc[oee_data['Performance'].idxmax(), 'Machine_Name'],
                oee_data.loc[oee_data['Quality'].idxmax(), 'Machine_Name'],
                oee_data.loc[oee_data['Total_Units_Produced'].idxmax(), 'Machine_Name'],
                oee_data.loc[oee_data['Downtime_Minutes'].idxmin(), 'Machine_Name'],
                oee_data.groupby('Shift')['OEE'].mean().idxmax()
            ],
            'Value': [
                f"{oee_data['OEE'].max():.2f}%",
                f"{oee_data['OEE'].min():.2f}%",
                f"{oee_data['Availability'].max():.2f}%",
                f"{oee_data['Performance'].max():.2f}%",
                f"{oee_data['Quality'].max():.2f}%",
                f"{oee_data['Total_Units_Produced'].max():,.0f}",
                f"{oee_data['Downtime_Minutes'].min():.1f} min",
                f"{oee_data.groupby('Shift')['OEE'].mean().max():.2f}%"
            ],
            'Date': [
                oee_data.loc[oee_data['OEE'].idxmax(), 'Date'],
                oee_data.loc[oee_data['OEE'].idxmin(), 'Date'],
                oee_data.loc[oee_data['Availability'].idxmax(), 'Date'],
                oee_data.loc[oee_data['Performance'].idxmax(), 'Date'],
                oee_data.loc[oee_data['Quality'].idxmax(), 'Date'],
                oee_data.loc[oee_data['Total_Units_Produced'].idxmax(), 'Date'],
                oee_data.loc[oee_data['Downtime_Minutes'].idxmin(), 'Date'],
                'Overall'
            ]
        })
        top_performers.to_excel(writer, sheet_name='Top_Performers', index=False)
    
    print("Excel export completed successfully!")
    print("File saved as: OEE_Analysis_Data.xlsx")
    print("\nSheets included:")
    print("1. Raw_Production_Data - Original production records")
    print("2. OEE_Calculated_Data - Data with OEE metrics calculated")
    print("3. Machine_Analysis - Performance by machine")
    print("4. Shift_Analysis - Performance by shift")
    print("5. Monthly_Trends - Monthly performance trends")
    print("6. Downtime_Summary - Downtime Pareto analysis")
    print("7. Speed_Loss_Analysis - Speed loss by machine")
    print("8. Quality_Analysis - Quality metrics by machine")
    print("9. Summary_Statistics - Overall project statistics")
    print("10. Top_Performers - Best and worst performing records")

if __name__ == "__main__":
    export_production_data_to_excel()
