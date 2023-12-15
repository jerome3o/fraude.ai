import "../app/globals.css";

import { ConversationHeaders } from "../fraude/apiService";

const ConversationList = ({
    conversations,
    conversationId,
    onSelect,
    newConversation,
}: {
    conversations: ConversationHeaders;
    conversationId: string | undefined;
    onSelect: (id: string, title: string) => void;
    newConversation: () => void;
}) => {
    const innerOnSelect = (i: number) => {
        return () => {
            onSelect(conversations[i].id, conversations[i].title);
        };
    };

    return (
        <div className="conversations-list">
            <h3>Conversations</h3>
            <div className="conversations-list-inner">
                {conversations.map((info, index) => {
                    return (
                        <button
                            key={info.id}
                            onClick={innerOnSelect(index)}
                            className={info.id === conversationId ? "active-convo" : "inactive-convo"}
                        >
                            {info.title}
                        </button>
                    );
                })}
                <button onClick={newConversation} className="inactive-convo">+</button>
            </div>
        </div >
    );
};

export default ConversationList;
