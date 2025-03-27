import React, { useEffect } from "react";
import Layoutwrap from "../Layout/Layoutwrap";

const About: React.FC = () => {
    
    useEffect(() => {
        document.title = "About";
    }, []);

    return (
        <Layoutwrap>

            {/* Dummy About Page */}

            <div className="w-full min-h-screen flex flex-col items-center pt-20 relative px-2 text-center">

                <h1 className="text-4xl md:text-6xl font-extrabold text-gray-600 bg-clip-text ">
                    About Perplexity AI
                </h1>

                <p className="text-lg md:text-xl text-gray-300 text-center max-w-3xl mt-4">
                    Perplexity AI is revolutionizing the way we interact with knowledge. Our generative AI models process vast amounts of data to provide real-time insights, answering complex queries with precision and accuracy.
                </p>
            </div>
        </Layoutwrap>
    );
};

export default About;
