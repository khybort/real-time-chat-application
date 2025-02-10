import { useReducer, useEffect, useRef, useState } from "react";
import { jwtDecode } from "jwt-decode";
import MessageList from "../components/MessageList";
import MessageInput from "../components/MessageInput";
import Sidebar from "../components/Sidebar";
import Layout from "../components/Layout";

interface Message {
  sender: string;
  message: string;
}

interface State {
  messages: Message[];
  activeRoom: string;
  currentUser: string;
  rooms: string[];
}

interface Action {
  type: string;
  payload?: any;
}

const initialState: State = {
  messages: [],
  activeRoom: "",
  currentUser: "",
  rooms: [],
};

const reducer = (state: State, action: Action) => {
  switch (action.type) {
    case "SET_MESSAGES":
      return { ...state, messages: action.payload };
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            sender: action.payload.sender,
            message: action.payload.message,
          },
        ],
      };
    case "SET_ACTIVE_ROOM":
      return { ...state, activeRoom: action.payload };
    case "SET_CURRENT_USER":
      return { ...state, currentUser: action.payload };
    case "SET_ROOMS":
      return { ...state, rooms: action.payload };
    default:
      return state;
  }
};

const ChatPage: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const socketRef = useRef<WebSocket | null>(null);
  const historySocketRef = useRef<WebSocket | null>(null);
  const [typingUsers, setTypingUsers] = useState<string[]>([]);
  const typingTimeoutRef = useRef<{ [key: string]: NodeJS.Timeout }>({});

  useEffect(() => {
    const getToken = () => {
      const token = localStorage.getItem("access");
      if (token) {
        const decoded: any = jwtDecode(token);
        dispatch({
          type: "SET_CURRENT_USER",
          payload: decoded.username || "default_user",
        });
      }
    };

    getToken();
  }, []);

  useEffect(() => {
    const savedRoom = localStorage.getItem("activeRoom");
    if (savedRoom) {
      dispatch({ type: "SET_ACTIVE_ROOM", payload: savedRoom });
    }
  }, []);

  useEffect(() => {
    if (state.activeRoom) {
      localStorage.setItem("activeRoom", state.activeRoom);
    }
  }, [state.activeRoom]);

  useEffect(() => {
    const setupWebSocket = () => {
      if (!state.activeRoom) return;
      const WEBSOCKET_BASE_URL =
        import.meta.env.WEBSOCKET_BASE_URL || "ws://localhost:8000/ws/chat";
      const WEB_SOCKET_URL = `${WEBSOCKET_BASE_URL}/${state.activeRoom}/?token=${localStorage.getItem("access")}`;
      const HISTORY_SOCKET_URL = `${WEBSOCKET_BASE_URL}/history/${state.activeRoom}/?token=${localStorage.getItem("access")}`;

      if (socketRef.current) {
        socketRef.current.close();
      }
      if (historySocketRef.current) {
        historySocketRef.current.close();
      }

      socketRef.current = new WebSocket(WEB_SOCKET_URL);

      socketRef.current.onopen = () => {
        console.log(`WebSocket connection opened: ${state.activeRoom}`);
        joinRoom(state.activeRoom);
      };

      socketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.error) {
          console.error("WebSocket error:", data.error);
          return;
        }

        if (data.type === "typing") {
          const sender = data.sender;
          if (sender !== state.currentUser) {
            if (typingTimeoutRef.current[sender]) {
              clearTimeout(typingTimeoutRef.current[sender]);
            }
            setTypingUsers((prev) => {
              if (prev.includes(sender)) {
                return prev;
              }
              return [...prev, sender];
            });

            typingTimeoutRef.current[sender] = setTimeout(() => {
              setTypingUsers((prev) => prev.filter((user) => user !== sender));
              delete typingTimeoutRef.current[sender];
            }, 3000);
          }
        } else if (data.type === "stop_typing") {
          const sender = data.sender;
          if (typingTimeoutRef.current[sender]) {
            clearTimeout(typingTimeoutRef.current[sender]);
            delete typingTimeoutRef.current[sender];
          }
          setTypingUsers((prev) => prev.filter((user) => user !== sender));
        } else if (data.type === "chat_message") {
          const sender = data.sender;
          if (typingTimeoutRef.current[sender]) {
            clearTimeout(typingTimeoutRef.current[sender]);
            delete typingTimeoutRef.current[sender];
          }
          setTypingUsers((prev) => prev.filter((user) => user !== sender));

          dispatch({
            type: "ADD_MESSAGE",
            payload: {
              sender: data.sender,
              message: data.message,
            },
          });
        }
      };

      socketRef.current.onclose = () => {
        console.log(`WebSocket connection closed: ${state.activeRoom}`);
      };

      historySocketRef.current = new WebSocket(HISTORY_SOCKET_URL);

      historySocketRef.current.onopen = () => {
        console.log(`History WebSocket connection opened: ${state.activeRoom}`);
        if (
          historySocketRef.current &&
          historySocketRef.current.readyState === WebSocket.OPEN
        ) {
          historySocketRef.current.send(
            JSON.stringify({ type: "get_message_history" }),
          );
        }
      };

      historySocketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "chat_history") {
          const formattedMessages = data.messages.map((msg: Message) => ({
            sender: msg.sender,
            message: msg.message,
          }));
          dispatch({ type: "SET_MESSAGES", payload: formattedMessages });
        }
      };

      historySocketRef.current.onclose = () => {
        console.log(`History WebSocket connection closed: ${state.activeRoom}`);
      };
    };

    setupWebSocket();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (historySocketRef.current) {
        historySocketRef.current.close();
      }
      Object.values(typingTimeoutRef.current).forEach((timeout) =>
        clearTimeout(timeout),
      );
      typingTimeoutRef.current = {};
    };
  }, [state.activeRoom]);

  const sendMessage = (message: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const messageData = {
        type: "chat_message",
        message: message,
        sender: state.currentUser,
      };

      socketRef.current.send(JSON.stringify(messageData));

      socketRef.current.send(
        JSON.stringify({
          type: "stop_typing",
          sender: state.currentUser,
        }),
      );

      setTypingUsers((prev) =>
        prev.filter((sender) => sender !== state.currentUser),
      );
    }
  };

  const joinRoom = (room: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: "join_room", room }));
    }
  };

  const changeRoom = (room: string) => {
    dispatch({ type: "SET_ACTIVE_ROOM", payload: room });
  };

  const handleTyping = (typing: boolean) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      if (typing) {
        if (!typingTimeoutRef.current[state.currentUser]) {
          socketRef.current.send(
            JSON.stringify({
              type: "typing",
              sender: state.currentUser,
            }),
          );
        }
      } else {
        socketRef.current.send(
          JSON.stringify({
            type: "stop_typing",
            sender: state.currentUser,
          }),
        );
      }
    }
  };

  return (
    <Layout>
      <div className="flex h-screen overflow-hidden">
        <Sidebar activeRoom={state.activeRoom} changeRoom={changeRoom} />

        <div className="flex flex-col flex-1 bg-gray-50">
          <main className="flex-1 overflow-auto p-6">
            <MessageList
              messages={state.messages}
              currentUser={state.currentUser}
              typingUsers={typingUsers}
            />
          </main>
          <footer className="bg-white p-4 shadow-md border-t-2">
            <MessageInput onSend={sendMessage} onTyping={handleTyping} />
          </footer>
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;
