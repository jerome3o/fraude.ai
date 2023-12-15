import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

import { useState, useEffect } from "react";

const ActiveConversation = ({
    conversationTitle,
    conversationId,
    messages,
}: {
    conversationTitle: string | undefined;
    conversationId: string | undefined;
    messages: string[];
}) => {
    return (
        <div className="active-conversation debug">
            <h3>
                {conversationTitle}, {conversationId}
            </h3>
            <MessageList messages={messages} />
            <MessageInput />
        </div>
    );
};

export default ActiveConversation;
