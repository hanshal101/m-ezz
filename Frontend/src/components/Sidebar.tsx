import { ArrowLeft, ArrowRight, Home, Info, MessageCircle } from 'lucide-react'
import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { context } from '../Layout/Context'
import { Closebar } from './Closebar'
import Openbar from './Openbar'


const Sidebar: React.FC = () => {
    const {isOpen , toggle_sidebar} = useContext(context)

    const [md_sidebar, setmd_sidebar] = useState(false)

    const md_togglebar = () => {
        setmd_sidebar(!md_sidebar)
    }

    const icon = {
        0: <Home />,
        1: <Info />,
        2: <MessageCircle />
    }

    return (

        <aside
            className={`w-full ${md_sidebar ? 'md:w-64' : 'md:w-20'} p-4 transition-transform transform space-y-2 h-screen z-10 ${isOpen ? 'translate-x-0 absolute h-screen' : '-translate-x-full absolute h-screen'
                } md:translate-x-0 md:relative`} style={{ "backgroundColor": "oklch(96.3% 0.007 106.523 / 1)" }}
        >
            <div className='mb-5'>
                {md_sidebar && <Closebar /> || <Openbar />}
            </div>
            <div className={`flex ${md_sidebar ? 'justify-between' : 'justify-center'}`}>
                <span className='font-bold text-gray-600 text-xl mb-4'>{md_sidebar && 'Menu'}</span>
                <ArrowLeft className={`mt-1  text-gray-600 bg-gray-300 rounded-full ${!md_sidebar && 'hidden'}`} onClick={md_togglebar} />
                {!md_sidebar && <ArrowRight size={30} className='mt-1 p-1 text-gray-600 bg-gray-300 rounded-full mb-6' onClick={md_togglebar} />}
            </div>
            <nav className="flex flex-col gap-4 pt-2">
                {['Home', 'About', 'Chat'].map((list, index) => (
                    <Link onClick={()=>toggle_sidebar()} key={index} to={list == "Home" ? '/' : `/${list}`} className={`flex items-center gap-2 text-cyan-800 hover:rounded-r-4xl hover:bg-gray-200 py-2 w-full ${!md_sidebar && 'justify-center'}`}>
                        {Object.values(icon)[index]} {md_sidebar && list}
                    </Link>
                ))}
            </nav>
        </aside>

    )
}

export default Sidebar