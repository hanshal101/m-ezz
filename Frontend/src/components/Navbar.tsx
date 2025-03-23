import { Settings, Menu } from 'lucide-react';
import React, { useContext } from 'react';
import { context } from '../Layout/Context';

export const Navbar: React.FC = () => {

     const {isOpen , toggle_sidebar} = useContext(context)

    return (

        <React.Fragment>

            <header className="bg-white border-b border-gray-200 p-4">
                <div className="max-w-5xl mx-auto flex justify-between items-center">
                    <button className="visible text-gray-600 hover:text-gray-800 md:hidden" onClick={() => toggle_sidebar()}>
                        <Menu />
                    </button>
                    <h1 className="text-xl font-semibold text-cyan-700">{"Perplexity".toUpperCase()}</h1>
                    <button className="text-gray-600 hover:text-gray-800">
                        <Settings />
                    </button>
                </div>
            </header>          

        </React.Fragment>
    );
};
