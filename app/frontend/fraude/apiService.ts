
// in python it's list[tuple[str, str]]
type ConversationHeaders = {
  title: string,
  id: string
}[];

interface StoredMessage {
  id: string;
  content: string;
  responses: StoredMessage[];
  conversation_id: string;
}

interface StoredConversation {
  id: string | undefined;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  messages: StoredMessage[];
}


function getThread(messages: StoredMessage[]): StoredMessage[] {
  // initialise an array of StoredMessage
  const thread: StoredMessage[] = [];

  // while messages is not empty
  while (messages.length > 0) {
    // get the last message
    const message = messages[messages.length - 1];

    thread.push(message);
    messages = message.responses;
  }
  return thread;
}


class ApiService {
  private baseUrl: string;
  private user: string;

  // default to ""
  constructor(user: string, baseUrl: string = "") {
    this.user = user;
    this.baseUrl = baseUrl;
  }

  async getConversationHeaders(): Promise<ConversationHeaders> {
    const response = await fetch(`${this.baseUrl}/api/conversations/user/${this.user}`);

    if (!response.ok) {
      throw new Error(`Could not fetch user with id ${this.user}`);
    }

    return await response.json();
  }

  async getConversation(id: string): Promise<StoredConversation> {
    const response = await fetch(`${this.baseUrl}/api/conversations/id/${id}`);

    if (!response.ok) {
      throw new Error(`Could not fetch conversation with id ${id}`);
    }

    return await response.json();
  }
}

export {
  getThread,
  ApiService,
  type StoredMessage,
  type StoredConversation,
  type ConversationHeaders,
};
