"""
Enhanced Chart Generation Utilities for Stroke Prediction
Replaces matplotlib with modern, interactive-style charts using Python libraries
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import base64
from typing import Dict, List, Tuple, Optional

# Set modern style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

class ModernChartGenerator:
    """
    Modern chart generator for stroke prediction results
    Creates publication-quality charts with medical styling
    """
    
    def __init__(self):
        self.medical_colors = {
            'cnn': '#36A2EB',      # Blue
            'lstm': '#4BC0C0',     # Teal  
            'fused': '#FF6384',    # Red
            'success': '#4CAF50',  # Green
            'warning': '#FF9800',  # Orange
            'danger': '#F44336',   # Red
            'primary': '#2C5AA0'   # Medical Blue
        }
        
        # Configure matplotlib for better rendering
        plt.rcParams.update({
            'font.size': 12,
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Liberation Sans'],
            'axes.titlesize': 16,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 11,
            'figure.titlesize': 18,
            'axes.grid': True,
            'grid.alpha': 0.3,
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.spines.left': True,
            'axes.spines.bottom': True,
        })
    
    def create_prediction_comparison_chart(self, 
                                         cnn_pred: float, 
                                         lstm_pred: float, 
                                         fused_pred: float,
                                         confidence: float = 0.9) -> str:
        """
        Create a modern comparison chart for model predictions
        
        Args:
            cnn_pred: CNN model prediction (0-1)
            lstm_pred: LSTM model prediction (0-1) 
            fused_pred: Fused model prediction (0-1)
            confidence: Confidence level (0-1)
            
        Returns:
            Base64 encoded PNG image
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Multi-Modal Stroke Prediction Analysis', 
                    fontsize=18, fontweight='bold', color=self.medical_colors['primary'])
        
        # Main prediction comparison (left subplot)
        models = ['CNN\nModel', 'LSTM\nModel', 'Fused\nPrediction']
        predictions = [cnn_pred, lstm_pred, fused_pred]
        colors = [self.medical_colors['cnn'], self.medical_colors['lstm'], self.medical_colors['fused']]
        
        bars = ax1.bar(models, predictions, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        
        # Add value labels on bars
        for bar, pred in zip(bars, predictions):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{pred*100:.1f}%', ha='center', va='bottom', 
                    fontweight='bold', fontsize=11)
        
        ax1.set_ylabel('Stroke Risk Probability', fontweight='bold')
        ax1.set_title('Model Predictions Comparison', fontweight='bold', pad=20)
        ax1.set_ylim(0, 1)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
        
        # Add confidence indicator
        ax1.text(0.02, 0.98, f'Confidence: {confidence*100:.1f}%', 
                transform=ax1.transAxes, fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=self.medical_colors['primary'], 
                         alpha=0.8, edgecolor='none'), color='white', va='top')
        
        # Risk level indicator (right subplot)
        risk_level = self.get_risk_level(fused_pred)
        risk_color = self.get_risk_color(fused_pred)
        
        # Create a gauge-style chart
        theta = np.linspace(0, np.pi, 100)
        r = 1
        
        # Background arc
        ax2.plot(r * np.cos(theta), r * np.sin(theta), 'lightgray', linewidth=8, alpha=0.3)
        
        # Risk level arcs
        low_theta = np.linspace(0, np.pi/3, 50)
        med_theta = np.linspace(np.pi/3, 2*np.pi/3, 50)
        high_theta = np.linspace(2*np.pi/3, np.pi, 50)
        
        ax2.plot(r * np.cos(low_theta), r * np.sin(low_theta), self.medical_colors['success'], linewidth=8, alpha=0.7)
        ax2.plot(r * np.cos(med_theta), r * np.sin(med_theta), self.medical_colors['warning'], linewidth=8, alpha=0.7)
        ax2.plot(r * np.cos(high_theta), r * np.sin(high_theta), self.medical_colors['danger'], linewidth=8, alpha=0.7)
        
        # Needle pointing to current risk
        needle_angle = np.pi * (1 - fused_pred)
        needle_x = 0.8 * np.cos(needle_angle)
        needle_y = 0.8 * np.sin(needle_angle)
        
        ax2.arrow(0, 0, needle_x, needle_y, head_width=0.05, head_length=0.05, 
                 fc=risk_color, ec=risk_color, linewidth=3)
        
        # Center circle
        circle = plt.Circle((0, 0), 0.1, color=risk_color, alpha=0.8)
        ax2.add_patch(circle)
        
        # Risk percentage in center
        ax2.text(0, -0.3, f'{fused_pred*100:.1f}%', ha='center', va='center', 
                fontsize=20, fontweight='bold', color=risk_color)
        ax2.text(0, -0.45, risk_level, ha='center', va='center', 
                fontsize=12, fontweight='bold', color=risk_color)
        
        # Labels
        ax2.text(-0.9, 0.1, 'Low\nRisk', ha='center', va='center', fontsize=9, color=self.medical_colors['success'])
        ax2.text(0, 1.1, 'Moderate\nRisk', ha='center', va='center', fontsize=9, color=self.medical_colors['warning'])
        ax2.text(0.9, 0.1, 'High\nRisk', ha='center', va='center', fontsize=9, color=self.medical_colors['danger'])
        
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-0.6, 1.2)
        ax2.set_aspect('equal')
        ax2.axis('off')
        ax2.set_title('Risk Assessment Gauge', fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_risk_factors_chart(self, risk_factors: Dict[str, Dict]) -> str:
        """
        Create a horizontal bar chart for risk factors analysis
        
        Args:
            risk_factors: Dict with factor names as keys and dict with 'value' and 'impact' as values
            
        Returns:
            Base64 encoded PNG image
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        factors = list(risk_factors.keys())
        values = [risk_factors[f]['value'] for f in factors]
        impacts = [risk_factors[f]['impact'] for f in factors]
        
        # Color mapping for impact levels
        impact_colors = {
            'low': self.medical_colors['success'],
            'medium': self.medical_colors['warning'], 
            'high': self.medical_colors['danger']
        }
        
        colors = [impact_colors.get(impact, self.medical_colors['primary']) for impact in impacts]
        
        # Create horizontal bar chart
        bars = ax.barh(factors, values, color=colors, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Add value labels
        for i, (bar, value, impact) in enumerate(zip(bars, values, impacts)):
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                   f'{value:.2f} ({impact})', ha='left', va='center', fontweight='bold')
        
        ax.set_xlabel('Risk Score', fontweight='bold')
        ax.set_title('Individual Risk Factors Analysis', fontweight='bold', fontsize=16, pad=20)
        ax.set_xlim(0, max(values) * 1.2)
        
        # Add legend
        legend_elements = [plt.Rectangle((0,0),1,1, facecolor=impact_colors[impact], alpha=0.8, label=impact.title()) 
                          for impact in ['low', 'medium', 'high']]
        ax.legend(handles=legend_elements, loc='lower right', title='Impact Level', title_fontsize=12)
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_model_performance_radar(self, performance_metrics: Dict[str, Dict[str, float]]) -> str:
        """
        Create a radar chart comparing model performance across multiple metrics
        
        Args:
            performance_metrics: Dict with model names as keys and metrics dict as values
            
        Returns:
            Base64 encoded PNG image
        """
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Metrics and models
        metrics = list(next(iter(performance_metrics.values())).keys())
        models = list(performance_metrics.keys())
        
        # Number of metrics
        N = len(metrics)
        
        # Angles for each metric
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Complete the circle
        
        # Colors for each model
        model_colors = [self.medical_colors['cnn'], self.medical_colors['lstm'], self.medical_colors['fused']]
        
        # Plot each model
        for i, (model, color) in enumerate(zip(models, model_colors)):
            values = [performance_metrics[model][metric] for metric in metrics]
            values += values[:1]  # Complete the circle
            
            ax.plot(angles, values, 'o-', linewidth=2, label=model, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        # Add metric labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, fontsize=11)
        
        # Set y-axis limits and labels
        ax.set_ylim(0, 1)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9)
        ax.grid(True)
        
        # Add title and legend
        ax.set_title('Model Performance Comparison\n(Radar Chart)', 
                    fontweight='bold', fontsize=16, pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def get_risk_level(self, prediction: float) -> str:
        """Get risk level text based on prediction value"""
        if prediction < 0.3:
            return "Low Risk"
        elif prediction < 0.7:
            return "Moderate Risk"
        else:
            return "High Risk"
    
    def get_risk_color(self, prediction: float) -> str:
        """Get risk color based on prediction value"""
        if prediction < 0.3:
            return self.medical_colors['success']
        elif prediction < 0.7:
            return self.medical_colors['warning']
        else:
            return self.medical_colors['danger']
    
    def create_comprehensive_report_chart(self, 
                                        cnn_pred: float,
                                        lstm_pred: float, 
                                        fused_pred: float,
                                        confidence: float,
                                        risk_factors: Dict[str, Dict],
                                        patient_data: Dict[str, any]) -> str:
        """
        Create a comprehensive multi-panel chart for complete analysis
        
        Returns:
            Base64 encoded PNG image
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Main prediction comparison (top left)
        ax1 = fig.add_subplot(gs[0, :2])
        models = ['CNN Model', 'LSTM Model', 'Fused Prediction']
        predictions = [cnn_pred, lstm_pred, fused_pred]
        colors = [self.medical_colors['cnn'], self.medical_colors['lstm'], self.medical_colors['fused']]
        
        bars = ax1.bar(models, predictions, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        for bar, pred in zip(bars, predictions):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{pred*100:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        ax1.set_ylabel('Stroke Risk Probability')
        ax1.set_title('Model Predictions', fontweight='bold')
        ax1.set_ylim(0, 1)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))
        
        # Risk gauge (top right)
        ax2 = fig.add_subplot(gs[0, 2])
        risk_level = self.get_risk_level(fused_pred)
        risk_color = self.get_risk_color(fused_pred)
        
        # Simple pie chart for risk visualization
        sizes = [fused_pred, 1-fused_pred]
        colors_pie = [risk_color, 'lightgray']
        ax2.pie(sizes, colors=colors_pie, startangle=90, counterclock=False)
        ax2.add_patch(plt.Circle((0,0), 0.5, color='white'))
        ax2.text(0, 0, f'{fused_pred*100:.1f}%\n{risk_level}', ha='center', va='center',
                fontweight='bold', fontsize=10)
        ax2.set_title('Risk Level', fontweight='bold')
        
        # Risk factors (middle row)
        ax3 = fig.add_subplot(gs[1, :])
        factors = list(risk_factors.keys())
        values = [risk_factors[f]['value'] for f in factors]
        impacts = [risk_factors[f]['impact'] for f in factors]
        
        impact_colors = {
            'low': self.medical_colors['success'],
            'medium': self.medical_colors['warning'],
            'high': self.medical_colors['danger']
        }
        colors_rf = [impact_colors.get(impact, self.medical_colors['primary']) for impact in impacts]
        
        bars_rf = ax3.barh(factors, values, color=colors_rf, alpha=0.8)
        for bar, value in zip(bars_rf, values):
            width = bar.get_width()
            ax3.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                    f'{value:.2f}', ha='left', va='center', fontweight='bold')
        
        ax3.set_xlabel('Risk Score')
        ax3.set_title('Risk Factors Analysis', fontweight='bold')
        
        # Patient summary (bottom)
        ax4 = fig.add_subplot(gs[2, :])
        ax4.axis('off')
        
        # Create patient summary text
        summary_text = f"""
        Patient Summary:
        Age: {patient_data.get('age', 'N/A')} years  |  Gender: {patient_data.get('gender', 'N/A')}  |  BMI: {patient_data.get('bmi', 'N/A')} kg/m²
        Hypertension: {'Yes' if patient_data.get('hypertension') == '1' else 'No'}  |  Glucose: {patient_data.get('glucose', 'N/A')} mg/dL
        Smoking Status: {patient_data.get('smoking', 'N/A')}
        
        Analysis Confidence: {confidence*100:.1f}%
        Recommendation: {self.get_recommendation(fused_pred)}
        """
        
        ax4.text(0.05, 0.8, summary_text, transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", 
                facecolor='lightblue', alpha=0.3))
        
        fig.suptitle('Multi-Modal Stroke Prediction - Comprehensive Analysis Report', 
                    fontsize=18, fontweight='bold', y=0.95)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def get_recommendation(self, prediction: float) -> str:
        """Get medical recommendation based on prediction"""
        if prediction < 0.3:
            return "Continue regular health monitoring and maintain healthy lifestyle."
        elif prediction < 0.7:
            return "Consult healthcare provider for risk assessment and preventive measures."
        else:
            return "Seek immediate medical consultation for comprehensive evaluation."


