"use client";

import "../app/globals.css";
import ActiveConversation from "./ActiveConversation";
import ConversationList from "./ConversationsList";

import { useState, useEffect } from "react";

import {
  ApiService,
  ConversationHeaders,
  getThread,
  StoredConversation,
} from "../fraude/apiService";

const ChatApp = () => {
  const user = "jerome";
  const fraude = new ApiService(user);

  const [conversations, setConversations] = useState<ConversationHeaders>([]);
  const [conversation, setConversation] = useState<
    StoredConversation | undefined
  >(undefined);
  const [latestHumanMessage, setLatestHumanMessage] = useState<
    string | undefined
  >(undefined);
  const [partialMessage, setPartialMessage] = useState<string | undefined>(
    undefined
  );

  useEffect(() => {
    fraude.getConversationHeaders().then((res) => {
      setConversations(res);
    });
  }, [fraude]);

  async function onSelect(id: string, title: string) {
    if (conversation?._id === id) {
      return;
    }

    const c = await fraude.getConversation(id);
    setConversation(c);
  }

  async function sendMessageWs(message: string) {
    if (!conversation) {
      return;
    }

    if (message === "") {
      return;
    }
    setPartialMessage(undefined);

    const thread = getThread(conversation.messages);
    const lastMessage = thread.pop();
    const lastMessageId = lastMessage?.id;

    setLatestHumanMessage(message);

    fraude.sendMessageStream(
      conversation._id,
      {
        content: message,
        type: "human",
        parent_message_id: lastMessageId,
      },
      setPartialMessage,
      async () => {
        const newConvo = await fraude.getConversation(conversation._id);
        setLatestHumanMessage(undefined);
        setConversation(newConvo);
      }
    );
  }

  async function newConversation() {
    const c = await fraude.createConversation("New Conversation");
    setConversations([...conversations, { id: c._id, title: c.title }]);
    setConversation(c);
  }

  async function renameConversation(newName: string) {
    if (!conversation) {
      return;
    }
    const newConversation = await fraude.renameConversation(
      conversation._id,
      newName
    );
    setConversation(newConversation);

    // TODO: don't need to re-hit the server
    fraude.getConversationHeaders().then((res) => {
      setConversations(res);
    });
  }

  return (
    <div className="chat-app">
      <ConversationList
        conversations={conversations}
        conversationId={conversation?._id}
        onSelect={onSelect}
        newConversation={newConversation}
      />
      <ActiveConversation
        conversation={conversation}
        sendMessage={sendMessageWs}
        latestHumanMessage={latestHumanMessage}
        partialMessage={partialMessage}
        renameConversation={renameConversation}
      />
    </div>
  );
};

export default ChatApp;
