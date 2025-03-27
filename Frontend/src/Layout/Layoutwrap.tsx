import React from 'react'
import Sidebar from '../components/Sidebar'

interface LayoutWrapperProps extends React.PropsWithChildren { }

const Layoutwrap: React.FC<LayoutWrapperProps> = ({ children }) => {
    return (
        <div className="flex flex-col md:flex-row w-full h-screen">

            <Sidebar />
            {children}

        </div>
    )
}

export default Layoutwrap