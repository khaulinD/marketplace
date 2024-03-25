
import { Route, Routes, BrowserRouter } from "react-router-dom";
import Server from "./pages/Server.tsx";
import Auth from "./pages/Auth.tsx";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/chat/:id"  element={<Server />}/>
        <Route path="/login"  element={<Auth />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App
