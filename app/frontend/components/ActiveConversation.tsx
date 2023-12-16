import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

import { getThread, StoredConversation } from "../fraude/apiService";
import { useState } from "react";

const ActiveConversation = ({
    conversation,
    sendMessage,
    latestHumanMessage,
    renameConversation,
}: {
    conversation: StoredConversation | undefined;
    sendMessage: (message: string) => Promise<void>;
    latestHumanMessage: string | undefined;
    renameConversation: (title: string) => Promise<void>;
}) => {
    if (!conversation) {
        return <div className="active-conversation"></div>;
    }

    const messages = getThread(conversation.messages);
    const [titleInput, setTitleInput] = useState(conversation.title);


    // TODO: make this pop up a component?
    const [popupClass, setPopupClass] = useState("popup closed");
    function openPopup() {
        setTitleInput(conversation?.title || "Cool new name");
        setPopupClass("popup open");
    }
    function closePopup() {
        setPopupClass("popup closed");
    }
    function cancelPopup() {
        closePopup();
    }
    function submitPopup() {
        renameConversation(titleInput);
        closePopup();
    }

    return (
        <div className="active-conversation">
            <h3>
                {conversation.title}
            </h3>
            <button onClick={openPopup}>edit</button>
            <div className={popupClass} id="conversation-popup">
                <input type="text" value={titleInput} onChange={(e) => setTitleInput(e.target.value)} />
                <button onClick={submitPopup}>accept</button>
                <button onClick={cancelPopup}>cancel</button>
            </div>
            <MessageList
                messages={messages}
                latestHumanMessage={latestHumanMessage}
            />
            <MessageInput sendMessage={sendMessage} />
        </div >
    );
};

export default ActiveConversation;
