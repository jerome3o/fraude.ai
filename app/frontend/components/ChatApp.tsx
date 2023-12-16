"use client";

import "../app/globals.css";
import ActiveConversation from "./ActiveConversation";
import ConversationList from "./ConversationsList";

import { useState, useEffect } from "react";

import {
    ApiService,
    ConversationHeaders,
    getThread,
    StoredMessage,
    StoredConversation,
} from "../fraude/apiService";

const ChatApp = () => {
    const user = "jerome";
    const fraude = new ApiService(user);

    let [conversations, setConversations] = useState<ConversationHeaders>([]);
    let [conversation, setConversation] = useState<StoredConversation | undefined>(undefined);
    let [latestHumanMessage, setLatestHumanMessage] = useState<string | undefined>(undefined);

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

        if (message === "") {
            return;
        }
        const thread = getThread(conversation.messages);
        const lastMessage = thread.pop();
        const lastMessageId = lastMessage?.id;

        setLatestHumanMessage(message);

        conversation = await fraude.sendMessage(conversation._id, {
            content: message,
            type: "human",
            parent_message_id: lastMessageId,
        });

        setLatestHumanMessage(undefined);
        setConversation(conversation);
    }

    async function newConversation() {
        const c = await fraude.createConversation("New Conversation");
        setConversations([...conversations, { id: c._id, title: c.title }]);
        setConversation(c);
    }

    async function renameConversation(newName: string) {
        console.log("renameConversation", newName);
        if (!conversation) {
            return;
        }
        const newConversation = await fraude.renameConversation(conversation._id, newName);
        setConversation(newConversation);

        // TODO: don't need to re-hit the server
        fraude.getConversationHeaders().then((res) => {
            setConversations(res);
        });
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
                latestHumanMessage={latestHumanMessage}
                renameConversation={renameConversation}
            />
        </div>
    );
};

export default ChatApp;
