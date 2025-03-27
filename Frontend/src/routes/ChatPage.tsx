import { Send, Copy, Mic } from 'lucide-react';
import React, { useRef, useEffect, useState } from 'react';
import Openbar from '../components/Openbar';
import Layoutwrap from '../Layout/Layoutwrap';
import SkeletonLoader from '../components/SkeletonLoader';

const ChatPage: React.FC = () => {

    const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        document.title = "Ask AI"
    }, [])

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (!inputValue.trim()) return;

        setMessages([...messages, { role: 'user', content: inputValue }]);
        setInputValue('');

        setIsLoading(true);
        setTimeout(() => {
            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: `This is a simulated response to: "${inputValue}". In a real application, this would be replaced with an actual API call to OpenAI or another service.`
                }
            ]);
            setIsLoading(false);
        }, 1000);
    };

    return (
        <React.Fragment>
            <Layoutwrap>
                <div className="flex flex-col flex-grow items-center">
                    <div className={`flex-1 w-full px-4 overflow-y-auto ${messages.length && 'md:py-4'}`}> {/* mb-26 */}
                        {!messages.length && (
                            <div className="min-h-screen max-w-2xl mx-auto text-center flex flex-col items-center justify-center w-full space-y-3">
                                <span><Openbar /></span>
                                <h1 className='text-2xl text-gray-700 md:text-4xl font-semibold'>How can I assist you?</h1>
                                <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Illo suscipit ab, dolor tempora quos ut velit sint deleniti saepe et.</p>
                            </div>
                        )}
                        <div className={`max-w-3xl mx-auto space-y-1 md:space-y-4 ${messages.length && 'mb-32 md:mb-38'}`}>  {/* mb-26 */}
                            {messages.map((message, index) => (
                                <div key={index} className={`flex ${message.role === 'user' ? 'justify-start font-bold text-2xl text-gray-600' : 'justify-start'}`}>
                                    {message.role === 'assistant' ? (
                                        <div className="border-gray-300 px-4 md:px-4 w-full">
                                            <h3 className="font-semibold text-md underline underline-offset-13">Answer</h3>
                                            <p className="text-gray-800 mt-2 border-t border-gray-400 pt-3 mb-4">
                                                {message.content.charAt(0).toUpperCase() + message.content.slice(1).toLowerCase()}
                                            </p>
                                            <div className='flex justify-between items-center'>
                                                <span><Copy size={15} /></span>
                                            </div>
                                        </div>
                                    ) : (
                                        <div className={`px-2 py-2 flex ${message.content.length > 20 ? 'items-start' : 'items-center'} w-full justify-start space-x-1.5`}>
                                            <span className={`${message.content.length > 20 && 'w-25'}`}>{message.content && <Openbar />}</span>
                                            <span className="text-xl md:text-2xl">{message.content.charAt(0).toUpperCase() + message.content.slice(1).toLowerCase()}</span>
                                        </div>
                                    )}
                                </div>))}
                            {isLoading && (
                                <SkeletonLoader />
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    </div>

                    <form onSubmit={handleSubmit} className="fixed bottom-0 mx-auto w-full max-w-3xl py-3 px-2 md:px-0">
                        <div className="relative flex items-center">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={handleInputChange}
                                placeholder="Type your message here..."
                                className="flex-grow shadow-sm p-3 md:p-4 pl-4 pr-24 bg-white border border-gray-400 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <button
                                // onClick={props.startlistening}
                                // d`isabled={props.disablelistening}
                                className={`absolute right-13 p-3 text-gray-600 rounded-lg`}
                            >
                                <Mic size={20} />
                            </button>
                            <button
                                type="submit"
                                disabled={!inputValue.trim() || isLoading}
                                onClick={() => handleSubmit}
                                className={`absolute right-4 p-3 rounded-lg ${!inputValue.trim()}`}
                            >
                                <Send size={18} />
                            </button>
                        </div>
                        <div>
                            <p className='text-xs text-center pt-1'>M-Ezz can make mistakes. Check important info.</p>
                        </div>
                    </form>
                </div>
            </Layoutwrap>
        </React.Fragment>
    );
}

export default ChatPage;
