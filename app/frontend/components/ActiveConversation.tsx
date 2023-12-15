import '../app/globals.css'
import MessageInput from "./MessageInput"
import MessageList from "./MessageList"

const ActiveConversation = () => {
    return (
        <div className='active-conversation debug'>
            <h1>ActiveConversation</h1>
            <MessageList />
            <MessageInput />
        </div>
    )
}

export default ActiveConversation
