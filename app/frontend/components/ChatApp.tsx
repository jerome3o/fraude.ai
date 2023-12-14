import ActiveConversation from "./ActiveConversation"
import ConversationList from "./ConversationsList"

const ChatApp = () => {
    return (
        <div>
            <h1>ChatApp</h1>
            <ConversationList />
            <ActiveConversation />
        </div>
    )
}

export default ChatApp
