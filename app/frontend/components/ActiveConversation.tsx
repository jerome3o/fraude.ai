import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

import { getThread, StoredConversation } from "../fraude/apiService";

const ActiveConversation = ({
    conversation,
    sendMessage,
    latestHumanMessage,
}: {
    conversation: StoredConversation | undefined;
    sendMessage: (message: string) => Promise<void>;
    latestHumanMessage: string | undefined;
}) => {
    if (!conversation) {
        return <div className="active-conversation"></div>;
    }

    const messages = getThread(conversation.messages);

    return (
        <div className="active-conversation">
            <h3>
                {conversation.title}
            </h3>
            <MessageList
                messages={messages}
                latestHumanMessage={latestHumanMessage}
            />
            <MessageInput sendMessage={sendMessage} />
        </div>
    );
};

export default ActiveConversation;
