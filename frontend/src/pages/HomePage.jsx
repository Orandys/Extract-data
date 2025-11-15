import React, { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import DocumentList from '../components/DocumentList';
import ExtractionView from '../components/ExtractionView';
import { documentsAPI } from '../services/api';

function HomePage() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const data = await documentsAPI.list();
      setDocuments(data);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (document) => {
    setDocuments([document, ...documents]);
  };

  const handleDocumentDeleted = (id) => {
    setDocuments(documents.filter((doc) => doc.id !== id));
    if (selectedDocument?.id === id) {
      setSelectedDocument(null);
    }
  };

  const handleDocumentSelect = (document) => {
    setSelectedDocument(document);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Document Extraction System
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Extract data from delivery notes using OCR
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column - Upload */}
          <div className="lg:col-span-1">
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </div>

          {/* Right column - Documents and Extraction */}
          <div className="lg:col-span-2 space-y-6">
            {selectedDocument ? (
              <ExtractionView
                documentId={selectedDocument.id}
                onClose={() => setSelectedDocument(null)}
              />
            ) : (
              <DocumentList
                documents={documents}
                onDocumentSelect={handleDocumentSelect}
                onDocumentDeleted={handleDocumentDeleted}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default HomePage;
