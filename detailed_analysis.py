"""
Detailed OEE Analysis - Loss Analysis, Root Cause, and Visualizations
=====================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from oee_analysis import OEEAnalyzer
import warnings
warnings.filterwarnings('ignore')

class DetailedOEEAnalysis:
    """
    Extended OEE Analysis with Loss Analysis, Root Cause, and Visualizations
    """
    
    def __init__(self, analyzer: OEEAnalyzer):
        self.analyzer = analyzer
        self.data = analyzer.oee_results
        self.raw_data = analyzer.raw_data
        
    def downtime_pareto_analysis(self):
        """
        Perform downtime Pareto analysis
        """
        print("\n" + "="*50)
        print("DOWNTIME PARETO ANALYSIS")
        print("="*50)
        
        # Filter records with downtime
        downtime_data = self.raw_data[self.raw_data['Downtime_Minutes'] > 0].copy()
        
        # Aggregate by downtime reason
        downtime_summary = downtime_data.groupby('Downtime_Reason').agg({
            'Downtime_Minutes': ['sum', 'mean', 'count'],
            'Machine_Name': 'count'
        }).round(2)
        
        downtime_summary.columns = ['Total_Downtime_Min', 'Avg_Downtime_Min', 'Frequency', 'Records']
        downtime_summary = downtime_summary.sort_values('Total_Downtime_Min', ascending=False)
        
        # Calculate cumulative percentage
        downtime_summary['Cumulative_Pct'] = (downtime_summary['Total_Downtime_Min'].cumsum() / 
                                            downtime_summary['Total_Downtime_Min'].sum() * 100).round(1)
        
        print("Downtime Analysis Summary:")
        print(downtime_summary)
        
        # Machine-specific downtime
        print("\nMachine-wise Downtime Breakdown:")
        machine_downtime = downtime_data.groupby(['Machine_Name', 'Downtime_Reason']).agg({
            'Downtime_Minutes': 'sum'
        }).round(2)
        print(machine_downtime)
        
        return downtime_summary, machine_downtime
    
    def speed_loss_analysis(self):
        """
        Analyze speed losses (ideal vs actual cycle time)
        """
        print("\n" + "="*50)
        print("SPEED LOSS ANALYSIS")
        print("="*50)
        
        # Calculate speed loss for each record
        self.data['Speed_Loss_Percent'] = ((self.data['Actual_Cycle_Time'] - self.data['Ideal_Cycle_Time']) / 
                                          self.data['Ideal_Cycle_Time'] * 100).round(2)
        
        # Speed loss by machine
        speed_loss_summary = self.data.groupby('Machine_Name').agg({
            'Speed_Loss_Percent': ['mean', 'std', 'max'],
            'Ideal_Cycle_Time': 'mean',
            'Actual_Cycle_Time': 'mean',
            'Total_Units_Produced': 'sum'
        }).round(2)
        
        speed_loss_summary.columns = ['Avg_Speed_Loss_Pct', 'Std_Speed_Loss', 'Max_Speed_Loss',
                                     'Avg_Ideal_Cycle', 'Avg_Actual_Cycle', 'Total_Units']
        
        print("Speed Loss Analysis by Machine:")
        print(speed_loss_summary)
        
        # Identify worst performers
        worst_speed = self.data.nlargest(10, 'Speed_Loss_Percent')[['Date', 'Machine_Name', 
                                                                    'Speed_Loss_Percent', 'Shift']]
        print("\nTop 10 Worst Speed Loss Records:")
        print(worst_speed)
        
        return speed_loss_summary, worst_speed
    
    def quality_loss_analysis(self):
        """
        Analyze quality losses
        """
        print("\n" + "="*50)
        print("QUALITY LOSS ANALYSIS")
        print("="*50)
        
        # Calculate defect rate
        self.data['Defect_Rate_Percent'] = (self.data['Defective_Units'] / 
                                           self.data['Total_Units_Produced'] * 100).round(3)
        
        # Quality analysis by machine
        quality_summary = self.data.groupby('Machine_Name').agg({
            'Defect_Rate_Percent': ['mean', 'std', 'max'],
            'Quality': ['mean', 'min'],
            'Defective_Units': 'sum',
            'Total_Units_Produced': 'sum'
        }).round(3)
        
        quality_summary.columns = ['Avg_Defect_Rate', 'Std_Defect_Rate', 'Max_Defect_Rate',
                                  'Avg_Quality', 'Min_Quality', 'Total_Defects', 'Total_Units']
        
        print("Quality Loss Analysis by Machine:")
        print(quality_summary)
        
        # Quality by shift
        shift_quality = self.data.groupby('Shift').agg({
            'Defect_Rate_Percent': 'mean',
            'Quality': 'mean'
        }).round(2)
        
        print("\nQuality Performance by Shift:")
        print(shift_quality)
        
        return quality_summary, shift_quality
    
    def root_cause_analysis(self):
        """
        Perform structured root cause analysis
        """
        print("\n" + "="*50)
        print("ROOT CAUSE ANALYSIS")
        print("="*50)
        
        # Fishbone Analysis for top issues
        print("\nFISHBONE ANALYSIS - TOP DOWNTIME CAUSE: BREAKDOWN")
        print("-" * 60)
        
        fishbone_analysis = {
            'Man': [
                'Insufficient training on equipment operation',
                'Fatigue during night shifts',
                'Lack of standard operating procedures',
                'Inadequate supervision during changeovers'
            ],
            'Machine': [
                'Aging equipment (average 8+ years)',
                'Inadequate preventive maintenance',
                'Worn-out components in mixer and filler',
                'Sensor calibration issues'
            ],
            'Method': [
                'Reactive maintenance approach',
                'Inefficient changeover procedures',
                'Lack of real-time monitoring',
                'No standardized troubleshooting guides'
            ],
            'Material': [
                'Inconsistent raw material quality',
                'Contamination in ingredients',
                'Variations in dough consistency',
                'Packaging material jams'
            ],
            'Environment': [
                'High humidity affecting equipment',
                'Temperature fluctuations',
                'Poor lighting in work areas',
                'Vibration from adjacent equipment'
            ]
        }
        
        for category, causes in fishbone_analysis.items():
            print(f"\n{category}:")
            for i, cause in enumerate(causes, 1):
                print(f"  {i}. {cause}")
        
        # 5 Whys Analysis for Breakdown
        print("\n" + "="*50)
        print("5 WHYS ANALYSIS - EQUIPMENT BREAKDOWN")
        print("="*50)
        
        five_whys = [
            "Why did the equipment breakdown occur?",
            "→ Why was the component not replaced during maintenance?",
            "→ Why was the preventive maintenance schedule not followed?",
            "→ Why are maintenance resources insufficient?",
            "→ Why has the maintenance budget not been increased?"
        ]
        
        for i, why in enumerate(five_whys, 1):
            print(f"{i}. {why}")
        
        return fishbone_analysis, five_whys
    
    def create_visualizations(self):
        """
        Create comprehensive OEE visualizations
        """
        print("\n" + "="*50)
        print("CREATING VISUALIZATIONS")
        print("="*50)
        
        # Add YearMonth column if not exists
        if 'YearMonth' not in self.data.columns:
            self.data['YearMonth'] = pd.to_datetime(self.data['Date']).dt.to_period('M')
        
        # Set up the figure with multiple subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. OEE Trend by Month
        plt.subplot(3, 3, 1)
        monthly_oee = self.data.groupby('YearMonth')['OEE'].mean()
        plt.plot(range(len(monthly_oee)), monthly_oee.values, marker='o', linewidth=2)
        plt.title('Monthly OEE Trend', fontsize=12, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('OEE (%)')
        plt.grid(True, alpha=0.3)
        plt.xticks(range(len(monthly_oee)), [str(m) for m in monthly_oee.index], rotation=45)
        
        # 2. Machine-wise OEE Comparison
        plt.subplot(3, 3, 2)
        machine_oee = self.data.groupby('Machine_Name')['OEE'].mean().sort_values(ascending=False)
        bars = plt.bar(machine_oee.index, machine_oee.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        plt.title('OEE by Machine', fontsize=12, fontweight='bold')
        plt.ylabel('OEE (%)')
        plt.xticks(rotation=45)
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 3. Availability, Performance, Quality Comparison
        plt.subplot(3, 3, 3)
        metrics = ['Availability', 'Performance', 'Quality']
        machine_metrics = self.data.groupby('Machine_Name')[metrics].mean()
        x = np.arange(len(machine_metrics.index))
        width = 0.25
        
        plt.bar(x - width, machine_metrics['Availability'], width, label='Availability', color='#FF6B6B')
        plt.bar(x, machine_metrics['Performance'], width, label='Performance', color='#4ECDC4')
        plt.bar(x + width, machine_metrics['Quality'], width, label='Quality', color='#45B7D1')
        
        plt.title('OEE Components by Machine', fontsize=12, fontweight='bold')
        plt.xlabel('Machine')
        plt.ylabel('Percentage (%)')
        plt.xticks(x, machine_metrics.index, rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 4. Downtime Pareto Chart
        plt.subplot(3, 3, 4)
        downtime_data = self.raw_data[self.raw_data['Downtime_Minutes'] > 0]
        downtime_pareto = downtime_data.groupby('Downtime_Reason')['Downtime_Minutes'].sum().sort_values(ascending=False)
        
        # Create pareto chart
        ax1 = plt.gca()
        bars = ax1.bar(range(len(downtime_pareto)), downtime_pareto.values, color='#FF6B6B')
        ax1.set_title('Downtime Pareto Analysis', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Total Downtime (Minutes)')
        ax1.set_xticks(range(len(downtime_pareto)))
        ax1.set_xticklabels(downtime_pareto.index, rotation=45)
        
        # Add cumulative line
        ax2 = ax1.twinx()
        cumulative = np.cumsum(downtime_pareto.values) / downtime_pareto.sum() * 100
        ax2.plot(range(len(downtime_pareto)), cumulative, 'o-', color='#45B7D1', linewidth=2)
        ax2.set_ylabel('Cumulative Percentage (%)', color='#45B7D1')
        ax2.axhline(y=80, color='red', linestyle='--', alpha=0.7)
        ax2.text(len(downtime_pareto)-1, 82, '80%', color='red', fontweight='bold')
        
        # 5. Shift Performance Comparison
        plt.subplot(3, 3, 5)
        shift_oee = self.data.groupby('Shift')['OEE'].mean()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        bars = plt.bar(shift_oee.index, shift_oee.values, color=colors)
        plt.title('OEE by Shift', fontsize=12, fontweight='bold')
        plt.ylabel('OEE (%)')
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 6. Speed Loss by Machine
        plt.subplot(3, 3, 6)
        speed_loss = self.data.groupby('Machine_Name')['Speed_Loss_Percent'].mean().sort_values(ascending=False)
        bars = plt.bar(speed_loss.index, speed_loss.values, color='#96CEB4')
        plt.title('Average Speed Loss by Machine', fontsize=12, fontweight='bold')
        plt.ylabel('Speed Loss (%)')
        plt.xticks(rotation=45)
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 7. Quality Rate by Machine
        plt.subplot(3, 3, 7)
        quality_rate = self.data.groupby('Machine_Name')['Quality'].mean().sort_values(ascending=False)
        bars = plt.bar(quality_rate.index, quality_rate.values, color='#45B7D1')
        plt.title('Quality Rate by Machine', fontsize=12, fontweight='bold')
        plt.ylabel('Quality (%)')
        plt.xticks(rotation=45)
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom')
        
        # 8. OEE Distribution
        plt.subplot(3, 3, 8)
        plt.hist(self.data['OEE'], bins=20, color='#4ECDC4', alpha=0.7, edgecolor='black')
        plt.title('OEE Distribution', fontsize=12, fontweight='bold')
        plt.xlabel('OEE (%)')
        plt.ylabel('Frequency')
        plt.axvline(self.data['OEE'].mean(), color='red', linestyle='--', linewidth=2)
        plt.text(self.data['OEE'].mean() + 1, plt.ylim()[1]*0.9, 
                f'Mean: {self.data["OEE"].mean():.1f}%', color='red', fontweight='bold')
        
        # 9. Production Volume Trend
        plt.subplot(3, 3, 9)
        monthly_production = self.data.groupby('YearMonth')['Total_Units_Produced'].sum()
        plt.plot(range(len(monthly_production)), monthly_production.values, marker='s', linewidth=2, color='#FF6B6B')
        plt.title('Monthly Production Volume', fontsize=12, fontweight='bold')
        plt.xlabel('Month')
        plt.ylabel('Units Produced')
        plt.grid(True, alpha=0.3)
        plt.xticks(range(len(monthly_production)), [str(m) for m in monthly_production.index], rotation=45)
        
        plt.tight_layout()
        plt.savefig('c:/Users/rohil/Downloads/project 1/oee_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Dashboard saved as 'oee_dashboard.png'")
        
        return fig

def main():
    """
    Main execution for detailed analysis
    """
    # Initialize and run basic analysis
    analyzer = OEEAnalyzer()
    production_data = analyzer.generate_production_data(4000)
    oee_data = analyzer.calculate_oee_metrics(production_data)
    
    # Perform detailed analysis
    detailed_analyzer = DetailedOEEAnalysis(analyzer)
    
    # Loss Analysis
    downtime_summary, machine_downtime = detailed_analyzer.downtime_pareto_analysis()
    speed_loss_summary, worst_speed = detailed_analyzer.speed_loss_analysis()
    quality_summary, shift_quality = detailed_analyzer.quality_loss_analysis()
    
    # Root Cause Analysis
    fishbone_analysis, five_whys = detailed_analyzer.root_cause_analysis()
    
    # Create Visualizations
    fig = detailed_analyzer.create_visualizations()
    
    print("\n" + "="*60)
    print("DETAILED ANALYSIS COMPLETE")
    print("="*60)
    
    return detailed_analyzer

if __name__ == "__main__":
    detailed_analyzer = main()
