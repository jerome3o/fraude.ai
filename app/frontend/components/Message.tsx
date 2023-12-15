import '../app/globals.css'

const Message = ({ content, isAi }: { content: string, isAi: boolean }) => {

    const innerClass = `${isAi ? "ai-message-inner" : "human-message-inner"} message-inner`
    const outerClass = `${isAi ? "ai-message" : "human-message"} message`


    return (
        <div className={outerClass}>
            <div className={innerClass}>
                <p>{content}</p>
            </div>
        </div >
    )
}

export default Message
