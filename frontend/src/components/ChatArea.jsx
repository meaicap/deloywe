import { useState } from 'react';
import { Send, Zap, BookOpen, Sparkles } from 'lucide-react';
import clsx from 'clsx';
import { api } from '../api';

export const ChatArea = ({ user, selectedDoc, onFlashcardsCreated, onQuizCreated }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleCreateFlashcards = async () => {
        setLoading(true);
        addMessage({ role: 'user', content: 'Create Flashcards' });
        try {
            addMessage({ role: 'assistant', content: 'Generating flashcards...', loading: true });
            await api.createFlashcards({
                user_id: user.id,
                document_id: selectedDoc.id,
                num_cards: 10
            });
            removeLoadingMessage();
            addMessage({ role: 'assistant', content: 'Flashcards created! Check the notes panel.' });
            onFlashcardsCreated();
        } catch (err) {
            removeLoadingMessage();
            addMessage({ role: 'assistant', content: 'Error creating flashcards.', error: true });
        } finally {
            setLoading(false);
        }
    };

    const handleCreateQuiz = async () => {
        setLoading(true);
        addMessage({ role: 'user', content: 'Create Quiz' });
        try {
            addMessage({ role: 'assistant', content: 'Generating quiz...', loading: true });
            await api.createQuiz({
                user_id: user.id,
                document_id: selectedDoc.id,
                num_questions: 10
            });
            removeLoadingMessage();
            addMessage({ role: 'assistant', content: 'Quiz created! Check the notes panel.' });
            onQuizCreated();
        } catch (err) {
            removeLoadingMessage();
            addMessage({ role: 'assistant', content: 'Error creating quiz.', error: true });
        } finally {
            setLoading(false);
        }
    };

    const addMessage = (msg) => {
        setMessages(prev => [...prev, { id: Date.now(), ...msg }]);
    };

    const removeLoadingMessage = () => {
        setMessages(prev => prev.filter(m => !m.loading));
    };

    if (!selectedDoc) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-gray-500 bg-white">
                <Sparkles className="w-16 h-16 text-notebook-accent opacity-20 mb-4" />
                <h2 className="text-xl font-semibold text-gray-700">Select a source to begin</h2>
                <p className="max-w-md mt-2">Upload a PDF or select an existing one from the sidebar to start studying with AI.</p>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col h-screen bg-white relative">
            {/* Header */}
            <div className="p-4 border-b border-gray-100 flex items-center justify-between z-10 bg-white/80 backdrop-blur-sm sticky top-0">
                <h1 className="text-lg font-semibold text-gray-800 truncate px-2">{selectedDoc.filename || "Untitled Source"}</h1>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4 space-y-6">
                {messages.length === 0 && (
                    <div className="mt-10 mx-auto max-w-2xl">
                        <div className="text-center mb-10">
                            <div className="bg-gradient-to-br from-blue-500 to-purple-600 w-16 h-16 rounded-2xl mx-auto flex items-center justify-center mb-4 shadow-lg shadow-blue-200">
                                <Sparkles className="w-8 h-8 text-white" />
                            </div>
                            <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600">
                                Notebook Guide
                            </h2>
                            <p className="text-gray-500 mt-2">NotebookLM-inspired AI Assistant</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <button
                                onClick={handleCreateFlashcards}
                                disabled={loading}
                                className="bg-gray-50 hover:bg-white hover:shadow-md border border-transparent hover:border-gray-200 p-6 rounded-2xl text-left transition-all group"
                            >
                                <div className="bg-blue-100 w-10 h-10 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                    <Zap className="w-5 h-5 text-blue-600" />
                                </div>
                                <h3 className="font-semibold text-gray-900">Flashcards</h3>
                                <p className="text-sm text-gray-500 mt-1">Generate study cards from this document</p>
                            </button>

                            <button
                                onClick={handleCreateQuiz}
                                disabled={loading}
                                className="bg-gray-50 hover:bg-white hover:shadow-md border border-transparent hover:border-gray-200 p-6 rounded-2xl text-left transition-all group"
                            >
                                <div className="bg-purple-100 w-10 h-10 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                                    <BookOpen className="w-5 h-5 text-purple-600" />
                                </div>
                                <h3 className="font-semibold text-gray-900">Quiz</h3>
                                <p className="text-sm text-gray-500 mt-1">Test your knowledge with a quiz</p>
                            </button>
                        </div>
                    </div>
                )}

                {messages.map((msg, i) => (
                    <div key={msg.id || i} className={clsx(
                        "flex w-full",
                        msg.role === 'user' ? 'justify-end' : 'justify-start'
                    )}>
                        <div className={clsx(
                            "max-w-[80%] rounded-2xl p-4 text-sm leading-relaxed shadow-sm",
                            msg.role === 'user'
                                ? 'bg-notebook-accent text-white rounded-br-none'
                                : 'bg-gray-100 text-gray-800 rounded-bl-none'
                        )}>
                            {msg.loading ? (
                                <div className="flex items-center space-x-2">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            ) : (
                                msg.content
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Input */}
            <div className="p-4 bg-white border-t border-gray-100">
                <div className="relative max-w-3xl mx-auto">
                    <input
                        type="text"
                        className="w-full bg-notebook-sidebar border-0 rounded-full py-4 pl-6 pr-14 text-sm focus:ring-2 focus:ring-notebook-accent/50 outline-none transition-shadow"
                        placeholder="Ask a question about your source..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                if (!input.trim()) return;
                                addMessage({ role: 'user', content: input });
                                setInput('');
                                setTimeout(() => {
                                    addMessage({ role: 'assistant', content: "Chat functionality is not yet connected to the backend. Please use the buttons above to generate Flashcards or Quizzes." });
                                }, 600);
                            }
                        }}
                    />
                    <button
                        className="absolute right-2 top-2 p-2 bg-notebook-accent text-white rounded-full hover:bg-blue-600 transition-colors"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
};
