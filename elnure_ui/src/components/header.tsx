import { useEffect, useState } from "react";
import { Navigate } from "react-router";
import { post } from "src/api";

const Header = () => {
  const [isLoggedOut, setIsLoggedOut] = useState<boolean>(false);

  useEffect(() => {
    if (isLoggedOut) {
      post("logout");
    }
  }, [isLoggedOut])

  const logout = () => {
    localStorage.removeItem("user")
    localStorage.removeItem("appwindow")
    setIsLoggedOut(true);
  }

  if (isLoggedOut) {
    return <Navigate to="/login"/>
  }

  return (
      <nav className="navbar navbar-dark bg-dark">
        <ul className="navbar-nav ml-auto">
          <li><img onClick={logout} src="../../../logout-xxl.png" width="30" height="30"className="d-inline-block align-top" alt="Logout Logo"/></li>
        </ul>
      </nav>
  )
};

export default Header;
