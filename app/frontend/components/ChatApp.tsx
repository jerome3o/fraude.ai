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
        if (conversation?._id === id) {
            return;
        }

        const c = await fraude.getConversation(id);
        setConversation(c);
    }

    async function sendMessage(message: string) {
        if (!conversation) {
            return;
        }
        const thread = getThread(conversation.messages);
        const lastMessageId = thread.pop()?.id;

        conversation = await fraude.sendMessage(conversation._id, {
            content: message,
            type: "human",
            parent_message_id: lastMessageId,
        });

        setConversation(conversation);
    }

    async function newConversation() {
        const c = await fraude.createConversation("New Conversation");
        setConversations([...conversations, { id: c._id, title: c.title }]);
        setConversation(c);
    }

    return (
        <div className="chat-app">
            <ConversationList
                conversations={conversations}
                conversationId={conversation?._id}
                onSelect={onSelect}
                newConversation={newConversation}
            />
            <ActiveConversation
                conversation={conversation}
                sendMessage={sendMessage}
            />
        </div>
    );
}

export default ChatApp;
