"use client";

import "../app/globals.css";
import ActiveConversation from "./ActiveConversation";
import ConversationList from "./ConversationsList";

import { useState, useEffect } from "react";

import { ApiService, ConversationHeaders, getThread, StoredMessage, StoredConversation } from "../fraude/apiService";

const ChatApp = () => {
    const user = "jerome";
    const fraude = new ApiService(user);

    let [conversations, setConversations] = useState<ConversationHeaders>([]);
    let [conversation, setConversation] = useState<StoredConversation | undefined>(undefined);

    useEffect(() => {
        fraude.getConversationHeaders().then((res) => {
            setConversations(res);
        });
    }, []);

    async function onSelect(id: string, title: string) {
        const conversation = await fraude.getConversation(id);
        setConversation(conversation);
    }

    return (
        <div className="chat-app">
            <h1>Fraude</h1>
            <div className="chat-app-inner">
                <ConversationList conversations={conversations} onSelect={onSelect} />
                <ActiveConversation
                    conversation={conversation}
                />
            </div>
        </div>
    );
};

export default ChatApp;
