import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Feed from "./pages/Feed";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' index element={<Feed />}></Route>
        <Route path={`/login/`} element={<Login />}></Route>
        <Route path={`/register`} element={<Register />}></Route>
      </Routes>
    </BrowserRouter>
  );
}
