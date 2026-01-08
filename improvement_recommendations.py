"""
OEE Improvement Recommendations & Impact Simulation
===================================================

FMCG Manufacturing Plant - Biscuit Production Line
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from oee_analysis import OEEAnalyzer
from detailed_analysis import DetailedOEEAnalysis
import warnings
warnings.filterwarnings('ignore')

class OEEImprovementPlan:
    """
    Comprehensive OEE Improvement Plan with FMCG-specific recommendations
    """
    
    def __init__(self, analyzer: OEEAnalyzer, detailed_analyzer: DetailedOEEAnalysis):
        self.analyzer = analyzer
        self.detailed_analyzer = detailed_analyzer
        self.current_data = analyzer.oee_results.copy()
        self.baseline_oee = self.current_data['OEE'].mean()
        
    def generate_improvement_recommendations(self):
        """
        Generate FMCG-specific improvement recommendations
        """
        print("\n" + "="*60)
        print("OEE IMPROVEMENT RECOMMENDATIONS")
        print("="*60)
        
        recommendations = {
            'Availability_Improvements': [
                {
                    'Action': 'Implement Predictive Maintenance Program',
                    'Target': 'Reduce breakdown downtime by 40%',
                    'Timeline': '3-6 months',
                    'Investment': '$150,000',
                    'Expected_Gain': '+8.5% OEE',
                    'FMCG_Specific': 'Install vibration sensors on mixers and fillers, implement condition-based monitoring'
                },
                {
                    'Action': 'SMED (Single-Minute Exchange of Die)',
                    'Target': 'Reduce changeover time by 60%',
                    'Timeline': '2-4 months',
                    'Investment': '$75,000',
                    'Expected_Gain': '+4.2% OEE',
                    'FMCG_Specific': 'Standardized changeover procedures for biscuit recipe changes, pre-staged tooling'
                },
                {
                    'Action': 'Operator Training & Certification',
                    'Target': 'Reduce minor stoppages by 50%',
                    'Timeline': '1-3 months',
                    'Investment': '$45,000',
                    'Expected_Gain': '+3.1% OEE',
                    'FMCG_Specific': 'Focus on filler and packer operation, troubleshooting common jams'
                },
                {
                    'Action': 'Power Backup Systems',
                    'Target': 'Eliminate power failure downtime',
                    'Timeline': '1-2 months',
                    'Investment': '$80,000',
                    'Expected_Gain': '+2.3% OEE',
                    'FMCG_Specific': 'UPS systems for critical controls, backup generator for main production line'
                }
            ],
            
            'Performance_Improvements': [
                {
                    'Action': 'Process Optimization for Filler',
                    'Target': 'Improve filler speed by 25%',
                    'Timeline': '2-3 months',
                    'Investment': '$60,000',
                    'Expected_Gain': '+6.8% OEE',
                    'FMCG_Specific': 'Optimize biscuit dough consistency, adjust filling head pressure'
                },
                {
                    'Action': 'Conveyor Speed Synchronization',
                    'Target': 'Reduce conveyor bottlenecks by 30%',
                    'Timeline': '1-2 months',
                    'Investment': '$35,000',
                    'Expected_Gain': '+3.5% OEE',
                    'FMCG_Specific': 'Install variable frequency drives, implement line balancing'
                },
                {
                    'Action': 'Mixer Cycle Time Reduction',
                    'Target': 'Reduce mixing time by 15%',
                    'Timeline': '3-4 months',
                    'Investment': '$90,000',
                    'Expected_Gain': '+4.1% OEE',
                    'FMCG_Specific': 'High-speed mixers, improved ingredient feeding systems'
                }
            ],
            
            'Quality_Improvements': [
                {
                    'Action': 'Automated Weight Control System',
                    'Target': 'Reduce weight variations by 70%',
                    'Timeline': '2-3 months',
                    'Investment': '$120,000',
                    'Expected_Gain': '+2.8% OEE',
                    'FMCG_Specific': 'In-line checkweighers with feedback control, statistical process control'
                },
                {
                    'Action': 'Packaging Quality Enhancement',
                    'Target': 'Reduce packaging defects by 60%',
                    'Timeline': '1-2 months',
                    'Investment': '$55,000',
                    'Expected_Gain': '+1.9% OEE',
                    'FMCG_Specific': 'Improved sealing systems, vision inspection for packaging defects'
                },
                {
                    'Action': 'Raw Material Quality Control',
                    'Target': 'Reduce contamination by 80%',
                    'Timeline': '1-3 months',
                    'Investment': '$40,000',
                    'Expected_Gain': '+1.5% OEE',
                    'FMCG_Specific': 'Supplier quality programs, incoming inspection protocols'
                }
            ]
        }
        
        # Print recommendations
        for category, actions in recommendations.items():
            print(f"\n{category.replace('_', ' ').upper()}:")
            print("-" * 50)
            for i, action in enumerate(actions, 1):
                print(f"\n{i}. {action['Action']}")
                print(f"   Target: {action['Target']}")
                print(f"   Timeline: {action['Timeline']}")
                print(f"   Investment: {action['Investment']}")
                print(f"   Expected Gain: {action['Expected_Gain']}")
                print(f"   FMCG Specific: {action['FMCG_Specific']}")
        
        return recommendations
    
    def simulate_improvement_impact(self, recommendations):
        """
        Simulate the impact of improvements on OEE
        """
        print("\n" + "="*60)
        print("IMPROVEMENT IMPACT SIMULATION")
        print("="*60)
        
        # Create improved dataset
        improved_data = self.current_data.copy()
        
        # Apply improvements based on recommendations
        # Availability improvements
        improved_data['Downtime_Minutes'] = improved_data['Downtime_Minutes'] * 0.65  # 35% reduction
        improved_data['Availability'] = ((improved_data['Planned_Production_Time'] - improved_data['Downtime_Minutes']) / 
                                        improved_data['Planned_Production_Time']) * 100
        
        # Performance improvements
        improved_data['Actual_Cycle_Time'] = improved_data['Actual_Cycle_Time'] * 0.85  # 15% improvement
        operating_time = improved_data['Planned_Production_Time'] - improved_data['Downtime_Minutes']
        improved_data['Performance'] = (improved_data['Ideal_Cycle_Time'] * improved_data['Total_Units_Produced'] / 
                                      (operating_time * 60)) * 100
        
        # Quality improvements
        improved_data['Defective_Units'] = improved_data['Defective_Units'] * 0.5  # 50% reduction
        improved_data['Good_Units'] = improved_data['Total_Units_Produced'] - improved_data['Defective_Units']
        improved_data['Quality'] = (improved_data['Good_Units'] / improved_data['Total_Units_Produced']) * 100
        
        # Recalculate OEE
        improved_data['OEE'] = (improved_data['Availability'] * improved_data['Performance'] * improved_data['Quality']) / 10000
        
        # Cap values
        metric_cols = ['Availability', 'Performance', 'Quality', 'OEE']
        improved_data[metric_cols] = improved_data[metric_cols].clip(upper=100)
        
        # Calculate improvements
        baseline_oee = self.current_data['OEE'].mean()
        improved_oee = improved_data['OEE'].mean()
        oee_improvement = improved_oee - baseline_oee
        
        baseline_availability = self.current_data['Availability'].mean()
        improved_availability = improved_data['Availability'].mean()
        availability_improvement = improved_availability - baseline_availability
        
        baseline_performance = self.current_data['Performance'].mean()
        improved_performance = improved_data['Performance'].mean()
        performance_improvement = improved_performance - baseline_performance
        
        baseline_quality = self.current_data['Quality'].mean()
        improved_quality = improved_data['Quality'].mean()
        quality_improvement = improved_quality - baseline_quality
        
        # Production impact
        baseline_production = self.current_data['Total_Units_Produced'].sum()
        improved_production = baseline_production * (improved_oee / baseline_oee)
        production_increase = improved_production - baseline_production
        
        # Financial impact (assuming $0.50 per biscuit)
        revenue_increase = production_increase * 0.50
        
        print("\nBEFORE vs AFTER COMPARISON:")
        print("-" * 40)
        print(f"OEE: {baseline_oee:.2f}% → {improved_oee:.2f}% (+{oee_improvement:.2f}%)")
        print(f"Availability: {baseline_availability:.2f}% → {improved_availability:.2f}% (+{availability_improvement:.2f}%)")
        print(f"Performance: {baseline_performance:.2f}% → {improved_performance:.2f}% (+{performance_improvement:.2f}%)")
        print(f"Quality: {baseline_quality:.2f}% → {improved_quality:.2f}% (+{quality_improvement:.2f}%)")
        
        print(f"\nPRODUCTION IMPACT:")
        print("-" * 40)
        print(f"Annual Production: {baseline_production:,.0f} → {improved_production:,.0f} units")
        print(f"Production Increase: {production_increase:,.0f} units ({production_increase/baseline_production*100:.1f}%)")
        print(f"Revenue Increase: ${revenue_increase:,.0f}")
        
        # ROI calculation
        total_investment = 0
        for category in recommendations.values():
            for action in category:
                investment_str = action['Investment'].replace('$', '').replace(',', '')
                total_investment += float(investment_str)
        
        roi = (revenue_increase / total_investment) * 100
        
        print(f"\nFINANCIAL ANALYSIS:")
        print("-" * 40)
        print(f"Total Investment: ${total_investment:,.0f}")
        print(f"Annual Revenue Increase: ${revenue_increase:,.0f}")
        print(f"ROI: {roi:.1f}%")
        print(f"Payback Period: {total_investment/revenue_increase:.2f} years")
        
        return improved_data, {
            'oee_improvement': oee_improvement,
            'production_increase': production_increase,
            'revenue_increase': revenue_increase,
            'roi': roi,
            'payback_period': total_investment/revenue_increase
        }
    
    def create_before_after_visualization(self, baseline_data, improved_data):
        """
        Create before/after comparison visualizations
        """
        # Add YearMonth column if not exists
        if 'YearMonth' not in baseline_data.columns:
            baseline_data['YearMonth'] = pd.to_datetime(baseline_data['Date']).dt.to_period('M')
        if 'YearMonth' not in improved_data.columns:
            improved_data['YearMonth'] = pd.to_datetime(improved_data['Date']).dt.to_period('M')
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # OEE Comparison
        ax1 = axes[0, 0]
        baseline_oee = baseline_data['OEE'].mean()
        improved_oee = improved_data['OEE'].mean()
        bars = ax1.bar(['Before', 'After'], [baseline_oee, improved_oee], 
                      color=['#FF6B6B', '#4ECDC4'])
        ax1.set_title('OEE Improvement', fontweight='bold', fontsize=14)
        ax1.set_ylabel('OEE (%)')
        ax1.set_ylim(0, 100)
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Component Comparison
        ax2 = axes[0, 1]
        components = ['Availability', 'Performance', 'Quality']
        baseline_values = [baseline_data[comp].mean() for comp in components]
        improved_values = [improved_data[comp].mean() for comp in components]
        
        x = np.arange(len(components))
        width = 0.35
        ax2.bar(x - width/2, baseline_values, width, label='Before', color='#FF6B6B')
        ax2.bar(x + width/2, improved_values, width, label='After', color='#4ECDC4')
        ax2.set_title('OEE Components Comparison', fontweight='bold', fontsize=14)
        ax2.set_ylabel('Percentage (%)')
        ax2.set_xticks(x)
        ax2.set_xticklabels(components)
        ax2.legend()
        ax2.set_ylim(0, 100)
        
        # Machine-wise Improvement
        ax3 = axes[0, 2]
        machine_baseline = baseline_data.groupby('Machine_Name')['OEE'].mean()
        machine_improved = improved_data.groupby('Machine_Name')['OEE'].mean()
        
        x = np.arange(len(machine_baseline.index))
        width = 0.35
        ax3.bar(x - width/2, machine_baseline.values, width, label='Before', color='#FF6B6B')
        ax3.bar(x + width/2, machine_improved.values, width, label='After', color='#4ECDC4')
        ax3.set_title('Machine-wise OEE Improvement', fontweight='bold', fontsize=14)
        ax3.set_ylabel('OEE (%)')
        ax3.set_xticks(x)
        ax3.set_xticklabels(machine_baseline.index, rotation=45)
        ax3.legend()
        ax3.set_ylim(0, 100)
        
        # Production Volume Comparison
        ax4 = axes[1, 0]
        baseline_monthly = baseline_data.groupby('YearMonth')['Total_Units_Produced'].sum()
        improved_monthly = improved_data.groupby('YearMonth')['Total_Units_Produced'].sum()
        
        months = range(min(len(baseline_monthly), len(improved_monthly)))
        ax4.plot(months, baseline_monthly.iloc[:len(months)], 'o-', label='Before', color='#FF6B6B', linewidth=2)
        ax4.plot(months, improved_monthly.iloc[:len(months)], 's-', label='After', color='#4ECDC4', linewidth=2)
        ax4.set_title('Monthly Production Volume', fontweight='bold', fontsize=14)
        ax4.set_ylabel('Units Produced')
        ax4.set_xlabel('Month')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Downtime Reduction
        ax5 = axes[1, 1]
        baseline_downtime = baseline_data[baseline_data['Downtime_Minutes'] > 0]['Downtime_Minutes'].sum()
        improved_downtime = improved_data[improved_data['Downtime_Minutes'] > 0]['Downtime_Minutes'].sum()
        
        bars = ax5.bar(['Before', 'After'], [baseline_downtime, improved_downtime], 
                      color=['#FF6B6B', '#4ECDC4'])
        ax5.set_title('Total Downtime Reduction', fontweight='bold', fontsize=14)
        ax5.set_ylabel('Downtime (Minutes)')
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # Quality Improvement
        ax6 = axes[1, 2]
        baseline_defects = baseline_data['Defective_Units'].sum()
        improved_defects = improved_data['Defective_Units'].sum()
        
        bars = ax6.bar(['Before', 'After'], [baseline_defects, improved_defects], 
                      color=['#FF6B6B', '#4ECDC4'])
        ax6.set_title('Defective Units Reduction', fontweight='bold', fontsize=14)
        ax6.set_ylabel('Defective Units')
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('c:/Users/rohil/Downloads/project 1/improvement_impact.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Before/After comparison saved as 'improvement_impact.png'")
        
        return fig

def main():
    """
    Main execution for improvement recommendations
    """
    # Initialize analyzers
    analyzer = OEEAnalyzer()
    production_data = analyzer.generate_production_data(4000)
    oee_data = analyzer.calculate_oee_metrics(production_data)
    
    detailed_analyzer = DetailedOEEAnalysis(analyzer)
    
    # Generate improvement recommendations
    improvement_plan = OEEImprovementPlan(analyzer, detailed_analyzer)
    recommendations = improvement_plan.generate_improvement_recommendations()
    
    # Simulate improvement impact
    improved_data, impact_metrics = improvement_plan.simulate_improvement_impact(recommendations)
    
    # Create visualizations
    fig = improvement_plan.create_before_after_visualization(oee_data, improved_data)
    
    print("\n" + "="*60)
    print("IMPROVEMENT ANALYSIS COMPLETE")
    print("="*60)
    
    return improvement_plan, recommendations, improved_data, impact_metrics

if __name__ == "__main__":
    improvement_plan, recommendations, improved_data, impact_metrics = main()
