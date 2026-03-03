import { useState } from 'react';

const TranscriptionResults = ({ results, showToast }) => {
  const [copied, setCopied] = useState(false);
  const [copiedJSON, setCopiedJSON] = useState(false);
  const [showJSON, setShowJSON] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(results.transcription || '');
      setCopied(true);
      showToast('Transcription copied to clipboard!', 'success');
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      showToast('Failed to copy transcription', 'error');
    }
  };

  const handleCopyJSON = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(results, null, 2));
      setCopiedJSON(true);
      showToast('JSON response copied to clipboard!', 'success');
      setTimeout(() => setCopiedJSON(false), 2000);
    } catch (error) {
      showToast('Failed to copy JSON', 'error');
    }
  };

  const handleCopyDiarization = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(results.diarization, null, 2));
      showToast('Diarization data copied to clipboard!', 'success');
    } catch (error) {
      showToast('Failed to copy diarization data', 'error');
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = (seconds % 60).toFixed(2);
    return `${mins}:${secs.padStart(5, '0')}`;
  };

  const getSpeakerColor = (channel) => {
    const colors = [
      'bg-blue-100 dark:bg-blue-900/30 border-blue-300 dark:border-blue-700 text-blue-800 dark:text-blue-300',
      'bg-green-100 dark:bg-green-900/30 border-green-300 dark:border-green-700 text-green-800 dark:text-green-300',
      'bg-purple-100 dark:bg-purple-900/30 border-purple-300 dark:border-purple-700 text-purple-800 dark:text-purple-300',
      'bg-orange-100 dark:bg-orange-900/30 border-orange-300 dark:border-orange-700 text-orange-800 dark:text-orange-300',
      'bg-pink-100 dark:bg-pink-900/30 border-pink-300 dark:border-pink-700 text-pink-800 dark:text-pink-300',
    ];
    return colors[channel % colors.length];
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
          Transcription Result
        </h2>
        <div className="flex gap-2">
          <button 
            onClick={() => setShowJSON(!showJSON)}
            className="btn-secondary text-xs"
          >
            {showJSON ? 'Hide JSON' : 'Show JSON'}
          </button>
          <button 
            onClick={handleCopy}
            className="btn-primary text-xs"
          >
            {copied ? '✓ Copied' : 'Copy Text'}
          </button>
        </div>
      </div>
      
      {/* Transcription Text */}
      <div className="bg-gray-50 dark:bg-slate-800/30 p-4 rounded-lg mb-4 border border-gray-200 dark:border-gray-700">
        <p className="text-gray-700 dark:text-gray-200 whitespace-pre-wrap leading-relaxed text-sm">
          {results.transcription || 'No transcription available'}
        </p>
      </div>
      
      {/* Metadata */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs mb-4">
        <div className="bg-gray-50 dark:bg-slate-800/30 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-gray-500 dark:text-gray-400 font-medium mb-1">
            Model
          </div>
          <div className="text-gray-700 dark:text-gray-200 font-mono text-xs break-words">{results.model_used}</div>
        </div>
        <div className="bg-gray-50 dark:bg-slate-800/30 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-gray-500 dark:text-gray-400 font-medium mb-1">
            Duration
          </div>
          <div className="text-gray-700 dark:text-gray-200 font-semibold">
            {results.audio_duration ? `${results.audio_duration.toFixed(2)}s` : 'N/A'}
          </div>
        </div>
        <div className="bg-gray-50 dark:bg-slate-800/30 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-gray-500 dark:text-gray-400 font-medium mb-1">
            Processing
          </div>
          <div className="text-gray-700 dark:text-gray-200 font-semibold">{results.processing_time.toFixed(2)}s</div>
        </div>
        <div className="bg-gray-50 dark:bg-slate-800/30 p-3 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="text-gray-500 dark:text-gray-400 font-medium mb-1">
            Diarization
          </div>
          <div className="text-gray-700 dark:text-gray-200 font-semibold">
            {results.diarization_enabled ? '✓ Enabled' : '✗ Disabled'}
          </div>
        </div>
      </div>

      {/* Diarization Results */}
      {results.diarization_enabled && results.diarization && results.diarization.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-gray-800 dark:text-gray-100">
              Speaker Diarization ({results.diarization.length} segments)
            </h3>
            <button 
              onClick={handleCopyDiarization}
              className="btn-secondary text-xs"
            >
              Copy Diarization JSON
            </button>
          </div>
          <div className="bg-gray-50 dark:bg-slate-800/30 p-4 rounded-lg border border-gray-200 dark:border-gray-700 max-h-96 overflow-y-auto">
            <div className="space-y-2">
              {results.diarization.map((segment, index) => (
                <div 
                  key={index}
                  className={`p-3 rounded-lg border ${getSpeakerColor(segment.channel)}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-xs">
                        Speaker {segment.channel}
                      </span>
                      <span className="text-xs opacity-75">
                        {formatTime(segment.offset)} → {formatTime(segment.offset + segment.duration)}
                      </span>
                      <span className="text-xs opacity-60">
                        ({segment.duration.toFixed(2)}s)
                      </span>
                    </div>
                  </div>
                  <p className="text-sm leading-relaxed">
                    {segment.text}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* JSON Response */}
      {showJSON && (
        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-gray-700 dark:text-gray-200">
              Complete JSON Response
            </h3>
            <button 
              onClick={handleCopyJSON}
              className="btn-secondary text-xs"
            >
              {copiedJSON ? '✓ Copied' : 'Copy JSON'}
            </button>
          </div>
          <div className="bg-gray-900 dark:bg-black p-4 rounded-lg border border-gray-700 overflow-x-auto max-h-96 overflow-y-auto">
            <pre className="text-xs text-green-400 font-mono">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranscriptionResults;
