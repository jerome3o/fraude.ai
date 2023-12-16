
// in python it's list[tuple[str, str]]
type ConversationHeaders = {
  title: string,
  id: string
}[];

interface StoredMessage {
  id: string;
  type: string;
  content: string;
  responses: StoredMessage[];
  conversation_id: string;
}

interface StoredConversation {
  _id: string;
  title: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  messages: StoredMessage[];
}

interface CreateMessage {
  type: string;
  content: string;
  parent_message_id: string | undefined;
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
  private wsUrl: string;
  private user: string;

  // default to ""
  constructor(user: string, baseUrl: string = "") {
    this.user = user;
    this.baseUrl = baseUrl || window.location.origin;

    // handle when http is in the URL.. ?
    this.wsUrl = this.baseUrl.replace("http", "ws");
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

  async sendMessage(id: string, message: CreateMessage): Promise<StoredConversation> {
    const response = await fetch(`${this.baseUrl}/api/conversations/id/${id}/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    });

    if (!response.ok) {
      throw new Error(`Could not send message to conversation with id ${id}`);
    }

    return await response.json();
  }

  async sendMessageStream(
    id: string,
    message: CreateMessage,
    onPartial: (partialMessage: string) => void,
    onFinish: () => void,
  ) {
    const url = `${this.wsUrl}/api/conversations/id/${id}/message`
    const socket = new WebSocket(url);

    socket.onopen = () => {
      socket.send(JSON.stringify(message));
    }

    let partialMessage = "";
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      partialMessage += data.latest_token
      onPartial(partialMessage);
    }

    socket.onclose = () => {
      onFinish();
    }
  }

  async createConversation(title: string): Promise<StoredConversation> {
    const response = await fetch(`${this.baseUrl}/api/conversations/user/${this.user}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    });

    if (!response.ok) {
      throw new Error(`Could not create conversation with title ${title}`);
    }

    return await response.json();
  }

  async renameConversation(id: string, title: string): Promise<StoredConversation> {
    const response = await fetch(`${this.baseUrl}/api/conversations/id/${id}/rename`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title }),
    });

    if (!response.ok) {
      throw new Error(`Could not rename conversation with id ${id}`);
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
