import React, { useEffect, useState } from 'react'
import Layoutwrap from '../Layout/Layoutwrap'
import { Search } from 'lucide-react'
import McpCard from '../components/McpCard'


const McpPage: React.FC = () => {

    useEffect(() => {
        document.title = "Models"
    }, [])
    
    const [inputvalue, setinputvalue] = useState<string>('')

    return (
        <Layoutwrap>
            <div className='w-full overflow-y-auto mb-4'>
                <div className='py-4 w-full px-6'>
                    <div
                        className="flex items-center justify-self-end border w-80 pr-3 gap-2 bg-white border-gray-500/30 h-[46px] rounded-[5px]"
                    >
                        <input
                            className="w-full h-full pl-5 outline-none placeholder-gray-500 text-sm"
                            placeholder="Search for model"
                            value={inputvalue}
                            onChange={(e: { target: { value: React.SetStateAction<string> } }) => setinputvalue(e.target.value)}
                            type="text"
                        />
                        <Search className='text-gray-600 cursor-pointer' />
                    </div>
                </div>
                <div className="grid xs:grid-cols-1 max-h-screen sm:grid-cols-2 md:grid-cols-3 gap-2 px-6 py-4 mx-auto w-full">
                    <McpCard inputvalue={inputvalue} />
                </div>
            </div>
        </Layoutwrap>

    )
}

export default McpPage