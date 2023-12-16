import "../app/globals.css";
import Message from "./Message";

import { StoredMessage } from "../fraude/apiService";

const MessageList = ({
    messages,
    latestHumanMessage,
    partialMessage,
}: {
    messages: StoredMessage[];
    latestHumanMessage: string | undefined;
    partialMessage: string | undefined;
}) => {
    return (
        <div className="message-list">
            <div className="message-list-box">
                {messages.map((message, index) => {
                    return (
                        <Message
                            key={index}
                            content={message.content}
                            isAi={message.type === "ai"}
                        />
                    );
                })}
                {
                    latestHumanMessage &&
                    <Message
                        key={messages.length + 100}
                        content={latestHumanMessage}
                        isAi={false}
                    />
                }
                {
                    latestHumanMessage &&
                    <Message
                        key={messages.length + 101}
                        content={partialMessage || "..."}
                        isAi={true}
                    />
                }
            </div>
        </div>
    );
};

export default MessageList;
