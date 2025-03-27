import { Menu } from 'lucide-react';
import React, { useContext } from 'react';
import { context } from '../Layout/Context';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {

    const { toggle_sidebar } = useContext(context) ?? {};

    return (

        <React.Fragment>

            <header className="md:hidden visible bg-white border-b border-gray-200 p-4">
                <div className="max-w-5xl mx-auto flex justify-between items-center">
                    <button className="visible text-gray-600 hover:text-gray-800 md:hidden" onClick={() => toggle_sidebar}>
                        <Menu />
                    </button>
                    <Link to={'/'} className="text-xl font-semibold text-cyan-700">{"M-Ezz".toUpperCase()}</Link>
                </div>
            </header>

        </React.Fragment>
    );
};
