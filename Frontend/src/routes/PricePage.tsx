import React, { useEffect } from 'react'
import PriceCard from '../components/PriceCard'
import Layoutwrap from '../Layout/Layoutwrap'

const PricePage: React.FC = () => {

    useEffect(() => {
        document.title = "Pricing"
    }, [])


    return (
        <Layoutwrap>
            <div className="relative isolate px-6 py-6 md:py-18 lg:px-8 w-full overflow-y-auto">
                <div className="mx-auto max-w-4xl text-center">
                    <h2 className="text-base/7 font-semibold text-indigo-600">Pricing</h2>
                    <p className="mt-2 text-2xl font-semibold text-slate-700 tracking-tight text-balance sm:text-5xl">Choose the right plan for you</p>
                </div>
                <div className="mx-auto mt-10 grid grid-cols-1 items-center gap-y-6 sm:mt-10 gap-x-4 sm:gap-y-3 max-w-6xl lg:max-w-5xl lg:grid-cols-3  md:grid-cols-2">
                    <PriceCard />
                    <PriceCard />
                    <PriceCard />
                </div>
            </div>
        </Layoutwrap>
    )
}

export default PricePage