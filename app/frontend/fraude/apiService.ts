
// in python it's list[tuple[str, str]]
type ConversationHeaders = {
    title: string,
    id: string
}[];

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

    // Add more methods for other endpoints
}

export {
  ApiService,
  type ConversationHeaders,
};
