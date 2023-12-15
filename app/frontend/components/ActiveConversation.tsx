import "../app/globals.css";
import MessageInput from "./MessageInput";
import MessageList from "./MessageList";

const ActiveConversation = ({
    conversationTitle,
    conversationId,
}: {
    conversationTitle: string | undefined;
    conversationId: string | undefined;
}) => {
    return (
        <div className="active-conversation debug">
            <h3>
                {conversationTitle}, {conversationId}
            </h3>
            <MessageList />
            <MessageInput />
        </div>
    );
};

export default ActiveConversation;
