import '../app/globals.css'

const Message = ({ content, isAi }: { content: string, isAi: boolean }) => {

    const style = isAi ? "message ai" : "message human"

    return (
        <div className={style}>
            <p>{content}</p>
        </div>
    )
}

export default Message
