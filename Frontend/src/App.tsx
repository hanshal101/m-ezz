import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import ChatPage from './routes/ChatPage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { context } from './Layout/Context';
import About from './routes/About';
import Home from './routes/Home';
import McpPage from './routes/McpPage';
import PricePage from './routes/PricePage';

const App: React.FC = () => {

  const [isOpen, setIsOpen] = useState(false)

  const toggle_sidebar = () => {
    setIsOpen(!isOpen)
  }

  return (
    <>
      <context.Provider value={{ isOpen, toggle_sidebar }}>
        <BrowserRouter>
          <Navbar />
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='/chat' element={<ChatPage />} />
            <Route path='/About' element={<About />} />
            <Route path='/mcp' element={<McpPage />} />
            <Route path='/pricing' element={<PricePage />} />
          </Routes>
        </BrowserRouter>
      </context.Provider>
    </>
  );
};

export default App
