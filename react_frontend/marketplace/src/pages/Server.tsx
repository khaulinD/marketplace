import useWebsocket from "react-use-websocket"
import { useEffect, useState } from "react";
import axios from "axios";

const socketUrl = "ws://127.0.0.1:8000/chat/1"

const Server = () => {
    const [newMessage, setNewMessage] = useState<string[]>([])
    const [message, setMessage] = useState("")
    // Define inputValue state if needed
    // const [inputValue, setInputValue] = useState("")

    const { sendJsonMessage } = useWebsocket(socketUrl, {
        onOpen: () => {
            console.log("connect")
        },
        onClose: () => {
            console.log("Close")
        },
        onError: () => {
            console.log("Error")
        },
        onMessage: (msg: any) => {
            const data = JSON.parse(msg.data);
            setNewMessage(prev_msg => [...prev_msg, data.new_message])
        }
    })

    const login = async (username: string, password: string): Promise<number | void> => {
        try {
            const response = await axios.post(
                `http://127.0.0.1:8000/api/token/`,
                {
                    username,
                    password,
                },
                { withCredentials: true }

            );
            console.log(response)
            // Handle successful login here
            console.log("Login successful");
        } catch (err: any) {
            if (err.response.status === 403) {
                console.log("verify email or create account")
            }
            return err.response.status;
        }
    };

    return (<div>
        <div>
            Recived Data: {newMessage.map((msg, index) => {
                return (
                    <div key={index}><p>{msg}</p></div>
                )
            })}
            <form>
                <label> Enter msg:
                    <input type="text" value={message} onChange={(e) => {
                        setMessage(e.target.value)
                    }}></input>
                </label>
            </form>
            <button onClick={() => {
                sendJsonMessage({ type: "message", message })
            }}>
                send
            </button>

            {/* Call login function when the button is clicked */}
            <button onClick={() => login("a", "1234")}>
                login
            </button>
        </div>
    </div>)
}

export default Server
