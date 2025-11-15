import React from 'react';
import { documentsAPI } from '../services/api';

function DocumentList({ documents, onDocumentSelect, onDocumentDeleted }) {
  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this document?')) {
      try {
        await documentsAPI.delete(id);
        if (onDocumentDeleted) {
          onDocumentDeleted(id);
        }
      } catch (err) {
        console.error('Delete failed:', err);
        alert('Failed to delete document: ' + (err.response?.data?.detail || err.message));
      }
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 bg-gray-50 border-b">
        <h2 className="text-xl font-semibold">Uploaded Documents</h2>
      </div>

      <div className="divide-y">
        {documents.length === 0 ? (
          <div className="px-6 py-8 text-center text-gray-500">
            No documents uploaded yet. Upload a delivery note to get started.
          </div>
        ) : (
          documents.map((doc) => (
            <div
              key={doc.id}
              className="px-6 py-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <h3 className="font-medium text-gray-900">{doc.filename}</h3>
                  <p className="text-sm text-gray-500">
                    Uploaded: {new Date(doc.uploaded_at).toLocaleString()}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">ID: {doc.id}</p>
                </div>

                <div className="flex items-center space-x-2">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(
                      doc.status
                    )}`}
                  >
                    {doc.status}
                  </span>

                  <button
                    onClick={() => onDocumentSelect(doc)}
                    className="px-4 py-2 bg-blue-600 text-white text-sm rounded-md
                      hover:bg-blue-700 transition-colors"
                  >
                    View
                  </button>

                  <button
                    onClick={() => handleDelete(doc.id)}
                    className="px-4 py-2 bg-red-600 text-white text-sm rounded-md
                      hover:bg-red-700 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default DocumentList;
