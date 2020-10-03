import React, { useState } from 'react'
import { useUserDispatch, loginUser } from "../Context/UserContext";

function Login(props) {
    var userDispatch = useUserDispatch();
    var [isLoading, setIsLoading] = useState(false);
    var [error, setError] = useState(null);
    // var [activeTabId, setActiveTabId] = useState(0);
    // var [nameValue, setNameValue] = useState("");
    var [loginValue, setLoginValue] = useState("");
    var [passwordValue, setPasswordValue] = useState("");
    return (
      <div className="container" style={{paddingTop: "100px",maxWidth:"400px",display:"flex",flexDirection:"row"}}>
        
        <br/>
        <br/>
        <br/>
        {
          (error) ? <div class="alert alert-danger" role="alert">Login failure</div> : null
        }
        <div class="card">
            <div class="card-header">
              MI19 Admin Panel
            </div>
          <div class="card-body">
            <form>
              <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="text" value={loginValue} onChange={(e) => setLoginValue(e.target.value)} class="form-control" id="exampleInputEmail1" />
                {/* <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small> */}
              </div>
              <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input type="password" value={passwordValue} onChange={(e) => setPasswordValue(e.target.value)} class="form-control" id="exampleInputPassword1"/>
              </div>
              <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="exampleCheck1"/>
                <label class="form-check-label" for="exampleCheck1">Check me out</label>
              </div>
              <button type="submit" onClick={() => loginUser(userDispatch,loginValue,passwordValue,props.history,setIsLoading,setError,)} class="btn btn-primary">Submit</button>
            </form>
          </div>
        </div>
      </div>
    )
}

export default Login;