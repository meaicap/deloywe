import { useState, useEffect, useRef } from 'react';
import { Plus, FileText, Trash2, Loader2 } from 'lucide-react';
import { api } from '../api';

export const Sidebar = ({ user, selectedDocId, onSelectDoc }) => {
    const [docs, setDocs] = useState([]);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);

    useEffect(() => {
        fetchDocs();
    }, [user.id]);

    // Expose fetchDocs to parent if needed? 
    // Better to lift state up to Layout, but keeping here for simplicity as requested "perfect connection" mostly implies functionality.
    // Actually, if Layout needs to know about docs (e.g. for title), we should lift state.
    // I'll keep local for now, but pass `onSelectDoc` with the *object*? No, ID is fine. 
    // But wait, ChatArea needs Title.
    // I will assume parent has the list or I pass the full object up.

    const fetchDocs = async () => {
        try {
            const res = await api.getDocuments(user.id);
            setDocs(res.data);
        } catch (err) {
            console.error("Failed to fetch docs", err);
        }
    };

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);
        formData.append('user_id', user.id);

        try {
            const res = await api.uploadPdf(formData);
            await fetchDocs();
            onSelectDoc(res.data); // Pass full object if possible?
            // Re-fetch logic might desync if parent doesn't know.
            // Let's stick to ID and let parent refetch? Or Sidebar manages the list.
            // If Sidebar manages the list, parent needs a way to get the doc details.
            // I'll update `onSelectDoc` to take the full object.
            // But api.uploadPdf returns: { document_id, filename... }
            // The `docs` list has: { id, filename... }
            // I'll normalize.
            onSelectDoc({ id: res.data.document_id, filename: res.data.filename });
        } catch (err) {
            alert("Upload failed: " + (err.response?.data?.detail || err.message));
        } finally {
            setUploading(false);
            if (fileInputRef.current) fileInputRef.current.value = '';
        }
    };

    const handleDelete = async (e, docId) => {
        e.stopPropagation();
        if (!confirm("Delete this document?")) return;
        try {
            await api.deleteDocument(docId, user.id);
            await fetchDocs();
            if (selectedDocId === docId) onSelectDoc(null);
        } catch (err) {
            alert("Delete failed");
        }
    };

    // On Selection, find the doc from local list to pass full object?
    const handleSelect = (doc) => {
        onSelectDoc(doc);
    };

    return (
        <div className="w-72 bg-notebook-sidebar border-r border-gray-200 h-screen flex flex-col flex-shrink-0">
            <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-transparent">
                <h2 className="font-semibold text-gray-700">Sources</h2>
                <button
                    onClick={() => fileInputRef.current?.click()}
                    className="p-1.5 hover:bg-gray-200 rounded-full transition-colors"
                    disabled={uploading}
                >
                    {uploading ? <Loader2 className="w-5 h-5 animate-spin text-notebook-accent" /> : <Plus className="w-5 h-5 text-gray-600" />}
                </button>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    accept=".pdf"
                    className="hidden"
                />
            </div>

            <div className="flex-1 overflow-y-auto p-3 space-y-2">
                {docs.map(doc => (
                    <div
                        key={doc.id}
                        onClick={() => handleSelect(doc)}
                        className={`p-3 rounded-xl flex items-center group cursor-pointer transition-all border ${selectedDocId === doc.id
                                ? 'bg-white border-blue-200 shadow-sm'
                                : 'hover:bg-gray-100 border-transparent'
                            }`}
                    >
                        <div className={`p-2 rounded-lg mr-3 flex-shrink-0 ${selectedDocId === doc.id ? 'bg-blue-50 text-notebook-accent' : 'bg-gray-200 text-gray-500'}`}>
                            <FileText className="w-5 h-5" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <h3 className={`text-sm font-medium truncate ${selectedDocId === doc.id ? 'text-notebook-accent' : 'text-gray-700'}`}>
                                {doc.filename}
                            </h3>
                            <p className="text-xs text-notebook-gray mt-0.5 truncate">PDF Source</p>
                        </div>
                        <button
                            onClick={(e) => handleDelete(e, doc.id)}
                            className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-50 hover:text-red-500 rounded text-gray-400 transition-all"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    </div>
                ))}
                {docs.length === 0 && !uploading && (
                    <div className="flex flex-col items-center justify-center mt-20 text-center opacity-50 px-6">
                        <div className="bg-gray-200 p-3 rounded-full mb-3">
                            <FileText className="w-6 h-6 text-gray-400" />
                        </div>
                        <p className="text-sm font-medium text-gray-500">No sources</p>
                        <p className="text-xs text-gray-400 mt-1">Upload a PDF to get started</p>
                    </div>
                )}
            </div>
        </div>
    );
};
