/**
 * Advanced File Upload Component with TypeScript
 * Handles drag-and-drop, file validation, preview, and progress tracking
 */

interface FileUploadConfig {
  allowedTypes: string[];
  maxSize: number;
  multiple?: boolean;
  previewEnabled?: boolean;
}

interface FileValidationResult {
  isValid: boolean;
  error?: string;
}

interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

class FileUploadManager {
  private config: FileUploadConfig;
  private uploadArea: HTMLElement;
  private fileInput: HTMLInputElement;
  private previewContainer: HTMLElement;
  private errorContainer: HTMLElement;
  private progressBar?: HTMLElement;
  private onFileSelect?: (files: FileList) => void;
  private onFileRemove?: (file: File) => void;
  private onValidationError?: (error: string) => void;

  constructor(
    uploadAreaId: string,
    fileInputId: string,
    config: FileUploadConfig
  ) {
    this.config = {
      multiple: false,
      previewEnabled: true,
      ...config
    };

    this.uploadArea = document.getElementById(uploadAreaId)!;
    this.fileInput = document.getElementById(fileInputId) as HTMLInputElement;
    this.previewContainer = document.getElementById('filePreview')!;
    this.errorContainer = document.getElementById('imageError')!;
    this.progressBar = document.getElementById('uploadProgress');

    this.init();
  }

  private init(): void {
    this.setupEventListeners();
    this.setupDragAndDrop();
    this.updateFileInputAttributes();
  }

  private updateFileInputAttributes(): void {
    this.fileInput.accept = this.config.allowedTypes.join(',');
    this.fileInput.multiple = this.config.multiple || false;
  }

  private setupEventListeners(): void {
    // Click to upload
    this.uploadArea.addEventListener('click', () => {
      this.fileInput.click();
    });

    // File input change
    this.fileInput.addEventListener('change', (e) => {
      const target = e.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        this.handleFileSelection(target.files);
      }
    });

