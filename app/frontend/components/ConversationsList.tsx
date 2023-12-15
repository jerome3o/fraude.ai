import "../app/globals.css";

import { ConversationHeaders } from "../fraude/apiService";

const ConversationList = ({
    conversations,
    onSelect,
}: {
    conversations: ConversationHeaders;
    onSelect: (id: string, title: string) => void;
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
                        <button key={info.id} onClick={innerOnSelect(index)}>
                            {info.title}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default ConversationList;
