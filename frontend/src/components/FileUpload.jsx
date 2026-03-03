import { useState, useRef } from 'react';

const FileUpload = ({ onFileSelect, selectedFile, onTranscribe, disabled }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (file) => {
    const allowedExtensions = ['.wav', '.mp3', '.flac', '.m4a', '.ogg'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExtension)) {
      throw new Error(`Invalid file format. Allowed formats: ${allowedExtensions.join(', ')}`);
    }
    
    const maxSize = 25 * 1024 * 1024; // 25MB
    if (file.size > maxSize) {
      throw new Error('File is too large. Maximum size is 25MB.');
    }
    
    return true;
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        validateFile(file);
        onFileSelect(file);
      } catch (error) {
        alert(error.message);
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const file = e.dataTransfer.files[0];
    if (file) {
      try {
        validateFile(file);
        onFileSelect(file);
      } catch (error) {
        alert(error.message);
      }
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  const handleChangeFile = () => {
    onFileSelect(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleDropAreaClick = (e) => {
    // Only trigger file input if clicking the drop area itself, not child buttons
    if (!selectedFile && e.target === e.currentTarget) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div>
      <div
        onClick={handleDropAreaClick}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`file-drop-area border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all duration-200 ${
          isDragging
            ? 'border-blue-500 bg-blue-50 dark:bg-slate-800/50'
            : selectedFile
            ? 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-slate-800/30'
            : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 hover:bg-gray-50 dark:hover:bg-slate-800/30'
        }`}
      >
        {!selectedFile ? (
          <div className="space-y-3">
            <div className="text-4xl">📁</div>
            <div>
              <p className="text-base font-semibold text-gray-700 dark:text-gray-200 mb-1">
                Drop audio file here
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">or</p>
            </div>
            <button 
              type="button" 
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
              className="btn-primary inline-flex items-center space-x-2 text-sm"
            >
              <span>Browse Files</span>
            </button>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
              Supported: WAV, MP3, FLAC, M4A, OGG (Max: 25MB)
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="text-4xl">🎵</div>
            <div className="space-y-1">
              <p className="text-sm font-semibold text-gray-700 dark:text-gray-200">{selectedFile.name}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {formatFileSize(selectedFile.size)}
              </p>
            </div>
            <div className="flex gap-2 justify-center pt-2">
              <button 
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleChangeFile();
                }}
                className="btn-secondary inline-flex items-center space-x-1 text-sm"
              >
                <span>Change</span>
              </button>
              <button 
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  onTranscribe();
                }}
                disabled={disabled}
                className="btn-success inline-flex items-center space-x-1 text-sm"
              >
                <span>Transcribe</span>
              </button>
            </div>
          </div>
        )}
      </div>
      <input 
        type="file" 
        ref={fileInputRef}
        accept=".wav,.mp3,.flac,.m4a,.ogg" 
        onChange={handleFileChange}
        className="hidden"
      />
    </div>
  );
};

export default FileUpload;
