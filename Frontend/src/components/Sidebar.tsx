import { ArrowLeft, ArrowRight, Box, Home, Info, MessageCircle, UserCircle } from 'lucide-react'
import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { context } from '../Layout/Context'
import { Closebar } from './Closebar'
import Openbar from './Openbar'
import image from '../assets/image/mcp_logo.jpg'

const Sidebar: React.FC = () => {
    const { isOpen, toggle_sidebar } = useContext(context) ?? {};

    const [md_sidebar, setmd_sidebar] = useState<boolean>(false)

    const md_togglebar = () => {
        setmd_sidebar(!md_sidebar)
    }

    const icon = {
        0: <Home />,
        1: <Info />,
        2: <MessageCircle />,
        3 : <Box/>
    }

    return (

        <aside
            className={`w-full ${md_sidebar ? 'md:w-64' : 'md:w-20'} bg-b; flex flex-col md:justify-between p-4 transition-transform transform space-y-2.5 absolute h-screen z-10 ${isOpen ? 'translate-x-0' : '-translate-x-full'
                } md:translate-x-0 md:relative`} style={{ "backgroundColor": "oklch(96.3% 0.007 106.523 / 1)" }}
        >
            <div>
                <div className='mb-5'>
                    <Link to={'/'}>{md_sidebar && <Closebar /> || <Openbar />}</Link>
                </div>
                <div className={`flex ${md_sidebar ? 'justify-between' : 'justify-center'}`}>
                    <span className='font-bold text-gray-600 text-xl mb-4'>{md_sidebar && 'Menu'}</span>
                    <ArrowLeft className={`mt-1 cursor-pointer text-gray-600 bg-gray-300 rounded-full ${!md_sidebar && 'hidden'}`} onClick={md_togglebar} />
                    {!md_sidebar && <ArrowRight size={30} className='mt-1 p-1 cursor-pointer text-gray-600 bg-gray-300 rounded-full mb-6' onClick={md_togglebar} />}
                </div>
                <div className='mb-5' onClick={() => toggle_sidebar()}>
                    <Link to={'/mcp'} className={`flex gap-2 items-center ${md_sidebar && 'bg-amber-200 py-2 rounded-full pl-2'}`}><img src={image} alt="" className={`mix-blend-multiply ${md_sidebar && 'w-8' || 'w-15 mx-auto'}`} />{md_sidebar && 'MCP'}</Link>
                </div>
                <nav className="flex flex-col gap-4 pt-2">
                    {['Home', 'About', 'Chat' , 'Pricing'].map((list, index) => (
                        <Link onClick={() => toggle_sidebar()} key={index} to={list == "Home" ? '/' : `/${list}`} className={`flex items-center gap-2 text-cyan-800 hover:rounded-r-4xl hover:bg-gray-200 py-2 w-full ${!md_sidebar && 'justify-center'}`}>
                            {Object.values(icon)[index]} {md_sidebar && list}
                        </Link>
                    ))}
                </nav>
            </div>
            <div className={`flex gap-3 ${!md_sidebar && 'justify-center'} md:pt-0 pt-3`}>
                <UserCircle/>{md_sidebar && 'Paresh'}
            </div>

        </aside>

    )
}

export default Sidebar