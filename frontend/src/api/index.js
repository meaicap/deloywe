import axios from 'axios';

// Get API Base URL from environment or default to current origin (which works with proxy dev)
// BUT for production, if frontend and backend are different domains, we need the full URL.
// If using Render Static Site + Web Service, the backend is a different URL.
// Vite exposes env vars prefixed with VITE_
const API_BASE = import.meta.env.VITE_API_URL || '';
// If API_BASE is empty (dev mode or same domain), it uses relative paths.
// If Production and different domain, user must set VITE_API_URL.

const API = axios.create({
    baseURL: API_BASE,
});

export const api = {
    // Auth
    login: (data) => API.post('/auth/login', data),
    register: (data) => API.post('/auth/register', data),

    // Documents
    getDocuments: (userId) => API.get(`/documents/user/${userId}`),
    uploadPdf: (formData) => API.post('/upload/pdf', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
    deleteDocument: (docId, userId) => API.delete(`/documents/${docId}?user_id=${userId}`),

    // Flashcards
    createFlashcards: (data) => API.post('/flashcard/create', data),
    listFlashcards: (userId, docId) => API.get(`/flashcard/list/${userId}`, { params: { document_id: docId } }),
    getFlashcardSet: (setId, userId) => API.get(`/flashcard/${setId}`, { params: { user_id: userId } }),
    deleteFlashcardSet: (setId, userId) => API.delete(`/flashcard/${setId}`, { params: { user_id: userId } }),

    // Quiz
    createQuiz: (data) => API.post('/quiz/create', data),
    listQuizzes: (userId, docId) => API.get(`/quiz/list/${userId}`, { params: { document_id: docId } }),
    getQuiz: (quizId, userId) => API.get(`/quiz/${quizId}`, { params: { user_id: userId } }),
    deleteQuiz: (quizId, userId) => API.delete(`/quiz/${quizId}`, { params: { user_id: userId } }),
};
