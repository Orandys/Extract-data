import React, { useState, useEffect } from 'react';
import { extractionAPI } from '../services/api';

function ExtractionView({ documentId, onClose }) {
  const [extractions, setExtractions] = useState([]);
  const [selectedExtraction, setSelectedExtraction] = useState(null);
  const [editing, setEditing] = useState(false);
  const [editData, setEditData] = useState({});
  const [processing, setProcessing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadExtractions();
  }, [documentId]);

  const loadExtractions = async () => {
    try {
      const data = await extractionAPI.getByDocument(documentId);
      setExtractions(data);
      if (data.length > 0) {
        setSelectedExtraction(data[0]);
        setEditData(data[0]);
      }
    } catch (err) {
      console.error('Failed to load extractions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProcess = async (engine = 'tesseract') => {
    setProcessing(true);
    try {
      const result = await extractionAPI.process(documentId, engine);
      setExtractions([result, ...extractions]);
      setSelectedExtraction(result);
      setEditData(result);
    } catch (err) {
      alert('Processing failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setProcessing(false);
    }
  };

  const handleSave = async () => {
    try {
      const updated = await extractionAPI.update(selectedExtraction.id, {
        ...editData,
        validated: 1,
      });
      setSelectedExtraction(updated);
      setEditing(false);
      
      // Refresh extractions
      loadExtractions();
    } catch (err) {
      alert('Save failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleFieldChange = (field, value) => {
    setEditData({ ...editData, [field]: value });
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
        <h2 className="text-xl font-semibold">Document Extraction</h2>
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
            <p className="text-gray-600">No extractions yet. Process this document?</p>
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
            {/* Extraction info */}
            <div className="flex justify-between items-center">
              <div className="text-sm text-gray-600">
                <p>Engine: {selectedExtraction.ocr_engine}</p>
                <p>Confidence: {(selectedExtraction.confidence_score * 100).toFixed(1)}%</p>
                <p>
                  Status:{' '}
                  {selectedExtraction.validated ? (
                    <span className="text-green-600 font-medium">Validated</span>
                  ) : (
                    <span className="text-yellow-600 font-medium">Not Validated</span>
                  )}
                </p>
              </div>

              {!editing ? (
                <button
                  onClick={() => setEditing(true)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md
                    hover:bg-blue-700"
                >
                  Edit & Validate
                </button>
              ) : (
                <div className="space-x-2">
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-green-600 text-white rounded-md
                      hover:bg-green-700"
                  >
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setEditing(false);
                      setEditData(selectedExtraction);
                    }}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md
                      hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              )}
            </div>

            {/* Extracted fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { key: 'delivery_note_number', label: 'Delivery Note Number' },
                { key: 'delivery_date', label: 'Delivery Date' },
                { key: 'supplier_name', label: 'Supplier Name' },
                { key: 'customer_name', label: 'Customer Name' },
                { key: 'total_amount', label: 'Total Amount' },
                { key: 'currency', label: 'Currency' },
              ].map((field) => (
                <div key={field.key}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                  </label>
                  {editing ? (
                    <input
                      type="text"
                      value={editData[field.key] || ''}
                      onChange={(e) => handleFieldChange(field.key, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md
                        focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div className="px-3 py-2 bg-gray-50 rounded-md">
                      {selectedExtraction[field.key] || '-'}
                    </div>
                  )}
                </div>
              ))}

              {[
                { key: 'supplier_address', label: 'Supplier Address' },
                { key: 'customer_address', label: 'Customer Address' },
              ].map((field) => (
                <div key={field.key} className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label}
                  </label>
                  {editing ? (
                    <textarea
                      value={editData[field.key] || ''}
                      onChange={(e) => handleFieldChange(field.key, e.target.value)}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md
                        focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div className="px-3 py-2 bg-gray-50 rounded-md whitespace-pre-wrap">
                      {selectedExtraction[field.key] || '-'}
                    </div>
                  )}
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
