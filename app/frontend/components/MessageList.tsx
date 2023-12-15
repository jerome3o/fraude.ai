import '../app/globals.css'
import Message from "./Message"

const MessageList = () => {
    return (
        <div className="message-list debug">
            <Message content="AI message" isAi={true} />
            <Message content="Human message" isAi={false} />
        </div>
    )
}

export default MessageList
