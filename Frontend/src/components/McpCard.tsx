import { X } from "lucide-react";
import React, { useState } from "react";

const McpCard: React.FC = (props) => {

    const dummyjson = [
        {
            "id": 1,
            "title": "Gmail",
            "description": "Like so many organizations these days, Autodesk is a company in transition. It was until recently a traditional boxed software company selling licenses.",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAABFFBMVEX////qQjVChfQ1qFP6uwDFIhz09f7z9/RIh/Q8qVgyfvPK5NAgo0bI2Pv7vwDqPTbdNy7vcSvqPjBunfZnuHnpOCnGLCf6vBf/+fP59PPpMiHBAAD/uwDvhoHpLhv1uLb0r6zFHhTrT0X52tnrWE/64uHueXP47u7RbWvJRkP6wDz94bbrWVDrU0k0iPzHGQCTtWPltLPUeHfHOjbJQz/OW1jbl5bu0dH+7M/81pP7xlH6viv7zXL83an7yWX+7tnpxMP95b7+9Of+7NH5zbTuZhBljO2/VmntvkZmr2SocKLJu1mEhNLNNye8WXHOj6jWoYNSsGicuPiZyqLf5vze7OCyx/mv1bePr/eLxJZ+pfZ4vYYkSi6sAAAFr0lEQVR4nO2ba3vTNhxHraTpoIQxDE6bS5OmIU0v0DtlkNJCNxiD3YCN3b7/95jdOE3iSNbfsuRIe37nBS9lzqMTXRLX8wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUKM+GAzqi/5PeN7a1dqagWEHR8c7J7VK7fTp2TMDw1P59vmL3dWl1eHu+Z5ey/52t9ntdiuV8J9m8+RI6+B0Xg5bS2NaSxeX2gYebDdDuQndZu2VtsHpvF6d+I0kLzTN46tKs5Kg2zwu+gO5dp7wu+a1jqHPZicwprnT1zE4matdnuBS62X+oc/mJnA8jUV+Gve4fpHi87xDHwkEo2ksrlRuobHiXr6hBxVeogWXeskvdMxVrsG3xVNYWKnCQmMu8gz+LFXwulRdHkJSCo07/S7H6E9TGo0VT82Werkr8Qt5oT58XTaFUaldk6V+L/cLJ1F9409ZSKdor2tUmmX9zdcUQ/VN8Zhk+E2waabU/mZwn2K4dK78iFPpx/DakPlBR6PYmI7v36MZDpWfUSMaMtbQX+p6gzGi4arqM+p0Q6a71P6TgNENVZeaeo0iODLUXGon8JlthlpLjQq10JAFj/SU2n8cMDsNmd/QUWqn4TNbDRnTsPuvtyfDWWjIgsf5Sp0UaqthzjU1XkOtNsxV6nShFhsqlzpbqM2GiqWG59DkQNYaKpWaLNRyw7DUXqZnzRdqu2HGUhNrqBOGmc6p43OoY4YseEJbU0c3pUUYLu8c5DIklioolG7YGiobvv2Boig2JJUqKpRs2Hr341eqhqX99wfya36aobRUcaFUw9aH8m1lw1ul/Z9OpNOYasj8dlqpnbawUJpha3hYzmVY2peXmm4YlSr6jaqeVijJMCy0nNOwVLolK1VmKLz79x+lFUoxbH24Xc5vKC1VaigoVVKo3PC6UB2GslLlhrxSpYVKDUeFajGUlEoxnCuVfw7NYhgXqskwLPVn4TSSDBO7f8ouTzQcF6rLMCz1F5EizTC6Ud2UyrspZTKcFKrNMKVUquHN7i9fQ2WGU4VqNBSWSjZkvh+VyrnLZzRcPSyXTRiK1lS64XWp1EKFhrOFajUUlJrFkAUNaqEiw0Shmg25u38mw2xwDIeHST+9hrxSizScL1S7YWn+RlWgIadQA4ZzpRZm2OIVasIwWWpRhvxCjRgmSi3IMLzLizBgOFNqIYbCQk0ZTp9TizAUF2rMMGRcagGGgjXUtOG4VOOGqYWaNByXatowvVCjhvE51bChpFDDhmGptQOzhrJCTRtGuz/hGyVlwzfvPsoFzRqGjr/SvnNRwPd/I/gZN1y529vMcuejE2z27lStMPS8LROlNrY8zxpDb0N7qX6w4dlk6OkuNSzUs8vQq29l+IZJSntr9N2qTYY6Sx0Vap+htlLjQi001FTquFAbDcNSG3lL9RsbU+PZZ5i71KlCLTUMS82z+ze2Zn9JtdEwLFX+67UAv72RGMtOQ+VSE4VabEj7jX6OZKE2G6qsqbNrqP2GXo9lKzVg3DduLTZMfyNvjuim5JxhhnPq5BzqliF5TeWsoY4YEnd/3hrqiiGlVHGhbhh6vdQ3ZKN3bFL/asEBQ8mNqp1SqCuGabs/f5d3z1BYqqRQhww9/ntQskJdMuSVOn9TcttwbvdP2eUdNUysqZRCXTOcLlW+hrppeFMqsdAIxwzj36hENyUezhmG59SAXGiEe4ZeL9tfzzpomBEYwlACDGGoARjCUAIMYagBGMJQAgxhqAEYwlACDN039JwxVB7/rSOGH5XH/7TihGH1s/L4vzti+If6Ax44YfgwxwMok7hwwzxT6Hlf5IqLNqz+me8R8sVmwYY5lpmYLysSx4UaVvPOYMTyX6VUycUZVqvlv5VPMzMs3/30zwMxRg0fivn38x09fgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/J/4D2zvGK6VGtwBAAAAAElFTkSuQmCC",
            "active": true
        },
        {
            "id": 2,
            "title": "Outlook",
            "description": "Microsoft Outlook is a personal information manager software system from Microsoft, available as a part of the Microsoft Office suite.",
            "image": "data:image/jpeg;base64,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",
            "active": false
        },
        {
            "id": 3,
            "title": "Slack",
            "description": "Slack is a messaging app for businesses that connects people to the information they need. Slack transforms communication into a more productive workspace.",
            "image": "data:image/png;base64,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",
            "active": true
        },
    ]

    const [isEnabled, setIsEnabled] = useState<{ [key: number]: boolean }>(
        dummyjson.reduce((acc, data) => {
            acc[data.id] = data.active;
            return acc;
        }, {} as { [key: number]: boolean })
    );

    const toggleSwitch = (id: number) => {
        setIsEnabled((prev) => ({
            ...prev,
            [id]: !prev[id],
        }));
    };


    const filteredCards = dummyjson.filter((card) =>
        card.title.toLowerCase().includes(props.inputvalue || '')
    );


    return (
        <>
            {filteredCards.length > 0 && (
                filteredCards.map((data) => (
                    <div key={data.id} className=" shadow-md border border-slate-200 p-5 rounded-lg bg-white">
                        <div className="flex flex-col gap-4 md:flex-row items-center">
                            <div className="shrink-0 overflow-hidden">
                                <img
                                    src={data.image}
                                    alt={data.title}
                                    className="rounded-full w-20 h-20 md:w-24 md:h-24"
                                />
                            </div>

                            <div className="text-center md:text-left">
                                <h4 className="mb-2 text-slate-700 text-xl font-semibold">{data.title}</h4>
                                <p className="mb-4 text-slate-600 leading-normal font-light">
                                    {data.description}
                                </p>
                            </div>
                        </div>

                        <div className="flex justify-between items-center mt-4">
                            <span className="flex items-center text-sm font-medium text-gray-900">
                                <span
                                    className={`w-2.5 h-2.5 rounded-full mr-1.5 ${isEnabled ? "bg-teal-500" : "bg-gray-400"}`}
                                ></span>
                                {isEnabled[data.id] ? "Active" : "Inactive"}
                            </span>

                            <label className="cursor-pointer flex items-center">
                                <input type="checkbox" value="" className="absolute w-0 h-0 peer" onChange={() => toggleSwitch(data.id)} />
                                <div className="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600 dark:peer-checked:bg-blue-600"></div>
                                <span className="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300"> {isEnabled[data.id] ? "Enabled" : "Disabled"}</span>
                            </label>
                        </div>
                    </div>

                )))
                ||
                <div className="p-4 mb-4 text-sm flex items-center gap-2 text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                    <span className="font-medium"><X /></span> No Models Found
                </div>
            }
        </>
    );
};

export default McpCard;
