import { useReducer, useEffect, useRef } from 'react';
import { jwtDecode } from 'jwt-decode';
import MessageList from '../components/MessageList';
import MessageInput from '../components/MessageInput';
import Sidebar from '../components/Sidebar';
import Layout from '../components/Layout';

interface Message {
  user: string;
  content: string;
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
  activeRoom: '',
  currentUser: '',
  rooms: [],
};

const reducer = (state: State, action: Action) => {
  switch (action.type) {
    case 'SET_MESSAGES':
      return { ...state, messages: action.payload };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.payload] };
    case 'SET_ACTIVE_ROOM':
      return { ...state, activeRoom: action.payload, messages: [] };
    case 'SET_CURRENT_USER':
      return { ...state, currentUser: action.payload };
    case 'SET_ROOMS':
      return { ...state, rooms: action.payload };
    default:
      return state;
  }
};

const ChatPage: React.FC = () => {
  const [state, dispatch] = useReducer(reducer, initialState);
  const socketRef = useRef<WebSocket | null>(null);
  const historySocketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const getToken = () => {
      const token = localStorage.getItem('access');
      if (token) {
        const decoded: any = jwtDecode(token);
        dispatch({ type: 'SET_CURRENT_USER', payload: decoded.username || 'default_user' });
      }
    };

    getToken();
  }, []);

  useEffect(() => {
    const setupWebSocket = () => {
      if (!state.activeRoom) return;
      const WEBSOCKET_BASE_URL = import.meta.env.WEBSOCKET_BASE_URL || 'ws://localhost:8000/ws/chat'
      const WEB_SOCKET_URL = `${WEBSOCKET_BASE_URL}/${state.activeRoom}/?token=${localStorage.getItem('access')}`;
      const HISTORY_SOCKET_URL = `${WEBSOCKET_BASE_URL}/history/${state.activeRoom}/?token=${localStorage.getItem('access')}`;

      if (socketRef.current) {
        socketRef.current.close();
      }
      if (historySocketRef.current) {
        historySocketRef.current.close();
      }

      socketRef.current = new WebSocket(WEB_SOCKET_URL);

      socketRef.current.onopen = () => {
        console.log(`WebSocket bağlantısı açıldı: ${state.activeRoom}`);
        joinRoom(state.activeRoom);
      };

      socketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);

        if (data.type === 'chat_message') {
          dispatch({ type: 'ADD_MESSAGE', payload: { user: data.user, content: data.message } });
        }
      };

      socketRef.current.onclose = () => {
        console.log(`WebSocket bağlantısı kapandı: ${state.activeRoom}`);
      };

      historySocketRef.current = new WebSocket(HISTORY_SOCKET_URL);

      historySocketRef.current.onopen = () => {
        console.log(`WebSocket geçmişi bağlantısı açıldı: ${state.activeRoom}`);
        getMessageHistory();
      };

      historySocketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'chat_history') {
          dispatch({ type: 'SET_MESSAGES', payload: data.messages });
        }
      };

      historySocketRef.current.onclose = () => {
        console.log(`WebSocket geçmişi bağlantısı kapandı: ${state.activeRoom}`);
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
    };
  }, [state.activeRoom]);

  const sendMessage = (message: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const newMessage = { sender: state.currentUser, content: message };
      socketRef.current.send(JSON.stringify(newMessage));
      dispatch({ type: 'ADD_MESSAGE', payload: newMessage });
    }
  };

  const joinRoom = (room: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type: 'join_room', room }));
    }
  };

  const getMessageHistory = () => {
    if (historySocketRef.current && historySocketRef.current.readyState === WebSocket.OPEN) {
      historySocketRef.current.send(JSON.stringify({ type: 'get_message_history' }));
    }
  };

  const changeRoom = (room: string) => {
    dispatch({ type: 'SET_ACTIVE_ROOM', payload: room });
  };

  return (
    <Layout>
      <div className="flex h-screen overflow-hidden">
        <Sidebar activeRoom={state.activeRoom} changeRoom={changeRoom}/>

        <div className="flex flex-col flex-1 bg-gray-50">
          <main className="flex-1 overflow-auto p-6">
            <MessageList messages={state.messages} currentUser={state.currentUser} />
          </main>
          <footer className="bg-white p-4 shadow-md border-t-2">
            <MessageInput onSend={sendMessage} />
          </footer>
        </div>
      </div>
    </Layout>
  );
};

export default ChatPage;
