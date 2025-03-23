import React, { useEffect } from "react";
import Layoutwrap from "../Layout/Layoutwrap";
import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";

const Home: React.FC = () => {

    useEffect(() => {
        document.title = "Home"
    }, [])

    return (
        <Layoutwrap>

            {/* Dummy Home Page */}

            <section className="bg-white dark:bg-gray-900 w-full">
                <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16 lg:px-12">
                    <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-700 md:text-5xl lg:text-6xl dark:text-white">Empowering Conversations with AI</h1>
                    <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 xl:px-48 dark:text-gray-400">Experience the future of communication with our intelligent AI assistant—where innovation meets seamless interaction, unlocking insights and enhancing conversations effortlessly.</p>
                    <div className="flex w-fit mx-auto flex-col mb-8 lg:mb-16 space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                        <Link to="/chat" className="inline-flex justify-center gap-2 items-center py-3 px-5 text-base font-medium text-center rounded-lg bg-cyan-700 text-white hover:bg-cyan-800">
                            Get Started <ArrowRight size={18}/>
                        </Link>
                    </div>
                </div>
            </section>
        </Layoutwrap>
    );
};

export default Home;
