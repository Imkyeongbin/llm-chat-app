// frontend/src/App.js

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null); // 채팅창 스크롤을 위한 ref

  // 메시지 배열이 업데이트될 때마다 맨 아래로 스크롤
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { sender: 'user', text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // 백엔드 API(FastAPI)에 요청
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: input,
      });

      const botMessage = { sender: 'bot', text: response.data.reply };
      setMessages((prevMessages) => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = { sender: 'bot', text: '죄송합니다, 응답을 가져오는 중 오류가 발생했습니다.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LLM 채팅 데모 (React + FastAPI)</h1>
      </header>
      <main className="chat-container">
        <div className="message-list">
          {messages.map((msg, index) => (
            <div key={index} className={`message-bubble ${msg.sender}`}>
              <p>{msg.text}</p>
            </div>
          ))}
          {isLoading && (
            <div className="message-bubble bot loading">
              <div className="spinner"></div>
            </div>
          )}
          {/* 스크롤 대상이 될 빈 div */}
          <div ref={messagesEndRef} />
        </div>
        <form onSubmit={handleSubmit} className="message-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="메시지를 입력하세요..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            전송
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;