# Example usage function for Django views
def generate_prediction_charts(cnn_pred: float, lstm_pred: float, fused_pred: float, 
                             confidence: float, patient_data: Dict) -> Dict[str, str]:
    """
    Generate all charts for stroke prediction results
    
    Returns:
        Dictionary with chart names as keys and base64 images as values
    """
    generator = ModernChartGenerator()
    
    # Sample risk factors (would come from actual analysis)
    risk_factors = {
        'Age': {'value': 0.7, 'impact': 'medium'},
        'Hypertension': {'value': 0.8, 'impact': 'high'},
        'Glucose Level': {'value': 0.6, 'impact': 'medium'},
        'BMI': {'value': 0.4, 'impact': 'low'},
        'Smoking': {'value': 0.9, 'impact': 'high'}
    }
    
    # Sample performance metrics
    performance_metrics = {
        'CNN': {'Accuracy': 0.85, 'Precision': 0.87, 'Recall': 0.82, 'F1-Score': 0.84},
        'LSTM': {'Accuracy': 0.82, 'Precision': 0.80, 'Recall': 0.84, 'F1-Score': 0.82},
        'Fused': {'Accuracy': 0.93, 'Precision': 0.92, 'Recall': 0.90, 'F1-Score': 0.91}
    }
    
    charts = {
        'main': generator.create_prediction_comparison_chart(cnn_pred, lstm_pred, fused_pred, confidence),
        'risk_factors': generator.create_risk_factors_chart(risk_factors),
        'performance': generator.create_model_performance_radar(performance_metrics),
        'comprehensive': generator.create_comprehensive_report_chart(
            cnn_pred, lstm_pred, fused_pred, confidence, risk_factors, patient_data
        )
    }
    
    return charts