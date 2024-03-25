import axios from "axios";
import {useNavigate} from "react-router-dom";




const Auth = () => {
    const navigate = useNavigate()
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
            localStorage.setItem("id", response.data.user_id)
            // navigate("/chat/1")
        } catch (err: any) {
            if (err.response.status === 403) {
                console.log("verify email or create account")
            }
            return err.response.status;
        }
    };

    return (<div>
        <button onClick={()=>{
            login("a", "1234")
        }}>
            login
        </button>
    </div>)
}

export default Auth