    // Remove file buttons
    document.addEventListener('click', (e) => {
      const target = e.target as HTMLElement;
      if (target.classList.contains('remove-file-btn')) {
        const fileIndex = parseInt(target.dataset.fileIndex || '0');
        this.removeFile(fileIndex);
      }
    });
  }

  private setupDragAndDrop(): void {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      this.uploadArea.addEventListener(eventName, this.preventDefaults, false);
      document.body.addEventListener(eventName, this.preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
      this.uploadArea.addEventListener(eventName, () => {
        this.uploadArea.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      this.uploadArea.addEventListener(eventName, () => {
        this.uploadArea.classList.remove('dragover');
      }, false);
    });

    // Handle dropped files
    this.uploadArea.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt?.files;
      
      if (files && files.length > 0) {
        this.handleFileSelection(files);
      }
    }, false);
  }

  private preventDefaults(e: Event): void {
    e.preventDefault();
    e.stopPropagation();
  }

  private handleFileSelection(files: FileList): void {
    const filesToProcess = this.config.multiple ? 
      Array.from(files) : 
      [files[0]];

    let validFiles: File[] = [];
    
    for (const file of filesToProcess) {
      const validation = this.validateFile(file);
      
      if (validation.isValid) {
        validFiles.push(file);
      } else {
        this.showError(validation.error || 'Invalid file');
        return;
      }
    }

    if (validFiles.length > 0) {
      this.clearError();
      this.updateFileInput(validFiles);
      
      if (this.config.previewEnabled) {
        this.showPreviews(validFiles);
      }
      
      if (this.onFileSelect) {
        const fileList = this.createFileList(validFiles);
        this.onFileSelect(fileList);
      }
    }
  }

  private validateFile(file: File): FileValidationResult {
    // Check file type
    if (!this.config.allowedTypes.includes(file.type)) {
      const allowedExtensions = this.config.allowedTypes
        .map(type => type.split('/')[1].toUpperCase())
        .join(', ');
      
      return {
        isValid: false,
        error: `Please select a valid file type (${allowedExtensions})`
      };
    }

    // Check file size
    if (file.size > this.config.maxSize) {
      const maxSizeMB = (this.config.maxSize / (1024 * 1024)).toFixed(1);
      return {
        isValid: false,
        error: `File size must be less than ${maxSizeMB}MB`
      };
    }

    // Check if file is actually an image (for image uploads)
    if (file.type.startsWith('image/')) {
      return this.validateImageFile(file);
    }

    return { isValid: true };
  }

  private validateImageFile(file: File): FileValidationResult {
    return new Promise<FileValidationResult>((resolve) => {
      const img = new Image();
      const url = URL.createObjectURL(file);
      
      img.onload = () => {
        URL.revokeObjectURL(url);
        
        // Check minimum dimensions if needed
        const minWidth = 100;
        const minHeight = 100;
        
        if (img.width < minWidth || img.height < minHeight) {
          resolve({
            isValid: false,
            error: `Image must be at least ${minWidth}x${minHeight} pixels`
          });
        } else {
          resolve({ isValid: true });
        }
      };
      
      img.onerror = () => {
        URL.revokeObjectURL(url);
        resolve({
          isValid: false,
          error: 'Invalid image file'
        });
      };
      
      img.src = url;
    }) as any; // Type assertion for synchronous usage in this context
  }

  private updateFileInput(files: File[]): void {
    const dt = new DataTransfer();
    files.forEach(file => dt.items.add(file));
    this.fileInput.files = dt.files;
    
    // Trigger change event for form validation
    this.fileInput.dispatchEvent(new Event('change', { bubbles: true }));
  }

  private createFileList(files: File[]): FileList {
    const dt = new DataTransfer();
    files.forEach(file => dt.items.add(file));
    return dt.files;
  }

  private showPreviews(files: File[]): void {
    this.previewContainer.innerHTML = '';
    
    files.forEach((file, index) => {
      if (file.type.startsWith('image/')) {
        this.createImagePreview(file, index);
      } else {
        this.createFilePreview(file, index);
      }
    });
    
    this.previewContainer.classList.remove('d-none');
    this.uploadArea.style.display = 'none';
  }

  private createImagePreview(file: File, index: number): void {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const previewHtml = `
        <div class="file-preview-item" data-file-index="${index}">
          <div class="row align-items-center">
            <div class="col-md-3">
              <img src="${e.target?.result}" 
                   class="img-fluid rounded preview-image" 
                   alt="Preview" 
                   style="max-height: 100px; object-fit: cover;">
            </div>
            <div class="col-md-6">
              <h6 class="mb-1 file-name">${file.name}</h6>
              <small class="text-muted file-size">${this.formatFileSize(file.size)}</small>
              <div class="file-info mt-1">
                <small class="text-muted">
                  ${this.getImageDimensions(e.target?.result as string)}
                </small>
              </div>
            </div>
            <div class="col-md-3 text-end">
              <button type="button" 
                      class="btn btn-outline-danger btn-sm remove-file-btn" 
                      data-file-index="${index}">
                <i class="fas fa-trash me-1" aria-hidden="true"></i>Remove
              </button>
            </div>
          </div>
          <div class="upload-progress-container mt-2 d-none">
            <div class="progress">
              <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
          </div>
        </div>
      `;
      
      this.previewContainer.insertAdjacentHTML('beforeend', previewHtml);
    };
    
    reader.readAsDataURL(file);
  }

  private createFilePreview(file: File, index: number): void {
    const previewHtml = `
      <div class="file-preview-item" data-file-index="${index}">
        <div class="row align-items-center">
          <div class="col-md-3">
            <div class="file-icon text-center">
              <i class="fas fa-file fa-3x text-muted"></i>
            </div>
          </div>
          <div class="col-md-6">
            <h6 class="mb-1 file-name">${file.name}</h6>
            <small class="text-muted file-size">${this.formatFileSize(file.size)}</small>
            <div class="file-info mt-1">
              <small class="text-muted">${file.type}</small>
            </div>
          </div>
          <div class="col-md-3 text-end">
            <button type="button" 
                    class="btn btn-outline-danger btn-sm remove-file-btn" 
                    data-file-index="${index}">
              <i class="fas fa-trash me-1" aria-hidden="true"></i>Remove
            </button>
          </div>
        </div>
      </div>
    `;
    
    this.previewContainer.insertAdjacentHTML('beforeend', previewHtml);
  }

  private getImageDimensions(src: string): string {
    const img = new Image();
    img.src = src;
    return `${img.naturalWidth} × ${img.naturalHeight} pixels`;
  }

  private formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  private removeFile(index: number): void {
    const currentFiles = Array.from(this.fileInput.files || []);
    currentFiles.splice(index, 1);
    
    if (currentFiles.length > 0) {
      this.updateFileInput(currentFiles);
      this.showPreviews(currentFiles);
    } else {
      this.clearFiles();
    }
    
    if (this.onFileRemove && this.fileInput.files) {
      this.onFileRemove(this.fileInput.files[index]);
    }
  }

  private clearFiles(): void {
    this.fileInput.value = '';
    this.previewContainer.classList.add('d-none');
    this.previewContainer.innerHTML = '';
    this.uploadArea.style.display = 'block';
    this.clearError();
  }

  private showError(message: string): void {
    this.errorContainer.textContent = message;
    this.errorContainer.style.display = 'block';
    
    if (this.onValidationError) {
      this.onValidationError(message);
    }
  }

  private clearError(): void {
    this.errorContainer.style.display = 'none';
    this.errorContainer.textContent = '';
  }

  // Public methods
  public setOnFileSelect(callback: (files: FileList) => void): void {
    this.onFileSelect = callback;
  }

  public setOnFileRemove(callback: (file: File) => void): void {
    this.onFileRemove = callback;
  }

  public setOnValidationError(callback: (error: string) => void): void {
    this.onValidationError = callback;
  }

  public getFiles(): FileList | null {
    return this.fileInput.files;
  }

  public clear(): void {
    this.clearFiles();
  }

  public updateProgress(progress: UploadProgress): void {
    if (this.progressBar) {
      this.progressBar.style.width = `${progress.percentage}%`;
      this.progressBar.setAttribute('aria-valuenow', progress.percentage.toString());
    }
    
    // Update progress in preview items
    const progressBars = this.previewContainer.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
      (bar as HTMLElement).style.width = `${progress.percentage}%`;
    });
  }

  public showUploadProgress(): void {
    const progressContainers = this.previewContainer.querySelectorAll('.upload-progress-container');
    progressContainers.forEach(container => {
      container.classList.remove('d-none');
    });
  }

  public hideUploadProgress(): void {
    const progressContainers = this.previewContainer.querySelectorAll('.upload-progress-container');
    progressContainers.forEach(container => {
      container.classList.add('d-none');
    });
  }
}

// Export for use in other modules
export { FileUploadManager, FileUploadConfig, FileValidationResult, UploadProgress };