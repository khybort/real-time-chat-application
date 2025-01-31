import { create } from "zustand";

export interface Message {
  id: string;
  user: string;
  content: string;
  timestamp: string;
}

interface ChatStore {
  user: string | null;
  messages: Message[];
  setUser: (user: string) => void;
  addMessage: (message: Message) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  user: null,
  messages: [],
  setUser: (user: string) => set({ user }),
  addMessage: (message: Message) =>
    set((state) => ({ messages: [...state.messages, message] })),
}));
