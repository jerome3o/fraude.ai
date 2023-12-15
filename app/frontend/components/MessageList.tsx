import "../app/globals.css";
import Message from "./Message";

const MessageList = ({ messages }: { messages: string[] }) => {
    return (
        <div className="message-list debug">
            {messages.map((message, index) => {
                return <Message key={index} content={message} isAi={index % 2 === 1} />;
            })}
        </div>
    );
};

export default MessageList;
