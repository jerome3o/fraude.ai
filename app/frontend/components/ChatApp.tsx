'use client';

import '../app/globals.css'
import ActiveConversation from "./ActiveConversation"
import ConversationList from "./ConversationsList"

import { useState, useEffect } from 'react';

import { ApiService, ConversationHeaders } from '../fraude/apiService'

const ChatApp = () => {

    const user = "jerome";
    const fraude = new ApiService(user);

    let [conversations, setConversations] = useState<ConversationHeaders>([]);

    useEffect(() => {
        fraude.getConversationHeaders().then((res) => {
            setConversations(res);
        });
    }, []);


    return (
        <div className='chat-app'>
            <h1>Fraude</h1>
            <div className='chat-app-inner'>
                <ConversationList conversations={conversations} />
                <ActiveConversation conversationTitle='Test conversation title' />
            </div>
        </div>
    )
}

export default ChatApp
