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
            <div className="active-conversation-header">
                <h3>
                    {conversation.title}
                </h3>
                <button onClick={openPopup}>edit</button>
            </div>
            <div className={popupClass} id="conversation-popup">
                <div className="centered">
                    <input
                        type="text"
                        value={titleInput}
                        onChange={(e) => setTitleInput(e.target.value)}
                        className="message-input-text"
                    />
                    <div id="conversation-popup-buttons">
                        <button onClick={cancelPopup}>cancel</button>
                        <button onClick={submitPopup}>accept</button>
                    </div>
                </div>
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
