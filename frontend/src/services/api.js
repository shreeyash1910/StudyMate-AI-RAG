const API_URL =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:10000";


// ==============================
// USER API
// ==============================

export async function createUser(name, email, password_hash) {

    const params = new URLSearchParams();

    params.append("name", name);
    params.append("email", email);
    params.append("password_hash", password_hash);

    const response = await fetch(
        `${API_URL}/users/?${params.toString()}`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        throw new Error("Failed to create user");
    }

    return response.json();
}


export async function getUsers() {

    const response = await fetch(
        `${API_URL}/users/`
    );

    if (!response.ok) {
        throw new Error("Failed to get users");
    }

    return response.json();
}


// ==============================
// DOCUMENT API
// ==============================

export async function uploadDocument(file) {

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/documents/upload`,
        {
            method: "POST",
            body: formData
        }
    );

    if (!response.ok) {
        const error = await response.text();
        throw new Error(error);
    }

    return response.json();
}


// ==============================
// CONVERSATION API
// ==============================

export async function createConversation(
    userId,
    title
) {

    const params = new URLSearchParams();

    params.append("user_id", userId);
    params.append("title", title);

    const response = await fetch(
        `${API_URL}/conversations/?${params.toString()}`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        throw new Error("Failed to create conversation");
    }

    return response.json();
}


export async function getConversations(userId) {

    const response = await fetch(
        `${API_URL}/conversations/?user_id=${userId}`
    );

    if (!response.ok) {
        throw new Error("Failed to get conversations");
    }

    return response.json();
}


// ==============================
// MESSAGE API
// ==============================

export async function createMessage(
    conversationId,
    role,
    content
) {

    const params = new URLSearchParams();

    params.append(
        "conversation_id",
        conversationId
    );

    params.append(
        "role",
        role
    );

    params.append(
        "content",
        content
    );

    const response = await fetch(
        `${API_URL}/messages/?${params.toString()}`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        throw new Error("Failed to create message");
    }

    return response.json();
}


export async function getMessages(
    conversationId
) {

    const response = await fetch(
        `${API_URL}/messages/?conversation_id=${conversationId}`
    );

    if (!response.ok) {
        throw new Error("Failed to get messages");
    }

    return response.json();
}


// ==============================
// CHAT / RAG API
// ==============================

export async function askQuestion(
    question,
    documentId
) {

    const response = await fetch(
        `${API_URL}/chat/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                user_id: 1,
                question: question,
                document_id: documentId,
                top_k: 5
            })
        }
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            errorText || "Failed to get answer"
        );
    }

    return response.json();
}