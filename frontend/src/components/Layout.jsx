import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { ChatArea } from './ChatArea';
import { NoteBlock } from './NoteBlock';
import { LogOut } from 'lucide-react';

export const Layout = ({ user, onLogout }) => {
    const [selectedDoc, setSelectedDoc] = useState(null); // Full object { id, filename }
    const [refreshNotes, setRefreshNotes] = useState(0);

    const handleSelectDoc = (doc) => {
        // doc can be {id, filename} or null
        setSelectedDoc(doc);
    };

    const triggerNoteRefresh = () => {
        setRefreshNotes(prev => prev + 1);
    };

    return (
        <div className="flex h-screen bg-[#F0F2F5] overflow-hidden font-sans text-notebook-text">
            {/* Sidebar (Left) */}
            <Sidebar
                user={user}
                selectedDocId={selectedDoc?.id}
                onSelectDoc={handleSelectDoc}
            />

            {/* Main Area (Middle - Chat) */}
            <div className="flex-1 flex flex-col min-w-0 m-2 mr-0 rounded-2xl bg-white shadow-sm border border-gray-200 overflow-hidden relative">
                {/* User Controls (Floating Top Right) */}
                <div className="absolute top-4 right-4 z-50 flex items-center space-x-3 pointer-events-auto">
                    <div className="flex items-center space-x-2 bg-white/90 backdrop-blur border border-gray-200 rounded-full px-3 py-1.5 shadow-sm hover:shadow transition-all">
                        <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 text-xs font-bold">
                            {user.username?.[0]?.toUpperCase()}
                        </div>
                        <span className="text-sm font-medium text-gray-600 max-w-[100px] truncate">{user.username}</span>
                        <div className="h-4 w-px bg-gray-200 mx-2"></div>
                        <button onClick={onLogout} title="Logout" className="text-gray-400 hover:text-red-500 transition-colors">
                            <LogOut className="w-4 h-4" />
                        </button>
                    </div>
                </div>

                <ChatArea
                    user={user}
                    selectedDoc={selectedDoc}
                    onFlashcardsCreated={triggerNoteRefresh}
                    onQuizCreated={triggerNoteRefresh}
                />
            </div>

            {/* Right Panel (Notes) */}
            {/* Pass selectedDoc to ensure it knows context */}
            <NoteBlock
                user={user}
                selectedDoc={selectedDoc}
                refreshTrigger={refreshNotes}
            />
        </div>
    );
};
