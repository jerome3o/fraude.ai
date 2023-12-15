import "../app/globals.css";
import Message from "./Message";

import { StoredMessage } from "../fraude/apiService";

const MessageList = ({ messages }: { messages: StoredMessage[] }) => {
    return (
        <div className="message-list debug">
            {messages.map((message, index) => {
                return <Message key={index} content={message.content} isAi={message.type === "ai"} />;
            })}
        </div>
    );
};

export default MessageList;
