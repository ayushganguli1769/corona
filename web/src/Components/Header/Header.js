import React from 'react'
import { useUserDispatch, signOut } from "../../Context/UserContext";
// import './style.css'

function Header(props) {
  var userDispatch = useUserDispatch();

  return (
    <div>
        <nav id="navbar-example2" class="navbar navbar-light" style={{backgroundColor: "#1976d2", color: "white", padding:"2.5vh", boxShadow: "2px 2px 8px #888888"}}>
            <a class="navbar-brand" style ={{color:"white"}} href="#">MI19 Admin Panel</a>
            <ul class="nav nav-pills">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Admin &nbsp;&nbsp;&nbsp;&nbsp;</a>
                <div class="dropdown-menu">
                  <div class="dropdown-menu"></div>
                  <a class="dropdown-item" onClick={() => signOut(userDispatch, props.history)} style={{cursor:"default"}}><i class="fa fa-sign-out"/> Logout</a>
                </div>
              </li>
            </ul>
        </nav>
    </div>
  )
}

export default Header
