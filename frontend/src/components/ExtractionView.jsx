import React, { useState, useEffect } from 'react';
import { extractionAPI, correctionsAPI } from '../services/api';

function ExtractionView({ document, onClose }) {
  const [extractions, setExtractions] = useState([]);
  const [editedValues, setEditedValues] = useState({});
  const [processing, setProcessing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (document) {
      loadExtractions();
    }
  }, [document]);

  const loadExtractions = async () => {
    setLoading(true);
    try {
      // Check if document has extractions already
      if (document.extractions && document.extractions.length > 0) {
        setExtractions(document.extractions);
        initializeEditedValues(document.extractions);
      } else {
        setExtractions([]);
      }
    } catch (err) {
      console.error('Failed to load extractions:', err);
    } finally {
      setLoading(false);
    }
  };

  const initializeEditedValues = (extractions) => {
    const values = {};
    extractions.forEach(ext => {
      values[ext.field_name] = ext.extracted_value || '';
    });
    setEditedValues(values);
  };

  const handleProcess = async (engine = 'tesseract') => {
    setProcessing(true);
    try {
      const result = await extractionAPI.process(document.id, engine);
      setExtractions(result);
      initializeEditedValues(result);
    } catch (err) {
      alert('Processing failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setProcessing(false);
    }
  };

  const handleFieldChange = (fieldName, value) => {
    setEditedValues({
      ...editedValues,
      [fieldName]: value
    });
  };

  const handleSaveCorrections = async () => {
    setSaving(true);
    try {
      // Save corrections for each modified field
      const corrections = [];
      for (const extraction of extractions) {
        const originalValue = extraction.extracted_value || '';
        const correctedValue = editedValues[extraction.field_name] || '';
        
        if (originalValue !== correctedValue) {
          await correctionsAPI.save({
            extraction_id: extraction.id,
            original_value: originalValue,
            corrected_value: correctedValue,
            bbox: extraction.bbox // Pass along the bounding box if available
          });
          corrections.push(extraction.field_name);
        }
      }
      
      if (corrections.length > 0) {
        alert(`Saved corrections for: ${corrections.join(', ')}`);
        // Reload to get updated data
        await loadExtractions();
      } else {
        alert('No changes to save');
      }
    } catch (err) {
      alert('Save failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setSaving(false);
    }
  };

  const getFieldLabel = (fieldName) => {
    const labels = {
      'numero_bon': 'Numéro de Bon',
      'date': 'Date',
      'client': 'Client',
      'adresse': 'Adresse',
      'transporteur': 'Transporteur',
      'articles': 'Articles'
    };
    return labels[fieldName] || fieldName;
  };

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="text-center py-8">Loading...</div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold">Document: {document.filename}</h2>
          <p className="text-sm text-gray-600">Status: {document.status}</p>
        </div>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700"
        >
          ✕ Close
        </button>
      </div>

      <div className="p-6">
        {extractions.length === 0 ? (
          <div className="space-y-4">
            <p className="text-gray-600">No extractions yet. Process this document with OCR?</p>
            <div className="flex space-x-2">
              <button
                onClick={() => handleProcess('tesseract')}
                disabled={processing}
                className="px-4 py-2 bg-blue-600 text-white rounded-md
                  hover:bg-blue-700 disabled:bg-gray-400"
              >
                {processing ? 'Processing...' : 'Process with Tesseract'}
              </button>
              <button
                onClick={() => handleProcess('doctr')}
                disabled={processing}
                className="px-4 py-2 bg-green-600 text-white rounded-md
                  hover:bg-green-700 disabled:bg-gray-400"
              >
                {processing ? 'Processing...' : 'Process with Doctr'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div className="text-sm text-gray-600">
                <p>Total fields extracted: {extractions.length}</p>
              </div>
              <button
                onClick={handleSaveCorrections}
                disabled={saving}
                className="px-4 py-2 bg-green-600 text-white rounded-md
                  hover:bg-green-700 disabled:bg-gray-400"
              >
                {saving ? 'Saving...' : 'Save Corrections'}
              </button>
            </div>

            {/* Extracted fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {extractions.map((extraction) => (
                <div key={extraction.id} className="space-y-1">
                  <label className="block text-sm font-medium text-gray-700">
                    {getFieldLabel(extraction.field_name)}
                  </label>
                  {extraction.field_name === 'articles' || extraction.field_name === 'adresse' ? (
                    <textarea
                      value={editedValues[extraction.field_name] || ''}
                      onChange={(e) => handleFieldChange(extraction.field_name, e.target.value)}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md
                        focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder={`Enter ${getFieldLabel(extraction.field_name)}`}
                    />
                  ) : (
                    <input
                      type="text"
                      value={editedValues[extraction.field_name] || ''}
                      onChange={(e) => handleFieldChange(extraction.field_name, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md
                        focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder={`Enter ${getFieldLabel(extraction.field_name)}`}
                    />
                  )}
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Confidence: {extraction.confidence ? (extraction.confidence * 100).toFixed(0) : 0}%</span>
                    {extraction.bbox && <span>Has bbox</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ExtractionView;
