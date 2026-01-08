"""
OEE & Productivity Improvement in FMCG Manufacturing Plant
==========================================================

Project: Comprehensive OEE analysis for biscuit production line
Author: Manufacturing Analytics Consultant
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style for professional visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class OEEAnalyzer:
    """
    Comprehensive OEE Analysis Tool for FMCG Manufacturing
    """
    
    def __init__(self):
        self.machines = ['Mixer', 'Filler', 'Packer', 'Conveyor']
        self.shifts = ['Morning', 'Afternoon', 'Night']
        self.downtime_reasons = ['Breakdown', 'Changeover', 'Cleaning', 'Minor Stoppage', 'Power Failure']
        self.defect_types = ['Weight Variation', 'Packaging Defect', 'Contamination', 'Shape Defect', 'Sealing Issue']
        
        # FMCG Biscuit Production Parameters (realistic values)
        self.cycle_times = {
            'Mixer': {'ideal': 45, 'actual_range': (48, 65)},  # seconds per batch
            'Filler': {'ideal': 2.5, 'actual_range': (2.8, 4.2)},  # seconds per unit
            'Packer': {'ideal': 3.0, 'actual_range': (3.2, 4.8)},  # seconds per unit
            'Conveyor': {'ideal': 1.8, 'actual_range': (1.9, 2.5)}  # seconds per unit
        }
        
        self.planned_production_minutes = {
            'Morning': 480,    # 8 hours
            'Afternoon': 480,  # 8 hours  
            'Night': 420       # 7 hours
        }
        
        # Initialize data storage
        self.raw_data = None
        self.oee_results = None
        
    def generate_production_data(self, num_records: int = 4000) -> pd.DataFrame:
        """
        Generate realistic FMCG production data for 6 months
        """
        print(f"Generating {num_records} records of production data...")
        
        data = []
        start_date = datetime(2025, 7, 1)  # 6 months period
        
        for i in range(num_records):
            # Generate date with realistic distribution
            days_offset = random.randint(0, 180)  # 6 months
            current_date = start_date + timedelta(days=days_offset)
            
            # Skip weekends (reduced production)
            if current_date.weekday() >= 6 and random.random() < 0.7:
                continue
                
            shift = random.choice(self.shifts)
            machine = random.choice(self.machines)
            
            # Planned production time
            planned_time = self.planned_production_minutes[shift]
            
            # Generate realistic downtime (FMCG patterns)
            if machine == 'Mixer':
                downtime_mean = 45  # Higher downtime for mixing
            elif machine == 'Filler':
                downtime_mean = 35
            elif machine == 'Packer':
                downtime_mean = 25
            else:  # Conveyor
                downtime_mean = 15
                
            downtime_minutes = max(0, np.random.normal(downtime_mean, 15))
            downtime_minutes = min(downtime_minutes, planned_time * 0.5)  # Cap at 50% of planned time
            
            # Assign downtime reason
            if downtime_minutes > 0:
                if downtime_minutes > 60:
                    reason = random.choice(['Breakdown', 'Changeover'])
                elif downtime_minutes > 30:
                    reason = random.choice(['Cleaning', 'Breakdown'])
                else:
                    reason = random.choice(['Minor Stoppage', 'Power Failure'])
            else:
                reason = 'None'
            
            # Cycle times
            ideal_cycle = self.cycle_times[machine]['ideal']
            actual_cycle = np.random.uniform(*self.cycle_times[machine]['actual_range'])
            
            # Production calculations
            available_time = planned_time - downtime_minutes
            total_units = int(available_time * 60 / actual_cycle)
            
            # Quality losses (FMCG realistic defect rates)
            if machine == 'Filler':
                defect_rate = np.random.uniform(0.8, 3.5)  # Higher defects in filling
            elif machine == 'Packer':
                defect_rate = np.random.uniform(0.5, 2.0)
            else:
                defect_rate = np.random.uniform(0.2, 1.0)
                
            defective_units = int(total_units * defect_rate / 100)
            
            data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Shift': shift,
                'Machine_Name': machine,
                'Planned_Production_Time': planned_time,
                'Downtime_Minutes': round(downtime_minutes, 1),
                'Downtime_Reason': reason,
                'Ideal_Cycle_Time': ideal_cycle,
                'Actual_Cycle_Time': round(actual_cycle, 2),
                'Total_Units_Produced': total_units,
                'Defective_Units': defective_units,
                'Good_Units': total_units - defective_units
            })
        
        df = pd.DataFrame(data)
        self.raw_data = df
        
        print(f"Generated {len(df)} production records")
        print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"Machines: {df['Machine_Name'].unique()}")
        print(f"Total units produced: {df['Total_Units_Produced'].sum():,}")
        
        return df
    
    def calculate_oee_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate comprehensive OEE metrics
        """
        print("Calculating OEE metrics...")
        
        # Availability = (Planned - Downtime) / Planned
        df['Availability'] = ((df['Planned_Production_Time'] - df['Downtime_Minutes']) / 
                              df['Planned_Production_Time']) * 100
        
        # Performance = (Ideal Cycle Time × Total Units) / Operating Time
        operating_time = df['Planned_Production_Time'] - df['Downtime_Minutes']
        df['Performance'] = (df['Ideal_Cycle_Time'] * df['Total_Units_Produced'] / 
                            (operating_time * 60)) * 100
        
        # Quality = Good Units / Total Units
        df['Quality'] = (df['Good_Units'] / df['Total_Units_Produced']) * 100
        
        # Overall OEE = Availability × Performance × Quality / 10000
        df['OEE'] = (df['Availability'] * df['Performance'] * df['Quality']) / 10000
        
        # Cap values at 100% for realism
        metric_cols = ['Availability', 'Performance', 'Quality', 'OEE']
        df[metric_cols] = df[metric_cols].clip(upper=100)
        
        self.oee_results = df.copy()
        
        print("OEE Calculation Summary:")
        print(f"Average OEE: {df['OEE'].mean():.2f}%")
        print(f"Average Availability: {df['Availability'].mean():.2f}%")
        print(f"Average Performance: {df['Performance'].mean():.2f}%")
        print(f"Average Quality: {df['Quality'].mean():.2f}%")
        
        return df
    
    def machine_wise_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Machine-wise OEE analysis
        """
        machine_stats = df.groupby('Machine_Name').agg({
            'OEE': ['mean', 'std', 'min', 'max'],
            'Availability': 'mean',
            'Performance': 'mean',
            'Quality': 'mean',
            'Total_Units_Produced': 'sum',
            'Defective_Units': 'sum',
            'Downtime_Minutes': 'mean'
        }).round(2)
        
        machine_stats.columns = ['OEE_Mean', 'OEE_Std', 'OEE_Min', 'OEE_Max',
                                'Availability_Mean', 'Performance_Mean', 'Quality_Mean',
                                'Total_Units', 'Defective_Units', 'Avg_Downtime']
        
        return machine_stats
    
    def shift_wise_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Shift-wise OEE analysis
        """
        shift_stats = df.groupby('Shift').agg({
            'OEE': 'mean',
            'Availability': 'mean',
            'Performance': 'mean',
            'Quality': 'mean',
            'Total_Units_Produced': 'sum',
            'Downtime_Minutes': 'mean'
        }).round(2)
        
        return shift_stats
    
    def monthly_trend_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Monthly OEE trend analysis
        """
        df['YearMonth'] = pd.to_datetime(df['Date']).dt.to_period('M')
        
        monthly_stats = df.groupby('YearMonth').agg({
            'OEE': 'mean',
            'Availability': 'mean',
            'Performance': 'mean',
            'Quality': 'mean',
            'Total_Units_Produced': 'sum',
            'Downtime_Minutes': 'mean'
        }).round(2)
        
        return monthly_stats

def main():
    """
    Main execution function
    """
    print("=" * 60)
    print("OEE & PRODUCTIVITY IMPROVEMENT PROJECT")
    print("FMCG Manufacturing Plant - Biscuit Production Line")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = OEEAnalyzer()
    
    # Generate production data
    production_data = analyzer.generate_production_data(4000)
    
    # Calculate OEE metrics
    oee_data = analyzer.calculate_oee_metrics(production_data)
    
    # Perform analyses
    machine_analysis = analyzer.machine_wise_analysis(oee_data)
    shift_analysis = analyzer.shift_wise_analysis(oee_data)
    monthly_analysis = analyzer.monthly_trend_analysis(oee_data)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    return analyzer, production_data, oee_data, machine_analysis, shift_analysis, monthly_analysis

if __name__ == "__main__":
    analyzer, production_data, oee_data, machine_analysis, shift_analysis, monthly_analysis = main()
