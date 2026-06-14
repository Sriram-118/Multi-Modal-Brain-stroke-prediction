/**
 * PredictionChart Component with TypeScript
 * Handles interactive chart visualization for stroke prediction results
 */

interface ChartData {
  labels: string[];
  datasets: ChartDataset[];
}

interface ChartDataset {
  label: string;
  data: number[];
  backgroundColor?: string | string[];
  borderColor?: string | string[];
  borderWidth?: number;
  fill?: boolean;
}

interface PredictionResult {
  cnnPrediction: number;
  lstmPrediction: number;
  fusedPrediction: number;
  confidence: number;
  riskFactors: RiskFactor[];
}

interface RiskFactor {
  name: string;
  value: number;
  impact: 'low' | 'medium' | 'high';
  description: string;
}

interface ChartConfig {
  type: 'bar' | 'line' | 'doughnut' | 'radar' | 'pie';
  responsive: boolean;
  maintainAspectRatio: boolean;
  plugins?: any;
  scales?: any;
}

class PredictionChart {
  private chartContainer: HTMLElement;
  private chart: any; // Chart.js instance
  private predictionData: PredictionResult;
  private chartConfig: ChartConfig;

  constructor(containerId: string, predictionData: PredictionResult) {
    this.chartContainer = document.getElementById(containerId)!;
    this.predictionData = predictionData;
    this.chartConfig = this.getDefaultConfig();
    
    this.init();
  }

  private init(): void {
    this.createChartCanvas();
    this.renderPredictionChart();
    this.setupInteractivity();
  }

  private createChartCanvas(): void {
    // Clear existing content
    this.chartContainer.innerHTML = '';
    
    // Create canvas element
    const canvas = document.createElement('canvas');
    canvas.id = 'predictionChart';
    canvas.width = 800;
    canvas.height = 400;
    
    this.chartContainer.appendChild(canvas);
  }

