import '../app/globals.css'
import MessageInput from "./MessageInput"
import MessageList from "./MessageList"

const ActiveConversation = ({ conversationTitle }: { conversationTitle: string }) => {
    return (
        <div className='active-conversation debug'>
            <h3>{conversationTitle}</h3>
            <MessageList />
            <MessageInput />
        </div>
    )
}

export default ActiveConversation
