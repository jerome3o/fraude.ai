'use client';

import '../app/globals.css'
import ActiveConversation from "./ActiveConversation"
import ConversationList from "./ConversationsList"

const ChatApp = () => {
    return (
        <div className='chat-app debug'>
            <h1>Fraude</h1>
            <div className='chat-app-inner debug'>
                <ConversationList />
                <ActiveConversation />
            </div>
        </div>
    )
}

export default ChatApp
