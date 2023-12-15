import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

import { getThread, StoredConversation } from "../fraude/apiService";

const ActiveConversation = ({
    conversation,
    sendMessage,
}: {
    conversation: StoredConversation | undefined;
    sendMessage: (message: string) => Promise<void>;
}) => {
    if (!conversation) {
        return <div className="active-conversation debug"></div>;
    }

    const messages = getThread(conversation.messages);

    return (
        <div className="active-conversation debug">
            <h3>
                {conversation.title}
            </h3>
            <MessageList messages={messages} />
            <MessageInput sendMessage={sendMessage} />
        </div>
    );
};

export default ActiveConversation;