  private getDefaultConfig(): ChartConfig {
    return {
      type: 'bar',
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Multi-Modal Stroke Prediction Results',
          font: {
            size: 18,
            weight: 'bold'
          },
          color: '#2c5aa0'
        },
        legend: {
          display: true,
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#2c5aa0',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: (context: any) => {
              const value = context.parsed.y;
              const percentage = (value * 100).toFixed(1);
              return `${context.dataset.label}: ${percentage}%`;
            },
            afterLabel: (context: any) => {
              if (context.datasetIndex === 2) { // Fused prediction
                return `Confidence: ${(this.predictionData.confidence * 100).toFixed(1)}%`;
              }
              return '';
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 1,
          ticks: {
            callback: function(value: any) {
              return (value * 100).toFixed(0) + '%';
            },
            font: {
              size: 11
            }
          },
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          title: {
            display: true,
            text: 'Stroke Risk Probability',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: 12
            }
          },
          grid: {
            display: false
          }
        }
      }
    };
  }

  private renderPredictionChart(): void {
    const ctx = document.getElementById('predictionChart') as HTMLCanvasElement;
    
    const chartData: ChartData = {
      labels: ['CNN Model', 'LSTM Model', 'Fused Prediction'],
      datasets: [{
        label: 'Stroke Risk Probability',
        data: [
          this.predictionData.cnnPrediction,
          this.predictionData.lstmPrediction,
          this.predictionData.fusedPrediction
        ],
        backgroundColor: [
          'rgba(54, 162, 235, 0.8)',   // CNN - Blue
          'rgba(75, 192, 192, 0.8)',   // LSTM - Teal
          'rgba(255, 99, 132, 0.8)'    // Fused - Red
        ],
        borderColor: [
          'rgba(54, 162, 235, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)'
        ],
        borderWidth: 2
      }]
    };

    // Initialize Chart.js
    this.chart = new (window as any).Chart(ctx, {
      type: this.chartConfig.type,
      data: chartData,
      options: this.chartConfig
    });
  }

  private setupInteractivity(): void {
    // Add click handlers for chart interaction
    this.chart.options.onClick = (event: any, elements: any[]) => {
      if (elements.length > 0) {
        const elementIndex = elements[0].index;
        this.showDetailedAnalysis(elementIndex);
      }
    };

    // Add hover effects
    this.chart.options.onHover = (event: any, elements: any[]) => {
      event.native.target.style.cursor = elements.length > 0 ? 'pointer' : 'default';
    };
  }

  private showDetailedAnalysis(modelIndex: number): void {
    const modelNames = ['CNN Model', 'LSTM Model', 'Fused Prediction'];
    const modelName = modelNames[modelIndex];
    
    let analysisContent = '';
    
    switch (modelIndex) {
      case 0: // CNN Model
        analysisContent = `
          <h5>CNN Model Analysis</h5>
          <p>The Convolutional Neural Network analyzed the brain scan image and detected:</p>
          <ul>
            <li>Image-based risk indicators</li>
            <li>Structural abnormalities</li>
            <li>Pattern recognition results</li>
          </ul>
          <p><strong>Prediction:</strong> ${(this.predictionData.cnnPrediction * 100).toFixed(1)}% stroke risk</p>
        `;
        break;
      case 1: // LSTM Model
        analysisContent = `
          <h5>LSTM Model Analysis</h5>
          <p>The Long Short-Term Memory network analyzed clinical parameters:</p>
          <ul>
            <li>Age and demographic factors</li>
            <li>Medical history patterns</li>
            <li>Clinical parameter correlations</li>
          </ul>
          <p><strong>Prediction:</strong> ${(this.predictionData.lstmPrediction * 100).toFixed(1)}% stroke risk</p>
        `;
        break;
      case 2: // Fused Prediction
        analysisContent = `
          <h5>Multi-Modal Fusion Analysis</h5>
          <p>Combined analysis of both image and clinical data:</p>
          <ul>
            <li>Weighted combination of CNN and LSTM predictions</li>
            <li>Cross-modal validation</li>
            <li>Enhanced accuracy through fusion</li>
          </ul>
          <p><strong>Final Prediction:</strong> ${(this.predictionData.fusedPrediction * 100).toFixed(1)}% stroke risk</p>
          <p><strong>Confidence Level:</strong> ${(this.predictionData.confidence * 100).toFixed(1)}%</p>
        `;
        break;
    }
    
    this.showModal('Detailed Analysis - ' + modelName, analysisContent);
  }

  private showModal(title: string, content: string): void {
    // Create modal if it doesn't exist
    let modal = document.getElementById('chartAnalysisModal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'chartAnalysisModal';
      modal.className = 'modal fade';
      modal.innerHTML = `
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="modalTitle"></h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body" id="modalBody"></div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
    
    // Update modal content
    document.getElementById('modalTitle')!.textContent = title;
    document.getElementById('modalBody')!.innerHTML = content;
    
    // Show modal using Bootstrap
    const bootstrapModal = new (window as any).bootstrap.Modal(modal);
    bootstrapModal.show();
  }

  public renderRiskFactorsChart(): void {
    // Create a separate chart for risk factors
    const riskContainer = document.createElement('div');
    riskContainer.className = 'risk-factors-chart mt-4';
    riskContainer.innerHTML = '<canvas id="riskFactorsChart" width="800" height="300"></canvas>';
    this.chartContainer.appendChild(riskContainer);

    const ctx = document.getElementById('riskFactorsChart') as HTMLCanvasElement;
    
    const riskData: ChartData = {
      labels: this.predictionData.riskFactors.map(rf => rf.name),
      datasets: [{
        label: 'Risk Impact',
        data: this.predictionData.riskFactors.map(rf => rf.value),
        backgroundColor: this.predictionData.riskFactors.map(rf => {
          switch (rf.impact) {
            case 'high': return 'rgba(255, 99, 132, 0.8)';
            case 'medium': return 'rgba(255, 206, 86, 0.8)';
            case 'low': return 'rgba(75, 192, 192, 0.8)';
            default: return 'rgba(201, 203, 207, 0.8)';
          }
        }),
        borderColor: this.predictionData.riskFactors.map(rf => {
          switch (rf.impact) {
            case 'high': return 'rgba(255, 99, 132, 1)';
            case 'medium': return 'rgba(255, 206, 86, 1)';
            case 'low': return 'rgba(75, 192, 192, 1)';
            default: return 'rgba(201, 203, 207, 1)';
          }
        }),
        borderWidth: 2
      }]
    };

    new (window as any).Chart(ctx, {
      type: 'bar',
      data: riskData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Individual Risk Factors Analysis',
            font: {
              size: 16,
              weight: 'bold'
            }
          },
          tooltip: {
            callbacks: {
              afterLabel: (context: any) => {
                const riskFactor = this.predictionData.riskFactors[context.dataIndex];
                return riskFactor.description;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Risk Score'
            }
          }
        }
      }
    });
  }

  public renderComparisonChart(): void {
    // Create a radar chart for comprehensive comparison
    const comparisonContainer = document.createElement('div');
    comparisonContainer.className = 'comparison-chart mt-4';
    comparisonContainer.innerHTML = '<canvas id="comparisonChart" width="600" height="400"></canvas>';
    this.chartContainer.appendChild(comparisonContainer);

    const ctx = document.getElementById('comparisonChart') as HTMLCanvasElement;
    
    const comparisonData: ChartData = {
      labels: ['Accuracy', 'Confidence', 'Clinical Relevance', 'Image Quality', 'Data Completeness'],
      datasets: [
        {
          label: 'CNN Model',
          data: [0.85, 0.78, 0.65, 0.92, 0.88],
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 2,
          fill: true
        },
        {
          label: 'LSTM Model',
          data: [0.82, 0.85, 0.95, 0.45, 0.90],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 2,
          fill: true
        },
        {
          label: 'Fused Model',
          data: [0.93, 0.88, 0.85, 0.78, 0.92],
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 2,
          fill: true
        }
      ]
    };

    new (window as any).Chart(ctx, {
      type: 'radar',
      data: comparisonData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Model Performance Comparison',
            font: {
              size: 16,
              weight: 'bold'
            }
          }
        },
        scales: {
          r: {
            beginAtZero: true,
            max: 1,
            ticks: {
              callback: function(value: any) {
                return (value * 100).toFixed(0) + '%';
              }
            }
          }
        }
      }
    });
  }

  public updateChart(newData: PredictionResult): void {
    this.predictionData = newData;
    
    // Update main chart data
    this.chart.data.datasets[0].data = [
      newData.cnnPrediction,
      newData.lstmPrediction,
      newData.fusedPrediction
    ];
    
    this.chart.update();
  }

  public exportChart(format: 'png' | 'pdf' = 'png'): void {
    if (format === 'png') {
      const url = this.chart.toBase64Image();
      const link = document.createElement('a');
      link.download = 'stroke-prediction-chart.png';
      link.href = url;
      link.click();
    } else if (format === 'pdf') {
      // Integration with jsPDF for PDF export
      const canvas = this.chart.canvas;
      const imgData = canvas.toDataURL('image/png');
      
      const { jsPDF } = (window as any).jspdf;
      const pdf = new jsPDF();
      
      pdf.addImage(imgData, 'PNG', 10, 10, 190, 100);
      pdf.save('stroke-prediction-results.pdf');
    }
  }

  public destroy(): void {
    if (this.chart) {
      this.chart.destroy();
    }
  }
}

// Export for use in other modules
export { PredictionChart, PredictionResult, RiskFactor, ChartData, ChartDataset };