import { useState, useEffect } from 'react';
import { Book, CheckCircle, Trash2, RotateCw } from 'lucide-react';
import { api } from '../api';

export const NoteBlock = ({ user, selectedDoc, refreshTrigger }) => {
    const [flashcards, setFlashcards] = useState([]);
    const [quizzes, setQuizzes] = useState([]);
    const [activeItem, setActiveItem] = useState(null); // { type: 'flashcard'|'quiz', id: ..., data: ... }

    useEffect(() => {
        if (selectedDoc) {
            fetchNotes();
            setActiveItem(null); // Reset view on doc change
        } else {
            setFlashcards([]);
            setQuizzes([]);
            setActiveItem(null);
        }
    }, [user.id, selectedDoc, refreshTrigger]);

    const fetchNotes = async () => {
        try {
            const fcRes = await api.listFlashcards(user.id, selectedDoc.id);
            const qRes = await api.listQuizzes(user.id, selectedDoc.id);
            setFlashcards(fcRes.data);
            setQuizzes(qRes.data);
        } catch (err) {
            console.error("Failed to fetch notes", err);
        }
    };

    const handleOpenFlashcard = async (id) => {
        try {
            const res = await api.getFlashcardSet(id, user.id);
            setActiveItem({ type: 'flashcard', id, data: res.data });
        } catch (e) { alert("Error loading flashcards: " + e.message); }
    };

    const handleOpenQuiz = async (id) => {
        try {
            const res = await api.getQuiz(id, user.id);
            setActiveItem({ type: 'quiz', id, data: res.data });
        } catch (e) { alert("Error loading quiz: " + e.message); }
    };

    const handleDelete = async (type, id) => {
        if (!confirm("Delete?")) return;
        try {
            if (type === 'flashcard') await api.deleteFlashcardSet(id, user.id);
            else await api.deleteQuiz(id, user.id);
            fetchNotes();
            if (activeItem?.id === id) setActiveItem(null);
        } catch (e) { alert("Delete failed"); }
    };

    // Sub-components
    const FlashcardViewer = ({ data }) => {
        const [index, setIndex] = useState(0);
        const [flipped, setFlipped] = useState(false);
        const cards = data.cards || [];

        if (!cards.length) return <div className="p-4">No cards found.</div>;

        const card = cards[index];

        return (
            <div className="p-4 bg-gray-50 rounded-xl border border-gray-200 h-full flex flex-col">
                <div className="flex justify-between items-center mb-4">
                    <h3 className="font-semibold truncate pr-2">{data.title || "Flashcards"}</h3>
                    <button onClick={() => setActiveItem(null)} className="text-sm text-blue-600 font-medium hover:underline">Close</button>
                </div>

                <div
                    className="flex-1 bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col items-center justify-center p-6 text-center cursor-pointer transition-all hover:shadow-md relative overflow-hidden"
                    onClick={() => setFlipped(!flipped)}
                >
                    <div className="absolute top-3 left-3 px-2 py-1 bg-gray-100 rounded text-xs font-bold text-gray-500 uppercase">
                        {flipped ? "Answer" : "Question"}
                    </div>
                    <div className="overflow-y-auto max-h-full w-full">
                        <p className="text-lg font-medium text-gray-800 leading-relaxed">
                            {flipped ? card.answer : card.question}
                        </p>
                    </div>
                </div>

                <div className="flex justify-between items-center mt-4">
                    <button
                        disabled={index === 0}
                        onClick={() => { setIndex(i => i - 1); setFlipped(false) }}
                        className="p-2 bg-white border rounded-lg shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-gray-600"
                    >
                        ← Prev
                    </button>
                    <span className="text-sm text-gray-500 font-medium">{index + 1} / {cards.length}</span>
                    <button
                        disabled={index === cards.length - 1}
                        onClick={() => { setIndex(i => i + 1); setFlipped(false) }}
                        className="p-2 bg-white border rounded-lg shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed text-gray-600"
                    >
                        Next →
                    </button>
                </div>
            </div>
        );
    };

    const QuizViewer = ({ data }) => {
        return (
            <div className="p-4 bg-gray-50 rounded-xl border border-gray-200 h-full flex flex-col">
                <div className="flex justify-between items-center mb-4 flex-shrink-0">
                    <h3 className="font-semibold truncate pr-2">Quiz</h3>
                    <button onClick={() => setActiveItem(null)} className="text-sm text-blue-600 font-medium hover:underline">Close</button>
                </div>
                <div className="space-y-4 overflow-y-auto flex-1 pr-1">
                    {data.map((q, i) => (
                        <div key={i} className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                            <p className="font-medium mb-3 text-gray-800">{i + 1}. {q.question}</p>
                            <div className="space-y-2">
                                {q.options && Object.entries(q.options).map(([k, v]) => (
                                    <div key={k} className={`p-2 rounded text-sm bg-gray-50 border border-transparent ${k === q.correct_answer ? 'bg-green-50 border-green-100' : ''}`}>
                                        <span className={`font-bold mr-2 ${k === q.correct_answer ? 'text-green-700' : 'text-gray-500'}`}>{k.toUpperCase()}.</span>
                                        <span className={k === q.correct_answer ? 'text-green-800' : 'text-gray-700'}>{v}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    if (!selectedDoc) return <div className="w-80 bg-notebook-sidebar border-l border-gray-200 flex-shrink-0"></div>;

    return (
        <div className="w-80 bg-notebook-sidebar border-l border-gray-200 flex flex-col h-screen flex-shrink-0">
            <div className="p-4 border-b border-gray-200 bg-transparent">
                <h2 className="font-semibold text-gray-700">Your Work</h2>
                <p className="text-xs text-gray-500">Saved flashcards & quizzes</p>
            </div>

            <div className="flex-1 overflow-hidden p-3 relative">
                {activeItem ? (
                    activeItem.type === 'flashcard' ? (
                        <FlashcardViewer data={activeItem.data} />
                    ) : (
                        <QuizViewer data={activeItem.data} />
                    )
                ) : (
                    <div className="space-y-3 overflow-y-auto h-full">
                        {flashcards.length === 0 && quizzes.length === 0 && (
                            <div className="text-center text-gray-400 mt-20 text-sm px-4">
                                <div className="bg-white w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3 shadow-sm">
                                    <Book className="w-6 h-6 text-gray-300" />
                                </div>
                                <p>Nothing saved yet.</p>
                                <p className="text-xs mt-1">Generate content in the chat interface.</p>
                            </div>
                        )}

                        {/* Flashcards List */}
                        {flashcards.map(fc => (
                            <div key={fc.id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer group relative" onClick={() => handleOpenFlashcard(fc.id)}>
                                <div className="flex items-start mb-2">
                                    <div className="bg-blue-100 p-2 rounded-lg mr-3 flex-shrink-0">
                                        <RotateCw className="w-4 h-4 text-blue-600" />
                                    </div>
                                    <div>
                                        <h4 className="font-medium text-sm text-gray-800 line-clamp-2">{fc.title}</h4>
                                        <p className="text-xs text-gray-400 mt-0.5">Flashcards</p>
                                    </div>
                                </div>
                                <button onClick={(e) => { e.stopPropagation(); handleDelete('flashcard', fc.id) }} className="absolute top-2 right-2 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-1">
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        ))}

                        {/* Quizzes List */}
                        {quizzes.map(q => {
                            // Handle tuple vs obj
                            const [id, title, date] = Array.isArray(q) ? q : [q.id, q.title, q.created_at];
                            return (
                                <div key={id} className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-all cursor-pointer group relative" onClick={() => handleOpenQuiz(id)}>
                                    <div className="flex items-start mb-2">
                                        <div className="bg-purple-100 p-2 rounded-lg mr-3 flex-shrink-0">
                                            <CheckCircle className="w-4 h-4 text-purple-600" />
                                        </div>
                                        <div>
                                            <h4 className="font-medium text-sm text-gray-800 line-clamp-2">{title}</h4>
                                            <p className="text-xs text-gray-400 mt-0.5">Quiz</p>
                                        </div>
                                    </div>
                                    <button onClick={(e) => { e.stopPropagation(); handleDelete('quiz', id) }} className="absolute top-2 right-2 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-1">
                                        <Trash2 className="w-4 h-4" />
                                    </button>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};
