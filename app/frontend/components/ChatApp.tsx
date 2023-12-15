"use client";

import "../app/globals.css";
import ActiveConversation from "./ActiveConversation";
import ConversationList from "./ConversationsList";

import { useState, useEffect } from "react";

import { ApiService, ConversationHeaders, getThread } from "../fraude/apiService";

const ChatApp = () => {
    const user = "jerome";
    const fraude = new ApiService(user);

    let [conversations, setConversations] = useState<ConversationHeaders>([]);
    let [conversationId, setConversationId] = useState<string | undefined>(undefined);
    let [conversationTitle, setConversationTitle] = useState<string | undefined>(undefined);
    let [messages, setMessages] = useState<string[]>(["hey", "hi", "hello"]);

    useEffect(() => {
        fraude.getConversationHeaders().then((res) => {
            setConversations(res);
        });
    }, []);

    async function onSelect(id: string, title: string) {
        setConversationId(id);
        setConversationTitle(title);
        const conversation = await fraude.getConversation(id);
        const messages = getThread(conversation.messages);

        console.log(conversation);
        setMessages(messages.map((message) => { return message.content }));
    }

    return (
        <div className="chat-app">
            <h1>Fraude</h1>
            <div className="chat-app-inner">
                <ConversationList conversations={conversations} onSelect={onSelect} />
                <ActiveConversation
                    conversationTitle={conversationTitle}
                    conversationId={conversationId}
                    messages={messages}
                />
            </div>
        </div>
    );
};

export default ChatApp;
