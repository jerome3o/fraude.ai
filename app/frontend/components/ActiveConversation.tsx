import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

import { getThread, StoredConversation } from "../fraude/apiService";

const ActiveConversation = ({
    conversation,
}: {
    conversation: StoredConversation | undefined;
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
            <MessageInput />
        </div>
    );
};

export default ActiveConversation;
